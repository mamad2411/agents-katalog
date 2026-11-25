---
name: <skill-slug>
description: One sentence — what this skill does and when to invoke it. This is what Claude Code matches against to decide whether to use the skill.
owner:                    # MANDATORY for user-facing skills — who the skill SERVES.
  - "[[<team-or-person>]]"   # team-shared: [[<team-slug>]] (leadership / sales / marketing / product / engineering / customer-success); personal: [[<person-slug>]]
creator:                  # MANDATORY for user-facing skills — who WROTE the skill.
  - "[[<person-slug>]]"
teams: []                 # optional — extra teams that routinely invoke this skill, beyond owner.
---

# <Skill name>

<!--
TEMPLATE NOTES — delete before saving a real skill.

- owner and creator are BOTH mandatory and are different fields. owner = who it serves; creator = who wrote it.
- Bundled sub-tools (skills/<slug>/<helper>/SKILL.md) OMIT owner and creator — they inherit from the parent.
- Double-write the reverse links in the same commit:
    owner [[<team>]]   -> (Referenced by on canon/team/<team>.md; no manual reverse)
    owner [[<person>]] -> people/<person-slug>.md -> skills:
    creator [[<person>]] -> people/<person-slug>.md -> skills_created:
- If this skill writes to the repo, LINK to the destination README's output-format spec — never copy it in here.
- English only in all output.
-->

**Owner**: [[<team-or-person>]]  <!-- team-shared: [[<team-slug>]]; personal: [[<person-slug>]] -->
**Creator**: [[<person-slug>]]

## Purpose

What this skill is for, in one or two sentences. The question it answers or the artifact it produces.

## When to use

The trigger conditions — what the user says or what state the repo is in when this skill should run. Mirror the `description` field, expanded.

## Inputs

- What the skill reads to do its job: a source tool (`<transcript tool>`, `<email>`, `<CRM>`, `<docs system>`, `<file storage>`), a date, a person, repo files.
- Which canon / team files it loads at run time for filters (`canon/team/<team>.md`, company canon).

## Procedure / Steps

1. <First step — usually: fetch the source material.>
2. <Entity-scan: match people / companies / systems / themes against the graph; create-on-first-mention via `<CRM>` where applicable.>
3. <Transform: produce the body in the required shape.>
4. <Tag: write frontmatter + double-write any bidirectional reverse links.>
5. <Write-back: pull-rebase, write the file, commit, push (see below).>

## Output

- Where the skill writes (path), and the file shape.
- Link to the destination's output-format spec rather than restating it, e.g. "follow [`signals/daily-call/README.md`](../../signals/daily-call/) -> Per-call section".

## Write-back

If the skill commits to the repo, state the loop explicitly: `git pull --rebase`, write, validate markdown links, `git commit`, `git push origin main`. Note any path that is review-gated rather than push-direct.
