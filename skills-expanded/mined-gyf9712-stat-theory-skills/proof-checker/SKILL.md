---
name: proof-checker
description: Cross-model deep-review worker for the proof pipeline. Reviews one theorem/lemma or cluster (or a whole paper when run standalone) through independent GPT-5.6-Sol xhigh review, records issues with failure certificates in the shared proofaudit workspace, and never edits the paper. Whole-paper orchestration and the final report belong to /proofcheck. Use when user says "verify proof", "审证明", "check this proof", "deep review this lemma", or wants an independent cross-model check of a specific proof; use /proofcheck for "proof check" of a full paper.
argument-hint: "[path-to-tex-file or unit label] [--deep-fix] [--restatement-check] [--workspace ABS]"
allowed-tools: Bash(*), Read, Grep, Glob, Agent, mcp__codex__codex, mcp__codex__codex-reply, mcp__manual_review__review, mcp__manual_review__review_reply
---

# Proof Checker: Rigorous Mathematical Verification & Fixing

Cross-model deep-review worker of the proof pipeline (`/proofcheck` is the orchestrator and report owner).
It reviews one theorem/lemma or cluster (or a whole paper standalone) through independent fresh-thread
`gpt-5.6-sol` `xhigh` review and records issues with failure certificates in the shared `proofaudit`
workspace. It is read-only: no paper edits; fixes belong to `/proof-repair`. Do not wrap it in `/loop`,
`/schedule` or `CronCreate` (verdict-bearing, threads reviewer memory across phases).
`proofaudit <sub>` = `uv run python "C:\Users\yguo12\.claude\skills\stat-shared-references\scripts\proofaudit_cli.py" <sub>`;
absolute `--workspace` paths, never bare `python`. Spec files in `../stat-shared-references/` win over any wording here.

## Hard rules (never skip)

- Cooperative, honest-executor audit (traces `SELF_ATTESTED_TRACE_BOUND`): a submission PASS is not tamper-resistant; never claim otherwise.
- The CLI is the agreed single entry point for authority files (not OS-enforced; direct edits are caught later by the hash chain); structured output goes through `capture --stdin` then `record`.
- This worker is read-only: it never edits the paper, never applies a fix, and owns no final verdict or report.
- Reviewer is fixed `gpt-5.6-sol` + `xhigh` (manual backend: non-Claude at `xhigh`); no model or effort fallback; unavailable means `REVIEW_UNAVAILABLE` and blocks the gate.
- Review prompts are path-only, rendered by `review-begin`; never paste or paraphrase the proof or tell the reviewer what you found.
- Fresh thread for every independent unit/cluster review; `codex-reply` only re-checks the reviewer's own finding with updated artifact paths and finding IDs, never fix summaries.
- Every S0, S1 and INVALID issue needs a failure certificate (exact counterexample or failing step); without one it stays a candidate.
- Label "counterexample found" only if verified in exact arithmetic via `evidence-run`; max `MAX_REVIEW_ROUNDS = 3` per finding.
- TIMEOUT/ERROR calls block the verdict and are never silently retried or downgraded.
- Verdicts are derived by `finalize-result`, never LLM-set; every count in a report comes from the CLI (`report-data`) plus an independent fact-check.
- `PROOF_AUDIT.json` is produced only by `proofaudit export`, never hand-written (key set in `references\submission-artifact.md`; the pre-2.0 schema in `references\legacy-submission-schema.md` is superseded).
- Main labels are frozen by the orchestrator before any issue is recorded; a later main-label change triggers the mechanical impact recompute, never a hand re-grade. Submission assurance is raised only by `set-assurance --to submission (--anchor ABS | --accept-no-anchor)`.
- Theory layer (optional): audit the route for missed patterns, read the REQUIRED references, follow the stage DAG (upstream FAIL/CONDITIONAL => downstream BLOCKED/CONDITIONAL); an unmet hypothesis of a cited theorem is a failed use step, never a false theorem, and one textbook hypothesis set must not reject a valid alternative route.
- No Lean or other formalization (project decision: mechanisms only); one result or tight cluster per review, never 20+ pages at once.
- Suggestions that add conditions or weaken a claim are flagged L4/L5 candidates (they need a Change Log in `/proof-repair`); they never edit a statement.

## Run order

Each step: read the named reference BEFORE executing it (`must-read:`).

1. Resolve the workspace: `proofaudit status --workspace ABS` / `proofaudit resume --workspace ABS` if `audit/state/RESULTS.json` exists, else:
   `uv run python "C:\Users\yguo12\.claude\skills\stat-shared-references\scripts\proofaudit_cli.py" init --workspace "C:\abs\paper-root" --main "C:\abs\paper-root\paper.tex"`
   `uv run python "C:\Users\yguo12\.claude\skills\stat-shared-references\scripts\proofaudit_cli.py" index --workspace "C:\abs\paper-root"`
   `uv run python "C:\Users\yguo12\.claude\skills\stat-shared-references\scripts\proofaudit_cli.py" freeze --workspace "C:\abs\paper-root"`
   must-read: references\phase-0-5-obligation-ledger.md BEFORE this step.
2. Read the canonical index; pick the target unit/cluster; the statement gate must be `PASSED` (else run the `statement-gate` review first). must-read: references\phase-0-5-obligation-ledger.md BEFORE this step.
3. Build the proof-obligation ledger (DAG, assumptions, symbols, quantified statements, micro-claims, limit-order map). must-read: references\phase-0-5-obligation-ledger.md BEFORE this step. For units citing classical results also `theory-route` and a use-point matrix. must-read: references\theory-logic.md BEFORE this step.
4. Render the prompt: `proofaudit review-begin ...` (writes the call `PENDING`). must-read: references\role-and-commands.md BEFORE this step (reviewer protocol and Phase 1 prompts are parts of it).
5. Call `mcp__codex__codex` (`model: gpt-5.6-sol`, `config: {"model_reasoning_effort": "xhigh"}`) with `prompt.txt` verbatim; first action on return `proofaudit review-bind`, then `proofaudit review-complete --receipt ...` (`review-correct-response`, max 2, for malformed output). must-read: references\role-and-commands.md BEFORE this step.
6. Capture and record findings: `proofaudit capture --stdin` then `proofaudit record`; the CLI allocates IDs and computes severity. must-read: references\taxonomy.md BEFORE this step (taxonomy, severity axes, side-condition checklists).
7. Counterexample red team on every key lemma and every INVALID/S0 candidate: `proofaudit evidence-run`, `proofaudit evidence-validate`; inputs via `proofaudit input-check`. must-read: references\red-team.md BEFORE this step.
8. Optional `--deep-fix`: repair-suggestion records for `/proof-repair --from-review`. must-read: references\deep-fix-mode.md BEFORE this step.
9. After the paper changed (newer freeze): re-check own findings by reply on the same thread, then blind fresh-thread re-review for every semantic diff or S0/S1 repair; `proofaudit diff`; `diff-record` is the last source-sensitive step before `issue-close`. must-read: references\red-team.md BEFORE this step (closure and blind re-review part).
10. Optional `--restatement-check`. must-read: references\red-team.md BEFORE this step (restatement regression part).
11. Per unit: `proofaudit finalize-result`; if the gate is stuck after MAX_REVIEW_ROUNDS write the Proof Unrecoverable Report. must-read: references\report-and-state.md BEFORE this step.
12. Standalone report: `proofaudit report-data`, narrative slots via `capture` + `report-record`, then the full fact-check lifecycle (`factcheck-begin`, MCP call, `review-bind`, `review-complete`, `factcheck-record`), `proofaudit finalize-audit`. must-read: references\report-and-state.md BEFORE this step (full sequence: `/proofcheck` report-template).
13. Export: `proofaudit export --format proof-audit-v1` (never hand-write `PROOF_AUDIT.json`). must-read: references\submission-artifact.md BEFORE this step.
14. If a wiki is active add claim-ledger entries (additive, non-blocking); optional `/render-html` of the final report (`RENDER_HTML = true`). must-read: references\phase-0-5-obligation-ledger.md BEFORE this step (wiki claim-ledger part).

## Read on demand

| Situation | Reference |
|---|---|
| Constants, role, command conventions, reviewer call states, acceptance gate, Phase 1 prompt, rigor/cross-model/scope rules | `references\role-and-commands.md` |
| Unit cites a classical theorem; route, use-point matrix, probes, `theory_logic` | `references\theory-logic.md` |
| Classifying an issue; severity axes; applying a named theorem (DCT, Fubini, ...) | `references\taxonomy.md` |
| Building the obligation ledger; research wiki | `references\phase-0-5-obligation-ledger.md` |
| Counterexample search; re-check, global closure, blind re-review; `--restatement-check` | `references\red-team.md` |
| `--deep-fix`; example invocations | `references\deep-fix-mode.md` |
| Report, state persistence, unrecoverable proof, output file list | `references\report-and-state.md` |
| `PROOF_AUDIT.json` keys, verdict table, thread independence | `references\submission-artifact.md` |
| Old (pre-2.0) `PROOF_AUDIT.json` schema, superseded, archive only | `references\legacy-submission-schema.md` |
| Where did an old section go | `references\MOVED.md` |

## Stop conditions / hand-offs

- Acceptance gate unmet after MAX_REVIEW_ROUNDS, or a gate stuck on TIMEOUT: result stays `UNFINISHED`, emit the Proof Unrecoverable Report; never declare success silently.
- Manual backend unavailable: stop and print the install command; do not fall back to Codex.
- Source changed since freeze (`STALE`, exit code 3): re-run `index` / `freeze`; do not review stale text.
- Fix design, ladder, change logs, patches: hand to `/proof-repair` (`--from-review` for deep-fix suggestions).
- Whole-paper orchestration, final report, convergence: `/proofcheck`.
- Context for this run: $ARGUMENTS
