---
name: rate-engine
description: >
  Computes the OPEN offer, the TARGET and the private MAX for a creator deal from the
  user's own rate bands, and how a creator's ask compares. Also sets the bands up, by
  interview or from past deals. Use for "what should I offer X", "is their ask
  reasonable", "what's our max", "price this collab", "set up my rates".
---

# Rate engine

Every figure in a creator email originates here. Never invented in the playbook,
never guessed in a draft, never typed from memory.

**Drafting a reply** needs only `references/using-the-card.md` (running `inbox rate`,
reading its card, the rules for a number in a draft). This file adds fee bands for
rate-card programs, rates setup and the advanced warehouse mode.

## Rate-card programs (fee bands)

Programs that price by format rather than by views (`pricing: rate-card` in
`program.md`, common for UGC) write fee ranges with `unit=fee`:

```
ugc_video: low=150 typical=200 high=300 unit=fee
```

`inbox rate --format ugc_video [--ask 350]` then returns OPEN / TARGET / MAX
from the range itself; views and geo are optional. `pricing: their-quote` uses either
kind of band to read the creator's quote (`--ask`). A no-fee program (its module says so)
doesn't use the engine.

## Set up rates ("set up my rates", about 10 minutes)

`references/setup-rates.md`: from past deals (`inbox rate-bands --csv`) or a guided
interview; it writes the ```rates block in the user's `rates.md`.

## Advanced mode: benchmarks from your own warehouse

For teams with a data warehouse of paid posts joined to attributed outcomes.
Adds own-history pricing for known creators, a per-creator price book, bulk
re-onboarding (`--bulk`), and automatic promo-code and link leak detection.

- Setup and refresh: `references/README.md` + `references/refresh_queries.sql`.
- Output lives in `~/.claude/inbox/rates/` (never in the plugin, never in git:
  `creators_snapshot.json` names creators alongside fees - treat it like a payroll
  export).
- Run: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/rate-engine/scripts/rate_engine.py" --platform youtube --niche <niche> --tier T1 --views 25000 --deliverable yt_integration --ask 1200`
  (or `--handle <handle>` for a known creator). Without populated benchmarks it runs
  in advisory mode and refuses to print a card.

The method: `references/README.md`.
