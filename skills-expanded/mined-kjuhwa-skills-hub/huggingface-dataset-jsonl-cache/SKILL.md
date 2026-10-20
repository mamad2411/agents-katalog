---
name: huggingface-dataset-jsonl-cache
description: Convert HuggingFace datasets to a flat JSONL cache with atomic tmp-file rename, so benchmark scripts load deterministically without re-downloading.
category: data-pipeline
version: 1.0.0
version_origin: extracted
tags: [huggingface, datasets, jsonl, caching, benchmark]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/z-lab/dflash.git
source_ref: main
source_commit: 1fe684b00efba56490d920d15eeb9ba6e4471751
source_project: dflash
source_path: dflash/benchmark.py
imported_at: 2026-04-18T00:00:00Z
---

# HF Dataset → JSONL Cache (Atomic)

## When to use
- You run the same benchmark many times over gsm8k / mbpp / humaneval / math500 / mt-bench style datasets and want to decouple the benchmark from HF networking.
- You need a single flat format (one JSON object per line with a `turns: [...]` field) so single-turn and multi-turn datasets can share the same loader.
- Concurrent benchmark processes may race to populate the cache — you need the final file to be either absent or complete, never half-written.

## Pattern

```python
CACHE_DIR = Path(__file__).parent.parent / "cache"

DATASETS = {
    "gsm8k": {
        "load_args": ("openai/gsm8k", "main"),
        "load_kwargs": {"split": "test"},
        "format": lambda x: "{question}\nPlease reason step by step, and put your final answer within \\boxed{{}}.".format(**x),
    },
    "mt-bench": {
        "load_args": ("HuggingFaceH4/mt_bench_prompts",),
        "load_kwargs": {"split": "train"},
        "format": lambda x: x["prompt"],      # already a list of turns
        "multi_turn": True,
    },
    ...
}

def _prepare_dataset(name: str) -> Path:
    from datasets import load_dataset
    cfg = DATASETS[name]
    CACHE_DIR.mkdir(exist_ok=True)
    out_path = CACHE_DIR / f"{name}.jsonl"
    tmp_path = out_path.with_name(f"{out_path.name}.{os.getpid()}.tmp")

    ds = load_dataset(*cfg["load_args"], **cfg["load_kwargs"])
    with open(tmp_path, "w") as f:
        for row in ds:
            turns = cfg["format"](row) if cfg.get("multi_turn") else [cfg["format"](row)]
            f.write(json.dumps({"turns": turns}) + "\n")
    os.replace(tmp_path, out_path)            # atomic rename
    return out_path


def load_and_process_dataset(name: str) -> list[dict]:
    if name not in DATASETS:
        raise ValueError(f"Unknown dataset '{name}'. Available: {list(DATASETS)}")
    path = CACHE_DIR / f"{name}.jsonl"
    if not path.exists():
        _prepare_dataset(name)
    with open(path) as f:
        return [json.loads(line) for line in f]
```

## Why this shape
- One object per line → you can `head -n 100 cache/gsm8k.jsonl` to spot-check without a JSON parser.
- Every dataset exposes a `turns` list so the benchmark loop treats single-turn and multi-turn uniformly.
- `os.replace(tmp, out)` is atomic on both POSIX and Windows; readers see either the old file or the new file, never a truncation.
- `tmp_path` includes `os.getpid()` so two concurrent writers don't clobber each other's tmp files.

## Gotchas
- `cache/` sits at repo root — add it to `.gitignore`; HF datasets are not redistributable.
- No file-level lock: two processes may both re-download if they find the cache missing at the same moment. Acceptable for benchmarks; not for production ingest.
- `cfg["format"]` is a lambda — keep it pickle-free (do not pass across processes).
