---
name: create-issue
description: Create a structured GitHub issue with proper context, acceptance criteria, and labels. Gathers context from code, docs, and conversation before drafting. Use when the user mentions "create issue", "open issue", "new issue", "file issue", "report bug", "feature request", or wants to create a GitHub issue.
---
<!-- Generated from .agents/ by scripts/sync-ai-workspace.mjs. Do not edit directly. -->


# Create Issue

Structured workflow for creating GitHub issues. Gathers context from the codebase, conversation, and docs to produce well-formed issues with acceptance criteria, labels, and cross-references.

## Critical Rules

1. **CONTEXT FIRST**: Investigate the codebase before writing the issue — reference specific files, functions, and patterns
2. **ACCEPTANCE CRITERIA ARE MANDATORY**: Every issue must have testable acceptance criteria
3. **NO DUPLICATE ISSUES**: Search for existing issues before creating
4. **LINK RELATED WORK**: Reference related issues, PRs, and code locations
5. **COMMENT PREFIX**: If posting follow-up comments, start with `**[Claude Code]:**`

---

## Instructions

### Step 1: Determine Issue Type

From the user's request, classify the issue:

| Type | Template | Labels |
|------|----------|--------|
| `bug` | Bug report with repro steps | `bug` |
| `feature` | Feature request with scope | `enhancement` |
| `task` | Implementation task (often from PR triage or planning) | `task` |
| `chore` | Maintenance, cleanup, tech debt | `chore` |

If unclear, ask the user.

### Step 2: Search for Duplicates

Search existing issues to avoid duplicates:

Search existing issues using the available GitHub tools (query: `repo:{owner}/{repo} {keywords from the issue}`). Check both open and recently closed issues.

If potential duplicates found:

```
Found potentially related issues:
- #{number}: {title} ({state})
- #{number}: {title} ({state})

Is this a duplicate, or should we create a new issue? (new/duplicate of #N/related to #N)
```

### Step 3: Gather Context

Investigate the codebase for relevant context:

1. **Search code** — grep/glob for related files, functions, patterns
2. **Read docs** — check `docs/` for relevant architecture or guides
3. **Check git history** — recent changes in the affected area
4. **Check related issues/PRs** — cross-reference for context

Present your findings:

```
Context gathered:
- Affected area: {files/modules}
- Related docs: {doc paths}
- Related issues: {#numbers}
- Current behavior: {what happens now}
- Relevant patterns: {what the codebase already does}
```

### Step 4: Draft the Issue

Present a draft to the user for review:

```
Draft Issue:

Title: {concise title, under 70 characters}
Labels: {labels}
Milestone: {if applicable}

---

## Summary
{1-3 sentences describing the issue}

## Context
{relevant background — affected files, current behavior, related issues}

## Acceptance Criteria
- [ ] {specific, testable criterion}
- [ ] {specific, testable criterion}
- [ ] {specific, testable criterion}

## Notes
{implementation hints, links to docs, constraints}

## Related
- #{number} — {brief description of relationship}
---

Review this draft. Any changes? (Y to create/edit instructions)
```

**Draft quality checklist:**
- Title is specific and actionable (not "Fix bug" or "Update code")
- Summary explains the **why**, not just the what
- Acceptance criteria are testable — someone can check each box and know it's done
- Context references actual code locations when applicable
- No acceptance criteria that duplicate what other issues already track

### Step 5: Create the Issue

Once the user approves:

```bash
gh issue create \
  --title "{title}" \
  --label "{label1},{label2}" \
  --body "{body}" \
  2>&1
```

Or create the issue using the available GitHub tools (owner, repo, title, body, labels).

### Step 6: Post-Creation

After creating:

1. **Report the issue URL** to the user
2. **Link to related issues** — if the issue references other issues, add a comment on those issues noting the new one
3. **Create a branch** if the user wants to start working immediately:
   - Branch name: `{issue-number}-{slug}` (e.g., `394-add-missing-skills`)
   - `git checkout -b {branch} origin/main && git push -u origin {branch}`

```
Created: #{number} — {title}
URL: {url}
Labels: {labels}

Want me to create a branch and start working on this? (Y/N)
```

## Checklist

- [ ] Issue type determined
- [ ] Duplicate search completed
- [ ] Codebase context gathered
- [ ] Draft reviewed by user
- [ ] Issue created on GitHub
- [ ] Related issues cross-linked
- [ ] Branch created (if requested)
