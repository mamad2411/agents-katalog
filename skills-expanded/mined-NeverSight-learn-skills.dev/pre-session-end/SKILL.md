---
name: pre-session-end
description: Use this skill PROACTIVELY when the user indicates they are done working, ending the session, wrapping up, or saying goodbye. Also use when significant work has been completed and the user hasn't explicitly asked to continue. Analyzes the session to evolve skills/commands/agents and propagates useful project permissions to global settings.
---

# Pre-Session-End Skill

Run this skill before ending a Claude Code session to capture learnings and propagate useful settings.

## When to Activate

- User says: "done", "wrapping up", "ending session", "goodbye", "that's all", "I'm finished"
- Significant work completed without explicit continuation request
- User explicitly invokes `/pre-session-end`

## Workflow

### Step 0: English Correction

Before proceeding with other steps, provide a corrected or more natural version of the user's original prompt from this session.

**Format:**
```
## English Correction

**Original:** [user's original prompt]
**Corrected:** [corrected/more natural version]
[If changes are significant, add brief explanation of what was changed and why]
```

- Only include this section if corrections are needed
- Focus on grammar, word choice, and natural phrasing
- Keep explanations concise

### Step 1: Analyze Session for Learnable Patterns

Review the chat history and identify:

#### Skill Candidates
Patterns that could become reusable skills:
- Repeated workflows (e.g., "always run tests before commit")
- Problem-solving approaches that worked well
- Domain-specific knowledge applied multiple times
- Code patterns or architectures used consistently

#### Command Candidates
Operations that could become slash commands:
- Multi-step sequences performed repeatedly
- Common parameter combinations for tools
- Project-specific workflows

#### Agent Candidates
Specialized task patterns that could become agents:
- Complex multi-tool operations
- Tasks requiring specific expertise or context
- Recurring analysis or review patterns

### Step 2: Present Extracted Learnings

For each candidate, present to user:
```
**Potential Skill: [name]**
- Pattern observed: [description]
- Would save: [how it helps]
- Proposed location: ~/.claude/skills/learned/[name].md

Create this skill? [Yes/No/Edit]
```

### Step 3: Propagate Project Permissions to Global

1. Read project settings: `.claude/settings.local.json`
2. Read global settings: `~/.claude/settings.json`
3. Identify permissions in project but not in global

For each permission found only in project settings:

**Categorize the permission:**
- **Generic tool permissions**: `Bash(git:*)`, `Bash(npm:*)`, `Bash(docker:*)` → likely useful globally
- **Domain-specific web**: `WebFetch(domain:docs.example.com)` → ask user if generally useful
- **Project-specific paths**: Contains project directory paths → skip (not portable)
- **MCP server permissions**: `mcp__*` → ask user (may be project-specific)

**Present each selectively:**
```
**Permission found in project settings:**
`Bash(helm template:*)`

This permission allows: Running helm template commands
Currently: Project-only
Recommendation: [Useful globally / Project-specific]

Propagate to global settings? [Yes/No]
```

### Step 4: Apply Approved Changes

1. **For approved skills**: Create files in `~/.claude/skills/learned/`
2. **For approved permissions**: Update `~/.claude/settings.json`
3. Report what was applied

### Step 5: Session Summary

Provide a brief summary:
```
## Session Wrap-Up Complete

**Learnings captured:**
- [X] Created skill: skill-name
- [X] Created command: command-name
- [ ] Skipped: pattern-name (user declined)

**Permissions propagated:**
- [X] Bash(helm:*) → global
- [ ] WebFetch(domain:internal.corp) → kept project-only

**Ready to end session.**
```

## Important Notes

- **Never auto-apply**: Always get user confirmation for each change
- **Preserve existing**: Don't overwrite existing skills/settings without explicit approval
- **Be selective**: Only propose truly useful patterns, not every repeated action
- **Explain value**: For each proposal, explain why it's worth saving
