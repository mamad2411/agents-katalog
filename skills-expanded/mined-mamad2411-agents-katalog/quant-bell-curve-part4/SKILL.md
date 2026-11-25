---
name: quant-bell-curve-part4
description: The Bell Curve video, Quant finance from scratch part 4 (@quantfinancetogo) - the 16-line numpy script transcribed from the video, runnable with built-in checks, plus what each line shows (coin flips pile into a bell, 400-step walks spread by sqrt(400), 68-95-99.7, 16% a year, why real returns have fat tails). Use to learn or teach the normal distribution with simulation, or to rerun the video's numbers.
---

# The bell curve from scratch

Source: a 144-second video by @quantfinancetogo; footer "simulated prices, education only, not financial advice". The code is in `scripts/bell_curve_from_scratch.py` (transcribed from the last frame; comments shortened). Run: `python scripts/bell_curve_from_scratch.py` (needs numpy). Checks at the bottom are mine and pass.

| Lines | What it does | Result when run [Certain] |
|---|---|---|
| 2 to 6 | 1,000 balls, 12 coin flips each, count rights | Counts pile near 6 of 12 |
| 7 to 9 | Part 3's walks: 1,000 walks of 400 steps | Spread of final positions about 19.9, close to sqrt(400) = 20 |
| 10 to 13 | 100,000 sums of 100 flat random moves; share within 1, 2, 3 standard deviations | 0.682, 0.955, 0.997: the 68-95-99.7 rule |
| 14 to 15 | Daily 1% move over 252 days | 16%, 32%, 48% (1, 2, 3 years) |
| 16 | 1 / share beyond 3 standard deviations | About 1 in 360; the exact normal figure is about 1 in 370 |

Video claim: "With 16% a year: 2 years in 3 within 16%, and 19 in 20 within 32%." Matches the 68% and 95% rows.

## Limits

The video itself shows that real returns have fat tails (a simulated market with moves beyond 4 standard deviations), so the bell curve understates extreme days. Treat the script as a teaching tool, not a risk model. Use `/bell-curve`.
