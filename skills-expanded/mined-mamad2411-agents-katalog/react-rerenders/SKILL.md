---
name: react-rerenders
description: "Measure unnecessary rendering and identify its causes. Use for a measured slow interaction; react-state addresses ownership inconsistency."
---

# react-rerenders

Measure unnecessary rendering and identify its causes.

## Choose this workflow

Use for a measured slow interaction; react-state addresses ownership inconsistency.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [React methods](../../references/packs/react.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; slow interaction, component scope, and profiler traces. Apply for an explicit fix request; profiling a local build is bounded local execution.

**Pack prerequisites:** Component source, React/framework versions, state/data conventions, and relevant test tooling. Browser/profiler evidence is needed for measured rendering claims. Preserve existing framework and state libraries unless changing them is part of the request.

- **Infer from evidence:** Read component callers, ownership of state, installed React/framework versions and existing interaction tests.
- **Reasonable default:** Retain the framework and state library; preserve intended loading/error/empty behavior while resolving the named bug.
- **Ask only when needed:** Ask when product semantics such as persistence, optimistic failure or reset behavior have conflicting evidence; missing profiler access only blocks measured performance claims.

Declared evidence requirements: `browser.inspect`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Unnecessary rendering, expensive render work, and state propagation.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: edit the requested local implementation and perform relevant bounded checks while preserving unrelated work. Live data changes, remote actions and paid jobs require their resolved target and existing session authorization.

## Execute

1. Capture a baseline of the same interaction in the profiler (React Performance Tracks where available), separating render from commit cost.
2. Trace the props, context or identity responsible for the expensive work. Before adding manual memoization, check if React Compiler is enabled and if the component compiled or bailed out.
3. When a fix is requested, change the measured cause, then repeat the interaction and compare behavior and timing.

## Technical method

- **Inspect:** Capture a representative interaction in the profiler with fixed data and production-like behavior.
- **Method:** Locate changing context/prop identities or expensive work, then optimize the measured cause while preserving fresh closures.
- **Avoid misdiagnosis:** Render counts include harmless work and development checks; memoization can retain stale behavior or cost more than recomputation.
- **Check the result:** Repeat the same interaction and compare duration/responsiveness while checking that updated inputs still reach callbacks.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [React worked example](../../references/examples/react.md).
- Creating, editing or reviewing frontend UI, copy, states or visual assets: [Frontend iconography](../../references/frontend-icons.md).
- The affected project uses React Native / Expo: [React Native / Expo](../../references/frameworks/react-native.md).
- The task specifically involves react testing, react race, hydration mismatch, react strictmode; load only the matching method: [React state, async and render evidence](../../references/methods/react-behavior.md).

## Decision branches

- **When render counts fall but latency or correctness worsens:** Reject the optimization and inspect stale closures, comparison cost or unrelated bottlenecks.

## Deliver and verify

- Interaction/profile conditions, the dominant component and cause, and a comparable result or patch with its evidence.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- The slow interaction improves measurably; memoization does not preserve stale data or break callbacks.

## Stop and recover

- Avoid blanket memoization and equating render count with user-visible cost. Missing profiles yield hypotheses only.

## Example requests

- **Normal (inspect):** Analyze why changing a filter rerenders the full product grid using this profile.
- **Edge (apply):** Improve filter typing in a large product grid without stale selections.
- **Blocked (inspect):** Inspect likely render causes without profiler access; do not add blanket memoization.
