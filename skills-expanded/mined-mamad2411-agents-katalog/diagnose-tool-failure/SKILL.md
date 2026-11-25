---
name: diagnose-tool-failure
description: "Pre-classify an agent-tool failure (env, auth, quota, code, data, unknown) before retrying or filing a bug, so the resulting report has a useful hypothesis and the right next step."
---

# Diagnose tool failure

Before retrying or filing an incident with `report_incident`, classify the
failure in **one** of these buckets and pick the matching next step.

## 1. Environment / infrastructure

**Signals**
- `Timed out after <N>ms` on `agent_filesystem_*` / `agent_terminal_run` /
  `agent_coding_run`.
- `ENV_STARTUP_FAILED`, "image not found", "container exited",
  "no space left on device".
- Sandbox starts but commands return `command not found` for tools that
  should be preinstalled.

**Action**
- Do **not** keep retrying — the sandbox is the bottleneck.
- Call `report_incident` with `hypothesis: "env"`.
- Suggested next step in the description: "platform team to retry image
  pull / increase container start timeout".

## 2. Auth / integration

**Signals**
- `AUTH_MISSING`, `INTEGRATION_DISABLED`, 401 / 403 from integration calls.
- Tool says "<service> is not connected".

**Action**
- If the user is in the loop: tell them which integration to (re)connect; do
  **not** file an incident.
- If you are running in a dispatched task with no user available: call
  `report_incident` with `hypothesis: "auth"` and route to the integration
  owner. Do not block work that does not need that service.

## 3. Quota / rate limit

**Signals**
- 429, "rate limit", "quota exceeded", `RESOURCE_EXHAUSTED`.

**Action**
- Back off (exponential), retry once after the suggested delay.
- If still failing, call `report_incident` with `hypothesis: "quota"` and
  propose the limit / plan that needs raising.

## 4. Code / schema defect

**Signals**
- Tool input rejected with "unknown property", "validation failed", or
  response shape does not match the documented schema.
- Same tool call passes for one input and fails for a near-identical input
  you can articulate.

**Action**
- Capture the smallest failing input via `reproducible-bug`.
- Call `report_incident` with `hypothesis: "code"` and attach the minimal
  repro.

## 5. Data drift

**Signals**
- Tool succeeds technically but the result is empty / nonsensical for an
  input that worked before.
- Search / RAG tools return zero hits for queries that historically
  returned results.

**Action**
- Re-run with a known-good input to confirm the tool itself works.
- Call `report_incident` with `hypothesis: "data"` if confirmed.

## 6. Unknown

**Signals** — None of the above clearly fits.

**Action** — Do **not** invent a hypothesis. Call `report_incident` with
`hypothesis: "unknown"` and include the raw error verbatim.

## Output for the reporter

After diagnosis, hand `self-report-agent-issue` the following so it can
populate the `report_incident` payload cleanly:

- Hypothesis bucket (one of the six above)
- Smallest reliable repro (params + response)
- Whether the failure is blocking
- Whether retry is worth attempting on the platform side
