---
name: kimi-lane
description: Run a job on Kimi models through the Kimi Code CLI (kimi -p): cheap execution of easy, testable work in its own git worktree, or a quick extra opinion. Use when the user asks for Kimi, when other lanes hit their limits, or when the orchestra routing table picks Kimi. Needs the orchestra skill's scripts.
---

# Kimi lane (Kimi Code CLI)

## Models

| Alias | Use |
|---|---|
| kimi-code/k3.1-pro | Default. Execution from explicit steps, opinions |
| kimi-code/k3.1-pro-highspeed | Same model, faster; needs a higher Kimi plan (else `status=limit`) |

`kimi` reads its model aliases from its config file. List them with `mmo-preflight`.

## Run

```bash
git worktree add ../wt-<task> -b lane/<task>
../orchestra/scripts/mmo-run kimi --mode rw -C ../wt-<task> --brief brief.md --out out/<task>.md
../orchestra/scripts/mmo-run kimi --mode ro --brief q.md --out out/kimi.md
```

`kimi -p` applies edits without asking, so the runner refuses `--mode rw`
outside a linked worktree. The runner reads the last assistant message from Kimi's JSON stream.

## Brief

Kimi does best with very explicit briefs: numbered steps, exact file names, the exact test command,
and a short list of things it must not do. Give it one job per run.

## After it finishes

Same gates as every lane: status `ok`, re-run the check, read the diff, merge. On `model` (exit 8) pick another model id from the table. On `limit` move to the
chatgpt-lane or deepseek-lane. On `auth` ask the user to log in to Kimi Code again.

## Read-only lanes

Kimi Code has no read-only sandbox: `kimi -p` may edit files even when told not to. In `--mode ro` the
runner gives it a throwaway detached worktree (or an empty folder outside git), discards whatever it wrote,
and marks the header `ro_violation=yes` if it tried.
