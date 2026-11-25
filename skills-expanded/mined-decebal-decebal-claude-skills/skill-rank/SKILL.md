---
name: skill-rank
description: "Find a skill that is not in your listing: search every installed Claude and Codex skill, ranked by a Jev rating of how often this user's work needs it. Also rescans, re-rates and re-fits the skill listing to its context budget."
---

# skill-rank

Every installed skill stays installed. `skill-rank apply` keeps the best-rated
skills fully listed inside each host's listing budget. The rest are listed by
name only (Claude Code) or switched off (Codex), and `skill-rank search` still
finds them.

## When to search

Before a task that may have specialised instructions (a framework, a vendor
API, a file format, a review or release procedure) when no skill in your
listing clearly fits it.

## How

```bash
skill-rank search <words...> [--host claude|codex] [--limit 8]
```

Each hit prints `score  rating  tier  host  name  path`, then the start of its
description. Read the `SKILL.md` at the printed path and follow it. A Claude
`name-only` skill can also be invoked by name; a Codex `disabled` skill cannot,
so read its file.

Score is word relevance times `0.35 + 0.65 * rating`. An unrated skill counts as
0.5 and shows `--`.

## How ratings are made and refreshed

1. `skill-rank scan [--days 60]` lists skills in `~/.claude/skills`, enabled
   Claude plugins, `~/.agents/skills`, `~/.codex/skills` (and `.system`) and
   enabled Codex plugins, and counts their use in Claude transcripts and Codex
   rollouts from the last `--days`.
2. `skill-rank rate [--dry-run] [--force]` asks TypeSafe Jev to score each
   unrated skill from 0 to 4 against `profile.md`, stored as 0 to 1. Editing
   `profile.md` makes every rating stale; `--force` rates everything again.
3. `skill-rank apply --host claude|codex [--dry-run]` fits the budget: 1%
   (Claude) or 2% (Codex) of `--context-tokens` (default 200000) at 4 chars per
   token, or `--budget-chars N`; on Codex a `[skills] max_context_tokens` in
   `config.toml` sets it. Plugin, system and command entries are charged first,
   then skills stay on by rating until the next one does not fit. Claude gets
   `"name-only"` entries in `skillOverrides` in `~/.claude/settings.json`;
   Codex gets a managed `[[skills.config]]` block in `~/.codex/config.toml`,
   parsed before and after the edit. A Codex skill that shares its name with a
   system or plugin skill stays on. Entries you set yourself are kept, and
   `skill-rank` itself always stays on. Each write keeps `*.skill-rank.orig`
   (the file before skill-rank first changed it, never overwritten) and
   `*.skill-rank.bak` (the version just replaced), both with the file's
   permissions.
4. `skill-rank list [--host claude|codex]` prints every skill by rating.

Run scan, rate and apply again after installing skills or editing `profile.md`.

## What leaves the machine

`rate` sends `profile.md`, each skill's name, description (first 700
characters), use counts and hosts to `api.typesafe.ai`. Paths and file contents
are not sent. Each line of `redact.txt` is a term replaced by `[redacted]`
(case-insensitive) in the profile, names and descriptions before sending; if
the terms do not build into a pattern, nothing is sent. `rate --dry-run` prints the first request
and sends nothing; every request and answer is kept in `jev-log/`. The key comes
from `TYPESAFE_API_KEY`, else `~/.config/typesafe/key`.

Data lives in `$SKILL_RANK_HOME`, else `~/.config/skill-rank/`: `profile.md`
and `redact.txt` (yours), `catalog.json` and `jev-log/` (the tool's).

## Install

From this skill's directory:

```bash
cargo install --locked --path scripts
```

Link or copy the directory to `~/.claude/skills/skill-rank` and
`~/.agents/skills/skill-rank`, write `~/.config/skill-rank/profile.md`, then run
`skill-rank scan`, `skill-rank rate` and `skill-rank apply --host claude --dry-run`.
