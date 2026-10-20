> ⚠️ PROJECT SCOPED: Move files within .claude/tasks/ only.

Mark current task as done, then review quality.

## Finish

1. Read files in .claude/tasks/inprogress/
2. Identify task from context or ask
3. Get developer name from .claude/settings.local.json or git config
4. Update task file: Completed By, Completed Date, check off acceptance criteria, add Summary
5. Move: .claude/tasks/inprogress/ → .claude/tasks/done/
6. Save log to .claude/tasks/logs/YYYY-MM-DD-[title].md
7. Suggest git commit message for team

## Auto-review

8. Read .claude/skills/_base.md ← rules + patterns to check against
9. Check rules from .claude/memory/rules.md were followed
10. Check correct patterns were used
11. Check error handling is correct
    Report: ✅ Pass / ❌ Fail per check. Flag any new gotchas or patterns to log.

Confirm task moved. Remind: commit and push so team sees it is done.
