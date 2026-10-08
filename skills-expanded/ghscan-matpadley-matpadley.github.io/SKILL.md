---
title: "A Skill for Publishing the Progress Log to the Site"
date: 2026-07-31T09:57:00+01:00
draft: false
description: "Turning an engineering log into articles is half deterministic and half judgement. The script does the first half and deliberately refuses the second."
summary: "Turning an engineering log into articles is half deterministic and half judgement. The script does the first half and deliberately refuses the second."
tags:
  - club-monitor
  - hugo
  - claude-code
  - tooling
source: "2026-07-31-0957-publish-progress-skill.md"
---

## What changed

The `progress/` entries are now published as articles on the personal site
(`~/GitHub/matpadley.github.io`) in a new Hugo section, `content/ClubMonitor/`, reachable at
`/ClubMonitor/`. Doing that by hand once was fine; doing it every time a progress entry lands is not,
so it is now a skill in this repo.

- **`.claude/skills/publish-progress/SKILL.md`** — the workflow, plus the conventions the existing
  articles already set (front matter shape, title style, English-only, dates carrying a time).
- **`.claude/skills/publish-progress/publish.py`** — the mechanical half: `status`, `write`, `verify`.

The split matters. The script does what is deterministic — parsing the `YYYY-MM-DD-HHMM` filename
prefix into an RFC3339 date with the right UK offset, assembling front matter, stripping the leading
H1 and `**Date:**` line, and copying the body **verbatim**. It deliberately does *not* invent titles,
descriptions or tags: those need to be read out of the entry, so they are passed in as a metadata
JSON file. A script that guessed them would produce worse articles than no script.

`status` is what makes the skill safe to run ad hoc. Each published article carries a `source:` front
matter key naming the `progress/` file it came from, so the script can diff the two directories and
report exactly which entries are unpublished. Re-running it publishes nothing twice. The eight
articles written before the skill existed were backfilled with `source:` so they are recognised.

## Why

Two reasons the obvious approach was avoided. Writing the conversion inline each time invites drift —
the section already has non-obvious conventions (an explicit `summary:` because these entries open
with a heading or a code block and Hugo's automatic summary would otherwise render markup onto the
list page; times on dates because several entries share a day). And the destination is genuinely
easy to get wrong: this repo has an empty `progress/hugo/` directory that looks like where the output
belongs, and it is not. Both are now written down where they will be read.

## Verification

- `publish.py status` against the eight existing articles: all eight detected as published, none
  pending.
- This entry was then used as a live test of `write` — detected as unpublished, converted, and the
  site rebuilt with `verify`.

## Note

Nothing is committed by the skill, in either repo. The site deploys to GitHub Pages on every push to
`main`, so publishing stays a manual decision.

## Files touched

`.claude/skills/publish-progress/SKILL.md`, `.claude/skills/publish-progress/publish.py`, plus this
entry. In the site repo (separate, uncommitted): `content/ClubMonitor/*` gained a `source:` key.
