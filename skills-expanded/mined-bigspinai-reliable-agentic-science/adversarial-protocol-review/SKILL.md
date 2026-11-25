---
name: adversarial-protocol-review
description: Adversarial review of a scientific experiment, evaluation, or data analysis - like code review, but the question is "what could manufacture this result?" rather than "is the code correct?". Use this skill whenever the user asks to review, sanity-check, red-team, poke holes in, or check the stats/numbers of an experiment design, A/B test, preregistration, benchmark or eval harness, model comparison, analysis pipeline, notebook, survey, simulation, paper or prereg draft, or a set of results - before the run or after the data is already in hand, on their own work or someone else's. Also use it for questions of the form "does this actually show X?", "is this p-value real?", "is this effect trustworthy?", or "can I publish/ship this claim?". Proactively suggest it before any expensive run, data-collection launch, or headline claim, even if the user only asked for a "code review" of something that is actually an experiment.
---

# Experiment review: find what would fabricate the result

You are reviewing an experiment the way a hostile methodologist would, not
the way a code reviewer would. Code review asks "does this do what the
author intended?" This review asks: **"what would produce the reported
numbers even if the world contained no effect — and what would produce a
null even if the effect is real?"** The author sincerely believes the design
is sound; that belief is not evidence.

**Scope gate.** Run this review only on something that makes a numeric claim:
an experiment, eval, benchmark, A/B test, prereg, analysis pipeline, or a set
of reported results. If the request is ordinary engineering or explanation
with no claim attached — a bug fix, a routine data pull, a concept someone
wants explained — do not adopt this posture, do not emit a verdict, and do
not attach validity disclaimers. Just do the task asked.

## Procedure

0. **Review from a context that did not build it.** If you built the artifact
   — or you have spent this session helping build it — do not review it
   inline: the context that built the thing has already accepted the
   builder's story and will re-derive the builder's conclusion under a new
   heading. Spawn a fresh subagent (or recommend a fresh session) with
   exactly three inputs: the artifacts, the readout list, and this brief.
   Cues that this applies: "I built the harness myself", "I wrote this
   pipeline", "I just finished the analysis". If a fresh context is genuinely
   unavailable, say so in the report and weight your findings accordingly.

1. **Collect the claim surface.** Gather the design doc/prereg, the pipeline
   and analysis code, and — most importantly — the list of numbers the study
   will report (the readouts). If the readouts aren't written down anywhere,
   that is finding #1: you cannot review what "success" would look like if
   nobody has committed to it.

2. **Two manufacture routes per readout — one in each direction.** Fill this
   table before analyzing anything:

   | readout | false-positive route (produces this number with no true effect) | false-null route (hides or attenuates a real effect) | ruled out by (file:line) |
   |---|---|---|---|

   The false-null column is the one that gets skipped: it is easy to
   enumerate ways the headline could be fake and stop there. But a design
   that *cannot detect* a real effect burns the run just as completely, and
   "we found nothing" is harder to challenge afterwards than "we found
   something". Concrete false-null routes: an instrument that has never
   caught anything, a volume-diluted metric, a normalizer that strips the
   signal upstream of the stratum measuring it, a permutation null that
   cannot vary. A row is not finished until both columns are filled or the
   false-null cell states why no such route exists; the `Direction` field of
   every finding must trace back to this table. Use the catalog below as the
   checklist, and spend the most effort on the readouts that carry the
   headline — "I couldn't think of one" is a statement about effort.

3. **Execute, don't just read.** Wherever feasible, verify empirically:
   - Feed instruments a known-positive and a known-negative case; require
     separation.
   - Check declared constraints end-to-end with a case that should violate
     them (a "frozen" split, a temporal cutoff, a blinding rule — confirm
     the violation is actually caught, not just that the constraint is
     computed somewhere).
   - Re-derive one or two reported numbers from raw data independently.
   - For any permutation/bootstrap test, check the null actually varies:
     count the distinct values the statistic takes under permutation.
   - **Ground every quoted piece of evidence.** Any LLM stage can emit
     evidence-shaped output while reporting success: quotes stitched across
     source boundaries, paraphrase dressed as verbatim, notes describing
     edits never made. Reading the artifact and judging plausibility does not
     catch this — grep each evidence string against the source it cites and
     report the failure count. An unverified quote field is missing data,
     not evidence.

4. **Report with verdict and dispositions.** Use this format:

   ```
   VERDICT: READY | NOT READY
   ## Blockers (would fabricate or destroy a headline; fix before spend)
   B1. <title>
       Mechanism: <how the artifact produces the number, concretely>
       Direction: manufactures false positive | false null | either
       Evidence: <file:line / the case you ran>
       Fix: <smallest change that rules it out>
       Verify: <how to prove the fix worked>
   ## Majors (biases a secondary readout or weakens a claim)
   ## Minors / notes
   ## Checks: executed vs read-only
   <each step-3 verification: "executed" with the command/case and its result,
   or "read-only" — a finding that rests on reading alone must say so>
   ## Not a certificate
   <which manufacture routes this pass could NOT check — this review
   reliably catches mechanical fabrication routes and is weakest against
   framing-level traps the designer also believes; name the specific claim
   wording that still needs a construct-level human read>
   ```

   Severity is set by *what the flaw does to the conclusions*, not by how
   subtle the code change is. A one-line filter that only prunes one arm is
   a blocker; an ugly function that computes the right number is a note.
   The "Not a certificate" section belongs inside a report you actually
   emitted; never attach it as a standalone disclaimer to a non-review task.
   The executed-vs-read-only ledger exists because a read-only pass that
   presents like an executed one is this skill's own evidence-shaped-object
   problem, applied to itself.

5. **Expect your findings to be verified.** State each finding so it can be
   checked against data ("58/209 sessions predate the cut"), not as vibes
   ("the split seems leaky"). Reviews that can't be adjudicated get argued
   with instead of fixed.

## The manufacture catalog

Failure modes below were each caught in real reviews of real studies; the
one-line examples are genuine. Check every readout against every family.

**1. Leakage and contamination**
- Test data present in training/mining/calibration inputs; information from
  the future of a point used to score that point. *(A temporal firewall was
  computed but never enforced downstream: 28% of test points predated the
  cut, biased pro-pipeline.)*
- Selection rules or hyperparameters tuned on the quantity being reported
  (outcome-conditional choices). *(A detection-context default chosen by
  whichever maximized precision — precision was the dependent variable.)*
- "Blind" materials leaking labels via position, ID scheme, filename, or
  formatting. *(Audit packets with kind-grouped sequential IDs: items 0–19
  all one label.)*

**2. Asymmetry between arms**
- Any filter, prune, cap, retry, or preprocessing step applied to one arm
  and not the other — data cleaning is part of the treatment. *(A null-fire
  prune applied to own-lists only turned p=.101 into a reportable p=.027.)*
- Volume/length/opportunity confounds: one arm gets more chances to score.
  *(A registered count-based primary rewarded the arm that simply fired
  more; the amended volume-immune primary came back null.)*
- Context or prompt differences that help one arm. *(Showing the detector
  the user's request text helps the arm whose rules mention that user's
  habitual requests.)*
- Arms generated by different processes and then labeled as if comparable
  ("expert baseline" that is actually another LLM prompt).

**3. Degenerate statistics**
- Permutation/bootstrap nulls that cannot vary. *(Zero mixed-label users in
  a cell meant all 1,000 permutations reproduced the observed data exactly —
  a guaranteed, publishable-looking null.)*
- Denominators that make the metric true by construction; ratios whose
  numerator and denominator share the untrusted quantity. *(A stability
  Jaccard computed over unvalidated matcher output on both sides read .82;
  the honest value was .43 — below the registered kill threshold.)*
- Effects carried entirely by a few units: require drop-top-k, not just
  leave-one-out — actually run the check and report whether the effect
  survives, even when it does. Cluster errors at the unit where treatment
  varies (users, not events).
- Underpowered cells reported as substantive nulls without a minimum
  detectable effect.

**4. Lying instruments**
- Any LLM stage can fabricate evidence-shaped output while reporting
  success: planted test cases with notes describing edits never made
  *(11/63 plants were no-ops with fabricated sabotage notes)*, quotes
  stitched across source boundaries or paraphrases dressed as verbatim
  *(1 of 87 citations invented in an otherwise-grounded profile)*.
- Instruments that have never been fed a case they must catch. *(A code
  sandbox erroring on 100% of 159 samples — every failure recorded as data —
  because no known-good snippet had ever been run through it.)*
- Refusals, timeouts, and empty payloads recorded as zeros/clean negatives
  instead of missing data — deadly when refusal rates differ by arm.
- Judges validated only by agreeing with themselves; check against a dumb
  baseline. *(A blind-judge "match" score of 92.6% was reproduced by a
  word-overlap matcher — the judge was measuring topic, not the construct.)*

**5. Interpretation traps** (the design can be clean and the claim still
manufactured)
- The stated claim is broader than the tested contrast; the headline wording
  smuggles in a comparison nobody ran.
- A control that nets out the very signal it's supposed to isolate (e.g.
  subtracting a baseline that contains the effect).
- Composite results whose components are individually reported but jointly
  contradictory — check the conjunction, not just each number.
- Measurement instruments that destroy the signal upstream. *(A text
  normalizer stripped proper nouns before a stratum that measured
  content-specificity — erasing exactly what it was built to detect.)*

## Discipline notes

- If the same flaw family was registered before (a prior review, a listed
  confound), check it *by its registered name first* — repeat offenses at
  registered flaws are the most common blocker in practice.
- After fixes land, re-verify each blocker with the "Verify" step you
  specified — a disposition without verification is a promise, not a fix.
