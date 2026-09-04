# New voices (40)

Click a **sample** to listen, click the **pack** to download. Every file is a native Supertonic-3 `voice_style` JSON: `tts.get_voice_style_from_path(...)` in Python, or copy it into `voice_styles/` for audio.cpp. Officials for comparison: [F1](../samples/en/F1.mp3) [F2](../samples/en/F2.mp3) [F3](../samples/en/F3.mp3) [F4](../samples/en/F4.mp3) [F5](../samples/en/F5.mp3) [M1](../samples/en/M1.mp3) [M2](../samples/en/M2.mp3) [M3](../samples/en/M3.mp3) [M4](../samples/en/M4.mp3) [M5](../samples/en/M5.mp3) . Ranked by UTMOSv2 (predicted MOS, higher is better); officials range 2.58..3.40. Gender/age from audeering wav2vec2, PQ = Audiobox-Aesthetics production quality (officials 7.68..8.10). All 40 have WER 0 vs. reference text. Recipe = base → target at t (t>1 extrapolates past the target) plus slider offsets.

| # | voice | sample | MOS | sex | age | PQ | recipe |
|---|---|---|---|---|---|---|---|
| 1 | [`P23.json`](P23.json) | [▶ en](../samples/en/P23.mp3) | 3.625 | M | 23 | 7.92 | M4 → M5 @ 0.75 · speed -0.5 |
| 2 | [`P35.json`](P35.json) | [▶ en](../samples/en/P35.mp3) | 3.51 | M | 25 | 7.77 | M1 → M5 @ 1.5 |
| 3 | [`P12.json`](P12.json) | [▶ en](../samples/en/P12.mp3) | 3.508 | F | 28 | 7.72 | F5 → M1 @ 0.5 · ax5 +1, gender +0.5 |
| 4 | [`P26.json`](P26.json) | [▶ en](../samples/en/P26.mp3) | 3.492 | M | 26 | 7.79 | M1 → M5 @ 1.75 · speed -0.25 |
| 5 | [`P01.json`](P01.json) | [▶ en](../samples/en/P01.mp3) | 3.424 | F | 43 | 7.84 | F1 → F3 @ 1.5 · speed +0.5 |
| 6 | [`P36.json`](P36.json) | [▶ en](../samples/en/P36.mp3) | 3.414 | M | 47 | 7.81 | F1 → M5 @ 2.25 |
| 7 | [`P10.json`](P10.json) | [▶ en](../samples/en/P10.mp3) | 3.398 | M | 26 | 7.68 | F1 → M4 @ 1.5 |
| 8 | [`P03.json`](P03.json) | [▶ en](../samples/en/P03.mp3) | 3.352 | M | 38 | 7.82 | F5 → M3 @ 0.75 · speed -0.5, gender -1.75 |
| 9 | [`P08.json`](P08.json) | [▶ en](../samples/en/P08.mp3) | 3.316 | M | 36 | 7.68 | M1 → M2 @ 2.25 |
| 10 | [`P00.json`](P00.json) | [▶ en](../samples/en/P00.mp3) | 3.295 | M | 29 | 7.96 | F2 → M5 @ 0.75 |
| 11 | [`P22.json`](P22.json) | [▶ en](../samples/en/P22.mp3) | 3.254 | F | 29 | 7.85 | F3 → F4 @ 0.5 |
| 12 | [`P14.json`](P14.json) | [▶ en](../samples/en/P14.mp3) | 3.219 | M | 25 | 7.28 | M3 → M4 @ 1.75 · ax5 +1 |
| 13 | [`P28.json`](P28.json) | [▶ en](../samples/en/P28.mp3) | 3.146 | M | 39 | 7.54 | M4 → M5 @ 1.0 · speed +1.5, ax3 -2.75 |
| 14 | [`P06.json`](P06.json) | [▶ en](../samples/en/P06.mp3) | 3.141 | M | 25 | 7.64 | F3 → M4 @ 1.5 |
| 15 | [`P04.json`](P04.json) | [▶ en](../samples/en/P04.mp3) | 3.139 | M | 38 | 7.8 | M3 → M5 @ 1.5 · ax5 +1.25, ax2 -0.25 |
| 16 | [`P30.json`](P30.json) | [▶ en](../samples/en/P30.mp3) | 3.119 | M | 30 | 8.0 | F3 → M2 @ 0.75 |
| 17 | [`P27.json`](P27.json) | [▶ en](../samples/en/P27.mp3) | 3.109 | M | 31 | 7.94 | F2 → M5 @ 1.75 · ax9 +1 |
| 18 | [`P07.json`](P07.json) | [▶ en](../samples/en/P07.mp3) | 3.102 | M | 33 | 7.87 | F2 → M5 @ 2.0 |
| 19 | [`P24.json`](P24.json) | [▶ en](../samples/en/P24.mp3) | 3.098 | F | 26 | 7.65 | F4 → F5 @ 0.5 · ax5 +1 |
| 20 | [`P02.json`](P02.json) | [▶ en](../samples/en/P02.mp3) | 3.096 | F | 26 | 7.77 | F1 → F5 @ 0.5 |
| 21 | [`P20.json`](P20.json) | [▶ en](../samples/en/P20.mp3) | 3.088 | F | 43 | 7.31 | F2 → F3 @ 2.75 |
| 22 | [`P31.json`](P31.json) | [▶ en](../samples/en/P31.mp3) | 3.086 | M | 27 | 7.3 | F2 → M3 @ 2.75 · gender +0.75 |
| 23 | [`P09.json`](P09.json) | [▶ en](../samples/en/P09.mp3) | 3.086 | F | 50 | 7.59 | F2 → F3 @ 2.75 · age +1.25 |
| 24 | [`P15.json`](P15.json) | [▶ en](../samples/en/P15.mp3) | 3.072 | M | 23 | 7.87 | F3 → M5 @ 0.5 |
| 25 | [`P32.json`](P32.json) | [▶ en](../samples/en/P32.mp3) | 3.027 | M | 33 | 7.98 | M1 → M2 @ 0.75 · speed +1.25, ax9 +0.75 |
| 26 | [`P16.json`](P16.json) | [▶ en](../samples/en/P16.mp3) | 3.014 | M | 41 | 7.54 | F3 → M5 @ 2.75 |
| 27 | [`P05.json`](P05.json) | [▶ en](../samples/en/P05.mp3) | 2.994 | M | 37 | 7.59 | F5 → M5 @ 1.75 · ax2 -0.5, arousal -2.5 |
| 28 | [`P19.json`](P19.json) | [▶ en](../samples/en/P19.mp3) | 2.986 | M | 19 | 7.77 | F4 → M4 @ 1.0 · ax9 +1.25 |
| 29 | [`P38.json`](P38.json) | [▶ en](../samples/en/P38.mp3) | 2.979 | F | 32 | 7.86 | F1 → M1 @ 0.5 · speed +0.75 |
| 30 | [`P13.json`](P13.json) | [▶ en](../samples/en/P13.mp3) | 2.969 | F | 28 | 7.85 | F1 → F5 @ 0.75 · arousal +0.5 |
| 31 | [`P17.json`](P17.json) | [▶ en](../samples/en/P17.mp3) | 2.947 | M | 33 | 7.93 | F5 → M5 @ 1.5 · speed +1.25 |
| 32 | [`P21.json`](P21.json) | [▶ en](../samples/en/P21.mp3) | 2.93 | M | 40 | 7.61 | F4 → M4 @ 2.75 · arousal +0.5, ax7 -1.25 |
| 33 | [`P11.json`](P11.json) | [▶ en](../samples/en/P11.mp3) | 2.9 | M | 35 | 7.76 | M2 → M5 @ 1.25 · ax7 -0.5, ax3 -1.5 |
| 34 | [`P34.json`](P34.json) | [▶ en](../samples/en/P34.mp3) | 2.867 | M | 23 | 7.84 | F5 → M3 @ 0.75 |
| 35 | [`P29.json`](P29.json) | [▶ en](../samples/en/P29.mp3) | 2.797 | M | 24 | 7.85 | F3 → M3 @ 0.75 · ax3 -1.25 |
| 36 | [`P18.json`](P18.json) | [▶ en](../samples/en/P18.mp3) | 2.729 | M | 38 | 7.81 | F4 → M3 @ 2.25 · ax5 +1.25, age +0.75 |
| 37 | [`P37.json`](P37.json) | [▶ en](../samples/en/P37.mp3) | 2.689 | M | 31 | 7.91 | F3 → M1 @ 0.75 · ax2 +0.5, ax3 -1.5 |
| 38 | [`P39.json`](P39.json) | [▶ en](../samples/en/P39.mp3) | 2.682 | M | 21 | 7.47 | M2 → M4 @ 1.75 |
| 39 | [`P25.json`](P25.json) | [▶ en](../samples/en/P25.mp3) | 2.645 | M | 19 | 7.09 | M1 → M4 @ 2.25 |
| 40 | [`P33.json`](P33.json) | [▶ en](../samples/en/P33.mp3) | 2.461 | F | 20 | 6.77 | F2 → F5 @ 3.0 · ax2 -0.5, age -5.25 |
