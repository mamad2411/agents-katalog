@prd.json @progress.txt

# CONTEXT

This is production code that will be maintained for years. Every shortcut becomes technical debt. Every pattern you establish will be copied. Fight entropy. Leave the codebase better than you found it.

# YOUR TASK

Work through the PRD items in prd.json. Each iteration, complete ONE task.

## 1. CHOOSE YOUR NEXT TASK

When selecting the next task, prioritize in this order:

1. Architectural decisions and core abstractions
2. Integration points between modules
3. Unknown unknowns and spike work
4. Standard features and implementation
5. Polish, cleanup, and quick wins

Do NOT just pick the first item. Pick the highest-priority incomplete item (where "passes": false).

## 2. KEEP CHANGES SMALL

- One logical change per commit
- If a task feels too large, break it into subtasks first
- Prefer multiple small commits over one large commit
- Run feedback loops after EACH change, not at the end
- Quality over speed. Small steps compound into big progress.

## 3. RUN ALL FEEDBACK LOOPS BEFORE COMMITTING

Before ANY commit, run ALL of these:

1. TypeScript: `npm run typecheck` (must pass with zero errors)
2. Tests: `npm run test` (must pass)
3. Lint: `npm run lint` (must pass)
4. Browser: If the work you have done effects the UI, then verify the results in the browser

Do NOT commit if ANY feedback loop fails. Fix issues first, then re-run all loops.

## 4. UPDATE PROGRESS

After completing each task, append to progress.txt:

- Task completed and PRD item reference
- Key decisions made and reasoning
- Files changed
- Any blockers or notes for next iteration

Keep entries concise. Sacrifice grammar for brevity. This file helps future iterations skip exploration.

## 5. UPDATE THE PRD

When a task is complete and all feedback loops pass:

- Set "passes": true for that PRD item in prd.json
- Commit both the code changes AND the updated prd.json and progress.txt

## 6. COMMIT YOUR WORK

Make a git commit with a clear message describing the feature/change.

## 7. SCOPE BOUNDARIES

What's in scope (be explicit):

- Files in: src/, tests/, lib/
- All user-facing AND internal commands
- Edge cases including: [list specific edge cases]

What's NOT in scope:

- Do not modify: [protected files/directories]
- Do not skip files just because they seem like "edge cases"
- Do not mark items complete by excluding them from coverage/scope

## 8. STOP CONDITION

If ALL PRD items have "passes": true, output:
<promise>COMPLETE</promise>

If you are blocked and cannot proceed, output:
<promise>BLOCKED</promise>
And explain what is blocking you in progress.txt.

# REMEMBER

- You choose the task, but you don't choose when "done" means done - the PRD does
- Never outrun your headlights - get feedback before moving on
- The codebase will outlive you. Code accordingly.
