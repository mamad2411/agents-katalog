---
name: agentra-e2e-testing
description: Plan, write, run, or review Agentra E2E tests using Playwright/browser tooling. Use for critical chat/auth/user journeys, flaky tests, screenshots, traces, and browser-driven validation.
---

# Agentra E2E Testing

Use this skill for browser-level validation of Agentra workflows.

## Sources of truth

- `AGENTS.md`
- Existing Playwright/browser-use tooling in the Codex environment.
- `.claude/skills/e2e-testing/SKILL.md` remains a reference for generic E2E
  patterns when deeper examples are needed.

## Workflow

1. Identify the critical user journey and owning workspace.
2. Prefer existing app scripts and test patterns before introducing new test
   structure.
3. Use stable selectors and explicit waits based on user-visible state.
4. Capture screenshots, traces, or console/network details when diagnosing.
5. Quarantine or document flaky behavior instead of hiding it with broad waits.

## Agentra focus areas

- Auth redirects and signed-in/signed-out states.
- Chat request lifecycle and SSE/stream interruption behavior.
- Error, loading, empty, and cancellation states.
- Runtime smoke handoff when UI symptoms point to AgentCore behavior.

## Output

Report journey, command or browser target, artifacts captured, result, and
follow-up risk.
