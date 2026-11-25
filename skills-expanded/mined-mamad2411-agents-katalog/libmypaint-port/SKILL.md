---
name: libmypaint-port
description: Port, review, or validate libmypaint 1.6.1 behavior in Rasterra's Rust brush engine and WESL pixel kernels. Use when inspecting vendored C code, changing the test-only C oracle or FFI wrapper, adding MyPaint fixtures, implementing brush settings, mappings, RNG, stroke state, dabs, smudge, or assessing CPU and GPU parity.
---

# Port libmypaint

Read `CONTRIBUTING.md`, `docs/plan.md`, and the relevant references in this skill before editing code.

## Workflow

1. Locate the behavior in `vendor/libmypaint` and update the entry in [the source map](references/source-map.md).
2. Add or select a focused fixture that exercises the behavior.
3. Capture the C oracle result before writing the Rust implementation.
4. Port the structure and formulas closely, preserving evaluation order and numeric types.
5. Compare the earliest observable boundary available: parsed settings, RNG values, mapping values, dab calls, color sampling, or raw pixels.
6. Add the mismatch as a permanent regression case.
7. Refactor only after the relevant parity layer passes.
8. For pixel-parallel behavior, establish Rust CPU parity first, then port it to WESL and compare actual GPU output with Rust.

## Invariants

- Pin compatibility to the vendored libmypaint 1.6.1 revision.
- Keep vendored C and all FFI out of production targets.
- Keep `tools/libmypaint-reference/CMakeLists.txt` aligned with upstream's
  `LIBMYPAINT_SOURCES`; write every configured or generated file outside the
  vendored subtree.
- Contain Rust unsafe code in the test oracle adapter and document each block with a `SAFETY` comment.
- Generate the raw test ABI from the Rasterra-owned wrapper header with a narrow bindgen allowlist; keep the safe adapter handwritten.
- Never edit vendored source casually. Put Rasterra behavior in the wrapper; document any unavoidable vendor patch.
- Never accept visual similarity as the sole compatibility criterion.
- Never update expected artifacts during an ordinary test run.
- Record upstream file and function names for non-obvious compatibility code.
- Separate parity changes from optimizations.

## Load references selectively

- Read [source-map.md](references/source-map.md) when choosing work or mapping C ownership to Rust and WESL.
- Read [parity-testing.md](references/parity-testing.md) when adding fixtures, comparisons, thresholds, or golden artifacts.
- Read [ffi-boundary.md](references/ffi-boundary.md) before changing the C wrapper, oracle executable, or Rust FFI adapter.
