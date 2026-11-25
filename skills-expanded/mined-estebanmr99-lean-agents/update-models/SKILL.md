---
name: update-models
description: Compare the tier-to-model mapping with the models the account can use now, and propose a change; also list newer tool versions than core/pins.json and bump them on approval. Use when the user asks about newer models or tool versions, a model was retired, models.dev shows a new one, or a version-watch issue is open.
---

# update-models

1. Read the current mapping: `~/.config/lean-agents/state.json` gives the profile, and `profiles/<name>.json` in the lean-agents repository gives the tiers.
2. List what this account can use:
   - OpenCode: `opencode models` or `opencode models <provider>`.
   - Claude Code: the `/model` command. The tiers use the aliases `haiku`, `sonnet`, `opus`.
   - Copilot CLI: the `/model` command in a session. Your plan or organization may hide some models.
   - Antigravity: `agy models` after signing in. Subagents take only `flash`, `pro` or `inherit`.
3. Read the provider's release notes for each candidate. Check price and whether prompts may be used for training. On OpenCode Go, avoid models named Contributor or Free.
4. Show the proposal as a table: tier, current model, proposed model, one-line reason. Keep the fast tier cheap.
5. Write nothing before the user approves. After approval, edit the profile, then rerun the installer with `--update`.
6. Report what changed and how to go back. The previous files are in `~/.config/lean-agents/backups`.

## Tool versions

`core/pins.json` lists the versions lean-agents fetches at run time, each with the day it was verified and the CI job that proves it.

1. For each entry, find the newest release: `npm view <source> version time --json` for `npm`, `git ls-remote --tags https://github.com/<source>` for `skill`. Skip anything published in the last 14 days.
2. Show a table: pin, current version, newer version, release-notes link, the `ci` job to run first. The open pin-bump PR from `ci-latest` has the same data. Entries with a `hold` in `core/pins.json` are listed as held with their reason, not proposed.
3. Write nothing before the user approves. After approval, change only `version` and `verified` for the approved entries, and ask the user to run the listed `real-*` job (or `tests/real-*.sh` in a sandbox HOME) before merging.
4. Also update the literal versions in docs: `skills/token-audit/SKILL.md` (codeburn) and `docs/manual-install.md`.
5. `--update` installs the new pins; `--doctor` reports `changed` rows until it runs.
