---
name: react-hydration
description: "Diagnose server/client rendering mismatches where applicable. Use for SSR/first-client mismatches; client-only rendering does not need hydration repair."
---

# react-hydration

Diagnose server/client rendering mismatches where applicable.

## Choose this workflow

Use for SSR/first-client mismatches; client-only rendering does not need hydration repair.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [React methods](../../references/packs/react.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply for a reported mismatch; SSR framework, route, server/client output, and logs.

**Pack prerequisites:** Component source, React/framework versions, state/data conventions, and relevant test tooling. Browser/profiler evidence is needed for measured rendering claims. Preserve existing framework and state libraries unless changing them is part of the request.

- **Infer from evidence:** Read component callers, ownership of state, installed React/framework versions and existing interaction tests.
- **Reasonable default:** Retain the framework and state library; preserve intended loading/error/empty behavior while resolving the named bug.
- **Ask only when needed:** Ask when product semantics such as persistence, optimistic failure or reset behavior have conflicting evidence; missing profiler access only blocks measured performance claims.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Server/client initial-render consistency and hydration behavior; applicable only to hydrated applications.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Reproduce the exact route and compare server markup with the first client render. Trace request-specific state, timestamps, locale, random values, browser-only APIs and invalid HTML nesting; distinguish parser repair from state mismatch.
2. Choose a stable initial contract and move browser-only transitions to the appropriate lifecycle. Ensure request-specific state is isolated across server requests; do not silence hydration warnings or disable rendering broadly to conceal the cause.
3. Verify direct server navigation and client navigation under differing locale/timezone and repeated requests where relevant. Confirm the page becomes interactive and retains its intended initial content, not merely that warnings disappeared.

## Technical method

- **Inspect:** Compare server HTML and first client render with timezone, locale, random IDs, browser storage and DOM nesting.
- **Method:** Find the first deterministic divergence; choose server-provided stable inputs or an explicit client-only boundary with appropriate loading behavior.
- **Avoid misdiagnosis:** Suppressing hydration warnings does not repair invalid markup or mismatched event/state attachment.
- **Check the result:** Load the real SSR page directly with varied timezone or saved state, inspect warnings and verify the affected interaction after hydration.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [React worked example](../../references/examples/react.md).
- Creating, editing or reviewing frontend UI, copy, states or visual assets: [Frontend iconography](../../references/frontend-icons.md).
- The affected project uses React Native / Expo: [React Native / Expo](../../references/frameworks/react-native.md).
- The task specifically involves react testing, react race, hydration mismatch, react strictmode; load only the matching method: [React state, async and render evidence](../../references/methods/react-behavior.md).

## Decision branches

- **When mismatch depends on user-specific data unavailable to the server:** Define a consistent initial snapshot or intentional client-only boundary for that region.

## Deliver and verify

- Hydration fix with server/client evidence.
- Mismatch source, initial-state contract and hydration plus interactivity checks.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Server and initial client output agree for the supported contract; interactivity and request isolation survive the repair. Suppressed warnings do not count as evidence.

## Stop and recover

- Do not suppress warnings or disable SSR globally as a default fix. Client-only applications receive an applicability explanation.

## Example requests

- **Normal (apply):** Fix the supplied server/client mismatch without disabling SSR globally.
- **Edge (apply):** Fix a clock and persisted theme that render differently on the server.
- **Blocked (inspect):** Diagnose supplied server/client markup without claiming a browser hydration run.
