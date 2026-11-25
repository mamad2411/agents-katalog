# Priority Scoring Model

## Purpose
Consistent scoring framework for ranking Epics and User Stories across roles.

## Role
Shared — PO, PM, Security Engineer, Solution Architect, QA Engineer

## Phase
Planning

## Triggered By
PM `task-prioritisation` skill during Stage 6 of the planning session.

## Inputs
- List of stories/epics under consideration
- Per-role dimension scores (see below)
- Compliance flags per story (if any)

## Process
1. Each role scores their dimension per story on a 1-5 scale.
2. Apply weights to each dimension score.
3. Calculate weighted total per story.
4. Rank stories highest to lowest.
5. Apply Must Ship / Should Ship / Can Hold classification.
6. Produce ranked priority table.

### Scoring Dimensions and Weights

| Dimension            | Owner              | Weight | Scale         |
|-----------------------|--------------------|--------|---------------|
| Security Risk         | Security Engineer  | × 3.0  | 1-5           |
| Dependency Blocking   | Solution Architect | × 2.5  | 1-5           |
| Business Value        | Product Owner      | × 2.0  | 1-5           |
| User Impact           | Product Owner      | × 1.5  | 1-5           |
| Testability Risk      | QA Engineer        | × 1.5  | 1-5           |
| Technical Complexity  | Solution Architect | × 1.0  | 1-5 (inverse) |

### Scale Definitions

**Security Risk**
- 5 = auth, PII, payment, public-facing sensitive data
- 4 = modifies security controls or adds external integration
- 3 = internal service with user data
- 2 = internal service, non-sensitive data
- 1 = read-only, no user data, fully internal

**Dependency Blocking**
- 5 = 4+ stories depend on this
- 4 = 3 stories depend on this
- 3 = 2 stories depend on this
- 2 = 1 story depends on this
- 1 = no dependencies

**Business Value**
- 5 = core feature, release cannot ship without
- 4 = high user value, strong stakeholder demand
- 3 = moderate value, planned in roadmap
- 2 = nice to have, low urgency
- 1 = minimal value, defer indefinitely

**User Impact**
- 5 = all users, every session
- 4 = majority of users, regularly
- 3 = subset of users, regularly
- 2 = small subset, occasionally
- 1 = edge case, rarely

**Testability Risk**
- 5 = many complex edge cases, hard to automate, high regression risk
- 4 = several edge cases, moderate automation complexity
- 3 = standard complexity, clear test cases
- 2 = simple, straightforward
- 1 = trivial, minimal test cases

**Technical Complexity** (inverse — higher complexity = lower priority concern)
- 5 = simple, well-understood
- 4 = moderate complexity
- 3 = significant complexity
- 2 = high complexity, multiple unknowns
- 1 = very high complexity, research needed

### Priority Classification
- Must Ship: score ≥ 70% of maximum possible
- Should Ship: score 40-69%
- Can Hold: score < 40%

### Override Rule
Compliance requirements bypass scoring entirely. Compliance stories are always Must Ship regardless of score.

## Outputs
Ranked priority table at `openspec/changes/sprint-{N}-priority/priority-table.md`

Format:

| Rank | Story | Score | Security | Dependency | Business | Impact | Testability | Complexity | Priority |
|------|-------|-------|----------|------------|----------|--------|--------------|------------|----------|

## Quality Gates
- [ ] All roles submitted scores for all stories
- [ ] Compliance stories marked Must Ship regardless of score
- [ ] Priority table committed to OpenSpec
- [ ] PM reviewed for conflicts before presenting to Edward

## References
- `.claude/skills/pm/task-prioritisation/SKILL.md`
- `.claude/skills/pm/sprint-planning/SKILL.md`
- `.claude/skills/pm/release-scope-management/SKILL.md`
