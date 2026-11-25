---
name: qwen-mtp-gguf
description: Complete agent-ready workflow for Qwen-family MTP or nextn GGUF conversion and release. Use when Codex or another coding agent needs to inspect a user's machine, estimate disk/RAM requirements from Hugging Face model sizes and requested quant formats, bootstrap llama.cpp and Python dependencies, extract MTP heads from a matching official/base Qwen model, merge them into a fine-tuned or target safetensors model, run local HF/GGUF smoke tests with Qwen chat formatting, quantize to GGUF, and optionally upload or resume Hugging Face releases.
---

# Qwen MTP GGUF

## Operating Principle

Run this as a staged release pipeline, not a blind conversion:

1. Identify the target model and matching MTP source model.
2. Preflight the environment, disk, RAM, tools, token access, and config compatibility.
3. Ask the user to choose upload strategy when it affects disk use.
4. Prepare the target HF directory and inject only missing MTP/nextn tensors.
5. Convert to a temporary F16 GGUF, smoke-test locally, then quantize.
6. Upload with resume support, or keep local artifacts if the user chooses local-only.

MTP/GGUF conversion and llama.cpp quantization do not require a GPU. GPU acceleration can make later inference tests faster, but the default smoke test should use CPU mode (`-ngl 0`) so it works on common machines.

## Required User Inputs

Ask for missing items only when they cannot be inferred safely:

- Target model: HF repo ID or local HF model directory.
- Matching MTP source model: the official/base Qwen-family repo with the same architecture, size, tokenizer, and MTP layout.
- Output mode: local-only, stream upload, or batch upload.
- Output repo ID when uploading.
- Quantization formats. Default full matrix: `q2_k,q3_k_s,q3_k_m,q3_k_l,iq4_xs,q4_k_s,q4_k_m,q5_k_s,q5_k_m,q6_k,q8_0,bf16`.

If the target and MTP source configs disagree on core architecture fields, stop and ask before continuing.

## Upload Strategy Choice

When the user has not specified a strategy, explain the tradeoff briefly and ask:

- `stream`: quantize one GGUF, upload it, then delete it. Lowest peak disk use and best default for large models.
- `batch`: quantize everything first, then upload. Useful when network is unstable but requires much more disk.
- `local-only`: prepare all GGUF files locally without uploading.

Use `stream` when the user asks for a full large-model release and does not care about keeping local copies.

## Environment Bootstrap

Use `scripts/bootstrap_qwen_mtp_env.sh` when llama.cpp or Python dependencies are missing.

```bash
bash scripts/bootstrap_qwen_mtp_env.sh --prefix ./qwen-mtp-env --backend cpu
source ./qwen-mtp-env/.venv/bin/activate
```

Backend options are `cpu`, `cuda`, `metal`, and `vulkan`. Prefer `cpu` unless the user explicitly wants accelerated smoke tests or already has a configured GPU toolchain.

## Preflight

Always run preflight before downloading large model weights:

```bash
python3 scripts/qwen_mtp_gguf_pipeline.py \
  --source-repo owner/target-qwen-finetune \
  --mtp-source-repo owner/matching-base-qwen-with-mtp \
  --output-repo owner/target-qwen-mtp-gguf \
  --work-root ./mtp-gguf-work \
  --llama-cpp ./qwen-mtp-env/llama.cpp \
  --token-env HF_TOKEN \
  --upload-strategy stream \
  --preflight-only
```

Review `preflight_report.md` before running. It reports:

- OS, CPU cores, total RAM, detected GPU hint, Python version.
- Required commands and packages.
- llama.cpp converter, quantizer, and `llama-cli` status.
- Target model size from HF file metadata or local files.
- Minimal MTP shard download size.
- Estimated F16/BF16 and quantized GGUF sizes.
- Required free disk with a safety factor.
- Recommended RAM and config mismatch warnings.

## Full Pipeline

```bash
python3 scripts/qwen_mtp_gguf_pipeline.py \
  --source-repo owner/target-qwen-finetune \
  --mtp-source-repo owner/matching-base-qwen-with-mtp \
  --output-repo owner/target-qwen-mtp-gguf \
  --work-root ./mtp-gguf-work \
  --llama-cpp ./qwen-mtp-env/llama.cpp \
  --filename-prefix target-qwen-MTP \
  --token-env HF_TOKEN \
  --upload-strategy stream \
  --private \
  --smoke-test-before-upload \
  --cleanup-after-upload
```

The pipeline:

- Downloads or copies the target HF model.
- Detects existing MTP/nextn tensors and validates index mappings.
- Downloads only the MTP source shards listed in the source index.
- Saves `mtp_heads.safetensors`, updates `model.safetensors.index.json`, and validates all new keys.
- Converts F16 for quantization and BF16 directly from the prepared HF directory.
- Runs GGUF smoke tests before upload when enabled. Prefer the model's embedded chat template when llama.cpp supports it; use ChatML only as a minimal fallback for load/generation sanity checks.
- Lists remote HF files before upload and skips completed GGUFs on resume.
- Deletes local GGUF files only after confirmed upload when cleanup is enabled.

## Smoke Tests

Use the GGUF smoke test for release validation:

```bash
python3 scripts/qwen_gguf_smoke_test.py \
  --model ./mtp-gguf-work/target-qwen-MTP-GGUF/target-qwen-MTP-Q8_0.gguf \
  --llama-cli ./qwen-mtp-env/llama.cpp/build/bin/llama-cli \
  --prompt "State the capital of France in one short sentence." \
  --gpu-layers 0
```

Use the HF smoke test only when the machine can load the HF model:

```bash
python3 scripts/qwen_hf_smoke_test.py \
  --model ./mtp-gguf-work/target-qwen-MTP-HF \
  --prompt "Write one concise sentence about MTP inference."
```

For Qwen-family chat formatting, use `apply_chat_template(..., add_generation_prompt=True, tokenize=False)` on the HF side. For GGUF, prefer the chat template embedded by llama.cpp conversion or copied from `tokenizer_config.json`; use raw ChatML only as a fallback smoke test, not as the quality/reasoning benchmark template.

## Agent Compatibility

This skill is Codex-native, but the workflow is intentionally agent-agnostic:

- Claude Code, Codex, OpenCode, Qwen Code, Hermes, and similar agents can run the same scripts from a shell.
- The agent should call `--preflight-only`, summarize blockers, ask for the upload strategy if needed, then run the full command.
- Keep user-specific tokens, paths, private repo names, and logs out of public PRs and model cards.

## References

- Read `references/environment-and-sizing.md` before changing preflight logic or resource thresholds.
- Read `references/technical-flow.md` before changing extraction, injection, conversion, or upload behavior.
- Read `references/agent-integration.md` when packaging this for another agent framework.
- Read `references/troubleshooting.md` when conversion, tensor lookup, disk, RAM, or upload steps fail.
