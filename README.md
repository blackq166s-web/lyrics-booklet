# 多语言对照歌词册生成器 / Lyrics Booklet

[中文说明](README.zh-CN.md)

Create print-ready multilingual lyric booklets from structured text data. The generator turns parallel lyrics and translations into an A4 PDF with an editorial cover, clean language columns, chorus styling, page numbers, and Typst-quality typesetting.

![Multilingual lyric booklet preview](assets/preview.svg)

## Why It Exists

Most lyric PDFs look like exported notes. `lyrics-booklet` is a multilingual parallel lyrics booklet generator for work that should feel intentional: album inserts, fan translation packs, rehearsal handouts, poetry translations, listening club zines, and private print runs.

## Features

- Multilingual layout with custom language order, labels, fonts, and sizes
- First-class coverage for Chinese, Japanese, Korean, English, and Spanish
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

The repository includes stable bundled fonts for English, Spanish, Simplified Chinese, Traditional Chinese, Japanese, and Korean:

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

## Language Coverage

The bundled font set covers:

| Language group | Keys | Default font |
| --- | --- | --- |
| English | `en` | Inter |
| Spanish | `es` | Inter |
| Simplified Chinese | `zh`, `zh-cn`, `zh-hans` | Noto Sans SC |
| Traditional Chinese | `zh-tw`, `zh-hant` | Noto Sans TC |
| Japanese | `ja` | Noto Sans JP |
| Korean | `ko` | Noto Sans KR |

Other languages can still be used by adding an entry to `LANGUAGES` with a suitable font.

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

The downloader uses direct links to the official Google Fonts repository. This repository now commits the CJK set so Chinese, Japanese, and Korean layouts work more reliably out of the box.

## Responsible Use

Only publish or distribute lyric booklets when you have the rights to the lyrics and translations. For commercial releases, verify typography licenses and lyric permissions before printing.

## Codex Skill

Install the folder into `~/.codex/skills/lyrics-booklet`, restart Codex, then ask Codex to use `$lyrics-booklet` for booklet generation tasks.
