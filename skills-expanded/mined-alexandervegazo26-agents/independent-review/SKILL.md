---
name: independent-review
description: "Review a change through four independent evidentiary bases in parallel, adversarially cross-check every finding, then merge into one ranked report. Usage: /independent-review <branch, path list, or \"working tree\">"
---

<!-- GENERATED from sdlc-suite/commands/independent-review.md — do not edit. Run python sdlc-suite/tools/generate_trees.py -->

`<the User instruction>` below is the text that followed `/independent-review`, shown as the `User instruction:` line of this message. If there is none, ask for it rather than guessing.

> **Hermes.** This command invokes the `Workflow` tool, which under Hermes
> is the `workflow` tool registered by the `.hermes/plugins/sdlc/` plugin.
> Call it with the `scriptPath` and the `args` OBJECT below — an object,
> never a bare string — and report the pipeline's result, not a substitute.
> If the `workflow` tool is not available in this session (the plugin is
> not enabled), say so to the user; do not improvise a substitute run, and
> do not report a result this pipeline did not produce.

Invoke the `Workflow` tool with:

```
scriptPath: "sdlc-suite/workflows/independent-review.js"
args: { "target": "<the User instruction>", "runtimeDir": "sdlc-suite/workflows", "policyDefault": "sdlc-suite/autonomy.json" }
```

If no target was given, pass `"the current working tree"`. Report surviving findings ranked by blast radius, and state how many were refuted.

Pass `args` as the literal OBJECT above, never a bare string. `runtimeDir` is what lets the workflow reach its run recorder, retry breaker, learnings loader and policy loader; a string `args` carries none of it, and the run then records nothing and learns nothing — the workflow reports that as status `incomplete` with a `runtime.unreachable` blocked gate, never as `completed`. `policyDefault` is the plugin's shipped policy, a fallback: a repo's own `.claude/autonomy.json` overrides it. To make a run stricter than the repo allows, also pass `policy`: an explicit policy is INTERSECTED with the repo's (a gate is authorized only if both authorize it), so it can tighten a repo's policy and never loosen it.

Autonomy: this run is unattended unless the user is clearly present. Gates not pre-authorized by the resolved policy are recorded as BLOCKED rather than halting the run.
