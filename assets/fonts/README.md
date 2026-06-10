# Fonts

This directory is the first font search path used by `scripts/generate_booklet.py`.
It currently includes fonts for Chinese, Japanese, Korean, English, and Spanish.

Use the downloader to cache fonts here:

```bash
python scripts/download_fonts.py --set core
python scripts/download_fonts.py --set core --set cjk-sc
python scripts/download_fonts.py --set all
```

The downloader uses the official Google Fonts repository and writes `FONT_SOURCES.md`
after download.

For this repository, the CJK set is committed so Chinese, Japanese, and Korean
booklets work more reliably out of the box.
