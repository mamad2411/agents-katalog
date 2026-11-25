---
name: proofcheck
description: Orchestrates a whole-paper audit of the mathematical proofs in a statistics/ML theory paper (statement gate, input provenance, per-unit checks, cross-model review, final report) and the --post-repair convergence audit. Use when user says "proof check", "check proofs", "verify proofs", "audit paper", "检查证明", "证明验证", or wants to verify correctness of a paper's mathematical proofs. For one result or cluster only, /proof-checker is the deep-review worker.
argument-hint: [path-to-paper.tex or paper-name] [--post-repair] [--assurance draft|submission] [--online] [--resume]
allowed-tools: Bash(*), Read, Grep, Glob, Agent, mcp__codex__codex, mcp__codex__codex-reply
model: opus
---

# ProofCheck — Mathematical Proof Verification for Statistics/ML Theory Papers

> 🔬 **Model Recommendation**: Run this skill on **Claude Opus** for best results.
> Mathematical proof verification requires deep reasoning. If your session is not on
> Opus, run `/model opus` before invoking. The skill will also delegate heavy
> reasoning to Opus sub-agents internally when the Agent tool is used.

Systematically check proofs in long technical appendices using a structured, evidence-based methodology with multi-pass verification.

Based on: https://github.com/maweiruc/proofcheck-stat-paper

Purpose: audit every proof of a statistics/ML theory paper (statement gate, input provenance, per-unit checks,
cross-model review, final report) and, with `--post-repair`, run the delta convergence audit. The goal is to find
correctness issues, never to summarize or silently repair a proof. `/proof-checker` is the per-result deep-review
worker; `/proof-repair` and `/proof-writer` run only after the audit is final. Full detail lives in `references\`;
read the file named in each step, not the whole directory.

## Context: $ARGUMENTS

## Hard rules (never skip)

- Cooperative trust model: honest-executor audit, no broker; reviews are `SELF_ATTESTED_TRACE_BOUND`; a `PASS` is not tamper-resistant and the report never says otherwise.
- The `proofaudit` CLI is the agreed single entry point for authority files (`audit/state/*`, `audit/01-08`, `PROOF_AUDIT.json`) and the paper source; never hand-write them (agreement, not OS-enforced).
- LLM output (proposals, sub-agent shards, Codex text) goes to `audit/inbox/` via `capture --stdin` and enters only through `record`.
- Statement gate before any deep check: no unit proceeds unless `gate.status = PASSED`; a rejected statement gets a new revision, never an in-place patch.
- One lemma/result (or one tight cluster) at a time; never send 20+ pages to a single review. Mechanisms only: no Lean or other formalization (project decision); the label stays `AUDIT_PASS (non-formal)`.
- Main labels (`init --main-label`) are frozen before any issue or review is recorded; adding one later triggers the mechanical impact recompute (S0/S1 may drop to `SUSPECT`, units go `STALE`): never re-grade by hand.
- S0, S1 and every INVALID issue need a failure certificate; without one the issue is `CANDIDATE`/`SUSPECT` and the result stays `UNFINISHED`. Float/random evidence is only ever a `CANDIDATE`.
- Severity is computed by the CLI from axes plus the dependency graph; you propose axes, never the level.
- Codex reviews: model `gpt-5.6-sol`, `xhigh`, fresh thread per result or cluster, prompts rendered by the CLI, file paths only, never Claude's issue or verdict; never fall back to lower effort or another model.
- Counts and tables in the report come only from `report-data`; a fresh read-only fact-check bound to the candidate hash must pass before `finalize-audit`.
- Theorem-using units get a theory route before the deep check (optional layer): REQUIRED patterns' references are read, every theorem application has a use-point matrix, and an upstream FAIL/CONDITIONAL makes downstream stages BLOCKED/CONDITIONAL, never an independent PASS; an unmet hypothesis is not a false theorem.
- Never edit the paper and never silently repair a proof: record the mismatch (proves B, claims A).
- Never pass `--engine` (not implemented); `--assurance` defaults to `draft`; it rises only via `set-assurance --to submission (--anchor ABS | --accept-no-anchor)` and `finalize-audit --assurance` never exceeds the run's level; `--auto-repair` only on explicit user opt-in.
- `repair-integrity` never rebaselines semantic files; only a human runs it, with `--invalidate-all --reviewed-diff-sha256 HASH` for semantic damage (exit code 3 on any mutating command means stop).
- Final label is `AUDIT_PASS (non-formal)`; never "proved" or "formally verified".
- Always `uv run python` (never bare `python`), absolute paths for every `--workspace`.

## Run order

Each step: read the named reference BEFORE executing it (`must-read:`); if a step's file is unread, stop.
CLI = `uv run python "C:\Users\yguo12\.claude\skills\stat-shared-references\scripts\proofaudit_cli.py"`. The full per-command sequence (reviews, finalize, fact-check lifecycle) is in `references\report-template.md`.

1. Resolve `$ARGUMENTS` to absolute paths; re-entering an existing workspace -> `resume` and continue from the phase it returns. must-read: references\workflow-setup-index.md BEFORE this step (session resume).
2. Setup workspace (`init`; submission needs `--anchor` or `--accept-no-anchor`), then bootstrap: read the paper, write the architecture narrative, `index` (dry run), `freeze`. must-read: references\workflow-setup-index.md BEFORE this step.
3. Pass 0: inventory, cross-reference audit, notation ledger, statement gate, input provenance. must-read: references\workflow-pass0.md BEFORE this step.
4. Per unit: provability triage and strategy classification first. must-read: references\contract-and-principles.md BEFORE this step.
5. Pass 1 critical path (sketch-vs-complete first), unit record, step completeness. must-read: references\workflow-pass1.md BEFORE this step. For units that cite classical results: `theory-route`, record activations, read the REQUIRED references, then record `theory_logic` with the local check. must-read: references\theory-logic.md BEFORE this step.
6. Passes 2-3 (support lemmas, global consistency), Pass 4 adversarial (mandatory counterexample attempt for INVALID/S0 candidates), Codex cross-review per shard, then bind and complete. must-read: references\workflow-passes-2-4.md BEFORE this step.
7. Final report: `finalize-result` per unit, `report-data`, narrative slots (`capture` then `report-record`), fact-check, `finalize-audit`, `export`, `snapshot`; then check the acceptance list. must-read: references\report-template.md BEFORE this step.
8. `--post-repair` (after `/proof-repair`, explicit user request only): delta audit plus fresh-thread convergence review. must-read: references\post-repair.md BEFORE this step.

Phase-level commands (everything else is in the references above):

```powershell
uv run python "C:\Users\yguo12\.claude\skills\stat-shared-references\scripts\proofaudit_cli.py" init --workspace "C:\abs\paper-root" --main "C:\abs\paper-root\paper.tex" --assurance submission --anchor "C:\abs\anchors\paper-anchor.jsonl"
uv run python "C:\Users\yguo12\.claude\skills\stat-shared-references\scripts\proofaudit_cli.py" freeze --workspace "C:\abs\paper-root"
uv run python "C:\Users\yguo12\.claude\skills\stat-shared-references\scripts\proofaudit_cli.py" finalize-result --workspace "C:\abs\paper-root" --unit-id U-0007
uv run python "C:\Users\yguo12\.claude\skills\stat-shared-references\scripts\proofaudit_cli.py" finalize-audit --workspace "C:\abs\paper-root"
uv run python "C:\Users\yguo12\.claude\skills\stat-shared-references\scripts\proofaudit_cli.py" export --workspace "C:\abs\paper-root" --format proof-audit-v1 --output "C:\abs\paper-root\PROOF_AUDIT.json"
```

## Read on demand

| Situation | File |
|---|---|
| Authority, commands, flags, final label, operating principles, severity axes, provability triage, pipeline chain | references\contract-and-principles.md |
| Unit looks like a sketch; writing the per-unit `check.json` view; suspected skipped steps | references\workflow-pass1.md |
| Unit cites a classical theorem; route, use-point matrix, probes, `theory_logic` | references\theory-logic.md |
| Diagnostic checklist of typical errors; asymptotic, concentration, optimization, Markov chain, M-estimation papers | references\failure-patterns.md |
| Little time (draft-assurance minimum); crash, stale source, parallel shards | references\workflow-setup-index.md |
| Codex shard coverage and reconciliation | references\workflow-passes-2-4.md |
| Fact-check lifecycle, report structure, acceptance list | references\report-template.md |
| Where did an old section go | references\MOVED.md |

## Stop conditions / hand-offs

- Any review call in state `TIMEOUT`, `ERROR`, `PENDING` or `NOT_RUN` makes the unit `UNFINISHED`; stop that gate, never retry silently or lower effort.
- Exit code 3 from a mutating command means integrity mismatch or STALE source: stop, only a human runs the two-step `repair-integrity`.
- Outstanding sketches (J > 0) cap the judgment at Incomplete; report checked AND unchecked scope honestly.
- Repair is a separate explicit user request (`/proof-repair`); never auto-trigger it; after patches run `--post-repair`.
- Findings Codex and Claude disagree on after 3 rounds per finding escalate to the user.
