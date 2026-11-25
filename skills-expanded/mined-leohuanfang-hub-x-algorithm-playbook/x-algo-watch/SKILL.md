---
name: x-algo-watch
description: Check what changed in X's open-source For You algorithm since a date, explain each change in plain English, and update this repo's CHANGELOG.md and RULES.md. Use when the user asks "did the X algorithm change", "what's new in the X algorithm", or wants to refresh the playbook.
---

# X algorithm watch

1. Run `python3 scripts/param_history.py --since <date>` from the repo root. It clones or updates github.com/xai-org/x-algorithm into `.x-algorithm/` and lists every parameter change in `home-mixer/params/param.rs` since that date.
2. Ignore experiment plumbing (salts, tracked IDs, parameters added and removed in the same week) unless they change behavior.
3. For each remaining change, write one line: what changed, old → new, and what it means for someone posting on X. If the meaning is unclear, read the code that uses the parameter (`grep -rn <ParamName> .x-algorithm`) before explaining; say "unclear" rather than guessing.
4. Also skim `git -C .x-algorithm log --since <date> --stat` for new filters, scorers or rules files (`home-mixer/filters/`, `home-mixer/scorers/`, `abuse-enforcement-service/`), and the README's "Notable Updates".
5. Update `CHANGELOG.md` (newest first, with commit hashes) and any affected line in `RULES.md`, including the pinned commit at the top.
6. Summarize for the user in 5 lines or fewer: the changes that matter for posting, and which checklist item (if any) changes.
