---
name: react-audit
description: "Review components, hooks, state ownership, and behavioral risks. Use for React correctness inspection; react-rerenders requires performance evidence and react-effects targets synchronization."
---

# react-audit

Review components, hooks, state ownership, and behavioral risks.

## Choose this workflow

Use for React correctness inspection; react-rerenders requires performance evidence and react-effects targets synchronization.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [React methods](../../references/packs/react.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; component tree/feature and behavioral concerns.

**Pack prerequisites:** Component source, React/framework versions, state/data conventions, and relevant test tooling. Browser/profiler evidence is needed for measured rendering claims. Preserve existing framework and state libraries unless changing them is part of the request.

- **Infer from evidence:** Read component callers, ownership of state, installed React/framework versions and existing interaction tests.
- **Reasonable default:** Retain the framework and state library; preserve intended loading/error/empty behavior while resolving the named bug.
- **Ask only when needed:** Ask when product semantics such as persistence, optimistic failure or reset behavior have conflicting evidence; missing profiler access only blocks measured performance claims.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Hooks, ownership, identity, effects, async boundaries, and component contracts.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Identify the React/framework version, the server/client boundary and existing tests.
2. Trace props, state ownership, hook order, key identity and lifecycle through reachable interaction states, and rank concrete risks by their reachable failure paths.

## Technical method

- **Inspect:** Inspect component ownership, hook dependencies, keys, server/client boundaries and concrete interactions.
- **Method:** Trace props and state across an actual transition; apply security guidance only to changed trust boundaries such as raw HTML or server actions.
- **Avoid misdiagnosis:** Missing memoization is not automatically a defect, and ordinary JSX text is escaped by React.
- **Check the result:** Tie each finding to a reproducible state/trigger and check the caller or framework guard before reporting it.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [React worked example](../../references/examples/react.md).
- The task depends on framework defaults, middleware, RLS, server/client or deployment behavior: [Framework-specific review branches](../../references/security/frameworks.md).
- Creating, editing or reviewing frontend UI, copy, states or visual assets: [Frontend iconography](../../references/frontend-icons.md).
- The affected project uses React Native / Expo: [React Native / Expo](../../references/frameworks/react-native.md).
- The task specifically involves react testing, react race, hydration mismatch, react strictmode; load only the matching method: [React state, async and render evidence](../../references/methods/react-behavior.md).

## Decision branches

- **When source suggests excess rendering without a profile:** Report a performance hypothesis separately from demonstrated correctness defects.

## Deliver and verify

- Findings with component location, triggering interaction, state transition, severity rationale and a repair suggestion.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A conditional hook or unstable key problem includes its trigger; a stylistic preference is not presented as a correctness bug.

## Stop and recover

- Do not rewrite components during an audit or infer runtime rendering cost solely from source size.

## Example requests

- **Normal (inspect):** Audit checkout hooks and state ownership for reachable behavioral bugs.
- **Edge (inspect):** Audit a reordered editable list and a component with an early return before a hook.
- **Blocked (inspect):** Review React source without a browser; mark interaction behavior unverified.
