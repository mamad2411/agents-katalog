---
name: react-async
description: "Fix loading races, cancellation, stale responses, and async behavior. Use for request races, optimistic updates and async states; react-effects handles effect lifetime, subscriptions and cleanup."
---

# react-async

Fix loading races, cancellation, stale responses, and async behavior.

## Choose this workflow

Use for request races, optimistic updates and async states; react-effects handles effect lifetime, subscriptions and cleanup.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [React methods](../../references/packs/react.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; async interaction, request/cache layer, and observed race or loading issue.

**Pack prerequisites:** Component source, React/framework versions, state/data conventions, and relevant test tooling. Browser/profiler evidence is needed for measured rendering claims. Preserve existing framework and state libraries unless changing them is part of the request.

- **Infer from evidence:** Read component callers, ownership of state, installed React/framework versions and existing interaction tests.
- **Reasonable default:** Retain the framework and state library; preserve intended loading/error/empty behavior while resolving the named bug.
- **Ask only when needed:** Ask when product semantics such as persistence, optimistic failure or reset behavior have conflicting evidence; missing profiler access only blocks measured performance claims.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Cancellation, response ownership, loading/error transitions, and optimistic recovery.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Trace resource identity, the owner of each request, component lifetime and every state publication path: loading, success, error and optimistic reconciliation. Define which completion is current after navigation, account changes or a new selection.
2. Use the existing framework/data layer mechanism to separate stale-result suppression from actual cancellation. Shared requests may outlive one component; cancelling one subscriber must not invalidate another subscriber’s result.
3. Guard both success and failure publication against stale identity and disposal. Clean up subscriptions/listeners on all terminal paths and prevent disposed owners from starting further work unless the lifecycle contract explicitly permits reactivation.
4. Control completion order in tests: newer success before older success, newer success before older failure, unmount while pending and shared-request cancellation. For optimistic writes, reconcile from authoritative state after ambiguous completion instead of assuming abort undid the server effect.

## Technical method

- **Inspect:** Identify request identity, state owner, shared work lifetime and cancellation contract.
- **Method:** Force out-of-order completion and gate writes by current identity or the established query-library guarantee.
- **Avoid misdiagnosis:** Canceling one waiter must not cancel shared work still owned by another; late rejection can delete a newer cache entry.
- **Check the result:** Resolve B before A, unmount before completion, and reject an old request after new success; visible state must retain the current result.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [React worked example](../../references/examples/react.md).
- Creating, editing or reviewing frontend UI, copy, states or visual assets: [Frontend iconography](../../references/frontend-icons.md).
- The affected project uses React Native / Expo: [React Native / Expo](../../references/frameworks/react-native.md).
- The task specifically involves react testing, react race, hydration mismatch, react strictmode; load only the matching method: [React state, async and render evidence](../../references/methods/react-behavior.md).

## Decision branches

- **When cancellation arrives after the server applied a write:** Reconcile authoritative state rather than assuming the business effect was undone.

## Deliver and verify

- Request ownership and state transitions, repair, deterministic stale-success/stale-error/disposal checks and optimistic reconciliation limits.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Neither an older success nor an older error can replace current state. Disposal releases owned resources and prevents later publication; shared consumers remain independent.

## Stop and recover

- Do not assume cancellation undoes server effects. Preserve the existing fetching library unless replacement is explicitly justified in scope.

## Example requests

- **Normal (apply):** Fix out-of-order search responses overwriting newer results.
- **Edge (apply):** Fix search results that revert when older requests finish last.
- **Blocked (inspect):** Inspect async behavior without live network access; use a controlled deferred-response fixture.
