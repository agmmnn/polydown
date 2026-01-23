import asyncio
import os
import aiohttp
from rich import print

from .controller import PolydownController
from .api import PolyHavenClient


def polycli(args):
    try:
        asyncio.run(_async_polycli(args))
    except KeyboardInterrupt:
        print("\n[yellow]Operation cancelled by user.[/yellow]")


async def _async_polycli(args):
    asset_type = args.asset_type[0]
    folder = args.folder
    overwrite = args.overwrite
    sizes = args.sizes
    category = args.category
    noimgs = args.noimgs
    iters = args.iters
    tone = args.tone
    fileformat = args.fileformat

    # Validation Phase
    async with aiohttp.ClientSession() as session:
        client = PolyHavenClient(session)

        # ->🔒asset type->
        try:
            asset_type_list = await client.get_asset_types()
        except Exception as e:
            print(f"[red]Error connecting to API: {e}[/red]")
            return

        if asset_type not in asset_type_list:
            print(f"'{asset_type}' is not a valid asset type!")
            return

        # ->🔒category->
        if category == "":
            try:
                js = await client.get_categories(asset_type)
                print(f"[green]There are {len(js)} available categories for {asset_type}:")
                print(js)
                return
            except Exception as e:
                print(f"[red]Error fetching categories: {e}[/red]")
                return
        elif category is not None:
            try:
                asset_category_list = await client.get_categories(asset_type)
                if category not in asset_category_list:
                    print(
                        f"[red]{category} is not a valid category.[/red]\nEnter empty '-c' argument to get the category list of the {asset_type}."
                    )
                    return
            except Exception as e:
                print(f"[red]Error validating category: {e}[/red]")
                return

    # ->🔒file_format->
    if asset_type == "hdris" and fileformat not in ["exr", "hdr"]:
        print(f"[red]{fileformat} is not a valid file format for {asset_type}.[/red]")
        return

    # ->🔒folder->
    # Handle empty folder arg -> current directory
    if folder == "":
        folder = os.getcwd()

    down_folder = os.path.abspath(folder)
    if not os.path.exists(down_folder):
        try:
            os.makedirs(down_folder, exist_ok=True)
            print(f'"{folder}" folder not found, creating...')
        except Exception as e:
            print("[red]Error: " + str(e))
            return

    print(
        f"\n[cyan]🔗(polyhaven.com/{asset_type}"
        + (f"/{category}" if category is not None else "")
        + ("['all sizes']" if sizes == [] else str(sizes))
        + f")=>🏠"
        + (f"({folder})" if folder else "")
        + "\n"
    )

    # Iters handling: -1 means all, so None for controller
    iter_limit = iters if iters != -1 else None

    controller = PolydownController()
    await controller.start(
        asset_type=asset_type,
        category=category,
        folder=down_folder,
        sizes=sizes,
        overwrite=overwrite,
        noimgs=noimgs,
        iters=iter_limit,
        tone=tone,
        fileformat=fileformat,
    )
