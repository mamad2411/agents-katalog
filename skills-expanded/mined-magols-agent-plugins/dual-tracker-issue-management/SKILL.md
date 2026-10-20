---
name: dual-tracker-issue-management
description: 'Provider-neutral issue management for GitHub Issues and Azure DevOps Work Items. Use when creating, updating, linking, transitioning, or closing tracked work across one or both systems.'
---

# Dual Tracker Issue Management

Provider-neutral issue operations mapped to GitHub and Azure DevOps.

## Supported Actions

- create
- update
- link
- transition
- close

## Canonical Issue Contract

Required fields:

- Title
- Description
- WorkType (`bug`, `feature`, `task`, `review-followup`)
- Priority
- Assignee (optional)
- LabelsOrTags (optional)
- SourceReference (commit, branch, PR, or review finding)

## Provider Mapping

| Canonical Field | GitHub | Azure DevOps |
|----------------|--------|--------------|
| Title | Issue title | Work item title |
| Description | Issue body | Work item description |
| WorkType | labels | work item type |
| Priority | label or project field | priority field |
| Assignee | assignees | assigned to |
| LabelsOrTags | labels | tags |
| State | open/closed | new/active/resolved/closed |

## Action Flow

1. Validate canonical fields.
2. Resolve provider targets (`github`, `azure-devops`, or both).
3. Execute provider operations.
4. Return a normalized result:

- CorrelationId
- Action
- ProviderResults[] with provider name, item id, url/reference, status
- Failures[] with remediation suggestions

## Failure Handling

- If one provider fails in dual mode, return partial success with explicit failed provider details.
- Never hide failed mappings or silently skip required fields.
- Include retry guidance for transient failures.
