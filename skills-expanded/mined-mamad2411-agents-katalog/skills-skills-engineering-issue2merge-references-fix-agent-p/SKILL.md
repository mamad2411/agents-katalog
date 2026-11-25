# Fix Sub-agent Prompt Template

Read this reference at Step 2 when constructing Fix sub-agent tasks.

## Required Skills (loaded automatically)

| Skill | Purpose | Location |
|-------|---------|----------|
| **coding-agent-common** | Delegates coding to Codex/Claude Code/OpenCode for bug fixes, refactoring, iterative coding | `workspace/skills/coding-agent-common/` |
| **coding** | Coding style memory — ensures fixes match your preferences, conventions, and patterns | `workspace/skills/coding/` |

## How to use these skills

### coding-agent-common
When the Fix sub-agent needs to implement code changes (especially multi-file fixes):
1. The `coding-agent-common` skill will auto-trigger when the agent detects coding activity
2. It provides guidance on delegating to the best available coding agent (Codex for speed, Claude Code for complex fixes)
3. The agent reads the affected files, plans the fix, and implements changes
4. After fixing, the code is ready for review. Do NOT write tests — a dedicated Test sub-agent handles that later.

### coding (style memory)
- The `coding` skill will auto-trigger to apply your established coding conventions
- Every fix automatically respects your naming, formatting, and structural preferences
- No need to manually invoke — it loads when the agent starts editing code

### Interaction with code-review skill
- The Review sub-agent will audit fixes using the **code-review** skill (checklists + severity labels)
- Fix sub-agents should NOT self-review — focus purely on implementation

## Template

```javascript
sessions_spawn({
  task: `## Fix Sub-agent: Group {GROUP_ID}

## Working directory (cwd)
{REPO_PATH}

## Required skills
This sub-agent MUST use:
1. **coding-agent-common** (workspace/skills/coding-agent-common/) — for implementing code fixes
2. **coding** (workspace/skills/coding/) — to follow established coding conventions

## Task
Fix the following issues in this group using the coding-agent-common skill.

## Issues to fix
{FROM ISSUE BODY — extract this group's issues with full context}

## Instructions
1. Read each affected file before editing
2. Use **coding-agent-common** skill to plan and implement fixes
3. The **coding** skill will automatically apply coding conventions
4. Fix ALL issues assigned to this group
5. **Lightweight test verification:** After making changes, run tests for ONLY the affected modules/files (not the full suite). This catches obvious regressions before Review. A dedicated Test sub-agent will write proper integration tests later. Use:
   ```bash
   cd {REPO_PATH}
   SECRET_KEY=test python -m pytest -v --tb=short -k "<affected_module_or_file_keyword>" --ds=config.settings.dev 2>&1 | tail -n 30
   ```
   If any affected test fails, fix it before reporting back. The full test suite will be run by the Review sub-agent.
6. **Commit changes:** After all fixes pass lightweight tests, commit the changes so the manager can see what was done:
   ```bash
   cd {REPO_PATH}
   git add -A
   git commit -m "fix({ISSUE_NUMBER}): {GROUP_ID} — {short description of fixes}"
   ```
   If nothing changed (no files modified), skip the commit.
7. Report back with the retrospective format below

## Retrospective format
=== RETROSPECTIVE ===
1. Files read
2. Issues fixed (id + description)
3. Files changed and what was changed
4. Difficulties or risks encountered
5. All assigned issues fixed? (Yes/No + reason)
=== END RETROSPECTIVE ===

## Save retrospective
After reporting back, WRITE the retrospective to:
```
~/.openclaw/workspace/memory/{YYYY-MM-DD}-{HH-MM}-{ISSUE_NUMBER}-fix-group-{GROUP_ID}.md
```
Example: `~/.openclaw/workspace/memory/2026-05-14-22-49-384-fix-group-A.md`
`,
  cwd: "{REPO_PATH}",
  runtime: "subagent",
  mode: "run"
})
```

## Rules

- Timeout: 0 (never timeout)
- Each fix agent receives ONLY its own group's issues
- Include full issue context so the agent doesn't need to re-fetch GitHub
- **Must use** coding-agent-common for implementation (do not edit files directly with basic edit tools)
- coding style memory will auto-apply conventions
- Do NOT self-review — the Review sub-agent handles that with the code-review skill
- **Do NOT write tests** — a dedicated Test sub-agent handles test creation after Review passes
- **⛔ Do NOT run git checkout, pull, or push** — the Manager handles these. You MAY run `git add` + `git commit` after fixing to checkpoint your work.
- **Run lightweight tests** for affected modules only (see Instructions step 5). The Review sub-agent will run the full test suite.
- **Save retrospective** to `~/.openclaw/workspace/memory/{YYYY-MM-DD}-{HH-MM}-{ISSUE_NUMBER}-fix-group-{GROUP_ID}.md`
