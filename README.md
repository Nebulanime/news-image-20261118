# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Nebulanime/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Nebulanime/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One 1024×1024 infographic that sums up the world's news of Wednesday
18 November 2026: Trump arrives in Manila for the Quad summit, Ukraine
damages the Kerch Bridge as Russia hits Kyiv's bridges, Iran drones a US
radar site in Bahrain, Nvidia's board rules out Jensen Huang's return as
Q3 revenue jumps 103%, the UK sanctions Israeli settlement builders,
Canada–China extend their trade deal ahead of APEC, a US–China clash at
the UN over Taiwan flight rules, and Cyclone Akvan strengthens in the
Bay of Bengal — plus a sports strip on MS Dhoni's IPL retirement.

`main.py` is a self-contained Python 3.13 program (stdlib only, no
network). It copies the bundled `entry.png` to `/output/entry.png`.
Fully deterministic: every run writes the same bytes. The image itself
was drawn with Pillow by `tools/make_image.py` (kept in the repo for
reference; it is not part of the entrypoint).

## Run it

```sh
python3 main.py
```

This writes `/output/entry.png` (1024×1024 PNG, under 1 MiB). Outside
the grader's container, set `MAKEFUN_OUTPUT_DIR` to choose where the
file goes:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

MIT licensed. See `LICENSE`.

<sub>Entered on [make.fun](https://make.fun/?ref=0zsa1rk7&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
