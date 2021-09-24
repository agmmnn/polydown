![screenshot](https://user-images.githubusercontent.com/16024979/134737875-9e9a5daf-d6ed-414b-937f-54e67feb0025.png)
<div align="center">
<a href="https://github.com/agmmnn/polydown">
<img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/agmmnn/polydown"></a>
<a href="https://pypi.org/project/polydown/">
<img alt="PyPI" src="https://img.shields.io/pypi/v/polydown"></a>

Batch downloader for [polyhaven.com](https://polyhaven.com/). You can download hdris, textures and models in all sizes. This project uses Poly Haven's [Public API](https://github.com/Poly-Haven/Public-API).
</div>

# How to Install

- `pip install polydown`

# How to Use
```
$ polydown hdris

# download all available sizes of all hdris into current folder.
> 🔗(polyhaven.com/hdris['all sizes'])=>🏠
```
```
$ polydown <asset_type>

# download all assets of this asset type to the current folder in all available sizes.
# asset types: "hdris", "textures", "models".
```
```
$ polydown textures -c

# list of category in the given asset type.
```
```
$ polydown hdris -f hdris_down -s 2k 4k

# download all hdris with given sizes into "hdris_down" folder.
# /if there is no such folder it will create it./
> 🔗(polyhaven.com/hdris['2k', '4k'])=>🏠(hdris_down)
```
```
$ polydown models -c decorative -f folder -s 1k

# download all models in the "decorative" category into the "folder".
> 🔗(polyhaven.com/models/decorative['all sizes'])=>🏠

Downloaded files structure:
```
![model files structure](https://user-images.githubusercontent.com/16024979/134737874-cc04a42e-5855-4acb-9394-dac08352efee.png)

# Arguments:

```
<asset_type>      "hdris, textures, models"
-h, --help        show this help message and exit
-f, --folder      target download folder.
-c, --category    category to download.
-s, --sizes       size(s) of downloaded asset files. eg: 1k 2k 4k
-o, --overwrite   overwrite if the files already exists. otherwise the current task will be skipped.
-no, --noimgs     do not download 'preview, render, thumbnail...' images.
-v, --version     show program's version number and exit
```

# To-Do
-   [ ] Unit Tests
-   [ ] Progressbar for current download task(s)
-   [ ] Select the file format to download
-   [ ] Download a specific asset, "polydown hdris stuttgart_suburbs"

# Requirements
- Python >3.5

## Dependencies
- [requests](https://pypi.org/project/requests/)
- [rich](https://github.com/willmcgugan/rich)

# License
[MIT](https://github.com/agmmnn/polydown/blob/master/LICENSE)