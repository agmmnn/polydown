![screenshot](https://user-images.githubusercontent.com/16024979/134770914-bbc829ac-f1aa-43eb-adf4-9d189379d307.gif)

<div align="center">
<a href="https://github.com/agmmnn/polydown">
<img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/agmmnn/polydown"></a>
<a href="https://pypi.org/project/polydown/">
<img alt="PyPI" src="https://img.shields.io/pypi/v/polydown"></a>

Batch downloader for [polyhaven.com](https://polyhaven.com/). Download HDRIs, textures, and models in any sizes you want.  
This project uses Poly Haven's [Public API](https://github.com/Poly-Haven/Public-API).

</div>

## Installation

```bash
pip install polydown
```

## Usage

### Basic Commands

Download all **HDRIs**:

```bash
polydown hdris
```

Download all **Textures**:

```bash
polydown textures
```

Download all **Models**:

```bash
polydown models
```

> **Note:** These commands will download all available sizes for every asset in the category.

---

### Advanced Usage

**Download specific sizes to a specific folder:**

```bash
polydown hdris -f my_hdris_folder -s 2k 4k
```

> Downloads all HDRIs in 2k and 4k resolution to the `my_hdris_folder`.

**Download from a specific category:**

```bash
polydown models -c decorative -f models_folder -s 1k
```

> Downloads all "decorative" models with 1k textures into `models_folder`.

**List available categories for an asset type:**

```bash
polydown textures -c
```

## Arguments

| Argument              | Description                                                |
| :-------------------- | :--------------------------------------------------------- |
| `asset_type`          | Type of asset to download: `hdris`, `textures`, `models`.  |
| `-h`, `--help`        | Show help message and exit.                                |
| `-f`, `--folder`      | Target download folder.                                    |
| `-c`, `--category`    | Category to download (e.g., `decorative`, `nature`).       |
| `-s`, `--sizes`       | Size(s) of downloaded assets. Example: `1k 2k 4k`.         |
| `-o`, `--overwrite`   | Overwrite existing files. Otherwise, skips existing files. |
| `-no`, `--noimgs`     | Do not download preview, render, or thumbnail images.      |
| `-it`, --iters`       | Amount of iterations (limit number of assets).             |
| `-t`, `--tone`        | Download 8K Tonemapped JPG (HDRIs only).                   |
| `-ff`, `--fileformat` | File format for HDRIs (`hdr`, `exr`).                      |
| `-v`, `--version`     | Show program's version number and exit.                    |

![screenshot](https://user-images.githubusercontent.com/16024979/134804570-a01138e9-7fc0-4d22-b1b5-c52b3cfcf8a2.png)

![file structure](https://user-images.githubusercontent.com/16024979/134737874-cc04a42e-5855-4acb-9394-dac08352efee.png)

## Development

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

### Setup

1. **Install `uv`**:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Sync dependencies**:

   ```bash
   uv sync
   ```

3. **Run the CLI**:

   ```bash
   uv run polydown --help
   ```

4. **Run tests**:

   ```bash
   uv run pytest
   ```

## To-Do

- [ ] Unit Tests
- [ ] Progressbar for current download task(s)
- [ ] Select the file format to download
- [ ] Download a specific asset, e.g., "polydown hdris stuttgart_suburbs"

## License

[MIT](https://github.com/agmmnn/polydown/blob/master/LICENSE)
