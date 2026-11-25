---
name: proof-repair
description: >-
  Generate self-consistent repair plans for mathematical proof issues found by /proofcheck,
  with literature-backed support. For each problematic assumption, model, proposition, or
  theorem, proposes fixes that preserve the full dependency chain and searches arXiv,
  Semantic Scholar, and Google Scholar for new references to support repairs.
  Use when user says "repair proofs", "fix proof issues", "修复证明", "proof repair",
  "修正计划", "fix theorem", "repair assumptions", or wants to go from proof audit to
  actionable repair plan with literature support.
argument-hint: [path-to-workspace] [--unit LABEL] [--from-review SUGGESTION] [--from-reaudit]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch, mcp__codex__codex, mcp__codex__codex-reply
model: opus
---

# Proof-Repair — Literature-Backed Repair Plans for Mathematical Proofs

Run on Claude Opus (`/model opus`). Takes a finished `/proofcheck` audit (final report plus an
`audit-baseline` snapshot ID) and produces per-issue repair proposals with vetted literature support.
Pipeline: `/proofcheck` -> (explicit user request) -> this skill -> `/proof-writer` (inside Run order step 8 (legacy section 5B) only) -> `/proofcheck --post-repair`.
This release only proposes: patches are never applied by this skill. Output is a legacy, non-authoritative
proposal headed `NON-AUTHORITATIVE PROPOSAL`.
`proofaudit <sub>` = `uv run python "C:\Users\yguo12\.claude\skills\stat-shared-references\scripts\proofaudit_cli.py" <sub>`; absolute `--workspace`, never bare `python`.

## Hard rules (never skip)

- Cooperative, honest-executor audit (traces `SELF_ATTESTED_TRACE_BOUND`): nothing here is tamper-resistant; never state or imply PASS, `AUDIT_PASS`, CONVERGED or submission assurance.
- Input is only the frozen `audit-baseline` snapshot; original issues, axes and S-levels are immutable: never re-grade severity; P0-P2 is a scheduling label only; never edit `audit/01-06`.
- Repair is append-only: records live under `audit/07_repairs/` (CLI-written once `repair-record` exists; the Markdown files are generated views); the paper source is never changed.
- MVP (this release) is proposal-only: write only `REPAIR_PROPOSAL_<date>.md` or `audit/inbox/repair-proposals/` (via `capture`); never call `/proof-writer` into `audit/07_repairs`, and stop at the first step that would need `repair-record` or an authority proof package.
- The CLI is the agreed single entry point (not OS-enforced); write only legacy proposal files via `capture` or `REPAIR_PROPOSAL_<date>.md`.
- `repair-record`, `patch-check`, `patch-apply`, `snapshot-restore` and `quote-record` are not implemented: any step needing one stops with "needs `<command>`, which is not yet implemented in the CLI"; never emulate by hand, never fabricate a CLI receipt.
- `--apply` and `--auto-repair` fail fast on entry; `--engine` is not implemented, do not pass or mention it.
- A `PAPER_CITATION` input stays `LOCAL_EXCERPT_ONLY` or `NOT_CHECKED` until `quote-record` exists; a repair depending on it is conditional.
- No LaTeX patch before the reference mode (A or B) is recorded; a post-patch `cross_file_ref_leak` is a patch defect.
- Repair Priority Ladder is a hard gate: Phase A (L1-L3) exhausted before L4/L5; L4/L5 changes need an Assumption-Extension / Weaken-Claim Change Log, else demoted to L6; level is checked against the CLI statement diff.
- Stress tests and reviews are path-only, fresh-thread, `gpt-5.6-sol` `xhigh`, max `MAX_REVIEW_ROUNDS = 3`; TIMEOUT/ERROR is never a pass and never triggers another model or effort.
- Proof content is drafted by `/proof-writer` only at Run order step 8 (legacy section 5B), into the proposal path, marked `Verification: Not checked` until a Codex pass accepts it; `assumptions.lock.md` changes only via the L4 registry step.
- Theory layer: a proposal names the pattern/hypothesis/stage obligation it repairs, redoes downstream stages per the stage DAG, and treats an unmet hypothesis as a use-step repair, not a false theorem. must-read: references\theory-logic.md BEFORE step 3.
- No Lean or other formalization (project decision: mechanisms only).
- Closing a repaired S0/S1 issue uses `diff-record --from SNAP-ID` (the last source-sensitive step) and `issue-close --issue-id I --review-call RV --diff-id D-NNNN`, never a hand-made diff.

## Run order

Each step: read the named reference BEFORE executing it (`must-read:`).

1. Locate inputs (finalized audit and baseline snapshot ID): `uv run python "C:\Users\yguo12\.claude\skills\stat-shared-references\scripts\proofaudit_cli.py" status --workspace "C:\abs\paper-root" --json`; no finalized audit: tell the user to run `/proofcheck` first. must-read: references\pipeline-and-authority.md BEFORE this step (locating inputs, modes).
2. Reference mode (HARD GATE): `proofaudit index --workspace ABS` again if the source changed since freeze; record `reference_mode`. must-read: references\pipeline-and-authority.md BEFORE this step.
3. Triage each issue and pick one repair class; SKETCH-ONLY/PARTIAL-SKETCH units get the expand-sketch treatment. must-read: references\triage-and-classes.md BEFORE this step.
4. Dependency impact analysis per issue. must-read: references\impact-analysis.md BEFORE this step.
5. Ladder gate and 1-3 candidates per issue (feasibility triage, strategy selection). must-read: references\triage-and-classes.md BEFORE this step (ladder and candidates parts).
6. Literature search and quality gate for repair support. must-read: references\literature.md BEFORE this step.
7. Assemble the selected repair per issue as a proposal section. must-read: references\repair-plan-template.md BEFORE this step.
8. MVP branch (proposal-only): optional draft of the repaired proof via `/proof-writer` with `PACKAGE_PATH` under `audit\inbox\repair-proposals\` (non-authoritative, `Verification: Not checked`), then lint it with `proof_gap_scan.py --proof` on that path. If the repair needs `repair-record` or an authority proof package, stop and report "needs `repair-record`, which is not yet implemented". Never write the writer output into the repair-record directory. must-read: references\writer-handoff.md BEFORE this step.
9. Codex stress test of every P0/P1 proposal that has a complete proof (fresh thread, paths only). must-read: references\writer-handoff.md BEFORE this step (stress-test part).
10. Cross-repair consistency (assumption matrix, rate/constant propagation, new reference compatibility). must-read: references\impact-analysis.md BEFORE this step (consistency part).
11. Write the master proposal `REPAIR_PROPOSAL_<date>.md` (headed `NON-AUTHORITATIVE PROPOSAL`) with BibTeX proposals and patch summary; `--apply` is unavailable. must-read: references\repair-plan-template.md BEFORE this step.
12. Report with the Output Summary and tell the user the post-repair steps (manual apply, `freeze --new-revision`, `diff`, `invalidate`, `/proofcheck --post-repair`). must-read: references\repair-plan-template.md BEFORE this step (output-summary part) and references\post-repair.md.

## Read on demand

| Situation | Reference |
|---|---|
| Authority, write boundary, implementation status, register; reading the audit; reference mode; quick mode, `--from-review` | `references\pipeline-and-authority.md` |
| Issue from a theory-pattern stage; naming obligations, downstream stages | references\theory-logic.md |
| Choosing a repair class, priority rules; sketch-only units; ladder, candidates, strategy | `references\triage-and-classes.md` |
| Downstream effects of a repair; cross-repair consistency | `references\impact-analysis.md` |
| Literature for a repair | `references\literature.md` |
| Per-issue repair file, plan structure, closure matrix, BibTeX, patch summary, `--apply`, final summary | `references\repair-plan-template.md` |
| `/proof-writer` handoff, quality gate, Codex stress test | `references\writer-handoff.md` |
| `--from-reaudit`, cycle limits | `references\post-repair.md` |
| Where did an old section go | `references\MOVED.md` |

## Stop conditions / hand-offs

- A step needs an unimplemented command (`repair-record`, `patch-check`, `patch-apply`, `snapshot-restore`, `quote-record`): stop with the fail-fast message.
- `--apply` / `--auto-repair`: stop on entry; the author applies proposed blocks manually.
- Resume: `proofaudit resume` reads only the audit results, there is no repair state machine yet; re-enter by re-reading the proposal file and re-running the steps above.
- No finalized audit: hand back to `/proofcheck` (or a lightweight inline check labeled `unaudited` that cannot feed `--post-repair`).
- Any S0/S1 issue or non-empty semantic diff: convergence is required via `/proofcheck --post-repair`; this skill never declares it.
- No automatic looping of `--from-reaudit`; after 2 cycles downgrade the theorem to NOT CURRENTLY JUSTIFIED and ask the user.
- New proof text: `/proof-writer` (step 8 only); statement or rate redesign: `/theory-design` or `/theory-sharpen`.
- Context for this run: $ARGUMENTS
