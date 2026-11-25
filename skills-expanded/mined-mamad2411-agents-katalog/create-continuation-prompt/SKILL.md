---
name: create-continuation-prompt
description: Creates a continuation prompt and posts to the console for easy context clearing and resume
---

# Create Continuation Prompt

Generates a concise continuation prompt that captures the current session state, enabling seamless context clearing and session resumption.

## Purpose

When context windows fill up or sessions need to be restarted, this skill creates a self-contained prompt that includes:
- Current task/objective
- Progress made so far
- Next steps
- Relevant file paths and locations
- Key decisions or constraints

## Output Format

The continuation prompt is displayed as raw markdown, optimized for copy-paste into a new session.

## Usage

```
/create-continuation-prompt
```

## What Gets Included

**Essential Information:**
- Current working objective
- Files modified or created (with paths)
- Key decisions made
- Blockers or open questions
- Next immediate action

**Excluded Information:**
- Long code snippets (use file paths instead)
- Verbose explanations (keep concise)
- Completed context (focus on what's next)

## Example Output

```markdown
Continue working on auth implementation:

**Progress:**
- Added JWT validation to `src/api/handlers/auth.ts`
- Tests passing in `src/api/handlers/auth.test.ts`

**Next:**
- Add refresh token endpoint
- Update routes in `src/api/routes.ts:45`

**Constraint:** Only use jsonwebtoken library (no other auth libs)
```

## Best Practices

1. **Keep it concise** - Aim for <10 lines
2. **Use file paths** - Reference code locations instead of copying code
3. **Focus forward** - Emphasize next steps over past work
4. **Include constraints** - Remind of critical rules or decisions
5. **Link resources** - Include relevant URLs, PRs, or issue numbers

## When to Use

- Context window approaching limits
- Switching between different work streams
- Before ending a work session
- After completing a milestone (to start fresh)
- When debugging requires a clean slate

## Integration

Use alongside:
- Git commits (for checkpoint history)
- Task tracking (for broader project context)
- Documentation updates (for permanent records)
