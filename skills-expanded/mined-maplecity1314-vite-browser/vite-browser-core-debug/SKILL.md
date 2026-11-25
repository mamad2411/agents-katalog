---
name: vite-browser-core-debug
description: >-
  Core troubleshooting workflow for Vue/React/Svelte Vite apps using
  vite-browser. Use this for first-pass debugging when the user reports broken
  UI behavior, wrong component state, router/store confusion, or a vague
  "page is broken" symptom and the dominant failure mode is not yet known.
---

# vite-browser-core-debug

Use this skill for first-pass diagnosis only. Escalate quickly if the problem is actually runtime or network driven.

## Workflow

1. Open app and detect framework.
2. Run error-first gate (`errors`, `logs`) AND `vite runtime`.
3. **IMMEDIATE ROUTING DECISION**:
   - If `vite runtime` shows HMR Socket closed/error/unknown → escalate to `vite-browser-runtime-diagnostics`
   - If `errors` contains "HMR", "hot", "reload", "import", "resolve", "module", "circular", "websocket" → escalate to `vite-browser-runtime-diagnostics`
   - If `network` shows 4xx/5xx/FAIL responses → escalate to `vite-browser-network-regression`
   - Otherwise, continue with framework state inspection
4. Inspect framework state (`vue/react/svelte tree`, plus router/pinia for Vue) only if the issue still looks component-driven.
5. Validate behavior with `network`, `screenshot`, and `eval`.
6. Return findings with command evidence and a minimal fix path.

## Escalation rules

Escalate to `vite-browser-runtime-diagnostics` if any of these are true:

1. The issue appeared right after a code edit or hot update.
2. `errors` or `logs` mention Vite, HMR, reload, import resolution, or websocket instability.
3. The page refreshes unexpectedly or falls back to full reload.

Escalate to `vite-browser-network-regression` if:

1. The main symptom is wrong data, empty data, or request failure.
2. `network` shows suspicious 4xx/5xx/FAIL responses.

## Command sequence

```bash
vite-browser open <url>
vite-browser detect
vite-browser vite runtime
vite-browser errors --mapped --inline-source
vite-browser logs
```

In `v0.3.3+`, prefer `errors --mapped --inline-source` over plain `errors` during first-pass triage. It captures browser-side runtime failures even when the Vite overlay is absent and now aligns better with live propagation diagnosis for Vue store-driven failures.

Then branch based on routing decision:

- Vue:
  - `vite-browser vue tree`
  - `vite-browser vue tree <id>`
  - `vite-browser vue pinia [store]`
  - `vite-browser vue router`
- React:
  - `vite-browser react tree`
  - `vite-browser react tree <id>`
  - `vite-browser react store list`
  - `vite-browser react store inspect <name>`
  - `vite-browser react hook health`
  - `vite-browser react commits [--limit <n>]`
- Svelte:
  - `vite-browser svelte tree`
  - `vite-browser svelte tree <id>`

Cross-check:

```bash
vite-browser network
vite-browser screenshot
vite-browser eval '<script>'
```

## Output format

Always report:

1. Confirmed symptom
2. Most likely failure class: `component-state`, `runtime-hmr`, or `network-data`
3. Evidence (exact command + key output)
4. Confidence: `high`, `medium`, or `low`
5. Minimal fix or next skill to run
6. Recheck commands

## When to switch skills

If diagnosis reveals the root cause is actually:
- HMR/runtime issue (hot update failures, module errors, import resolution) → switch to `vite-browser-runtime-diagnostics`
- Network/API issue (wrong data, failed requests, CORS, auth) → switch to `vite-browser-network-regression`
- Need final pre-release validation → switch to `vite-browser-release-smoke`
