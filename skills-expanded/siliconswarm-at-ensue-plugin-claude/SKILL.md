# autoresearch-ane-at-home

Rust bindings for Apple Neural Engine via reverse-engineered private API (`_ANEInMemoryModel`). Benchmarking direct ANE access vs Apple's CoreML on the same hardware.

## Quick start

```bash
claude --plugin-dir /path/to/autoresearch-ane-at-home-plugin
```

Then type `/autoresearch` to start the autonomous optimization loop. The agent handles setup, benchmarking, and optimization automatically.

To run manually:

```bash
make setup   # install Rust + Python deps, compile, download models, detect chip+RAM
make bench   # run ANE private API benchmark
```

## Benchmark

**Model:** DistilBERT (distilbert-base-uncased-finetuned-sst-2-english), sequence length 128, batch size 1.

**Metric:** median end-to-end inference latency (embedding + transformer layers + classifier). Lower is better.

**CoreML baseline** uses Apple's open-sourced [ml-ane-transformers](https://github.com/apple/ml-ane-transformers) model (`apple/ane-distilbert-base-uncased-finetuned-sst-2-english`). This is not a vanilla DistilBERT — Apple restructured the architecture for ANE: channel-last layouts, linear layers replaced with 1x1 convolutions, large matmuls split into ANE-friendly sizes. CoreML runs with `ComputeUnit.ALL` and may split work across ANE/GPU/CPU.

**ANE private API** uses the original HuggingFace DistilBERT weights with a vanilla transformer architecture, compiled and executed directly on ANE via `_ANEInMemoryModel`.

Both benchmarks use identical methodology: 50 warmup iterations, 1000 timed iterations, same statistics (median/mean/p5/p95/min). Both include embedding in the timed region.

```bash
make bench-coreml   # Apple's ANE-optimized CoreML model
make bench          # private ANE API
```

## Architecture

The `ane` crate (`ane_kernel/crates/ane/`) wraps Apple's private `AppleNeuralEngine.framework`:
- **Graph API** — build computation graphs with `inner_product`, `matrix_multiplication`, activations, reductions, etc.
- **Compile** — `graph.compile()` produces an `Executable` via `_ANEInMemoryModel`
- **Run** — `executable.run()` executes on ANE with IOSurface zero-copy I/O

### Key files

| File | What |
|------|------|
| `ane_kernel/crates/ane/src/graph/ops.rs` | All ANE graph operations |
| `ane_kernel/crates/ane/src/executable.rs` | Compile & run lifecycle |
| `ane_kernel/crates/ane/src/graph/compile.rs` | Graph → MIL → ANE machine code |
| `ane_kernel/crates/ane/src/coreml.rs` | CoreML bindings for comparison |
| `ane_kernel/crates/ane/examples/distilbert_model.rs` | DistilBERT kernel (the file agents optimize) |
| `ane_kernel/crates/ane/examples/distilbert_bench.rs` | Inference benchmark |
| `ane_kernel/crates/ane/examples/distilbert_verify.rs` | Accuracy verification (SST-2) |

## ANE private API ops

`inner_product`, `matrix_multiplication`, `convolution_2d`, `convolution_transpose_2d`, `relu`, `tanh`, `sigmoid`, `leaky_relu`, `elu`, `hard_sigmoid`, `softplus`, `softsign`, `addition`, `subtraction`, `multiplication`, `division`, `power`, `maximum`, `minimum`, `absolute`, `square_root`, `reciprocal_square_root`, `exponent`, `logarithm`, `reciprocal`, `soft_max`, `instance_norm`, `reduce_sum`, `reduce_mean`, `reduce_min`, `reduce_max`, `concat`, `slice`, `reshape`, `transpose`, `flatten_2d`, `pad`, `max_pool`, `avg_pool`, `global_avg_pool`

## Prerequisites

- macOS on Apple Silicon (M1/M2/M3/M4)
- Xcode Command Line Tools (`xcode-select --install`)

`make setup` handles the rest (Rust, Python packages, model downloads).

## Authors
- [svv232](https://github.com/svv232)

## License

MIT
