---
name: system-archaeology
description: "Reverse-engineer an undocumented system — derive who uses it and what it does in parallel, cross-check, and synthesize an as-built PRD. Usage: /system-archaeology <scope, e.g. a path or \"the whole application\">"
---

<!-- GENERATED from sdlc-suite/commands/system-archaeology.md — do not edit. Run python sdlc-suite/tools/generate_trees.py -->

`<the User instruction>` below is the text that followed `/system-archaeology`, shown as the `User instruction:` line of this message. If there is none, ask for it rather than guessing.

> **Hermes.** This command invokes the `Workflow` tool, which under Hermes
> is the `workflow` tool registered by the `.hermes/plugins/sdlc/` plugin.
> Call it with the `scriptPath` and the `args` OBJECT below — an object,
> never a bare string — and report the pipeline's result, not a substitute.
> If the `workflow` tool is not available in this session (the plugin is
> not enabled), say so to the user; do not improvise a substitute run, and
> do not report a result this pipeline did not produce.

Invoke the `Workflow` tool with:

```
scriptPath: "sdlc-suite/workflows/system-archaeology.js"
args: { "scope": "<the User instruction>", "runtimeDir": "sdlc-suite/workflows", "policyDefault": "sdlc-suite/autonomy.json" }
```

Output is evidence, never a recommendation about what to change.

Pass `args` as the literal OBJECT above, never a bare string. `runtimeDir` is what lets the workflow reach its run recorder, retry breaker, learnings loader and policy loader; a string `args` carries none of it, and the run then records nothing and learns nothing — the workflow reports that as status `incomplete` with a `runtime.unreachable` blocked gate, never as `completed`. `policyDefault` is the plugin's shipped policy, a fallback: a repo's own `.claude/autonomy.json` overrides it. To make a run stricter than the repo allows, also pass `policy`: an explicit policy is INTERSECTED with the repo's (a gate is authorized only if both authorize it), so it can tighten a repo's policy and never loosen it.

Autonomy: this run is unattended unless the user is clearly present. Gates not pre-authorized by the resolved policy are recorded as BLOCKED rather than halting the run.
