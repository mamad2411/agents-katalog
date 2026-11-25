---
name: ops-client
description: "Operate desktop clients through semantic protocols or UI controls, including background task submission and progress queries; use ops-device for mobile devices."
---

# Client Operations

## Entry Gate

Operate a named desktop client only after confirming target process/window/build, adapter capability, screen-session state, foreground constraints, allowed side effects, and evidence boundary. Installation, process, window, menu, and runtime behavior are separate claims.
For an app-owned session protocol, bind the executable/protocol/workspace/session
instead of requiring a native window; keep backend state and desktop presentation separate.
Task delegation, submission, progress queries, waiting and result readback preserve
the user's foreground and input state by default. Naming a client as the worker
does not authorize GUI interaction; use the background and session routes below.

Reuse existing task authority for requested local client acceptance. An implementation
handoff does not require renewed approval; installs, account changes, external writes,
and destructive actions still require their own applicable authority.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Launch/inspect/interact/capture a client | [usage](references/usage.md) | Verified client-layer evidence or safe stop |
| Background or focus-preserving operation, including capability qualification | [background operations](references/background-operations.md), plus the applicable platform in usage | Per-operation capability, result, non-interference and cleanup evidence |
| App-owned protocol, task delegation, progress query or result readback | [session protocols](references/session-protocols.md) and [background operations](references/background-operations.md) | Bound session, scoped tools, reconciled submission and progress/result evidence |
| Need examples/edge cases | [usage](references/usage.md) | Correct mode/boundary |

## Invariants

- Do not substitute browser, build, process, or menu evidence for real native-window acceptance.
- Verify project navigation, text entry, submission and capture as separate requested operations. A failed capture blocks visual acceptance, while independently authorized semantic controls remain eligible for verification. Confirm navigation through application state such as a selected-project menu mark; require accepted text before testing submission.
- An explicitly requested GUI interaction with a named app authorizes that bounded action and its ordinary window activation; do not ask again solely because semantic targeting may focus it. Preserve any foreground-app constraint, and stop the affected GUI interaction without reclaiming focus if the user changes the active app. Launch, restart, another app, or broader input need their own authority.
- Background operation bypasses focus-dependent input. A writable attribute, advertised action, permission preflight or successful API return is not proof of application acceptance or uninterrupted foreground continuity. Never silently fall back to activation, global input or clipboard paste.
- Route mobile physical-device, emulator and simulator operations to `ops-device`.
  A desktop client's embedded WebView remains client-owned; browser methods may
  supply bounded Web-content evidence after the real client is identified.
- Attempt the user-named app before aliasing; report checked sources rather than declaring machine-wide absence.
- Keep diagnostics, source fixes, browser behavior, and Git mutation with their owners; clean disposable probes.

## Output Map

Return client executable/build and applicable process/window or protocol/session identity, authorized actions, direct evidence, cleanup, and `Not verified` claims.
For background work, separate capability discovery, actual state change, foreground/input continuity, capture and restoration; report each requested operation at the level directly observed.

## Reference Map

- Read [usage](references/usage.md) for client modes, targeting, safety, evidence, and stop conditions.
- Read [background operations](references/background-operations.md) for task delegation, monitoring and result readback, an explicit foreground constraint, or qualification of a focus-preserving route.
- Read [session protocols](references/session-protocols.md) for app-owned CLI/RPC task submission, progress queries and reusable qualification evidence. For ZCode CLI account/model binding, exact-session continuation and result readback, load the [bundled CLI example](references/zcode-cli-example.md). Load the [app-server example](references/app-server-example.md) only when that separate host-driven protocol is selected.
- Read [legacy simulator handoff](references/simulator-operations.md) only when an older client entrypoint supplies a mobile-device request; route it to its current device owner.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
