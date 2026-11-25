---
name: planning-superseded-version-retirement
description: >-
  Composer — retire (delete to Trash on macOS) a superseded version of a
  versioned planning artifact (e.g., implementation-plan v1 superseded by
  v2) ONLY after (a) the mandatory coverage audit (base
  planning-version-coverage-audit) returns FULL and (b) explicit user
  authorization. Orchestrates the audit gate, trash, stale-reference sweep
  throughout the surviving version and task.md link, task.md re-sync, and
  dangling-reference verification.
category: General
---

# Superseded Version Retirement (v1)

> **Skill ID:** `planning-superseded-version-retirement`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Composer

## Composition Rationale

This is a **composer** — it orchestrates two atomic primitives (the mandatory
coverage audit and the recoverable macOS `trash` operation) around a
planning-domain lifecycle decision: retiring a superseded artifact version.

It composes:

1. **[`planning-version-coverage-audit`](../planning-version-coverage-audit/SKILL.md)** — invoked FIRST as the
   mandatory coverage gate via `scripts/audit-version-coverage.py --old <vN> --new <vN+1> --json` (self-anchored
   relative path). The composer ABORTS the retirement unless the audit verdict is `FULL`.
2. **[`git-hunk-staging-primitives … agents-md-stage-row.py`](../../../git-hunk-staging-primitives/scripts/agents-md-stage-
row.py)**
   — when the retired version is referenced in `AGENTS-legacy.md`, the composer re-stages the corrected row (relinking
   to the surviving version), rather than hand-editing the table.
3. **macOS `trash`** (AGENTS.md permanent rule 7) — the ONLY deletion mechanism; `rm` is forbidden by policy.
4. **[`planning-artifact-lifecycle`](../planning-artifact-lifecycle/SKILL.md)** — deleted-version-cleanup lifecycle
   default rules (batch deletion, keep-current, task-last) apply to the pieces the composer does not own.

The composer adds domain value ON TOP of the base audit: it decides *when* coverage is sufficient, it holds the
**human authorization gate**, it performs the stale-reference sweep + the task.md re-sync, and it verifies no
dangling references survive.

## Environment & Dependencies

| Requirement | Notes |
| --- | --- |
| macOS (or OS with a Trash/recoverable delete) | `trash` binary; `rm` is FORBIDDEN (AGENTS.md rule 7) |
| Python 3.12+ | `python3 -m py_compile` on its own script at first use |
| Base skill present | `planning-version-coverage-audit` must be installed next to this skill (sibling `../planning-version-coverage-audit/…`) |

## When to Use

- A user asks to delete / "get ridd of" / retire an OLD version of a versioned artifact while a newer version exists.
- A superseded installation leaves the trace that the old version is still "intact" in the surviving doc and
  those stales must be cleaned after the fact (as in the submodule-history session: "v1 is left intact per §8").

## Composer Protocol

Steps in BOLD are mandatory GATES — a gate that does not pass aborts the whole retirement.

1. **Coverage gate** — run `planning-version-coverage-audit/scripts/audit-version-coverage.py --old <vN> --new <vN+1>
--json` (via
   relative sibling path). If the verdict is `PARTIAL` or `MISSING`, STOP: present the `DROPPED` section list to the
   user; restoration/ rationale in the surviving doc is required before retirement can be re-attempted. FULL → proceed.
2. **Authorization gate** — present the plan (`--dry-run` output) to the user and obtain EXPLICIT consent
   ("remove v1", "trash it", "retire vN"). No consent → STOP, no changes.
3. **Stale-reference sweep** — run `retire-superseded-version.py --old <vN> --new <vN+1> --dry-run` first to see
   every referencing file; review the list; then run with `--confirm` to have the script
   (a) trash `<vN>`, (b) re-base affected rows in `AGENTS-legacy.md` (via the stage helper) if any link targets it,
   (c) rewrite the "v1 is intact/History mandate" claims in the surviving `<vN+1>` doc to "v1 was retired
   (trash) after user-authorized coverage audit", and (d) re-sync the task.md goal link if present.
4. **Dangling-reference verification** — run the sweep in `--check` mode: ZERO references to the retired filename
   may remain in the asset root (docs/ + skills). `git status` may show the claimed deletion.
5. No `git add` / `git commit` / `git push` by this composer (§13 sequential objective). The user triggers those.

## Script: `scripts/retire-superseded-version.py`

Deterministic half: coverage gate call, stale-reference scanning, and the trash + edit plan. Human consent + final
deletion are prose-gated. See the CLI table:

| Argument | Required | Description |
| --- | --- | --- |
| `--old <path>` | yes | Path of the retiring artifact (e.g. `…_plan_v1.md`). |
| `--new <path>` | yes | Path of the surviving artifact (e.g. `…_plan_v2.md`). |
| `--dry-run` | yes (for safety) | Compute + print the audit verdict, the stale-reference plan; perform NO writes. |
| `--json` | no | Machine-readable output. |
| `--verify` | no | After changes: assert zero remaining references to the old file base-name; exit 0/1. |
| `--confirm DELETE` | no | Authorized deletion marker (matches the user's explicit consent; e.g. `--confirm DELETE`). Without this the script NEVER deletes. |
| `--asset-root <dir>` | no | Root for the stale sweep (default: `docs/` under the old file's ancestor). |

Exit codes: `0` OK / clean; `1` coverage not FULL or stale refs remain (verify); `2` usage; `3` aborted — no consent.

Behavior:

- **Gate** — invoke `../planning-version-coverage-audit/scripts/audit-version-coverage.py` and require FULL.
- **Sweep** — walk `--asset-root` for markdown files whose content references the OLD FILE's base name
  (e.g. `…_plan_v1.md`), and classify each hit:
    - `TRACE` (Change History row mentioning "v1" with a rationalising term) → preserve;
    - `STALE` (prose "vN is kept intact / untouched / History mandate", markdown links to the vN path) → edit target.
- **Dry-run** prints audit verdict + the list of STALE hits + the planned trash/edit operations; performs no writes.
- **Execute** (only with `--confirm` value matching the user's authorized token): write the surviving `<new>`
  references and the task.md if present, then `trash` the old file.
- **Verify** (`--verify`): rescan and confirm zero STALE references; exit 0.

The script does NOT `rm` anything — it only builds and (with consent) executes a `trash` invocation.

Guardrails / notes:

- Destructive path gated behind explicit user string token.
- Read-write boundary is checked with `--dry-run` first.
- macOS-only `trash`; on non-macOS, the composer prints a TO-DO for a recoverable-delete equivalent and aborts.

## SSOT Compliance

- Coverage audit semantics: owned by `planning-version-coverage-audit` (no duplication here).
- Lifecycle deletion rules / keep-current / task-last: owned by `planning-artifact-lifecycle`.
- `trash` policy (recoverable not `rm`): owned by the repo's AGENTS.md rule 7 — enforced, not re-stated.
- Versioned-artifact naming: owned by `planning-artifact-naming`.

## Related Skills

- [`planning-artifact-naming`](../planning-artifact-naming/SKILL.md) — versioning of artifact filenames.
- [`git-atomic-commit-construction`](../../../git-atomic-commit-construction/SKILL.md) — optional helper for the AGENTS-
legacy step.

## Traceability

- Created: 2026-08-07
- Source: submodule-history-removal skills session where v1 was retired after the user asked to remove it,
  coverage audit returned FULL, user said "then remove v1", and the agent swept the surviving v2 + task.md —
  formalized as a composer so the exact order/gates never have to be re-derived.
