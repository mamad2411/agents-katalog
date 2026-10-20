---
name: schedule-task
description: "Create, update, list, or run scheduled tasks (one-off actions). Schedule a skill, prompt, or script to run at a specific date/time without creating a full routine. Use when user says 'schedule this for', 'run this at', 'agendar para', 'roda isso amanha', 'post this on Friday at 10am', 'schedule a task', or any reference to one-off scheduled actions."
metadata:
  author: evonexus
  version: "1.0"
---

# Schedule Task — One-Off Scheduled Actions

Create and manage one-off scheduled tasks that run at a specific date/time. Unlike routines (which repeat on cron), scheduled tasks execute once and are done.

## When to Use

- User wants to schedule something for a specific time: "posta no LinkedIn sexta 10h"
- User wants to run a report later: "roda o financial pulse amanha as 8h"
- User says "agenda pra", "schedule this for", "run at", "agendar tarefa"
- User wants to list or manage pending tasks: "quais tarefas agendadas?"

## API Reference

The dashboard backend exposes these endpoints:

| Method | Endpoint | Action |
|--------|----------|--------|
| GET | `/api/tasks` | List tasks (query: `?status=pending\|running\|completed\|failed`) |
| POST | `/api/tasks` | Create a new task |
| GET | `/api/tasks/<id>` | Get task details |
| PUT | `/api/tasks/<id>` | Edit a pending task |
| DELETE | `/api/tasks/<id>` | Cancel (pending) or delete (completed/failed) |
| POST | `/api/tasks/<id>/run` | Execute immediately |

## Task Types

| Type | Payload | When to Use |
|------|---------|-------------|
| `skill` | Skill name + args (e.g. `social-post-writer LinkedIn post about X`) | Running a Claude skill |
| `prompt` | Free-form prompt text | Running a raw Claude prompt |
| `script` | Script path relative to `ADWs/routines/` (e.g. `custom/financial_pulse.py`) | Running an existing routine script |

## Agents

| Agent ID | Short Name |
|----------|------------|
| `clawdia-assistant` | @clawdia |
| `flux-financeiro` | @flux |
| `atlas-project` | @atlas |
| `kai-personal-assistant` | @kai |
| `pulse-community` | @pulse |
| `sage-strategy` | @sage |
| `pixel-social-media` | @pixel |
| `nex-comercial` | @nex |
| `mentor-courses` | @mentor |

## Workflow

### Creating a Task

1. **Understand the request** — extract what, when, and how:
   - **What:** the action to perform
   - **When:** date + time (convert relative dates like "amanha", "sexta" to absolute ISO 8601 in UTC)
   - **Type:** skill, prompt, or script
   - **Agent:** which agent should handle it (if applicable)

2. **Confirm with user** — show a summary before creating:
   ```
   Agendar:
   - Nome: Post LinkedIn sobre Evolution Summit
   - Tipo: skill
   - Payload: social-post-writer LinkedIn post about Evolution Summit April 14-16
   - Agent: @pixel
   - Quando: 2026-04-11 13:00 (BRT)
   
   Confirma?
   ```

3. **Create via API:**

Use `from dashboard.backend.sdk_client import evo` — auto-handles URL + auth.

```python
from dashboard.backend.sdk_client import evo
task = evo.post("/api/tasks", {
    "name": "Post LinkedIn sobre Evolution Summit",
    "description": "LinkedIn post promoting the Evolution Summit event",
    "type": "skill",
    "payload": "social-post-writer LinkedIn post about Evolution Summit April 14-16",
    "agent": "pixel-social-media",
    "scheduled_at": "2026-04-11T16:00:00Z",
})
```

**Important:** Convert BRT times to UTC by adding 3 hours. The user's timezone is America/Sao_Paulo (UTC-3).

### Listing Tasks

```python
from dashboard.backend.sdk_client import evo
# All pending tasks
pending = evo.get("/api/tasks", params={"status": "pending"})
# All tasks
all_tasks = evo.get("/api/tasks")
```

Present as a clean table:
```
ID | Nome                          | Tipo  | Agendado        | Status
---|-------------------------------|-------|-----------------|--------
1  | Post LinkedIn Summit          | skill | 11/04 13:00 BRT | pending
2  | Financial Weekly extra         | script| 12/04 08:00 BRT | completed
```

### Running Now

If user wants to execute immediately:
```python
from dashboard.backend.sdk_client import evo
evo.post(f"/api/tasks/{task_id}/run")
```

### Cancelling

```python
from dashboard.backend.sdk_client import evo
evo.delete(f"/api/tasks/{task_id}")
```

## Date Parsing Rules

The user speaks Portuguese. Common patterns:
- "amanha as 10h" → tomorrow at 10:00 BRT → +1 day, 13:00 UTC
- "sexta 15h" → next Friday at 15:00 BRT → Friday 18:00 UTC
- "segunda de manha" → next Monday at 09:00 BRT → Monday 12:00 UTC
- "hoje a noite" → today at 21:00 BRT → today 00:00+1 UTC
- "daqui 2 horas" → now + 2 hours

Always confirm the parsed date with the user before creating.

## Examples

### "Agenda um post no LinkedIn pra sexta as 10h sobre o Summit"
```json
{
  "name": "Post LinkedIn — Evolution Summit",
  "type": "skill",
  "payload": "social-post-writer LinkedIn post about Evolution Summit April 14-16, 2026",
  "agent": "pixel-social-media",
  "scheduled_at": "2026-04-10T13:00:00Z"
}
```

### "Roda o community pulse amanha as 8h"
```json
{
  "name": "Community Pulse (manual)",
  "type": "script",
  "payload": "custom/community_daily.py",
  "agent": null,
  "scheduled_at": "2026-04-10T11:00:00Z"
}
```

### "Manda um resumo pro Telegram amanha 14h com status dos projetos"
```json
{
  "name": "Resumo projetos via Telegram",
  "type": "prompt",
  "payload": "Check the status of all active projects (Evo AI, Evolution Summit, Evo Academy) and send a summary via Telegram to Davidson",
  "agent": "atlas-project",
  "scheduled_at": "2026-04-10T17:00:00Z"
}
```

## Important Notes

- Tasks are one-off. For recurring actions, use `create-routine` skill instead.
- The scheduler checks for pending tasks every 30 seconds.
- Tasks run in background threads — they won't block the scheduler.
- Results are saved in `result_summary` and visible in the dashboard at `/tasks`.
- Always confirm with the user before creating a task.
- Convert all times from BRT (UTC-3) to UTC before sending to the API.
