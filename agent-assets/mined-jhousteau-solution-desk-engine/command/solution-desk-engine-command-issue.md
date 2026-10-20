---
allowed-tools: Task, Bash(gh:*), Read, Grep
argument-hint: [action-term] [instructions]
description: Create GitHub issue from current context
model: claude-sonnet-4-20250514
---

## Create GitHub Issue

Analyze the current conversation context and create a well-scoped GitHub issue.

### Context Analysis
Current discussion: Review the conversation to understand what needs to be done
Arguments provided: $ARGUMENTS

Parse the arguments to extract:
- Action term (first word): feature, bug, refactor, optimize, deprecate, cleanup, docs, test, etc.
- Instructions (rest of arguments): specific details about what needs to be done

### Issue Creation Process

Use the issue-analyst agent to ensure proper scoping:

1. Extract the core problem or feature from context
2. Create atomic, testable issue
3. Define clear success criteria
4. Ensure single deliverable

### Issue Format

Use the action term from arguments to create appropriate issue:

```markdown
## Title
[{ACTION_TERM}] {Component}: {Specific Behavior}
Example: "feature: Add dark mode toggle to settings"
Example: "bug: Fix authentication timeout on mobile"
Example: "refactor: Extract payment processing into service layer"

## Description
Clear statement of what needs to be done based on the instructions provided

## Success Criteria
- [ ] Specific, testable requirement
- [ ] Observable behavior change
- [ ] Tests pass

## Scope
- IN: What's included
- OUT: What's explicitly not included

## Technical Notes
Any implementation hints or constraints
```

### Labels
Apply appropriate label based on action term:
- feature → "enhancement"
- bug → "bug"
- refactor → "refactoring"
- optimize → "performance"
- deprecate → "deprecation"
- cleanup → "cleanup"
- docs → "documentation"
- test → "testing"

### Command to Execute
```bash
gh issue create --title "TITLE" --body "BODY" --label "LABEL"
```

Return the created issue number for use in subsequent commands.
