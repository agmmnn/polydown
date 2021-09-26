from rich import print
import os
from .hash_check import hash_check
from . import theme


class Downloader:
    def __init__(
        self,
        type,
        asset,
        session,
        down_folder,
        subfolder,
        filename,
        overwrite,
        # --
        url=None,
        md5=None,
        # --
        k=None,
        b=None,
    ):
        self.type = type
        self.asset = asset
        self.s = session
        self.down_folder = down_folder
        self.overwrite = overwrite
        self.md5 = md5
        self.url = url
        self.subfolder = subfolder
        self.filename = filename
        self.k = k
        self.b = b

        asset_k_folder = f"{subfolder}\\{asset}_{k}"
        textures_folder = f"{subfolder}\\{asset}_{k}\\textures"

        if type == "hdris":
            self.folder = down_folder + filename
        elif type == "models":
            self.folder = (
                f"{textures_folder}\\{self.filename}"
                if not b
                else f"{asset_k_folder}\\{self.filename}"
            )
        else:
            self.folder = (
                f"{textures_folder}\\{self.filename}"
                if not self.b
                else f"{asset_k_folder}\\{self.filename}"
            )

        if type == "hdris":
            self.filelist = [
                entry.name
                for entry in os.scandir(path=down_folder)
                if entry.is_file() and entry.name.endswith((".hdr", ".exr", ".png"))
            ]
        else:
            self.filelist = (
                [t.name for t in os.scandir(path=textures_folder) if t.is_file()]
                + [bl.name for bl in os.scandir(path=asset_k_folder) if bl.is_file()]
                + [pr.name for pr in os.scandir(path=subfolder) if pr.is_file()]
            )

    def file(self):
        def save_file():
            r = self.s.get(self.url)
            with open(self.folder, "wb") as f:
                f.write(r.content)

        args = (
            self.type,
            self.asset,
            self.filename,
            self.down_folder,
            self.subfolder,
            self.md5,
            self.k,
            self.b,
        )
        if self.filename in self.filelist and self.overwrite == False:
            h = hash_check(*args)
            h_result = theme.md5v if h == True else theme.md5x
            return (
                theme.t_skipped_file + theme.t_sk + self.filename + h_result,
                "exist",
                h,
            )
        else:
            save_file()
            ow = self.filename in self.filelist and self.overwrite
            h = hash_check(*args)
            h_result = theme.md5v if h == True else theme.md5x
            return (
                theme.t_down_file
                + (theme.t_ow if ow else theme.t_dw)
                + self.filename
                + h_result,
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

        print(theme.t_img)
        for i in imgs_dict:
            filename = f"{self.asset}_{i}.png"
            if filename in self.filelist and self.overwrite == False:
                print(theme.t_skipped_img + theme.t_sk + filename)
            elif filename in self.filelist and self.overwrite:
                save_file(imgs_dict[i], filename)
                print(theme.t_down_img + theme.t_ow + filename)
            else:
                save_file(imgs_dict[i], filename)
                print(theme.t_down_img + theme.t_dw + filename)
