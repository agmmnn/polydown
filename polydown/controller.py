import asyncio
import os
import aiohttp
from typing import List, Optional
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TaskID
)
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel

from .api import PolyHavenClient
from .downloader import DownloadManager, DownloadTask

console = Console()

class PolydownController:
    def __init__(self, concurrency: int = 4):
        self.concurrency = concurrency

    async def start(
        self,
        asset_type: str,
        category: Optional[str],
        folder: str,
        sizes: List[str],
        overwrite: bool,
        noimgs: bool,
        iters: Optional[int],
        tone: bool,
        fileformat: Optional[str],
    ):
        async with aiohttp.ClientSession() as session:
            client = PolyHavenClient(session)
            downloader = DownloadManager(session, concurrency=self.concurrency)

            # 1. Fetch Assets
            with console.status("[bold green]Fetching asset list...") as status:
                assets = await client.get_assets(asset_type, category)
                if iters:
                    assets = assets[:iters]
                console.log(f"Found {len(assets)} assets.")

            if not assets:
                return

            # 2. Process Assets & Build Tasks
            tasks: List[DownloadTask] = []

            # Limit metadata concurrency
            sem = asyncio.Semaphore(10)

            async def process_asset(asset_id):
                async with sem:
                    try:
                        files_data = await client.get_files(asset_id)
                        new_tasks = self._generate_tasks(
                            asset_type, asset_id, files_data, folder, sizes,
                            overwrite, noimgs, tone, fileformat
                        )
                        tasks.extend(new_tasks)
                    except Exception as e:
                        console.log(f"[red]Error fetching metadata for {asset_id}: {e}")

            with console.status("[bold green]Fetching file metadata...") as status:
                await asyncio.gather(*[process_asset(asset) for asset in assets])

            console.log(f"Generated {len(tasks)} download tasks.")

            if not tasks:
                console.print("[yellow]No files to download matching criteria.")
                return

            # 3. Execute Downloads
            await self._execute_downloads(tasks, downloader)


    async def _execute_downloads(self, tasks: List[DownloadTask], downloader: DownloadManager):
        queue = asyncio.Queue()
        for task in tasks:
            queue.put_nowait(task)

        results = {"downloaded": 0, "exists": 0, "failed": 0, "skipped": 0, "corrupted": 0}

        # UI Setup
        overall_progress = Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("({task.completed}/{task.total})"),
            TimeRemainingColumn(),
        )

        worker_progress = Progress(
            TextColumn("[bold green]{task.description}"),
            BarColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
        )

        progress_group = Group(
            Panel(overall_progress, title="Overall Progress", border_style="blue"),
            Panel(worker_progress, title="Worker Threads", border_style="green")
        )

        overall_task_id = overall_progress.add_task("Total Files", total=len(tasks))

        worker_task_ids = []
        for i in range(self.concurrency):
            tid = worker_progress.add_task(f"Worker {i+1}: Idle", visible=True, total=None)
            worker_task_ids.append(tid)

        async def worker(worker_id: int, task_id: TaskID):
            while True:
                try:
                    task = queue.get_nowait()
                except asyncio.QueueEmpty:
                    break

                worker_progress.update(task_id, description=f"Worker {worker_id+1}: {task.filename}", total=None, completed=0, visible=True)

                def progress_cb(chunk_size, total_size):
                    worker_progress.update(task_id, total=total_size, advance=chunk_size)

                filename, status, verified = await downloader.download(task, progress_cb)

                if status == "failed":
                    results["failed"] += 1
                elif status == "exists":
                    results["exists"] += 1
                else:
                    results["downloaded"] += 1

                if not verified:
                    results["corrupted"] += 1

                overall_progress.advance(overall_task_id)
                worker_progress.update(task_id, description=f"Worker {worker_id+1}: Idle", visible=True)
                queue.task_done()

        with Live(progress_group, console=console, refresh_per_second=10):
            workers = [
                asyncio.create_task(worker(i, worker_task_ids[i]))
                for i in range(self.concurrency)
            ]
            await asyncio.gather(*workers)

        # 4. Report
        console.print("\n[bold]Summary:[/bold]")
        console.print(f"[green]Downloaded: {results['downloaded']}")
        console.print(f"[yellow]Existing: {results['exists']}")
        console.print(f"[red]Failed: {results['failed']}")
        if results['corrupted'] > 0:
            console.print(f"[bold red]Corrupted (MD5 mismatch): {results['corrupted']}")


    def _generate_tasks(
        self,
        asset_type: str,
        asset_id: str,
        data: dict,
        root_folder: str,
        target_sizes: List[str],
        overwrite: bool,
        noimgs: bool,
        tone: bool,
        fileformat: Optional[str]
    ) -> List[DownloadTask]:
        tasks = []

        if asset_type == "hdris":
            # Data structure: data['hdri'][size][format]...
            available_sizes = data.get('hdri', {})

            for size, size_data in available_sizes.items():
                if target_sizes and size not in target_sizes:
                    continue

                formats_to_check = [fileformat] if fileformat else ['exr', 'hdr']

                for fmt in formats_to_check:
                    if fmt in size_data:
                        file_info = size_data[fmt]
                        url = file_info['url']
                        md5 = file_info.get('md5')
                        filename = url.split('/')[-1]

                        tasks.append(DownloadTask(
                            url=url,
                            destination_folder=root_folder,
                            filename=filename,
                            md5=md5,
                            overwrite=overwrite
                        ))

            # Images for HDRI
            if not noimgs:
                 tasks.extend(self._get_image_tasks(asset_type, asset_id, root_folder, overwrite, tone))

        else: # models, textures
            blend_data = data.get('blend', {})
            for size, content in blend_data.items():
                if target_sizes and size not in target_sizes:
                    continue

                # Subfolder logic
                asset_folder = os.path.join(root_folder, asset_id)
                size_folder = os.path.join(asset_folder, f"{asset_id}_{size}")
                textures_folder = os.path.join(size_folder, "textures")

                # Blend file
                if 'blend' in content:
                    b_info = content.get('blend', {})
                    if b_info:
                        url = b_info['url']
                        md5 = b_info.get('md5')
                        filename = url.split('/')[-1]

                        tasks.append(DownloadTask(
                            url=url,
                            destination_folder=size_folder,
                            filename=filename,
                            md5=md5,
                            overwrite=overwrite
                        ))

                        # Includes (textures)
                        includes = b_info.get('include', {})
                        for tex_key, tex_info in includes.items():
                            t_url = tex_info['url']
                            t_md5 = tex_info.get('md5')
                            t_filename = t_url.split('/')[-1]

                            tasks.append(DownloadTask(
                                url=t_url,
                                destination_folder=textures_folder,
                                filename=t_filename,
                                md5=t_md5,
                                overwrite=overwrite
                            ))

            # Images for Models/Textures
            if not noimgs:
                image_folder = os.path.join(root_folder, asset_id)
                tasks.extend(self._get_image_tasks(asset_type, asset_id, image_folder, overwrite, tone))

        return tasks

    def _get_image_tasks(self, asset_type, asset_id, folder, overwrite, tone):
        tasks = []
        imgs_dict = {}
        if asset_type == "hdris":
            imgs_dict = {
                "thumb": f"https://cdn.polyhaven.com/asset_img/thumbs/{asset_id}.png",
                "primary": f"https://cdn.polyhaven.com/asset_img/primary/{asset_id}.png",
                "renders_lone_monk": f"https://cdn.polyhaven.com/asset_img/renders/{asset_id}/lone_monk.png",
                "Tonemapped8K": f"https://dl.polyhaven.org/file/ph-assets/HDRIs/extra/Tonemapped%20JPG/{asset_id}.jpg",
            }
        elif asset_type == "textures":
            imgs_dict = {
                "primary": f"https://cdn.polyhaven.com/asset_img/primary/{asset_id}.png",
                "thumb": f"https://cdn.polyhaven.com/asset_img/thumbs/{asset_id}.png",
                "renders_clay": f"https://cdn.polyhaven.com/asset_img/renders/{asset_id}/clay.png",
            }
        elif asset_type == "models":
            imgs_dict = {
                "primary": f"https://cdn.polyhaven.com/asset_img/primary/{asset_id}.png",
                "renders_clay": f"https://cdn.polyhaven.com/asset_img/renders/{asset_id}/clay.png",
                "renders_orth_front": f"https://cdn.polyhaven.com/asset_img/renders/{asset_id}/orth_front.png",
                "renders_orth_side": f"https://cdn.polyhaven.com/asset_img/renders/{asset_id}/orth_side.png",
                "renders_orth_top": f"https://cdn.polyhaven.com/asset_img/renders/{asset_id}/orth_top.png",
            }

        for key, url in imgs_dict.items():
            if key == "Tonemapped8K" and not tone:
                continue

            ext = url.split('.')[-1]
            filename = f"{asset_id}_{key}.{ext}"

            tasks.append(DownloadTask(
                url=url,
                destination_folder=folder,
                filename=filename,
                md5=None,
                overwrite=overwrite
            ))
        return tasks
