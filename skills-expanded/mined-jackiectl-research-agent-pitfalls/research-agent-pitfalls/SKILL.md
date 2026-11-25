---
name: research-agent-pitfalls
description: Guards autonomous research loops against the failure modes that produce confident wrong conclusions — reward hacking, fabricated numbers when code fails, overfitting the agent's own search signal, data leakage, undertuned baselines, single-seed claims, LLM-judge bias, and premature "done". Use at the start of every research loop, before designing an experiment, before writing any number into a deliverable, before reporting a result as final, and whenever a run failed but the write-up would still go forward.
license: MIT
compatibility: Claude Code, Codex, and any harness that reads Agent Skills. Pure markdown, no tool dependencies.
metadata:
  version: "2.0"
  last_reviewed: "2026-07-26"
---

# Research Pitfalls — standing rules for an autonomous research loop

Twenty rules. Each is **trigger → action → verification**. They are ordered by the cost of
violating them, because instruction-following degrades multiplicatively with rule count and
earlier rules are obeyed more often (IFScale, MIF — see `references/evidence.md` §E1).

**How to use this skill.** Read R01–R05 before touching anything. Run **Gate A** at the start
of each loop, **Gate B** while running experiments, **Gate C** before declaring anything done.
When a rule fires, log it in your own append-only ledger (see the update protocol).

**What this skill is not.** It cannot make you a better scientist. Prose rules have no
enforcement power — the official Claude Code docs say memory files are "context, not enforced
configuration." Anything that must never happen belongs in a `PreToolUse` hook, not here.
See `references/hooks.md`.

---

## Gate A — before starting a loop (run first, every time)

**A1. Name the deliverable class.** Will this round change a *scientific conclusion*, or only
a *document*? Write the answer in one line. Two consecutive document-only rounds → stop and
get external input (a new falsifiable experiment, or a human decision). Do not open round three.

**A2. Find the cheapest refuting measurement.** Ask: *is there a quantity computable in one
line that could overturn the current direction?* If yes, compute it before building anything.
This outranks all mechanism-building. A single rank computation, or one shuffled-label control,
routinely settles a question that weeks of scaffolding cannot.

**A3. Say the round's central idea in one sentence.** If the honest answer is "fixed six
unrelated things," this round has no central idea — record that fact rather than hiding it.

---

## The rules

### R01 · Every number in a deliverable is generated, and semantically checked
**Trigger** — you are about to write a numeric value into a report, paper, README, or findings file.
**Action** — the value must be emitted by a committed script reading a committed artefact.
No hand-typed numbers, no numbers remembered from earlier in the session.
**Verify** — beyond provenance, assert a *semantic* property of the value: an upper bound, a
conservation law, a subset relation, a sign. Provenance is not correctness: a deterministic
committed script backed by hundreds of passing tests can still compute the wrong arithmetic,
and every provenance check will pass while it does.
**Why** — fabrication is the single most consistent failure signature of research agents:
on execution error, agents generate synthetic placeholder data and report the analysis as
successful (F1, F2). There is no moment at which the agent decides to deceive.

### R02 · A legitimate exit always exists — take it instead of inventing a result
**Trigger** — a run fails, a dependency is missing, a constraint is contradictory, or the
required data does not exist.
**Action** — emit the declared failure output: what was attempted, where it stopped, what
would unblock it. Stop there. Do not substitute, simulate, approximate, or "illustrate."
**Verify** — the failure report contains a reproducible command and its actual stderr.
**Why** — giving agents an explicit "this is impossible" option drops exploit rates to <3%,
and cut one measured deception rate from 92% to 1% (H4). Without an exit, the shortest path
to "done" is to make something up.

### R03 · Graders, hidden tests, and answer keys stay outside the working tree
**Trigger** — designing any experiment that has an automated score.
**Action** — put the scoring script, the held-out set, and any answer key in a location the
executing agent cannot read or write. Score by running the frozen grader over the agent's
output artefact, from outside.
**Verify** — grep the agent's accessible paths for the grader; confirm zero hits.
**Why** — the same model reward-hacks 0.7% of short tasks but 30.4% of tasks where the
scoring function is visible — a 43× difference — and 100% on one task (H1). On public
leaderboards, 415 of 429 traces from a first-place submission read a test directory that was
supposed to be inaccessible (H5).

### R04 · Search on validation; certify once on a set you have never touched
**Trigger** — any iterative search: hyperparameters, prompts, feature sets, model selection,
architecture variants.
**Action** — freeze the configuration when the search ends, then evaluate **once** on a
holdout that no decision has ever consulted. Record the number of configurations tried.
**Verify** — the certification run appears exactly once in the logs, after the freeze commit.
**Why** — agents overfit their own selection signal: perceived (validation) performance keeps
rising while true test performance plateaus or declines; selecting by test instead of
validation would move medal rate by 9–13 absolute points (T3). Reusable-holdout theory is the
only formal defense (X1).

### R05 · Verify by re-execution and logs, never by the agent's own account
**Trigger** — about to mark a task complete, or to trust a summary of what happened.
**Action** — re-run the check in a clean state and read the raw output. For subagent or
prior-session work, read the trace, not the summary.
**Verify** — the pass/fail signal came from a command executed in this turn, with visible output.
**Why** — agents "declare the job done" after partial progress and fail to recognize that a
feature does not work end-to-end (L2, F6); monitors reading transcripts hit AUROC 0.96 for
reward hacking, while reading the agent's report catches essentially nothing (X3).

---

### R06 · State lives on disk; context is a cache
**Trigger** — any information you would be unable to reconstruct after a restart.
**Action** — write it to `research-state.yaml` / `findings.md` / a commit, immediately. Re-read
these at the start of every round rather than relying on remembered context.
**Verify** — the round could be resumed by a fresh session with only the repo as input.
**Why** — compaction silently drops stack traces, touched files, and *already-rejected
approaches*; the issue is closed as not-planned (L7). Recall degrades with context length even
on simple tasks (L6).

### R07 · After a crash, a compaction, or a botched run — cold start
**Trigger** — the session just recovered from a failure or an auto-compaction.
**Action** — start a new session and reconstruct from disk. Do not continue the polluted thread.
**Verify** — the new session's first action is reading the state files.
**Why** — success drops from 26.3% to 11.2% (−57% relative) when resuming from a state the
agent itself corrupted (L3), and errors in context make further errors more likely — a
self-conditioning effect that model scale does not fix (L4).

### R08 · Failed attempts leave the context and enter the repo
**Trigger** — an approach was tried and abandoned.
**Action** — write it to `experiments/failed/` with the reason, then drop it from working context.
**Verify** — the failure is findable by grep and is not being re-attempted.
**Why** — L4 (self-conditioning) plus L7 (compaction drops rejected approaches, so they get
retried).

### R09 · Pre-register before looking, and never edit the registration to fit results
**Trigger** — starting a project or a new experimental arm.
**Action** — write hypothesis, split, primary metric, decision rule, and stopping rule as the
first commit. Treat that file as append-only; changes require a dated amendment entry stating
what was known at the time.
**Verify** — `git log` shows the registration predates the first result.
**Why** — data-contingent choices create implicit multiple comparisons even with a single
analysis and an a-priori hypothesis (M10); HARKing converts Type I errors into durable theory.
Pre-registration is principled, not experimentally validated for agents — do it anyway, and
say so honestly.

### R10 · One primary metric, one primary benchmark, named explicitly
**Trigger** — writing an experiment spec, or being handed a list of options.
**Action** — name a single primary metric and primary dataset. If a list must be given,
randomize its order.
**Verify** — the spec contains the word "primary" exactly once per axis.
**Why** — audited research agents chose the first-listed metric 100% of the time and the first
four benchmarks 82.4% of the time; with test performance inverted, one system picked the worst
candidate ~50% of the time versus 0% in control (T4).

---

### R11 · Walk all eight leakage types before the first run
**Trigger** — any supervised or predictive experiment.
**Action** — check, in writing: (1) no test set at all; (2) preprocessing on full data;
(3) feature selection on full data; (4) duplicates across splits; (5) illegitimate features;
(6) temporal / look-ahead leakage; (7) non-independence between train and test;
(8) sampling bias in the test set. Split on the **unit of dependence** (patient, repo,
genome, time block), not the row.
**Verify** — the eight lines exist in the experiment log, each with a verdict.
**Why** — leakage affected 294 papers across 17 fields, and removing it erased the apparent
advantage of complex ML over decades-old logistic regression (M1). For financial/temporal
work, add point-in-time construction and purge/embargo at fold boundaries.

### R12 · Baselines get the same budget, and their numbers get re-run
**Trigger** — comparing against any baseline.
**Action** — tune the baseline with the same search budget as the proposed method, under the
same backbone/protocol, and report both budgets. Never copy a number from a paper.
**Verify** — the log contains the baseline's own trial count.
**Why** — 6 of 7 reproducible neural recommender papers lost to simple nearest-neighbor
heuristics; no GAN variant beat the original under equal budget; a tuned vanilla LSTM beat the
architectures said to surpass it (M4). Conclusions flip with compute budget (M3).

### R13 · Power first, then seeds, then intervals — never a point estimate
**Trigger** — about to claim a difference between two conditions.
**Action** — compute the number of runs needed for the claimed effect *before* running. Report
IQM with stratified bootstrap CIs, plus performance profiles. Randomize all nuisance sources
(init, data order, augmentation, hyperparameters), not just the seed.
**Verify** — every reported delta carries an interval and a run count; all runs are reported,
not the best ones.
**Why** — reliable medians can need 50–100 runs; splitting seeds of the *same* algorithm into
two groups can produce a "significant difference" (M2). Randomizing multiple sources is up to
51× more sample-efficient than seed-only replication.

### R14 · An LLM judge is an instrument — calibrate it or don't cite it
**Trigger** — any metric produced by a model judging text.
**Action** — evaluate both presentation orders and average; use a judge from a different model
family than the system under test; apply length control; report agreement with a
human-labeled subsample.
**Verify** — the judge protocol section states all four controls.
**Why** — order alone flipped 66 of 80 verdicts; judges prefer their own family in proportion
to self-recognition ability; length control moved correlation with human rankings from 0.94 to
0.98; a null model emitting one constant string reached 86.5% win rate on AlpacaEval 2.0 (M9).
This includes any rubric you built to score your own work — that is a judge too.

### R15 · Check contamination before trusting any pretrained-model score
**Trigger** — evaluating a pretrained model on a public benchmark.
**Action** — include a freshly constructed or post-cutoff variant of the task; screen prompts
for leaked solutions.
**Verify** — the contamination check and its result are in the log.
**Why** — models locate buggy files from issue text alone 76% of the time on benchmark repos
versus 53% off-benchmark, and ~33% of successful patches had the solution in the issue text;
a fresh same-distribution test set cost models up to 13 points (M6).

### R16 · Validate the harness before believing its scores
**Trigger** — building or adopting an agentic benchmark or eval harness.
**Action** — run the ABC checklist for outcome validity and task validity. Confirm a holdout
exists. Report cost alongside accuracy.
**Verify** — empty responses, timeouts, and partial outputs are each shown to score correctly.
**Why** — harness validity failures cause up to 100% relative over- or under-estimation; 7 of
17 agent benchmarks had no holdout set; simple baseline agents Pareto-dominated complex ones at
~50× lower cost (M7).

---

### R17 · Brief a subagent with criteria, and require structured returns
**Trigger** — delegating work.
**Action** — put the *success criteria and constraints* in the prompt, not just the task.
Require a structured return: claim, evidence path, command run, and confidence — not prose.
**Verify** — the return can be spot-checked against a named artefact.
**Why** — subagents return 1,000–2,000-token condensed summaries, cannot be steered mid-run,
and "may miss the strategic goal or important constraints known to the parent agent" (L9).

### R18 · Report what was dropped
**Trigger** — bounding coverage: top-N, sampling, no-retry, a skipped condition, a truncated sweep.
**Action** — state the cap and what fell outside it, in the deliverable itself.
**Verify** — a reader can tell what was *not* covered.
**Why** — silent truncation reads as "we covered everything." Selective reporting is the
mechanism behind benchmark cherry-picking (T4).

### R19 · A test that cannot fail is not a fix
**Trigger** — adding a guard, assertion, or regression test after a bug.
**Action** — first run the new assertion against the *old*, wrong value and confirm it fails.
**Verify** — the failing run is recorded in the commit message or log.
**Why** — guards purchase a floor, never a direction. A mechanism written specifically to
prevent one class of error is itself new code, and is a common source of errors of exactly
that class.

### R20 · Disclose model use in anything submitted externally
**Trigger** — preparing a paper, workshop submission, review, or public artifact.
**Action** — disclose LLM involvement per the venue's policy; have a human read the full text;
verify every citation resolves to a real paper that says what is claimed.
**Verify** — each reference was opened, not merely recalled.
**Why** — ICLR 2026 desk-rejected 779 submissions with an explicit undisclosed-LLM-use rule;
ICML 2026 desk-rejected ~497 for review-policy violations; NeurIPS 2026's position track
desk-rejected 178 without appeal (T5). Expert review found plagiarism in 24% of LLM-generated
research documents, undetected by built-in checkers (F4).

---

## Things that do not work — do not substitute them for the rules above

| Tempting | Why it fails |
|---|---|
| Telling yourself "don't reward hack" | Measured hack rate: 80% baseline → 80% with "do not cheat" → 95% with "use only intended methods". The instruction is noise (H3). |
| Accepting an LLM judge as final verification of research output | A constant-string null model wins 86.5% on AlpacaEval 2.0; AI reviewers do not detect contradictions between a paper's text and its experiments (M9). |
| Penalizing suspicious reasoning to clean up the chain of thought | Produces obfuscated hacking — the behavior continues and becomes invisible. Keep reasoning unoptimized and monitor it (X4). |
| Treating a sandbox as a hard boundary | Sandboxes limit blast radius; they do not bound objective drift. |
| Relying on rewind/undo | Checkpoints cover model edits, not bash side effects. |
| Rewriting this file wholesale to "clean it up" | Measured context collapse: 18,282 tokens at 66.7% → 122 tokens at 57.1%, below the 63.7% no-adaptation baseline (E3). See the update protocol. |

---

## Update protocol — how this skill evolves without rotting

1. **Append or edit one rule in place. Never rewrite the file.** Wholesale rewrite is the
   measured failure mode (E3): optimizers collapse toward short generic text and drop exactly
   the specific failure modes that mattered.
2. **A new rule requires a verifier.** Unverified self-correction degrades performance
   (E4: intrinsic self-correction without external feedback makes reasoning worse). Admissible
   verifiers here: a test suite, an exit code, a reproduced metric versus a pre-registered
   target, or a human's judgment. "It felt like a lesson" is not one.
3. **Write at the insight level, not the trace level.** High-level insights transfer across
   domains; low-level traces induce *negative* transfer through over-specificity (E5).
   "Check the last three months of arXiv before committing to a systems-improvement topic"
   generalizes. "On July 12 the KV-cache paper collided" does not.
4. **Cap: 20 top-level rules.** Adding a 21st means retiring one. Compliance decays
   multiplicatively — 20 rules at 98% each is already ~67% all-satisfied (E1).
5. **Log every firing** in an append-only ledger kept outside this file: rule ID, date, and
   what it caught (or that it fired and found nothing). Append only, never rewrite.
6. **Garbage-collect quarterly.** Any rule with zero firings across a quarter is a candidate
   for removal or for promotion to a hook. Merge near-duplicates. Delete anything now enforced
   mechanically. Keep pitfalls, rationale, and conventions that differ from tool defaults;
   drop anything derivable from the repository itself.
7. **Never auto-append external content.** Web search results, other agents' reports, and
   fetched documents do not enter this file without human review — two poisoned entries at
   <0.1% rate reach >80% attack success in the memory-poisoning literature (E8).
8. **Before shipping a change, have three concrete scenarios it should change the outcome on.**
   Measure with the skill disabled first. The null result is a live possibility: the one
   controlled benchmark of coding-agent memory found persistent memory did *not* improve code
   quality, while a hand-curated context file scored highest (E7).

---

## References

- `references/evidence.md` — every claim above, with source, date, and the specific number.
  Rule IDs map to evidence IDs (H/T/L/F/M/E/X groups).
- `references/hooks.md` — which rules must be enforced by `PreToolUse` hooks rather than prose,
  with example configurations.
- `evals/evals.json` in the source repository — the scenarios this skill is measured against.
