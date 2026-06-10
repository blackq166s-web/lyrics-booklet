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
     --font-name "Noto Serif CJK SC" \
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

A CJK serif font is required for proper Chinese rendering. Common options:

- **Noto Serif CJK SC**: Install via `apt install fonts-noto-cjk` or download OTF/TTF
- **Source Han Serif**: Adobe's open-source CJK serif
- Any system font supporting both Latin and CJK characters

To extract SC (Simplified Chinese) from .ttc collections:
```python
from fontTools.ttLib import TTCollection
tc = TTCollection('NotoSerifCJK-Regular.ttc')
for font in tc:
    if 'SC' in font['name'].getDebugName(1):
        font.save('NotoSerifCJKsc-Regular.ttf')
```

## Customization

All parameters are CLI flags:

| Flag | Default | Description |
|------|---------|-------------|
| `--en-size` | 12pt | English lyric font size |
| `--zh-size` | 11pt | Chinese lyric font size |
| `--title-size` | 20pt | Song title size |
| `--margin-left` | 16mm | Left margin (binding side) |
| `--margin-right` | 12mm | Right margin |
| `--font-dir` | /usr/share/fonts | Font search path |
| `--album-title` | LYRICS | Cover title |
| `--artist` | Unknown | Artist name |

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
- CJK serif font (Noto Serif CJK SC recommended)
