---
name: lang-dart
description: Dart sound null safety, strict analyzer options, stream subscription hygiene, and compute/isolate isolation.
---

# Dart Sound Null-Safety Contract

## 1. Strict Analyzer Options
- Configure `analysis_options.yaml` with `strict-casts: true`, `strict-inference: true`, and `strict-raw-types: true`.
- Zero `as dynamic` or untyped dynamic invocation.

## 2. Resource & Stream Discipline
- All `StreamSubscription` objects must be canceled in `dispose()` lifecycle hooks.
- Offload heavy computation to `Isolate.run()`.
