---
name: claude-rules-link
description: Link the user's shared, path-scoped Claude rules (~/.claude/shared-rules) into the current project so they lazy-load via paths: frontmatter instead of loading globally every session. Use when setting up a new project/repo on this machine, when rules aren't applying in a project, or when the user asks to "add the shared rules", "link claude rules", or "set up rules here".
tags: [claude-code, rules, setup, symlink, onboarding]
---

# Link Shared Claude Rules into a Project

Path-scoped rules live in `~/.claude/shared-rules/` and stay out of the global startup context (that's the whole point — they reduce per-session token overhead). A rule only loads when Claude reads a file matching its `paths:` frontmatter, **and** only when the rules directory is discovered at the project level. This skill creates that project-level link.

It symlinks the shared rules into `<project>/.claude/rules/shared` (the symlink-to-shared-dir pattern that Anthropic documents and that is confirmed to honor `paths:` frontmatter correctly), then gitignores the link so it doesn't dangle on teammates' checkouts.

## Usage

```
/claude-rules-link            # links into the current directory
/claude-rules-link <path>     # links into a specific project directory
```

## What to do

1. Run the bundled script against the target project (default: current working directory):

   ```bash
   bash ~/.claude/skills/claude-rules-link/scripts/link-rules.sh "${1:-$PWD}"
   ```

2. Report the script's output to the user — specifically whether it linked, repaired an existing link, was already correct, or refused to clobber a real file.

3. If the script reports the project is not a git repo, mention that the `.gitignore` step was skipped (the symlink still works; it just won't be ignored if the directory later becomes a repo).

## Notes

- **Idempotent.** Safe to run repeatedly. It only repoints a wrong symlink or creates a missing one; it never overwrites a real file or directory at `.claude/rules/shared`.
- **Per machine.** The symlink targets an absolute path under the user's home, so it is intentionally gitignored and must be re-created on each machine/clone (just run this skill again).
- **Always-loaded rules are separate.** Any rules in `~/.claude/rules/` load every session regardless of this link.
- **Verify it loaded.** After linking, open a file matching one of your shared rules' `paths:` patterns to confirm the rule loads.
