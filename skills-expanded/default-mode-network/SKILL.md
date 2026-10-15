---
name: default-mode-network
description: A taste-driven autoresearcher — the idle network of an AI mind. Wanders through the user's interests, hits public search APIs (Wikipedia, ArXiv, HN, DuckDuckGo, ...), scores findings against a virtual-dopamine reward, and writes short markdown briefs to a local journal.
---

# default-mode-network

This skill drives the `default-mode-network` (DMN) repo.

The full agent instructions live in `program.md` at the repo root. **Read `program.md` first** — it tells you exactly how to set up a profile, run a wandering session, and report back to the user with the top-3 highest-dopamine briefs.

Quick reference:

- `uv run prepare.py --interactive` — first-run cold-start interview (agents: your shell is non-interactive — ask the questions in chat and pipe the answers in, one line each; see program.md Setup)
- `uv run prepare.py --dry-run` — synthetic profile, no input needed
- `uv run prepare.py --import browser,youtube,gmail,drive,twitter,readwise [--takeout-dir …]` — importers
- `uv run explore.py` — one wandering session, default 12-minute wall-clock budget
- `uv run explore.py --minutes 5` — quick browse
- `uv run explore.py --iterations 12` — reproducible iteration cap
- `uv run explore.py --dry-run --iterations 2` — no-API-key smoke test
- `uv run explore.py --generate --modalities image,music` — attach generative-media artifacts
- `uv run explore.py --seed "freetext question"` — single explicit seed override
- `uv run profiles.py export --out me.dmn.json` — share / back up the taste profile
- `uv run profiles.py import friend.dmn.json --replace` — load someone else's profile

LLM provider via `DMN_LLM_PROVIDER`: `anthropic`, `openai`, `ollama`, `lmstudio`, `stub`.
For fully-local wandering use `ollama` or `lmstudio`.

The user's taste profile, embeddings, and journal stay local. Don't upload them anywhere. Don't modify files under `dmn/` unless the user asks.
