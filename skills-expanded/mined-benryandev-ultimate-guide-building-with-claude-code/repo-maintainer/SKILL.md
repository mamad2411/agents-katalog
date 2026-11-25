---
name: repo-maintainer
description: Maintain the companion repo examples and docs. Use when updating examples, adding new configs, verifying documentation accuracy against current Claude Code releases, or preparing a refresh.
---

# Repo Maintainer

## When to Use
When updating this repo's example configs, docs, or README -- especially when
re-verifying it against a newer Claude Code release.

## Verification Pass
1. Check the installed version: `claude --version`. Compare against the "Last
   verified against" line in README.md.
2. Read the [CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md)
   from the last verified version forward. Note anything touching memory, skills,
   plugins, hooks, subagents, agent teams, workflows, models, or settings keys.
3. Re-check these high-churn facts against code.claude.com, because they have all
   moved before:
   - Model lineup, aliases, context windows, and per-Mtok pricing
   - Default `teammateMode` and whether Agent Teams is still flag-gated
   - Settings keys that have been removed (e.g. `teammateDefaultModel`)
   - CLAUDE.md size guidance and auto-memory load limits
   - Hook event names and exit-code semantics
   - Subagent and workflow caps
4. Grep for stale markers before assuming the repo is clean:
   `grep -rn -iE "delegate mode|[0-9]+.layer|under [0-9]+ lines" --include='*.md' .`

## Validation
- `jq empty` on every JSON example
- `bash -n` on every shell example
- Resolve every relative Markdown link; broken links are the most common regression

## Writing Rules
- Record corrections in `CHANGELOG.md`, separating "changed since" from "was wrong
  when written". Never silently delete an error.
- Update the "Last verified against" line in README.md at the end of every pass.
