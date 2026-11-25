---
name: chatgpt-lane
description: Run a job on OpenAI GPT models through the Codex CLI (gpt-6.1-sol for execution, gpt-6-astra for second opinions, gpt-6-luna for bulk). Use when the user asks for GPT, Codex or ChatGPT, or when the orchestra routing table picks the GPT side. Needs the orchestra skill's scripts.
---

# ChatGPT lane (Codex CLI)

## Models

| Model | Use | Effort |
|---|---|---|
| gpt-6.1-sol | Execution from a step-by-step brief | medium, high for hard work |
| gpt-6-astra | Second opinion, design critique, image generation | high |
| gpt-6-luna | Bulk and mechanical work | low |

Always pass `-m`. The CLI's own default may be an older model.

## Run

```bash
git worktree add ../wt-<task> -b lane/<task>
../orchestra/scripts/mmo-run codex -m gpt-6.1-sol -e high --mode rw -C ../wt-<task> \
  --brief brief.md --out out/<task>.md -t 1800
../orchestra/scripts/mmo-run codex -m gpt-6-astra -e high --mode ro --brief question.md --out out/astra.md
```

- `--mode ro` uses the Codex read-only sandbox. `--mode rw` lets it edit inside the worktree only.
- Several independent jobs: one worktree each, start them all, then wait.

## After it finishes

Follow the gates in the orchestra skill: status `ok`, re-run the check yourself, read the full diff
(`git -C ../wt-<task> diff`), then merge and remove the worktree. On `limit`, move the job to the
kimi-lane or deepseek-lane; on `auth`, ask the user to run `codex login`; on `model` (exit 8, id rejected for this account) switch the model id, do not wait.

## Images

For README art and illustrations, ask gpt-6-astra to use its built-in image tool and save into the workspace
(`--mode rw` in a worktree, or `-C` a scratch folder). Spell out every label you want in quotes, then open the
file and check the spelling before you use it.
