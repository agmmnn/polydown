import asyncio
import hashlib
import os
import aiohttp
from dataclasses import dataclass
from typing import Optional, Tuple, Literal

@dataclass
class DownloadTask:
    url: str
    destination_folder: str
    filename: str
    md5: Optional[str] = None
    overwrite: bool = False

DownloadStatus = Literal["downloaded", "downloaded_ow", "skipped", "failed", "exists"]

class DownloadManager:
    def __init__(self, session: aiohttp.ClientSession, concurrency: int = 4):
        self.session = session
        self.semaphore = asyncio.Semaphore(concurrency)

    async def verify_md5(self, filepath: str, expected_md5: str) -> bool:
        if not expected_md5:
            return True

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._check_md5_sync, filepath, expected_md5)

    @staticmethod
    def _check_md5_sync(filepath: str, expected_md5: str) -> bool:
        if not os.path.exists(filepath):
            return False

        hasher = hashlib.md5()
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest() == expected_md5

    async def download(self, task: DownloadTask) -> Tuple[str, DownloadStatus, bool]:
        """
        Downloads a file.
        Returns: (filename, status, md5_verified)
        """
        filepath = os.path.join(task.destination_folder, task.filename)
        existed_before = os.path.exists(filepath)

        # Check if file exists and we should skip
        if existed_before and not task.overwrite:
            # Validate existing file
            is_valid = await self.verify_md5(filepath, task.md5) if task.md5 else True
            return task.filename, "exists", is_valid

        # Download needed (either didn't exist, or overwrite is True)
        async with self.semaphore:
            try:
                os.makedirs(task.destination_folder, exist_ok=True)
                async with self.session.get(task.url) as response:
                    response.raise_for_status()
                    data = await response.read()

                    # Write to file
                    loop = asyncio.get_running_loop()
                    await loop.run_in_executor(None, self._write_file_sync, filepath, data)

                # Verify
                is_valid = await self.verify_md5(filepath, task.md5) if task.md5 else True
                status = "downloaded_ow" if existed_before else "downloaded"
                return task.filename, status, is_valid

            except Exception as e:
                # In a real app we might log this
                return task.filename, "failed", False

    @staticmethod
    def _write_file_sync(filepath: str, data: bytes):
        with open(filepath, "wb") as f:
            f.write(data)
