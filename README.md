# download-cia
A tool to download CIA files for 3DS system modules.

## Preparation
1. Clone with submodules.
2. Build `make_cdn_cia` found at `libs/make_cdn_cia`. If you have the correct build tools running `make` in the `make_cdn_cia` directory should be enough.

## Usage
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./download-cia.py <title_id> <version>
```

You can use the very useful [https://yls8.mtheall.com/ninupdates/reports.php](ninupdates) site to find title ids and versions of system modules.

Example (Downloading the latest version of the 3DS SSL Module)

```
./download-cia.py 0004013000002F02 9217
```
