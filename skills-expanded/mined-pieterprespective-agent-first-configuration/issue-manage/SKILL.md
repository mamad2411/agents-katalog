---
name: issue-manage
description: >
  Plan and manage development activities — create structured assignment or research plans,
  track issues discovered during work, and report on activity completion. Integrates with
  Jira for issue tracking and the project's Prompts/ folder for plan documents.
  Triggers on: "plan an assignment", "plan research", "new activity", "track issue",
  "complete activity", "issue plan", "research plan".
---

# Issue Management Skill

Manage the lifecycle of development activities: plan creation, issue tracking, and
completion reporting.

## Before Any Operation

1. Read `Prompts/BasePrompt.md` from the project root for project-specific guidelines.
   - **If not found: stop and report this to the user.** Do not proceed without it.
2. Read `.jira-config.md` for Jira project configuration.

## Plan Creation

### Inputs

The user provides one of:
- **Rough text description** of what needs to be done
- **Path to an .md file** containing a more detailed outline

### IssueID Resolution

Every activity needs an issueID. Ask the user which approach to use:

1. **Create new Jira issue**
   - Read project keys from `.jira-config.md`
   - List components via `jira-w --components <KEY>`
   - Let the user choose one or more components
   - Choose issue type (default: Task)
   - Create: `jira-w issue create -t"<Type>" -s"<Summary>" -C"<Component>" -p <KEY> --no-input`
   - The returned issue key becomes the issueID

2. **Use existing Jira issue**
   - User provides a key (e.g., ELOM-123)
   - Verify it exists: `jira-w issue view <KEY> --plain`
   - Use that key as issueID

3. **Custom ID**
   - User provides any string identifier
   - Use as-is for the issueID

### Output

Create `Prompts/{issueID}/` and populate with plan documents:

- **Assignment**: Use `templates/assignment-plan.md` as structure
  - Output file: `Prompts/{issueID}/00-PLAN-{slug}.md`
- **Research**: Use `templates/research-plan.md` as structure
  - Output file: `Prompts/{issueID}/00-RESEARCH-{slug}.md`

The slug should be kebab-case, max 4 words, derived from the activity title.

Also initialize `Prompts/{issueID}/new_issues.md` from `templates/new-issues-log.md`.

### Return to Main Agent

After creating the plan, return:
- The issueID
- Activity type (assignment/research)
- Plan file path(s)
- Brief summary of the plan

The main agent handles diary entries and git operations.

## Issue Tracking (reference — executed by main agent)

During work, the main agent uses `/issue-track` to record newly discovered issues.
See the slash command definition for details. This skill does not handle tracking
directly — the main agent follows the command instructions inline.

## Activity Completion (reference — executed by main agent)

On completion, the main agent uses `/issue-complete` to generate reports.
See the slash command definition for details.

## Platform Notes

- All Jira operations use `jira-w` wrapper (never `jira` directly)
- File paths use the OS-appropriate separator
- Git commands are read-only (branch, log, rev-parse)
