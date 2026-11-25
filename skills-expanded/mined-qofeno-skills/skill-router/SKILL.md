---
name: skill-router
description: Use this before starting substantive work on ANY request — coding, debugging, setup, design, writing, analysis, anything beyond a trivial one-line reply. Checks every other skill actually installed (from any source, any publisher, not just this one) for relevance before proceeding, so a matching skill never gets silently skipped just because the request didn't happen to use its exact trigger words.
---

# Skill Router

Before doing substantive work on a request, check what's actually installed — don't rely on the request happening to phrase itself the way a skill's description expects.

## Step 1 — List what's installed

Find and list every installed skill, regardless of publisher — not just skills from this repo. Skills are typically stored as folders containing a `SKILL.md`, commonly under a path like `.claude/skills/`, `~/.claude/skills/`, or an equivalent location for whatever tool is running (Cursor, Antigravity, Codex, etc.) — check the actual installed location for the current environment rather than assuming.

## Step 2 — Check each one's description against the actual request

Read each installed skill's `name` and `description` (the lightweight frontmatter, not the full body) and judge relevance against what the user is actually trying to do — not just literal keyword overlap. A request phrased casually ("get this live," "make it look better," "check if this is safe") can match a skill whose description uses different words for the same task.

## Step 3 — Use what matches, don't force what doesn't

- If one or more installed skills are relevant, use them instead of improvising a process from scratch.
- If multiple skills could apply, use the most specific match, not the broadest one.
- If nothing installed actually fits, proceed normally — this router is a check, not a requirement to force-fit an unrelated skill onto the task.
- Don't skip this check just because a request seems simple or the match seems unlikely — a quick check costs little; silently missing an installed skill the user expected to fire costs more.

## What this doesn't do

This can't literally guarantee the host tool invokes it on every single message — that's still governed by the platform's own triggering logic, same as any skill. What it does do: give an intentionally broad trigger so the router step fires for the wide majority of substantive requests, not just ones that happen to match a narrower skill's exact wording. Pairing this with a persistent context file (see the repo's setup guide) closes the gap further, since that file is guaranteed to load every session regardless of skill-matching.
