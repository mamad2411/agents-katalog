---
name: claude-skill-surgical-changes
description: Premium Claude Skill - Surgical Changes. Ensures edits are precise and minimally invasive. Matches existing style and avoids unrelated refactoring.
license: MIT
---

# Surgical Changes (Claude Skill)

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- **Don't "improve" adjacent code.** Avoid touching comments or formatting unrelated to the task.
- **Don't refactor what isn't broken.** Keep the diff clean and focused.
- **Match existing style.** Even if you prefer a different pattern, follow the project's lead.
- **Report unrelated dead code.** Mention it in the output instead of deleting it unless asked.

When your changes create orphans:
- **Clean up your own mess.** Remove imports, variables, or functions that YOUR changes made unused.
- **Leave pre-existing dead code alone.** Unless explicitly requested to clean it up.

**The test:** Every changed line should trace directly to the user's request.
