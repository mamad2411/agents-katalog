---
name: python-rust-client-fallback-with-warning
description: Python package ships both a maturin-built Rust CLI and a pure-Python fallback CLI; runtime detects the Rust binary and falls back with a stderr warning if it's missing.
category: bindings
version: 1.0.0
version_origin: extracted
confidence: medium
tags: [magika, bindings]
source_type: extracted-from-git
source_url: https://github.com/google/magika.git
source_ref: main
source_commit: 0a8cb9626bbf76c2194117d9830b23e9052a1548
source_project: magika
imported_at: 2026-04-18T00:00:00Z
---

# Python Rust Client Fallback With Warning

**Trigger:** Distributing a Python package whose performance path depends on a native binary that may not be available on uncommon architectures.

## Steps

- Declare two console_scripts entry points: magika (Rust) and magika-python-client (pure Python).
- Detect the Rust binary at startup via shutil.which() or a sentinel import.
- If the Rust binary is missing, print a one-line stderr warning and dispatch to the Python implementation.
- Keep CLI flags and output format identical between the two; share an integration test suite.
- Document that the Rust binary is recommended; the Python fallback exists for unsupported wheels only.
- Wire MAGIKA_USE_PYTHON_CLIENT env var so users can force the fallback for debugging.

## Counter / Caveats

- Two implementations doubles your test surface; share a golden test suite to keep them aligned.
- Performance gap can be 10–100x; users on slow platforms may give up — make the warning actionable.
- Version skew between Rust binary and Python package is real; document compatibility ranges.
- Warnings can spook users; keep them brief and tell them exactly how to opt out.

## Source

Extracted from `magika` (https://github.com/google/magika.git @ main).

Files of interest:
- `python/src/magika/cli/magika_rust_client_not_found_warning.py:1-40`
- `python/src/magika/cli/magika_client.py:15-25`
- `python/pyproject.toml:72-78`
