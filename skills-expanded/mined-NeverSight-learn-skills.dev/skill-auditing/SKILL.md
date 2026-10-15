---
name: skill-auditing
description: Audits any skills directory on two layers - format against shared authoring conventions, and content facts (commands, APIs, versions) against live documentation - reporting per-layer findings with sources. Use when asked to audit, review, or check whether skills are outdated, stale, or still correct.
---

# Skill Auditing

Find what has gone stale in a set of skills — on two independent layers,
reported separately so the user knows which findings are format and which
are facts.

## Step 1 — Pick the target

Default to the current project's installed skills (`.claude/skills/`,
`.agents/skills/`, or the repo's `skills/`). Accept any directory path the
user names, including a collection repo's own `skills/`.

## Step 2 — Format layer (offline)

For each skill, check against the authoring conventions in
[skill-writing's references/conventions.md](../skill-writing/references/conventions.md)
when available (the single source of truth), else the same rules inline:
frontmatter shape and name == directory; description is a capability
sentence + "Use when ..." ≤1024 chars; body ≤100 lines with detail in
references/; references links resolve; English only. Report each violation
with file and line.

## Step 3 — Content layer (live)

Extract the concrete factual claims a skill makes — commands, flags, API
calls, config keys, file paths, version numbers — and verify each against
current official documentation (web search / doc fetch; for library docs
prefer the docs tooling). Classify each:

- **confirmed** — matches current docs.
- **outdated** — current docs contradict it; cite the doc as the source.
- **unverifiable** — cannot confirm or deny from available sources; say so,
  never guess.

## Step 4 — Report and route fixes

Two sections, format then content. Each finding: the skill, the location,
the severity, and the evidence or source. Then, for approved fixes, route
to the **skill-writing** skill when installed; if it is not installed,
print the exact proposed edit for manual use and mention the install
option at most once.

## Principles

| Principle | Meaning |
| --- | --- |
| Two layers, never merged | Format (offline, convention) and content (live, factual) are reported separately. |
| Cite sources | Every "outdated" finding names the doc that contradicts the skill. |
| Honesty over coverage | What can't be verified is listed as unverifiable, not guessed. |
| Diagnose, don't mutate | The audit reports and proposes; skill-writing performs the edits. |

The repo's own CI lint stays the enforcement gate; skill-auditing is the
user-facing, any-directory diagnostic that also checks content facts CI
cannot.
