---
name: e2e
description: |
  E2E testing workflow with test-first development rules. Covers new features (test-first),
  test modifications (progressive testing), and refactoring (iterative testing). Framework-agnostic
  with Playwright/Cypress/Jest examples. Keywords: e2e, testing, tdd, playwright, cypress.
triggers:
  - /e2e
  - /e2e new-feature
  - /e2e test-change
  - /e2e refactor
  - /e2e help
  - /e2e dashboard
  - e2e testing workflow
  - test first development
negative_triggers:
  - unit testing only (use framework directly)
  - integration tests without UI
  - performance/load testing
version: 1.4.0
author: Christian Kusmanow / Claude
last_updated: 2026-04-12
security:
  trust_model: Test commands run locally, dashboard API is read-only
  api_endpoints:
    - GET /api/health/e2e (read-only, no auth required for local dev)
  notes: Dashboard API exposes test results; ensure not exposed in production
---

# Skill: E2E Testing

Injects the E2E testing workflow context with structured rules for test-driven development. Uses classic agile terminology (user story, use-case, test case) and framework-agnostic commands that work with any testing framework.

## Trigger

- `/e2e` - Load E2E testing context and rules
- `/e2e new-feature` - Start new feature workflow (Rule 1: Test-First)
- `/e2e test-change` - Start test modification workflow (Rule 2: Progressive Testing)
- `/e2e refactor` - Start refactoring workflow (Rule 3: Iterative Testing)
- `/e2e help` - Show testing rules quick reference

## Arguments

$ARGUMENTS

---

## Command Handling

### If `$ARGUMENTS` contains "new-feature":

**Execute Rule 1: Test-First Development**

1. **Ask for user story:**
   - "What user story are we implementing? (e.g., 'As a user, I can log in')"

2. **Define use-cases:**
   - Ask: "What use-cases (scenarios) should this feature cover?"
   - Examples: "Valid credentials", "Invalid password", "Account locked"

3. **Create TodoWrite list:**
   ```
   User Story: [story name]
   - [ ] Use-Case: [scenario 1]
     - [ ] Test Case: [test 1.1]
     - [ ] Test Case: [test 1.2]
   - [ ] Use-Case: [scenario 2]
     - [ ] Test Case: [test 2.1]
   - [ ] Implementation
   - [ ] Run component test suite
   - [ ] Run full app test suite
   ```

4. **Guide through workflow:**
   - Write test cases FIRST (mark in_progress)
   - Run tests (expect RED - failures)
   - Implement feature code
   - Run tests until GREEN (mark completed)
   - Run component suite
   - Run full app suite

### If `$ARGUMENTS` contains "test-change":

**Execute Rule 2: Progressive Testing**

1. **Ask which test:**
   - "Which test case are you modifying?"

2. **Create TodoWrite list:**
   ```
   Test Change: [test name]
   - [ ] Modify test case
   - [ ] Run single test
   - [ ] Run component test suite
   - [ ] Run full app test suite
   ```

3. **Guide through progressive workflow:**
   - Modify the specific test (mark in_progress)
   - Run ONLY that single test
   - If passes → run component test suite
   - If component passes → run full app suite (mark completed)
   - If ANY step fails → fix before proceeding to next level

### If `$ARGUMENTS` contains "refactor":

**Execute Rule 3: Iterative Testing**

1. **Ask which component:**
   - "Which component are you refactoring?"

2. **Identify affected tests:**
   - "What use-cases/features are affected by this refactoring?"

3. **Create TodoWrite list:**
   ```
   Refactor: [component name]
   - [ ] Use-Case: [affected feature 1]
     - [ ] Test Case: [test 1.1] - run until green
     - [ ] Test Case: [test 1.2] - run until green
   - [ ] Use-Case: [affected feature 2]
     - [ ] Test Case: [test 2.1] - run until green
   - [ ] Run full app test suite
   ```

4. **Guide through iterative workflow:**
   - Run affected feature tests ONLY (mark in_progress)
   - Continue refactoring until feature works
   - Mark feature completed, move to next
   - Repeat for ALL affected features
   - ONLY when ALL features pass → run full app suite

### If `$ARGUMENTS` contains "help":

Display the Testing Rules Quick Reference section.

### If `$ARGUMENTS` is empty or other:

**Load the E2E testing context** (default behavior - see rules below).

---

## E2E Testing Rules

### Rule 1: New Feature Development (Test-First)

> When you build something new, create e2e tests in advance before you start with the feature implementation.

**Workflow:**
1. Define user story and use-cases
2. Write test cases for each use-case BEFORE any implementation
3. Run tests → expect RED (failures)
4. Implement feature code
5. Run tests → work until GREEN (all pass)
6. Run component test suite
7. Run full app test suite

**Rationale:** Tests document expected behavior before code exists. This ensures you understand requirements and have a definition of "done" before writing code.

### Rule 2: Test Modification (Progressive Testing)

> When you change something inside a test, run only this test. After that, run the component test suite. Only when it does not fail, run the whole app suite.

**Workflow:**
1. Modify the specific test
2. Run ONLY that single test
3. If passes → run component test suite
4. If component passes → run full app test suite
5. If ANY step fails → fix before proceeding

**Levels:**
```
Single Test → Component Suite → App Suite
     ↓              ↓              ↓
   Fastest      Moderate      Complete
```

**Rationale:** Avoid wasting time running the full suite for every small change. Progressive testing catches issues early while maintaining confidence.

### Rule 3: Component Refactoring (Iterative Testing)

> When you refactor a component, run only the affected feature tests until all features are completely refactored and working. Then run the whole app test suite.

**Workflow:**
1. Identify all affected use-cases/features
2. Run affected feature tests ONLY
3. Refactor incrementally
4. Repeat until feature tests pass
5. Move to next affected feature
6. ONLY when ALL features pass → run full app suite

**Rationale:** Keep feedback loop tight during refactoring. Don't run unrelated tests that can't fail from your changes.

---

## Agile Terminology

| Term | Definition | Example |
|------|------------|---------|
| **User Story** | Feature from user perspective | "As a user, I can log in to my account" |
| **Use-Case** | Specific scenario within a story | "Valid credentials", "Invalid password" |
| **Test Case** | Individual test implementation | `test_login_with_valid_credentials()` |

### Hierarchy
```
User Story
├── Use-Case 1
│   ├── Test Case 1.1
│   └── Test Case 1.2
└── Use-Case 2
    └── Test Case 2.1
```

---

## TodoWrite Integration

The skill uses TodoWrite to track testing progress. Each workflow creates a structured todo list:

### Example: New Feature Todo
```
User Story: User can reset password
├── [ ] Use-Case: Request reset via email
│   ├── [ ] Test Case: valid email sends reset link
│   └── [ ] Test Case: invalid email shows error
├── [ ] Use-Case: Complete reset with token
│   ├── [ ] Test Case: valid token allows new password
│   └── [ ] Test Case: expired token shows error
├── [ ] Implementation
├── [ ] Component test suite
└── [ ] Full app test suite
```

### Todo Status Flow
- `pending` - Not started
- `in_progress` - Currently working on
- `completed` - Finished and verified

---

## Testing Commands (Framework-Agnostic)

The skill uses generic commands. Replace with your framework's equivalents:

| Generic Command | Playwright | Cypress | Jest |
|----------------|------------|---------|------|
| Run single test | `npx playwright test [file]` | `npx cypress run --spec [file]` | `npm test -- [file]` |
| Run component suite | `npx playwright test [folder]` | `npx cypress run --spec [folder]/**` | `npm test -- [folder]` |
| Run full app suite | `npx playwright test` | `npx cypress run` | `npm test` |

---

## Usage Guidelines

When this skill is invoked:

1. **Always use TodoWrite** to track testing progress with agile terms
2. **Follow the rules strictly** - don't skip testing levels
3. **Document user stories** before writing tests
4. **Keep tests focused** - one use-case per test where possible
5. **Report progress** at each testing level
6. **Stop on failures** - fix before proceeding to broader suites

---

## Example Usage

### Load Context
```
User: /e2e

Claude:
E2E testing context loaded. I'm now aware of:

- Rule 1: Test-First (new features - write tests before implementation)
- Rule 2: Progressive (test changes - single → component → app)
- Rule 3: Iterative (refactoring - affected features → app suite)
- Terminology: User Story → Use-Case → Test Case

Which workflow do you need?
- `/e2e new-feature` - Start test-first development
- `/e2e test-change` - Modify existing tests
- `/e2e refactor` - Refactor with iterative testing
```

### New Feature Workflow
```
User: /e2e new-feature

Claude:
Starting Rule 1: Test-First Development

What user story are we implementing?
(e.g., "As a user, I can log in to my account")

User: As a user, I can reset my password

Claude:
User Story: Password Reset

What use-cases should this feature cover?

User: Email request, token validation, password update

Claude:
Creating todo list for: User Story - Password Reset

[TodoWrite:
- Use-Case: Email request
  - Test Case: valid email sends reset link
  - Test Case: invalid email shows error
- Use-Case: Token validation
  - Test Case: valid token proceeds
  - Test Case: expired token rejected
- Use-Case: Password update
  - Test Case: new password saved
- Implementation
- Component suite
- Full app suite]

Let's write the first test case: "valid email sends reset link"
```

### Test Change Workflow
```
User: /e2e test-change

Claude:
Starting Rule 2: Progressive Testing

Which test case are you modifying?

User: login_with_valid_credentials test

Claude:
[TodoWrite:
- Modify test: login_with_valid_credentials [in_progress]
- Run single test
- Run auth component suite
- Run full app suite]

Make your changes to the test. When ready, I'll guide you through:
1. Run single test first
2. Then component suite
3. Finally full app suite
```

### Refactor Workflow
```
User: /e2e refactor

Claude:
Starting Rule 3: Iterative Testing

Which component are you refactoring?

User: The authentication service

Claude:
What use-cases/features are affected by this refactoring?

User: Login, logout, password reset, session management

Claude:
[TodoWrite:
- Use-Case: Login [in_progress]
  - run until green
- Use-Case: Logout [pending]
- Use-Case: Password reset [pending]
- Use-Case: Session management [pending]
- Full app suite [blocked]]

Refactoring: Authentication Service

Start with Login tests. Run them after each refactoring change.
Only move to Logout once Login is fully green.
Full app suite runs ONLY after all features pass.
```

---

## Dashboard Integration

The E2E test results can be visualized in the application dashboard via the E2E Results Service.

### E2E Results API

**Endpoint:** `GET /api/health/e2e`

Returns structured test results:
```json
{
  "available": true,
  "status": "success" | "warning" | "error",
  "summary": {
    "total": 69,
    "passed": 67,
    "failed": 0,
    "skipped": 2,
    "duration": 45.2
  },
  "byBrowser": {
    "chromium": { "passed": 45, "failed": 0, "skipped": 0 },
    "firefox": { "passed": 22, "failed": 0, "skipped": 2 }
  },
  "timestamp": "2026-01-20T12:00:00Z"
}
```

### Dashboard Widgets

| Widget | Purpose |
|--------|---------|
| Hero | Full-width summary at dashboard top |
| Card | Regular dashboard item with browser breakdown |
| Sidebar | Collapsible panel with spec details |

### Workflow: `/e2e dashboard`

When invoked with "dashboard" argument:
1. Check if E2E results exist (`dist/.playwright/apps/home-e2e/results.xml`)
2. If missing, run E2E tests: `nx e2e home-e2e`
3. Display summary from API endpoint
4. Show visual breakdown of test status

---

## Fixture-Driven Testing (Primary Workflow)

The fixture-driven test environment is the standard E2E workflow for the Teslasoft vault.
Fixtures are declarative test specs that run against an isolated Docker stack with no
production vault dependency.

### Architecture

- **Fixture worktree:** `.worktrees/e2e-fixture/` — minimal PARA skeleton (11 directories)
- **Isolated Docker stack:** `postgres-test:5433`, `drone-test:3837`, `vault-mcp-test:3938`
- **Standalone compose:** `docker-compose.test.yml` (no production vault dependency)
- **Fixture definitions:** `coordination/tests/fixtures/*.fixture.md`
- **Baseline tracking:** `coordination/tests/baseline-report.json`

### Standard Commands

| Command | Purpose |
|---------|---------|
| `pnpm docker:test` | Start test containers |
| `pnpm test:fixtures` | Run all 41 fixtures against fixture worktree |
| `pnpm docker:test:down` | Stop and remove test containers |
| `pnpm test:fixtures:ci` | CI mode — fail on regression |

### Workflow

```
pnpm docker:test          # Start isolated test containers
pnpm test:fixtures        # Run all fixtures (~500s)
pnpm docker:test:down     # Clean up when done
```

### 3-Tier Gate Strategy

| Gate | When | Behavior |
|------|------|----------|
| Project branches | During development | Fixtures run but DON'T block. Failures visible, parallel work continues. |
| Merge to development | Integration | Mandatory gate, non-blocking (advisory warnings) |
| Merge to main/master | Production | BLOCKING gate. Failures stop the merge. |

**Rationale:** Flexibility during development, strict production safety net.

### When to Use Fixture Tests vs Other Tests

| Test Type | Use For | Command |
|-----------|---------|---------|
| **Fixture tests** | Integration, E2E, pipeline validation | `pnpm test:fixtures` |
| **Unit tests** | Isolated function logic, pure transforms | Framework-specific (`pnpm test`, `bun test`) |
| **Cypress** | Visual rendering, screenshots, video (LR-E2E-002) | `pnpm cypress:run` |

Fixture tests are the primary verification mechanism for submodule changes (drone,
vault-mcp, harness-telemetry). Always run `pnpm test:fixtures` after modifying
submodule code.

---

## Related Skills

- `/teslasoft` - Teslasoft business context and portfolio goals
- `/webstatic` - WebStatic PHP/TypeScript CMS framework context
- `/repomix` - Repomix tool for packing codebases into AI-friendly formats
- `e2e:vault-testing` — Fixture worktree architecture and PARA test patterns
- `e2e:fixture-management` — Fixture runner, batching, baseline reports

---

## Related Resources

- [[E2E Testing Dashboard]] – Dashboard visualization patterns

---

## Metadata

**Last Updated:** 2026-04-12
**Version:** 1.4.0
**Author:** Christian Kusmanow / Claude
**Scope:** Global
**Changelog:**
- v1.4.0: Added fixture-driven testing as primary E2E workflow (P54-W7), 3-tier gate strategy, standard commands
- v1.2.0: SDL compliance - Added YAML frontmatter with triggers, negative_triggers, security section
- v1.1.0: Added dashboard integration and E2E Results API
- v1.0.0: Initial release with 3 testing rules (test-first, progressive, iterative)
