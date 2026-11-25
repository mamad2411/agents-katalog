---
name: axiom
description: Delegate a bounded build task to the local Axiom repo so Axiom supervises an opencode harness against an observable workspace.
---

# axiom

Use this skill when the user wants Axiom to drive a bounded creation/build task from OpenCrabs.

## What this does

This skill does **not** hijack an already-running opencode TUI session. That would be fake-magic bullshit.

Instead, it uses OpenCrabs as the front door, then:

1. switches into `~/Desktop/axiom`
2. inspects the Axiom repo and existing dogfood patterns
3. creates or adapts an Axiom config for the requested task
4. runs Axiom so **Axiom** supervises `opencode` as an external harness
5. verifies the resulting world state from files/build/tests instead of trusting harness self-report

## Required behavior

- Treat `~/Desktop/axiom` as the control repo unless the user explicitly says otherwise.
- Read the current Axiom docs/config examples before creating a new dogfood config.
- Keep the task bounded and observable. Convert vague requests into concrete required artifacts, checks, and build/test predicates.
- Prefer creating disposable example workspaces under `examples/opencode-dogfood/` unless the user explicitly wants a real target repo changed.
- Use real provider-qualified opencode model ids from the local opencode config.
- If the user asks to "take over my opencode instance", explain the boundary clearly: Axiom launches supervised delegated work; it does not possess another live TUI process.
- After the run, report what Axiom accomplished, what the harness did, and what the observed world proves.

## Inputs to gather from the user request

Extract or infer:
- the thing to build
- required artifacts/files
- required phrases/content
- any build/test command
- whether this should run in a disposable fixture or a real repo

If these are too vague to verify, tighten them before launching Axiom.

## Success criteria

The result is successful only when the observed world proves it:
- required files exist
- required content/build checks pass
- Axiom halts cleanly with success or a clearly explained failure mode

## Suggested command shape

A typical user invocation is:
- `/axiom build a run club website`
- `/axiom make axiom dogfood opencode against a landing page task`
- `/axiom create a disposable fixture that builds and verifies a docs microsite`

Interpret the trailing text as the task brief and execute the workflow above.
