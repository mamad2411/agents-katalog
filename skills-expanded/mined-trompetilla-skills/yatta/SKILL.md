---
name: yatta
description: Personal productivity system for task and capacity management. Create and organize tasks with rich attributes (priority, effort, complexity, tags), track time and streaks, manage capacity across projects and contexts, view Eisenhower Matrix prioritization, sync calendar subscriptions, handle delegation and follow-ups, and get AI-powered insights. Supports batch operations, multi-project workflows, and real-time capacity planning to prevent overcommitment.
homepage: https://github.com/chrisagiddings/openclaw-yatta-skill
metadata: {"openclaw":{"emoji":"✅","requires":{"env":["YATTA_API_KEY","YATTA_API_URL"],"bins":["curl","jq"]},"primaryEnv":"YATTA_API_KEY","disable-model-invocation":true,"capabilities":["task-management","project-management","context-management","comment-management","calendar-management","destructive-operations"],"credentials":{"type":"env","variables":[{"name":"YATTA_API_KEY","description":"Yatta! API key (yatta_...)","required":true},{"name":"YATTA_API_URL","description":"Yatta! API base URL","required":false,"default":"https://zunahvofybvxpptjkwxk.supabase.co/functions/v1"}]}}}
---

# Yatta! Skill

Interact with Yatta! task management system via API. Requires an API key from your Yatta! account.

## ⚠️ Security Warning

**This skill can perform DESTRUCTIVE operations on your Yatta! account:**

- **Task Management:** Create, update, archive, and batch-modify tasks
- **Project Management:** Create, update, and archive projects
- **Context Management:** Create contexts and assign them to tasks
- **Comment Management:** Add, update, and delete task comments
- **Calendar Management:** Create, sync, and modify calendar subscriptions
- **Follow-Up Management:** Update delegation schedules and mark complete
- **Capacity Management:** Trigger capacity computations

**Operation Types:**

**Read-Only Operations** (✅ Safe):
- List tasks, projects, contexts, comments
- Get analytics, insights, streaks
- View capacity and calendar data
- Get Eisenhower Matrix view
- All GET requests

**Destructive Operations** (⚠️ Modify or delete data):
- Create/update/archive tasks (POST, PUT, DELETE)
- Batch update tasks
- Create/update projects
- Create/assign contexts
- Add/update/delete comments
- Add/sync calendar subscriptions
- Update follow-up schedules
- All POST, PUT, DELETE requests

**Best Practices:**
1. **Review commands before running** - Check what the API call will do
2. **No undo for deletions** - Archived tasks can be recovered, but some operations are permanent
3. **Test on non-critical data first** - Create test tasks/projects to verify behavior
4. **Batch operations affect multiple items** - Be extra careful with batch updates
5. **Real-time sync** - Changes appear in Yatta! UI immediately

For detailed API operation documentation, see [API-REFERENCE.md](API-REFERENCE.md).

## Setup

### ⚠️ API Key Security

**Your Yatta! API key provides FULL access to your account:**
- Can create, read, update, and delete ALL tasks, projects, contexts
- Can modify calendar subscriptions and follow-up schedules
- Can archive data and trigger computations
- **No read-only scopes available** - keys have full permissions

**Security Best Practices:**
- Store keys in a secure password manager (1Password CLI recommended)
- Use environment variables, never hardcode keys in scripts
- Rotate keys regularly (every 90 days recommended)
- Create separate keys for different integrations
- Revoke unused keys immediately
- **Never commit keys to version control**

### 1. Get Your API Key

1. Log into Yatta! app
2. Go to Settings → API Keys
3. Create new key (e.g., "OpenClaw Integration")
4. Copy the `yatta_...` key
5. Store it securely

### 2. Configure the Skill

**Option A: Environment Variables (Recommended)**
```bash
# Add to your shell profile (~/.zshrc, ~/.bashrc)
export YATTA_API_KEY="yatta_your_key_here"
export YATTA_API_URL="https://zunahvofybvxpptjkwxk.supabase.co/functions/v1"  # Default
```

**Option B: 1Password CLI (Most Secure)**
```bash
# Store key in 1Password
op item create --category=API_CREDENTIAL \
  --title="Yatta API Key" \
  api_key[password]="yatta_your_key_here"

# Use in commands
export YATTA_API_KEY=$(op read "op://Private/Yatta API Key/api_key")
```

**Note:** Currently using direct Supabase URL. Clean branded URLs (yattadone.com/api) coming soon.

### 3. Test Connection
   ```bash
   curl -s "$YATTA_API_URL/tasks" \
     -H "Authorization: Bearer $YATTA_API_KEY" \
     | jq '.[:3]'  # Show first 3 tasks
   ```

## Tasks API

### List Tasks

**All tasks:**
```bash
curl -s "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

**Filter by status:**
```bash
# TODO tasks only
curl -s "$YATTA_API_URL/tasks?status=todo" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'

# Doing (active) tasks
curl -s "$YATTA_API_URL/tasks?status=doing" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'

# Completed tasks
curl -s "$YATTA_API_URL/tasks?status=done" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

**Filter by priority:**
```bash
# High priority tasks
curl -s "$YATTA_API_URL/tasks?priority=high" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.[] | {title, due_date, priority}'
```

**Filter by project:**
```bash
# Get project ID first
PROJECT_ID=$(curl -s "$YATTA_API_URL/projects" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq -r '.[] | select(.name=="Website Redesign") | .id')

# Get tasks for that project
curl -s "$YATTA_API_URL/tasks?project_id=$PROJECT_ID" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

**Filter by matrix state:**
```bash
# Delegated tasks
curl -s "$YATTA_API_URL/tasks?matrix_state=delegated" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.[] | {title, delegated_to, follow_up_date}'

# Waiting tasks
curl -s "$YATTA_API_URL/tasks?matrix_state=waiting" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

**Date range queries:**
```bash
# Tasks due this week
WEEK_END=$(date -v+7d "+%Y-%m-%d")
curl -s "$YATTA_API_URL/tasks?due_date_lte=$WEEK_END" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.[] | {title, due_date}'

# Overdue tasks
TODAY=$(date "+%Y-%m-%d")
curl -s "$YATTA_API_URL/tasks?due_date_lte=$TODAY&status=todo" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.[] | {title, due_date}'
```

**Pagination:**
```bash
# First 50 tasks
curl -s "$YATTA_API_URL/tasks?limit=50&offset=0" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'

# Next 50 tasks
curl -s "$YATTA_API_URL/tasks?limit=50&offset=50" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

**Archived tasks:**
```bash
curl -s "$YATTA_API_URL/tasks?archived=true" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### Create Task

**Simple task:**
```bash
curl -s "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Finish report",
    "priority": "high"
  }' \
  | jq '.'
```

**Task with full details:**
```bash
curl -s "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Review Q1 numbers",
    "description": "Go through revenue, costs, and projections",
    "priority": "high",
    "due_date": "2026-02-15",
    "effort_points": 5,
    "project_id": "uuid-of-project",
    "matrix_state": "active"
  }' \
  | jq '.'
```

**Delegated task with follow-up:**
```bash
curl -s "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Website redesign",
    "delegated_to": "Dev Team",
    "matrix_state": "delegated",
    "follow_up_schedule": {
      "type": "weekly",
      "day_of_week": "monday",
      "next_follow_up": "2026-02-17"
    }
  }' \
  | jq '.'
```

**Recurring task:**
```bash
curl -s "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team standup",
    "recurrence_rule": {
      "frequency": "daily",
      "interval": 1,
      "days_of_week": ["monday", "tuesday", "wednesday", "thursday", "friday"]
    },
    "effort_points": 1
  }' \
  | jq '.'
```

### Update Task

**Update single task:**
```bash
TASK_ID="uuid-of-task"
curl -s -X PUT "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "'$TASK_ID'",
    "status": "done",
    "completed_at": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"
  }' \
  | jq '.'
```

**Batch update tasks:**
```bash
curl -s -X PUT "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "ids": ["uuid-1", "uuid-2", "uuid-3"],
    "priority": "high",
    "project_id": "project-uuid"
  }' \
  | jq '.'
```

### Archive Task

```bash
TASK_ID="uuid-of-task"
curl -s -X DELETE "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "'$TASK_ID'"
  }' \
  | jq '.'
```

## Projects API

### List Projects

```bash
# All projects
curl -s "$YATTA_API_URL/projects" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'

# With task counts
curl -s "$YATTA_API_URL/projects?with_counts=true" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.[] | {name, task_count, open_count}'
```

### Create Project

```bash
curl -s "$YATTA_API_URL/projects" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Website Redesign",
    "description": "Complete overhaul of company site",
    "color": "#3b82f6",
    "icon": "🌐"
  }' \
  | jq '.'
```

### Update Project

```bash
PROJECT_ID="uuid-of-project"
curl -s -X PUT "$YATTA_API_URL/projects" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "'$PROJECT_ID'",
    "name": "Website Redesign v2",
    "archived": false
  }' \
  | jq '.'
```

### Get Project Tasks

```bash
PROJECT_ID="uuid-of-project"
curl -s "$YATTA_API_URL/projects/$PROJECT_ID/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

## Contexts API

### List Contexts

```bash
# All contexts
curl -s "$YATTA_API_URL/contexts" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'

# With task counts
curl -s "$YATTA_API_URL/contexts?with_counts=true" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.[] | {name, task_count}'
```

### Create Context

```bash
curl -s "$YATTA_API_URL/contexts" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "@deep-focus",
    "color": "#8b5cf6",
    "icon": "🧠"
  }' \
  | jq '.'
```

### Assign Context to Task

```bash
TASK_ID="uuid-of-task"
CONTEXT_ID="uuid-of-context"

curl -s -X POST "$YATTA_API_URL/contexts/assign" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "'$TASK_ID'",
    "context_ids": ["'$CONTEXT_ID'"]
  }' \
  | jq '.'
```

### Get Task Contexts

```bash
TASK_ID="uuid-of-task"
curl -s "$YATTA_API_URL/tasks/$TASK_ID/contexts" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### Get Context Tasks

```bash
CONTEXT_ID="uuid-of-context"
curl -s "$YATTA_API_URL/contexts/$CONTEXT_ID/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

## Comments API

### List Task Comments

```bash
TASK_ID="uuid-of-task"
curl -s "$YATTA_API_URL/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### Add Comment

```bash
TASK_ID="uuid-of-task"
curl -s -X POST "$YATTA_API_URL/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Waiting on client feedback before proceeding"
  }' \
  | jq '.'
```

### Update Comment

```bash
COMMENT_ID="uuid-of-comment"
curl -s -X PUT "$YATTA_API_URL/task-comments" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "'$COMMENT_ID'",
    "content": "Client responded, moving forward"
  }' \
  | jq '.'
```

### Delete Comment

```bash
COMMENT_ID="uuid-of-comment"
curl -s -X DELETE "$YATTA_API_URL/task-comments" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "'$COMMENT_ID'"
  }' \
  | jq '.'
```

## Follow-Ups API

### Get Today's Follow-Ups

```bash
curl -s "$YATTA_API_URL/follow-ups" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.[] | {title, delegated_to, follow_up_date}'
```

### Get Follow-Ups for Date

```bash
DATE="2026-02-15"
curl -s "$YATTA_API_URL/follow-ups?date=$DATE" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### Mark Follow-Up Complete

```bash
TASK_ID="uuid-of-task"
curl -s -X POST "$YATTA_API_URL/tasks/$TASK_ID/follow-up" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}' \
  | jq '.'
```

### Update Follow-Up Schedule

```bash
TASK_ID="uuid-of-task"
curl -s -X PUT "$YATTA_API_URL/tasks/$TASK_ID/follow-up-schedule" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "every_n_days",
    "interval": 3,
    "next_follow_up": "2026-02-12"
  }' \
  | jq '.'
```

## Calendar API

### List Calendar Subscriptions

```bash
curl -s "$YATTA_API_URL/calendar/subscriptions" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### Add Calendar Subscription

```bash
curl -s -X POST "$YATTA_API_URL/calendar/subscriptions" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Work Calendar",
    "ical_url": "https://calendar.google.com/calendar/ical/...",
    "default_context_id": "context-uuid"
  }' \
  | jq '.'
```

### Trigger Calendar Sync

```bash
SUBSCRIPTION_ID="uuid-of-subscription"
curl -s -X POST "$YATTA_API_URL/calendar/subscriptions/$SUBSCRIPTION_ID/sync" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### List Calendar Events

```bash
# Events for date range
START="2026-02-10"
END="2026-02-17"
curl -s "$YATTA_API_URL/calendar/events?start=$START&end=$END" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

## Capacity API

### Get Today's Capacity

```bash
curl -s "$YATTA_API_URL/capacity/today" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '{date, utilization_percent, status, used_minutes, total_minutes}'
```

### Get Capacity for Date Range

```bash
START="2026-02-10"
END="2026-02-17"
curl -s "$YATTA_API_URL/capacity?start=$START&end=$END" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.[] | {date, status, utilization_percent}'
```

### Trigger Capacity Computation

```bash
curl -s -X POST "$YATTA_API_URL/capacity/compute" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

## Analytics API

### Get Summary Insights

```bash
curl -s "$YATTA_API_URL/analytics/summary" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### Get Velocity Metrics

```bash
curl -s "$YATTA_API_URL/analytics/velocity" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### Get Task Distribution

```bash
curl -s "$YATTA_API_URL/analytics/distribution" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '{by_status, by_priority, by_matrix_state}'
```

### Get Streaks

```bash
curl -s "$YATTA_API_URL/analytics/streaks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### Get AI Insights

```bash
curl -s "$YATTA_API_URL/analytics/insights" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

## Matrix Endpoint

### Get Eisenhower Matrix View

```bash
curl -s "$YATTA_API_URL/tasks/matrix" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '{do_first, schedule, delegate, eliminate}'
```

## Common Patterns

### Daily Workflow Automation

**Morning briefing:**
```bash
#!/bin/bash
echo "=== Today's Tasks ==="
curl -s "$YATTA_API_URL/tasks?status=todo&due_date_lte=$(date +%Y-%m-%d)" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq -r '.[] | "- [\(.priority)] \(.title)"'

echo ""
echo "=== Follow-Ups Due ==="
curl -s "$YATTA_API_URL/follow-ups" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq -r '.[] | "- \(.title) (delegated to: \(.delegated_to))"'

echo ""
echo "=== Capacity Status ==="
curl -s "$YATTA_API_URL/capacity/today" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq -r '"Utilization: \(.utilization_percent)% - \(.status)"'
```

### Create Task from Email

```bash
#!/bin/bash
# Extract email subject and body
SUBJECT="$1"
BODY="$2"

curl -s "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "'"$SUBJECT"'",
    "description": "'"$BODY"'",
    "priority": "medium",
    "import_source": "email"
  }' \
  | jq -r '"Task created: \(.title)"'
```

### Weekly Planning Report

```bash
#!/bin/bash
WEEK_START=$(date -v+mon "+%Y-%m-%d")
WEEK_END=$(date -v+sun "+%Y-%m-%d")

echo "=== Week of $WEEK_START ==="
curl -s "$YATTA_API_URL/capacity?start=$WEEK_START&end=$WEEK_END" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq -r '.[] | "\(.date): \(.status) (\(.utilization_percent)%)"'

echo ""
echo "=== Tasks Due This Week ==="
curl -s "$YATTA_API_URL/tasks?due_date_gte=$WEEK_START&due_date_lte=$WEEK_END" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq -r '.[] | "[\(.due_date)] \(.title)"'
```

## Error Handling

**Check response status:**
```bash
RESPONSE=$(curl -s -w "\n%{http_code}" "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY")

STATUS=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$STATUS" -eq 200 ]; then
  echo "$BODY" | jq '.'
else
  echo "Error: HTTP $STATUS"
  echo "$BODY" | jq '.error'
fi
```

**Rate limit handling:**
```bash
RESPONSE=$(curl -s -i "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY")

# Check X-RateLimit headers
REMAINING=$(echo "$RESPONSE" | grep -i "X-RateLimit-Remaining" | cut -d' ' -f2)
RESET=$(echo "$RESPONSE" | grep -i "X-RateLimit-Reset" | cut -d' ' -f2)

if [ "$REMAINING" -lt 10 ]; then
  echo "Warning: Only $REMAINING requests remaining"
  echo "Rate limit resets at: $(date -r $RESET)"
fi
```

## Tips

- **Store API key securely:** Use 1Password CLI, env vars, or secrets manager
- **Use jq for filtering:** Pipe responses through `jq` for clean output
- **Batch operations:** Update multiple tasks at once when possible
- **Rate limits:** 100 requests/minute per API key
- **Date formats:** Always use ISO 8601 (YYYY-MM-DD for dates, YYYY-MM-DDTHH:MM:SSZ for timestamps)
- **Error responses:** Include `error` field with description

## Resources

- **API Documentation:** [Yatta! API Docs](https://yattadone.com/docs/api) (coming soon)
- **GitHub Repo:** https://github.com/chrisagiddings/openclaw-yatta-skill
- **Report Issues:** https://github.com/chrisagiddings/openclaw-yatta-skill/issues

## API URL Note

Currently using the direct Supabase Edge Functions URL for reliability:
```
https://zunahvofybvxpptjkwxk.supabase.co/functions/v1
```

Branded URLs (`yattadone.com/api`) will be available in a future release once proxy configuration is resolved with the hosting provider.
