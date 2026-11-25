---
name: proof-writer
description: Writes rigorous mathematical proofs for ML/AI theory as a provisional proof package that stays `Verification: Not checked` until a cross-model pass (inside /proof-repair step 5B it writes to the per-issue path it is given). Use when asked to prove a theorem, lemma, proposition, or corollary, fill in missing proof steps, formalize a proof sketch, 补全证明, 写证明, 证明某个命题, or determine whether a claimed proof can actually be completed under the stated assumptions.
argument-hint: [theorem-statement-and-assumptions]
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: opus
---

# Proof Write: Rigorous Theorem / Lemma Drafting

> 🔬 Run this skill on **Claude Opus**. Writing rigorous proofs needs deep reasoning;
> run `/model opus` first if your session is not on Opus.

Write a mathematically honest proof package, not a polished fake proof. The surrounding audit is a cooperative,
honest-executor audit (no broker; review traces are `SELF_ATTESTED_TRACE_BOUND`): a package is never "verified"
by this skill and nothing it produces is tamper-resistant evidence.

Purpose: produce exactly one of three terminal outputs for a claim, never a sketch: (1) a complete proof with every
obligation closed, (2) a corrected (usually weaker) claim plus its complete proof, or (3) a Blockage Record stating
why the claim is not currently justified. Completion means every nontrivial obligation is a typed closure object,
not that the prose reads smoothly. Detail lives in `references\`; read the file named in each step.

## Context: $ARGUMENTS

## Hard rules (never skip)

- Cooperative honest-executor audit: nothing this skill writes is "verified" or tamper-resistant evidence (review traces are `SELF_ATTESTED_TRACE_BOUND`).
- proof-writer never self-verifies: the package header always reads `Verification: Not checked`; never write `Verified`, "Conditionally verified" or any reviewed status; a clean lint certifies closure only.
- Result is a separate line `Writer result: DRAFTED_COMPLETE | BLOCKED`; `STATUS` is exactly one of `PROVABLE AS STATED | PROVABLE AFTER WEAKENING / EXTRA ASSUMPTION | NOT CURRENTLY JUSTIFIED`.
- Write only PACKAGE_PATH (the caller's per-issue path; standalone: `PROOF_PACKAGE_<claim-slug>_<YYYYMMDD>.md`, never overwrite another package); never the paper `.tex`, `assumptions.lock.md`, `cited_results.lock.md`, `audit/state` or `audit/01-06`.
- `assumptions.lock.md` is strictly read-only: invoke assumptions by registry ID, never append a row, never invent `A_new1`; a needed new one is an `ASSUMPTION_CHANGE_REQUEST` with premise `PROPOSED:<issue-id>:<n>`.
- Preserve the user's original statement; a weaker claim or added assumption is a labeled request to the caller, never a silent replacement.
- Every nontrivial obligation ends `CLOSED-LOCAL`, `CLOSED-CITED` (with applicability block) or `BLOCKED` (with attack record); never close an obligation with prose.
- No sketch, partial expansion or deferred step; no "clearly/obviously/by standard arguments"; if only a sketch is completable, output a Blockage Record.
- Any `BLOCKED` obligation forbids `PROVABLE AS STATED`; an `unverified-source` load-bearing citation caps the package at `AUDIT_PASS_CONDITIONAL` territory.
- Locate the verification target and bottleneck before forward algebra (Trap Catalogue in `../stat-shared-references/proof-strategy.md`); write the proof in Big Four register, not bullet lists.
- Cited classical theorems get one chosen hypothesis set and a use-point obligation per hypothesis, ordered by the stage DAG; boundaries, rate ledger and failure-probability budget are explicit lines; never self-pass. must-read: references\theory-logic.md BEFORE step 5.
- Always `uv run python` with absolute script paths (system `python` is a Store stub).

## Run order

Each step: read the named reference BEFORE executing it (`must-read:`).

1. Gather context: caller's package path and frozen statement revision, else user path, else local notes. must-read: references\workflow-steps.md BEFORE this step (section 1, gather context).
2. Normalize the claim; bind assumptions to the lock store read-only. must-read: references\workflow-steps.md BEFORE this step (section 2, normalize the claim).
3. Feasibility triage into exactly one STATUS. must-read: references\workflow-steps.md BEFORE this step (section 3, feasibility triage).
4. Record verification target, bottleneck, resolution path, literature anchor. must-read: references\workflow-steps.md BEFORE this step (strategy-selection part).
5. Build the dependency map and raise numbered obligations `O1..Ok`, lemmas `L1..`, bridges `B1..`. must-read: references\workflow-steps.md BEFORE this step (section 5, build the dependency map and raise obligations).
6. Construct the proof and close every obligation into the ledger. must-read: references\proof-construction.md BEFORE this step (construction and obligation-ledger parts).
7. Fill the package using the exact file structure. must-read: references\package-template.md BEFORE this step.
8. Run the Trap Catalogue checks and record each in `## Verification Checks`. must-read: references\proof-construction.md BEFORE this step (verification-checks part).
9. Lint, resolve every `STRUCTURAL-INCOMPLETE`, review each `CANDIDATE`. must-read: references\proof-construction.md BEFORE this step (verification-checks part).

```powershell
uv run python "C:\Users\yguo12\.claude\skills\stat-shared-references\scripts\proof_gap_scan.py" --proof "<PACKAGE_PATH>"
```

10. Reply briefly: status, `Writer result`, `Verification: Not checked`, claim unchanged or not, obligation count and BLOCKED count, assumption change requests, lint result, file path. must-read: references\constants-and-goal.md BEFORE this step (chat response and key rules part).

## Read on demand

| Situation | File |
|---|---|
| Constants, STATUS and WRITER_RESULT values, goal | references\constants-and-goal.md |
| Cited classical theorem; hypothesis sets, stage order, ledgers | references\theory-logic.md |
| User asks for a sketch, outline, or "just expand a bit" (termination rule) | references\constants-and-goal.md |
| Citing an imported result (applicability block fields) | references\proof-construction.md |
| Lint output unclear, malformed `Verification` line | references\proof-construction.md |
| Where did an old section go | references\MOVED.md |

## Stop conditions / hand-offs

- Claim false or not completable: write the Blockage Record (`NOT CURRENTLY JUSTIFIED`) with counterexample or repaired statement.
- Verification is never granted here; the orchestrator sets it after a Codex pass (`/proof-repair` step 8 / reference 5B, `/proofcheck`).
- Output produced after a plan reached `CONVERGED` re-opens the plan (the caller forces a new `--post-repair`).
- Missing lock file for a multi-theorem framework: proceed with local assumptions and flag that `theory-design` should initialize one.
