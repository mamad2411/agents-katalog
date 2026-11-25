---
name: pre-commit-verification-protocol
description: Three-step verification pipeline for skill doc edits and markdown file changes — cross-reference audit, markdown lint, and visual smoke test.
category: General
---

# Pre-Commit Verification Protocol (v1)

> **Skill ID:** `pre-commit-verification-protocol`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base

## Composition Rationale

This is a **base skill** — it owns the mechanical primitive of running
a deterministic verification sequence before any markdown or skill-doc
edit is committed. It does NOT own the individual audits (those are
delegated to their respective skills). It provides a reusable,
sequential pipeline that:

- The [`skill-factory`](../../skill-factory/SKILL.md) consumes in its
  Post-Drafting Checklist (§3) and Skill Enrichment Workflow (§6).
- Any skill author runs before declaring a skill-doc edit done.
- Any agent editing `.md` files runs as a pre-commit sanity check.

## Environment & Dependencies

| Requirement | Minimum | Notes |
| --- | --- | --- |
| `markdownlint-cli2` | latest | Global install (`npm i -g markdownlint-cli2`) or project-local |
| Python 3 | 3.10+ | For cross-reference audit script |
| Read permission | — | To read all SKILL.md files under `.agents/skills/` |
| `git` | 2.x+ | For smoke test diff inspection |

Verification:

```bash
markdownlint-cli2 --version && python3 -c "import re, json, sys; print('OK')"
```

## When to Use

- After creating or modifying any SKILL.md file.
- After editing any markdown file in the skill library.
- Before staging changes to skill or rule files.
- Before declaring a skill-doc edit done (per [`skill-factory`](../../skill-factory/SKILL.md)
  Post-Drafting Checklist).
- After running `markdownlint-cli2 --fix` to verify no new issues were introduced.

## Step-by-Step Procedure

### Step 1 — Cross-Reference Audit

Run the
[`skill-cross-reference-audit`](../skill-cross-reference-audit/SKILL.md)
to verify no structural issues were introduced:

```bash
python3 .agents/skills/general/skill-cross-reference-audit/scripts/audit-cross-refs.py
```

If issues are found, fix them per the audit skill's repair table
before proceeding. Exit code 0 means clean.

### Step 2 — Markdown Lint

Run the
[`markdown-lint-workflow`](../markdown-lint-workflow/SKILL.md)
pipeline on each modified file:

```bash
# Convenience pipeline (recommended)
python3 .agents/skills/general/markdown-lint-workflow/scripts/fix-markdown-pipeline.py path/to/SKILL.md
```

If `markdownlint-cli2` is not available globally:

```bash
npm i -g markdownlint-cli2
```

Zero errors from `markdownlint-cli2 path/to/SKILL.md` means the file is
lint-compliant.

### Step 3 — Visual Smoke Test

Inspect the diff for correctness and style consistency per
[`skill-factory` §5.8](../../skill-factory/SKILL.md#58-style-consistency-discipline-match-the-surrounding-document):

```bash
git diff --stat
git diff -U0 path/to/SKILL.md | head -200
```

Verify:

1. Only intended files are modified.
2. No stray content, debug text, or placeholder leftovers.
3. Style matches surrounding document (list marker, indentation,
   blank-line spacing per §5.8).
4. Cross-reference links use correct relative paths per
   [`skill-factory` §5.6](../../skill-factory/SKILL.md#56-cross-reference-link-discipline).

### Step 4 — Final Status Check

```bash
git status
git diff --cached --stat
```

Confirm the working tree is in the expected state before committing.

## SSOT Compliance

- The **cross-reference audit logic** is owned by
  [`skill-cross-reference-audit`](../skill-cross-reference-audit/SKILL.md).
- The **markdown lint pipeline** is owned by
  [`markdown-lint-workflow`](../markdown-lint-workflow/SKILL.md).
- The **style-consistency discipline** is owned by
  [`skill-factory` §5.8](../../skill-factory/SKILL.md#58-style-consistency-discipline-match-the-surrounding-document).
- This skill does NOT redefine any of them — it sequences them into a
  deterministic protocol.

## When to Skip

- Trivial single-line edits with no structural impact (e.g., fixing a
  typo in prose). Step 3 (smoke test) should still be performed.
- Files outside the skill library (e.g., project README, standalone
  docs) may not need Step 1 (cross-ref audit).

## Related Skills

- [`skill-cross-reference-audit`](../skill-cross-reference-audit/SKILL.md)
  — consumed in Step 1.
- [`markdown-lint-workflow`](../markdown-lint-workflow/SKILL.md) — consumed
  in Step 2.
- [`git-atomic-commit-construction`](../../git-atomic-commit-construction/SKILL.md)
  — the commit workflow this protocol precedes.
- [`list-indent-consistency`](../list-indent-consistency/SKILL.md) — indent
  drift repair after lint-fix scripts.
- [`planning-artifact-lifecycle`](../planning/planning-artifact-lifecycle/SKILL.md)
  — companion base skill for planning artifact lifecycle management.

## Traceability

- Created: 2026-07-03
- Source: OpenCode config versioning & preservation session. The protocol
  was executed iteratively: cross-ref audit → markdown lint → smoke test →
  fix → re-audit until zero errors.
