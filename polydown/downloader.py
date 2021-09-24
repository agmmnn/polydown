from rich import print as rprint
import os
from .hash_check import hash_check

# theme
t_skipped_file = "[on dark_khaki]📁↳[/on dark_khaki][green]"
t_down_file = "[grey11 on cyan]📁↓[/grey11 on cyan][cyan]"

t_skipped_img = "[on dark_khaki]🖼️↳[/on dark_khaki][green]"
t_down_img = "[grey11 on cyan]🖼️↓[/grey11 on cyan][cyan]"

v = " (MD5✔)"
x = " [red](MD5❌)"
# /theme


class Downloader:
    def __init__(
        self,
        type,
        session,
        down_folder,
        subfolder,
        filename,
        asset,
        k,
        url,
        md5,
        overwrite,
        b,
    ):
        self.type = type
        self.s = session
        self.down_folder = down_folder
        self.subfolder = subfolder
        self.filename = filename
        self.asset = asset
        self.k = k
        self.url = url
        self.md5 = md5
        self.overwrite = overwrite
        self.b = b
        self.asset_k_folder = f"{subfolder}\\{asset}_{k}"
        self.textures_folder = f"{subfolder}\\{asset}_{k}\\textures"

        if type == "hdris":
            self.folder = down_folder + filename
        elif type == "models":
            self.folder = (
                f"{self.textures_folder}\\{self.filename}"
                if not b
                else f"{self.asset_k_folder}\\{self.filename}"
            )
        else:
            self.folder = (
                f"{self.textures_folder}\\{self.filename}"
                if not self.b
                else f"{self.asset_k_folder}\\{self.filename}"
            )

        if type == "hdris":
            self.filelist = [
                entry.name
                for entry in os.scandir(path=down_folder)
                if entry.is_file() and entry.name.endswith((".hdr", ".exr", ".png"))
            ]
        else:
            self.filelist = (
                [t.name for t in os.scandir(path=self.textures_folder) if t.is_file()]
                + [
                    bl.name
                    for bl in os.scandir(path=self.asset_k_folder)
                    if bl.is_file()
                ]
                + [pr.name for pr in os.scandir(path=subfolder) if pr.is_file()]
            )

    def file(self):
        def save_file():
            r = self.s.get(self.url)
            with open(self.folder, "wb") as f:
                f.write(r.content)

        if self.filename in self.filelist and self.overwrite == False:
            h = hash_check(
                self.type,
                self.down_folder,
                self.subfolder,
                self.asset,
                self.k,
                self.filename,
                self.md5,
                self.b,
            )
            return (
                t_skipped_file
                + " Already exist (skipped): "
                + self.filename
                + (v if h == True else x),
                "exist",
                h,
            )
        elif self.filename in self.filelist and self.overwrite:
            save_file()
            h = hash_check(
                self.type,
                self.down_folder,
                self.subfolder,
                self.asset,
                self.k,
                self.filename,
                self.md5,
                self.b,
            )
            return (
                t_down_file
                + " Already exist (overwritten): "
                + self.filename
                + (v if h == True else x),
                "downloaded",
                h,
            )
        else:
            save_file()
            h = hash_check(
                self.type,
                self.down_folder,
                self.subfolder,
                self.asset,
                self.k,
                self.filename,
                self.md5,
                self.b,
            )
            return (
                t_down_file
                + " Download complete: "
                + self.filename
                + (v if h == True else x),
                "downloaded",
                h,
            )

    def img(self):
        if self.type == "hdris":
            imgs_dict = {
                "thumb": f"https://cdn.polyhaven.com/asset_img/thumbs/{self.asset}.png",
                "primary": f"https://cdn.polyhaven.com/asset_img/primary/{self.asset}.png",
                "renders_lone_monk": f"https://cdn.polyhaven.com/asset_img/renders/{self.asset}/lone_monk.png",
            }
        elif self.type == "textures":
            imgs_dict = {
                "primary": f"https://cdn.polyhaven.com/asset_img/primary/{self.asset}.png",
                "thumb": f"https://cdn.polyhaven.com/asset_img/thumbs/{self.asset}.png",
                "renders_clay": f"https://cdn.polyhaven.com/asset_img/renders/{self.asset}/clay.png",
            }
        elif self.type == "models":
            imgs_dict = {
                "primary": f"https://cdn.polyhaven.com/asset_img/primary/{self.asset}.png",
                "renders_clay": f"https://cdn.polyhaven.com/asset_img/renders/{self.asset}/clay.png",
                "renders_orth_front": f"https://cdn.polyhaven.com/asset_img/renders/{self.asset}/orth_front.png",
                "renders_orth_side": f"https://cdn.polyhaven.com/asset_img/renders/{self.asset}/orth_side.png",
                "renders_orth_top": f"https://cdn.polyhaven.com/asset_img/renders/{self.asset}/orth_top.png",
            }

        def save_file(url, filename):
            r = self.s.get(url)
            with open(
                f"{self.subfolder}\\{filename}"
                if self.type != "hdris"
                else f"{self.down_folder}\\{filename}",
                "wb",
            ) as f:
                f.write(r.content)

        for i in imgs_dict:
            filename = f"{self.asset}_{i}.png"
            if filename in self.filelist and self.overwrite == False:
                rprint(t_skipped_img + "Already exist (skipped): " + filename)
            elif filename in self.filelist and self.overwrite:
                save_file(imgs_dict[i], filename)
                rprint(t_down_img + "Already exist (overwritten): " + filename)
            else:
                save_file(imgs_dict[i], filename)
                rprint(t_down_img + "Download complete: " + filename)
