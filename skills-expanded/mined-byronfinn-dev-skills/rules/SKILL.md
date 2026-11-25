---
name: rules
description: "Use as the shared cross-skill rules bundle of the dev-skills set — anti-patterns, entry protocol, sub-agent runtime semantics, authoring discipline, and the engineering-principles catalog. Not a task skill: the other skills link into this directory, and this file exists so the bundle ships with them and those links resolve in installed copies."
disable-model-invocation: true
---

# Rules: Shared Cross-Skill Bundle

**This is not a task skill.** It carries no workflow, produces no artifact, and should never be routed to. Every other skill in this repository links into this directory (`../rules/<file>.md`), and those links must keep working after installation.

## Why this file exists

The skill installer ships exactly one thing: a directory containing a `SKILL.md`. Nothing else in a repository reaches installed copies. Without this file, `skills/rules/` stays repository-only and every cross-skill rules link breaks the moment a user installs the set — the shared-rules architecture would work for contributors and fail for everyone else.

Measured with the installer (`--project --copy`, isolated scope): before this file existed, 12 skills installed with `rules/` absent and 3 of `review/SKILL.md`'s rules links dangling; with it, 13 units install, `rules/` is present, and those links resolve. Evidence and the packaging analysis: `docs/audits/2026-09-14-shared-rules-not-installed.md`.

Two deliberate deviations from the skill conventions, both because this is not a task skill:

- **No outcome contract** — there is no outcome to contract. The contract here is the contents table below.
- **`disable-model-invocation: true`** — the bundle must never compete for routing. A user-invoked unit pays zero context load; its description is not model-loaded.

## Contents

Every file in this directory is listed here. A rules file that is not listed is invisible to anyone reading the bundle — `scripts/check-docs.py` fails when the two drift apart.

| File | Holds | Cited by |
|---|---|---|
| `anti-patterns.md` | Cross-skill behavioral constraints (main table + frozen-number Archive) | every skill; cited by number |
| `entry-protocol.md` | Shared bootstrap: project config, domain docs, upstream-artifact checks | every skill's first step |
| `sub-agent-runtime.md` | "Sub-agent" = re-read-from-disk discipline, not a scheduler | `tdd`, `review` |
| `writing-skills.md` | Authoring discipline: two loads, descriptions, information hierarchy, wording, pruning | contributors and any skill edit |
| `engineering-principles.md` | Single definition source for SOLID/DRY/KISS/YAGNI/LoD/composition/explicit/fail-fast/immutability, plus the gates that keep principle findings from becoming nitpicks | `review`, `improve-architecture`, `tdd`, `implement` |

## The rule that governs this directory

Each meaning lives in exactly one file here and is **linked, never restated** (anti-patterns.md #38). A consuming skill may cite a rule by number or link the file; it may not copy the rule's text. Skill-specific operational content — checklists, scan thresholds, refactor steps — stays in the skill.
