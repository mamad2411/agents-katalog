---
name: verify
description: How to verify a change to a skill, agent or reference in this repo by running a headless Claude against the working tree's plugins, not the installed cache.
---

# Verify a skill or agent change

The surface is the agent: run `claude -p` with this checkout's plugins and
read which skills it called and what it answered.

## Run

```bash
S=$(mktemp -d) && mkdir -p "$S/proj" && cd "$S/proj"
# a tiny fake project the prompt can talk about (package.json, README)
claude -p --setting-sources project \
  --plugin-dir /path/to/this/repo/plugins \
  --model sonnet --output-format stream-json --verbose \
  --max-turns 20 --permission-mode bypassPermissions \
  "<the user's prompt, in their words>" </dev/null > "$S/run.jsonl"
```

- `--setting-sources project` skips user settings, so the installed copies of
  these plugins do not load next to the working tree's.
- `--bare` does not work with a claude.ai login: it answers "Not logged in".
- `</dev/null` avoids a 3 s stdin wait.
- Run several prompts in parallel with `&` and `wait`; each is one session.

## Read

Print each `tool_use` (name and input) and the final `result` from the
stream-json. The checks that matter:

- did the router (`frontend-stack:frontend-stack`) load on its own, without
  the prompt naming it? Run once with and once without
  `/frontend-stack:frontend-stack` at the start, to tell a trigger problem
  from a routing problem;
- which reference it read and which skills it loaded, in order;
- whether it stopped where the flow says to stop (questions before any
  direction or code).

## Gotchas

- `pip install tiktoken` fails on PEP 668 systems; use
  `uv run --with tiktoken python3 scripts/token_budget.py`.
- CI also runs `claude plugin validate` on each `plugins/*/`, not only the
  root.
