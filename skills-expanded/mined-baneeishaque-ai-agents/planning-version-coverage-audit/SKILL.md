---
name: planning-version-coverage-audit
description: >-
  Base — literal section-by-section coverage audit between two versions of
  the same markdown artifact (implementation-plan, commit-preview, walkthrough,
  skill doc, etc.). For every H2/H3 section of the OLD document, classify whether
  the NEW document covers it, enhances it, or drops it, then emit a deterministic
  FULL / PARTIAL / MISSING verdict with exit codes. NOT a diff — a
  coverage/superset relation.
category: General
---

# Planning Version Coverage Audit (v1)

> **Skill ID:** `planning-version-coverage-audit`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base

## Composition Rationale

This is a **base skill** — it owns a single generic primitive: a literal,
section-by-section coverage audit between two versions of the SAME artifact.
Any answer to "does document B fully supersede / cover document A?" — plan
v1 vs v2, commit-preview v1 vs v2, audit-log v1 vs v2 — needs exactly this
deterministic relation. The test that drove extraction: *"could a different
domain ever need the same primitive?"* Yes — the retirement composer below,
any future supersession gate, and even manual "is B worth keeping A?" reviews.

It is consumed by:

| Composer | Composition Mechanism |
| --- | --- |
| [`planning-superseded-version-retirement`](../planning-superseded-version-retirement/SKILL.md) | Invokes `scripts/audit-version-coverage.py --old <v1> --new <v2> --json` as its mandatory COVERAGE GATE; aborts the retirement unless the verdict is FULL. |
| [`planning-artifact-lifecycle`](../planning-artifact-lifecycle/SKILL.md) | References §5's audit gate when a versioned artifact reaches a supersession decision. |

## Environment & Dependencies

| Requirement | Notes |
| --- | --- |
| Python 3.12+ | `python3 -m py_compile` self-check at first use |
| Read access to the two artifact files being compared | The audit only READS; it never mutates. |

## When to Use

- When a user asks "is vN entirely covered & enhanced by vN+1 / can we get ridd of an old version?"
- Before ANY retirement / deletion of a superseded versioned artifact (the retirement composer enforces this gate).
- To prove to a reviewer that a new artifact version is a strict superset of the old one.
- As post-hoc verification of the authoring-side
  [`versioned-artifact-superset-build`](../versioned-artifact-superset-build/SKILL.md)
  construction: when vN+1 was built as vN verbatim + deltas appended, this
  audit returns FULL mechanically — a mismatch here signals the
  construction convention was violated.

## Script: `scripts/audit-version-coverage.py`

Tier-1 Python 3.12+, stdlib only (`argparse`, `re`, `pathlib`, `json`). Self-anchored relative paths; emits
deterministic output; NEVER mutates its inputs.

### CLI contract

| Argument | Required | Description |
| --- | --- | --- |
| `--old <path>` | yes | Old artifact (e.g. `…_implementation-plan_v1.md`). |
| `--new <path>` | yes | New artifact (e.g. `…_implementation-plan_v2.md`). |
| `--json` | no | Machine-readable JSON (recommended for programmatic consumers). |
| `--headings <regex>` | no | Only audit sections whose heading matches this regex (default: `^## \| ^###`). |

### Output / Exit codes

- Per old section → one row: `COVERED` | `ENHANCED` | `DROPPED`, plus the matching new heading (ENHANCED/COVERED)
  or "no match" (DROPPED).
- Verdict: `FULL` (no DROPPED) / `PARTIAL` (≥1 DROPPED) / `MISSING` (old file absent).
- Exit: `0` FULL, `1` PARTIAL (or file-missing on the old side), `2` usage error.

Classification rules (respectively):

- **COVERED** — the exact heading appears in the new doc, and the body block content is byte-present (ordered
  or as a superset).
- **ENHANCED** — heading exists in new doc AND the new block strictly contains more content than the old block
  (the old body is a byte-subset of the new body).
- **DROPPED** — heading does not appear in the new doc, OR the old body is not a subset of the new body, AND
  the "change-history row" exemption does not apply.

The script does not edit ARTIFACTS. Nothing is written to the two inputs.

## Composition by Higher-Level Skills

Table shown in Composition Rationale above; the ONLY current consumer is
[`planning-superseded-version-retirement`](../planning-superseded-version-retirement/SKILL.md) (COVERAGE GATE).

This skill does NOT compose the construction-side companion skill in this
folder (see Related Skills): that skill CONSTRUCTS vN+1 (verbatim +
deltas); this skill VERIFIES the relation between two existing files.
They are companions on opposite sides of authoring.

## SSOT Compliance

- Coverage/retirement AGENTS.md gate mandates are owned by
  [`planning-artifact-lifecycle`](../planning-artifact-lifecycle/SKILL.md) §5 and
  [`planning-superseded-version-retirement`](../planning-superseded-version-retirement/SKILL.md) §Protocol.
- This skill does NOT redefine them — it operationalizes the *literal audit* that those two skills call out.

## Related Skills

- [`planning-artifact-naming`](../planning-artifact-naming/SKILL.md) — the naming convention that versions the audited
files.
- [`versioned-artifact-superset-build`](../versioned-artifact-superset-build/SKILL.md) — the authoring-side companion
that CONSTRUCTS vN+1 as vN verbatim + deltas (makes this audit's FULL verdict mechanically attainable).

## Traceability

- Created: 2026-08-07
- Source: submodule-history-removal skills session — the "v1 is entirely covered & enhanced by v2 — right?"
  question, answered by a literal step-to-step mapping table; extracted as a standalone primitive so future
  sessions never hand-audit again.
