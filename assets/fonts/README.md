# Fonts

This directory is the first font search path used by `scripts/generate_booklet.py`.

Use the downloader to cache fonts here:

```bash
python scripts/download_fonts.py --set core
python scripts/download_fonts.py --set core --set cjk-sc
python scripts/download_fonts.py --set all
```

The downloader uses the official Google Fonts repository and writes `FONT_SOURCES.md`
after download.

The repository should usually commit the small `core` set. CJK fonts are much
larger, so decide whether to commit only the languages the project needs.
