# Custom Commands

> ⚠️ PROJECT SCOPED: Save to .claude/commands/custom/ only.
> All custom commands use r- prefix.

## Template

Create: .claude/commands/custom/r-[name].md

Content:
---

> ⚠️ PROJECT SCOPED: All reads and writes stay within .claude/ only.
> [Exact instructions for Claude to execute when this command is typed]

---

## To add a custom command

/r-task create custom command /r-[name] that does [description]

## Ideas

- /r-deploy → your deployment steps
- /r-test → run test suite your way
- /r-migrate → database migration workflow
- /r-seed → database seeding workflow
- /r-lint-fix → auto fix linting issues
