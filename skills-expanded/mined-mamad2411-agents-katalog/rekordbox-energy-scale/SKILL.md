---
name: rekordbox-energy-scale
description: Compute, validate and apply a relative 1-10 energy scale across the whole rekordbox library (or any playlist) from deterministic audio DSP plus essentia ML features. Use when the user asks about energy tags/labels/levels, wants tracks ranked by energy, wants set-building by intensity, or asks why the Energy My Tags look wrong.
---

# Relative energy scale (1-10)

Scripts referenced here live alongside the rest of the library tooling.

## The core principle: energy is DEFINED, not learned

There is **no usable ground truth for energy in this library**. Two candidates were
tested and both are dead ends — do not spend time re-deriving these:

- **The `hi`/`mid`/`lo` My Tags are NOT hand-curated energy judgements.** They came
  from the playlists `psy/energy-sets/{hi,mid,lo}` — **psytrance only**, a genre-specific subset.
  A ridge on the 1280-dim embedding predicts them at held-out rho 0.767, but that is
  largely "which psy subgenre", not energy. Never train a library-wide energy model
  on them.
- **Play position within recorded sets is NOT an energy signal.** Across recorded
  sessions it correlates 0.02-0.05 with every candidate feature, and the sign
  flips by genre (psy -0.135, house +0.116). An early 0.362 reading was n=229 noise.
  Sets are not strictly energy-ramped.

So every component of the score is a **named, signed, inspectable number**. No
black-box scalar is allowed to define the axis.

## Why the old tags were wrong (context if the user asks)

`ingest_tags.py` thresholded `mood_aggressive` — an essentia **mood** classifier — at
fixed cutoffs. That detects harsh timbre, not energy, so it inverted whole genres:
**dnb came out 66% "warmup"**, disco 83%, hip-hop 75%, while psy was 47% "peak". It
correlates only 0.343 with the (unused) `essentia_ml|energy`, and 38.4% of tracks fell
below the bottom cutoff, making "warmup" a dumping ground at 36.7% of the library.

Separately, `audio_features.py`'s `energy` is **raw RMS over a fixed 30-120s window** —
it measures the mastering, not the music, and often lands on an intro. Measured: it puts
**16.9% of duplicate files of the SAME SONG more than two deciles apart.**

## Pipeline

### 1. Extract (`energy_analyze.py`)
```
~/.rekordbox-venv/bin/python energy_analyze.py --workers 6
```
ffmpeg -> numpy, **no librosa** (the old `~/.rbx-audio` py3.12 venv is gone;
`~/.rekordbox-venv` has numpy and is all this needs). Writes `source='dsp2'` into
`energy_features.sqlite`. Incremental — re-running skips finished ids. ~0.50s/track with 6 workers.

**Profiling (measured; corrects an earlier assumption that this is I/O-bound).**
Single-threaded the split is decode 55% / compute 45%. With 6 workers the observed rate
barely improved on the single-threaded per-track time — parallel efficiency of roughly
18%. The cause is memory bandwidth, not disk: the framing step materialises a ~212 MB
index array per track per worker, and on Apple Silicon every core shares one memory
controller. Measured findings, in order of value:
1. Replace fancy-index framing with `np.lib.stride_tricks.sliding_window_view` —
   **3.23x faster** single-threaded, and it removes the large allocation entirely, so
   parallel scaling should gain more than that figure suggests.
2. Do **not** raise worker count. Decode measured 0.117 s/track at 6 workers, 0.239 at
   10, 0.287 at 16 — an external USB SSD degrades under concurrent random access.
3. Do **not** use Apple's AudioToolbox decoder (`-c:a mp3_at`): measured **34% slower**
   than ffmpeg's software path, which is already NEON-optimised.
4. No precision win available — numpy already returns complex64 from float32 input.

Three design rules that matter:
1. **Each track is divided by its own RMS before measurement** — master gain cancels,
   so this measures arrangement density and spectral balance, not the mastering engineer.
2. **Whole track** (720s cap), not a fixed window.
3. **Percentile summaries, not means** — p90 captures what a track does at its peak.

Note `flux_p50` is inert by construction (flux is normalised by its own median, so p50
is always 1.0). It is excluded from the composite.

### 2. Score (`energy_score.py`)
Robust-z (median/IQR, clipped +-4) each feature, apply its sign, pool into four groups,
**re-standardise each group score before weighting**, then weight:

| group | w | meaning | members |
|---|---|---|---|
| drive | 0.30 | busyness / movement | onsets_per_beat, flux_p90, pump |
| weight | 0.25 | spectral force | r_bass, r_sub, r_hi, centroid |
| full | 0.20 | how much runs at full tilt | sustain, -crest, -dyn_range |
| percept | 0.25 | essentia mood models | aggressive, party, energy, -relaxed |

**The re-standardisation is load-bearing.** Without it the weights are fiction: the four
essentia features all move together, so at a nominal 0.25 the `percept` group exerted
+0.756 influence on the final score.

### 3. Calibration (`energy_calibration.json`) — REGENERATE AFTER ANY FORMULA CHANGE
`--recalibrate` freezes the per-feature median/IQR, the group-norm params, and the
decile thresholds. Scoring then uses those fixed numbers, so **importing tracks no
longer reshuffles existing scores**. Measured: rescoring a random half of the library
gives 100% identical deciles frozen, vs 39.6% in relative mode.

The thresholds map today's library to deciles **1-8**, leaving 9-10 as headroom for
material harder than anything currently owned (~4% currently spills into 9-10, which
is accepted — some tracks genuinely are that hard).

`load_cal()` refuses a STALE file (one whose component set no longer matches
`COMPONENTS`) and falls back to relative mode with a warning. So after editing
`COMPONENTS` or `GROUP_W` you MUST re-run `--recalibrate`.

### 4. Rank
Scoring and ranking are deliberately separate. The stored value is a **continuous
score**, so deciles are computed over whatever set is asked for — the whole library
(`--all`) or a single playlist (`--playlist NAME`). Same numbers, different denominator.

## Validation — always run these before applying tags

1. **Duplicate-file consistency (the strict test).** Group tracks by normalised
   artist+title; the same song as two files must score the same. Composite achieves
   mean |delta pct| 0.025 with 2.6% of pairs >2 deciles apart, vs raw RMS at 0.112 /
   16.9%.
2. **Embedding-neighbour smoothness.** Near-duplicates (cosine > 0.97) agree to ~0.048.
   **Do NOT maximise this metric** — it rewards genre detectors; `mood_aggressive`
   scores a "better" ratio 0.30 vs the composite's 0.54 precisely *because* it is a
   timbre readout. It is a floor to clear, not a target.
3. **Genre medians must be sane and non-inverted** (hip-hop and disco low, techno and
   psy high) and **BPM correlation must stay modest** — energy must not be a tempo proxy.
4. **No single component may dominate** the final score.

## Cross-check via the embedding
Energy is a linear diagonal direction in the 1280-dim embedding, predicting the composite
at held-out rho **0.843** — see the `energy-direction-in-embedding` memory. Because the
DSP composite is computed from raw audio with no knowledge of the embedding, and the
embedding comes from a separate model, this is genuine cross-validation. Use it also to
**impute energy for tracks whose audio files are missing** (a meaningful share of `track_files` paths are dead) but which still have embeddings.

## Do not delete
`energy_analyze.py`, `energy_score.py`, `energy_features.sqlite` and
`energy_progress.sh` are the deterministic pipeline and must be kept even if the
scoring formula is later replaced — the raw `dsp2` features are formula-independent
and re-extraction costs hours.
