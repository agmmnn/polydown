import os
import requests
import json
from rich import print as rprint

from .poly import Poly


def polycli(args):
    # rprint(args, "\n")
    asset_type = args.asset_type[0]
    folder = args.folder
    overwrite = args.overwrite
    sizes = args.sizes
    category = args.category
    noimgs = args.noimgs
    s = requests.Session()

    # ->🔒asset type->
    asset_type_list = list(json.loads(s.get("https://api.polyhaven.com/types").content))
    if asset_type not in asset_type_list:
        rprint(f"'{asset_type}' is not a valid asset type!")
        exit()

    # ->🔒category->
    if category == "":
        js = json.loads(
            s.get(f"https://api.polyhaven.com/categories/{asset_type}").content
        )
        rprint(f"[green]There are {len(js)} available categories for {asset_type}:")
        rprint(js)
        exit()
    elif category != None:
        asset_category_list = list(
            json.loads(
                s.get(f"https://api.polyhaven.com/categories/{asset_type}").content
            )
        )
        if category not in asset_category_list:
            rprint(
                f"[red]{category} is not a valid category.[/red]\nEnter empty '-c' argument to get the category list of the {asset_type}."
            )
            exit()

    # ->🔒file_format->
    # if file_format == None:
    #     pass
    # elif asset_type == "hdris" and file_format not in ["exr", "hdr"]:
    #     rprint(f"[red]{file_format} is not a valid file format for {asset_type}.[/red]")
    #     exit()
    # elif asset_type in ["models", "textures"] and file_format not in [
    #     "jpg",
    #     "png",
    #     "exr",
    # ]:
    #     rprint(f"[red]{file_format} is not a valid file format for {asset_type}.[/red]")
    #     exit()

    # ->🔒folder->
    if os.path.exists(folder):
        down_folder = folder + "\\" if folder[:-1] != "\\" else ""
    else:
        down_folder = os.getcwd() + "\\" + folder + "\\" if folder[:-1] != "\\" else ""
        try:
            if os.path.exists(down_folder) == False:
                os.mkdir(down_folder)
                print("Folder not found, creating...")
        except Exception as e:
            rprint("[red]Error: " + str(e))
            exit()

    rprint(
        f"\n[cyan]🔗(polyhaven.com/{asset_type}"
        + (f"/{category}" if category != None else "")
        + ("['all sizes']" if sizes == [] else str(sizes))
        + f")=>🏠"
        + (f"({folder})" if not folder == "" else "")
        + "\n"
    )

    Poly(asset_type, s, category, down_folder, sizes, overwrite, noimgs)
