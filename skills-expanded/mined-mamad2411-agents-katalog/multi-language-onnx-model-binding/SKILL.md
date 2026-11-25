---
name: multi-language-onnx-model-binding
description: Expose one ONNX model across Rust (ort), Python (onnxruntime+maturin), JS (TensorFlow.js), and Go (CGO) bindings.
category: bindings
version: 1.0.0
version_origin: extracted
confidence: high
tags: [magika, bindings]
source_type: extracted-from-git
source_url: https://github.com/google/magika.git
source_ref: main
source_commit: 0a8cb9626bbf76c2194117d9830b23e9052a1548
source_project: magika
imported_at: 2026-04-18T00:00:00Z
---

# Multi Language Onnx Model Binding

**Trigger:** Building a portable ML inference library that must support multiple language ecosystems with consistent behavior.

## Steps

- Embed or reference ONNX model file in platform-native binaries (Rust: include_bytes!, Go: linked binary).
- Use each language's native runtime: Rust ort crate session builder, Python onnxruntime, JS TensorFlow.js, Go CGO to ONNX Runtime C API.
- Expose identical sync/async input abstraction (SyncInput / AsyncInput in Rust; file/bytes/stream in Python; loadUrl in JS).
- Coordinate model version across bindings via shared assets/models/ directory + semver tag.
- Generate per-language type stubs and content_type enums from a single config.min.json source of truth.
- Add cross-binding inference parity tests that pin reference outputs from one language and verify the others match.

## Counter / Caveats

- Version mismatch across bindings is fragile; requires coordinated cargo-dist + maturin + npm + Go module release pipeline.
- ONNX Runtime behavior differs subtly across platforms (GPU availability, threading semantics); test on every target OS.
- TensorFlow.js browser vs Node have different loading paths; detect environment and branch.
- Go via CGO requires the ONNX Runtime C library installed; consider vendoring or prebuilt binaries.

## Source

Extracted from `magika` (https://github.com/google/magika.git @ main).

Files of interest:
- `rust/lib/src/model.rs:23-31`
- `python/pyproject.toml:41-49`
- `js/src/model.ts:15-29`
- `go/onnx/onnx_runtime.go:1-25`
