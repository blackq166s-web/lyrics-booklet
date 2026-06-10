#!/usr/bin/env python3
"""Download optional fonts for lyrics-booklet.

Sources are Google Fonts' public repository. The default `core` set is small
enough to commit. CJK fonts are larger, so download only the scripts needed by
the booklet.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import urllib.request
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DEST = SKILL_DIR / "assets" / "fonts"

FONT_FILES = {
    "inter": {
        "group": "core",
        "filename": "Inter[opsz,wght].ttf",
        "url": "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz,wght%5D.ttf",
    },
    "inter-italic": {
        "group": "core",
        "filename": "Inter-Italic[opsz,wght].ttf",
        "url": "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter-Italic%5Bopsz,wght%5D.ttf",
    },
    "playfair-display": {
        "group": "core",
        "filename": "PlayfairDisplay[wght].ttf",
        "url": "https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf",
    },
    "space-grotesk": {
        "group": "core",
        "filename": "SpaceGrotesk[wght].ttf",
        "url": "https://raw.githubusercontent.com/google/fonts/main/ofl/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf",
    },
    "noto-sans-sc": {
        "group": "cjk-sc",
        "filename": "NotoSansSC[wght].ttf",
        "url": "https://raw.githubusercontent.com/google/fonts/main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf",
    },
    "noto-sans-tc": {
        "group": "cjk-tc",
        "filename": "NotoSansTC[wght].ttf",
        "url": "https://raw.githubusercontent.com/google/fonts/main/ofl/notosanstc/NotoSansTC%5Bwght%5D.ttf",
    },
    "noto-sans-jp": {
        "group": "cjk-jp",
        "filename": "NotoSansJP[wght].ttf",
        "url": "https://raw.githubusercontent.com/google/fonts/main/ofl/notosansjp/NotoSansJP%5Bwght%5D.ttf",
    },
    "noto-sans-kr": {
        "group": "cjk-kr",
        "filename": "NotoSansKR[wght].ttf",
        "url": "https://raw.githubusercontent.com/google/fonts/main/ofl/notosanskr/NotoSansKR%5Bwght%5D.ttf",
    },
}

LICENSE_FILES = {
    "inter": "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/OFL.txt",
    "playfairdisplay": "https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/OFL.txt",
    "spacegrotesk": "https://raw.githubusercontent.com/google/fonts/main/ofl/spacegrotesk/OFL.txt",
    "notosanssc": "https://raw.githubusercontent.com/google/fonts/main/ofl/notosanssc/OFL.txt",
    "notosanstc": "https://raw.githubusercontent.com/google/fonts/main/ofl/notosanstc/OFL.txt",
    "notosansjp": "https://raw.githubusercontent.com/google/fonts/main/ofl/notosansjp/OFL.txt",
    "notosanskr": "https://raw.githubusercontent.com/google/fonts/main/ofl/notosanskr/OFL.txt",
}


def wanted_fonts(groups: list[str]) -> dict[str, dict[str, str]]:
    if "all" in groups:
        return FONT_FILES

    expanded: set[str] = set()
    for group in groups:
        if group == "cjk":
            expanded.update({"cjk-sc", "cjk-tc", "cjk-jp", "cjk-kr"})
        else:
            expanded.add(group)

    return {name: item for name, item in FONT_FILES.items() if item["group"] in expanded or name in expanded}


def download(url: str, dest: Path, force: bool) -> None:
    if dest.exists() and not force:
        print(f"exists: {dest.name}")
        return

    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": "lyrics-booklet-font-downloader"})
    with urllib.request.urlopen(request, timeout=120) as response, tmp.open("wb") as file_handle:
        shutil.copyfileobj(response, file_handle)
    tmp.replace(dest)
    print(f"downloaded: {dest.name}")


def write_sources(dest: Path, fonts: dict[str, dict[str, str]]) -> None:
    lines = [
        "# Font Sources",
        "",
        "Downloaded from the official Google Fonts repository.",
        "",
        "| File | Source |",
        "| --- | --- |",
    ]
    for item in fonts.values():
        lines.append(f"| `{item['filename']}` | {item['url']} |")
    lines.append("")
    lines.append("Each family is distributed under the SIL Open Font License in the upstream Google Fonts repository.")
    (dest / "FONT_SOURCES.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Download fonts used by lyrics-booklet.")
    parser.add_argument(
        "--set",
        action="append",
        default=["core"],
        choices=["core", "cjk-sc", "cjk-tc", "cjk-jp", "cjk-kr", "cjk", "all"],
        help="Font set to download. Repeat as needed. Default: core.",
    )
    parser.add_argument("--dest", default=str(DEFAULT_DEST), help="Destination font directory.")
    parser.add_argument("--force", action="store_true", help="Redownload existing files.")
    parser.add_argument("--skip-licenses", action="store_true", help="Do not download OFL license files.")
    args = parser.parse_args(argv)

    dest = Path(args.dest).expanduser().resolve()
    fonts = wanted_fonts(args.set)
    if not fonts:
        raise SystemExit("No fonts selected.")

    for item in fonts.values():
        download(item["url"], dest / item["filename"], args.force)

    if not args.skip_licenses:
        for family, url in LICENSE_FILES.items():
            if any(family.replace("display", "-display") in name or family in name.replace("-", "") for name in fonts):
                download(url, dest / f"OFL-{family}.txt", args.force)

    write_sources(dest, fonts)
    print(f"font directory: {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
