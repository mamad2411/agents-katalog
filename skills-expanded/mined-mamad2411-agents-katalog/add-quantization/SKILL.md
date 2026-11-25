---
name: add-quantization
description: Add a quantized precision to a float recipe. Tries w8a8, falls back to w8a16, or gives up. Checks both tflite and qnn_dlc and disables the pairs that fail. Hard-requires a dataset + evaluator (authors them under supervision if missing). Best run after `validate-on-device`, but does not require it.
---

# Add Quantization

Shallow first pass. Try w8a8; if unreasonable, try w8a16; if both fail, revert to `[float]` and stop. No mixed precision / sensitivity search / per-op tuning — that's follow-up work.

**Both runtimes, same as `validate-on-device`.** A precision is only "added" once you know what it does on `tflite` *and* `qnn_dlc`. Quantization is exactly where the two diverge: TFLite and QNN pick different quantization parameters for the same graph, and an op that stays on NPU under one falls back to CPU under the other. A w8a8 that holds on `qnn_dlc` and collapses on `tflite` is a normal result, and it means `tflite` gets disabled — not that w8a8 gets rejected.

## Prerequisites

**Hard requirement — stop and report if missing.** `model.py` implements `get_evaluator()`, `get_eval_dataset_classes()`, `get_calibration_dataset_cls()`, and the returned dataset class exists (either under `qai_hub_models/datasets/` listed in `manifest.yaml`'s `datasets:`, or as a local `dataset.py` in the recipe folder — both are fine).

If the dataset/evaluator is missing, prompt the user to wire an existing one from `qai_hub_models/datasets/` + `templates/…` or author new ones (see `.claude/docs/onboarding/datasets-and-evaluators.md`).

**Recommended but not required — `validate-on-device` green at `float`.** Prefer it: it gives you an on-device float metric per runtime, so a quantized miss is attributable to *quantization* rather than to the runtime, and it means a failure here isn't tangled up with an unanswered question about whether the recipe ever ran on device at all. But a user who asks for quantization on a recipe that has only been through `onboard` gets it. Proceed, with two adjustments:

- **Measure torch float accuracy here.** Drop `--skip-torch-accuracy` from the *first* `evaluate` call so it produces the number. It's runtime-independent, so keep the flag on every call after that and reuse the value.
- **Baseline against torch float**, since no on-device float metric exists. Say so in the report: that delta folds the runtime's own error into the quantization drop, so a miss under it does not prove quantization is at fault. On a miss, offer to run `validate-on-device` at `float` to separate the two — do **not** disable a pair on an ambiguous number.

## Command

```
qai-hub-models evaluate <path> --target-runtime <runtime> --precision w8a8 --num-samples 100 \
    --skip-torch-accuracy
```

`<runtime>` is `tflite` and `qnn_dlc`. If `validate-on-device` ran, compare each against the **same-runtime** float number it produced — a cross-runtime comparison conflates the quantization drop with the runtime difference — and skip any runtime it already disabled at `float`, since there's no baseline to compare against and the pair inherits the float failure. If it didn't run, use the torch float number per the prerequisite above.

**`tflite` only supports `w8a8`.** `TargetRuntime.supports_precision` allows exactly that one quantized precision on TFLite, so `--precision w8a16 --target-runtime tflite` is rejected before a job is ever submitted. w8a16 is a `qnn_dlc`-only fallback. Do not add a `w8a16`/`tflite` entry to `disabled_paths` for it either — the pair is unsupported by construction, `is_supported` already returns false, and `failure_reason` says so without your help.

No separate "torch pre-check" — without `--compute-quant-cpu-accuracy`, torch runs *float*, so `--skip-torch-accuracy` skips re-deriving a number that cannot have changed: a full local pass over all 100 samples, on every one of these runs (twice for w8a8, again for a w8a16 fallback). Keep the flag when `validate-on-device` already measured torch float. Drop it on the **first** call when it didn't, then put it back for the rest.

**No profile job.** The `evaluate` run above is the whole signal, because it submits an inference job: a pair that can't run on device fails it (→ `scorecard_failure`), and a pair that runs with bad numerics comes back with the metric (→ `scorecard_accuracy_failure`). Every threshold in this skill is an accuracy threshold, so latency and peak memory wouldn't change any decision you make here — and if `validate-on-device` ran, it already established the model fits and executes on the device. If the user wants the quantized speedup measured, that's one `export --skip-inferencing` after this skill reports, not part of it.

## Flow

1. **Try w8a8 on both runtimes.** Add to `supported_precisions:`, run the command for each. Within the threshold below on **at least one** runtime → w8a8 is the precision; disable the pairs that missed (next section) and you're **done**.
2. **Fall back to w8a16.** Only if w8a8 missed on *every* runtime. Remove `w8a8`, add `w8a16`, rerun — **`qnn_dlc` only**, per the note above. Same threshold check.
3. **Give up.** If w8a8 missed on both runtimes and w8a16 missed on `qnn_dlc`, revert `supported_precisions:` to `[float]`, **remove the quantized `disabled_paths` entries you added** (nothing consults them once the precision leaves `supported_precisions`, so they'd sit there forever as noise, and scorecard won't clear them either), and report the numbers plus what follow-up work would look like (mixed precision, per-channel schemes, different calibration data). Do NOT try those yourself.

Iterate at most **once** on a failure, and only if the fix is an obvious wiring problem: wrong `get_calibration_dataset_cls()` return, calibration dataset returning wrong dtype/shape/range, evaluator needing a per-precision hyperparameter. Anything else — stop. A wiring fix invalidates both runtimes; rerun both.

## Disabling a quantized path

Same mechanism and same field rules as `validate-on-device` — read that skill's "Disabling a path that won't work" section; the fields, the reason text, and the no-job-IDs rule apply verbatim with the precision key changed. The loop policy here is this skill's own iterate-once rule above, not that skill's report-and-stop. A pair that compiled and ran but drifted too far is `scorecard_accuracy_failure`; one whose compile or quantize job failed outright is `scorecard_failure`.

One addition: **don't disable on a torch-only baseline.** If `validate-on-device` never ran, a miss could be the runtime rather than the quantization, and you can't tell which from one number. Report it and offer the float run.

```yaml
supported_precisions:
  - float
  - w8a8
disabled_paths:
  w8a8:
    tflite:
      scorecard_accuracy_failure: "Torch and On-device accuracy diff (-31.2 Top-1) above threshold (3 pp)"
```

`float` entries stay untouched — you are adding a precision, not re-litigating the float result. Include the actual numbers in the reason, in the same shape scorecard writes them, so the entry stays readable when scorecard later rewrites or clears it.

## Thresholds (max drop from float)

| Task | Threshold |
|------|-----------|
| Classification (Top-1) | 3 pp |
| Detection (mAP) | 5 pp |
| Segmentation (mIoU) | 3 pp |
| Super-resolution (PSNR) | 1 dB |
| Speech-to-text (WER) | 2 pp |
| LLM | see closest sibling's `numerics.yaml` |

For anything else, check a sibling's `numerics.yaml` — any drop smaller than what it accepted is fine.

## Reporting

Always report both runtimes, including the disabled one.

Success:
```
Quantization: PASS — chose <w8a8|w8a16>

qnn_dlc  PASS
- float:       <metric>  (<from validate-on-device | torch, no on-device float baseline>)
- <precision>: <metric>  (drop: <delta>)

tflite   DISABLED -> manifest.yaml disabled_paths.<precision>.tflite
- float:       <metric>  (<from validate-on-device | torch, no on-device float baseline>)
- <precision>: <metric>  (drop: <delta>) — over threshold
```

Failure:
```
Quantization: FAILED — reverted to [float], quantized disabled_paths entries removed
- w8a8   qnn_dlc: <metric> (drop: <delta>) — over threshold
- w8a8   tflite:  <metric> (drop: <delta>) — over threshold
- w8a16  qnn_dlc: <metric> (drop: <delta>) — over threshold
- w8a16  tflite:  not attempted — TFLite supports only w8a8

Follow-up: mixed precision (w8a8_mixed_int16), per-channel schemes, different calibration data.
```

Hand off to the user for the PR either way.
