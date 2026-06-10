# Lyrics Booklet

Create print-ready lyric booklets from structured text data. The generator turns multilingual song lyrics into an A4 PDF with an editorial cover, clean language columns, chorus styling, page numbers, and Typst-quality typesetting.

![Lyrics Booklet preview](assets/preview.svg)

## Why It Exists

Most lyric PDFs look like exported notes. `lyrics-booklet` is for booklets that feel intentional: album inserts, fan translation packs, rehearsal handouts, poetry translations, listening club zines, and private print runs.

## Features

- Multilingual layout with custom language order, labels, fonts, and sizes
- Backward-compatible EN/ZH tuple format
- Four visual presets: `gallery`, `minimal`, `noir`, and `zine`
- Two body layouts: side-by-side columns or stacked multilingual rows
- Bundled core fonts plus an official Google Fonts downloader
- Typst source export for manual design tweaking
- A4 print defaults with binding-friendly margins
- Codex skill instructions included in `SKILL.md`

## Quick Start

```bash
python -m pip install typst
python scripts/generate_booklet.py examples/album_data.py \
  --preset gallery \
  --languages en,zh,ja \
  --output paper-moon-booklet.pdf
```

The repository includes a small stable font set in `assets/fonts/`. To refresh or add CJK fonts:

```bash
python scripts/download_fonts.py --set core
python scripts/download_fonts.py --set core --set cjk-sc
python scripts/download_fonts.py --set core --set cjk
```

To inspect or customize the generated Typst source without compiling:

```bash
python scripts/generate_booklet.py examples/album_data.py \
  --preset noir \
  --typst-out paper-moon.typ \
  --no-pdf
```

## Data Format

Define `BOOKLET`, `LANGUAGES`, and `TRACKS` in a Python file:

```python
BOOKLET = {
    "album_title": "Paper Moon Sessions",
    "album_subtitle": "English / 中文 / 日本語 lyric booklet",
    "artist": "Example Artist",
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
        "sections": [
            {
                "label": "Verse 1",
                "lines": [
                    {"en": "I folded the night", "zh": "我把夜晚折起", "ja": "夜を折りたたむ"},
                ],
            },
        ],
    },
]
```

See `references/lyrics-format.md` for the full schema.

## Presets

| Preset | Use it for |
| --- | --- |
| `gallery` | polished album inserts and giftable PDFs |
| `minimal` | dense black-and-white laser printing |
| `noir` | dramatic covers with high contrast |
| `zine` | indie demos and handmade booklet energy |

## Fonts

`scripts/generate_booklet.py` automatically searches:

1. `assets/fonts/`
2. Common system font folders such as `C:\Windows\Fonts` and `/usr/share/fonts`
3. Extra paths passed with `--font-dir`

The downloader uses direct links to the official Google Fonts repository. The default committed set is small; CJK fonts are optional because they are much larger.

## Responsible Use

Only publish or distribute lyric booklets when you have the rights to the lyrics and translations. For commercial releases, verify typography licenses and lyric permissions before printing.

## Codex Skill

Install the folder into `~/.codex/skills/lyrics-booklet`, restart Codex, then ask Codex to use `$lyrics-booklet` for booklet generation tasks.
