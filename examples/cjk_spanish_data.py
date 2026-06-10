BOOKLET = {
    "album_title": "Five Scripts Demo",
    "album_subtitle": "中文 / 日本語 / 한국어 / English / Español",
    "artist": "Lyrics Booklet",
    "label": "CJK + Spanish coverage demo",
}

LANGUAGES = [
    {"key": "en", "label": "English", "font": "Inter", "style": "italic", "width": "1fr"},
    {"key": "zh", "label": "中文", "font": "Noto Sans SC", "width": "1fr"},
    {"key": "ja", "label": "日本語", "font": "Noto Sans JP", "width": "1fr"},
    {"key": "ko", "label": "한국어", "font": "Noto Sans KR", "width": "1fr"},
    {"key": "es", "label": "Español", "font": "Inter", "style": "italic", "width": "1fr"},
]

TRACKS = [
    {
        "number": "01",
        "title": "Five Scripts",
        "subtitle": "layout stress test",
        "sections": [
            {
                "label": "Verse 1",
                "lines": [
                    {
                        "en": "The paper moon is rising over town",
                        "zh": "纸月亮正从城市上空升起",
                        "ja": "紙の月が街の上に昇る",
                        "ko": "종이 달이 도시 위로 떠오른다",
                        "es": "La luna de papel sube sobre la ciudad",
                    },
                    {
                        "en": "Every window keeps a little sound",
                        "zh": "每扇窗都收藏一点声音",
                        "ja": "どの窓にも小さな音が残る",
                        "ko": "모든 창문마다 작은 소리가 남아 있다",
                        "es": "Cada ventana guarda un pequeño sonido",
                    },
                ],
            },
            {
                "label": "Chorus",
                "chorus": True,
                "lines": [
                    {
                        "en": "Hold the light, let the silence bloom",
                        "zh": "握住光，让沉默开花",
                        "ja": "光を抱き、静けさを咲かせて",
                        "ko": "빛을 붙잡고 침묵을 피워",
                        "es": "Sostén la luz, deja florecer el silencio",
                    },
                ],
            },
        ],
    },
]
