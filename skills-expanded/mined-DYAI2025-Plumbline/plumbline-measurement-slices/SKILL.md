---
name: plumbline-measurement-slices
description: Commands and hard-won honesty rules for Plumbline measurement, benchmark, council A/B and Council-GUI slices. Load before running the metrics harness (emit_run, process_health, council_review_scorer, arm_a_review_runner, council_measurement_run, council_free_diversity_probe), before the Council GUI composition root, or before publishing any benchmark/catch-rate claim.
---

# Measurement, benchmark and Council-GUI slices

Migrated out of the always-loaded root `CLAUDE.md` on 2026-07-31 so it loads only for measurement/benchmark/GUI work. Same rules, same authority.

## Commands

```bash
# Benchmark + measurement harness (config/claude/metrics/ → metrics/):
python3 config/claude/metrics/emit_run.py --corpus-id <id> --mode <core|full> \
  --metrics '{...}' --gate-outcomes '{...}' --human-overrides 0   # append a run to runs.jsonl
python3 config/claude/metrics/process_health.py                   # SPC + drift attribution
python3 config/claude/metrics/challenge_token_oracle.py            # deterministic catch oracle
python3 config/claude/metrics/council_review_scorer.py             # catch / cry-wolf scorer
python3 config/claude/metrics/arm_a_review_runner.py               # single-model arm (Arm A)
python3 config/claude/metrics/council_measurement_run.py           # A/B council measurement
python3 config/claude/metrics/council_free_diversity_probe.py       # free-tier probe (EXP-009)

# Council GUI (Slice 4) — the real composition root; fails LOUD on a missing precondition:
config/claude/bin/plumbline-council-gui --self-check   # wiring proof, crosses no boundary
config/claude/bin/plumbline-council-gui                # serve (live needs COUNCIL_INFERENCE_LIVE=1)
```

## Benchmark-claim honesty (learned)

When publishing benchmark results (README/docs), a claim must carry its own scope and **both** anti-Goodhart metrics. The v0.10 n=6 slice showed catch-rate and false-positive-rate can move in *opposite* directions (the DNA was net-positive on Opus but a catch-vs-cry-wolf trade-off on sub-Opus). So: never headline catch-rate alone ("DNA halves escapes") without the cry-wolf number beside it; keep `n=`, task count, and model scope visible; "strictly better" is a claim that needs *both* metrics to support it. Any cost-optimization lever (M7) is promoted only when it holds catch **and** does not raise cry-wolf — gated on **BOTH**.

## Measurement-run honesty (learned — council-measurement-run / Slice 3b, 2026-06-20)

Each rule is from a real incident in the Slice-3b build, caught by the defense-in-depth gates.

- **An A/B comparison measurement must feed BOTH arms through the IDENTICAL instrument — same prompt protocol, same parser, same scorer.** Slice 3b's first design measured Arm A (Claude) on a structured flag protocol (near-lossless JSON parse) while Arm B (the council) returned free-text prose that a separate, lossy, one-arm parser converted to flags — and `parse_flag_set` can't parse prose at all, so the council would have scored structurally zero. The spec-auditor flagged this as the #1 BLOCKER: a parser that turns one arm's output into the scored form IS part of the instrument, and it touched only one arm → an asymmetric, biased, uninterpretable comparison. The fix is symmetric: prompt BOTH arms in the same structured protocol (appended to the subject) and parse both with the same parser; a non-protocol output is the same classified failure for both. When you build any A-vs-B measurement, prove the extraction/scoring path is byte-identical for both arms before trusting the numbers.
- **At tiny n, `demonstrated`/`refuted` are definitionally out of reach — frame the pilot as underpowered and never launder a lucky split.** The n=2 pilot's cross-task variance is unestimable, so no catch-delta lies "outside the noise band." The honest outcome vocabulary at n=2 is `underpowered` / `tradeoff-signal-to-investigate` only; the real risk is not underpowered-as-refuted but a lucky 2/2-vs-0/2 split sold as `demonstrated`. Pre-register that `demonstrated`/`refuted` require the powered run, make `underpowered` a distinct reachable outcome (survivors-below-floor OR delta-below-MDE), and treat the pilot's value as the cost/flakiness ESTIMATE, not a verdict. (Our pilot returned `underpowered` with 100% free-tier Arm-B attrition — the actionable finding was "free tier is unusable here; the powered run needs paid models," exactly what a pilot is for.)
- **Don't mis-apply a test invariant to a consumer that legitimately needs the dependency — fix the test's scope, don't obfuscate to pass it.** An `assert_no_code_token '_real_transport|urllib'` check was correct for the import-pure 3a scorer, but wrong for the 3b orchestrator, which legitimately consumes `council_inference._real_transport` for the live Arm-A boundary. The coder satisfied the prohibition with a `getattr(council_inference, "_"+"real"+...)` dodge so the literal wasn't a code token — test-gaming of the same family as the Slice-3a `_preview_safe` hack, making the source less readable to pass a contract that should not apply. The fix: relax the test to the real invariant ("defines no transport, imports no http") so a plain reference is allowed, then reference the dependency plainly. A test that forces obfuscation is mis-scoped — repair the test (tester), never game it (coder).

## Measurement-instrument + free-tier hygiene (learned — free-diversity-probe / EXP-009, 2026-06-20)

Each rule is from a real incident running the no-budget free reframe of the council measurement.

- **A measurement instrument that pins itself byte-unchanged cannot be reconfigured for a new experiment — build a SEPARATE harness that reuses its primitives read-only.** The 3b council-measurement orchestrator's own contract (`test_council_measurement_run.sh`) asserts `git diff --quiet -- council_presets.py` (+ the other instrument files) — the frozen-instrument invariant (REQ-MR-009). So repointing the council at chosen models by editing `FREE_MODEL_FAMILY_PREFERENCE`/the preset roster would have reddened run_all. The right move for a new experiment (EXP-009) was a NEW harness (`council_free_diversity_probe.py`) that IMPORTS the vetted primitives (`run_arm_a`, `score_flag_set`, `classify_outcome`) read-only and adds only the new dispatch loop — the frozen instrument stays byte-unchanged. When you need to vary what a frozen instrument measures, wrap it, never edit it.
- **A saturated corpus (baseline already scores 100%) cannot show the treatment's advantage — a diversity/quality corpus needs tasks the baseline MISSES.** EXP-009's free council showed catch-delta 0 — but only because both the single-model baseline AND the council caught 100% on the n=2 corpus (a ceiling). With no headroom, the only thing the comparison can surface is a cry-wolf difference (here the council added +0.25 cry-wolf — the "more reviewers → more noise" hint). Before a powered A/B over a corpus, verify the baseline does NOT already ace it; otherwise you are measuring noise, not the lever. Headroom (tasks a single model fails) is a corpus-design precondition, not an afterthought.
- **Free-tier model reachability is intermittent — probe it IMMEDIATELY before a live run and pin the baseline to a reachable model.** Two reachability probes minutes apart returned 2/5 then 5/8 reachable (429s shift minute-to-minute; they are often daily caps, not transient). The measurement's paired-exclusion drops a subject if EITHER arm's model 429s, so an unreachable baseline → 100% attrition regardless of the council (the pilot's outcome). So: probe the exact model set just before the run, set the baseline to a currently-reachable model, and treat reachability luck itself as a disclosed confound (the pilot got 100% attrition; EXP-009 got 0% — same corpus, days apart).
