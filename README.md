# makefun-news21

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/woodhntr1-gif/makefun-news21/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/woodhntr1-gif/makefun-news21/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

The World in One Image — 21 November 2026. A one-page newspaper front page drawn entirely in code (Pillow) that sums up the world's news of Saturday, 21 November 2026, in a single 1024×1024 image.

What the picture holds: the lead story is Iran striking US bases in Bahrain, illustrated with a small geometric drawing of Bahrain's skyline on the Gulf and a naval ship. Six cards below it cover the Russian missile that hit Zelensky's hometown of Kryvyi Rih, the AI sell-off dragging markets into correction, Mexico capturing FBI most-wanted cartel boss "El Chapo Isidro", COP31 running past its deadline over fossil fuels, the UK and EU signing three post-Brexit deals, and the claimed AI-assisted proof of the Riemann hypothesis. A strip of six short briefs follows: an Israeli strike killing three in a Gaza food vehicle, Saudi defences intercepting three Houthi missiles, drones hitting the Russian cargo ship Sparta II, France's nationwide protests, Bolsonaro taken to ICU in Brasilia, and the EU–Indonesia trade deal.

The news was taken from reporting by One Turn, Reuters, the NYT and the Telegraph on 21 November 2026. Honest note: this entry was built on 22 November 2026 and covers news reported on 21 November 2026, before that day's deadline. The Riemann story is worded as a claim, not a confirmed fact. The drawing is fully deterministic — rendering it twice produces byte-identical output.

## Run it

```sh
python3 main.py
```

That copies the pre-rendered `entry.png` (1024×1024) into the working directory, or into `$MAKEFUN_OUTPUT_DIR` when it is set. Nothing is drawn while the program runs — `render.py` documents how the picture was drawn (Pillow, fully deterministic), and `main.py` only copies the exact bytes.

## Verification

The picture was rendered twice from `render.py` and both renders were byte-identical (md5 `ebb0d7e0b3e8de77a89c93a152f8b608`). `main.py` was tested with an empty environment and `$MAKEFUN_OUTPUT_DIR` set to two different directories: both runs exited 0 and wrote bytes identical to `entry.png` in the repository. It was also run without the output variable, from another directory and from inside the repository itself, and exited 0 every time. The runtime program imports nothing but the standard library — no Pillow, no fonts, no image libraries — so it cannot fail for a missing rendering dependency. `entry.png` is 1024×1024 and under 1 MiB.

---

<sub>Entered on [make.fun](https://make.fun/?ref=rez34v58&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
