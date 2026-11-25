---
name: lean-reduce
description: Shorten and speed up kernel-verified Lean proofs for the Lean Refactor Arena, judging every candidate with the public Arena score computed locally. Use when reducing, refactoring, golfing or re-scoring Lean proofs for the arena, running `rma reduce`, deciding whether a candidate proof is better, or estimating a submission's score before sending it.
---

# Lean proof reduction against the public Arena score

## The objective is public — compute it, do not wait for the server

    problem score = mean( length reduction % , heartbeat reduction % , zero-shot compatibility % )
    your score    = mean of the problem scores over ALL benchmark problems

- length reduction % = 100 · (1 − L / R). `L` counts tokens of the proof body after `:=`
  (comments ignored); `R` is the ORIGINAL reference length (`proof_length` in the benchmark).
- heartbeat reduction % = 100 · (1 − H / RH). `H` is `#count_heartbeats` of the declaration;
  `RH` is the ORIGINAL reference count (the "of N" in an official row). Not clamped: slower than
  the reference is negative.
- zero-shot % = share of the problem's listed `version_info` toolchains on which the proof
  compiles unchanged.
- A missing, non-compiling, statement-changing or forbidden-pattern proof scores 0 on all axes and
  still counts in the mean.

Denominators are the ORIGINAL proof's counts, not the current best's, so the axes are not
equally weighted relative changes. For one problem at fixed compatibility:

    Δ problem score = 100/3 · ( ΔL_saved / R + ΔH_saved / RH )      Δ run score = Δ problem score / N

1 token is worth 100/(3R) points; 100 heartbeats are worth 10⁴/(3·RH). A shorter proof that is
slower can lose, and a longer one that is much faster can win — compute both before judging.
Losing one of k listed versions costs 100/(3k) points, which almost never pays.

## How to measure locally (what `rma reduce` does)

- `rma/reduction/score.py` implements the rule. `arena_tokens(body)` is a Lean-aware lexer fitted
  to 41 official (proof, length) pairs: 21 exact, mean absolute error 1.3 tokens.
- Heartbeats: compile with the Arena harness (`#count_heartbeats in` for Mathlib-based corpora,
  the `#reduce_count` elaborator for Strata) in the pinned repository; unchanged proofs reproduce
  the server's count exactly.
- Zero-shot: compile the unchanged proof in a checkout of every listed commit. Versions not
  prepared locally are reported as a lower/upper bound, never assumed to pass.
- `rma reduce` ranks candidates by this score, promotes only kernel-verified candidates that pass
  every configured listed version, writes per-problem `score` bounds into `state.json`, and the run
  estimate into `results.json` (`estimated_score.run_lower` / `run_upper`).

## Local environment (this machine)

- Toolchains: `~/.elan` (v4.26.0, v4.30.0, v4.31.0, v4.32.0, v4.33.0-rc2); the arena copy lives in
  `~/code/lean-refactor-arena/tools/elan`.
- Pinned sources: `~/code/lean-refactor-arena/sources/{strata,physlib,leanprover-cslib-3aa9d44,arklib,mathlib426}`.
  Older listed commits: `sources/versions/<corpus>-<version>` (pass each with another `--repo CORPUS=PATH`).
- Current best submission, official 77.98%: `~/code/lean-refactor-arena/round4/delivery/`;
  later local improvements live in `rma_reduce_round*/submission.jsonl`.

## Use RMA's loop, not only rewrites

`rma reduce --mode rma` runs critic → solver → literature → meeting → revise → concepts → evaluator per round. Prefer it when a
proof has concrete local waste (unused simp arguments, a `have` used once, repeated steps, heavy automation): issues are located
and ranked by expected points, fixes are small anchored patches, failed moves are remembered with Lean's reason, and the meeting
plans the coordinated rewrite from that evidence. Judge every change by the public score, never by the issue's estimate.

## Reduction patterns that paid on this benchmark (see documents/development/rma-reduce-literature.md)

1. **Shotgun automation → explicit reasoning** (heartbeats): replace `grind`/`aesop`/`simp_all`/`nlinarith`/`tauto`
   by the lemma, constructor term or narrow closer that proves that exact goal (07: −97% HB; 15: −98% HB).
2. **Merge symmetric branches** (length): `refine ⟨?_, ?_⟩ <;>`, `first | a | b`, multi-alternative `case a | b` (11).
3. **Library lemma instead of re-proof** (both): search the pinned sources before an induction or `have … := by` (12).
4. **Terms instead of scaffolding** (length): inline single-use `have`, `⟨_, _⟩`, dot-constructors, `fun _ h => …`.
5. **Restructure machine-generated proofs** around the two or three real lemmas (15: 289 → 47 lines).
6. **Minimal simp sets, delete no-ops** (both): Lean's `unusedSimpArgs` and Mathlib's `linter.unusedTactic` are
   free, kernel-backed deletion signals; run them before any model call.

Length and compile cost are only weakly correlated (Lean Refactor, arXiv 2605.20244): pick the strategy for the axis
with more remaining points, and never accept a shorter proof without measuring its heartbeats. Resampling from the
current best beats long repair chains (ProofOptimizer, arXiv 2510.15700); keep one compiler-feedback repair for
high-value moves only.

## Defaults (use these unless comparing)

`rma reduce` defaults to `--mode rma`: a strategy-driven rewrite opens every round, then Lean-lint and proof-state
informed critic issues, localized patches (one compiler-feedback repair for issues worth >= 1 point), grounded library
lookup, meeting -> revise, and API-free local search closing each round. `--mode flat` is the older rewrite portfolio.
Note honestly: on the one paired comparison run so far, flat still scored higher on 04/05/08/11 (+7.1/+7.4 vs +4.6),
concentrated entirely in problem 11; the every-round rewrite is the fix and is not yet validated.

## Rules that stay fixed

- Keep the statement byte-identical; only the body after `:=` changes. No `sorry`, `admit`, new
  axioms, `native_decide`, `unsafe`, `#eval`, `IO.*`, metaprogramming or extra declarations.
- The target's axiom audit may only show `propext`, `Classical.choice`, `Quot.sound`.
- Spend only within the user's gpt-6-astra budget; reuse the run's ledger, never reset it.
