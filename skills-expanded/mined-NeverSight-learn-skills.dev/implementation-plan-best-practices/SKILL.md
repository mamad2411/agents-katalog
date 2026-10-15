---
name: implementation-plan-best-practices
description: Educational guide on best practices for creating implementation plans that prevent drift. Covers style anchors, task sizing, TDD requirements, affirmative instructions, drift handling, and quality gates. Use when creating or improving implementation plans to ensure they follow proven patterns.
---

# Implementation Plan Best Practices

Proven best practices for creating implementation plans that prevent drift and maintain alignment with project standards.

## Core Principle

> Models optimize locally; enforce global constraints with layered verification (prompt → IDE → commit → CI → runtime).

## 1. Style Anchors
- Always include 2-3 exemplary files as templates in prompts
- Reference exact paths and line numbers (e.g., `src/auth/login.ts:45-78`)
- Prefer concrete repository examples with code + tests + README
- Example: `examples/style-anchor/pkg/greeter/greeter.go` (code), `greeter_test.go` (tests), `README.md` (docs)
- Place anchors early in task instructions to prevent architectural drift

**Template:**
```
Style Anchors:
- src/auth/login.ts:45-78 (authentication pattern with proper error handling)
- src/auth/login.test.ts:12-34 (test structure for auth flows)
- src/middleware/validation.ts:15-30 (input validation pattern)
```

## 2. Task Sizing
- **Target duration:** 30-150 minutes (0.5-2.5 hours)
- **File scope:** 1-3 files per task (max 5 with justification)
- **Splitting strategy:** tests + scaffolding → minimal implementation → refactor & polish
- Commit after each small task; revert immediately on drift
- If task <30m, document rationale or split it

**Examples:**
- Small: Fix bug in `src/utils/parse.ts` — 30-60 mins
- Medium: Add API endpoint `src/server/user.ts` with tests — 90-150 mins
- Large: Migrate auth system — Split into design + 3-5 incremental tasks

## 3. Affirmative Instructions
- State permitted actions explicitly (e.g., `ONLY use: cobra, go-playground/validator, sqlite`)
- Avoid negative framing ("Don't use X" → "ONLY use: Y, Z")
- Specify exact file scopes: `Touch ONLY: src/api/handlers/user.ts, user.test.ts`

## 4. Tiered Rules
- **Global:** User prefs (format, language, length)
- **Project:** Persistent rules in `CLAUDE.md` or `.cursor/rules/` (loaded every session)
- **Context-aware:** Auto-attached rules per directory or file pattern

## 5. TDD as Anchor
- Require TDD checklist: tests → minimal code → more tests → refactor
- When tests fail: "Revise implementation to pass this test while keeping all previously passing tests. Do not modify the test. Do not add dependencies."
- Include explicit validation commands:
```bash
npm test src/auth/login.test.ts
go test ./pkg/auth -v
pytest tests/test_auth.py -v
```

## 6. Prompt Positioning
- Put critical specs, style anchors, and hard rules at the **beginning**
- Reiterate them at the **end** of prompts
- Avoid burying requirements in the middle

## 7. Model Strategies
- **Claude:** Use for surgical, minimal-diff edits; request `research → plan → implement`, `minimal diff, no renames, explain each edit`; use thinking triggers (`think`, `think hard`, `ultrathink`)
- **GPT:** Use for exploratory/greenfield work and code review; ask for tactical plans and side-effect checks

## 8. Self-Consistency & AI-on-AI Review
- Generate 3+ implementations (higher temperature), then ask model to pick most consistent
- Use multi-model review (e.g., Claude writes, GPT/Gemini reviews) to catch subtle issues

## 9. Drift Handling

**Stop & revert immediately if:**
- New dependencies introduced (not in allowed list)
- Files touched outside specified targets (>3 unexpected files)
- Linting/type errors cannot be resolved within task scope
- Tests fail and model proposes changing tests instead of implementation

**Immediate actions:**
1. Stop the session
2. Revert to pre-task state (only if changes produced by agent in this session)
3. Create incident note in `docs/drift-incidents/` with:
   - What happened
   - Files changed unexpectedly
   - New dependencies proposed
   - Remediation steps

**Allowed deviations:**
- Minor formatting (editorconfig)
- Whitespace-only edits
- Single-line refactors within scope and type-checked

**Recording learnings:**
- Update `.cursor/rules/` or `CLAUDE.md` with new rules after each session
- Add to style anchors if new pattern discovered

## 10. Quality Gates

**Pre-commit:**
- `make lint` with zero warnings
- `make test` with all tests passing
- `make typecheck` with zero errors

**CI gates:**
- Count violations (gofmt, lint, typecheck) and fail if threshold exceeded
- Run tests with race detection (e.g., `go test -race`)

**Per-task validation:**
```yaml
validation:
  commands:
    - npm run lint
    - npm test src/[module].test.ts
    - npm run typecheck
  expected_output: "All tests passing, 0 lint errors"
  failure_handling: "STOP and report. Do not continue to next task."
```

## 11. Layered Verification

1. **Prompt level:** Explicit constraints, style anchors, task sizing
2. **IDE level:** Linting, type checking, auto-formatting
3. **Commit level:** Pre-commit hooks, validation scripts
4. **CI level:** Quality gates, test suites, coverage thresholds
5. **Runtime level:** Input validation, proper error handling, monitoring

## 12. Key Learnings from Milestone 0
- **Make templates explicit vs concrete:** Include all schema-required top-level fields to avoid validation failures
- **Enforce concrete style anchors early:** Include 2-3 concrete anchors (code + tests + README) on every planning task
- **Mark inferred edits:** Use `assumption: true` with rationale for any inferred additions
- **Respect task-sizing constraints:** Enforce 30-150m task estimates; split shorter tasks with rationale
- **Keep validation inline:** Add `validation` summary with `quality_score`, `issues`, and `approval`
- **Prefer concrete execution snippets:** Add explicit validator commands in `instructions`
- **Scope implementation rules:** Keep implementation-only pattern checks scoped with `when: implementation_phase`
- **Use repository examples as anchors:** Small, well-scoped examples are high-leverage anchors

## Task Template Example

```yaml
task:
  id: t-auth-001
  name: "Add login endpoint with JWT validation"
  estimate_minutes: 90

  files:
    touch_only: [src/api/handlers/auth.ts, src/api/handlers/auth.test.ts]
    modify_only: [src/api/routes.ts]

  style_anchors:
    - {path: src/api/handlers/user.ts, lines: 45-78, pattern: "Handler with proper error handling"}
    - {path: src/api/handlers/user.test.ts, lines: 12-45, pattern: "Test structure for API handlers"}

  constraints:
    dependencies:
      only_use: [jsonwebtoken, express-validator]
    file_scope:
      max_files: 3
      stop_if_exceeded: true

  instructions: |
    ## CRITICAL CONSTRAINTS
    - ONLY modify files listed above
    - ONLY use dependencies: jsonwebtoken, express-validator
    - MUST pass: npm test, npm run lint

    ## Style Anchors
    See src/api/handlers/user.ts:45-78 for handler pattern
    See src/api/handlers/user.test.ts:12-45 for test structure

    ## TDD Checklist
    - [ ] Write failing test for POST /auth/login
    - [ ] Implement minimal handler to pass
    - [ ] Add tests for edge cases
    - [ ] Refactor for clarity

    ## Drift Policy
    STOP if: files touched >3, new dependencies, tests fail

    ## Validation
    npm test src/api/handlers/auth.test.ts && npm run lint && npm run typecheck

  validation:
    commands: [npm test src/api/handlers/auth.test.ts, npm run lint, npm run typecheck]
    expected_output: "All tests passing, 0 errors"
    failure_handling: "STOP. Revise implementation to pass tests."
```

## Quick Practical Checklist

When creating implementation plans:

1. Create `CLAUDE.md` or `.cursor/rules/` with prompt-level rules
2. Add 2-3 concrete style anchors to prompts (prefer repository examples)
3. Rescope tasks to 30m-2.5h and commit per task
4. Convert negative constraints to affirmative instructions
5. Enforce linting zero-warnings, pre-commit hooks, and CI gates
6. Require TDD plans and tests before making changes
7. Use proper error handling for runtime validation
8. Include all schema-required fields in generated YAML
9. Mark inferred additions with `assumption: true` and rationale
10. Place critical constraints at beginning AND end of prompts

## Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| No style anchors | Model introduces inconsistent patterns | Add 2-3 concrete examples with line numbers |
| Tasks >2.5 hours | Difficult to review, easy to drift | Split into tests + implementation + refactor |
| Negative framing | "Don't use X" is harder to follow | "ONLY use: Y, Z" |
| Buried rules | Model misses important constraints | Put at beginning AND end |
| No validation commands | Unclear when task is complete | Include explicit lint/test/typecheck commands |
| Allowing test modification | Tests weakened to pass implementation | "Revise implementation, not tests" |
| No drift policy | Small drifts compound | Explicit stop criteria and revert process |
| No commit checkpoints | Large uncommitted changes hard to debug | Commit after each task |

## Integration with Other Skills

- **implementation-planner:** Apply these practices when generating plans
- **implementation-plan-review:** Validate plans against these practices
- **business-requirements-interview:** Ensure requirements align with these practices
- **technical-requirements-interview:** Technical specs should follow these practices

## Examples

See `examples/` directory for:
- Well-structured task with all best practices applied
- Before/after examples showing improvements
- Common mistakes and how to fix them
