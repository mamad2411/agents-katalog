# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this is

A WebGPU transformer inference engine that runs in the browser. WGSL kernels, no
runtime dependency. `src/` is the engine, `tests/` is the verification, `docs/`
explains the design.

## The rule that matters most

**A GPU kernel is not correct because it runs.** WebGPU reports a bad shader by
returning an *invalid pipeline* that silently computes zeros, and an invalid
buffer allocation the same way. Both produce plausible-looking output.

So: every kernel has a CPU reference in the same repository, and every change to
a kernel is accompanied by a parity number. If you cannot produce one, say so
rather than describing the change as done.

Real examples from this codebase:

- A fractional loop bound produced invalid WGSL that compiled to nothing. The
  mixture-of-experts output was completely wrong; relative error `1.0`. Nothing
  threw.
- A parity sweep passed at f32 while the real models use 4-bit K-quants,
  verifying a path that never executes.
- A prompt template rendered with the wrong JSON spacing, producing a byte
  sequence no model was trained on. Everything looked fine.

## Working style

**Ground claims in the artefact.** Read the actual model header, the actual
specification, the actual file. Several assumptions in this project's history
were confidently wrong and only a real file disproved them.

**Do not hardcode what the data already says.** Prompt format comes from the
model's chat template. Architecture support comes from the tensor inventory.
Both were once hardcoded and both were wrong for the majority of models.

**Report status precisely.** "Kernels verified, not wired" is useful. "Done" for
the same state is not. Partial work described accurately is worth more than
complete-sounding work that has not been checked.

**Fix the cause, not the symptom.** When a test fails, establish whether the
test or the code is wrong before changing either. Several test expectations in
this repository were wrong and the implementation was right.

## Verification commands

```bash
bun run typecheck
bun test
WGPU_LLM_TEST_MODELS=/path/to/models bun test    # model-dependent tests
bun run build
```

In-browser harnesses on `window.__wgpuLLM`: `parity`, `moeParity`,
`shortConvParity`, `profile`, `cpuProfile`, `health`. See
[docs/TESTING.md](docs/TESTING.md).

## Constraints

- No hardcoded filesystem paths anywhere, including tests.
- No new runtime dependencies. The browser bundle depends on nothing.
- Keep `bun run typecheck` clean.
- Comments explain why. Delete any comment whose removal would not confuse a
  reader.
