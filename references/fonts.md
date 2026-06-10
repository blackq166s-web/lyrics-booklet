# Font Strategy

The generator searches fonts in this order:

1. `assets/fonts/` inside the skill
2. Common system font folders such as `C:\Windows\Fonts` and `/usr/share/fonts`
3. Extra directories passed with `--font-dir`

## Recommended Bundled Set

Commit the core fonts for stable cover and Latin layout:

```bash
python scripts/download_fonts.py --set core
```

For Chinese-first booklets, also download Simplified Chinese:

```bash
python scripts/download_fonts.py --set core --set cjk-sc
```

For broad CJK coverage:

```bash
python scripts/download_fonts.py --set core --set cjk
```

## Official Sources

The downloader uses direct links to the official Google Fonts repository:

| Family | Source folder |
| --- | --- |
| Inter | `https://github.com/google/fonts/tree/main/ofl/inter` |
| Playfair Display | `https://github.com/google/fonts/tree/main/ofl/playfairdisplay` |
| Space Grotesk | `https://github.com/google/fonts/tree/main/ofl/spacegrotesk` |
| Noto Sans SC | `https://github.com/google/fonts/tree/main/ofl/notosanssc` |
| Noto Sans TC | `https://github.com/google/fonts/tree/main/ofl/notosanstc` |
| Noto Sans JP | `https://github.com/google/fonts/tree/main/ofl/notosansjp` |
| Noto Sans KR | `https://github.com/google/fonts/tree/main/ofl/notosanskr` |

## Size Guidance

- `core` is small and suitable to commit.
- `cjk-sc` is roughly 17 MB and is reasonable for a Chinese-first repository.
- `cjk` is roughly 50 MB and may make installation slower.
