---
name: tracker-integration
description: "Detects issue tracker MCPs (Jira, Linear, GitHub Issues, Shortcut). Asks user once per project for opt-in. Syncs sprint tasks as tracker tickets. Updates ticket status as sprint progresses. Adds review findings as comments. Falls back to local-only if no MCP."
---

# Tracker Integration

Sync sprint workflow с issue tracker (если MCP установлен).

## Когда применять

- Phase 0 sprint cycle (detection)
- Throughout sprint cycle (status updates, comments)
- При создании tasks (auto-create tickets)

## Detection

Look for known issue tracker MCPs:

```yaml
# Known MCPs (community и official):
- jira-mcp / atlassian-mcp
- linear-mcp
- github-issues-mcp / github-mcp
- shortcut-mcp
- asana-mcp
- monday-mcp
- clickup-mcp
- notion-mcp (если using Notion для tracking)
```

```python
def detect_tracker_mcps():
    available = []
    for mcp_name in KNOWN_TRACKER_MCPS:
        if is_mcp_available(mcp_name):
            available.append(mcp_name)
    return available
```

## First-time setup

When ai-scrum first runs in project с tracker MCP detected:

```
[ai-scrum] Detected tracker MCP: jira-mcp
[ai-scrum] Configure tracker integration?
  (a) Yes - sync sprint tasks to Jira issues
  (b) No - keep all locally в .sprints/
  (c) Ask me each task

> User selects: a

[ai-scrum] Project key for new issues? > MERIDIAN
[ai-scrum] Default issue type? (Story/Task/Bug) > Task
[ai-scrum] Save in config? > Yes

[ai-scrum] Saved to .sprints/config.yaml
[ai-scrum] Tracker integration enabled.
```

After this initial setup - НЕ asking again. Used automatically.

## Configuration

Stored в `.sprints/config.yaml`:

```yaml
tracker:
  enabled: true
  mcp_name: "jira-mcp"
  
  jira:
    project_key: "MERIDIAN"
    default_issue_type: "Task"
    base_url: "https://yourcompany.atlassian.net"
  
  sync:
    create_tickets: true
    update_status: true
    add_review_comments: true
    link_to_retrospective: true
  
  # Optional: workflow status mapping
  status_mapping:
    planned: "To Do"
    in_progress: "In Progress"
    in_review: "In Review"
    done: "Done"
    failed: "Blocked"
```

## What syncs

### Task creation

When task added to plan (after decomposition approved):

```
Создать ticket в Jira:
  Title: T-1 - {{TASK_TITLE}}
  Description:
    {{TASK_DESCRIPTION}}
    
    Acceptance Criteria:
    - {{AC_1}}
    - {{AC_2}}
    
    Definition of Ready:
    [filled DoR criteria]
    
    Test approach:
    {{TEST_APPROACH}}
    
    Dependencies: T-2, T-3
    
    PRD: {{LINK}}
    Design: {{LINK}}
    Expected ADR: {{TITLE}}
    
    Local task file: .sprints/active/tasks/T-1.md
  
  Labels: ai-scrum, sprint-{N}
  Issue type: Task
```

Save ticket ID back в local task file.

### Status transitions

When task status changes:
- Local: `planned` → ticket: `To Do`
- `in_progress` → `In Progress`
- `in_review` → `In Review`
- `done` → `Done`
- `failed` → `Blocked`

Use status_mapping config для project-specific names.

### Review comments

When SE/Codex review provides findings:

```
Add comment на ticket:

## Internal SE Review (Sprint {{N}})

Verdict: {{PASS | FAIL | WAIVE}}

Findings:
- HIGH: {{description}}
- MEDIUM: {{description}}

(Full review: link to .sprints/...)
```

### Linking to retrospective

When task complete:

```
Add comment:

## Task Completed

This task was part of sprint cycle "{{TASK_NAME}}".
Retrospective: {{LINK_TO_RETROSPECTIVE}}
HTML report: {{LINK_TO_REPORT}}
```

## What stays local

Even with tracker integration - some things стay в `.sprints/`:

- Detailed execution log (tool history)
- Plan revisions
- Honesty warnings
- Configuration

Tracker has executive view, local has detail.

## Fallback behavior

### If tracker MCP missing

Plugin works normally - all локально:
- Tasks just local files
- No tickets created
- No status syncing
- Retrospectives stay local

### If MCP installed but user opts out

User selected "(b) No" or "(c) Ask each task":

For (b): No syncing.
For (c): Ask before creating each ticket. Can disable mid-cycle.

### If tracker API down

If MCP available но API request fails:
- Don't block sprint workflow
- Log error: "Tracker API unavailable - skipping sync this time"
- Retry later (next status change)
- Note в retrospective: "Tracker sync had failures - manual review of tracker recommended"

## Workflow

### On task creation

```python
def on_task_created(task):
    if not tracker.enabled:
        return
    
    if config.tracker.sync.ask_each_task:
        if not user_approves():
            return
    
    ticket = tracker.create_ticket(
        title=f"{task.id} - {task.title}",
        description=format_ticket_description(task),
        labels=['ai-scrum', f'sprint-{task.sprint_number}'],
        issue_type=config.tracker.default_issue_type
    )
    
    save_ticket_id_to_task(task, ticket.id)
```

### On status change

```python
def on_task_status_change(task, new_status):
    if not tracker.enabled or not task.ticket_id:
        return
    
    tracker_status = config.tracker.status_mapping.get(new_status, new_status)
    tracker.update_ticket_status(task.ticket_id, tracker_status)
```

### On review complete

```python
def on_review_complete(sprint, review_type, review):
    if not tracker.enabled:
        return
    
    for task in sprint.tasks:
        if not task.ticket_id:
            continue
        
        comment = format_review_as_comment(review, task)
        tracker.add_comment(task.ticket_id, comment)
```

## Output

Updated tracker tickets (external).

Local tracking в `.sprints/active/tracker-sync.log`:

```
2026-04-30 14:32:15 | T-1 | Created MERIDIAN-234
2026-04-30 14:35:42 | T-1 | Status: planned → in_progress
2026-04-30 14:38:00 | T-1 | Status: in_progress → in_review
2026-04-30 14:40:15 | T-1 | Comment added: SE Review (PASS)
2026-04-30 14:41:00 | T-1 | Status: in_review → done
```

Tracker references appear в HANDOFF.md updates if integration enabled.

## Privacy / security

When sending к tracker:
- Don't include secrets (run gitleaks check first)
- Don't include sensitive PII unless tracker is private
- Configurable: redaction policy per project

## Limitations

- Field mapping не universal - need adapter per tracker type
- Some MCPs limited subset of tracker features
- Custom fields в Jira/Linear не auto-mapped (need user config)
- Pull request linking (если using GitHub) requires GitHub MCP separately

These limitations OK для MVP. Advanced features в v0.2.0+ if user requests.
