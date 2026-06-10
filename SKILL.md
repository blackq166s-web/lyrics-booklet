---
name: lyrics-booklet
description: Generate printer-ready A4 lyric booklets, album inserts, translation zines, and poetry/song collections with Python and Typst. Use when the user wants a PDF booklet for lyrics or bilingual/multilingual text such as English-Chinese, Chinese-English, Japanese-English, Korean-English, or any multi-language side-by-side translation. Supports artistic presets, custom language fonts, Typst source export, and print-oriented layout. Trigger on requests like lyrics booklet, lyric book, album lyrics PDF, bilingual lyrics, multilingual lyrics, 歌词集, 歌词本, 打印歌词, 中英对照歌词, 多语言歌词排版.
---

# Lyrics Booklet

Use this skill to turn structured lyric or poetry text into a print-ready A4 PDF. The generator is useful for album inserts, bilingual lyric sheets, translation collections, listening-club handouts, and small zines. It has first-class bundled font coverage for Chinese, Japanese, Korean, English, and Spanish.

## Workflow

1. Confirm the user has the lyrics/translations or rights to use them.
2. Create or update a Python data file containing `BOOKLET`, `LANGUAGES`, and `TRACKS`.
3. Read `references/lyrics-format.md` when building or validating the data file.
4. Read `references/fonts.md` when the task involves CJK scripts, missing glyphs, or portable GitHub packaging.
5. Choose a visual preset from `references/style-guide.md`.
6. Run `scripts/generate_booklet.py`.
7. If Typst or fonts are missing, generate `.typ` with `--no-pdf --typst-out output.typ` and tell the user what dependency is missing.

## Quick Command

```bash
python scripts/generate_booklet.py examples/album_data.py \
  --preset gallery \
  --languages en,zh,ja \
  --output lyrics_booklet.pdf
```

Use this inspection path when the PDF compiler is unavailable:

```bash
python scripts/generate_booklet.py examples/album_data.py \
  --preset noir \
  --typst-out lyrics_booklet.typ \
  --no-pdf
```

## Data Model

Prefer the dictionary schema:

```python
BOOKLET = {
    "album_title": "Paper Moon Sessions",
    "album_subtitle": "English / 中文 / 日本語 lyric booklet",
    "artist": "Example Artist",
    "label": "Private demo · 2026",
}

LANGUAGES = [
    {"key": "en", "label": "English", "font": "Inter", "style": "italic"},
    {"key": "zh", "label": "中文", "font": "Noto Sans SC"},
    {"key": "ja", "label": "日本語", "font": "Noto Sans JP"},
]

TRACKS = [
    {
        "number": "01",
        "title": "Paper Moon",
        "subtitle": "demo version",
        "sections": [
            {
                "label": "Verse 1",
                "lines": [
                    {"en": "English line", "zh": "中文翻译", "ja": "日本語訳"},
                ],
            },
            {
                "label": "Chorus",
                "chorus": True,
                "lines": [
                    {"en": "Bold chorus line", "zh": "加粗副歌", "ja": "太字のサビ"},
                ],
            },
        ],
    },
]
```

The script also accepts the original tuple format for two-language data:

```python
TRACKS = [
    ("01", "Song Title", "feat. Artist", [
        ("Verse 1", [
            ("English line", "中文翻译"),
        ]),
        ("Chorus", [
            ("Chorus line", "副歌中文"),
        ], True),
    ]),
]
```

## Layout Choices

- Use `--preset gallery` for a polished editorial booklet.
- Use `--preset minimal` for dense, black-and-white laser printing.
- Use `--preset noir` for a dramatic cover with a clean white interior.
- Use `--preset zine` for indie/demo booklet styling.
- Use `--line-layout columns` for 1 to 3 languages.
- Use `--line-layout stacked` for 4+ languages or long translations.
- Use `--languages en,zh,ja` to reorder or export only selected languages.

## Font Guidance

- The generator searches `assets/fonts/` automatically before common system font folders.
- Use `scripts/download_fonts.py --set core` to cache stable Inter, Inter Italic, Playfair Display, and Space Grotesk files from Google Fonts.
- Use `scripts/download_fonts.py --set core --set cjk-sc` for Chinese-first projects.
- Use `scripts/download_fonts.py --set core --set cjk` for Simplified Chinese, Traditional Chinese, Japanese, and Korean.
- Use Google Fonts family names in data files, such as `Noto Sans SC`, `Noto Sans TC`, `Noto Sans JP`, and `Noto Sans KR`.
- Use `Inter` for English and Spanish.
- Pass custom font folders with repeated `--font-dir` flags when the user has their own brand fonts.
- Keep expressive fonts for covers and readable fonts for lyric bodies.

## Main Options

| Option | Purpose |
| --- | --- |
| `--preset gallery|minimal|noir|zine` | Visual system |
| `--languages en,zh,ja` | Select or reorder languages |
| `--line-layout auto|columns|stacked` | Body layout |
| `--typst-out output.typ` | Save Typst source |
| `--no-pdf` | Skip PDF compilation |
| `--font-dir PATH` | Add a font search path |
| `--cover-font FONT` | Override cover/title font |
| `--accent-color #RRGGBB` | Override accent color |

## Font Downloader

```bash
python scripts/download_fonts.py --set core
python scripts/download_fonts.py --set core --set cjk-sc
python scripts/download_fonts.py --set all
```

Commit the small `core` set for stable GitHub demos. Commit `cjk-sc` when Chinese output is a first-class use case. Avoid committing every CJK font unless repo size is acceptable.

## Validation

Before delivering a booklet:

1. Run the script with `--typst-out` to confirm the data normalizes.
2. Compile the PDF if `typst` is installed.
3. Check that every requested language appears in the expected order.
4. Check page margins if the output will be stapled or bound.
5. Remind the user to verify lyric and translation rights before public distribution.
