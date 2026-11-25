---
name: outcome-check
description: When you're about to claim a previous fix worked, or are tempted to repeat an approach Claude Code has tried in this repo before, consult the outcome telemetry. presence tracks every commit Claude made and watches for reverts. Look up "did my last attempt at X stick?" before re-trying.
---

# Outcome check: learn from your own past

`presence` records every commit you make (`~/.claude/presence/telemetry/claims.jsonl`) and scans for reverts in subsequent sessions (`outcomes.jsonl`). When you're about to do something you've done before in this repo, **check first whether it worked**.

## When this skill should fire

- You're about to fix a bug in a file you've previously fixed.
- You're proposing an architectural change you suspect was tried before.
- A user asks "didn't you fix this?" or "this looks familiar."
- You're about to commit something with a message similar to an earlier commit.

## How to consult

```bash
PRESENCE_ROOT="${CLAUDE_PLUGIN_ROOT:-$(realpath ~/.claude/plugins/presence 2>/dev/null || echo .)}"
PYTHONPATH="$PRESENCE_ROOT/lib" python3 -c "
from _common import read_jsonl, repo_id
from telemetry import claims_path, outcomes_path
rid = repo_id('$PWD')
claims = [c for c in read_jsonl(claims_path()) if c.get('repo') == rid]
outcomes = read_jsonl(outcomes_path())
reverted_shas = {o['sha'] for o in outcomes if o.get('kind') == 'revert'}
for c in claims[-20:]:
    sha = c.get('sha', '?')[:8]
    msg = (c.get('message') or '')[:80]
    fate = '  REVERTED' if c.get('sha') in reverted_shas else '  '
    print(f'{sha} {fate} {msg}')
"
```

## How to apply what you find

If a similar approach was reverted, **acknowledge it explicitly to the user** before retrying:

> "Note: I committed something similar last week (`a1b2c3d4`) and it was reverted within 24h. Likely cause: <hypothesis>. I'll try a different approach this time, specifically: <how this attempt differs>."

If the previous attempt landed cleanly, you can reference it as a precedent rather than re-explaining the rationale.

## What this skill does NOT do

- Predict whether your *next* commit will be reverted. presence has no model of code quality; it just records facts.
- Read PR comments or external review feedback. Only commit-graph signals are tracked.
- Modify your behavior automatically. The skill helps you make informed choices; the choice is still yours.
