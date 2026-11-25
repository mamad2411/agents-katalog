---
name: adh
description: Control real Windows desktop applications with the ADH trusted-Python Computer SDK over eight MCP tools or the ADH CLI. Use to discover, launch, or focus apps; observe windows or displays; click, hover, type, set values, press window or global keys, scroll, drag windows or desktop overlays, or verify UI state; diagnose ADH readiness; or author and debug a reusable RPA workflow.
---

# ADH Computer Use

Use ADH through its Python code-first surface. Use shell, filesystem/network
APIs, or ordinary code for non-UI work, and cross into ADH only when a step
requires visible user-session state or input. Do not replace an explicitly
requested real-app interaction with a hidden implementation. Send every visible
desktop side effect through ADH; never call its native driver, named pipes,
internal action paths, raw input, or another desktop automation library.

## Read first

Before controlling an app, read `references/basic-workflows.md`. It is the
canonical guide for MCP sessions, target and foreground selection, observation,
action-created windows, popup/overlay safety, selectors, input, and recovery.

Read only the reference needed for the current task:

- `references/api.md`: SDK signatures and objects, selectors, MCP result
  transport/lifecycle, desktop overlays, and CLI-only execution.
- `references/action-path-diagnostics.md`: action, cell, selector, timeout, or
  partial-effects failures.
- `references/platform-diagnostics.md`: missing MCP tools, installation,
  readiness, session, capture, integrity, or elevation failures.
- `references/rpa-authoring.md` and `references/robot-library-api.md`: read both
  before authoring or debugging reusable Robot source that imports
  `adh.robot.ADHLibrary`.
- `subskills/screenshot-text-extraction/SKILL.md`: read immediately when the
  task extracts text from visible pixels, including screenshots, image/document
  previews, OCR, or Text Extractor. Read it before discovery, launch,
  dependency selection, or `init_rpa`, for both interactive and Robot work.

## Initialize

Prefer the eight host-managed MCP tools. Use `run_python`; its cells provide
`computer`, `session`, and `emit`. Omit `session_id` for sequential work and use
an explicit session only for isolation or parallelism. Use `reset_python` only
to discard broken Python state, and close the session when the desktop task is
complete. Use `emit(...)` for every value the agent must inspect; final
expressions are discarded. Emit compact, task-specific projections, not broad
dumps.

Use the CLI only after `references/platform-diagnostics.md` establishes that
the host-managed tools are unavailable and the CLI fallback is appropriate.

## Core loop

1. Select exactly one intended window from returned ADH identities; focus and
   observe it before input.
2. Prefer semantic selectors or current snapshot-scoped elements. Request a
   screenshot only when visual evidence or screenshot-bound geometry is needed.
3. Keep deterministic work in one cell while its evidence remains current.
   Re-observe after an action or external event may have changed the UI.
4. Use the bounded action-created-window pattern from
   `references/basic-workflows.md`; never replace readiness with one immediate
   lookup or a fixed sleep.
5. On failure, preserve the original result and partial-effects evidence, then
   follow `references/action-path-diagnostics.md`. Retry only bounded,
   side-effect-free probes and continue only unfinished work.

## Reusable RPA

Use host-managed `init_rpa`, `validate_rpa`, and `run_rpa`, not their shell
equivalents, when those tools are available. Interactive exploration does not
prove the Robot source works; follow the environment-contract, smallest-slice,
validation, evidence, retry, selector, and cleanup rules in
`references/rpa-authoring.md`.

Treat `references/robot-library-api.md` as the complete public Robot contract.
Do not inspect `ADHLibrary` implementation source during normal authoring. Read
it only to diagnose a suspected library defect or a confirmed public-contract
mismatch, and never depend on private details in delivered source.

## Boundaries

Apply the host confirmation policy immediately before consequential UI actions.
Scope approval to the pending target and values; do not reuse it for a different
recipient, amount, file, or action. Re-observe after approval when the UI may
have changed, and stop before the action if approval is declined or unavailable.

Never use non-ADH input, subprocesses, imports, `ctypes`, file/network access,
or another path to perform or conceal a desktop side effect or bypass ADH
policy, recovery, logging, or host confirmation.
