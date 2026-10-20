---
name: test-cases-from-requirements
description: Turn requirements or user stories into a test case table with steps, data, expected results, priority, type, traceability matrix and coverage summary. Use when the user asks for test cases, test scenarios, a QA checklist, or UAT scripts.
---

# Test Cases from Requirements

## Inputs
- User stories with acceptance criteria (Gherkin or bullets)
- BRD/FRD sections, client emails, change requests
- UI field lists, API specs, business rules tables
- Optional: existing test suite (to avoid duplicates and reuse IDs)

Several sources: merge by requirement ID. When sources conflict (story vs spec), write tests for the documented rule, mark them "Blocked: conflict" and list the conflict under Needs input.

## Defaults (ask vs assume)
| Setting | Default if not stated | Options |
|---|---|---|
| Level | Functional (system/UAT) | Unit · API · UAT · Regression |
| Output | Markdown tables | Markdown · CSV (same columns) for Excel/TestRail/Xray |
| ID prefix | TC-ModuleCode-001 (e.g. TC-EDO-001) | User's scheme |
| Depth | Positive + negative + boundary for every rule; security for auth/data | Smoke only |
| Automation hint | Off | On: add Playwright hand-off (`references/playwright-handoff.md`) |

Ask one question only if a business rule has no limits and the answer changes the test data. Otherwise assume, mark the assumption, and continue.

## Steps
1. Read all input once. List each testable rule/criterion with its ID (REQ-/story ID or AC-1, AC-2).
2. For each rule, pick techniques from `references/techniques.md`: equivalence partitioning for inputs, boundary values for limits, decision table for rule combinations, state transition for status flows (e.g. AWB: Booked, RCS, DEP, ARR, DLV).
3. Write test cases: ID, title, preconditions, steps, test data, expected result, priority, type (Positive / Negative / Boundary / Edge / Security), requirement ID.
4. Add security cases where there is login, roles, file upload, or personal/commercial data (authorization, injection, data leakage between customers).
5. Build the traceability matrix: every requirement against its test IDs.
6. Write the coverage summary: counts by type and priority, uncovered requirements, assumptions.
7. If automation hint is on, add the hand-off block from `references/playwright-handoff.md`.
8. Fill `templates/testcase-template.md`. See `templates/example-testcases.md` for a filled example (fake data).
9. Run the self-check and fix before returning.

## Format
Use `templates/testcase-template.md`: Scope line, Test case table, Traceability matrix, Coverage summary, (optional) Automation hand-off, Assumptions & Needs input.

## Rules
- **Branding only on request:** use plain, neutral formatting by default. Apply a company or brand design skill (colours, fonts, logo, templates) only when the user names that skill or brand in the request; never pick one automatically.
- Never invent business limits, error messages or field names; mark assumed values "(assumed)" and list them under Needs input.
- Keep requirement IDs, field names, codes and message types exactly as given.
- One expected result per verifiable outcome; no "works correctly" or "as expected".
- Steps are numbered, one action each; test data is concrete and clearly fake (AWB 000-00000000).
- Every requirement has at least one Positive and one Negative case, or is marked "Not testable: reason".
- Priority: High = money, compliance, data integrity, main flow; Medium = alternate flows; Low = cosmetic.
- Empty section: write "None". Never delete a section.

## Self-check
- [ ] Every requirement in the traceability matrix; gaps listed as uncovered
- [ ] Each rule with a limit has boundary cases (min-1, min, max, max+1)
- [ ] Status flows have valid and invalid transitions
- [ ] Security cases present where auth or data exposure applies
- [ ] No vague expected results
- [ ] Assumed values marked and listed under Needs input
- [ ] Coverage counts match the table

## Output
Return the test pack from `templates/testcase-template.md`, then an **Assumptions & Needs input** block (defaults, assumed limits/messages, conflicts, untestable items).

After edits to this skill, rerun `evals/test-cases.md`.
