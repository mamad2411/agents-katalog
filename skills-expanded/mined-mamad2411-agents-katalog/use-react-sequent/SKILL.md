---
name: use-react-sequent
description: 'Consumer-facing guidance for using react-sequent in React apps. Use when answering questions about multi-step forms, onboarding flows, modal flows, wizards, checkout flows, or when choosing between useSequentFlow, useSequentStep, useSequentContext, and defineSequentFlow. Prefer a light overview first, then point to the hosted docs and llms.txt for deeper API and edge-case details.'
argument-hint: 'Describe the flow you want to build or the react-sequent API question you want answered.'
---

# Use react-sequent

## What This Skill Produces

- Consumer-oriented explanations of react-sequent's philosophy and API.
- Small implementation sketches for common UX flows such as onboarding, checkout, and modal wizards.
- Hook-selection guidance grounded in the library's actual public surface.
- Pointers to the hosted documentation and `llms.txt` when the user needs deeper detail.

## When to Use

- The user wants to build a step-based UX flow with react-sequent.
- The user asks how react-sequent differs from a centralized state machine.
- The user needs to choose between `useSequentFlow()`, `useSequentStep()`, `useSequentContext()`, and `defineSequentFlow()`.
- The user wants a minimal example, a migration path, or help structuring a flow around steps, context, chrome, async loading, or typed scopes.

## Core Framing

- Lead with the defining idea: the current step decides what comes next.
- Treat flows as implicit. Do not introduce or require a centralized transition map.
- Keep the API surface small in explanations. Prefer the minimal pattern that solves the user's problem.
- Present context as consumer-owned data carried through the flow, not as a state management system.
- Mention that `retreat()` navigates backward but does not restore step-local component state.
- Keep chrome outside step components. Chrome and idle children should read flow data with `useSequentContext()`, not `useSequentStep()`.

## API Selection Guide

- Use `useSequentFlow()` at the flow host. It provides `init()`, `status`, `result`, and the bound `SequentOutlet`.
- Use `useSequentStep()` inside active step components. It provides `advance()`, `retreat()`, `resolve()`, `abort()`, and the current flow context.
- Use `useSequentContext()` in chrome, idle children, or any flow-level consumer component that needs context or termination controls but not navigation.
- Use `defineSequentFlow()` only when shared context and result typing materially improve the consumer experience.
- Explain `SequentOutlet` as the render target for the active flow, with optional idle children, async fallback, stable chrome, and error handling.

## Procedure

1. Identify the flow shape the user is building: onboarding, modal, wizard, checkout, async branch, or typed reusable flow.
2. Start with a short, high-level explanation of the paradigm before giving code.
3. Choose the smallest relevant API surface using the guide above.
4. Sketch a minimal host plus two or three steps. Keep branching in step code with normal conditionals.
5. Add context only when the user needs cross-step data, persistent values across retreat, or chrome state.
6. Add `defineSequentFlow()` only when the user will benefit from shared TypeScript context and result types.
7. If the user asks for full signatures, prop details, or edge cases, consult the hosted docs and `llms.txt` instead of guessing.

## Implementation Guardrails

- Prefer one `useSequentFlow()` host per rendered flow instance.
- Ensure `SequentOutlet` is rendered before calling `init()`.
- For async steps, prefer a step loader such as `() => import("./MyStep")` and let the outlet's fallback handle loading.
- If state must survive a retreat, write it into flow context before advancing.
- Do not place `useSequentStep()` in chrome or idle children.
- Do not over-design the flow with extra wrappers or machine-style config unless the user explicitly asks for them.

## Escalate to Deeper References

Use these sources when the request moves beyond a light overview:

- Hosted docs: https://ganondev.github.io/react-sequent/
- API reference: https://ganondev.github.io/react-sequent/docs/api/use-sequent-flow
- LLMS index: https://ganondev.github.io/react-sequent/llms.txt

Reach for the hosted docs first when you need exact examples or page-level guidance. Reach for `llms.txt` when you need a compact, high-signal summary of philosophy, vocabulary, API shape, and behavioral constraints.
