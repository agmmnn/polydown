import hashlib


def hash_check(
    type,
    asset,
    filename,
    down_folder,
    subfolder,
    hash,
    k=None,
    b=None,
):
    if type == "hdris":
        file = down_folder + filename
    else:
        file = (
            f"{subfolder}/{asset}_{k}/textures/{filename}"
            if not b
            else f"{subfolder}/{asset}_{k}/{filename}"
        )

    with open(file, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)

    if hash != file_hash.hexdigest():
        return False
    return True
