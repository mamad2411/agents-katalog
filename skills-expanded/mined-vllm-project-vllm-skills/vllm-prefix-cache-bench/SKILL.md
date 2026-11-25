---
name: vllm-prefix-cache-bench
description: This is a skill for benchmarking the efficiency of automatic prefix caching in vLLM using fixed prompts, real-world datasets, or synthetic prefix/suffix patterns. Use when the user asks to benchmark prefix caching hit rate, caching efficiency, or repeated-prompt performance in vLLM.
---

# vLLM Prefix Caching Benchmark

Benchmark the efficiency of vLLM's automatic prefix caching (APC) feature. The offline script `benchmarks/benchmark_prefix_caching.py` runs directly against the vLLM engine (no server required). For online/serving tests, use `vllm bench serve` with the `prefix_repetition` dataset.

## When to use

- User wants to measure the performance impact of prefix caching for repeated or partially-shared prompts.
- User wants to compare throughput/latency with and without `--enable-prefix-caching`.
- User wants to test prefix caching using a fixed synthetic prompt, a real dataset (e.g. ShareGPT), or a synthetic prefix/suffix repetition pattern.

## Option 1 (default). Fixed Prompt with Prefix Caching

Runs a synthetic benchmark with a fixed prompt repeated multiple times to directly measure cache hit efficiency. No dataset download required.

```bash
python3 benchmarks/benchmark_prefix_caching.py \
  --model Qwen/Qwen3-8B \
  --enable-prefix-caching \
  --num-prompts 1 \
  --repeat-count 100 \
  --input-length-range 128:256
```

To compare against the baseline without caching:

```bash
python3 benchmarks/benchmark_prefix_caching.py \
  --model Qwen/Qwen3-8B \
  --no-enable-prefix-caching \
  --num-prompts 1 \
  --repeat-count 100 \
  --input-length-range 128:256
```

## Option 2. ShareGPT Dataset with Prefix Caching

Uses real-world conversational data from ShareGPT to evaluate prefix caching with naturally occurring prompt sharing.

First, download the dataset:

```bash
wget https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/resolve/main/ShareGPT_V3_unfiltered_cleaned_split.json
```

Then run the benchmark:

```bash
python3 benchmarks/benchmark_prefix_caching.py \
  --model Qwen/Qwen3-8B \
  --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json \
  --enable-prefix-caching \
  --num-prompts 20 \
  --repeat-count 5 \
  --input-length-range 128:256
```

## Option 3. Prefix Repetition Dataset (Online)

Uses `vllm bench serve` with the synthetic `prefix_repetition` dataset to test caching via the serving API. This requires a running vLLM server.

First, start the server:

```bash
vllm serve Qwen/Qwen3-8B
```

Then run the benchmark:

```bash
vllm bench serve \
  --backend openai \
  --model Qwen/Qwen3-8B \
  --dataset-name prefix_repetition \
  --num-prompts 100 \
  --prefix-repetition-prefix-len 512 \
  --prefix-repetition-suffix-len 128 \
  --prefix-repetition-num-prefixes 5 \
  --prefix-repetition-output-len 128
```

Key parameters for `prefix_repetition`:

| Parameter | Description |
|---|---|
| `--prefix-repetition-prefix-len` | Number of tokens in the shared prefix portion |
| `--prefix-repetition-suffix-len` | Number of tokens in the unique suffix portion |
| `--prefix-repetition-num-prefixes` | Number of distinct prefixes to cycle through |
| `--prefix-repetition-output-len` | Number of output tokens to generate per request |

## Notes

- Run all commands from the root of the vLLM repository (`cd vllm`).
- Keep the default model (`Qwen/Qwen3-8B`) unless the user specifies a different one or the model is unavailable; change only `--model`.
- `--repeat-count` in Option 1 and 2 controls how many times each sampled prompt is replayed; higher values increase cache hit rate.
- `--input-length-range` accepts a `min:max` token range, e.g. `128:256`.
- For multi-GPU setups, add `--tensor-parallel-size <N>`.
- To test different hash algorithms for prefix caching internals, use `--prefix-caching-hash-algo xxhash` (requires `pip install xxhash`).

## Arguments for `benchmark_prefix_caching.py`

| Argument | Required | Description |
|---|---|---|
| `--model` | Yes | Model name or path (HuggingFace ID or local path) |
| `--num-prompts` | Yes | Number of prompts to process |
| `--input-length-range` | Yes | Token length range for inputs, e.g. `128:256` |
| `--repeat-count` | No | Number of times each prompt is repeated (default: 1) |
| `--dataset-path` | No | Path to a dataset file (e.g. ShareGPT JSON). Omit for synthetic fixed-prompt mode |
| `--prefix-len` | No | Fixed prefix token length to prepend to every prompt |
| `--output-len` | No | Number of output tokens to generate per request |
| `--sort` | No | Sort prompts by length before benchmarking |
| `--enable-prefix-caching` / `--no-enable-prefix-caching` | No | Toggle APC (recommended: enable to test caching) |
| `--prefix-caching-hash-algo` | No | Hash algorithm: `sha256`, `sha256_cbor`, `xxhash`, `xxhash_cbor` |
| `--tensor-parallel-size` | No | Number of GPUs for tensor parallelism |
| `--disable-detokenize` | No | Skip detokenization to reduce overhead |

## Troubleshooting

- If `python3 benchmarks/*.py` reports file not found, locate your local vLLM repository first and run the command from that repo root.
- If you do not have the repository yet, clone it and continue:

```bash
git clone https://github.com/vllm-project/vllm
cd vllm
```

- If HuggingFace model download fails due to access restrictions, set your token: `export HF_TOKEN=<your_token>` or pass `--hf-token <your_token>`.
- If `xxhash` or `cbor2` is not installed and you use those hash algorithms, install them first: `pip install xxhash cbor2`.
