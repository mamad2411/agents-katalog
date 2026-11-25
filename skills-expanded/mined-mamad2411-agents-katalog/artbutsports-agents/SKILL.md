# ArtButSports agent handoff

## Goal and current state

Pair a sports photograph with public-domain artwork. Judge success by human
ratings of the served gallery, not proxy rank or a model's confidence.

- **The product metric is `findable` (`eval.quality`), not `good@3`.** Every
  served gallery in every release is now rated all ten deep. `good@3` read
  three of those ten, ignored position inside them, and collapsed "good" and
  "would post" into one bucket, so it could not see a change that reorders
  a gallery - which is the only kind of change v15.1 makes. `mean@3` and
  `good@3` are still computed and still reported; they no longer lead.
- **v15.1 is the accepted release.** Same retrieval as v12; the decisive final
  call ranks the ten works the gallery serves. Pooled over the 50 photographs
  of its four blind gates: findable `+4.91 [+0.46, +9.55]`. Every wave is
  positive; none clears zero alone. The promotion was the operator's call on
  that re-analysis, not a fresh preregistered experiment - the original
  preregistered primary (first-wave `good@3 +0.125 [-0.125, +0.375]`) still
  spans zero. Say so when the number is quoted.
- **v16 is a rated-in-progress preview; v15.1 remains the only stable release.**
  It keeps the v15.1 blended winner, then restores the strong final's order for
  the other nine works (`ARTBUTSPORTS_CURATOR_SIGNAL_BLEND_PREFIX=1`). On the
  31 photographs whose counterfactual ten is already fully rated: findable
  `+1.75 [+0.43, +3.35]`, ordering `+2.30 [+0.61, +4.40]`, reachable unchanged;
  all four wave point estimates are positive and no measured case regresses.
  This is coverage-selected retrospective development evidence, not a blind
  win. The 50-photo preview introduces 22 unrated pairs across 19 photographs;
  grade those through the site before judging it. A fresh blind gate still
  requires genuinely new sports photographs because every executable local
  case has already been exposed.
- **v12 is archived**, superseded by v15.1. It clearly beat v9 and was never
  proven better than v11.
- **v13 was rejected.** A much wider slate cost more and did not improve the
  human result.
- **v15 is rejected.** Its 20-case four-arm capture and blind grading found no
  conclusive treatment effect. The specificity selector's offline gain was an
  artifact of counting fewer art lanes, not of choosing better ones. Filling
  a 20-place final retained known-good finalists and did not convert them.
- The v15.1 waves under both metrics, each sealed on its own:
  wave 1 (16 never-served) `findable +1.93 [-6.48, +9.38]`, `good@3 +0.125`;
  wave 2 (10 reserved) `+4.18 [-1.27, +11.57]`, `good@3 +0.000`;
  wave 3 (14 already in v12) `+1.85 [-4.73, +9.71]`, `good@3 +0.357 [+0.071, +0.714]`;
  wave 4 (10 already in v12) `+14.72 [+3.35, +27.45]`, `good@3 +0.200`.
  Gallery is 50 and fully rated. No further captures for this release.
- The same grader's test/retest swing is `0.100 good@3` and `15.1 findable
  points`; smaller absolute changes are a useful lead, not a win. Both floors
  are measured on the 50 v9 galleries that survive in the frozen first-session
  snapshot (`eval.quality.noise_floor`).

## Pipeline

Load once with `artbutsports.pipeline.load()`, then call
`await artbutsports.pipeline.run_query(system, image_bytes)`. It builds a
structured visual brief, unions fast retrieval lanes into a family-diverse
slate, runs an opaque-ID tournament, then blends judge rank with DINO-full and
the text bridge. Fatal curator failures serve the untouched fast order;
partial failures retain traced, comparison-safe degraded output.

v15.1's shipped default is v12 retrieval with `CURATOR_FINAL_GROUP_SIZE=10`
and `CURATOR_FILL_FINAL=1`. Old manifests pin
`ARTBUTSPORTS_CURATOR_FINAL_GROUP_SIZE=20` and
`ARTBUTSPORTS_CURATOR_FILL_FINAL=0` so v12/v13 retain their intended geometry.
v15 still records `ARTBUTSPORTS_CURATOR_ART_TARGET_LANE_LIMIT=3`; that knob is
no longer read. v16 changes only terminal delivery: the normal 35% DINO/text
blend still computes a full diagnostic order, but only its first candidate is
served ahead of the unmodified strong-judge order. Traces retain all three as
`judged_order`, `blended_order`, and `delivered_order`. Prefix zero preserves
the v15.1/legacy full-blend policy.

## How quality is measured

`eval/quality.py` is the single definition; `eval.build_site` imports it, so
the public page and the research report cannot drift apart.

- `findable(gallery) = max over ranks of VALUE[rating] * ATTENTION[rank]`, over
  the whole served ten. `VALUE = (0, 0.15, 0.70, 1.00)` prices the label scale
  as the posting decision it is; `ATTENTION` is the log-sigmoid this project
  used for target findability, knee 4, steepness 1.8, normalised so rank 1 is
  1.0. A score of 100 means every photograph's first result was a "would post".
- `reachable` is the same score with position ignored (retrieval), `ordering`
  is `findable / reachable` (delivery). They are the two losses the audit
  already knew were separate, finally on one scale.
- The constants are a judgement call, so they are only allowed to decide what
  they would also decide under other reasonable ones. `eval.quality.sensitivity`
  re-runs the verdict across four pricings and three curves; the v15.1 blind
  result is positive in all twelve and clears zero in nine. The three it does
  not clear are the `(0,0,1,1)` pricing - which is exactly what `good@3` did.
  That is the finding, not a caveat.
- Evidence has two strengths and the page says which is which. **Blind A/B**:
  both arms on one photograph, rated in one pass with the arm hidden; immune to
  cohort and to grader drift. **Same photographs**: two captures over the
  photographs they share; fixes the cohort, not the rating session. Never quote
  an absolute score as a comparison.
- Do not add a third comparison that models cohort difficulty. An additive
  photograph+version fit over all 375 observed cells puts v15.1 at `+14.8`
  against v12, three times the blind estimate, because it corrects for the
  cohort and not for the grading session. It was tried and left out.

## Hard truths from the audit

- Reordering the already-served top ten has `+0.59` to `+0.67 good@3` oracle
  headroom. Ordering is the largest known opportunity, and v15.1 is the first
  change to convert any of it on a blind test. Absolute `ordering` is 0.86 for
  v15.1 against 0.81 for v12: most of the headroom is still there.
- Retrieval and delivery are separate losses. From v11→v12, 65 incumbent good
  top-three works became 53 slate members, 37 blended top-ten, and 31 served
  top-three. From v12→v13 the slate/blended-delivery funnel was 38→38→17→11;
  the pure judge top ten retained 13.
- Of 25 published pairings we own, v12 admits 6; 11 lose at lane quota and 8
  never reach any lane's top 1,000. None lose at the slate cap.
- All 25 targets are within rank 32 when searched with a caption of the target
  artwork itself. The index is capable; query interpretation is the gap.
- Allocation at this cap is finished. Thirteen lanes sharing 150 round-robin
  slots are each read about eleven deep. No subset, quota, share weighting or
  fusion beats v12's six-of-twenty-five published-target admission, and the
  ceiling for *any* policy is seven of twenty-five at depth 35. Depth 256
  needs the slate v13 shipped and had rejected. Change what a query means, not
  how its results are apportioned.
- The v15 specificity selector scored `+0.113 [+0.028, +0.211]` known-good
  works against six art lanes. Against a 300-draw null of choosing any three
  of the six it lands at the 78th percentile (one-sided p=0.217). A uniformly
  random art lane scores `+0.056` on the same metric. The gain was lane count.
- Filling the final to 20, replaying v13 traces, retained 70 of 141 known-good
  opportunities versus 53, `+0.57 [0.30, 0.87]` per case. Across the graded
  v15 gate, 52 of 53 screening survivors reached the strong judge under fill
  against 27 under control, and both arms then delivered 25 vs 24 known-good
  works into the served three. Finalist retention is not a proxy for quality.
- Ranking the v12 served ten in one interleaved 5-vs-10 final
  (`eval/judge_runs/gemini-3.6-flash__final_size_20260823.json`) moved
  good@3 `0.864 -> 0.909 (+0.045 [-0.182, +0.273])` and mean@3
  `0.924 -> 1.000 (+0.076 [-0.076, +0.227])`. Twenty-nine of 66 served-three
  slots changed. Neither interval clears zero; the change is structural. The
  v15.1 gate then replicated the direction on 16 disjoint cases at roughly
  three times the size. Reproduce both from `eval/labels/current.jsonl`.
- The judge already emits relational, composition and visual-echo scores that
  serving discards. A $0.12 four-case probe on those dimensions
  (`eval/subscores.py`) found them collinear with `overall_score` or unable to
  beat it on good@3. Do not revive sub-score reranking without a new signal.
- Three v16 fast-stage continuations were falsified against the full corpus.
  Unconstrained human-trained DINO weights collapsed known-good median rank
  from 47.5 to 3,812; preservation-constrained weights became inert and never
  improved all five held-out case folds. Image-space pseudo-relevance feedback
  over 24 `k/alpha/background` settings never beat v12's `6/25` target
  admission and every setting lost at least one baseline known-good work; the
  leave-one-case-out total fell `208 -> 203`. Do not evaluate a learned metric
  only inside the label-selected candidate pool or revive centroid feedback.
- A sealed $0.8557 development run made one extra five-way call over each
  v15.1 gallery's head. Moving that call's winner first made findable
  `-2.07 [-3.80, -0.27]` on all 50 photos, with negative point estimates in
  three of four waves. The blend already picks the better champion. Do not add
  a polishing call or infer quality from judge confidence/margin.
- More candidates, captions, calls, or prompt prose are not inherently more
  information. Measure admission and human quality, not log-rank alone.
- Model aliases drift between service epochs. A/B arms must be interleaved in
  one session and record date, exact model, prompt, preprocessing, and input
  hashes. Nominal seeds do not make calls historically reproducible.
- The historical negative top-level colour weight was skipped by production,
  while rank fusion still used colour positively. Do not "fix" that mismatch:
  replaying negative colour made target retrieval worse.
- Settled null/negative paths: prompt-only caption tuning, 12 captions, named
  artwork, subject vocabulary, shape and self-similarity lanes, crop/resolution
  variants, cheap triage, second opinion, few-shot taste boards, learned or
  personalized taste rerankers, specificity-gated art lanes, and discarded
  judge sub-scores.
- Repeating tournament partitions roughly doubles calls for only `+0.082`
  known-good finalists per case. Shared anchors may address group-scale drift,
  but need a preregistered blind experiment, not another speculative release.

## Experiment contract

Before a paid run, write the hypothesis, unit (case, never pair), primary human
metric, guardrail, holdout, cost cap, and stopping rule. Compare both arms on
the same cases and labels; interleave model calls in one session. Report paired
case-bootstrap intervals. Track published-target recall **and** loss of known
good works. Run `eval.captures` to locate the stage of every regression. Test
one substantive uncertainty per arm; if a recovery candidate combines gated
changes, retain single-change controls before publishing it. All paid calls
must use the durable budget ledger; never bypass it or publish/grade
automatically.

Do not compare combined v15 with a historical v12 capture. The completed 20-case
2×2 remains development evidence: v12 geometry (six lanes/fill off), selector
only (three/off), fill only (six/on), and combined (three/on). Read it with
`eval.capture_gate report --state showcase/data/v15-gate.json`. Every arm
restored the original opaque shuffle before its final; the historical
five-final path leaked screening order, so that control is v12 geometry under
this common measurement-hygiene correction, not a byte replay of the published
v12 capture.

The confirmatory v15.1 question was: does ranking the
whole served gallery in one strong final beat sending only the five group
winners? `eval.capture_gate` is the only valid runner. It shares one
interpretation and one screening, then obtains two independent finals per
case. It fails closed on a partial run and publishes no gallery until every
arm is comparison-safe. The run is done: `showcase/data/v15.1-gate.json`,
plan `58b1a12b…`, 16 cases x 2 arms, $1.129397 actual against a $1.30 cap.
Read it with `eval.capture_gate report`:

```
control    n=16  mean@3=1.292  good@3=1.250
candidate  n=16  mean@3=1.437  good@3=1.375
control -> candidate  mean@3: +0.146 [-0.000, +0.312]
control -> candidate  good@3: +0.125 [-0.125, +0.375]
```

Guardrails were clean: published-target recall 0/5 in both arms, and of the 48
works rated good anywhere in either served ten the candidate delivered 22 into
its served three against 20, and 46 into its ten against 45. Candidate gained
a good work in 3 cases and lost one in 1; on mean@3 it was better on 6, worse
on 3, tied on 7. The gains are rescues of dead galleries (`[0,0,0]` to
`[0,2,0]`), which is the mechanism doing what it was built for.

Two things this gate settled that are worth keeping. The change is **not** a
pure reorder: 35 of 48 served-three slots and 126 of 160 served-ten slots
differ between the arms, and the served ten is the same *set* of works in only
6 of 16 cases, because a different judge order feeds a different blend window.
And a second, disjoint paired measurement of the same 5-vs-10 contrast
(`eval/judge_runs/gemini-3.6-flash__final_size_20260823.json`, 22 v12 served
tens, pure judge order) moved `good@3 +0.045 [-0.182, +0.273]` and `mean@3
+0.076 [-0.076, +0.227]`. Combined over all 38 paired cases: `good@3 +0.079
[-0.079, +0.263]`, `mean@3 +0.105 [-0.000, +0.219]`. Four positive point
estimates and not one interval that clears zero. That is the honest shape of
this effect, and no cohort this project can afford will sharpen it.

Two facts about that cohort are load-bearing, and both were fixed before the
arms that carry them ran. The sealed order is
`sha256("v15.1-final-size-gate-2026-08-26:" + case)` over the 27 cases that
have never been captured or graded; only the first 17 were affordable, so the
cohort is that prefix. `abmis-2025-033` then proved unexecutable: its shared
visual brief exceeds `max_output_tokens=1536` and, at `temperature=0,
seed=17`, truncates at the same byte every time, so neither arm ever ran and
no gallery for it ever existed. Raising the limit for one photograph would
have given it a different query interpretation from the other sixteen. It is
recorded in `INFEASIBLE_CASES` and dropped through `capture_gate amend`,
which is the only sanctioned way to narrow a sealed plan: it may drop cases
and nothing else, refuses any case that already produced a result, refuses
reordering and any change to the hypothesis, unit, metrics or arms, and
writes the superseded digest and the reason into the artifact. The ten unrun
cases past that prefix are the remainder wave: same seed, positions 18-27,
`showcase/data/v15.1-gate-2.json`, plan `ee6727e5…`, 10 cases × 2 arms,
$0.651665 actual against a $3.00 cap, status complete, rated 2026-08-26.
Both arms mean@3 1.433 / good@3 1.500. good@3 +0.000 [-0.500, +0.500],
mean@3 -0.000 [-0.233, +0.267]. Do not pool it with the first wave as one
preregistered experiment. Report each with `eval.capture_gate report --state`.

The first-wave captureGate stays `v15.1-gate.json` for fully-rated statistics.
`site.ratingGates` lists `v15.1-gate-2.json`, `v15.1-gate-3.json`, and
`v15.1-gate-4.json` so later waves enter the blind queue without replacing
the first-wave numbers. An incomplete remainder or expansion writes only its
wave-local file and must not delete `showcase/data/v15.1.json`.

A third wave, `showcase/data/v15.1-gate-3.json`, plan `e8844952…`, captured
14 photographs already served by v12 ($0.956 against a $1.50 cap). Gallery
expansion, not a confirmatory holdout. Rated: good@3 +0.357 [+0.071, +0.714],
mean@3 +0.024 [-0.167, +0.214]. Report it separately.

A fourth wave, `showcase/data/v15.1-gate-4.json`, plan `50daaf28…`, captured
10 more already-served v12 photographs ($0.706 against a $1.00 cap). Gallery
is 50 and fully rated: good@3 +0.200 [-0.300, +0.800], mean@3 +0.000
[-0.333, +0.333]. Report it separately. The comparer now shares 24
photographs with v12. No further captures for this preview.

## Site and rating workflow

The showcase is the canonical release hub, not an optional publication step.
Every numbered version must have a `releases/vN.json` entry in the same change
that creates it, including point releases such as `v15.1`. `eval.build_site`
discovers those manifests automatically and orders them by dotted version;
never add a second hard-coded frontend release list.

- Set `site.status` to exactly one of `stable`, `preview`, `rejected`, or
  `archive`. Exactly one release is stable and must have a capture; currently
  that is v15.1. `site.gateLabels` maps a gate artifact to the wave name the
  page prints, so wave naming lives in the manifest and not in the frontend. An implemented but ungraded or uncaptured version is a preview,
  never the latest stable.
- Keep rejected and archived releases as compact metadata logs even after
  deleting their dead runtime. Do not restore obsolete code or caches just to
  make a gallery. A legacy capture name belongs in `site.capture`.
- A preview without `showcase/data/vN.json` stays visible but cannot be selected
  or rated. Adding its capture and rebuilding automatically unlocks it in the
  comparer and blind-rating queue; changing release status is a separate
  evidence decision.
- The comparer stacks versions against the *same* photograph, so a
  confirmatory capture shares nothing with the stable release and pairing them
  renders an empty page. `default_comparison` opens on such a preview alone.
  The v15.1 expansion waves added 24 v12 photographs, so that pair now has overlap;
  keep the shared-photo rule if you touch the manifest defaults.
- Run `uv run python -m eval.build_site` after every release, capture, or label
  change. Never hand-edit ignored `showcase/site/data/`; the builder owns it and
  removes stale generated payloads. A release's declared `site.captureGate`
  drives fully rated gate statistics; optional `site.ratingGates` adds further
  completed gate files to the blind-rating queue. Never copy gate numbers into
  a second frontend data list.
- Grade through `showcase/site/grade.html`, export
  `artbutsports-ratings.jsonl`, review/merge those rows into
  `eval/labels/current.jsonl`, rerun the offline evaluation suite, then rebuild
  the site. The export is the browser's whole `localStorage`, not a delta:
  merge on `(pair_id, ts, score)` and append only rows that key does not
  already match, or you will double-count old ratings as a second pass. Capture, blind grading, release acceptance, and deployment remain
  separate actions.
- Before publishing, smoke-test Overview, Results, and Rate in the rendered
  site at desktop and mobile widths. Confirm stable/preview labels, selected
  version highlighting, unavailable-preview behavior, and a clean browser
  console. Do not deploy unless the user asks.

## Commands

```bash
uv sync --group dev
uv run pytest -q
uv run python -m eval.quality
uv run python -m eval.captures
uv run python -m eval.slate --variant h6
uv run python -m eval.lanes
uv run python -m eval.recall
uv run python -m eval.reliability
uv run python -m eval.build_site
uv run python -m eval.capture_gate report --state showcase/data/v15-gate.json
uv run python -m eval.capture_gate report --state showcase/data/v15.1-gate.json
uv run python -m eval.capture_gate report --state showcase/data/v15.1-gate-2.json
uv run python -m eval.capture_gate report --state showcase/data/v15.1-gate-3.json
uv run python -m eval.capture_gate report --state showcase/data/v15.1-gate-4.json
uv run python -m eval.capture_gate run --dry-run
uv run python -m eval.capture_gate run --cap 1.00
uv run python -m eval.capture_gate report
uv run python -m eval.capture_gate amend --reason "why a sealed case cannot run"
```

Once dependencies are installed, every evaluation command above is
network-free except a live `capture_gate run` without `--dry-run`. Paid
capture must run only through `eval.capture_gate`; never publish or grade a
partial gate. After the operator explicitly opened the remaining key balance
for v16 research, the durable ledger stands at $15.394 spent of a $25.50
operator-set ceiling. The v16 head-polish falsification spent $0.856 of its
$2.00 experiment cap. The remainder wave used $0.652 of a $3.00 cap; the
first expansion used $0.956 of a $1.50 cap; the second expansion used $0.706
of a $1.00 cap. An agent must never raise the ceiling unprompted.

## Safety and provenance

- Do not modify `artbutsports/features.py` casually. Its bytes and dependency
  versions authenticate the frozen feature table. Build a new table under a
  new contract instead.
- Pose extraction and `ultralytics` remain compatibility-only because they are
  part of that frozen contract; serving does not run them or provision a YOLO
  checkpoint. Remove them only with an explicit feature-schema migration.
- Feature and calibration paths are separate decisions in
  `artbutsports/artifact_paths.py`; never override them through `.env`.
- Query-feature caches must include extractor-contract and input hashes.
- Matrix rebuilds contain only locally reproducible signals; paid retrieval
  lanes are evaluated from the separately authenticated slate caches.
- Retained slate caches fail closed on cohort, corpus, policy, inputs, exact
  vectors, and result bodies. A paid query-vector refresh must be explicit.
- H6 brief and most text-embedding calls predate call-time provenance; exact
  source/vector bytes are bound, but their provider epoch is unknown. Do not
  claim historical replay.
- Keep candidate order opaque to the judge, family diversity, deterministic
  fallbacks, and stage membership/order traces. Numeric judge scores are
  call-local and must never be compared across tournament groups.
- A capture is not a release. Blind human grades settle quality.
- `require_untouched_cohort` guards *sealing*, not reading: once a gate has run
  and been graded its cohort is of course labelled. Likewise a gate whose
  status is `complete` serves its sealed record even when the files its plan
  hashes have since changed, so recording a verdict cannot lock the artifact.
  Both refusals stay live for any gate that could still run an arm.
- A fresh clone must restore ignored `data/`, `cases/`, and `showcase/data/`.
  Restore `eval/pair_matrix.npz` or run `eval.build_matrix` before `eval.captures`
  or reliability audits; the visual showcase also needs `showcase/public/images/`.
