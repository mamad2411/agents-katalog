---
name: quality-gates
description: Graduated pre-commit quality checks that scale with project complexity and user tier. Level 0 for Builder-tier small projects, up to Level 4 for enterprise codebases. Thresholds configurable in architecture.md.
invoke_when: Use when committing code, creating a PR, running a quality audit, or when the post-tool-use hook detects a git commit.
---

# Quality Gates

## Graduated Levels

Quality checks scale with project maturity and user tier. The plugin detects the project's current level based on file count and user tier, then adjusts expectations accordingly.

### Level 0: Just Ship It (Builder-Tier, <5 Source Files)

For Builder-tier users with small projects. The goal is momentum, not perfection. Two checks:

- [ ] Build succeeds (the code runs without crashing)
- [ ] No hardcoded secrets, API keys, or credentials in source files

That's it. No lint rules, no coverage thresholds, no architectural purity tests. The project has 4 files — it doesn't need governance, it needs to exist.

**Automatic Graduation:** Level 0 automatically graduates to Level 1 when either condition is met:
- The project has its first successful deployment (it's real now, treat it that way)
- The project reaches 5+ source files (complexity is emerging, basic hygiene matters)

When graduation happens, inform the user: "Your project is growing — I'm going to start checking for a few more things before commits to keep things solid. Nothing heavy, just making sure tests pass and the code is clean."

### Level 1: Foundation (5+ Source Files, Always Active for Engineer-Tier)
Every project that's past the prototype stage:
- [ ] All existing tests pass
- [ ] No TypeScript/lint errors (if applicable)
- [ ] No `console.log` in production code — use a structured logger (pino, winston). Install one if none exists.
- [ ] No hardcoded secrets, API keys, or credentials
- [ ] New code has corresponding tests
- [ ] Build completes successfully
- [ ] Linter configured and passing — set up ESLint (TypeScript/JS), Ruff (Python), or golangci-lint (Go) if not present
- [ ] Input validation uses a schema library (Zod, Pydantic) — not manual if/else
- [ ] Test coverage tooling configured (vitest --coverage, pytest-cov, go test -cover)

### Level 2: Growing (10+ Source Files)
Building discipline:
- [ ] All Level 1 checks
- [ ] Test coverage for new code above threshold (default: 70%)
- [ ] No `TODO` without a ticket number or date
- [ ] No `any` type in TypeScript strict mode projects
- [ ] No unused imports or variables
- [ ] Error handling on all async operations

### Level 3: Maturing (50+ Source Files)
Architectural integrity:
- [ ] All Level 2 checks
- [ ] No circular imports (verify with dependency analysis)
- [ ] Bundle size within budget (if frontend)
- [ ] API contracts validated against types
- [ ] Database migrations are reversible
- [ ] No direct database queries outside the data layer
- [ ] All public functions have JSDoc/docstrings

### Level 4: Production (100+ Source Files)
Enterprise readiness:
- [ ] All Level 3 checks
- [ ] Performance benchmarks pass
- [ ] Accessibility audit passes (if frontend)
- [ ] Security scan clean (no known vulnerabilities in dependencies)
- [ ] API documentation synchronized with implementation
- [ ] Error tracking integration verified
- [ ] Health check endpoints respond correctly

---

## Level Selection Logic

```
if user_tier == "Builder" AND source_files < 5:
    level = 0
elif source_files < 10:
    level = 1
elif source_files < 50:
    level = 2
elif source_files < 100:
    level = 3
else:
    level = 4

# Override: Engineer-tier always starts at Level 1 minimum
if user_tier == "Engineer" AND level == 0:
    level = 1
```

## How to Run

When this skill activates:
1. Count source files to determine the project's level
2. Check user tier (Builder-tier can be Level 0; Engineer-tier starts at Level 1)
3. Run through the applicable checklist
4. Report results as: PASS / FAIL / ADVISORY
5. FAIL = must fix before committing
6. ADVISORY = should fix, but non-blocking

**For Builder-tier users at Level 0-1:** Report simply. "Everything looks good, ready to commit" or "Found a potential API key in the code — let me move that to an environment variable first."

**For Engineer-tier users or Level 2+:** Report the full checklist with details on any failures.

## Configuration

Quality gate thresholds can be customized in `.shipworthy/architecture.md`:
```markdown
## Quality Gate Levels
Level 0 (builder, <5 files): [build, no secrets]
Level 1 (always): [custom checks]
Level 2 (15+ files): [custom threshold]
Level 3 (75+ files): [custom checks]
Level 4 (150+ files): [custom checks]
Coverage threshold: 80%
Bundle size limit: 250KB
```

---

## Rationalization Pressure Test

These are excuses you might generate to skip quality gates. Each one is wrong.

| Rationalization | Why It's Wrong | What To Do Instead |
|----------------|---------------|-------------------|
| "The user just wants to commit quickly" | A fast commit with bugs is slower than a 2-minute quality check | Run the gates. They take less time than fixing a broken deploy |
| "This is a WIP commit" | WIP commits become permanent commits. Standards apply always | At minimum, run Level 0 (build + no secrets). Always |
| "Quality gates are too strict for this project" | The gates are graduated — Level 0 has only 2 checks. That's not strict | Apply the level that matches the project. Don't skip entirely |
| "I already checked manually" | Manual checks miss things. That's why automated gates exist | Run the automated checks. Trust the output over your memory |
| "This is just documentation" | Docs can contain secrets, broken links, and incorrect information | Run Level 0 at minimum. Secrets scanners catch credentials in any file |
