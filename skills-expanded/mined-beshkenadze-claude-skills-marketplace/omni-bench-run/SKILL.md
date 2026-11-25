---
name: omni-bench-run
description: Run a model through the omni-bench benchmark to MEASURE it — produce a run-artifact and score it, then read the numbers. Use when asked to run, benchmark, measure, evaluate, or "test the results of" a model with omni-bench — ASR (WER/CER, RTFx) or text generation (tok/s, TTFT, prefill tok/s, prompt-cache speedup). Covers the adapter seam (Transcriber/Generator), the prepare→run→score→diff CLI flow, the offline no-download smoke task, and how to interpret each metric. NOT for publishing to a leaderboard (use omni-bench-publish) or changing the framework itself (use omni-bench).
version: 1.0.0
---

# Running omni-bench to measure a model

omni-bench measures **quality + speed tied to specific hardware** (ASR: WER/CER + RTFx;
text generation: tok/s, TTFT/prefill, prompt-cache benefit). It is a **framework, not a
runner**: YOU provide inference through a small adapter seam; omni-bench owns the datasets,
the scoring, and the metrics. Scoring lives in **one** place (the Python scorer) so numbers
are comparable across languages/backends — **never reimplement scoring in your host**.

Full producer guide (Python + Swift, copy-paste): **`omni-bench/docs/integration.md`**.

## The seam — plug in your model

Implement one structural contract (no inheritance; Swift mirrors Python 1:1):
- **ASR**: `Transcriber.transcribe(audio, language, task) -> Transcript` (`text` + optional
  `backend_native.decode_s`, `peak_mem_gb`).
- **Text generation**: `Generator.generate(prompt, task) -> Generation` + `reset_cache()`.
  The seam is non-streaming, so **all** latency/token metrics are **host-reported** via
  `backend_native`: `ttft_s`, `prefill_s`, `prompt_tokens`, `generated_tokens`,
  `reused_tokens`, `cache_hit`, `decode_s`, `peak_mem_gb`. The scorer derives the rates —
  emit raw counts/times, don't compute tok/s yourself.

## The flow

```bash
omni-bench prepare <task_id>                 # materialize dataset → data/<task_id>/{manifest.json, references.jsonl}
omni-bench run --adapter pkg.mod:factory \   # YOUR host over the manifest → run-artifact.jsonl
    --manifest data/<task_id>/manifest.json --out runs/x.jsonl
omni-bench score --artifact runs/x.jsonl \   # centralized scorer → result.json (the numbers)
    --references data/<task_id>/references.jsonl --out runs/x.result.json
omni-bench diff  --result-a … --artifact-a … --result-b … --artifact-b … --out p.json  # optional: parity of two runs
```
`--adapter` is a dotted path `module:factory`; `factory()` returns
`(Transcriber|Generator, model, backend)` — `model`/`backend` are host-declared identity
(base_model_id, artifact_id, sha256, quantization; backend id + build_sha). omni-bench and
your model package must import in the **same** interpreter (`uv pip install -e omni-bench/python`
into your env, or set `PYTHONPATH`). Swift hosts call `Producer.run(transcriber:/generator: …)`.

## Offline smoke (no downloads)

`textgen.shared_prefix.en.v1` is fully synthetic (4 groups × 3 prompts, shared ~1k-word
prefix) — the only downloads-free task; ASR tasks hit HuggingFace. For a pipeline-only smoke
(no real model) point `--adapter` at a fake Generator returning fixed text + plausible timings;
to benchmark a **real** model, wrap its inference in the seam.

## Read the numbers (`result.json` → `rows[0]`)

- **ASR row**: `quality{wer_norm, wer_ortho, cer}` (lower better), `speed{rtfx_native,
  rtfx_wall, peak_mem_gb}`. `rtfx_native` (from `decode_s`) is cross-implementation
  comparable; `rtfx_wall` is harness-scoped (rendered distinct). `quality: null` ⇒ no sample
  transcribed (a failed run, not a perfect one).
- **Text-generation row**: `main_score: "tok_per_s"`; `speed{tok_per_s, prefill_tok_per_s,
  ttft_s_p50, prefill_s_p50, peak_mem_gb}`; `cache{cold, warm, ttft_speedup,
  reused_tokens_mean, cache_hit_rate}|null`; `quality{exact_match}|null` (null when the task
  ships no references — the synthetic scenario does).
  - `prefill_tok_per_s` = cache-free prompt-processing rate (cold samples only in the
    shared-prefix scenario; the llama-bench `pp` equivalent).
  - `ttft_speedup` = `cold.ttft_s_p50 / warm.ttft_s_p50` (> 1 ⇒ the prompt cache helped) —
    the canonical single-number cache benefit. Nothing is discarded as warmup; cold is the baseline.
- Sanity: `counts{n_ok, n_error, n_timed}` — a run with `n_error > 0` had per-sample failures
  (the producer records them and never aborts).

## Rules that keep results honest

- **Never reimplement scoring** in the host — emit hypotheses/generations + raw counts, let the
  one Python scorer grade them (this is the whole point: no measurer drift).
- **Declare hardware honestly** — `hardware{soc, mem_gb}` keys the identity and speed is
  hardware-scoped; off macOS the collector can't see the accelerator, so pass it explicitly.
- **Deterministic** — greedy/temperature 0/seed pinned; `prepare` twice ⇒ identical hashes.

## Next / related

- **Share the numbers on a leaderboard** → the `omni-bench-publish` skill (`omni-bench publish`,
  api-key injected from a secrets manager).
- **Change the framework** (schemas, scorer, seams, datasets) → the `omni-bench` skill.
- `just`/`uv` may live outside the default PATH (e.g. `/opt/homebrew/bin`).
