# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/muse431/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/muse431/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-image newspaper front page summing up Monday 23 November 2026 in thirty stories: Nvidia reinstates Jensen Huang and the markets snap back, Ukraine sinks the Russian corvette Merkury off Libya, the COP31 climate talks collapse with no deal, Verstappen wins a 35-lead-change thriller in Las Vegas, Modi and Nepal's Prime Minister Shah reset ties in Delhi, and the Wellington Test ends in a draw — plus twenty more stories from the day, in brief. Every story was checked against at least two independent reports, and no figure in the image comes from a single outlet.

## Run it

```sh
python3 draw_poster.py   # redraws poster.png from the story list (no network)
python3 main.py          # copies poster.png to /output/entry.png
```

The poster is 1024×1024 and under 1 MiB. It is drawn entirely by `draw_poster.py` with Pillow — masthead, a large red date band reading MONDAY 23 NOVEMBER 2026, nine feature stories and a twenty-item "rest of the day" grid — from the hand-written story list in the same file. The news was researched on the full day of 23 November 2026 and every story cross-checked in at least two independent outlets (Reuters, AP, CNN, Al Jazeera, NHK, Dawn, Formula 1, ESPNcricinfo and others).

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
