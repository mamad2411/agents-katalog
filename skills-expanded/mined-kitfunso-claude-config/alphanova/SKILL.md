---
name: alphanova
description: Playbook for the AlphaNova quant competition. Use for AlphaNova repo work, Predictor submissions, or the overfitting gate.
---

# AlphaNova playbook

Cycle 1 cost 39 research rounds and 34 uploads to reach one positive score at
rank 19. Almost all of that was learning the rules of the game, not building
models. The rules are written down here. Cycle 2 started at round 39 and still
repeated round 1 on a different construct (section 11). The method block below
is the fix. Read it before anything else.

**Repo:** `~/alphanova`. Read `comp6_scientist_release/COMPETITION.md`
and the repo `CLAUDE.md` before writing model code. Full ledger:
`research/SCOREBOARD.md` (every round, every retraction). **Every number in this
skill, with its source and the experiments behind it, is in `evidence.md` next to
this file.** Read that when you need detail; this file carries the decisions.

## The method: read this first

Sections 0-11 are the reference. They say how to pass the gate and what is
dead. They do not find alpha. This block is the method. Cycle 2 ran without it
and repeated cycle 1 (section 11).

1. **Stage 0, before the first run.** Load `/quant-ml-protocol`. Open
   `docs/EXPERIMENT-PROTOCOL.md` in the repo. Add the cycle's registry entry and
   read the trial-ledger count (N = 116 files, 66 uploads at the end of cycle 2).
   A run not declared there is a diagnostic, never evidence.
2. **The yardstick, quoted next to every number.** n_independent ~207 (24,800
   scored rows / 120 h). SE(IC) ~0.015, so the detectable IC floor is ~0.03,
   above the cycle-1 board leader's +0.028. Sharpe noise bar 0.0127 on the
   7-period confirm window; the pooled 31-period bar is registry item P0. The
   expected maximum of N=116 noise draws is ~3.1 SE. Every local best so far
   sits inside that ceiling. A local number inside the bar never justifies the
   next run of the same kind.
3. **The upload bar (Keith, "B", Sep-2).** Local net Sharpe >= 0.02 on all 31
   periods (`runner.py --full --gauge-fix`), one look, pre-registered, above the
   process-null p95 (registry item P1), union-pot corr <= 0.5 to every admitted
   signal including ours (`research/50_c2pot_corr.py`). Below the bar = no slot.
   The one exception is the declared anchor, one per cycle. Unspent slots cost
   nothing. A sub-bar admission costs a pot ticket for the season (F5).
4. **The stop rule.** A construct family gets the anchor plus two
   single-variable probes. No third slot unless one scores above +0.0135 on the
   server (the cycle-1 Q3 cutoff, the protocol's tripwire). Three local runs
   inside the best run's interval, or two rounds with no new best, = stop the
   construct and write the self-audit (quant-ml-protocol steering bank, stage 5:
   "What else is wrong with what you did?") before the next run. Cycle 2 ran 47 runner shell calls (10 loops, 134 run logs) and 30 of 32
   uploads on one ridge.
5. **Hunt constructs and inputs, not parameters.** The unexplored space is the
   hunt map in section 8 (inventory of `research/families/`, Sep-2). Each
   candidate gets a registry id, a mechanism, a kill criterion, and one look.
6. **Delegate the width.** One Sonnet sub-agent per registry entry, launched in
   one batch. Brief: the construct spec, the hard rules (section 7), the three
   gate commands, the bar, the ledger line format. It returns the family file,
   the runner line, invariants 6/6, the crash screen, the union-pot max corr.
   The main thread judges against the bar and writes the GATE line. Never two
   agents on one file. The main thread does not hand-sweep. Zero skills loaded
   after 40 tool calls is a defect, not a style.
7. **Sign-off before any slot.** Surface to Keith: the bar restated, every metric
   with its yardstick, the trial count, the NOT-DONE table, the caution flags.
   Wait for the sign-off. Then the GATE line in `research/SCOREBOARD.md`, then
   the upload, then verify the counter moved.

---

## 0. The data, in ten lines

Phase 1 solved this. Do not re-derive it.

- **Target** ≈ cross-sectionally z-scored **120-hour forward sum** of the
  proprietary returns, clipped ±5. Horizon scan peaks exactly at h=120 (IC
  0.94-0.97). So: forecasting 5-day relative performance, re-estimated hourly.
- **Six features.** F1-F4 are ONE slow factor (pairwise corr 0.96-0.985, autocorr
  ~0.97). F5 is fast, F6 very slow and tiny. **All linear ICs are ~0** by design;
  textbook signals score zero here.
- **The factor is the poisoned dimension.** Every ablation that added factor
  levels made the model worse.
- **Rotation.** Each period is independently rotated in asset space. Inner
  products survive it; **ranks and absolute values do not**. A single-frame IC is
  partly frame luck (the same construct read +0.0115, -0.000 and +0.0075 in three
  frames). Only `runner.py --full` walking across periods is honest.
- **The static-tilt trap.** A causal expanding mean of the target's own past rows
  scores IC +0.074, the largest number in the data, and it is worthless: a static
  tilt survives label shuffling, so the gate's null contains all of it. Always
  de-tilt. The k>1 discovery in §2 is the inversion of this trap, not an exception.
- **Panel rules:** returns are proprietary (never reconstruct from outside data);
  tickers are not stable across periods; period files are cumulative (never
  concatenate); leading exact-zero rows are warm-up (drop them in `train()`).

---

## 1. The five facts that decide everything

**F1. The gate is degenerate for hand-written rules.** The server retrains your
model on shuffled labels and rejects it if the shuffled model still scores well.
If `train()` is a no-op, the shuffled model *is* your signal, so it scores
identically, so the test collapses to "reject if it performs". Proof: `mfb_240`
(admitted) and `mfb_inverse` (rejected) are the same file with one sign flipped.
Ten hand-written rules died this way in cycle 1. **Never submit a model-free
rule. Ever.**

**F2. No local number ranks candidates, except the rank of concentration.**
Cycle 1 wrote this as "within-construct sweeps transfer". Cycle 2 falsified the
general form.

- *Across constructs*, the runner lies. `corr(local net Sharpe, official) =
  -0.558`, measured across different families. `ml_apex` beat `ml_overtilt` 2-4x
  on every local metric and scored worse, IC flipping sign (+0.0243 runner to
  -0.0039 server). Never rank two different constructs by a runner number.
- *Within one construct*, the k sweep ordered k = 3, 7, 15, 25 correctly on all
  four server points (-0.0050, -0.0019, -0.0003, **+0.0003**). That is four
  points on one axis. On cycle 2's fit-row axes the local order was
  non-evidence: `win` read -0.0091 locally and scored best (+0.0049); local IC
  is anti-correlated with server IC inside one construct (-0.78, section 3).
- Every delta in the section 2 table (0.0003 to 0.0053) is inside the noise bar
  0.0127 (section 6). Rank order on four points is not magnitude evidence.

So: a single-variable sweep is a local diagnostic on a registered construct. It
is never evidence for a slot; the bar is (method, item 3). What transfers is the
RANK of local gauge-fixed concentration (+0.96) and of local ic_std. Nothing
local measures the sign of server IC. Every model fitted *across* heterogeneous
signals in cycle 1 failed to rank *within* one family, including the field
regression in F3.

**F3. The scoring function is known.** Regression over 64 scored signals from
the leaderboard API (`research/33_leaderboard_study.py`), leave-one-out R² 0.237:

```
Sharpe  ≈  0.58·IC  +  0.024·concentration  −  0.013·IC_std  −  0.011
```

`concentration` (= ‖mean of the gauge-fixed unit vectors‖, i.e. directional
stability over time) correlates +0.477 with official Sharpe, the strongest single
correlate on the board. `compression_loss` is exactly `IC·(1 − 1/concentration)`
and carries no extra information.

**Use it to size the target, never to rank two variants of one signal.** It is
fitted across 64 different constructs, so it inherits the F2 problem: it predicts
`otv_k3` (-0.0036) above `otv_k25` (-0.0039) and the server returned -0.0050 and
+0.0003. Its IC coefficient is too large and its concentration coefficient too
small for a single family.

**F4. Prize needs a POSITIVE Sharpe, then top-3 rank inside the quality set.**
Cycle-2 rules (2026-09-01) dropped "statistically significant": quality-set
step 1 is now any positive Sharpe, then ranked, then `|corr| ≤ 0.5` against
every higher-ranked signal and the legacy pot (the fund's background signals no
longer occupy space). Under the new rule cycle 1 closed with Q=36 (pot
saturated, top 3 paid 60/25/15, Q3 cutoff +0.0135) and `otv_k25` was Q36, the
last one in. Negative Sharpe cannot win anything, at any rank. **Ten free
novelty checks per cycle** report legacy-pot novelty before a slot is spent;
use one on every candidate that is kin to something already admitted.

**F5. Everything admitted in cycle 1 is burned.** At cycle close every entry
that passed entry checks moves into the season legacy pot and keeps occupying
its neighbourhood for the rest of the season. All 20 of our admitted signals are
in there. Worse: all over-de-tilted signals correlate 0.82-0.99 with each other
*regardless of features* (`research/36_candidate_corr.py`; `alt_feat` shares no
inputs with `ml_apex` and still correlates 0.954). **The whole over-de-tilt
family is one ticket and `otv_k25` is now the holder** (highest-ranked of the
seven, so the greedy selection keeps it and prunes the rest behind it). Cycle 2
needs a different mechanism, not different inputs.

---

## 2. Where cycle 1 finished, and what the k-curve showed

Best signal we own: **`otv_k25`**, server Sharpe **+0.0003**, rank 19. The only
positive score of the campaign. It is `ml_overtilt` with one number changed:
`TILT_K` 7 to 25.

The four single-variable probes that produced it, all at span 96 on f1's model
except where noted:

| file | k | spans | capacity | Sharpe | IC | IC_std | conc |
|---|---|---|---|---|---|---|---|
| **otv_k25** | 25 | 96 | f1 | **+0.0003** | +0.0034 | 0.1823 | 0.3110 |
| otv_k15 | 15 | 96 | f1 | -0.0003 | +0.0038 | 0.1852 | 0.3078 |
| otv_minimal | 7 | 96 | **minimal** | -0.0012 | **+0.0065** | 0.1953 | 0.2963 |
| ml_overtilt | 7 | 96 | f1 | -0.0019 | +0.0049 | 0.1941 | 0.2960 |
| otv_s2k7 | 7 | 240/480 | f1 | -0.0023 | +0.0026 | 0.1923 | 0.2992 |
| ml_apex | 25 | 240/480 | f1 | -0.0031 | -0.0039 | 0.1794 | 0.3157 |
| otv_k3 | 3 | 96 | f1 | -0.0050 | +0.0067 | 0.2102 | 0.2620 |

Three readings, all load-bearing:

1. **Sharpe is monotone in k. IC falls while it does** (+0.0067 down to +0.0034).
   What rises is stability: concentration 0.2620 to 0.3110, IC_std 0.2102 down to
   0.1823. **k trades IC for directional stability, and the trade pays.** Do not
   treat IC as the thing to maximise.
2. **The multi-timescale blend is what killed `ml_apex`, not the high k.** At
   fixed k=7, moving to spans 240/480 costs 0.0004; at k=25 it costs 0.0034. Slow
   span blending is the poison, and it is worse the higher k goes.
3. **Capacity down worked, and stacks with nothing yet.** `otv_minimal` posts the
   highest IC at its output stage (+0.0065 vs +0.0049) purely from depth 2 /
   3 leaves / 25 rounds. It was never tried at k=25.

**Do not build `otv_minimal` at k=25.** Checked Sep-1: local pooled corr +0.989
with `otv_k25`, and the server novelty check said NOT NOVEL (no slot spent). Any
`sig - k*tilt` build with k>1 is a copy of the pot occupant regardless of inputs
or capacity. The over-de-tilt family is closed for season 1.

Board leaders for scale: IC +0.0281 at conc 0.337, and IC +0.0256 at conc 0.397.
Our +0.0003 made the quality set under the cycle-2 rule (Q36 of 36) but the
paid cutoff was +0.0135 (F4).

---

## 3. Kill list: measured dead, do not re-run

Each line cost real rounds in cycle 1. Re-testing any of them needs a new
argument, written down first.

**Constructions**
- Hand-written / model-free rules of any kind. See F1. 10/10 rejected when good.
- Re-using over-de-tilt (`sig − k·tilt`, k>1) or anything correlating > 0.5 with
  `otv_k25`. Burned by F5. The *mechanism* is still worth carrying; the construct
  is not.
- Ensembling across model families: rank-averaging 5 families gave IC +0.0051 at
  concentration **0.0843**, below its own components' 0.21. Averaging did not buy
  stability.
- Label engineering (rank-smoothed target): identical model, only the label
  changed, runner IC +0.0058 → **-0.0092**. It hurt.
- Learning-to-rank (LightGBM `lambdarank`): IC **-0.0140**. NDCG is top-weighted,
  IC weights the whole cross-section uniformly. Wrong objective by construction.
- CatBoost: lost to LightGBM; ordered boosting was the worst variant tried.
- Multi-timescale output blending at unit de-tilt: rejected by the gate. At k=25
  it is admitted but strictly worse than a single span (§2).
- Turnover engineering (step-hold, banding, tranching, band-pass, longer holds).
  Halving turnover made the score **worse** (-0.0073 → -0.0103, IC -0.0131 →
  -0.0237). At step 240 the whole bill is ~0.0011, so a zero-alpha signal beats
  our best. **Costs were never the binding constraint.**
- **Hyperparameter optimisation as practised in cycle 1.** 8 families × 25 Optuna
  trials returned selection ICs of +0.073 to +0.100 for *every* family, including
  KNN and ElasticNet matching gradient boosting. With ~120h autocorrelation the
  se of a period's mean IC is ≈0.035, so the expected max of 25 noise draws is
  ≈+0.07: it was fitting noise, and the numbers said so before the confirm window
  did. Confirm result: mean selection IC +0.0876 → **mean confirm IC -0.0206,
  zero of eight positive**, `corr(selection, confirm) = -0.582`. It ranked the
  families *inversely*. It also pushed every family toward more capacity, which
  server data later showed is the wrong direction. **If you tune, tune capacity
  downward and score on a window the tuner never saw.**

**Diagnostics and axes**
- Hour-of-day / day-of-week: IC spread 0.0064 vs per-bucket se 0.0027. Dead.
- Confidence-based book sizing: IC autocorrelation is +0.899 at lag 1 but
  **-0.002 at lag 120**, and 120h is the rebalance horizon. The lag-1 number is
  mechanical (EWM smoothing), not skill persistence. Nothing to size on.
- Feature engineering as a route to decorrelation: F5 shows it does not work.
- Local shuffle rehearsal as a ranking or blocking device: it failed in both
  directions (best-margin `zoo_xgb` rejected, worst-margin `zoo_hgb` admitted;
  it failed `ml_overtilt`, which the server then admitted at our best rank).
  Keep it only as a crash screen. Never let it block an upload.
- The **gate/cost trap map** (round 21): rehearsal output claiming only one
  output configuration can clear the gate, and that profitable and admissible are
  disjoint. The server contradicted it by admitting the most persistence-leaning
  signal we ever built. Non-evidence.
- Runner `city novelty` and `concentration` as server-equivalent LEVELS. The
  runner computes novelty against a shipped city database the organiser has said
  to ignore. Runner concentration is construct-dependent in scale: `f1` read
  0.0758 local vs 0.2265 server, `ml_overtilt` 0.3153 vs 0.2960. No fixed
  conversion exists. But it transfers in RANK: calibration on all 20 cycle-1
  admitted signals (`research/41_local_vs_server.py`, round 40b) gave
  corr(local conc, server conc) +0.96 across trained models and +0.88 inside
  the over-de-tilt family, and local conc is the strongest local correlate of
  server Sharpe (+0.88 / +0.90). Local `ic_std` transfers the same way
  (negative for Sharpe). **Local IC does not transfer at all: -0.39 against
  server IC across trained models, -0.78 inside one construct.** The common
  metric to build against is rank of local concentration and rank of local
  ic_std, never local IC. Nothing local measures the sign of server IC.
- **Any hand-built proxy for a server metric.** A raw-position stability proxy
  read 0.114 where the real gauge-fixed concentration was 0.0709, and it was on
  the record as a pre-registered bar. Concentration lives in the rotating target
  frame; nothing computed in raw position space tracks it.
- The dashboard's **validation score**. It disagrees with the test score, and the
  test score is what ranks you (`mid_fac_blend`: validation +0.0373, test
  -0.0073). A high validation number is not good news.
- A custom evaluation harness. One was built in cycle 1, disagreed with
  `runner.py` twice (6x underestimate, then a sign flip), and every number it
  produced had to be retracted. **`runner.py --full --gauge-fix` is the only
  local harness. It is what the server runs.**

**Dead theories about the gate** (six, all pattern-fits to fewer than 15
verdicts): temporal-op syntax, signal speed, fund-city correlation, compression
loss, a strength ceiling, in-sample Sharpe. The theory that survived came from a
*designed* experiment: one file, one sign flipped, opposite verdicts. Design the
discriminator; do not curve-fit the verdict list.

---

## 4. What actually works

Three ingredients, each earned from a server verdict:

1. **A trained model.** Shuffling labels genuinely changes it, so the null is
   proper and the gate admits it while it performs. Every trained model we sent
   was admitted except one; 5 of 6 carried positive server IC.
2. **Small capacity.** One of only two monotone relationships ever found in
   server data (the other is the k-curve in §2):

   | model | capacity | server IC |
   |---|---|---|
   | f1_interactions | depth 3, 7 leaves, 40 rounds | **+0.0071** |
   | zoo_lgb | depth 6, 12 leaves, 95 rounds | +0.0047 |
   | zoo_hgb | depth 7, 193 iters | +0.0034 |
   | zoo_et | 91 trees, depth 4 | +0.0018 |
   | zoo_rf | 145 trees, depth 5 | +0.0004 |
   | zoo_mlp | 64x32x16 | -0.0071 |

   **Server IC falls as capacity rises.** Optuna maximised selection-window IC
   and pushed every family bigger; every bigger model scored worse. If you tune,
   tune *downward*.
3. **Causal de-tilt of the output, and the coefficient is the biggest single
   lever found all cycle.** The persistent cross-sectional component is
   anti-predictive: keep it (k=0) and IC goes negative. Removing *more* than one
   unit adds it back negated, which is predictive and persistent at once. Server
   Sharpe rises monotonically from k=3 to k=25 and it moved our best score by
   0.0053, more than every feature, model-class and cost experiment combined.
   The construct itself is burned for season 1 (F5), but the *mechanism* -
   deliberately amplifying an anti-predictive persistent component - is the one
   idea worth carrying into a new construct.

Structural skeleton: `baseline_predictor.py` in this skill directory (a copy of
`research/families/ml_overtilt.py` with the burned k stripped back to 1). Reuse
the *shape* (warm-up drop, 120-row embargo, csrank helper, EWM, de-tilt,
de-mean), not the signal.

---

## 5. The opening move for a new cycle

Do these before writing any model code. None of it costs a submission slot.

0. **STOP. Load `/quant-ml-protocol` and open `docs/EXPERIMENT-PROTOCOL.md`.**
   No run, no slot, no sweep before the protocol file has the cycle's registry
   entry and the trial-ledger count. Then list the skills and agents that apply
   and delegate the construct hunt to parallel sub-agents. Cycle 2 skipped this
   step and repeated cycle 1 exactly (section 11). The method block at the top
   is the plan; sections 1-10 are the reference.

1. **Confirm the cycle's rules page.** Dates, slot count, pot. Windows run
   boundary to boundary on the 1st and 15th UTC.
2. **Pull the leaderboard and the city map from the API**, re-fit the field
   regression (`research/33_leaderboard_study.py`). The coefficients move as the
   board fills. This is free information and in cycle 1 it sat unused for 23
   rounds while two wrong theories drove the work.
3. **Re-extract the data** if the cycle ships new periods. Data is gitignored;
   source is `Downloads/files.zip`. Period files are cumulative, never
   concatenate them.
4. **Re-run `baseline_predictor.py` through `runner.py --full --gauge-fix`** to
   confirm the harness and data are wired. Expect a roughly-zero Sharpe. That is
   the smoke test, not a result.
5. **Write the cycle's pre-registration into `research/SCOREBOARD.md`** before
   the first upload: what mechanism, what the bar is, what each verdict will
   discriminate.

### Then spend slots only against the bar

Cycle 1 spent 14 slots learning the rules. Cycle 2 spent 20 on parameter
variants of one construct. Neither found alpha. The slot plan is the method
block, items 3 and 4:

| Slots | Purpose |
|---|---|
| 1 | **Anchor.** The declared construct with the largest server novelty angle. Free novelty check first. The one sub-bar exception per cycle. |
| 0-19 | **Bar-clearing constructs only.** Registry id, one look, above the process-null p95, union-pot corr <= 0.5 to every admitted signal, GATE line on record. |
| <= 2 per family | **Single-variable probes** on a family that has an anchor. No third slot unless one scored above +0.0135 on the server. |

Unspent slots are not a loss; they cost nothing. A sub-bar admission is a loss:
it is a permanent pot ticket (F5), and cycle 2's 20 admissions are now one
ticket (section 11). Two rules stay: never upload two variables changed at once,
and never upload a signal correlating >0.5 with one already admitted.

---

## 6. Slot economy and measurement discipline

- 20 slots per cycle. **Rejections refund their slot** and do not enter the
  legacy pot. Unused slots expire worthless at cycle close.
- **10 free novelty checks per cycle** (added cycle 2). A check reports novelty
  against the legacy pot without spending a slot; a novel signal auto-proceeds
  to scoring. Spend one before the anchor and before any kin of an admitted
  signal. They expire with the cycle too.
- The wrong moves, in order: a sub-bar admission (permanent pot ticket), a
  duplicate of an admitted signal (the same), then an unspent slot (costs only
  the option). Cycle 2 ran this order backwards and spent 20 slots on one ticket.
- **Every upload is an experiment with a written prediction.** Before uploading,
  record in the ledger what each possible verdict would prove. An upload that
  cannot change what you do next is a wasted slot.
- **The prediction starts with a GATE line, before the score line:** "gate:
  admitted | rejected, because <rule>". Rules on record: model-free rules are
  rejected when they perform (F1); slow, persistent output at k <= 1 is rejected
  (cycle 1 round 5b gate law, round 32b `ml_multiscale`, cycle 2 `ridge_slow`:
  EWM-480 inputs, span 1920, k=1). A gate line that says "rejected" means the
  file does not go up. Cycle 2 spent an onboard on a file whose own ledger entry
  carried that prediction as branch (c) instead of as the headline.
- Change one variable at a time. Cycle 1's `ml_apex` moved k and the spans
  together, so its failure was unattributable and cost four follow-up probes to
  decompose.
- Verdict classes seen: `OK`, `Overfitted submission`, `Failed to run`,
  `Processing` (the path admitted signals take; rejections flip straight to
  Overfitted).
- Uploads are manual through the browser (`alphanova.tech`, account `cookedjay`).
  **Verify the counter moved.** Matching the file picker's filename label is not
  proof the upload landed; that produced a false "submitted" claim in cycle 1.

**Measurement discipline.** Adopted mid-cycle, never falsified, keep all of it.

- **The noise bar: 0.0127.** Block bootstrap (120-row blocks, 2000 resamples) of
  the confirm-window net Sharpe. **Any local improvement under ~0.013 is luck.**
  Most of cycle 1's "wins" were inside it.
- **Plateau, not argmax.** Take a config whose grid neighbours are also good. A
  lone spike is a discretisation artifact: an 800-row evaluation block fits only
  3-4 rebalances, so step-aligned grids are spiky by construction.
- **Two windows, counted looks.** Selection = periods 001-024, confirm = 025-031.
  One confirm look per decision, budgeted in advance. By round 7 the confirm
  window had had 12+ looks and was spent; after that only server history was clean.
- **Multiplicity honesty.** Carry a "Tried" count per family in the ledger so a
  best-of-13 is never written up as a single measurement.
- **Overlap-adjusted significance.** The 120h-overlapping label means naive
  t-stats divide by ~sqrt(120). At 120-240h holds the effective sample is ~100-200
  observations, so mean IC -0.013 is only t ≈ -0.87. Correlated signals are one
  observation, not six.
- **Pre-register.** Candidate, bars, and what each verdict proves, written before
  the run. It is what made cycle 1's failed predictions legible instead of
  rationalisable.

---

## 7. Hard rules for the submission file

Server-side auto-rejection. Check every one before upload.

- No `assert` on row order, derived values, or the target (cycle-2 rule). The
  gate retrains on shuffled labels; a crashed retrain fails the whole run.
  `predict()` must be pure inference and may see rows overlapping `train()`.
  Screen for it: `.venv/Scripts/python research/40_crash_screen.py <file>`
  trains on real and on row-permuted labels and checks the output. Crash
  screen only; it says nothing about the gate verdict.
- One `.py` file. All logic inside the single `Predictor` subclass. Module-level
  imports only. No top-level helpers, no global state.
- `predict()` output cross-sectionally de-meaned: `p.sub(p.mean(axis=1), axis=0)`.
- No future-looking operations anywhere. No `shift(-n)`, no `bfill`, no
  `center=True` rolling windows, never touch the target inside `predict()`.
  Only `.shift(1)` is sanctioned.
- CPU only. `train()` < 4 min, `predict()` < 60 s, RAM < 8 GB. Profile
  `predict()` for instance-based models: `zoo_knn` returned "Failed to run" on
  the 60 s budget.
- Never modify anything in `comp6_scientist_release/`.
- Extra deps via a PEP 723 header. Pre-installed: numpy, pandas, scikit-learn,
  xgboost, lightgbm, pyarrow.
- Ticker identity is not stable across periods. Cross-sectional structure only.
- Embargo the last 120 rows of the training tail. The label is a 120h forward
  sum, so the tail leaks.

**Mandatory pre-upload gates:**
```
python research/11_gate_guard.py <file>        # static legality, must say LEGAL
python -m pytest research/tests/test_invariants.py -k <family>   # 6/6
python runner.py <file> --full --gauge-fix     # from comp6_scientist_release/
```
The guard caught a banned centred window on a training label in cycle 1. Keep it
in the loop.

---

## 8. The open problem, and the untried mechanisms

**The open problem: no local quantity predicts the server score.** Not across
constructs, and for IC and Sharpe not within one either (F2). Concentration rank
and ic_std rank transfer; nothing local measures the sign of server IC. So the
local instrument is the bar plus the process null (method, items 2-3), and the
server is the only oracle of sign. Design for it: few uploads, each a different
construct, each with a written prediction. Rejections being free makes a wrong
construct cheap. A wrong admission is not free (F5).

**The bar, from the field regression, at IC_std ≈ 0.19:**

| concentration | server IC needed for Sharpe > 0 |
|---|---|
| 0.20 | +0.0150 |
| 0.30 | +0.0109 |
| 0.40 | +0.0068 |

We reach concentration 0.31 and IC +0.0034. Treat the table as a rough target,
not a ranking device (F3): the k-curve cleared zero at an IC the table says is
far too low, because stability was doing work the coefficients understate.

**Explored space (inventory of `research/families/`, 116 files, Sep-2, by
grep; re-read a file before you cite it).** Inputs: F1-F4 ranks, abs-ranks,
averages, negation, the F1-F3 and F3-F4 spreads; F5 and F6 ranks, EWM-then-rank
and rank-then-EWM at spans 240-960, squares; a 480h and a 240h F6 change;
per-feature cross-sectional dispersion and rank x dispersion
(`xsec_ctx_mlp.py`); rotation-covariant unit-norm rows (`f2_covariant.py`).
Models: ridge, Huber, ElasticNet, LightGBM regression / multiclass / lambdarank,
MLP, KNN, RF, ET, HGB, XGBoost, seed-bagged LightGBM (`f1_bag.py`), cross-family
rank ensemble. Output: TILT_K 0-25, output EWM 24-1920, step-hold 120, recency
weights 0.5-8, WINDOW 0.5, tranching, EWM tilt estimator, output csrank. Labels:
de-tilted, rank-smoothed, quintile classes. Training: EMBARGO 120, LOOKBACK
120-960, one global fit per `train()`. Every temporal op is `.ewm()`. Every
normalisation is cross-sectional.

**The hunt map: not found in `research/families/`, ranked by distance from the
pot.** Each item is one registry entry, one sub-agent, one look against the bar.

1. **Per-asset time-series normalisation.** Zero `.rolling(` and zero `groupby`
   calls in 116 files. Every input is a cross-sectional rank. A per-asset
   z-score or percentile against its own history is a different object.
2. **Feature deltas and accelerations at several horizons.** One delta exists
   (F6, 480h). No delta ladder, no second difference on any feature.
3. **F5 volatility or regime measures.** F5 appears only as a rank or an EWM
   rank. No rolling std, no dispersion of F5, no regime flag.
4. **Rolling per-asset autocorrelation or sign-persistence as an input.**
   Measured once as a diagnostic (IC autocorr +0.899 at lag 1), never fed in.
5. **Sign-agreement across F1-F4.** The spreads use magnitude differences; no
   concordance count exists.
6. **Bagging across training windows**, not across seeds (`f1_bag.py` bags
   seeds).
7. **Per-period re-fitting inside one submission.** Every file fits once.
8. **Row-wise gauge normalisation of the output** (cycle-1 item, still untried).
   Concentration is the norm of the mean unit vector; normalising each row
   before the de-mean targets it directly.
9. **Feature-PC neutralisation.** Project the prediction off the first PC of the
   feature panel instead of its own time-mean tilt.
10. **Embargoed early stopping.** An inner purged split chooses `N_ROUNDS`.

Tried since cycle 1 and off the list: seed-bagging (`f1_bag.py`),
classification framing (`f1_cls.py`), recency-weighted training (cycle 2,
`rs_rec_*`, admitted at +0.0039 to +0.0043, inside the noise). A sweep of a
hunt-map item's parameters is a local diagnostic after it clears the bar, not
before.

---

## 9. File map

In this skill directory:

| File | What it is |
|---|---|
| `evidence.md` | The full measured record: data, metrics, every failed lane with numbers, the instruments that lied, the six dead gate theories |
| `baseline_predictor.py` | Structural skeleton to start from, k reset to 1 |

In the repo:

| Path | What it is |
|---|---|
| `comp6_scientist_release/COMPETITION.md` | The law. Gate mechanics at lines ~215-240, legacy pot ~23-38, quality set ~60-92 |
| `comp6_scientist_release/runner.py` | The only trustworthy local harness |
| `comp6_scientist_release/city_tools.py:105` | `concentration` definition |
| `research/SCOREBOARD.md` | Append-only ledger, 39 rounds, every retraction |
| `research/11_gate_guard.py` | Static legality check, mandatory |
| `research/tests/test_invariants.py` | Per-family invariant suite |
| `research/04_shuffle_gate.py` | Shuffle rehearsal. Crash screen only, never a blocker |
| `research/33_leaderboard_study.py` | Field regression over the scored board |
| `research/36_candidate_corr.py` | Correlation matrix, run before spending a slot |
| `research/37_untried_axes.py` | Diagnoses an axis before you build on it |
| `research/40_crash_screen.py` | Trains on real and permuted labels; crash screen before upload, says nothing about the verdict |
| `research/41_local_vs_server.py` | Local-vs-server calibration on the 20 cycle-1 admissions (conc rank +0.96) |
| `research/50_c2pot_corr.py` | Union-pot screen (cycle-1 pot + our cycle-2 admissions); merges subset runs by family |
| `docs/EXPERIMENT-PROTOCOL.md` | Governs every run: sample-size math, the bar, registry P0-P3, NOT-DONE table, tripwire |
| `research/families/rs_s96_win.py` | **Cycle-2 best: +0.0049, rank 1 on day 1.** Pot-blocks every ridge-on-F5/F6 variant |
| `research/families/xsec_ctx_mlp.py` | The only creative input set (rank x dispersion, 22 columns); never uploaded; base of the cycle-3 anchors |
| `research/families/otv_k25.py` | Cycle-1 best: +0.0003, rank 19. Burned by the pot |
| `research/families/otv_minimal.py` | Highest IC at its output stage (+0.0065) via minimal capacity |
| `research/families/f1_interactions.py` | Best raw server IC we ever posted (+0.0071) |
| `research/families/otv_recency.py` | Recency weighting; verdicted in cycle 2 as `rs_rec_*`, inside the noise |
| `docs/plans/2026-08-17-cycle2-design.md` | Mostly stale: its levers 1 and 4 were later falsified |

---

## 10. Why cycle 1 took 39 rounds

Written so it does not repeat. One root cause, six expressions.

**Root cause: we optimised what we could measure instead of measuring what we
were scored on.**

1. We submitted before understanding the gate. Half the uploads were
   hand-written rules. F1 was derivable from `COMPETITION.md` on day 1 without
   spending a single slot.
2. We trusted local metrics for 20 rounds. `corr(local, official) = -0.558` was
   computable after the first four verdicts and was not computed until round 17.
3. We did not read the field until round 23. The leaderboard API hands you 64
   scored signals with IC, concentration, IC_std and Sharpe. One regression gives
   the scoring function, free, on day 1. It falsified two live theories the hour
   it ran.
4. We fitted six theories to the verdict list instead of designing experiments
   against it. Every curve-fit died. The designed one-variable experiment solved
   it in a single upload.
5. We built a second harness alongside the official runner. It disagreed twice
   and every number it produced was retracted.

6. **We theorised where we should have swept.** The campaign's only positive
   score came from four cheap probes that each changed one number, fired on the
   last day. Thirty rounds of theory produced -0.0019; the probes produced
   +0.0003 and corrected a wrong attribution at the same time. A parameter sweep
   against the real scorer beats a model of the real scorer. **Cycle 2 then
   inverted the error: it swept where it should have hunted**, 30 of 32 uploads
   on one construct (section 11). The sweep is a local diagnostic on a
   registered construct. It never plans the slots; the bar does.

**The corresponding habits:** derive the gate before uploading; measure the
local-versus-official correlation as soon as four verdicts exist; fit the field
regression on day 1 and re-fit as the board fills; spend early local runs,
never slots, on a single-variable sweep of the most suspicious parameter; keep
exactly one harness, the official one.

## 11. Cycle 2 record (Sep 1-2, 2026): what worked, what did not

**Outcome.** 32 uploads, 20 admitted, 12 rejected, all 20 slots spent by Sep-2
01:00. Best: `rs_s96_win` +0.0049 (rank 1, the sole Q1 star on day 1, server IC
-0.0001). The cycle-1 Q3 cutoff was +0.0135. Nothing we built is above the noise,
locally or on the server. Full detail: `research/SCOREBOARD.md` lines 1990-2300.

**Worked (server-verified).**
- A trained ridge on two slow inputs (F5, F6 EWM-480 ranks), output EWM span 96,
  unit de-tilt: admitted every time at spans 24-144 and lookbacks 240-480. The
  gate passes it. It scores about zero.
- The fit-row lever: the same ridge fitted on recent rows only (recency weights,
  or the newest half) sat above every plain fit, 7/7 vs 0/13, and moved the score
  from +0.0006 to +0.0049. Still inside the noise bar.
- Local gauge-fixed concentration rank transfers to the server (+0.96). No other
  local number does.
- Pre-registered GATE lines, one variable per file: 13/13 correct on admission by
  the end. The gate is understood; every verdict was attributable.

**Did not work.**
- Local Sharpe and IC as a ranking device, again. Local IC is anti-correlated
  with server IC inside one construct (-0.78); `win` read -0.0091 locally and
  scored best. On fit-row levers the local order is non-evidence.
- Gate-out at k=1: output span 192+, input lookback 960, any nonlinear term of
  the ranked inputs (product, squares), LightGBM on slow inputs, Huber loss. The
  one-input theory was falsified (`f6` admitted).
- Concentration alone does not pay: `rts` had the board-high conc 0.2186 at
  -0.0029.
- Sweeping one construct. 30 of 32 uploads were parameter variants of one ridge.
  All 20 admissions are now ONE pot ticket (0.75-1.0 among themselves) and every
  held build is pot-blocked.
- No new features in cycle 2. Zero. The xsec context set (cycle 1) is the only
  creative input set built, and it was never uploaded.

**Self-audit, written Sep-2.**
- Data: clean. Contemporaneous features, warm-up dropped, 120-row embargo.
- Statistics: the sample-size math was never written. n_indep ~207 gives
  SE(IC) ~0.015, so no achievable IC is locally detectable; the Sharpe bar
  0.0127 was known and every "win" sat inside it. Trial count: 116 family files,
  66 uploads. The local maxima are noise maxima.
- Code: one defect, fixed (`50_c2pot_corr.py` overwrote its table on subset runs).
- Process: no protocol file, no trial ledger, no process null, and the
  quant-ml-protocol skill was not used. Slots went to sweeps of a construct known
  to sit at zero. Fixed Sep-2: `docs/EXPERIMENT-PROTOCOL.md` v1 in the repo.

**Cycle-3 rule (Keith, "B", Sep-2).** No slot below local net Sharpe 0.02 on all
31 periods, one look, pre-registered, above the process-null p95. Hunt new
constructs and new inputs, not parameters. The protocol file governs.
