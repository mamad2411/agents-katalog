---
name: multi-backend-argparse-dispatcher
description: Single argparse CLI that dispatches to per-backend implementations (transformers / sglang / vllm / mlx) by required --backend choice, with post-parse cross-flag validation.
category: cli
version: 1.0.0
version_origin: extracted
tags: [argparse, cli, dispatch, multi-backend, validation]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/z-lab/dflash.git
source_ref: main
source_commit: 1fe684b00efba56490d920d15eeb9ba6e4471751
source_project: dflash
source_path: dflash/benchmark.py
imported_at: 2026-04-18T00:00:00Z
---

# Multi-Backend argparse Dispatcher

## When to use
- One CLI (`python -m pkg.benchmark ...`) needs to support several mutually-exclusive backends that each require their own Python deps.
- Some args are universal (`--model`, `--dataset`) and some only make sense for specific backends (`--draft-model` required for `transformers`/`mlx`; `--base-url` for server backends).
- You want a flat argparse surface (no subparsers) so `--help` stays readable and users can copy commands between backends.

## Pattern

```python
def main() -> None:
    p = argparse.ArgumentParser(description="DFlash benchmark")
    p.add_argument("--backend", choices=["transformers", "sglang", "vllm", "mlx"], required=True)
    p.add_argument("--model", type=str, required=True)
    p.add_argument("--dataset", type=str, required=True)
    p.add_argument("--max-new-tokens", type=int, default=2048)
    p.add_argument("--temperature", type=float, default=0.0)
    p.add_argument("--draft-model", type=str, default=None)    # only used by transformers/mlx
    p.add_argument("--base-url", type=str, default="http://127.0.0.1:30000")  # server only
    p.add_argument("--enable-thinking", action="store_true")
    # ... more shared / server-only args ...

    args = p.parse_args()

    # Post-parse cross-flag guards — errors read like argparse's own output.
    assert not (args.enable_thinking
                and any(x in args.model.lower() for x in ["qwen3-4b", "qwen3-8b"])), (
        "DFlash draft models for Qwen3-4B and Qwen3-8B were not trained with thinking traces."
    )

    if args.backend == "transformers":
        if args.draft_model is None:
            p.error("--draft-model is required for transformers backend")   # argparse-style error
        _run_transformers(args)
    elif args.backend == "mlx":
        if args.draft_model is None:
            p.error("--draft-model is required for mlx backend")
        _run_mlx(args)
    else:
        _run_server(args)   # sglang / vllm share a server path
```

## Why this shape, not subparsers
- You can swap backends in a long shell script by just changing one flag, keeping the rest of the command line identical.
- `p.error(...)` exits with code 2 and prints the usage — consistent with missing-arg errors.
- Conditional-required is resolved *after* parsing; argparse's own `required=True` would force `--draft-model` on backends that do not need it.

## Per-backend runner split
- `_run_transformers(args)` — imports torch / transformers inside the function. Users without those libs can still run `mlx` or `sglang`.
- `_run_mlx(args)` — imports `mlx_lm`.
- `_run_server(args)` — handles both `sglang` and `vllm` because they share "POST to a URL" semantics; inside, `is_vllm = args.backend == "vllm"` gates the two request shapes.

## Gotchas
- Do not import heavy deps (`torch`, `mlx`, `vllm`) at module top; keep them inside the runner functions so `--help` works on a minimal install.
- When flags are ambiguous across backends (e.g., `--block-size` means something different in MLX vs transformers), keep the name but document the backend-specific meaning in the help text.
