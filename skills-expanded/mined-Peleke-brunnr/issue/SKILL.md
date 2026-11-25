---
name: issue
description: Draft well-structured GitHub issues with clear titles, structured descriptions, acceptance criteria, and appropriate labels. Use this skill when a user asks to create, write, or draft a GitHub issue, bug report, feature request, task ticket, or RFC/proposal. Also use when a user asks to file an issue, open a ticket, or report a bug.
metadata:
  openclaw:
    emoji: "\U0001F3AB"
    requires:
      bins: ["gh"]
---

# GitHub Issue Drafting

Draft comprehensive GitHub issues that are actionable, well-scoped, and easy for contributors to pick up.

## Workflow

1. **Gather context** -- Understand what the user wants to report or request
2. **Classify the issue type** -- Bug report, feature request, task, or RFC/proposal
3. **Draft the issue** -- Apply the appropriate structure from `references/issue-templates.md`
4. **Refine** -- Suggest labels, link related issues, and tighten scope

## Step 1: Gather Context

Before drafting, establish:

- **What happened or what is needed?** Get the core problem or request.
- **Who is affected?** Users, developers, specific teams.
- **What is the impact?** Severity, frequency, blocking status.
- **Is there existing context?** Related issues, PRs, Slack threads, error logs.

If the user provides minimal context, ask targeted questions. Do not ask more than 3-5 questions at once. If the user provides rich context (error logs, reproduction steps, design ideas), proceed directly to drafting.

When working in a codebase, use available tools to gather context:
- Read relevant source files to reference specific code paths
- Check git log for recent changes related to the issue
- Search for existing issues or TODOs in the codebase

## Step 2: Classify Issue Type

Select the type based on the user's intent:

| Signal | Type |
|--------|------|
| Something is broken, wrong output, crash, error | **Bug report** |
| New capability, improvement, user-facing change | **Feature request** |
| Internal work, refactor, chore, migration | **Task** |
| Architectural change, needs team input, multiple valid approaches | **RFC/proposal** |

If ambiguous, default to **task** for internal work or **feature request** for user-facing work. Ask the user only if the classification materially changes the issue structure.

## Step 3: Draft the Issue

Load `references/issue-templates.md` and apply the template for the classified type.

### Writing Good Titles

Titles are the most-read part of any issue. Follow these rules:

- **Start with a verb** for bugs and tasks: "Fix", "Add", "Update", "Remove", "Migrate"
- **Start with a noun or area** for features and RFCs: "Authentication: support SSO", "API: rate limiting strategy"
- **Be specific, not vague:** "Fix null pointer in UserService.getProfile when email is missing" not "Fix bug in user service"
- **Include the affected component** when the repo has multiple areas: "[api] Fix 500 on /users/me with expired token"
- **Stay under 72 characters** when possible

**Bad titles:**
- "Bug" / "Fix issue" / "Update code" / "Improvement"
- "It doesn't work" / "Something is wrong with login"

**Good titles:**
- "Fix crash when uploading files larger than 10MB"
- "Add dark mode support to settings page"
- "Migrate user sessions from Redis to PostgreSQL"
- "RFC: Replace REST API with GraphQL for mobile clients"

### Structural Guidelines

Apply these regardless of issue type:

**Description section:**
- Lead with the most important information. A reader should understand the issue from the first two sentences.
- Use concrete, observable facts. Replace "sometimes fails" with "fails on 3 of 10 attempts with error X".
- Include code references as links or path+line when relevant: `src/api/auth.ts:42`

**Acceptance criteria:**
- Every issue needs at least one acceptance criterion.
- Phrase criteria as checkboxes: `- [ ] Criterion here`
- Each criterion must be independently verifiable. "Works correctly" is not a criterion. "Returns 200 with valid JSON body matching schema X" is.
- Include non-functional criteria when relevant: performance, backward compatibility, documentation.

**Scope control:**
- If the issue grows beyond a single PR's worth of work, suggest splitting it.
- Explicitly call out what is out of scope to prevent scope creep.
- Prefer smaller, focused issues over large omnibus issues.

## Step 4: Refine

After drafting, review and improve:

### Suggest Labels

Recommend 2-4 labels based on the issue. Common taxonomy:
- **Type:** `bug`, `enhancement`, `task`, `rfc`, `documentation`
- **Priority:** `priority:critical`, `priority:high`, `priority:medium`, `priority:low`
- **Area:** `area:frontend`, `area:backend`, `area:api`, `area:infra`

Check the repo's existing labels first (via `gh label list` if available) to match the project's conventions.

### Link Related Context

- Reference related issues: "Related to #123" or "Blocked by #456"
- Mention relevant PRs: "Regression from #789"
- Link to external resources: docs, Slack threads, monitoring dashboards
- Tag specific people only when their input is required to unblock the issue

### Final Checks

Before presenting the draft to the user:

1. Can someone unfamiliar with the codebase understand what needs to happen?
2. Is the scope clear and achievable in a single PR (or explicitly broken into phases)?
3. Are acceptance criteria specific and testable?
4. Does the title accurately summarize the issue?

## Creating Issues via CLI

When the user wants to actually create the issue (not just draft it), use the GitHub CLI:

```bash
gh issue create --title "Title here" --body "$(cat <<'EOF'
Issue body in markdown...
EOF
)" --label "bug,priority:high"
```

Always present the full draft to the user for review before creating. Never create issues without explicit user confirmation.

If the repo has issue templates configured (`.github/ISSUE_TEMPLATE/`), read them first and adapt the draft to match the project's template structure instead of the generic templates in this skill.

## Resources

### references/
- `issue-templates.md` -- Structural templates for each issue type (bug, feature, task, RFC) and label taxonomy. Load when drafting any issue.
