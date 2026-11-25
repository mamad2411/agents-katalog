---
name: github-pr-reviewer-aimemo
description: Review GitHub PRs with learned code style preferences using aimemo persistent memory
metadata: {"openclaw": {"requires": {"env": ["GITHUB_TOKEN"]}, "emoji": "🔍"}}
---

# GitHub PR Reviewer with aimemo Memory

This skill reviews GitHub Pull Requests and learns your code style preferences over time using aimemo's persistent memory.

## How It Works

1. **Loads learned preferences** from previous sessions
2. **Reviews PR** applying your established code style rules
3. **Stores new patterns** discovered during review
4. **Remembers feedback** you provide for future reviews

## Memory Integration

**CRITICAL**: This skill uses aimemo for persistent memory. Always pass `context: "github-pr-reviewer-aimemo"` to all memory tool calls.

### On Session Start

```
ALWAYS call memory_context FIRST before reviewing:
{
  "context": "github-pr-reviewer-aimemo"
}
```

This loads:
- Code style preferences
- Common patterns to watch for
- Previous feedback and corrections
- In-progress review tasks

### During Review

Store discoveries immediately:
```
{
  "context": "github-pr-reviewer-aimemo",
  "entities": [{
    "name": "code-style-preferences",
    "entityType": "preferences",
    "observations": ["New pattern you discovered"]
  }]
}
```

### On Session End

Write a journal entry:
```
{
  "context": "github-pr-reviewer-aimemo",
  "journal": "Reviewed PR #123. Updated: variable naming rules. Next: discuss error handling patterns with user."
}
```

## Instructions

When the user asks you to review a GitHub PR:

### Step 1: Load Memory (MANDATORY)

**Before doing ANYTHING else**, call:
```
memory_context({
  "context": "github-pr-reviewer-aimemo"
})
```

This gives you access to:
- User's code style preferences
- Previously identified anti-patterns
- Ongoing review tasks
- Past user feedback

### Step 2: Fetch PR Details

Use GitHub API or ask user for PR link. Retrieve:
- PR title and description
- Changed files and diffs
- Existing review comments
- PR metadata (author, labels, etc.)

### Step 3: Review Code

Apply learned preferences from memory:

**Code Style**:
- Check naming conventions (snake_case, camelCase, etc.)
- Verify indentation and formatting
- Look for trailing commas, semicolons based on preferences

**Patterns to Watch For**:
- Error handling (try/catch, early returns, explicit types)
- Code organization (file structure, imports)
- Comments and documentation
- Test coverage

**Anti-Patterns**:
- Check against known issues from memory
- Flag repeated mistakes user wants to avoid

### Step 4: Provide Review

Structure your review:

```markdown
## Summary
[High-level assessment: approve, request changes, or comment]

## Key Issues
[Critical problems that must be fixed]

## Style Observations
[Code style issues based on learned preferences]

## Suggestions
[Optional improvements]

## Positive Notes
[Things done well - reinforce good patterns]
```

### Step 5: Store New Learnings

**Immediately after review**, store:

**New Style Rules**:
```
memory_store({
  "context": "github-pr-reviewer-aimemo",
  "entities": [{
    "name": "code-style-preferences",
    "entityType": "preferences",
    "observations": ["User prefers early returns over deeply nested if-else"]
  }]
})
```

**New Patterns**:
```
memory_store({
  "context": "github-pr-reviewer-aimemo",
  "entities": [{
    "name": "error-handling-patterns",
    "entityType": "patterns",
    "observations": ["Wrap all database errors with custom AppError type"]
  }]
})
```

**Anti-Patterns to Flag**:
```
memory_store({
  "context": "github-pr-reviewer-aimemo",
  "entities": [{
    "name": "common-mistakes",
    "entityType": "anti-patterns",
    "observations": ["Don't use console.log in production code"]
  }]
})
```

### Step 6: Learn from User Feedback

If user corrects you or provides feedback:

```
memory_store({
  "context": "github-pr-reviewer-aimemo",
  "entities": [{
    "name": "user-corrections",
    "entityType": "feedback",
    "observations": ["User clarified: 'TODO' comments are acceptable in draft PRs"]
  }]
})
```

### Step 7: Session Summary

Before ending conversation:

```
memory_store({
  "context": "github-pr-reviewer-aimemo",
  "journal": "Reviewed PR #456 (auth refactor). Learned: user wants explicit error types. In progress: discussing naming conventions for API endpoints. Next: establish testing standards."
})
```

## Example Interaction

**User**: "Review PR #789"

**You**:
1. Call `memory_context({context: "github-pr-reviewer-aimemo"})`
2. Load: "User prefers snake_case, explicit error types, no trailing commas"
3. Fetch PR #789 details
4. Review code applying loaded preferences
5. Provide structured review
6. Store: "Discovered user wants constants in SCREAMING_SNAKE_CASE"
7. Journal: "Reviewed PR #789. Updated: naming conventions."

**User**: "Actually, trailing commas are fine in arrays"

**You**:
1. Call `memory_store({context: "github-pr-reviewer-aimemo", entities: [{name: "code-style-preferences", observations: ["Trailing commas are acceptable in arrays"]}]})`
2. Acknowledge: "Got it, I'll remember that for future reviews."

## Entity Types to Use

| Entity Type | Purpose | Examples |
|-------------|---------|----------|
| `preferences` | Code style rules | "Prefer snake_case", "4-space indent" |
| `patterns` | Good patterns to encourage | "Early returns", "Explicit error types" |
| `anti-patterns` | Bad patterns to flag | "Avoid console.log", "No hardcoded credentials" |
| `feedback` | User corrections | "TODOs OK in drafts", "Comments optional for simple functions" |
| `project-context` | Project-specific info | "This is a TypeScript monorepo", "Uses ESLint + Prettier" |
| `review-checklist` | Things to always check | "Test coverage", "Migration scripts", "Changelog updated" |

## Tags to Use

Organize observations with tags:
- `naming`: Variable/function/file naming
- `formatting`: Indentation, whitespace, line breaks
- `error-handling`: Try/catch, error types, logging
- `testing`: Test coverage, test quality
- `documentation`: Comments, README, API docs
- `security`: Auth, validation, secrets handling
- `performance`: Optimization, caching, queries

Example:
```
memory_store({
  "context": "github-pr-reviewer-aimemo",
  "entities": [{
    "name": "error-handling-rule-1",
    "entityType": "patterns",
    "observations": ["Always wrap third-party API errors"],
    "tags": ["error-handling", "best-practices"]
  }]
})
```

## Linking Related Entities

Connect related knowledge:
```
memory_link({
  "context": "github-pr-reviewer-aimemo",
  "from": "snake-case-preference",
  "relation": "conflicts-with",
  "to": "camel-case-in-json"
})
```

## Progressive Learning

**Session 1**: Learn basic preferences
- snake_case vs camelCase
- Indentation style
- Comment preferences

**Session 2-5**: Build pattern library
- Error handling approaches
- File organization
- Testing standards

**Session 6+**: Refine and specialize
- Project-specific patterns
- Team conventions
- Domain-specific rules

## Debugging

If memory seems incorrect:

**Check loaded context**:
```
memory_search({
  "context": "github-pr-reviewer-aimemo",
  "query": ""  // List all
})
```

**Update incorrect preference**:
```
memory_store({
  "context": "github-pr-reviewer-aimemo",
  "entities": [{
    "name": "code-style-preferences",
    "entityType": "preferences",
    "observations": ["CORRECTION: User prefers camelCase, not snake_case"]
  }]
})
```

**Search specific topic**:
```
memory_search({
  "context": "github-pr-reviewer-aimemo",
  "query": "error handling",
  "limit": 5
})
```

## Critical Rules

1. **ALWAYS use `context: "github-pr-reviewer-aimemo"`** - Never omit this
2. **Load memory FIRST** - Before reviewing any PR
3. **Store as you learn** - Don't wait until session end
4. **Write journal entries** - Help future you understand what was done
5. **Learn from corrections** - When user corrects you, store it immediately
6. **Use semantic names** - "code-style-preferences" not "data"
7. **Tag observations** - Makes searching easier later
8. **Link related entities** - Build a knowledge graph over time

## Skill Lifecycle

**First Use**: Skill has empty memory
- Ask user about basic preferences
- Store initial preferences
- Establish baseline standards

**Ongoing**: Build knowledge base
- Load preferences every session
- Store new patterns as discovered
- Refine rules based on feedback

**Mature**: Comprehensive style guide
- Understands full project conventions
- Catches subtle issues
- Provides consistent, personalized reviews

## Performance Tips

- Load memory once per session (beginning), not per PR
- Store discoveries after each PR, not all at end
- Use `memory_search` for specific lookups during review
- Journal entries help track long-term learning progress

---

**Remember**: The skill's value grows over time as it learns your preferences. Be patient in early sessions and correct mistakes - the skill will remember and improve.
