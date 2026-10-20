---
name: persona-qa-sweep
description: "Derive real end-user personas from code evidence, explore the app as each, then probe authorization boundaries between every persona pair. Usage: /persona-qa-sweep <target URL> [env]"
---

<!-- GENERATED from sdlc-suite/commands/persona-qa-sweep.md — do not edit. Run python sdlc-suite/tools/generate_trees.py -->

`<the User instruction>` below is the text that followed `/persona-qa-sweep`, shown as the `User instruction:` line of this message. If there is none, ask for it rather than guessing.

> **Hermes.** This command invokes the `Workflow` tool, which under Hermes
> is the `workflow` tool registered by the `.hermes/plugins/sdlc/` plugin.
> Call it with the `scriptPath` and the `args` OBJECT below — an object,
> never a bare string — and report the pipeline's result, not a substitute.
> If the `workflow` tool is not available in this session (the plugin is
> not enabled), say so to the user; do not improvise a substitute run, and
> do not report a result this pipeline did not produce.

Invoke the `Workflow` tool with:

```
scriptPath: "sdlc-suite/workflows/persona-qa-sweep.js"
args: { "target": "<target from <the User instruction>>", "env": "<env, default non-production>", "runtimeDir": "sdlc-suite/workflows", "policyDefault": "sdlc-suite/autonomy.json" }
```

Never point this at production. If `<the User instruction>` names a production host or no target at all, stop and say so instead of running.

Pass `args` as the literal OBJECT above, never a bare string. `runtimeDir` is what lets the workflow reach its run recorder, retry breaker, learnings loader and policy loader; a string `args` carries none of it, and the run then records nothing and learns nothing — the workflow reports that as status `incomplete` with a `runtime.unreachable` blocked gate, never as `completed`. `policyDefault` is the plugin's shipped policy, a fallback: a repo's own `.claude/autonomy.json` overrides it. To make a run stricter than the repo allows, also pass `policy`: an explicit policy is INTERSECTED with the repo's (a gate is authorized only if both authorize it), so it can tighten a repo's policy and never loosen it.

Autonomy: this run is unattended unless the user is clearly present. Gates not pre-authorized by the resolved policy are recorded as BLOCKED rather than halting the run.
