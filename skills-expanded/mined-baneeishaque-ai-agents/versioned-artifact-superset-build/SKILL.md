---
name: versioned-artifact-superset-build
description: >-
  Base — construct version n+1 of ANY versioned markdown artifact
  (implementation-plan, commit-preview, walkthrough, audit-log, summary,
  skill doc) as version n's text kept byte-verbatim with version n+1's
  deltas appended (Verbatim-Superset Construction). Optional Change History
  table row stamp and byte-for-byte --verify mode. Construction-only — the
  OLD version file is never mutated. NOT a verification gate (that is
  planning-version-coverage-audit).
category: General
---

# Versioned Artifact Superset Build (v1)

> **Skill ID:** `versioned-artifact-superset-build`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base

## Composition Rationale

This is a **base skill** — it owns a single generic primitive: the
DETERMINISTIC construction of a new artifact version as a byte-verbatim
superset of the previous one. Any "create version n+1 of versioned
document X" task — plan v1 → v2, commit-preview v2 → v3, audit-log v1 →
v2, skill doc v3 → v4 — needs exactly this construction. The layering
test that drove extraction: *"could a different domain ever need the
same primitive?"* Yes — any versioned artifact in any repo, because the
verbatim-superset convention (mandated by
[`ai-agent-planning-rules.md` §7.1](../../../../../ai-agent-rules/ai-agent-planning-rules.md))
applies to ALL versioned artifacts, not just planning plans.

It complements (does NOT duplicate) the verification side: the coverage
audit skill in this folder VERIFIES that vN+1 covers vN *after the fact*;
this skill CONSTRUCTS the vN+1 that makes that audit trivially FULL.

It is consumed by:

| Composer | Composition Mechanism |
| --- | --- |
| [`planning-artifact-lifecycle`](../planning-artifact-lifecycle/SKILL.md) | Invokes `scripts/build-version-superset.py --old <vN> --new <vN+1> --deltas <deltas>` as the construction half of Step 3 (CAM §7.1 enforcement); the coverage audit then runs as post-hoc verification. |

## Environment & Dependencies

| Requirement | Notes |
| --- | --- |
| Python 3.12+ | `python3 -m py_compile` self-check at first use |
| Read access to vN (the `--old` file) and the deltas block; write access for `--new` | The OLD file is NEVER mutated. |

## When to Use

- When creating version n+1 of ANY versioned markdown artifact and the
  verbatim-superset convention applies (plans, previews, walkthroughs,
  audit-logs, summaries, skill docs, release notes).
- Whenever the new version must provably contain the old version's text
  unchanged (byte-preservation proof via `--verify`).
- As the authoring-side companion to `planning-version-coverage-audit`:
  build with this skill → the coverage audit returns FULL mechanically.

## Script: `scripts/build-version-superset.py`

Tier-1 Python 3.12+, stdlib only (`argparse`, `hashlib`, `json`, `re`,
`pathlib`, `sys`). Self-anchored relative paths; deterministic output;
NEVER mutates its `--old` input.

### CLI contract

| Argument | Required | Description |
| --- | --- | --- |
| `--old <path>` | yes | vN file (read-only; never mutated). |
| `--new <path>` | yes | vN+1 output file to create. |
| `--deltas <path>` | yes | Markdown deltas block file to append (author-authored; judgement tier). |
| `--change-history-row "<ts> \| <summary> \| <rationale>"` | no | Single row appended after the last row of the FIRST `## Change History` table — the only sanctioned in-place edit inside the vN region (it is vN+1's own metadata, not old content). Passed without surrounding pipes, the row is auto-normalized to a well-formed table row (`\| ts \| summary \| rationale \|`). Errors (exit 2) if no Change History table exists. |
| `--overwrite` | no | Allow replacing an existing `--new` file (refused otherwise). |
| `--dry-run` | no | Print the build plan (byte counts, sha256, row stamp, overwrite flag); write nothing. |
| `--verify` | no | Recompute the expected bytes from the same inputs and compare byte-for-byte against `--new`. |
| `--json` | no | Machine-readable JSON output. |

### Build semantics (deterministic)

```text
new = old_bytes (with optional change-history row inserted) + "\n" + deltas_bytes
```

- The old region is preserved byte-for-byte — nothing rewritten, reworded,
  reordered, or dropped.
- The deltas block is appended AFTER the old region (never interleaved).
- `--change-history-row` errors (exit 2) if no Change History table exists.

### Output / Exit codes

- `--dry-run` / `--verify` / default build each emit one summary line (or
  JSON with `--json`): old/deltas/new byte counts, old sha256, and (for
  verify) the OK/MISMATCH verdict.
- Exit: `0` OK (build written / dry-run printed / verify matched),
  `1` verify mismatch, `2` usage or precondition error (missing file,
  `--new` exists without `--overwrite`, `--old == --new`, no Change
  History table for a row stamp).

### Safety rules

1. `--old` is opened read-only; the script never writes it.
2. `--new` existing → refusal (exit 2) unless `--overwrite`.
3. `--old` and `--new` resolving to the same path → refusal.
4. Run `--verify` immediately after a build, BEFORE any manual edits, so
   the byte-for-byte proof is valid (manual later edits make `--verify`
   advisory only).

## Composition by Higher-Level Skills

Table shown in Composition Rationale above; the ONLY current consumer is
[`planning-artifact-lifecycle`](../planning-artifact-lifecycle/SKILL.md)
(Step 3 construction half).

## SSOT Compliance

- The **Verbatim-Superset Construction mandate** is owned by
  [`ai-agent-planning-rules.md` §7.1](../../../../../ai-agent-rules/ai-agent-planning-rules.md)
  (CAM). This skill does NOT redefine it — it operationalizes the
  deterministic construction mechanics.
- The **post-hoc coverage verification** is owned by
  [`planning-version-coverage-audit`](../planning-version-coverage-audit/SKILL.md).
  This skill never audits; the audit skill never constructs.

## Related Skills

- [`planning-version-coverage-audit`](../planning-version-coverage-audit/SKILL.md)
  — the verification-side companion: build with this skill, then audit
  with that one (FULL becomes mechanically attainable).
- [`planning-artifact-naming`](../planning-artifact-naming/SKILL.md) —
  the naming convention (§2.2 versioning rules) for the artifacts this
  skill versions.
- [`planning-superseded-version-retirement`](../planning-superseded-version-retirement/SKILL.md)
  — downstream consumer: a version built by this skill passes the FULL
  coverage gate, unlocking the authorized retirement path.

## Traceability

- Created: 2026-08-08
- Source: 2026-08-08 planning session — the fork-log-cleanup skills
  session proved the convention empirically: plan v3 was authored as v2
  verbatim + deltas and its coverage audit returned FULL mechanically,
  while v1 (not verbatim-embedded) required a manual preservation annex.
  The user stated the convention as a strict rule; the audit showed it
  was documented nowhere (CAM §7.1 said "restore OR rationalize", §9 said
  "restate"), so it was extracted as a mandate + this construction
  primitive.
