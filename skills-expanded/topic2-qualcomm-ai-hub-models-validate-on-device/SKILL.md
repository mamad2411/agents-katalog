---
name: validate-on-device
description: Compile, profile, and check numerics for a float recipe on a Snapdragon device via AI Hub, across both tflite and qnn_dlc, running the matrix in parallel. Records every failed (precision, runtime) pair in the manifest's disabled_paths and reports it rather than debugging; troubleshoots with `.claude/docs/on-device-debugging.md` only when asked. Use after `onboard` produces a `validate`-green float recipe, and before `add-quantization`.
---

# Validate a Float Recipe on Device

`onboard` proves the recipe is *authored* correctly. This skill proves it **compiles, profiles, and holds its numerics** on a real device at `float`, **on both `tflite` and `qnn_dlc`**. No quantization here — `supported_precisions:` stays `[float]`.

## Prerequisites

- `qai-hub-models validate <path>` prints `0 failed`. If not, go back to `onboard` — do NOT paper over validate failures to reach this skill.
- User's AI Hub token is configured (`qai-hub configure --api_token ...`). If not, stop and tell them.
- `supported_precisions:` in `manifest.yaml` includes `float`. If not, this skill has nothing to check.

## The runtime matrix

Run the whole sequence **twice**, once per runtime:

| Runtime | Why both |
|---|---|
| `tflite` | The default runtime, and the one most consumers hit first. Litert/TFLite delegates differ from QNN on layout, dtype coercion, and which ops fall back to CPU. |
| `qnn_dlc` | The NPU path, and the gate for the whole AOT family — `qnn_context_binary` and `precompiled_qnn_onnx` resolve to the `qnn_dlc` entry via `failure_reason` when the model doesn't `requires_aot_prepare`, so proving (or disabling) `qnn_dlc` covers them. |

Runtimes are independent: `tflite` passing tells you nothing about `qnn_dlc`. Being independent, they also run **concurrently** — see "Run the matrix in parallel". Do **not** stop after the first runtime passes, and do not stop after the first one fails.

## Pass criteria (per runtime — all must hold; do not declare success on a subset)

1. **Compile** — Hub job for `--target-runtime <runtime> --precision float` on the manifest's `default_device` finishes `state == SUCCESS`.
2. **Profile** — completes with non-empty `layer_details`, `estimated_inference_time_ms`, `peak_memory_usage`. No `dspservice just died`, no unresolved rank / memory / segfault errors in the device log.
3. **Numerics** — exactly one of these two, decided by whether an evaluator is wired:
   - **Evaluator wired** (`get_evaluator()` **and** `get_eval_dataset_classes()` both present) → **skip inferencing**, pass `--skip-inferencing` to `export`, and get numerics from `evaluate` instead. A dataset metric on 100 samples is strictly more informative than PSNR on one sample, and running both means paying for a second inference job that tells you less.
     - **Torch accuracy** — within ~5 pp of the reference number (model card / paper / sibling `numerics.yaml`) on a 100-sample subset, or matches the reference exactly if the model is deterministic on that many samples. Runtime-independent, so check it **once**, not per runtime.
     - **On-device accuracy** — within ~1 pp of torch at float, per runtime. Larger gap → preprocessing / postprocessing / dtype / layout issue. Quantization drift is a separate concern that belongs to `add-quantization`, not here.
   - **No evaluator** → **run inferencing** (drop `--skip-inferencing`) and read the PSNR table `export` prints comparing on-device against local torch. **Every output ≥ 20 dB**, matching the scorecard's own threshold (`aggregate_scorecard_results.py --psnr-threshold`, default `20.0`). Below that, the graph is computing something different on device — same failure taxonomy as an accuracy gap. Outputs listed in the manifest's `outputs_to_skip_validation` are exempt, and that key exists precisely for outputs whose PSNR is meaningless (many low-confidence values filtered out in postprocessing); adding a *new* entry to dodge a low number is bypassing the check, not configuring it.

## Commands

**Internal (in-tree) models:** prefix every `qai-hub-models` invocation with `QAIHM_DEV_MODE=1`. The model isn't published yet, so without it the CLI blocks on the unpublished-model prompt and rejects any `--precision` / `--target-runtime` not already listed in `supported_precisions:`. Standalone/external recipes don't need it.

`<runtime>` below is `tflite` or `qnn_dlc`. Run each block once per runtime.

Compile + profile, **evaluator wired** (numerics come from `evaluate`):
```
qai-hub-models export <path> --target-runtime <runtime> --precision float \
    --skip-inferencing --skip-downloading
```

Compile + profile + PSNR, **no evaluator** (numerics come from the inference job):
```
qai-hub-models export <path> --target-runtime <runtime> --precision float \
    --skip-downloading
```

`--skip-summary` is deliberately absent from both: the summary is what prints the PSNR table, so skipping it costs you a check to save a few seconds of waiting.

By default `export` submits both compile and profile. Read job URLs from stdout and wait for both.

Torch-only accuracy pre-check (fast, ~seconds; runtime-independent, run **once**):
```
qai-hub-models evaluate <path> --precision float --num-samples 100 --skip-device-accuracy
```

On-device accuracy, per runtime (few minutes) — `--skip-torch-accuracy` because the pre-check above already produced that number and it doesn't change per runtime. Without it, `evaluate` runs a full local torch pass over all 100 samples on every call:
```
qai-hub-models evaluate <path> --target-runtime <runtime> --precision float --num-samples 100 \
    --skip-torch-accuracy
```

Always run the torch-only pre-check first, alone. If torch is already broken, on-device will be too, and torch failures are much cheaper to diagnose. It is also the cheapest way to find out an evaluator you thought was wired isn't.

Use these forms verbatim, adjusting `<path>` and `--device` if the user asked for a specific device. Do not invent flags.

## Run the matrix in parallel

Run serially, this skill is almost entirely waiting on Hub — two runtimes × (compile + profile + numerics), one at a time. Almost none of it is actually ordered. Fan it out.

Only one ordering is real: the torch-only pre-check runs first, alone. It's local, takes seconds, and if torch is broken every device number is meaningless — one cheap failure saves four Hub jobs.

Everything else goes at once: `export` for **both** runtimes, plus `evaluate` for both when an evaluator is wired. Within one runtime, `export` and `evaluate` are separate invocations that each compile for themselves, so they don't queue behind each other either — 4 concurrent invocations with an evaluator wired, 2 without.

Launch each with Bash `run_in_background`, one log file per invocation, so two failures don't interleave into one unreadable transcript:

```
qai-hub-models export <path> --target-runtime tflite --precision float --skip-inferencing \
    --skip-downloading > "${TMPDIR:-/tmp}/claude/export_tflite.log" 2>&1
```

Then read the logs and assemble the report. **Collect the whole matrix even when something fails early** — a fast failure on one runtime is not a reason to abandon the other. The first report should carry every result, not a partial one.

Hub may still queue jobs behind one another on a busy device, so the wall-clock win is mostly on the compile side and isn't guaranteed. Parallelizing costs nothing either way, so do it regardless.

## On failure: report, don't debug

**One attempt per check.** Then finish the rest of the matrix, record the failure in `disabled_paths` (next section), report, and stop. Don't edit `model.py`, walk resolution down, or resubmit variants unprompted — that spends the user's Hub quota and changes the recipe before anyone agreed the fix is wanted.

The report needs every `(runtime, check)` pair, the verbatim error, your hypothesis from the taxonomy below **marked as one**, and what a fix would involve so the user can price it.

**If the user asks you to debug:** apply a targeted fix, rerun the **same** check, don't skip ahead. Stop when two consecutive attempts give the same failure signature — same error class, same offending op, same delta from torch. Never bypass a check by removing, mocking, or suppressing it.

**A fix for one runtime invalidates the other.** Any change to `model.py` / `app.py` / the input spec means the runtime you already proved is now unproven. Rerun it. Reordering ops to dodge a QNN rank error routinely changes the TFLite numbers.

## Disabling a path that won't work

Every `(precision, runtime)` pair you watched fail goes in `manifest.yaml` under `disabled_paths` — the same mechanism in-tree models use, and valid for standalone recipes too.

**Record it on the first failure, before anyone debugs.** Otherwise the manifest claims a path works while you have evidence it doesn't — advertised in the generated README, and handed to the next person as the default to try.

It isn't a verdict, because it doesn't stick. `export`/`evaluate` still let a user select the pair explicitly; they just stop *defaulting* to it, and warn first. And for in-tree recipes the entry clears itself: PR CI skips a disabled pair (`ignore_known_failures: false`) so it stops blocking unrelated PRs, while the weekly scorecard keeps running it (that input defaults to `true` there) and removes the entry once the model passes. Standalone recipes have neither, so there the entry stands until someone re-runs the pair — which is what the warning on selecting it says.

Investigation only changes what the reason may claim: the error plus `— not investigated` when you haven't looked, the named cause when you have. Never write the second on the strength of the first — a guessed cause outlives the guess and reads as something that was checked.

```yaml
disabled_paths:
  float:
    tflite:
      scorecard_failure: "Compile failed: QnnDsp incorrect Rank 6 — not investigated"
```

Write exactly one of two fields, whichever matches what actually failed:

| Field | Use for |
|---|---|
| `scorecard_failure` | Compile, profile, link, or inference job failure. Anything that didn't produce a number. |
| `scorecard_accuracy_failure` | It ran, but the number was wrong: accuracy gap over threshold, PSNR under 20 dB. |

Those two are the whole vocabulary available to this skill, and they are the fields the weekly scorecard itself writes — which is what makes them self-clearing, as above.

**Never write `issue` or `causes_timeout`.** `issue` means a human filed and owns a tracked bug; it requires a real tetracode/JIRA link, it never clears itself, and inventing one — or pointing at an issue you didn't file — fabricates a paper trail. If the failure looks like it deserves a filed issue, say so in your report and let the user decide; filing is theirs, not yours. `causes_timeout` additionally disables scorecard, so the path would never be retried at all.

Rules:

- **State what failed — the error class and the offending op.** "Doesn't work" is useless to whoever picks this up. **No job IDs or URLs**: a job belongs to the account that submitted it, so the next reader can't open it, and the entry outlives the run by months. Describe the failure so it stands on its own. Job URLs go in your report to the user, not in the manifest.
- **Disable the narrowest thing that failed.** One runtime under `float`, not the whole precision. Remember `qnn_dlc` also covers the AOT family, so don't add separate `qnn_context_binary` entries.
- **Never disable a path you didn't run.** No pre-emptive entries, no copying a sibling's `disabled_paths`. This is the real guard — the entry must record something you observed.
- **Disabling is not a substitute for reporting.** Write the entry *and* report the failure. Silently recording it and calling the run a pass is the one thing that makes this skill untrustworthy.
- **If every runtime for `float` is disabled, this skill FAILED.** Do not ship a recipe that supports nothing and call it a pass. Report both failures and hand back to the user — a float recipe that runs on no runtime is an `onboard` problem, not a manifest problem.

## Failure taxonomy

See `.claude/docs/on-device-debugging.md` for the canonical list. Use this to name the *hypothesis* in your report; the fixes below are what you apply once the user asks you to debug, not on your own initiative. Highlights:

**Compile:**
- `ImportError` / `ModuleNotFoundError` → missing `external_repos:` entry, self-referential import in a standalone recipe (see `onboard` rule), or missing `requirements.txt` line. Fix and rerun.
- Rank > 5 (`incorrect Rank 6`) → a reshape/permute produces a 6D intermediate. Restructure to stay ≤5D, verify torch output is numerically identical before resubmitting. See `.claude/docs/on-device-debugging.md` § Rank errors.
- Unsupported op → compile log names the specific op. Options: replace with an equivalent supported op, monkeypatch upstream to swap the impl, or slice the graph so the op runs on CPU (last resort).

**Profile:**
- Memory exceeded (`unable to tile`, `std::bad_alloc`) → walk resolution down; when the model has a resolution knob, walk it until profile succeeds and set that as `default_resolution` in the manifest. See `.claude/docs/on-device-debugging.md` § Resolution Search.
- `dspservice just died` → nearly always memory pressure; same fix path.
- Timeout → graph too large. Iterative structure (autoregressive decoding, refinement loops) → likely needs to be split into a `CollectionModel` (see `.claude/docs/collection-models.md`).

**Torch accuracy:**
- Way below reference → preprocessing is almost always the culprit. Verify resolution, normalization mean/std, channel order (RGB vs BGR), interpolation mode (bicubic vs bilinear) all match upstream. For timm-based models, `timm.data.resolve_data_config()` is ground truth.
- Slightly below → statistical noise on a 100-sample subset. Bump `--num-samples` to 500–1000 for a tighter check.

**On-device accuracy / PSNR at float:**
- Torch fine, device off → nearly always dtype / layout. QNN typically expects `NHWC` inputs when the model was authored `NCHW`. Check `get_input_spec()` and `forward()` for dtype coercion.
- Postprocessing diverging on device → some ops (softmax, argmax, NMS) run differently on device. Heavy postprocessing → move it out of the compiled graph into the App layer on CPU.
- **PSNR fine on one output, near-zero on another** → look at what that output *is* before touching the model. A logits tensor dominated by filtered-out low-confidence values legitimately scores badly; that is what `outputs_to_skip_validation` is for. An image or mask output scoring near zero is a real bug.
- **One runtime good, the other bad** → almost always layout or a CPU fallback. Compare the two profile jobs' per-op compute units: an op that lands on NPU under QNN and CPU under TFLite (or vice versa) is where the numbers diverge.

## Reporting

Report **every** runtime, always — a pass on one and a disable on the other is the normal outcome, and hiding either is what makes this skill untrustworthy.

```
Float on-device validation: PASS (tflite) / DISABLED (qnn_dlc)

Torch: <metric> on <n> samples (ref: <ref>)          # runtime-independent

tflite   PASS
- Compile:  <job_url>  (SUCCESS, <s>s)
- Profile:  <job_url>  (SUCCESS, <ms>ms, <MB> peak)
- Numerics: <metric> on <n> samples (Δ torch: <delta>)   | or: min PSNR <db> dB across <k> outputs

qnn_dlc  DISABLED -> manifest.yaml disabled_paths.float.qnn_dlc
- Compile: <job_url> FAILED — <error class, offending op>
- Hypothesis: <from the taxonomy> (not investigated)
- A fix would mean: <what it would take>
```

Say plainly which checks were skipped and why — "no evaluator wired, numerics checked by PSNR only". Never let a skipped check read as a passed one.

A disabled path is not a passed one either: if any runtime is disabled the headline says so, and if **every** runtime for `float` is disabled the whole run is `FAIL`, not a pass with caveats. Where nothing was debugged, say that rather than implying the path is dead.

## Non-goals

- **Not adding quantization.** `supported_precisions:` stays `[float]`.
- **Not authoring the recipe.** If the recipe isn't `validate`-green, hand off to `onboard`.
- **Not debugging unprompted.** The default output for a failure is a report, not a fix. Troubleshooting happens when the user asks for it.
- **Not tuning perf.** Once compile + profile succeed with reasonable numbers, ship it. Perf work is a separate project.
- **Not the on-target demo.** `has_on_target_demo` is `onboard`'s to set and nothing here exercises it. A demo that only breaks under `--eval-mode on-device` is a demo bug, not a recipe-on-device bug.
- **Not scorecarding.** In-tree recipes get scorecarded automatically by weekly CI (see `onboard-internal`); do not attempt to trigger it here. Writing a `scorecard_failure` into `disabled_paths` is not scorecarding — it's recording a failure you observed yourself, in the field scorecard will later clear.
- **Not the other runtimes.** `onnx`, `qnn_context_binary`, `precompiled_qnn_onnx`, and the Genie family are out of scope. `qnn_dlc` is the gate for the AOT family; the rest belong to whoever needs them.
