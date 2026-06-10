# Lyrics Data Format

The generator reads a Python file and expects `TRACKS`. Add `BOOKLET` and `LANGUAGES` for a polished multilingual booklet.

## Recommended Schema

```python
BOOKLET = {
    "album_title": "Paper Moon Sessions",
    "album_subtitle": "English / 中文 / 日本語 lyric booklet",
    "artist": "Example Artist",
    "label": "Private demo · 2026",
}

LANGUAGES = [
    {
        "key": "en",
        "label": "English",
        "font": "Inter",
        "size": "11pt",
        "style": "italic",
        "width": "1fr",
    },
    {
        "key": "zh",
        "label": "中文",
        "font": "Noto Sans SC",
        "size": "10.4pt",
        "width": "1.05fr",
    },
    {
        "key": "ja",
        "label": "日本語",
        "font": "Noto Sans JP",
        "size": "10.2pt",
        "width": "1fr",
    },
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
                    {"en": "English lyric", "zh": "中文翻译", "ja": "日本語訳"},
                    {"en": "", "zh": "", "ja": ""},  # optional blank line
                ],
            },
            {
                "label": "Chorus",
                "chorus": True,
                "lines": [
                    {"en": "Chorus line", "zh": "副歌中文", "ja": "サビ"},
                ],
            },
        ],
    },
]
```

## Fields

| Field | Required | Notes |
| --- | --- | --- |
| `BOOKLET.album_title` | No | Cover title. CLI `--album-title` overrides it. |
| `BOOKLET.album_subtitle` | No | Cover subtitle. |
| `BOOKLET.artist` | No | Artist or collection owner. |
| `BOOKLET.label` | No | Small cover metadata, usually label/year/version. |
| `LANGUAGES[].key` | Yes | Stable key used inside each lyric line. |
| `LANGUAGES[].label` | No | Printed language label. Defaults to uppercase key. |
| `LANGUAGES[].font` | No | Defaults by script/language family where possible. |
| `LANGUAGES[].size` | No | Typst size such as `10.5pt`. |
| `LANGUAGES[].style` | No | Usually `normal` or `italic`. |
| `LANGUAGES[].weight` | No | Usually `regular` or `bold`. |
| `LANGUAGES[].fill` | No | Typst color, e.g. `luma(48)` or `#444444`. |
| `LANGUAGES[].width` | No | Column width, e.g. `1fr` or `1.08fr`. |
| `TRACKS[].number` | No | Defaults to sequence number. |
| `TRACKS[].title` | Yes | Track title. |
| `TRACKS[].subtitle` | No | Featuring/version text. |
| `sections[].label` | No | Verse, Chorus, Bridge, etc. |
| `sections[].chorus` | No | `True` makes the section visually stronger. |
| `sections[].lines` | Yes | List of dictionaries keyed by language. |

## Legacy Tuple Format

The old two-language format still works:

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

If `LANGUAGES` has more than two entries, tuple lines map by order. Missing languages are left blank.

## Exporting Subsets

Use `--languages` to select or reorder language columns without changing the data file:

```bash
python scripts/generate_booklet.py data.py --languages zh,en -o zh-en.pdf
python scripts/generate_booklet.py data.py --languages en,zh,ja --line-layout stacked
```

## Escaping

The generator escapes Typst-sensitive characters such as `#`, `[`, `]`, `*`, `_`, `$`, and backslashes in lyric text.
