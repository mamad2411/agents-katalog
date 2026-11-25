---
name: ultraplanning
description: Complete execution blueprint with dependency graph, parallel tracks, gates, and rollback plans
triggers: [ultraplanning, full plan, execution blueprint, dependency, plan everything, complete plan]
---

# SKILL: UltraPlanning

## Purpose
Create a plan where NOTHING is missing. Not "we'll figure it out as we go."
Every task is sized, sequenced, verified, and has a rollback path.

## The 8-Phase Blueprint

### Phase 1: Scope Contract

Before any task breakdown, lock the scope:

```markdown
## Scope Contract — [Project Name]

### In Scope (will be built)
- [Capability 1]: [description + measurable acceptance criterion]
- [Capability 2]: [description + measurable acceptance criterion]

### Out of Scope (will NOT be built in this phase)
- [Thing]: [reason it's deferred]
- [Thing]: [reason it's deferred]

### Acceptance Criteria (all must be true for "done")
- [ ] [specific, testable criterion]
- [ ] [specific, testable criterion]
- [ ] Performance: P95 < 200ms under 1000 concurrent users
- [ ] Security: all findings from security review resolved
- [ ] Tests: ≥ 80% coverage, all tests green
- [ ] Documentation: README updated, .env.example complete

### Dependencies (external things needed)
- [External API credentials]: needed before [phase]
- [Design mockups]: needed before [phase]
- [Third-party contract]: needed before [phase]
```

### Phase 2: Work Breakdown Structure

Every task must have ALL of these:
```
✓ Exact file path(s) to create or modify
✓ What to implement (behavior, not implementation)
✓ Input/output specification
✓ Time estimate (2-5 minutes)
✓ Verification method (how do you know it's done?)
✓ Dependencies (which tasks must complete first)
```

**Task template:**
```markdown
### Task N.N: [Action verb] + [what]

File: `src/[path/to/file.py]`
Depends on: Task N.M (or "none")
Time: ~[N] minutes

What to build:
[Precise description of the behavior — input X produces output Y]
[Include: validation rules, error cases, side effects]

Inputs:
- [param_name: type, description]

Outputs:
- [return value or side effect]

Verification:
- [ ] Unit test passes: `pytest tests/test_[feature].py::test_[name]`
- [ ] Returns [specific value] when given [specific input]
- [ ] Raises [specific error] when [condition]
```

### Phase 3: Dependency Graph

Map which tasks block others:

```
LAYER 0 — Must complete before anything else
  Task 1.1: Database migrations
  Task 1.2: Environment configuration

LAYER 1 — Unblocked after Layer 0 (can parallelize within layer)
  Task 2.1: User model (depends on 1.1)
  Task 2.2: Auth service (depends on 1.1)
  Task 2.3: Email service (depends on 1.2)

LAYER 2 — Unblocked after Layer 1
  Task 3.1: Registration endpoint (depends on 2.1, 2.2, 2.3)
  Task 3.2: Login endpoint (depends on 2.1, 2.2)

LAYER 3 — Frontend (depends on Layer 2)
  Task 4.1: Registration form (depends on 3.1)
  Task 4.2: Login form (depends on 3.2)

INTEGRATION CHECKPOINT after Layer 2:
  Full backend flow testable end-to-end before frontend starts

INTEGRATION CHECKPOINT after Layer 3:
  Full user flow works in browser
```

Parallelization opportunities:
- Tasks in same layer with no shared state → dispatch to parallel agents
- Frontend + tests → can run in parallel with each other after backend layer complete

### Phase 4: Quality Gates (per phase)

Each phase ends with a gate that must pass before the next phase starts:

```
GATE 1: Environment Ready
  □ `make setup` runs without errors
  □ Database migrations apply cleanly
  □ Tests run (even with 0 passing — just verifying runner works)
  □ Linter passes on empty project

GATE 2: Data Layer Ready
  □ All models defined with correct types
  □ Migrations run on clean database
  □ Seed data exists for development
  □ Model unit tests pass

GATE 3: Backend Ready
  □ All API endpoints return correct response shapes
  □ Auth flow works end-to-end (register → login → protected route)
  □ API tests pass
  □ No type errors (mypy / tsc --noEmit)
  □ No lint errors

GATE 4: Frontend Ready
  □ All pages render without console errors
  □ Core user flow works in browser
  □ Mobile responsive (check on 375px width)
  □ No accessibility violations (axe scan)

GATE 5: Integration Complete
  □ E2E tests pass (Playwright)
  □ Performance: API P95 < target
  □ Security scan: no critical findings
  □ All acceptance criteria met

GATE 6: Production Ready
  □ CI/CD pipeline green
  □ Health check endpoint works
  □ All env vars documented in .env.example
  □ Rollback procedure tested
  □ Monitoring configured
```

### Phase 5: Rollback Plan (per phase)

For EVERY phase, define what happens if it fails:

```
Phase 3 (API Layer) Rollback:
  Trigger: API tests < 80% passing after 2 hours of debugging
  Action: revert to last working commit
  Command: git revert HEAD~[N] or git checkout [last-green-commit]
  Data impact: none (no data written yet)
  Time to rollback: < 5 minutes

Production Rollback:
  Trigger: error rate > 1% within 10 minutes of deploy
  Action: redeploy previous Docker image
  Command: fly deploy --image [previous-image-tag]
  Data impact: assess if migration needs reverting
  Time to rollback: < 3 minutes
  Communication: notify team in #incidents Slack
```

### Phase 6: Execution Tracking

**Task status tracking:**
```
[ ] = not started
[~] = in progress (add: started YYYY-MM-DD HH:MM)
[x] = complete (add: completed YYYY-MM-DD HH:MM)
[!] = blocked (add: blocked by [reason])
[s] = skipped (add: skipped because [reason])
```

**Progress updates (every 2 hours of work):**
```
Update CONTEXT_STATE.md with:
  - Tasks completed since last update
  - Active task right now
  - Any blockers encountered
  - Revised estimate if needed
```

### Phase 7: Standard Task Order

For ALL software projects, always this order:
```
PHASE 1: FOUNDATION (nothing else can start without this)
  → Environment setup (Docker, dependencies, env vars)
  → Database: schema + migrations
  → Core models / data types
  → Base configuration

PHASE 2: CORE LOGIC (the heart of the system)
  → Service layer business logic
  → Core algorithms
  → Unit tests for all core logic (written FIRST in TDD)

PHASE 3: API LAYER
  → Endpoints / routes
  → Request/response validation
  → Authentication + authorization
  → API integration tests

PHASE 4: FRONTEND / CLIENT
  → Layout and routing
  → Data-fetching components
  → Forms and interactions
  → Mobile responsiveness
  → Loading and error states

PHASE 5: INTEGRATION
  → E2E tests
  → Performance testing
  → Security scan
  → Cross-browser testing

PHASE 6: PRODUCTION READINESS
  → CI/CD pipeline
  → Monitoring and alerting
  → Documentation
  → Deployment

PHASE 7: QUALITY ASSURANCE
  → Full test suite run
  → Security review
  → Code review
  → Performance profiling
```

### Phase 8: Definition of "Done"

A project is DONE only when ALL of these are true:
```
Quality:
  □ All acceptance criteria met (from scope contract)
  □ All tests pass with ≥ 80% coverage
  □ No type errors (mypy / tsc)
  □ No lint errors
  □ No critical or high security findings

Documentation:
  □ README has working setup instructions (tested by someone else)
  □ .env.example is complete with all required variables
  □ API documented (OpenAPI/Swagger or README)
  □ Architecture decisions documented
  □ PROGRESS.md updated

Deployment:
  □ CI/CD pipeline configured and green
  □ Health check endpoint returns 200
  □ Monitoring configured (error rate, latency, saturation)
  □ Rollback procedure documented and tested

Handoff:
  □ Another developer can set up and run the project from README alone
  □ On-call runbook exists for known failure modes
```

## Output
- `docs/IMPLEMENTATION_PLAN_ULTRA.md` with all phases
- Dependency graph (visual or text)
- Quality gates per phase
- Rollback plans
- Definition of Done checklist

## Quality checks
- [ ] Every task has exact file path
- [ ] Every task has 2-5 minute estimate
- [ ] Every task has specific verification method
- [ ] Dependencies explicitly mapped
- [ ] Quality gates defined per phase
- [ ] Rollback plan exists for every phase
- [ ] Parallelization opportunities identified
- [ ] Definition of Done is objective (not "looks good")
