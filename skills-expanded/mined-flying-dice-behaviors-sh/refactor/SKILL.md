---
skill: refactor
description: >-
  Iteratively refactor code by finding the single worst DRY or Single Responsibility violation anywhere in the project and fixing it. Runs one pass at a time so each fix can be reviewed before moving on.
---

## Goal

Find the **single worst offender** against DRY or the Single Responsibility Principle anywhere in the project, fix it, and stop. The user can re-invoke `/refactor` to continue iterating.

Always apply the clean-code skill (@.claude/skills/clean-code/) when writing the fix.

## Process

1. **Check existing TODOs** — Before scanning for new violations, grep the codebase for `// TODO:` comments that match the pattern `// TODO: <score> - <description>`. If any exist, skip the Scan and Analyse steps — pick the highest-scored TODO from the list, fix it, remove the TODO comment, and continue from step 5 (Verify).

2. **Scan** — Use a Sonnet agent to list all source files in the project (exclude `node_modules`, `dist`, build output, lockfiles, and other generated files). If the project is empty, tell the user and stop.

3. **Analyse** — Launch 2 parallel Sonnet agents across all source files:

   a. **DRY agent**: Read the source files. Identify duplicated logic — repeated code blocks, near-identical functions, copy-pasted patterns, or constants defined in more than one place. For each instance report: the files and line ranges involved, what is duplicated, and a severity score (1-10, where 10 is the most egregious).

   b. **SRP agent**: Read the source files. Identify Single Responsibility violations — functions/classes/modules that do more than one job, mixed I/O and logic, god components, "and" functions. For each instance report: the file and line range, what responsibilities are tangled, and a severity score (1-10).

4. **Rank** — Collect all findings from both agents. Pick the single highest-severity issue. If scores tie, prefer the one with the larger blast radius (more lines, more callers, harder to change later). If no issues score above 3, report "Nothing worth refactoring right now" and stop. For every issue that was identified but **not** fixed this pass, insert a `// TODO: <score> - <description>` comment at the violation site so future runs can pick them up directly without re-scanning.

5. **Fix** — Apply the fix following the clean-code skill principles. Keep the change minimal and focused — touch only what is needed to resolve this one violation. Do not fix other issues you noticed. Remove the `// TODO:` comment if one existed for this violation.

6. **Verify** — Run the project's lint/typecheck commands if they exist. If tests exist for the affected code, run them. If anything fails, fix it before reporting done.

7. **Commit & Push** — Stage all changed files, commit with a message in the format `refactor: <one-sentence summary of the fix>`, and push to the current branch.

8. **Report** — Show what was fixed using this format, then remind the user they can run `/refactor` again:

   ```
   ### Refactored

   **Violation**: DRY | SRP
   **Severity**: N/10
   **Location**: path/to/file.ts:L12-L45
   **Problem**: <one-sentence description>
   **Fix applied**: <one-sentence summary of what changed>
   ```

## Rules

- One fix per invocation. Do not chain multiple refactors.
- Never change behaviour. Refactoring is structure-only; inputs and outputs must stay identical.
- Never refactor test files unless the duplication is in the test files themselves.
- Any source file in the project is fair game.
- This is a hands-off operation. Do not ask for confirmation — analyse, fix, verify, and report.
