---
name: lyrics-booklet
description: Generate printer-ready A4 PDF booklets with side-by-side bilingual (EN↔ZH) song lyrics using Python + Typst. Use when the user wants to create, print, or export lyric booklets, album lyric collections with Chinese translations, dual-column lyric PDFs for laser printing, or bilingual poetry/song collections with professional typesetting. Triggers on phrases like "歌词集", "歌词本", "打印歌词", "中英对照歌词", "lyrics booklet", "lyric book", "album lyrics PDF", "bilingual lyrics print".
---

# Lyrics Booklet Generator

Generate bilingual (English + Chinese) lyric booklets as printer-ready A4 PDFs using
Typst's professional typesetting engine.

## Quick Start

1. Prepare lyrics data as a Python module (see `references/lyrics-format.md`)
2. Run the generator:
   ```bash
   pip install typst --break-system-packages  # one-time
   python3 scripts/generate_booklet.py data.py \
     --font-dir /path/to/fonts \
     --album-title "ALBUM NAME" \
     --artist "Artist" \
     --label "Label · 2024" \
     -o output.pdf
   ```

## Data Format

Create a Python file exporting `TRACKS`. See `references/lyrics-format.md` for the full specification.

```python
TRACKS = [
    ("01", "Song Title", "feat. Artist", [
        ("Verse 1", [
            ("English line", "中文翻译"),
        ]),
        ("Chorus", [
            ("Chorus line", "副歌中文"),
        ], True),  # is_chorus → bold
    ]),
]
```

## Font Requirements

| Element | Font | Style | Size |
|---------|------|-------|------|
| Cover title | **Playfair Display** (decorative serif) | Bold | 34pt |
| English lyrics | **Inter** (geometric sans) | Italic | 12pt |
| Chinese lyrics | **Noto Sans CJK SC / 思源黑体** | Regular | 11pt |
| Song titles | **Inter** | Bold | 20pt |
| Section labels | **Noto Sans CJK SC** | Light (luma 110) | 7pt |

### Font Installation

```bash
# CJK fonts (Required)
apt install fonts-noto-cjk

# English fonts — download TTF/OTF from Google Fonts or other sources:
#  - Inter: https://fonts.google.com/specimen/Inter
#  - Playfair Display: https://fonts.google.com/specimen/Playfair+Display
```

Place all .ttf/.otf files in a single directory and pass `--font-dir /path/to/fonts`.

To extract SC (Simplified Chinese) from .ttc collections:
```python
from fontTools.ttLib import TTCollection
tc = TTCollection('NotoSansCJK-Regular.ttc')
for font in tc:
    if 'SC' in font['name'].getDebugName(1):
        font.save('NotoSansCJKsc-Regular.ttf')
```

## Typographic Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Page | A4 (210×297mm) | Portrait |
| Left margin | 16mm | Binding side |
| Right margin | 12mm | |
| Top/Bottom margin | 14mm | |
| Line spacing (within lyric) | `leading: 0.6em` | Tight — wrapped lines stay together |
| Line spacing (between lines) | `gutter: 5mm` | Wide — clear separation between different lyrics |
| Colors | Black text on white background | Laser-printer optimized |
| Page numbering | Centered footer, 7pt | |

## Customization

All parameters are CLI flags:

| Flag | Default | Description |
|------|---------|-------------|
| `--en-font` | Inter | English body font |
| `--zh-font` | Noto Sans CJK SC | Chinese body font |
| `--cover-font` | Playfair Display | Cover title decorative font |
| `--en-size` | 12pt | English lyric font size |
| `--zh-size` | 11pt | Chinese lyric font size |
| `--title-size` | 20pt | Song title size |
| `--margin-left` | 16mm | Left margin (binding side) |
| `--margin-right` | 12mm | Right margin |
| `--font-dir` | /usr/share/fonts | Font search path |
| `--album-title` | LYRICS | Cover title |
| `--album-subtitle` | 中英对照歌词集 | Cover subtitle |
| `--artist` | Unknown | Artist name |
| `--label` | (empty) | Label & year on cover (", · 2024") |
| `--output` / `-o` | lyrics_booklet.pdf | Output PDF path |

## Output

- A4 portrait PDF, black & white optimized
- Cover page (dark background, centered motif)
- Dual-column table layout: English left, Chinese right
- Chorus sections bolded on both sides
- Auto page numbering
- Back cover with artist credit

## Dependencies

- Python 3.8+
- `typst` (pip package, includes native compiler ~25MB)
- `brotli` (pip, required for woff2→ttf font extraction)
- `fonttools` (pip, required for .ttc font extraction)
- Fonts:
  - Inter (English body) — download TTF from Google Fonts
  - Playfair Display (cover title) — download TTF from Google Fonts
  - Noto Sans CJK SC / 思源黑体 (Chinese) — `apt install fonts-noto-cjk`
