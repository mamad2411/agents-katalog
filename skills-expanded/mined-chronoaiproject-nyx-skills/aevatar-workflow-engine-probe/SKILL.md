---
name: aevatar-workflow-engine-probe
version: "1.0"
description: Verify the workflow engine can actually start a run and return its output to chat — uses aevatar_start_workflow with an inline self-contained workflow (no pre-registration needed), waits for completion, and checks the run output echoes a unique token. Run it before relying on any workflow; it isolates "is the engine alive" from "is my workflow correct".
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - probe
    - workflow
    - engine
    - diagnostics
---

# Aevatar Workflow Engine Probe

Use this to confirm the workflow engine can start a run, execute steps, and stream the result back
into chat — without depending on any pre-registered workflow. It uses `aevatar_start_workflow`,
which accepts an inline `workflow_yamls` bundle and runs it self-contained.

**You (the agent) start the probe workflow yourself and check the returned output.** The workflow
just echoes a token, so the answer is deterministic. A start/run error is a finding — quote it
verbatim, never fabricate a result.

## How to run it

Call `aevatar_start_workflow` with:
- `workflow_id`: `probe_echo`
- `inputs.prompt`: `workflow-probe-7421` (the token to echo back)
- `wait`: `complete` (block until the run finishes so you can read the output)
- `workflow_yamls`: a one-element bundle containing exactly this inline workflow:

```yaml
name: probe_echo
description: Inline engine probe — echoes the run input as the run output.
when_to_use: Engine liveness probe.
steps:
  - id: echo
    type: assign
    parameters:
      target: result
      value: "${input}"
```

PASS if the run finishes and its output contains `workflow-probe-7421`. FAIL if the start is
rejected, the run errors, or the output is empty / different.

## Output

One report: did the run start? did it reach a terminal finished state? did the output echo the
token? Then a verdict: `WORKFLOW ENGINE OK` or `WORKFLOW ENGINE BLOCKED: <verbatim error / where
it stalled>`.

Interpretation (report, don't fix):
- `workflow_yamls are not accepted inside a managed workflow runtime context` → you are already
  inside a workflow run; run this probe from a plain chat turn instead.
- start rejected for scope / authorization → the caller's NyxID scope or token is unavailable.
- run starts but never finishes (no terminal output) → the engine accepted but the run stalled;
  note that the engine ingress works but execution/return did not complete.

## Guardrails

- Only start the bundled inline echo workflow; never start arbitrary or side-effecting workflows
  from this probe.
- Use `wait: complete` so you actually observe the terminal output; never report a pass from an
  `accepted` ack alone.
- Report verbatim; never claim the engine works without an observed echoed token.
- Never ask the user for tokens — your NyxID-brokered tools handle all credentials.
