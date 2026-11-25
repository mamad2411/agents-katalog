---
name: ui-browser-debug
description: Use when the task requires browser-flow debugging, DOM-aware interaction planning, UI-state inspection, or screenshot-driven verification. Sanitized adaptation of upstream browser automation skills.
---

# UI Browser Debug

## When to use
- Reproducing or diagnosing a browser flow.
- Verifying a UI state with screenshots or fresh DOM references.
- Planning browser automation without immediately adding a test suite.

## Creane-first workflow
1. Inspect existing browser tooling first:
   - `browser_tools.py`
   - `browser_session_runtime.py`
   - `workers/browser_delegate_worker.py`
2. If the task is a delegated browsing task, prefer Creane's browser worker and artifact flow over introducing new browser stacks.
3. If terminal-side browser automation is still required, keep it CLI-first and avoid generating `@playwright/test` files unless the user explicitly asks for tests.
4. Re-capture state after navigation, modal changes, or tab switches. Do not trust stale element references.
5. Save screenshots and traces under `analysis_artifacts/` or another task-scoped output directory instead of creating random top-level folders.

## Guardrails
- Use the smallest tool that can answer the question.
- Prefer fresh snapshots and explicit commands over opaque browser eval blocks.
- Do not add Node or Playwright dependencies unless the repo task actually needs them.
- If browser automation depends on credentials or login state, stop and ask for the missing access path instead of faking success.

## Output expectations
- State what page or flow was checked.
- Note the last confirmed UI state.
- Link any artifacts you created.
- If you could not verify visually, say so explicitly.
