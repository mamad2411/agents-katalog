---
name: soac-annotate
description: Profile a small Python code snippet with an example workload, collect post-opt-v3 BlockPy, specialized CLIF, and VCode views, annotate the requested view inline, and answer follow-up questions about generated blocks, guards, counters, helper calls, and optimization decisions.
---

# SOAC Annotate

Use this when the user gives Python source plus an example workload and asks to
annotate or explain the post-opt-v3 definition, specialized CLIF, or VCode.
Default to the post-opt-v3 BlockPy view unless the user asks for CLIF or VCode.

This workflow executes the workload. Treat the source as code the user intends
to run locally.

## Workflow

1. Run the bundled collector from the repo root, passing the source on stdin:

```bash
just py-fast .codex/skills/soac-annotate/scripts/profile_snippet_annotation.py \
  --workload '"add(1, 1)"' <<'PY'
def add(a, b):
    return a + b
PY
```

`just py-fast` forwards arguments through its shell recipe and falls back to the
full runtime setup when inputs are stale, so keep the extra inner quotes around
workloads containing parentheses or spaces.

If the workload call does not directly identify the function to inspect, pass
`--function <qualname>`.

Pass `--view clif` or `--view vcode` when the user explicitly asks for those
views. The default is `--view post-opt`.

2. Read the printed `annotation_context.md` path. It contains:

- original Python source
- workload and result repr
- module/function metadata
- optimizer v3 decision CLI output
- printed optimizer v3 plan
- decoded specialization counters
- post-opt-v3 BlockPy definition from `mod.optv3.blockpy`
- InstrTyped input to specialized codegen
- pre-inlining specialized CLIF, before runtime support CLIF inlining and
  Cranelift optimization
- specialized CLIF
- specialized VCode

3. Produce the annotated view in the answer:

- Return the requested view with comments, not a prose-only summary.
- Default to `post_opt_v3.blockpy.txt` when the user did not request a view.
- Use `pre_inline.clif` to explain semantically meaningful helper calls, because
  runtime support calls are still visible before inlining. Use
  `specialized.clif` for the final optimized block/control-flow shape.
- Use `specialized.vcode` when the user asks how Cranelift lowered the selected
  shape into machine-level VCode.
- Preserve original order and instructions as much as practical.
- Add a short comment before each block or definition explaining what it does.
- Add inline comments for guards, fast paths, slow paths, exception edges,
  direct indexed dict access, refcount cleanup, helper calls, and fallback
  calls when visible.
- Tie comments to Python source and counter evidence where possible.
- Mark uncertain block purposes as inferred.

4. For follow-up questions in the same conversation, reuse the artifact
directory from the prior run rather than reprofiling unless the source,
workload, counters, or requested function changed.

## Useful Artifacts

The script writes one directory under `work/logs/soac-annotations/`:

- `source.py`
- `workload.txt`
- `result_repr.txt`
- `counters/profile.bin`
- `specializations.txt`
- `optimization_decisions_v3.txt`
- `optimization_plan_v3.txt`
- `post_opt_v3.blockpy.txt`
- `instr_typed.txt`
- `pre_inline.clif`
- `specialized.clif`
- `specialized.vcode`
- `annotation_context.md`
- `metadata.json`
