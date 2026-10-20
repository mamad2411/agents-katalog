Run a code review on recent changes using the **reviewer** agent.

## Steps

1. Delegate to the `reviewer` agent.
2. It runs `git diff` and `git diff --cached`, reads each modified file in full, and checks the changes against the app's conventions (`.claude/rules/`).
3. Report findings grouped by severity: Errors > Warnings > Suggestions.
4. Summarize with a pass / fail verdict.
