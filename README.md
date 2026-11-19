# The World Today — Thursday 19 November 2026

[![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/contact-nathanealphi/news-image-20261119-b/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/contact-nathanealphi/news-image-20261119-b/reward.svg)](https://make.fun/bounty/news-image-20261119)

A bold modern, photo-led front page summing up the world's news of
Thursday 19 November 2026, drawn entirely with Pillow primitives
(no photos, no copied artwork).

Lead story: the first three-way summit of Trump, Xi and Putin in
Shenzhen. Also: Gulf strikes, the Kerch Bridge, Anthropic's Nasdaq
debut as ANT, Gaza floods, Israel's government talks — plus ICJ/Myanmar,
the EU–Indonesia trade deal, Voyager 1 and North Korea in ALSO TODAY.

## How it works

- `tools/render.py` draws `assets/entry.png` (1024x1024, under 1 MiB),
  deterministic: no network, no randomness, no timestamps.
- `main.py` (Python 3.13, standard library only) copies
  `assets/entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Reproduce

```sh
python3 tools/render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
