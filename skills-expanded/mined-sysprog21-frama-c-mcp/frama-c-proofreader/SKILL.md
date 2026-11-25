---
name: frama-c-proofreader
description: Verify and proofread C code with ACSL using this repository's Frama-C MCP workflow, Frama-C WP static proof, EVA alarms, and optional E-ACSL runtime checks. Use when asked to run Frama-C, check ACSL contracts, explain WP goals, inspect EVA alarms, validate C annotations, or state what a C proof does and does not establish.
---

# Frama-C Proofreader

## Workflow

Prefer the MCP server when it is available. Start with the install check and the shortest useful call:

```text
self_check {}
reload_project {files, rte: true}
check {function?, timeout?}
```

If `check` reports alarms or non-valid goals, inspect the concrete payload before changing code:

```text
get_wp_goals {want: ["alarms"], function?, status?}
get_wp_goals {want: ["investigation"], marker, depth}
get_wp_goals {function, status?}
context {function, want: ["current_annotations", "function_ast"]}
```

`investigation` takes the property marker off an alarm or goal row. A `check`
payload is not proved while `incomplete[]` has any entry; read each entry's
guidance before treating a valid goal as evidence.

Validate candidate ACSL with dry-run injection first:

```text
inject_all_annotations {function, dry_run: true, annotations: [{kind, acsl, ...}]}
inject_all_annotations {function, annotations: [{kind, acsl, ...}]}
run_wp {functions: [function]}
```

Use `run_e_acsl` only as runtime evidence for concrete executions. If it is unavailable or fails to compile instrumentation, report that runtime checking was unavailable.

Read `references/mcp-workflow.md` for the full MCP call order, `references/wp-output.md` when interpreting WP goals, and `references/e-acsl-output.md` before making runtime-check claims.

## Reporting

Always separate these outcomes:

- Environment failure: tool missing, prover not configured, instrumentation failed.
- Static proof gap: WP did not prove a goal; this is not automatically a bug.
- Runtime violation: E-ACSL found a violation on an executed path.
- Proven under assumptions: WP proved the generated goals for the ACSL and RTE configuration that actually ran.

Do not claim proof without tool output. Report exact goal names, proof counts, and whether `rte: true` or `-wp-rte` was used.

Before calling a function verified, run `check {files, smoke: true}` and confirm there is no `SMOKE_TEST_FAILED`: a contradictory `requires` or dead code makes every goal in scope provable, and only smoke tests notice.

## Boundaries

WP proves obligations generated from the C program and ACSL. It does not prove requirements that were omitted from the specification.

EVA alarms and WP goals are complementary. A clean WP result does not replace checking missing frame conditions or assumed callee contracts.

E-ACSL checks only executed paths and inputs. Passing one run is evidence, not exhaustive proof.
