---
name: react-best-practices
description: |
  Provides focused implementation guidance for React and Next.js changes, including component boundaries,
  hooks, accessibility, and client/server rendering behavior.
  Use when: implementing or modifying React components, hooks, Next.js routes, or React client/server boundaries.
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# React and Next.js Best Practices

Use this skill only for React or Next.js work. It supplements the repository's conventions; local project
patterns and documented framework configuration take precedence.

## Implementation Guidance

- Reuse existing components, design-system primitives, data-access helpers, and route conventions before adding new ones.
- Keep components focused. Extract a component or hook only when it has a clear responsibility and matches local patterns.
- Follow the existing state-management approach. Keep derived values derived instead of duplicating them in state.
- Use hooks at the top level, give effects complete dependency lists, and include cleanup for subscriptions, timers,
  and other side effects.
- Preserve accessible semantics: use native controls where appropriate, labels for form inputs, keyboard support,
  visible focus behavior, and meaningful loading/error states.
- For Next.js, respect the existing server/client component boundary. Add `'use client'` only when browser APIs,
  client state, event handlers, or client-only hooks require it; keep data fetching and secrets on the server.
- Avoid hydration mismatches by keeping server and initial client output deterministic and by using established
  project patterns for browser-only values.
- Test user-visible behavior and important loading, empty, and failure states using the repository's existing test tools.

## Before Handoff

Check the changed routes and components for console warnings, accessibility regressions, unnecessary client-side
work, and broken loading or error paths. Then return to the execution skill for the standard verification and
review handoff.
