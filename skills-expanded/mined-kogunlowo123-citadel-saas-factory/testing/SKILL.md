---
name: testing
description: Test generation with coverage analysis. Generates unit, integration, and E2E tests following TDD methodology.
allowed-tools: [Bash, Read, Write]
---

# Testing Skill

## When to Invoke
- New feature implementation
- Bug fix verification
- Coverage gaps identified

## TDD Workflow
1. **RED** — Write failing test first
2. **GREEN** — Implement minimal code to pass
3. **IMPROVE** — Refactor while tests stay green

## Test Types
- **Unit** — Individual functions, isolated, fast (pytest / vitest)
- **Integration** — API endpoints with real database (pytest + service containers)
- **E2E** — Critical user flows (Playwright)

## Coverage Target
- Minimum 80% code coverage
- Run: `pytest --cov=app --cov-report=term-missing`
- Frontend: `npm test -- --coverage`
