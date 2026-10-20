# GitHub Copilot instructions — Daymark

## Required first step
Before any repository work, read the complete root `AGENTS.md`. It is the canonical source for project constraints, agent attribution, coordination, testing, release, signing, security, and evidence requirements. Do not start coding or reviewing before reading it.

## Working sequence
1. Read `AGENTS.md`; also read any scoped `AGENTS.md` in directories being changed.
2. Check live `main`, open PRs, and issues; identify overlapping agent work.
3. Make a focused change, preserve existing behavior, and add/update regression checks.
4. Run the checks required by `AGENTS.md`; report exact outcomes and the tested commit.
5. Keep device-only checks marked `NOT TESTED` unless performed on a real device/emulator.

## GitHub contributions
Every PR, issue, review summary, release note, handoff, or substantive comment must identify the actual agent, model/version (or `not disclosed by runtime`), tools actually used, and current UTC timestamp. Never copy another contributor's attribution or leave placeholders. Coordinate in existing GitHub threads and do not claim a merge, green CI, release, or device pass without evidence.

If these instructions conflict with root `AGENTS.md`, follow `AGENTS.md` unless a higher-priority system or platform instruction applies. These repository instructions do not override system, safety, or platform rules.
