# Definition of Done Enforcement

## Purpose
Verifies every PR satisfies the Definition of Done checklist before moving to In Review status for Edward's merge.

## Role
Tech Lead

## Phase
Development

## Triggered By
Developer signals PR is ready for review.

## Inputs
- PR diff and description
- CI results (lint, check, tests, coverage)

## Process
1. Read DoD checklist against the PR.
2. If any item fails: block PR with a specific message identifying which items fail.
3. Developer resolves and updates PR.
4. Tech Lead re-checks only the failed items.
5. When all items pass: proceed with `code-review`.

### DoD Checklist (ALL required before In Review)
- [ ] `bun turbo lint` passes with no errors
- [ ] `bun turbo check` (TypeScript) passes with no errors
- [ ] Unit tests pass and new code coverage ≥ 80%
- [ ] Component integration tests pass (where applicable)
- [ ] No manually edited files in `packages/api/src/generated/`
- [ ] Generated files regenerated if proto/graphql/prisma schema changed
- [ ] `bun run supergraph` run if GraphQL SDL changed
- [ ] Local ZAP baseline scan run (for PRs with public-facing endpoints)
- [ ] PR description completed in full (What/Why/How/Testing sections)
- [ ] Docs updated IF PR touches `contracts/` OR `apps/servers/` OR `openspec/diagrams/`
- [ ] `story-changelog-writing` complete (story-level PRs only)
- [ ] No open critical/high bug cards linked to this task

## Outputs
PR moved to In Review, or blocked with specific failing items listed.

## Quality Gates
- [ ] All checklist items verified (not assumed)
- [ ] Specific failures identified (not generic "doesn't meet DoD")
- [ ] PR only moves to In Review after complete DoD + code-review approval

## References
- `.claude/skills/tech-lead/code-review/SKILL.md`
- `.claude/skills/tech-lead/story-changelog-writing/SKILL.md`
