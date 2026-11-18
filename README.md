# news-image-20261117-r2

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/kazamisao/news-image-20261117-r2/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/kazamisao/news-image-20261117-r2/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

Round 2: a one-page illustrated broadsheet of the world news of Tuesday, 17 November 2026, drawn in code with Pillow. A hero panel on the Kerch Bridge strike; six panels on the Hormuz tanker attacks, the Zaporizhzhia strike, the Western call to open Gaza's crossings, the COP31 draft deal, the US losing its measles-free status, and Trump landing in Manila; plus an "Also today" strip on Japan's jet scramble, the US outages, Nvidia's earnings, the Kemerovo crash, the French protests and Ebola in DR Congo — twelve stories in all. `render.py` draws the image at 3x and downscales it to `news.png`; `main.py` (stdlib only) copies it to the output path, byte-identical on every run.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=p5dwa49p&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
