---
name: gabe-debt
description: "Architecture decision-debt scanner — decisions never made explicitly or silently contradicting each other across SCOPE/PLAN/code/history; findings written to the four KDBP targets."
when_to_use: "When complexity feels unexplained, during retros, or before a big refactor."
context: fork
agent: Explore
metadata:
  version: 1.1.1
---

# Gabe Debt — Architectural Decision-Debt Scanner

## Gabe execution contract (E1–E7)

This skill runs under the suite execution contract — E1 EVIDENCE · E2 RUN-BEFORE-✅ · E3 NO SILENT DOWNGRADE · E4 REUSE FIRST · E5 STATE SYNC · E6 MISSING ANCHOR = STOP · E7 REPORT WHERE — floors, not ceilings; a skill's own gate may be stricter, never looser. Full text: `../gabe-docs/references/execution-contract.md` (if that file is missing, E6 applies — STOP).

## What this does

Catches complexity gravity wells before they deepen — decisions never made explicitly ("we'll figure out state ownership later") or decisions that contradict each other silently (SCOPE says one topology; PLAN binds another; code assumes a third). Scans using evidence-anchored patterns (P1-P11, project-local `debt-patterns/` overrides global) plus project-local rules (`.kdbp/RULES.md` / `docs/rebuild/LESSONS.md` / retro files), and cites advisory Architecture Principles (AP1-AP13) when finding evidence directly touches one. Every finding carries severity (tier-adjusted), confidence (triangulated), blast radius, and status, then triages to one of four targets: `DECISIONS.md` (ADRs), `SCOPE.md §14` (open questions), `RULES.md` (scar-tissue constraints), `PENDING.md` (deferred work). Distinct from the archived `gabe-teach`'s "gravity wells" vocabulary: wells are architectural domains, gabe-debt finds the debt accumulating in each.

## Usage / modes

`/gabe-debt [brief | dry-run | audit-rules | extract-rules | pattern=Pn | since=<ref> | strict | <file-or-folder>]`

| Mode | Behavior |
|---|---|
| (default) | Full scan + interactive triage + writes |
| `brief` | Findings table + severity + counts; no writes, no triage |
| `dry-run` | Full scan + proposed DECISIONS/SCOPE §14/RULES/PENDING diffs; no writes |
| `audit-rules` | Read-only: check current code/scope against existing RULES.md + LESSONS.md; report violations only |
| `extract-rules` | Read-only: mine retrospective files and propose new R-NN candidates; interactive y/n |
| `strict` | Non-zero exit if any CRITICAL unresolved finding (pre-commit hook form) |

Modes compose (`brief pattern=P3`, `dry-run since=HEAD~20`, etc.). Target defaults to the whole project's `.kdbp/` + code + commit history since the last SCOPE.md Change Log anchor; `pattern=P<n>` restricts to one pattern, `since=<ref>` limits the commit-history pass, `[file-or-folder]` restricts the code+commit sweep. Maturity tier gate (from `.kdbp/BEHAVIOR.md`): MVP surfaces CRITICAL only, Enterprise adds HIGH, Scale adds MEDIUM; `--full` overrides the gate.

## Procedure

1. Treat any text after the invocation as `$ARGUMENTS`; parse mode, target, and any tier override.
2. Read `references/debt-spec.md` IN FULL before executing — the binding spec. If missing, E6 applies — STOP.
3. **Step 0 Preflight** — detect `.kdbp/`, load maturity from BEHAVIOR.md, load existing DECISIONS/SCOPE/RULES/PENDING/debt-ignore state, resolve the active phase, load the pattern catalog (project-local overrides global; E6 STOP if zero pattern files load) and the AP catalog.
4. **Step 1** — index project-local rules (`RULES.md`, `LESSONS.md`, retro files) into a single `rules_index`.
5. **Step 2** — run each pattern's doc pass, code pass, and commit pass; cross-check hits against `rules_index` for rule-violation findings.
6. **Step 3** — score every finding (severity, confidence, blast radius, status); findings with zero evidence lines are dropped, not demoted.
7. **Step 4** — filter by the maturity tier gate (rule-violation findings always survive); order CRITICAL → HIGH → MEDIUM, confident-first, blast-radius-desc within tier.
8. **Step 5** — interactive triage per finding (skipped for `brief`/`dry-run`/`audit-rules`/`extract-rules`/`strict`): promote (d)ecision, (o)pen question, (r)ule, (p)ending, (s)kip, (m)ulti, (e)dit, (q)uit.
9. **Step 6** — after confirmation, write only to approved targets with idempotent stable-ID hashes; never auto-commit — writes land as dirty working-tree changes for the user to review and commit via `/gabe-commit`.
10. **Step 7** — print a summary report (scanned/triaged/written counts, confidence distribution, suggested follow-ups).
11. **Step 8** (`extract-rules` mode only) — mine retrospective files for rule candidates, de-duplicate against existing RULES.md, promote interactively.

## Output contract (summary)

Findings route to four KDBP targets — `DECISIONS.md`, `SCOPE.md §14`, `RULES.md`, `PENDING.md` — each entry idempotent via a `<!-- gabe-debt-stable-id: ... -->` hash comment so re-runs update in place rather than duplicate. Every write is accompanied by a `SCOPE.md §15` Change Log entry. Nothing is ever auto-committed. `brief`, `dry-run`, and `audit-rules` modes are read-only reports with no writes. The full output contract in the spec is binding.
