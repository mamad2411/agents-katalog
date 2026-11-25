---
name: review-fix-gemini
description: Run Gemini CLI review against the current branch, fix only the review comments that are still valid for the current codebase, and leave invalid comments unchanged.
allowed-tools: Bash(bunx:*)
---

# Review workflow

1. Run the following command from the repository root with 1 hour timeout: `bunx @willbooster/agent-skills@latest review --agent gemini`
2. Treat the returned review results as the candidate comment set to process. If the command returns `There is no concern.`, quit without modifying code.
3. For each returned review comment, judge whether it is still valid in the current codebase.
4. Fix only the comments you judged valid, and leave invalid comments unchanged.
5. After applying fixes, run the smallest relevant verification commands for the changed code.
