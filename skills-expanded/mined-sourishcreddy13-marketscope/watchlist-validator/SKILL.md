---
name: watchlist-validator
description: Deterministically validates MarketScope watchlist payloads against the root watchlist rules before test generation or implementation handoff.
---

# Watchlist Validator

Use this skill whenever an agent creates or changes watchlist fixtures, seed payloads, API examples, or test vectors.

## Rules

A watchlist payload must have:

- a string `name` containing non-whitespace text
- a `symbols` array
- at least one symbol
- no duplicate symbols after trimming and upper-casing

The specification caps a customer at 10 watchlists; it sets no per-watchlist symbol limit, so none is enforced here.

The skill validates structural rules only. It does not verify stock existence or customer authorization because those require application context.

## Invocation

```bash
python .claude/skills/watchlist-validator/watchlist_validator.py --input <json-file>
```

Exit codes:

- `0` valid
- `1` domain validation failure
- `2` input/CLI failure
