---
name: cursor-principle-explain-the-number
description: "Apply before you measure, and before you trust, report, or act on a number you measured: a speedup, a regression, a throughput, a latency, or an eval result. Find what limits it, and rule out that it measured something other than the work you think."
disable-model-invocation: true
---

## Runtime selection

Before runtime-dependent work, read [execution selection](references/runtime/selection.md). In a verified T3 host follow [the T3 contract](references/runtime/t3.md) and its method reference; the inline section below is the native Codex branch, not literal T3 dispatch. Outside T3, native Codex follows that inline branch unchanged. If the host is ambiguous or a required capability is unavailable, report the gap; a permission refusal never authorizes switching branches.

## Native Codex branch

# Explain the Number

- **Write the decision before you run.** Name the result that would change it, and the noise floor. Stop when the run-to-run spread is larger than the effect.
- **Ask "why not double?"** Name the resource or code path that bounds the result, from a profile or counters taken during a run. A guess from reading the code is not a limiter.
- **List what else the number could be measuring** (errors, skipped or cached work, code that never ran, an untuned side, noise, a piece too small to matter) and rule out each one with evidence.
- **Keep the run count, the spread, and the limiter with the number.**

For a performance number, run the [benchmark-checklist](../cursor-benchmark-checklist/SKILL.md) skill. For an eval result, ask whether every run did the task, whether the gap holds across trials and models, and whether the scenario matters.
