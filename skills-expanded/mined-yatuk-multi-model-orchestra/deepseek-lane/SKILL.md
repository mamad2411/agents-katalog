---
name: deepseek-lane
description: Run a job on DeepSeek models (deepseek-v4-pro, deepseek-flash) through the Kimi Code CLI with a DeepSeek provider configured: an independent opinion from another model family, cheap execution, or bulk labeling. Use when the user asks for DeepSeek or the orchestra routing table picks it. Needs the orchestra skill's scripts.
---

# DeepSeek lane (via Kimi Code CLI)

The Kimi Code CLI can talk to any provider listed in its config. Add DeepSeek there once
(provider + model aliases `deepseek/deepseek-v4-pro` and `deepseek/deepseek-flash`); `mmo-preflight`
then shows the lane as available.

## Models

| Alias | Use |
|---|---|
| deepseek/deepseek-v4-pro | Third opinion from a non-GPT, non-Claude family; cheap execution |
| deepseek/deepseek-flash | Bulk labeling and cleanup, fast and cheap |

## Run

```bash
../orchestra/scripts/mmo-run deepseek --mode ro --brief q.md --out out/ds.md
../orchestra/scripts/mmo-run deepseek -m deepseek/deepseek-flash --mode ro --brief bulk.md --out out/labels.md
git worktree add ../wt-<task> -b lane/<task>
../orchestra/scripts/mmo-run deepseek --mode rw -C ../wt-<task> --brief brief.md --out out/<task>.md
```

## Failures

DeepSeek is prepaid. An empty balance shows up as HTTP 402 and the runner reports `status=limit` (exit 6). A rejected model id is `status=model` (exit 8): pick another id, do not wait.
Tell the user, route the job to the fallback lane, and do not retry in a loop.
