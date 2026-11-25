---
name: version-control-best-practices
description: >
  Use when managing versions of code, documentation, knowledge, or configuration.
  This skill provides standardized version control practices across all repositories
  and knowledge stores, ensuring consistency, traceability, and recoverability.
---

# Version Control Best Practices

## Overview
This skill defines version control standards for all work products beyond just git - including documentation versions, knowledge entries, configuration, and data. Consistent version control practices enable traceability, recovery, and collaboration.

## When to Use
- When committing any change to shared repositories
- When creating versions of documents, knowledge entries, or configurations
- When branching, merging, or managing parallel work streams
- When tagging releases or important milestones
- **Don't use when:** Working only on local drafts not yet ready for shared storage

## Core Procedures

### Step 1: Commit Standards
Every commit must have:
- **Clear message:** Start with verb, describe WHAT changed and WHY (not just "update" or "fix")
- **Atomic:** One logical change per commit (don't mix unrelated changes)
- **Attributed:** Correct author information
- **Tested:** Don't commit known-broken code to shared branches

Message format:
```
[type]: brief description

Detailed explanation if needed.

Related: [ticket/issue number if applicable]
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `config`, `knowledge`

### Step 2: Branch Strategy
- **main/master:** Always deployable, protected branch
- **develop:** Integration branch for features (if using gitflow)
- **feature/name:** One branch per feature or task
- **hotfix/name:** Urgent fixes to production
- **release/version:** Stabilization before release
- Branch names use lowercase-with-dashes

### Step 3: Version Numbering
Use semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR:** Breaking changes that require user action
- **MINOR:** New features that are backward compatible
- **PATCH:** Bug fixes and minor improvements

For documentation/knowledge:
- Major structural rewrites
- New content sections added
- Corrections, clarifications, updates

### Step 4: Knowledge Versioning
For non-code assets (knowledge, documentation):
- Track version in document frontmatter
- Maintain changelog at top of significant documents
- Use tags to mark: current, deprecated, archived, experimental
- Never delete, only supersede or archive

### Step 5: Merge and Review
- Never push directly to main (if protected)
- Create pull request or merge request for all changes
- At least one reviewer for significant changes
- Resolve all conflicts before merging
- Delete branches after merging

## Quality Checklist
- [ ] All commits follow message format
- [ ] Branch naming follows convention
- [ ] Version numbers follow semantic versioning
- [ ] No broken code committed to shared branches
- [ ] All merges are reviewed before completion
- [ ] Old versions properly archived, not deleted

## Error Handling
- **Error:** Accidentally committed secrets or sensitive data
  **Response:** Immediately revoke secret, force push to rewrite history, rotate all potentially exposed secrets
- **Error:** Merge conflict in critical file
  **Response:** Don't force merge, get input from both authors, ensure both intents preserved
- **Error:** Committed broken code to main
  **Response:** Revert immediately, fix on separate branch, improve guardrails to prevent recurrence

## Cross-Team Integration
**Related Skills:** finishing-a-development-branch, using-git-worktrees, requesting-code-review, knowledge-capture
**Used By:** ALL agents working with shared repositories, especially developers, documenters, knowledge managers