# news-image-20261122 — THE FULL DAY (ATLAS v6)

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Yuu078/news-image-20261122-atlas-v6/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Yuu078/news-image-20261122-atlas-v6/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One-page newspaper poster summing up the world's news of **Sunday 22 November 2026**:
16 stories across 7 regions, led by the tanker strikes in the Strait of Hormuz,
with the COP31 collapse as second lead.

Built for the [make.fun](https://make.fun/bounty/news-image-20261122) bounty
**news-image-20261122** ("Sum up 22 November's world news in one image").

## What it is

- `entry.png` — the poster itself, 1024×1024 PNG (123,295 bytes).
- `render_full_day.py` — the program that draws the poster from scratch
  with Pillow (black masthead, illustrated Hormuz hero, COP31 second lead,
  Serang rail card, 8 illustrated story cards, an ALSO TODAY band with 5
  more stories, a DATE CHECK box and a wire-checked stamp). Run it twice
  and the bytes are identical.
- `main.py` — the entry program: pure standard library. It validates the
  bundled poster's dimensions and size, copies it to `MAKEFUN_OUTPUT_DIR`
  (default: the repo folder) and verifies the copy by SHA-256.

## How to run

```sh
python3 render_full_day.py   # rebuild entry.png (deterministic)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # write out/entry.png
```

## License

MIT — see `LICENSE`.
