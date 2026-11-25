---
name: implement
description: "Use for implementing a piece of work based on a PRD or set of issues — orchestrates /tdd at pre-agreed seams, runs typechecking and tests regularly, dispatches /review at the end, and commits the completed work to the current branch. Explicit /implement invocation only. Trigger words: 实现, 编码实现, 开发这个需求, 开始写代码, implement these issues, orchestrate the build."
disable-model-invocation: true
---

# Implement: Workflow Orchestration

🥷 Implement from PRD or issues — orchestrate /tdd, test, review, commit.

Sequences the full implementation pipeline for a set of pre-agreed vertical slices: delegate to `/tdd` where testable, implement directly where not, run typechecking and tests after each seam, dispatch `/review` at the end, and commit per completed item.

## Outcome Contract

- **Outcome**: All items from the PRD's acceptance criteria or child issues are implemented, tested, reviewed, and committed.
- **Done when**: Each seam is GREEN (typecheck + tests pass), `/review` has been dispatched, and each item is committed.
- **Evidence**: Typechecker passes per item, test suite passes per item and in full, `/review` report produced, commits visible on current branch.
- **Output**: Summary of implemented items, commits made, test results, next step.

## Process Summary

**Step 0 — Quick assessment.** If the work is trivial (single file, one obvious change), recommend `/tdd` and stop — this skill is unnecessary overhead.

**Step 1 — Entry Protocol.** Apply the [Skill Entry Protocol](../rules/entry-protocol.md). Read project config (`docs/agents/`), domain docs (CONTEXT.md, ADRs, research INDEX), and the input work items (PRD or Issues from `/story`). Check upstream quality: if PRD Traceability shows `Created by: /story (minimal PRD)`, note that requirements may not be decision-complete; if `Grilled by` is empty, note the plan is unvalidated.

**Step 2 — Work Inventory.** List all items to implement:
- If Issues from `/story` exist — each issue is a seam
- If only a PRD — extract Acceptance Criteria as work items
- Sort by dependency order (blocked-by relationships from `/story`)
- Update PRD Status from `Sliced` to `In Progress` in the PRD's status line

**Step 3 — Implement each seam.** For each work item in dependency order:

1. **Assess TDD suitability** — does this item have clear acceptance criteria testable at a public interface boundary? (See [REFERENCE.md §TDD Suitability](REFERENCE.md))
2. **If suitable** — call the Skill tool with "tdd" for this item. Put the implement workflow aside, execute tdd's full cycle (Steps 1-4) for this item, then resume here.
3. **If not suitable** — implement directly, writing tests alongside code.
4. **Typecheck** — run the project's typechecker. If it fails, fix before proceeding.
5. **Test** — run the test suite for this item / changed files. All must pass.
6. **Commit** — commit with a descriptive message referencing the issue (format: `[PRD-NNNN] <seam description> — <summary>`).

Update the issue's status in the PRD's `Sliced into` list to `— Done`.

**Step 4 — Full test suite.** After all items are implemented, run the full test suite. If anything fails, return to the affected item and fix.

**Step 5 — Recommend /review.** Present the completed changes and instruct: "Next: Run `/review` to review all changes before merge."

**Step 6 — Output.** Produce summary of implemented items, commits made, test results.

See [REFERENCE.md](REFERENCE.md) for detailed step instructions, TDD suitability checklist, direct implementation guidelines, and recovery procedures.

## Gotchas

| What happened | Rule |
|---|---|
| /tdd was run on an item that had unclear requirements | REFERENCE §3a: assess TDD suitability first — /tdd requires clear, testable acceptance criteria |
| Tests failed after direct implementation | Step 3.5: run tests per item immediately — don't batch all changes before testing |
| Typechecker not configured for the project | Step 3.4: detect typechecker from project config (tsconfig, pyproject.toml, etc.); if none, skip and note the gap |
| Work items had hidden dependency on incomplete items | Step 2: read blocked-by relationships from `/story` issues; implement in dependency order |
| /tdd was cancelled mid-cycle by the user | REFERENCE §3b: resume from last completed /tdd phase; if no completed phases, move item to direct implementation |
| Commit conflicts with uncommitted work not from this session | Step 3.6: warn user about existing dirty state; ask how to handle before committing |
| PRD Traceability shows ungrilled or unsliced state | Step 1: flag the gap in output but proceed — implement is not blocked by missing upstream steps |
| User expected /review to run automatically | Step 5: dispatch /review as a recommendation (per no-auto-chain convention); do not auto-run it |

## Output

```
Implement complete.

**Work items:**
* <issue-#N / PRD acceptance criterion> — /tdd | direct — commit <hash>
* <issue-#M / PRD acceptance criterion> — /tdd | direct — commit <hash>

**PRD**: PRD-NNNN — Status: In Progress

**Full test suite**: <pass / N failures>

**Next**: Run /review to review all changes before merge.
```
