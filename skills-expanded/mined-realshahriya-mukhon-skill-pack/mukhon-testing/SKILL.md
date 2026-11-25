---
name: mukhon-testing
description: |
  Comprehensive testing standard for MUKHON. Covers end-to-end (E2E) browser testing with Playwright,
  component-level rendering tests, backend REST/WebSocket integration tests, Chrome DevTools auditing,
  and Test-Driven Development (TDD) red-green-refactor workflows.
license: MIT
metadata:
  version: v1.0.0
  publisher: mukhon-core
---

# MUKHON Testing & Quality Assurance Standard

This skill establishes the testing practices, frameworks, and verification protocols across the MUKHON platform.

---

## 1. Test Architecture & Directory Layout

```
apps/
├── api/
│   └── src/tests/               # Backend integration & security test suites
│       ├── integration.test.ts  # Core API, e-KYC, SafePay escrow, and auth integration
│       └── rls-stress-*.test.ts # PostgreSQL RLS security policy challenge harness
└── web/
    └── tests/                   # Frontend component and Playwright E2E suites
        ├── e2e/                 # Full browser user flow tests (Playwright)
        └── components/          # Component rendering and interaction tests
```

---

## 2. Playwright E2E Testing Guidelines

### Pinned Execution Commands
Always use pinned versions or project scripts to prevent supply-chain vulnerabilities:
```bash
# Recommended: Run via package.json script
npm run test:e2e --workspace=@mukhon/web

# Direct execution with pinned version
npx @playwright/test@1.49.0 test

# Run specific spec with UI or headed mode for debugging
npx @playwright/test@1.49.0 test tests/e2e/feed.spec.ts --headed
```

### Detailed Testing References
- [Page Object Models](references/page-objects.md): Clean abstraction classes for MUKHON Feed, SafePay Escrow, and Modals.
- [Network Mocking](references/network-mocking.md): Route interception (`page.route()`) for Porichoy NID e-KYC and courier webhooks.
- [Test Fixtures](references/fixtures.md): Reusable authenticated citizen test contexts.

### Core Testing Rules
1. **User-Facing Locators**: Always prioritize user-visible selectors over CSS structure:
   - `page.getByRole('button', { name: /পোস্ট|Post/i })`
   - `page.getByLabel('Search Mukhon')`
   - `page.getByText('24h Citizen Stories')`
   - Avoid brittle XPath or dynamic class chains (e.g. `div > div:nth-child(2)`).
2. **Web-First Assertions with Auto-Waiting**:
   - `await expect(page.getByRole('dialog')).toBeVisible();`
   - Never use arbitrary `page.waitForTimeout()` sleeps. Always wait for specific DOM states, network responses, or URL changes.
3. **Session & Auth State Storage**:
   - Save authenticated browser states (`storageState`) to avoid re-logging in before every individual test case.
4. **Responsive Testing**:
   - Test both desktop viewport (`1280x800`) and mobile viewport (`390x844` iPhone 14/15 equivalent) to verify mobile bottom navigation bar (`.mobile-bottom-nav`) and collapsible sidebars.

---

## 3. Backend & Security Testing Guidelines

1. **Dual-Mode Execution**:
   - Every backend test suite must cleanly run in both **In-Memory Store Mode** and **PostgreSQL Mode** without crashing when `DATABASE_URL` is omitted.
2. **Zero-PII Storage Validation**:
   - Verify that National ID numbers are strictly hashed with HMAC-SHA256 blind indexing and passwords use `scrypt`.
3. **Escrow & SafePay Invariants**:
   - Test that money transfers and escrow locks enforce double-entry ledger balance rules and 3-attempt OTP brute force limits.

---

## 4. Test-Driven Development (Red-Green-Refactor)

1. **Red**: Write a failing test capturing the exact bug or new capability.
2. **Green**: Implement the minimal, clean code change required to satisfy the assertion.
3. **Refactor**: Simplify and optimize while keeping the full test suite green.
4. **Gate**: Run `npm run typecheck` or `npx typescript@5.9.3 tsc --noEmit` across all workspaces before declaring any task complete.
