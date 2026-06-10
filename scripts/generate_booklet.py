#!/usr/bin/env python3
"""Generate printer-ready lyric booklets with Typst.

The script accepts a small Python data file and writes a Typst source file and,
when the `typst` Python package is installed, a PDF.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSET_FONT_DIR = SKILL_DIR / "assets" / "fonts"


DEFAULT_LANGUAGES = [
    {
        "key": "en",
        "label": "English",
        "font": "Inter",
        "size": "11.2pt",
        "style": "italic",
        "weight": "regular",
        "fill": "luma(35)",
        "width": "1fr",
    },
    {
        "key": "zh",
        "label": "中文",
        "font": "Noto Sans SC",
        "size": "10.5pt",
        "style": "normal",
        "weight": "regular",
        "fill": "luma(48)",
        "width": "1.08fr",
    },
]

FONT_HINTS = {
    "en": "Inter",
    "fr": "Inter",
    "de": "Inter",
    "es": "Inter",
    "it": "Inter",
    "pt": "Inter",
    "ru": "Noto Serif",
    "uk": "Noto Serif",
    "el": "Noto Serif",
    "zh": "Noto Sans SC",
    "zh-cn": "Noto Sans SC",
    "zh-hans": "Noto Sans SC",
    "zh-tw": "Noto Sans TC",
    "zh-hant": "Noto Sans TC",
    "ja": "Noto Sans JP",
    "ko": "Noto Sans KR",
    "ar": "Noto Naskh Arabic",
    "he": "Noto Sans Hebrew",
    "hi": "Noto Sans Devanagari",
    "th": "Noto Sans Thai",
    "vi": "Noto Sans",
}

PRESETS = {
    "minimal": {
        "cover_fill": "#ffffff",
        "page_fill": "#ffffff",
        "text_fill": "#111111",
        "muted_fill": "luma(115)",
        "accent": "#111111",
        "cover_font": "Playfair Display",
        "ui_font": "Inter",
        "title_case": "upper",
        "cover_kicker": "LYRICS BOOKLET",
    },
    "gallery": {
        "cover_fill": "#f6efe6",
        "page_fill": "#fffdf9",
        "text_fill": "#211b17",
        "muted_fill": "#806f62",
        "accent": "#a2644a",
        "cover_font": "Playfair Display",
        "ui_font": "Inter",
        "title_case": "title",
        "cover_kicker": "Collected Lyrics",
    },
    "noir": {
        "cover_fill": "#111111",
        "page_fill": "#ffffff",
        "text_fill": "#111111",
        "muted_fill": "luma(120)",
        "accent": "#c9a45c",
        "cover_font": "Playfair Display",
        "ui_font": "Inter",
        "title_case": "upper",
        "cover_kicker": "Private Press",
    },
    "zine": {
        "cover_fill": "#fff7ed",
        "page_fill": "#fffdf8",
        "text_fill": "#18181b",
        "muted_fill": "luma(105)",
        "accent": "#e11d48",
        "cover_font": "Space Grotesk",
        "ui_font": "Space Grotesk",
        "title_case": "asis",
        "cover_kicker": "DIY LYRIC ZINE",
    },
}


def typst_str(value: Any) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def typst_color(value: Any) -> str:
    text = str(value or "black").strip()
    if text.startswith("#"):
        return f"rgb({typst_str(text)})"
    return text


def typst_text(value: Any) -> str:
    text = "" if value is None else str(value)
    replacements = {
        "\\": "\\\\",
        "#": "\\#",
        "[": "\\[",
        "]": "\\]",
        "*": "\\*",
        "_": "\\_",
        "$": "\\$",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def load_python_module(path: Path):
    spec = importlib.util.spec_from_file_location("lyrics_booklet_data", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Cannot load data file: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def language_font(key: str) -> str:
    return FONT_HINTS.get(key.lower(), FONT_HINTS.get(key.lower().split("-")[0], "Noto Sans"))


def normalize_languages(raw: Any) -> list[dict[str, str]]:
    if raw is None:
        raw_items: list[Any] = DEFAULT_LANGUAGES
    elif isinstance(raw, dict):
        raw_items = []
        for key, value in raw.items():
            if isinstance(value, dict):
                raw_items.append({"key": key, **value})
            else:
                raw_items.append({"key": key, "label": str(value)})
    else:
        raw_items = list(raw)

    languages: list[dict[str, str]] = []
    for item in raw_items:
        if isinstance(item, str):
            item = {"key": item}
        if not isinstance(item, dict):
            raise SystemExit(f"Invalid language entry: {item!r}")

        key = str(item.get("key") or item.get("code") or item.get("id") or "").strip()
        if not key:
            raise SystemExit("Language entries require a `key` field.")

        languages.append(
            {
                "key": key,
                "label": str(item.get("label") or key.upper()),
                "font": str(item.get("font") or language_font(key)),
                "size": str(item.get("size") or "10.5pt"),
                "style": str(item.get("style") or "normal"),
                "weight": str(item.get("weight") or "regular"),
                "fill": str(item.get("fill") or "luma(48)"),
                "width": str(item.get("width") or "1fr"),
            }
        )
    return languages


def normalize_line(raw: Any, lang_keys: list[str]) -> dict[str, str]:
    if isinstance(raw, dict):
        return {key: str(raw.get(key, "")) for key in lang_keys}
    if isinstance(raw, (list, tuple)):
        return {key: str(raw[index]) if index < len(raw) else "" for index, key in enumerate(lang_keys)}
    if raw is None:
        return {key: "" for key in lang_keys}
    return {key: str(raw) if index == 0 else "" for index, key in enumerate(lang_keys)}


def normalize_section(raw: Any, lang_keys: list[str]) -> dict[str, Any]:
    if isinstance(raw, dict):
        label = str(raw.get("label") or raw.get("name") or "")
        chorus = bool(raw.get("chorus") or raw.get("is_chorus") or False)
        raw_lines = raw.get("lines") or raw.get("pairs") or []
    elif isinstance(raw, (list, tuple)):
        if len(raw) < 2:
            raise SystemExit(f"Invalid section tuple: {raw!r}")
        label = str(raw[0] or "")
        raw_lines = raw[1] or []
        chorus = bool(raw[2]) if len(raw) > 2 else False
    else:
        raise SystemExit(f"Invalid section: {raw!r}")
    return {
        "label": label,
        "chorus": chorus,
        "lines": [normalize_line(line, lang_keys) for line in raw_lines],
    }


def normalize_track(raw: Any, index: int, lang_keys: list[str]) -> dict[str, Any]:
    if isinstance(raw, dict):
        number = str(raw.get("number") or raw.get("track") or f"{index + 1:02d}")
        title = str(raw.get("title") or f"Track {number}")
        subtitle = str(raw.get("subtitle") or raw.get("featuring") or raw.get("artist") or "")
        raw_sections = raw.get("sections") or raw.get("lyrics") or []
    elif isinstance(raw, (list, tuple)):
        if len(raw) < 4:
            raise SystemExit(f"Invalid track tuple: {raw!r}")
        number = str(raw[0])
        title = str(raw[1])
        subtitle = str(raw[2] or "")
        raw_sections = raw[3] or []
    else:
        raise SystemExit(f"Invalid track: {raw!r}")
    return {
        "number": number,
        "title": title,
        "subtitle": subtitle,
        "sections": [normalize_section(section, lang_keys) for section in raw_sections],
    }


def select_languages(languages: list[dict[str, str]], selected: str | None) -> list[dict[str, str]]:
    if not selected:
        return languages
    wanted = [item.strip() for item in selected.split(",") if item.strip()]
    by_key = {language["key"]: language for language in languages}
    missing = [key for key in wanted if key not in by_key]
    if missing:
        raise SystemExit(f"Unknown language key(s): {', '.join(missing)}")
    return [by_key[key] for key in wanted]


def transform_title(title: str, mode: str) -> str:
    if mode == "upper":
        return title.upper()
    if mode == "lower":
        return title.lower()
    if mode == "title":
        return title.title()
    return title


def text_cell(text: str, language: dict[str, str], fill: str | None = None, weight: str | None = None) -> str:
    fill_value = fill or language["fill"]
    weight_value = weight or language["weight"]
    return (
        "[\n"
        f"    #set text(font: {typst_str(language['font'])}, size: {language['size']}, "
        f"style: {typst_str(language['style'])}, weight: {typst_str(weight_value)}, "
        f"fill: {typst_color(fill_value)})\n"
        f"    {typst_text(text)}\n"
        "  ]"
    )


def header_cell(language: dict[str, str], accent: str, ui_font: str) -> str:
    label = typst_text(language["label"])
    return (
        "[\n"
        f"    #set text(font: {typst_str(ui_font)}, size: 6.5pt, weight: \"bold\", "
        f"fill: {typst_color(accent)})\n"
        f"    {label}\n"
        "  ]"
    )


def render_language_table(doc, section: dict[str, Any], languages: list[dict[str, str]], preset: dict[str, str]) -> None:
    widths = ", ".join(language["width"] for language in languages)
    doc("#table(")
    doc(f"  columns: ({widths},),")
    doc("  stroke: none,")
    doc("  inset: (x: 0mm, y: 0.7mm),")
    doc("  gutter: 3mm,")
    for language in languages:
        doc(f"  {header_cell(language, preset['accent'], preset['ui_font'])},")
    for line in section["lines"]:
        for language in languages:
            value = line.get(language["key"], "")
            weight = "bold" if section["chorus"] else None
            fill = preset["text_fill"] if section["chorus"] else None
            doc(f"  {text_cell(value, language, fill=fill, weight=weight)},")
    doc(")")


def render_language_stack(doc, section: dict[str, Any], languages: list[dict[str, str]], preset: dict[str, str]) -> None:
    for line in section["lines"]:
        doc("#grid(")
        doc("  columns: (14mm, 1fr),")
        doc("  gutter: 1.8mm,")
        for language in languages:
            label_language = {
                **language,
                "font": preset["ui_font"],
                "size": "6.5pt",
                "style": "normal",
                "weight": "bold",
                "fill": preset["accent"],
            }
            weight = "bold" if section["chorus"] else None
            fill = preset["text_fill"] if section["chorus"] else None
            doc(f"  {text_cell(language['label'], label_language)},")
            doc(f"  {text_cell(line.get(language['key'], ''), language, fill=fill, weight=weight)},")
        doc(")")
        doc("#v(2mm)")


def build_typst(
    tracks: list[dict[str, Any]],
    languages: list[dict[str, str]],
    album_title: str,
    album_subtitle: str,
    artist: str,
    label: str,
    preset_name: str,
    line_layout: str,
    margin_left: str,
    margin_right: str,
    margin_top: str,
    margin_bottom: str,
    title_size: str,
    cover_font: str | None,
    accent_color: str | None,
) -> str:
    preset = dict(PRESETS[preset_name])
    if cover_font:
        preset["cover_font"] = cover_font
    if accent_color:
        preset["accent"] = accent_color

    lines: list[str] = []
    doc = lines.append
    cover_text = "#ffffff" if preset_name == "noir" else preset["text_fill"]
    body_mode = line_layout
    if body_mode == "auto":
        body_mode = "columns" if len(languages) <= 3 else "stacked"

    doc("// Generated by lyrics-booklet")
    doc(f"#set document(title: {typst_str(album_title)}, author: {typst_str(artist)})")
    doc(f"#let accent = {typst_color(preset['accent'])}")
    doc(f"#let body-fill = {typst_color(preset['text_fill'])}")
    doc(f"#let muted-fill = {typst_color(preset['muted_fill'])}")
    doc("")
    doc("#set par(leading: 0.55em)")
    doc("#set page(")
    doc('  paper: "a4",')
    doc(f"  margin: (left: {margin_left}, right: {margin_right}, top: {margin_top}, bottom: {margin_bottom}),")
    doc("  numbering: \"1\",")
    doc("  number-align: center,")
    doc("  footer: context [")
    doc(f"    #set text(size: 7pt, font: {typst_str(preset['ui_font'])}, fill: muted-fill)")
    doc("    #counter(page).display()")
    doc("  ],")
    doc(")")
    doc("")

    # Cover
    doc(f"#set page(fill: {typst_color(preset['cover_fill'])}, margin: (x: 18mm, y: 18mm))")
    doc(f"#set text(fill: {typst_color(cover_text)})")
    doc("#align(center + horizon)[")
    doc("  #v(20mm)")
    doc(f"  #text(size: 7pt, font: {typst_str(preset['ui_font'])}, weight: \"bold\", fill: accent)[{typst_text(preset['cover_kicker'])}]")
    doc("  #v(16mm)")
    doc(f"  #text(size: 38pt, font: {typst_str(preset['cover_font'])}, weight: \"bold\")[{typst_text(album_title)}]")
    doc("  #v(5mm)")
    doc(f"  #text(size: 13pt, font: {typst_str(preset['ui_font'])}, fill: muted-fill)[{typst_text(album_subtitle)}]")
    doc("  #v(10mm)")
    doc("  #rect(width: 42mm, height: 0.7pt, fill: accent)")
    doc("  #v(10mm)")
    doc(f"  #text(size: 11pt, font: {typst_str(preset['ui_font'])})[{typst_text(artist)}]")
    if label:
        doc("  #v(4mm)")
        doc(f"  #text(size: 8pt, font: {typst_str(preset['ui_font'])}, fill: muted-fill)[{typst_text(label)}]")
    doc("]")
    doc("")

    # Body pages
    doc("#pagebreak()")
    doc(f"#set page(fill: {typst_color(preset['page_fill'])}, margin: (left: {margin_left}, right: {margin_right}, top: {margin_top}, bottom: {margin_bottom}))")
    doc(f"#set text(fill: {typst_color(preset['text_fill'])})")
    doc("")

    for track_index, track in enumerate(tracks):
        if track_index:
            doc("#pagebreak()")
        title = transform_title(track["title"], preset["title_case"])
        track_line = f"TRACK {track['number']}"
        if track["subtitle"]:
            track_line += f" / {track['subtitle']}"

        doc("#align(center)[")
        doc(f"  #text(size: 7pt, font: {typst_str(preset['ui_font'])}, weight: \"bold\", fill: accent)[{typst_text(track_line)}]")
        doc("  #v(2mm)")
        doc(f"  #text(size: {title_size}, font: {typst_str(preset['cover_font'])}, weight: \"bold\")[{typst_text(title)}]")
        doc("]")
        doc("#v(8mm)")

        for section in track["sections"]:
            label = section["label"]
            if label:
                display_label = label.upper() if section["chorus"] else label
                doc(f"#text(size: 7pt, font: {typst_str(preset['ui_font'])}, weight: \"bold\", fill: accent)[{typst_text(display_label)}]")
                doc("#v(1mm)")
                doc("#rect(width: 100%, height: 0.35pt, fill: accent)")
                doc("#v(2mm)")
            if body_mode == "stacked":
                render_language_stack(doc, section, languages, preset)
            else:
                render_language_table(doc, section, languages, preset)
                doc("#v(4mm)")

    # Back cover
    doc("#pagebreak()")
    doc(f"#set page(fill: {typst_color(preset['page_fill'])}, margin: (x: 18mm, y: 22mm))")
    doc("#align(center + horizon)[")
    doc("  #v(34mm)")
    doc(f"  #text(size: 10pt, font: {typst_str(preset['ui_font'])}, style: \"italic\", fill: muted-fill)[{typst_text(artist)} - {typst_text(album_title)}]")
    doc("  #v(30mm)")
    doc("  #rect(width: 28mm, height: 0.55pt, fill: accent)")
    doc("  #v(8mm)")
    doc(f"  #text(size: 7pt, font: {typst_str(preset['ui_font'])}, fill: muted-fill)[Typeset with Typst / lyrics-booklet]")
    doc("]")
    doc("")
    return "\n".join(lines)


def read_data(path: Path, selected_languages: str | None) -> tuple[dict[str, Any], list[dict[str, str]], list[dict[str, Any]]]:
    module = load_python_module(path)
    if not hasattr(module, "TRACKS"):
        raise SystemExit("Data file must export TRACKS.")
    meta = dict(getattr(module, "BOOKLET", {}) or getattr(module, "META", {}) or {})
    languages = normalize_languages(getattr(module, "LANGUAGES", None))
    languages = select_languages(languages, selected_languages)
    lang_keys = [language["key"] for language in languages]
    tracks = [normalize_track(track, index, lang_keys) for index, track in enumerate(module.TRACKS)]
    return meta, languages, tracks


def compile_pdf(typ_path: Path, output_path: Path, font_dirs: list[str]) -> int:
    try:
        import typst  # type: ignore
    except ImportError:
        print("Typst Python package is not installed.", file=sys.stderr)
        print("Install with: python -m pip install typst", file=sys.stderr)
        print("Or rerun with --no-pdf --typst-out booklet.typ to inspect Typst source.", file=sys.stderr)
        return 2

    pdf_bytes = typst.compile(str(typ_path), font_paths=font_dirs or None)
    output_path.write_bytes(pdf_bytes)
    print(f"PDF: {output_path} ({len(pdf_bytes) / 1024:.0f} KB)")
    return 0


def default_font_dirs() -> list[str]:
    candidates = [
        ASSET_FONT_DIR,
        Path("C:/Windows/Fonts"),
        Path("/usr/share/fonts"),
        Path("/usr/local/share/fonts"),
        Path.home() / ".local" / "share" / "fonts",
        Path.home() / "Library" / "Fonts",
        Path("/Library/Fonts"),
        Path("/System/Library/Fonts"),
    ]
    return [str(path) for path in candidates if path.exists()]


def parser_for_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a multilingual lyric booklet PDF.")
    parser.add_argument("data_module", help="Python data file exporting TRACKS.")
    parser.add_argument("--output", "-o", default="lyrics_booklet.pdf", help="Output PDF path.")
    parser.add_argument("--typst-out", help="Optional path for generated .typ source.")
    parser.add_argument("--no-pdf", action="store_true", help="Only write Typst source; do not compile PDF.")
    parser.add_argument(
        "--font-dir",
        action="append",
        default=[],
        help="Extra font directory. May be repeated. The bundled assets/fonts directory and common system font paths are searched automatically.",
    )
    parser.add_argument("--languages", help="Comma-separated language keys to include or reorder, e.g. en,zh,ja.")
    parser.add_argument("--preset", choices=sorted(PRESETS), default="gallery", help="Visual preset.")
    parser.add_argument("--line-layout", choices=["auto", "columns", "stacked"], default="auto", help="Lyrics layout.")
    parser.add_argument("--album-title", help="Cover title. Defaults to BOOKLET['album_title'] or LYRICS.")
    parser.add_argument("--album-subtitle", help="Cover subtitle. Defaults to BOOKLET['album_subtitle'].")
    parser.add_argument("--artist", help="Artist name. Defaults to BOOKLET['artist'] or Unknown.")
    parser.add_argument("--label", help="Small cover label/year line. Defaults to BOOKLET['label'].")
    parser.add_argument("--cover-font", help="Override cover/title font.")
    parser.add_argument("--accent-color", help="Override preset accent color, e.g. #7c3aed.")
    parser.add_argument("--title-size", default="22pt", help="Track title size.")
    parser.add_argument("--margin-left", default="16mm", help="Left page margin.")
    parser.add_argument("--margin-right", default="13mm", help="Right page margin.")
    parser.add_argument("--margin-top", default="15mm", help="Top page margin.")
    parser.add_argument("--margin-bottom", default="15mm", help="Bottom page margin.")
    parser.add_argument("--en-font", help="Legacy shortcut: override default English font.")
    parser.add_argument("--zh-font", help="Legacy shortcut: override default Chinese font.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = parser_for_cli()
    args = parser.parse_args(argv)

    data_path = Path(args.data_module).expanduser().resolve()
    meta, languages, tracks = read_data(data_path, args.languages)

    for language in languages:
        if args.en_font and language["key"] == "en":
            language["font"] = args.en_font
        if args.zh_font and language["key"] in {"zh", "zh-cn", "zh-hans"}:
            language["font"] = args.zh_font

    album_title = args.album_title or meta.get("album_title") or meta.get("title") or "LYRICS"
    album_subtitle = args.album_subtitle or meta.get("album_subtitle") or meta.get("subtitle") or "Multilingual Lyric Booklet"
    artist = args.artist or meta.get("artist") or "Unknown"
    label = args.label if args.label is not None else str(meta.get("label") or "")

    typ_source = build_typst(
        tracks=tracks,
        languages=languages,
        album_title=str(album_title),
        album_subtitle=str(album_subtitle),
        artist=str(artist),
        label=label,
        preset_name=args.preset,
        line_layout=args.line_layout,
        margin_left=args.margin_left,
        margin_right=args.margin_right,
        margin_top=args.margin_top,
        margin_bottom=args.margin_bottom,
        title_size=args.title_size,
        cover_font=args.cover_font,
        accent_color=args.accent_color,
    )

    output_path = Path(args.output).expanduser().resolve()
    typ_path: Path
    remove_typ = False
    if args.typst_out:
        typ_path = Path(args.typst_out).expanduser().resolve()
        typ_path.write_text(typ_source, encoding="utf-8")
    else:
        handle = tempfile.NamedTemporaryFile(mode="w", suffix=".typ", delete=False, encoding="utf-8")
        with handle:
            handle.write(typ_source)
        typ_path = Path(handle.name)
        remove_typ = True

    print(f"Loaded {len(tracks)} track(s), {len(languages)} language column(s).")
    print(f"Preset: {args.preset}; layout: {args.line_layout}.")
    font_dirs = list(dict.fromkeys(default_font_dirs() + args.font_dir))
    if font_dirs:
        print("Font paths:")
        for font_dir in font_dirs:
            print(f"  - {font_dir}")
    if args.typst_out:
        print(f"Typst source: {typ_path}")

    try:
        if args.no_pdf:
            return 0
        return compile_pdf(typ_path, output_path, font_dirs)
    finally:
        if remove_typ:
            try:
                os.unlink(typ_path)
            except OSError:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
