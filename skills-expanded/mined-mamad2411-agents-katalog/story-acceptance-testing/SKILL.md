# Story Acceptance Testing

## Purpose
PO validates business logic correctness of a deployed user story in UAT from a user/business perspective (not technical).

## Role
Product Owner

## Phase
UAT

## Triggered By
`/approve-story` deploys story to `uat-{KAN-N}.uat.internal`.

## Inputs
- User Story AC from kanban card
- UAT environment URL

## Key Distinction
NOT testing code quality — that is QA's job. TESTING business outcomes — does this behave as the business intended?

## Process
1. Read User Story AC from kanban card.
2. Access UAT environment: `uat-{KAN-N}.uat.internal`.
3. Test each AC from a real user perspective.
4. Test domain-specific edge cases from business knowledge.
5. Test end-to-end workflow completeness: can a real user complete this flow without confusion?
6. Document findings per AC:
   - PASS: business logic correct
   - FAIL: describe expected vs actual behaviour
7. All pass → add label `po: uat-approved` to story PR.
8. Any fail → create bug kanban card: `type: bug-story`, `area: business-logic`, severity `critical` if it blocks the workflow, `low` if edge case.

Note: PO tests in parallel with QA — do not block each other.

## Outputs
`po: uat-approved` label OR bug card(s) in kanban.

## Quality Gates
- [ ] Every AC tested from user perspective
- [ ] Domain edge cases tested
- [ ] Either uat-approved label added or bug cards created
- [ ] Not testing code quality (that is QA's domain)

## References
- `.claude/skills/qa/` (parallel UAT testing)
- `.claude/skills/pm/kanban-board-management/SKILL.md`
