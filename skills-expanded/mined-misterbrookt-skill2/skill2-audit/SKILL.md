---
name: skill2-audit
description: "Use when reviewing one skill or a skill library for structural, safety, linkage, size, or static trigger-boundary problems."
---

# Audit Skill Libraries

Find evidence-backed defects without changing the library.

## Scope

| Target | Checks |
| --- | --- |
| One Skill | Frontmatter, description, links, resources, scripts, secrets, local paths, size |
| Skill Library | Every single-Skill check plus duplicate names, ownership, scope, and static trigger overlap |

## Ownership

- Audit owns static structure, safety, references, metadata, and trigger overlap.
- Test owns live activation and outcome behavior.
- Visualize owns inventory/usage/test evidence and conservative lifecycle review candidates.
- Create owns applying approved structural changes.

## Method

1. Run `uv run --script <skill-dir>/scripts/run -- lint <target> --json` first for a single Skill or a library. Save and use its static findings as evidence.
2. Manually review what CLI cannot prove: description semantics, ownership, scope, and trigger overlap.
3. If CLI is unavailable or fails: state limitation / `inconclusive`. Never claim clean.
4. Do not execute scripts. Do not auto-fix.

## Checks

- Missing or invalid `SKILL.md` and frontmatter
- Directory/name mismatch
- Workflow summaries or ambiguous triggers in `description`
- Broken relative links and unused resources
- Non-executable or risky scripts
- Secrets and accidental machine-local paths
- Oversized bodies that should use progressive disclosure
- Static trigger overlap across sibling skills
- Project-only instructions inside a global package

## Severity

| Level | Meaning |
| --- | --- |
| P0 | Install or execution breaks |
| P1 | Triggering or ownership is wrong |
| P2 | Safety or maintenance risk |
| P3 | Cleanup or style debt |

## Output

Return severity, file, evidence, impact, and smallest suggested change. Do not apply fixes unless requested.

```bash
uv run --script <skill-dir>/scripts/run -- lint skills/<name> --json
uv run --script <skill-dir>/scripts/run -- lint skills --json
uv run --script <skill-dir>/scripts/run -- scan skills/<name> --json
uv run --script <skill-dir>/scripts/run -- scan skills --json
```
