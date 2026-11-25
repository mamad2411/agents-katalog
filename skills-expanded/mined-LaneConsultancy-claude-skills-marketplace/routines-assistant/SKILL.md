---
name: routines-assistant
description: Create, fire, and manage Codex cloud routines (scheduled/API/GitHub-triggered remote agents). Use when George asks to set up a recurring remote agent, a webhook-triggered workflow, automate a daily/weekly task in the cloud, schedule a cron job for Codex, or anything involving Codex.ai/code/scheduled. Triggers on "routine", "schedule a remote agent", "webhook to Codex", "daily/weekly Codex job", "cron routine", or /routines-assistant.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, ToolSearch, WebFetch, RemoteTrigger
---

# Routines — Cloud Scheduled Agents

Routines are **saved Codex configurations that run on Anthropic-managed cloud infrastructure** — a prompt + repo(s) + connectors, fired on a schedule, HTTP POST, or GitHub event. They keep working when George's laptop is closed.

Docs: https://code.Codex.com/docs/en/routines
Fire API: https://platform.Codex.com/docs/en/api/Codex/routines-fire
Web UI: https://Codex.ai/code/scheduled

## When to use routines vs other scheduling

| Need | Use |
|------|-----|
| Runs unattended in cloud, survives laptop off | **Routine** (this skill) |
| Runs inside the current REPL session only | `CronCreate` (in-session) |
| Runs on George's local machine with local file/MCP access | Desktop scheduled task |
| One-shot reminder later today | `CronCreate` with `recurring: false` |

**Hard constraint**: routines run in Anthropic cloud. They have **no access to**:
- Chrome DevTools MCP (George's logged-in X/social/etc. sessions)
- Local files outside the cloned repo
- Local `.env` variables
- Any local CLI tools, local databases, or anything on `~/Dropbox/Projects/` not in the GitHub repo

If the task needs any of those, either adapt it to use WebFetch/WebSearch + API calls (with secrets added to the cloud env), or use a local scheduler instead.

## Canonical creation body (tested, works)

Load `RemoteTrigger` first, then call `{action: "create", body: ...}` with this exact shape:

```json
{
  "name": "DESCRIPTIVE_NAME",
  "cron_expression": "MM HH * * *",
  "enabled": true,
  "job_config": {
    "ccr": {
      "environment_id": "YOUR_ENVIRONMENT_ID",
      "session_context": {
        "model": "Codex-sonnet-4-6",
        "sources": [
          {"git_repository": {"url": "https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO"}}
        ],
        "allowed_tools": ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "WebFetch", "WebSearch"]
      },
      "events": [
        {
          "data": {
            "uuid": "GENERATE_FRESH_LOWERCASE_V4_UUID",
            "session_id": "",
            "type": "user",
            "parent_tool_use_id": null,
            "message": {
              "role": "user",
              "content": "THE_PROMPT_HERE"
            }
          }
        }
      ]
    }
  }
}
```

### Hardcoded values for George's account
- **`environment_id`**: `YOUR_ENVIRONMENT_ID` — find this at https://Codex.ai/code/environments (Default, anthropic_cloud kind). **Update this skill with George's actual ID before first use.**
- **Default repo**: `https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO` — update to George's default repo, or ask if a different repo is needed
- **Default model**: `Codex-sonnet-4-6` (routines are research/automation, not heavy reasoning)
- **Creator UUID**: `YOUR_CREATOR_UUID` (for reference; not needed in the body)

## Cron conventions

- **Cron is UTC**. George's timezone is `Europe/London` (BST = UTC+1 late March–late October, GMT = UTC+0 otherwise). Convert and confirm with him — and remember the offset changes twice a year.
- **Minimum interval: 1 hour**. `*/30 * * * *` is rejected.
- **Avoid minute 0 and 30** — every routine on the platform lands on those. Pick an off-minute (`:07`, `:17`, `:43`, `:51`).
- **Stagger multiple daily routines** by 15+ min so they don't compete for resources.

Examples (London local → UTC, assuming BST / UTC+1):
- Daily at 8 AM BST → `17 7 * * *`
- Daily at 7 AM BST → `43 6 * * *`
- Sunday 8 PM BST → `7 19 * * 0`
- Every 2 hours → `13 */2 * * *`

During GMT (winter), local time == UTC, so drop the −1 offset.

## Allowed tools

Pick the smallest set the routine actually needs. Common combos:

| Routine type | Tools |
|--------------|-------|
| Web research / scanning | `Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch` |
| API automation (no code) | `Bash, Read, Write, Edit, WebFetch` |
| Code review / PR work | `Bash, Read, Write, Edit, Glob, Grep` |
| Data pull + report | `Bash, Read, Write, Edit, Glob, Grep, WebFetch` |

Do **not** add MCP tools — routines have no MCP connectors unless explicitly attached via `mcp_connections` (confirm with George before assuming any are attached).

## UUID generation

Events require a fresh lowercase v4 UUID. Generate one per routine:

```bash
python3 -c "import uuid; print(uuid.uuid4())"
# or
uuidgen | tr '[:upper:]' '[:lower:]'
```

Never reuse a UUID across routines.

## Output conventions

Routines should write results to the cloned repo on a `Codex/*` branch (the default allowed prefix). Standard pattern:

1. Write markdown report to `active/{routine-name}/YYYY-MM-DD-HHmm-report.md`
2. Commit to `Codex/{routine-name}-YYYY-MM-DD` branch
3. Also print the report to stdout so it shows in the session transcript at Codex.ai/code/scheduled/{trigger_id}

George can open the session URL to see output, or pull the branch if he wants the file.

## Secrets and environment variables

The Default cloud env has no custom env vars. To give a routine API access (Fireflies, ClickUp, Resend, or whatever third-party service it needs):

1. Go to https://Codex.ai/code/environments
2. Edit Default (or create a new env) and add `KEY=VALUE` pairs
3. Reference them in the prompt as `$KEY` — the routine's Bash sessions will see them

**Always check for secret presence in the prompt** and exit gracefully if missing:

```
REQUIRED ENV VAR: SOME_API_KEY must be set. If missing, print
"Missing SOME_API_KEY — add at Codex.ai/code/environments" and exit.
```

Never hardcode secrets in prompts — they're logged.

## Firing a routine

**Manually (right now, for testing)**:
```
RemoteTrigger({action: "run", trigger_id: "trig_01..."})
```
Returns the trigger config (not the session URL — fire is async; the session appears at Codex.ai/code/scheduled/{trigger_id}).

**Via HTTP (for webhooks)**:
```
POST https://api.anthropic.com/v1/Codex/routines/{trigger_id}/fire
Authorization: Bearer {per-routine-token}
anthropic-version: 2023-06-01
anthropic-beta: experimental-cc-routine-2026-04-01
Content-Type: application/json

{"text": "freeform context appended to the saved prompt"}
```

The `text` field is a single string appended as a user turn. Max 65,536 chars. If sending a JSON webhook payload, stringify it — the routine can parse the string in its prompt.

**Generating the per-routine token**: Web UI only. Open the routine at https://Codex.ai/code/scheduled, click pencil → Add another trigger → API → Generate token. Shown once, can't be retrieved.

## Trigger types and how to add them

| Trigger | Created via | Notes |
|---------|-------------|-------|
| Schedule | `RemoteTrigger create` (this skill) or web UI | Cron in UTC, min 1h |
| API | Web UI only (generates bearer token) | Attach to existing routine |
| GitHub event | Web UI only | Requires Codex GitHub App installed on repo |

A single routine can have multiple triggers.

## Common webhook patterns

### Pattern 1: Fireflies meeting → recap email

```
Fireflies webhook (meeting.completed)
  → POSTs {"text": "<stringified webhook JSON>"} to /fire endpoint
  → Routine parses text to get meetingId
  → curl Fireflies GraphQL API with FIREFLIES_API_KEY for full transcript
  → Codex drafts personalized recap email
  → curl Resend API with RESEND_API_KEY to send
```

Secrets needed: `FIREFLIES_API_KEY`, `RESEND_API_KEY`.

### Pattern 2: ClickUp task closed → kickoff email

```
ClickUp webhook (taskStatusUpdated, filtered to status="Closed")
  → POSTs to /fire endpoint
  → Routine calls ClickUp API with CLICKUP_API_TOKEN to get full task (client email, notes)
  → Codex drafts kickoff email with Cal.com booking link
  → Sends via Resend
```

Secrets: `CLICKUP_API_TOKEN`, `RESEND_API_KEY`, Cal.com booking link in the prompt.

### Webhook payload → /fire translation

Most third-party webhooks (Fireflies, ClickUp, Stripe, GitHub) send their own JSON shape, but `/fire` only accepts `{"text": "..."}`. Two options:

- **Configure the sender to custom body template**: set body to `{"text": "{{stringified_event}}"}`. Works for Zapier, Make, Fireflies custom webhooks.
- **Middleware**: Cloudflare Worker / Vercel function that receives the webhook, reformats, POSTs to `/fire`. Use if you want signature verification or branching logic.

## Managing routines

```
# List all
RemoteTrigger({action: "list"})

# Get one
RemoteTrigger({action: "get", trigger_id: "trig_01..."})

# Update (partial)
RemoteTrigger({action: "update", trigger_id: "trig_01...", body: {"cron_expression": "..."}})

# Fire now
RemoteTrigger({action: "run", trigger_id: "trig_01..."})
```

**Cannot delete via API**. Direct George to https://Codex.ai/code/scheduled to delete.

**Pausing**: set `"enabled": false` via update. Re-enable by setting back to `true`.

## Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `prompt: Extra inputs are not permitted` | Put `prompt` at top level | Move to `job_config.ccr.events[0].data.message.content` |
| `job_config must have "ccr" shape` | Used `session_request` or empty `job_config` | Use `job_config.ccr.{environment_id, session_context, events}` |
| `session_request.worker: Field required` | Used old `session_request` shape | Switch to `job_config.ccr` (v2 shape) |
| `invalid cron expression` | Interval < 1h, or 6-field cron | Use 5-field, ≥1h |
| `proto: unknown field "type"` | Added unknown top-level field | Remove non-schema fields |
| Session fires but does nothing visible | Expected — fire is async, output is in session URL | Check Codex.ai/code/scheduled/{trigger_id} |

## Full working example

Creates a daily 6:51 AM BST routine that scans for mentions of George and commits a report:

```python
# Pseudocode for the RemoteTrigger call
RemoteTrigger(action="create", body={
    "name": "Daily Mention Scan",
    "cron_expression": "51 5 * * *",  # 6:51 AM BST = 5:51 UTC (use 6:51 during GMT/winter)
    "enabled": True,
    "job_config": {
        "ccr": {
            "environment_id": "YOUR_ENVIRONMENT_ID",
            "session_context": {
                "model": "Codex-sonnet-4-6",
                "sources": [{"git_repository": {"url": "https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO"}}],
                "allowed_tools": ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "WebFetch", "WebSearch"]
            },
            "events": [{
                "data": {
                    "uuid": "GENERATE_FRESH_LOWERCASE_V4_UUID",
                    "session_id": "",
                    "type": "user",
                    "parent_tool_use_id": None,
                    "message": {
                        "role": "user",
                        "content": "Run WebSearch queries for 'George Lane' with after:{today-2} date filter across reddit, x, HN, linkedin, youtube, podcasts. Filter hard for newsworthy signal (notable mentions, press, complaints, big wins). Commit findings to Codex/george-scan-YYYY-MM-DD branch if anything interesting, else print 'No notable mentions.' and exit."
                    }
                }
            }]
        }
    }
})
```

Response includes `trigger.id` (prefix `trig_`). Store for future fire/update calls.

## Workflow checklist

When George asks for a new routine:

1. **Clarify the task** — what runs, when, what output, what secrets needed
2. **Check constraints** — does it need Chrome DevTools / local files / local env? If yes, redirect to local scheduler
3. **Pick schedule** — UTC, off-:00 minute, stagger against existing routines (check `RemoteTrigger list`). Remember BST vs GMT when converting London time.
4. **Pick tools** — minimum viable set (avoid adding WebFetch if not needed)
5. **Draft prompt** — self-contained, specific steps, explicit output format + save path, graceful handling of missing secrets
6. **Generate fresh UUID**
7. **Create** — `RemoteTrigger create`
8. **Test** — `RemoteTrigger run` immediately
9. **Report back** — trigger ID, schedule in local time, session URL, any secrets George still needs to add
10. **Add to active/todo.md if secrets are pending**

## Reference: active routines (update as they change)

Check `RemoteTrigger({action: "list"})` for the current set. Past history is on Codex.ai/code/scheduled.
