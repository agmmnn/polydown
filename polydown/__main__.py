import argparse
import datetime
from .cli import polycli

__version__ = "0.3.2"

ap = argparse.ArgumentParser()
ap.add_argument(
    "asset_type",
    type=str,
    nargs="*",
    help='"hdris, textures, models"',
)
ap.add_argument(
    "-f",
    "--folder",
    action="store",
    type=str,
    default="",
    help="target download folder.",
)
ap.add_argument(
    "-c",
    "--category",
    nargs="?",
    const="",
    help="category to download.",
)
ap.add_argument(
    "-s",
    "--sizes",
    nargs="+",
    default=[],
    help="size(s) of downloaded asset files. eg: 1k 2k 4k",
)
ap.add_argument(
    "-it",
    "--iters",
    action="store",
    type=int,
    default=-1,
    help="amount of iterations.",
)
ap.add_argument(
    "-ff",
    "--fileformat",
    action="store",
    type=str,
    default="hdr",
    help="file format for hdris (hdr, exr).",
)
ap.add_argument(
    "-o",
    "--overwrite",
    action="store_true",
    default=False,
    help="Overwrite if the files already exists.  otherwise the current task will be skipped.",
)
ap.add_argument(
    "-t",
    "--tone",
    action="store_true",
    default=False,
    help="Download 8K Tonemapped JPG (only HDRIs).",
)
ap.add_argument(
    "-no",
    "--noimgs",
    action="store_true",
    default=False,
    help="Do not download 'preview, render, thumbnail...' images.",
)
ap.add_argument("-v", "--version", action="version", version="%(prog)s v" + __version__)
args = ap.parse_args()


def cli():
    if args.asset_type == []:
        print("<asset_type> is required.")
        exit(0)

    execution_start_time = datetime.datetime.now()

    try:
        polycli(args)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt!")

    print("Total runtime: {}".format(datetime.datetime.now() - execution_start_time))


if __name__ == "__main__":
    try:
        cli()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt!")
