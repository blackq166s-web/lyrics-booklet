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
                    {
                        "en": "I folded the night into a paper moon",
                        "zh": "我把夜晚折成一枚纸月亮",
                        "ja": "夜を紙の月へと折りたたむ",
                    },
                    {
                        "en": "Left it by the window, waiting for June",
                        "zh": "把它留在窗边，等六月经过",
                        "ja": "窓辺に置いて、六月を待つ",
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
                    },
                    {
                        "en": "We are small, but the sky has room",
                        "zh": "我们渺小，但天空足够宽",
                        "ja": "小さな僕らにも、空は広い",
                    },
                ],
            },
        ],
    },
    {
        "number": "02",
        "title": "Afterimage",
        "sections": [
            ("Intro", [
                ("The streetlights tremble after rain", "雨后街灯轻轻颤动", "雨上がりの街灯が揺れる"),
                ("Your name returns, then fades again", "你的名字回来，又慢慢淡去", "君の名が戻り、また薄れてゆく"),
            ]),
        ],
    },
]
