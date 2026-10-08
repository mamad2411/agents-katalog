---
name: po
description: Product Owner - scans codebase and creates or amends GitHub issues with PRD. Use when: PRD, feature, issue, create issue, amend issue, what should we build, plan feature, design feature, scope, requirements.
---

# Product Owner

**Scan the codebase, write a PRD, and open a GitHub issue.**

## Usage

- `/po <prompt>` - Create a GitHub issue from the given feature description
- `/po <prompt> --priority <P0|P1|P2|P3>` - Create issue with explicit priority
- `/po` - Ask user what to build, then create the issue
- `/po amend <issue_number> <summary>` - Append a revision to an existing issue

If no `--priority` is given, ask the user which priority to assign.

## Workflow

1. **Scan the codebase** to understand current state:
   - Read relevant context modules (Blog, Import, Export)
   - Explore relevant source files for what's already implemented
   - Identify gaps, dependencies, and integration points
2. **Write the PRD** as the issue body (no local file)
3. **Create GitHub issue** with conventional title and PRD body

## Issue Title

Conventional format:

```
feat(<context>): <short description>
```

Examples:
- `feat(blog): add article pinning`
- `feat(export): add rss feed generation`
- `fix(import): handle rate limiting from dev.to api`

Rules:
- Lowercase after prefix
- Present tense imperative ("add", not "added")
- Under 70 characters
- Context name matches domain area (blog, import, export, web)

## Issue Body (PRD)

```markdown
## Overview
What we're building and why.

## Problem Statement
What user problem does this solve?

## Current State
What already exists in the codebase relevant to this feature.

## Requirements
- [ ] R-1: Description

## Technical Approach
- Affected modules
- Data flow changes
- Database changes if any

## Acceptance Criteria
Given/When/Then scenarios.

## Out of Scope
What we're explicitly NOT doing.
```

## Creating the Issue

```bash
gh issue create \
  --title "feat(<context>): <description>" \
  --body "$(cat <<'EOF'
<PRD content>
EOF
)" \
  --label "prd" \
  --label "P2: medium"
```

Report the issue URL to the user when done.

## Amending an Issue

When called with `/po amend <issue_number> <summary>`, append a revision to the existing issue. **The original PRD is immutable** — never edit or overwrite it.

Append a `## Revision <N>` block with changes, updated requirements, and removed/deferred items.

## Pipeline

```
/po <prompt> -> GitHub issue -> /dev -> /review -> /commit -> /pr
```
