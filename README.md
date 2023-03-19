# SVGRepoCollectionDownloader

This script does exactly what it sounds like... It's a helper script to download complete collections from SVGRepo.com.

## Usage

Example to download the collection `flare-dashed-icons` to %USERPROFILE%/Documents/icons (or ~/icons on Linux):
```python
py download.py https://www.svgrepo.com/collection/flare-dashed-icons
```

The script also takes a -p/--path argument to specify the output directory:
```python
py download.py https://www.svgrepo.com/collection/flare-dashed-icons -p /my/custom/path
```
