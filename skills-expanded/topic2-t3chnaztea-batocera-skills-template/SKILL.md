---
name: batocera-yourskill
description: >-
  Use when [the specific situations, symptoms, and phrases that should trigger
  this skill]. Pack the words someone would actually type or think when they
  hit this problem. Describe ONLY when to use it, never summarize the workflow
  inside. Keep the whole frontmatter under 1024 characters. End by naming what
  this skill is NOT for, pointing at the sibling skill that covers it.
compatibility: Requires SSH access to a Batocera host (tested on v41-v43).
---

# Batocera Yourskill

One or two sentences: what this skill covers and that it assumes the connection
pattern, filesystem model, and safety doctrine from `batocera-ops`. Cross-
reference sibling skills by name (`batocera-roms`, `batocera-display`,
`batocera-tuning`, `batocera-maintenance`) rather than repeating their content.

## Guidelines for a good Batocera skill

Delete this section in your real skill; it's guidance for authoring.

- **Name:** `batocera-<area>`, lowercase and hyphens only. The directory name
  MUST equal the frontmatter `name`.
- **Description:** starts with "Use when…", lists concrete triggers and keywords,
  ends with a "not for X, use Y" pointer. No workflow summary (an agent will
  follow the description instead of reading the body).
- **Original prose only.** Do not paste text from the Batocera wiki or other
  docs — write the lesson in your own words and link the wiki as the canonical
  manual. Ship institutional knowledge the wiki doesn't have.
- **Parameterize everything host-specific.** Use `$BATOCERA_HOST`, never a real
  IP; read passwords from env; never commit tokens, credentials, MQTT secrets,
  or personal ROM/library specifics.
- **Non-destructive doctrine.** Prefer hide/move/append over delete/overwrite;
  back up configs and gamelists before editing; never inject synthetic input.
- **Verify against ground truth.** Show the reader how to confirm the change
  (read the generated config, launch + screenshot), not just make it.
- Keep `SKILL.md` under ~500 lines. Push heavy detail into `references/*.md` and
  reusable code into `scripts/`. Scripts should be `--dry-run`-first where they
  mutate, idempotent, and self-documenting in a header.

## Overview

What this is and the core principle in 1–2 sentences.

## When to use

Symptoms and situations (bullets). When NOT to use.

## [Your sections]

Quick-reference tables, worked examples, the specific traps you learned. One
excellent example beats five generic ones.

## References

- [references/topic.md](references/topic.md) — heavy detail loaded on demand.
