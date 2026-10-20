---
name: testing-master
description: Master hub for Testing & test automation. Use to set up or write tests: unit, integration, E2E, TDD, smoke testing, and autonomous full-app QA audits (Playwright crawl, fix-retest loop, QA_AUDIT_REPORT.md). Bundles 10 specialized skills (in skills/<name>/GUIDE.md). Use this for any testing task.
---

# Testing & test automation — Master Hub

Use to set up or write tests: unit, integration, E2E, TDD, and smoke testing.

## How to use this hub

This single skill bundles **all 10 testing skills**. Each bundled skill's full instructions live in `skills/<name>/GUIDE.md` (plus any `scripts/`, `data/`, `references/` next to it).

**Workflow:**
1. Match the user's request to one or more skills in the list below.
2. Read that skill's `skills/<name>/GUIDE.md` for full instructions before acting.
3. Combine multiple bundled skills when a task spans several areas.

## Bundled skills

- **autonomous-qa-audit-complete** ⭐ — Full autonomous E2E QA audit: scan codebase, discover routes/APIs/flows, Playwright crawl (every page, button, form, modal, CRUD, auth), console/network monitoring, screenshots, **fix → retest loop until green**. Deliver `QA_AUDIT_REPORT.md`, `FIXES_APPLIED.md`, `TEST_COVERAGE.md` + ready scripts.  
  → `skills/autonomous-qa-audit-complete/GUIDE.md`
- **adding-e2e-tests** — Set up Playwright end-to-end testing in a project, including test configuration, example tests, and CI integration.  
  → `skills/adding-e2e-tests/GUIDE.md`
- **anthropic-webapp-testing** — Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browse...  
  → `skills/anthropic-webapp-testing/GUIDE.md`
- **api-smoke-testing** — Start the dev server, discover API routes from the codebase, hit every endpoint, and report which ones return errors.  
  → `skills/api-smoke-testing/GUIDE.md`
- **cursor-skills-testing** — Testing rules for Cursor — unit, integration, E2E, performance testing, Jest, Cypress, and test automation. Use when writing or setting up tests.  
  → `skills/cursor-skills-testing/GUIDE.md`
- **form-testing** — Use Cursor's browser to fill and submit every form in the app with valid and invalid data, verifying validation, error states, and success flows.  
  → `skills/form-testing/GUIDE.md`
- **mattpocock-tdd** — Test-driven development with red-green-refactor loop. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants integration tests, or asks for test-first dev...  
  → `skills/mattpocock-tdd/GUIDE.md`
- **parallel-test-fixing** — When multiple tests fail, assign each failing test file to a separate subagent that fixes it independently in parallel.  
  → `skills/parallel-test-fixing/GUIDE.md`
- **python-tdd-with-uv** — Test-driven development in Python using uv as the package manager. Covers the red-green-refactor cycle, vertical slicing, and uv project setup.  
  → `skills/python-tdd-with-uv/GUIDE.md`
- **writing-tests** — Analyze existing code and write comprehensive unit and integration tests for it. Detects the test framework, identifies untested code paths, and generates tests with proper mocking, edge cases, and...  
  → `skills/writing-tests/GUIDE.md`

## Note

These bundled skills are intentionally not registered as separate Cursor skills (their files are `GUIDE.md`, not `SKILL.md`) so only this master appears in the skills list. Read the relevant `GUIDE.md` on demand.
