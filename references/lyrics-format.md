# Lyrics Data Format

The generator expects a Python module exporting a `TRACKS` list with this structure:

```python
TRACKS = [
    ("01", "Song Title", "feat. Artist Name", [
        # Each section: (label, line_pairs, is_chorus?)
        ("Section Label", [
            ("English lyric line", "中文翻译"),
            ("", ""),  # blank line for spacing
        ]),
        ("Chorus", [
            ("Chorus English", "副歌中文"),
        ], True),  # is_chorus=True → bold styling
    ]),
    # ... more tracks
]
```

## Field Reference

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Track number | str | Yes | e.g. "01" |
| Title | str | Yes | Song title |
| Featuring | str | No | Empty string if none |
| Section label | str | No | Shown in grey before section |
| Line pair (EN, ZH) | tuple | Yes | Both can be empty for blank line |
| is_chorus | bool | No | Default False; True = bold both sides |

## Blank Lines

Use `("", "")` for a blank/separator row. The table will still generate a row with no content.

## Supported Characters

Special Typst characters (`#`, `\`) are automatically escaped. Smart quotes and apostrophes are preserved.
