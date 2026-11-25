---
name: jira
description: "Jira project management skill for creating, updating, commenting, and linking tickets via Atlassian MCP. Use when managing Jira issues."
---

# Jira

## Purpose

This skill provides comprehensive Jira project management capabilities through the Atlassian MCP integration. It enables agents to create, update, search, comment on, and link issues programmatically. Use this skill whenever a task involves managing work items in Jira — whether creating new tickets, updating existing ones, querying backlogs, or orchestrating cross-issue relationships.

## Issue Types & Hierarchy

### Hierarchy (top → bottom)

```
Epic
 └── Story / Task / Bug
      └── Sub-task
```

### Issue Types

| Type | Purpose | When to Use |
|------|---------|-------------|
| **Epic** | Large body of work spanning multiple sprints | Feature areas, initiatives, major deliverables |
| **Story** | User-facing functionality | "As a user, I want..." — delivers value to end users |
| **Task** | Technical work not directly user-facing | Infrastructure, refactoring, tooling, research spikes |
| **Sub-task** | Granular unit of work under a Story/Task | Backend endpoint, frontend component, test suite, migration |
| **Bug** | Defect in existing functionality | Something that worked before and is now broken, or doesn't match spec |

### Hierarchy Rules

- Epics contain Stories, Tasks, and Bugs (via Epic Link field).
- Stories, Tasks, and Bugs can have Sub-tasks.
- Sub-tasks cannot have children.
- Every Story/Task/Bug should belong to an Epic unless it is truly standalone.

## Fields Reference

### Required Fields

| Field | Description | Notes |
|-------|-------------|-------|
| `project` | Project key (e.g., `PROJ`) | Must exist in the Jira instance |
| `summary` | One-line title | Imperative mood, <80 characters |
| `issuetype` | Epic, Story, Task, Sub-task, Bug | Must match project's configured types |

### Common Optional Fields

| Field | Description | Example Values |
|-------|-------------|----------------|
| `description` | Detailed body (ADF or markdown) | See templates below |
| `priority` | Urgency level | Highest, High, Medium, Low, Lowest |
| `labels` | Categorical tags (array) | `["backend", "api", "tech-debt"]` |
| `components` | Architectural components (array) | `["auth-service", "web-app"]` |
| `assignee` | Account ID of the assignee | Use `jira_search` to resolve names → IDs |
| `sprint` | Sprint ID (not name) | Retrieve via board/sprint API |
| `story_points` / `customfield_XXXXX` | Estimation | Fibonacci: 1, 2, 3, 5, 8, 13 |
| `epic_link` / `customfield_XXXXX` | Parent Epic key | `PROJ-42` |
| `fix_versions` | Target release versions | `["v2.1.0"]` |

### Summary Writing Conventions

- **Imperative mood**: "Add user authentication" not "Added user authentication" or "Adding user authentication"
- **Under 80 characters**: Be concise but specific
- **No trailing period**: Summaries are titles, not sentences
- **Include scope hint**: "[API] Add rate limiting to /users endpoint"
- **Bug summaries state the symptom**: "Login fails with 500 when email contains +"

### Description Templates

**Story Description:**
```
h2. User Story
As a [persona], I want [action] so that [benefit].

h2. Acceptance Criteria
* [ ] Criterion 1
* [ ] Criterion 2
* [ ] Criterion 3

h2. Technical Notes
* Implementation approach or constraints
* Relevant endpoints, schemas, dependencies

h2. Out of Scope
* What this story explicitly does NOT cover
```

**Bug Description:**
```
h2. Summary
Brief description of the defect.

h2. Steps to Reproduce
# Step 1
# Step 2
# Step 3

h2. Expected Behavior
What should happen.

h2. Actual Behavior
What actually happens. Include error messages, status codes, screenshots.

h2. Environment
* Browser/OS/Device:
* Version/Build:
* Environment: staging / production

h2. Severity Assessment
* Impact: [Critical / High / Medium / Low]
* Frequency: [Always / Often / Sometimes / Rarely]
* Workaround: [None / Exists — describe]
```

## Workflow States

### Standard Workflow

```
To Do → In Progress → In Review → Done
```

| State | Meaning | Transition Trigger |
|-------|---------|-------------------|
| **To Do** | Work not started, in backlog or sprint | Issue created or moved to sprint |
| **In Progress** | Actively being worked on | Developer starts work |
| **In Review** | Code complete, awaiting review | PR opened or review requested |
| **Done** | Accepted and complete | PR merged, QA passed |

### Transition Rules

- Only transition forward unless explicitly reverting (e.g., review rejection → In Progress).
- Moving to "In Progress" should set/confirm the assignee.
- Moving to "Done" should verify all sub-tasks are also Done.

## Issue Link Types

| Link Type | Forward Description | Reverse Description | When to Use |
|-----------|-------------------|---------------------|-------------|
| **Blocks** | blocks | is blocked by | Issue A must complete before B can start |
| **Relates to** | relates to | relates to | Loosely related work, shared context |
| **Duplicates** | duplicates | is duplicated by | Same defect reported twice |
| **Clones** | clones | is cloned by | Copy of an issue for another project/sprint |
| **Causes** | causes | is caused by | Root cause relationship (bugs) |

## MCP Tools Available

### `jira_create_issue`
Create a new Jira issue.
```
Parameters: project, summary, issuetype, description?, priority?, labels?, components?, assignee?, parent? (for sub-tasks)
Returns: key, id, self (URL)
```

### `jira_update_issue`
Update fields on an existing issue.
```
Parameters: issue_key, fields (object with fields to update)
Returns: confirmation
```

### `jira_add_comment`
Add a comment to an existing issue.
```
Parameters: issue_key, body (comment text)
Returns: comment ID, created timestamp
```

### `jira_link_issues`
Create a link between two issues.
```
Parameters: inward_issue, outward_issue, link_type
Returns: confirmation
```

### `jira_search`
Search issues using JQL.
```
Parameters: jql, fields? (array of field names), max_results?
Returns: array of matching issues
```

### `jira_get_issue`
Retrieve full details of a single issue.
```
Parameters: issue_key
Returns: full issue object with all fields
```

### `jira_transition_issue`
Move an issue to a new workflow state.
```
Parameters: issue_key, transition_id or transition_name
Returns: confirmation
```

## JQL Quick Reference

### Common Queries

```jql
-- My open issues
assignee = currentUser() AND status != Done

-- Sprint backlog
sprint in openSprints() AND project = PROJ

-- Unresolved bugs by priority
project = PROJ AND issuetype = Bug AND status != Done ORDER BY priority ASC

-- Recently updated
project = PROJ AND updated >= -7d ORDER BY updated DESC

-- Blocked work
issuefunction in hasLinks("is blocked by")

-- Epics missing stories
issuetype = Epic AND project = PROJ AND NOT issuefunction in hasLinks("is Epic of")

-- Issues without estimates
project = PROJ AND issuetype in (Story, Task) AND story_points is EMPTY AND sprint in openSprints()
```

### JQL Operators

| Operator | Example | Notes |
|----------|---------|-------|
| `=`, `!=` | `status = "In Progress"` | Exact match |
| `in`, `not in` | `issuetype in (Story, Bug)` | Multiple values |
| `~` | `summary ~ "auth"` | Contains text (fuzzy) |
| `is EMPTY` / `is not EMPTY` | `assignee is EMPTY` | Null checks |
| `>=`, `<=` | `created >= -30d` | Date/number comparison |
| `was`, `was in`, `was not` | `status was "In Progress"` | Historical state |
| `changed` | `status changed FROM "To Do" TO "In Progress"` | Transition history |
| `ORDER BY` | `ORDER BY priority ASC, created DESC` | Sorting |

### JQL Functions

| Function | Purpose |
|----------|---------|
| `currentUser()` | The authenticated user |
| `openSprints()` | All active sprints |
| `closedSprints()` | All completed sprints |
| `futureSprints()` | All upcoming sprints |
| `startOfDay()`, `endOfDay()` | Day boundaries |
| `startOfWeek()`, `endOfWeek()` | Week boundaries |
| `now()` | Current timestamp |

## Comment Conventions

- **Status updates**: Start with the new state. "In Progress — starting backend implementation."
- **Questions**: Tag the person. "@john.doe — can you clarify the auth flow for SSO users?"
- **Blockers**: Flag clearly. "BLOCKED — waiting on PROJ-456 (API schema finalization)."
- **Completion**: Summarize what was done. "Done — implemented rate limiter with token bucket algorithm. See PR #234."
- **Technical notes**: Use code blocks for snippets, stack traces, or config.

## Conventions

1. **Always search before creating** — avoid duplicates. Run a JQL query for similar summaries first.
2. **One ticket, one concern** — don't bundle unrelated work into a single issue.
3. **Link related issues** — if two tickets touch the same code or feature, link them.
4. **Keep summaries scannable** — a PM should understand the ticket from the summary alone.
5. **Set priority explicitly** — never leave priority as the default unless it truly is Medium.
6. **Assign during sprint planning** — not at creation time, unless the assignee is obvious.
7. **Sub-tasks for decomposition** — if a Story has >3 days of work, break it into Sub-tasks.

## Knowledge Strategy

- **Patterns to capture:** Project-specific field mappings (custom field IDs), common JQL queries that prove useful, description templates refined for specific teams.
- **Examples to collect:** Successfully created ticket payloads, effective bug reports, JQL queries for recurring audits.
- **Update permission:** Agents may freely add/update files in `references/`. Changes to `SKILL.md` or `scripts/` require user approval.
