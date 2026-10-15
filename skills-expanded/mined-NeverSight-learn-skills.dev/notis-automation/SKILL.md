---
name: notis-automation
description: Use when the user wants to schedule, automate, trigger, or be reminded of anything — "remind me…", "every morning…", "in two hours…", "when a new Gmail arrives", "when this record changes", "post a weekly summary". Decides between a reminder, an automation, and a skill, and builds the correct payloads.
mcp_resource: true
mcp_tool_patterns: ["LOCAL_NOTIS_*REMINDER*", "LOCAL_NOTIS_*AUTOMATION*", "LOCAL_NOTIS_LIST_INTEGRATION_TRIGGERS"]
---

# Notis Automation Skill

Use this skill whenever the user wants something to happen later, on a schedule, or in response to an event. It covers the three Notis building blocks and how they fit together:

- **Skills** hold the **business logic** — the reusable "what to do".
- **Automations** are the **glue**: they link a **trigger** to business logic. They are also how you make Notis **do something in the future**.
- **Reminders** are **dumb**: they deliver a fixed message at a time or on a schedule. No reasoning, no tools, no computed content.

The single most important job of this skill is to **pick the right primitive**, then build a valid payload for it.

## Tool names

These are native Notis tools. When their canonical `LOCAL_NOTIS_*` names are available in the current tool set, call them directly. Do not send an already-available native automation or reminder tool through `COMPOSIO_SEARCH_TOOLS` or wrap it in `COMPOSIO_MULTI_EXECUTE_TOOL`; discovery is only for a capability that is not loaded. Always call native tools by their canonical names:

| Area | Canonical tools |
|---|---|
| Reminders | `LOCAL_NOTIS_INSERT_REMINDER`, `LOCAL_NOTIS_UPDATE_REMINDER`, `LOCAL_NOTIS_LIST_REMINDERS`, `LOCAL_NOTIS_DELETE_REMINDER` |
| Automations | `LOCAL_NOTIS_INSERT_AUTOMATION`, `LOCAL_NOTIS_UPDATE_AUTOMATION`, `LOCAL_NOTIS_LIST_AUTOMATIONS`, `LOCAL_NOTIS_GET_AUTOMATION`, `LOCAL_NOTIS_RUN_AUTOMATION`, `LOCAL_NOTIS_LIST_AUTOMATION_RUNS`, `LOCAL_NOTIS_GET_AUTOMATION_RUN`, `LOCAL_NOTIS_DELETE_AUTOMATION`, `LOCAL_NOTIS_LIST_INTEGRATION_TRIGGERS` |
| Skills | `LOCAL_NOTIS_CREATE_SKILL`, `LOCAL_NOTIS_LIST_SKILLS`, `LOCAL_NOTIS_UPDATE_SKILL`, `LOCAL_NOTIS_INSTALL_SKILL`, `LOCAL_NOTIS_DISABLE_SKILL`, `LOCAL_NOTIS_DELETE_SKILL` |
| Databases (for `database` triggers) | `LOCAL_NOTIS_DATABASE_LIST_DATABASES`, `LOCAL_NOTIS_DATABASE_GET_DATABASE` |

## The paradigm

```
trigger  ->  automation  ->  business logic (often a skill)
time     ->  reminder     ->  static message
```

- A **trigger** is anything that should start work: a clock (cron), a future moment (one-time), an inbound HTTP call (webhook), an external integration event (new email, new calendar event), or a change to a Notis database record.
- An **automation** binds a trigger to a `prompt` that the Notis agent actually runs (a full agent turn). The prompt is the glue, not the place to dump a long procedure.
- A **skill** is where the real, reusable procedure lives. When the work is non-trivial or will be reused, put the steps in a skill and have the automation's prompt **cite that skill** (`/skill-name`). Keep automation prompts thin; keep logic in skills.
- A **reminder** is for when there is literally nothing to compute — the user just wants a nudge with fixed text.

### Choose the primitive

| The user wants... | Use | Why |
|---|---|---|
| A fixed nudge at a time or on a schedule ("remind me to call the dentist at 5pm") | **Reminder** | No reasoning needed — just deliver the exact text |
| Work to run on a schedule, on an event, or via a webhook ("every Monday summarize last week's deals", "reply when a new Gmail arrives") | **Automation** | A trigger must run business logic |
| To run a one-off task in the future ("in two hours, draft the recap") | **Automation** with `trigger_type: "one_time"` | "Do something later" that involves work is still an automation |
| A future message with fixed text and no computation ("at 6pm tonight, message me 'leave for the airport'") | **Reminder** with `trigger_type: "one_time"` | Future, but still just a static message |
| The procedure to be reusable across many triggers/threads | A **skill** (cited by the automation) | Business logic belongs in a skill |

Rules of thumb:

- If the action needs the agent to think, read or write a database, call any tool, fetch anything, or produce computed text → **automation**, never a reminder.
- "In the future" alone does not mean reminder. A future task with work is a **one-time automation**; a future fixed message is a **one-time reminder**.
- If you find yourself writing a long step-by-step procedure inside an automation `prompt`, stop and move it into a skill, then cite the skill from the prompt.

Before creating anything, **list what already exists** (`LOCAL_NOTIS_LIST_REMINDERS`, `LOCAL_NOTIS_LIST_AUTOMATIONS`) so you do not create a duplicate, and confirm the trigger and the action with the user in plain language.

---

## Two rules for writing automation prompts

These two mistakes break automations. Always follow them.

### 1. Never put the delivery destination in the prompt

Where the automation's response goes is set by the `channel` (and `channel_account_id`) field — **not** the prompt. The automation's output is delivered to that channel automatically.

- Do **not** write "send this to me on WhatsApp", "post the summary to Slack", "email me the result", or "reply in this thread" in the prompt.
- The prompt describes **only the work and the output to produce**. Delivery is configured separately.

```
Bad  prompt:  "Summarize yesterday's sales and post it to my Slack."
Good prompt:  "Summarize yesterday's sales."     (with channel: "slack")
```

### 2. Never put scheduling / recurrence wording in the prompt

The schedule lives in the **trigger** (the cron expression / one-time timestamp). The prompt runs *once* each time the trigger fires. If the prompt says "every morning", "each Monday", "daily", or "set this up to run…", the agent may interpret it as an instruction to **create another automation** — causing a recursive loop instead of doing the work.

- Write the prompt as a single, present-tense action to perform **right now**.
- Leave all timing/frequency to the trigger.

```
Bad  prompt:  "Every morning, send me a digest of new emails."
Good prompt:  "Compile a digest of emails received since yesterday."   (with cron: "0 8 * * *")
```

---

## Reminders (dumb message delivery)

A reminder stores a static `message` and delivers it verbatim through a channel — no agent run. Tools: `LOCAL_NOTIS_INSERT_REMINDER`, `LOCAL_NOTIS_UPDATE_REMINDER`, `LOCAL_NOTIS_LIST_REMINDERS`, `LOCAL_NOTIS_DELETE_REMINDER`.

`trigger_type` is `"schedule"` (recurring) or `"one_time"` (single future delivery). Cannot be changed after creation.

Fields:

- `message` (required) — the exact text to send (max 5000 chars). Static only. If it needs computation, it is an automation.
- `trigger_type` (required) — `"schedule"` or `"one_time"`.
- `cron_expression` (schedule only) — standard 5-field cron. **Cannot run more often than once per hour.**
- `expires_at` (one_time only) — ISO 8601 with timezone, in the future.
- `channel` (optional) — `manager`, `whatsapp`, `slack`, `telegram`, `imessage`, `sms`, `email`. Defaults to the channel the user is talking on.
- `channel_account` / `channel_account_id` (optional) — required when the user has more than one account on the target channel. Resolve which account before asking the user for an id.

Recurring reminder:

```json
{
  "trigger_type": "schedule",
  "message": "Stand up and stretch.",
  "cron_expression": "0 14 * * 1-5",
  "channel": "whatsapp"
}
```

One-time reminder:

```json
{
  "trigger_type": "one_time",
  "message": "Leave now for the airport.",
  "expires_at": "2026-06-19T16:30:00-07:00"
}
```

Notes:

- `LOCAL_NOTIS_INSERT_REMINDER` returns the new `reminder_id`, the user's `active_reminders`, and an `llm_prompt` asking you to check for duplicates — actually do that check and delete any duplicates.
- `LOCAL_NOTIS_UPDATE_REMINDER` can change `message`, `channel`, `status` (`active`/`paused`), and `cron_expression`/`expires_at` for the matching type. It cannot change `trigger_type`. For schedule reminders, the next run is managed by cron — do not try to set `expires_at`.
- `LOCAL_NOTIS_DELETE_REMINDER` is a soft delete.

---

## Automations (trigger -> business logic)

An automation runs its `prompt` as a real agent turn when its trigger fires. Tools:

| Tool | Purpose |
|---|---|
| `LOCAL_NOTIS_INSERT_AUTOMATION` | Create an automation |
| `LOCAL_NOTIS_UPDATE_AUTOMATION` | Change fields (not `trigger_type`) |
| `LOCAL_NOTIS_LIST_AUTOMATIONS` | Browse/search existing automations |
| `LOCAL_NOTIS_GET_AUTOMATION` | Read one automation in full |
| `LOCAL_NOTIS_RUN_AUTOMATION` | Fire it now (manual / test run) |
| `LOCAL_NOTIS_LIST_AUTOMATION_RUNS` | See past runs and whether delivery happened |
| `LOCAL_NOTIS_GET_AUTOMATION_RUN` | Inspect one run |
| `LOCAL_NOTIS_DELETE_AUTOMATION` | Remove it |
| `LOCAL_NOTIS_LIST_INTEGRATION_TRIGGERS` | Discover available integration triggers + config schemas (call before building an `integration` automation) |

Common `LOCAL_NOTIS_INSERT_AUTOMATION` fields:

- `prompt` (required) — the instruction the agent runs when the trigger fires (max 5000 chars). Keep it thin, present-tense, single-run; cite a skill for real logic. Follow the two prompt rules above: **no delivery destination, no recurrence wording.**
- `trigger_type` (required) — one of `schedule`, `one_time`, `webhook`, `integration`, `database`. Cannot be changed later.
- `name` (optional) — short label.
- `channel` / `channel_account_id` (optional) — **where the result is delivered**; defaults to the current channel. This is the one and only place delivery is set.
- `keep_context` (optional, default false) — `true` reuses a single pinned thread across runs; `false` starts a fresh thread each run.
- `intelligence_mode` (optional) — `auto` (default), `low`, `medium`, or `high`.

`LOCAL_NOTIS_INSERT_AUTOMATION` returns `automation_id`, the portal URLs, and — for webhooks — the `webhook_url`. Surface those to the user.

### Trigger type: schedule (recurring)

Standard 5-field cron, minimum interval one hour. The recurrence lives here — keep it out of the prompt. `expires_at` is reserved for one-time automations and must not be set on a recurring schedule. To stop a recurring automation, pause or delete it explicitly.

```json
{
  "trigger_type": "schedule",
  "name": "Weekly deal recap",
  "cron_expression": "0 9 * * 1",
  "prompt": "Compile last week's closed deals using /weekly-deal-recap and produce the summary.",
  "channel": "slack"
}
```

Cron quick reference: `0 * * * *` hourly · `0 9 * * *` daily 09:00 · `0 9 * * 1` Mondays 09:00 · `0 9 * * 1-5` weekdays 09:00. Build a concrete expression — never leave the schedule unresolved.

### Trigger type: one_time (do something in the future)

A single future run that does real work. `expires_at` is ISO 8601 with timezone, in the future.

```json
{
  "trigger_type": "one_time",
  "name": "Draft launch recap",
  "expires_at": "2026-06-20T18:00:00-07:00",
  "prompt": "Draft the launch recap from today's notes."
}
```

If the future action is just a fixed message, use a one-time **reminder** instead.

### Trigger type: webhook (inbound HTTP)

No trigger config; the tool returns a generated `webhook_url` to POST to. Give that URL to the user.

```json
{
  "trigger_type": "webhook",
  "name": "Lead intake",
  "prompt": "A new lead was posted to this webhook. Enrich it with /lead-intake and add a row to the CRM database."
}
```

### Trigger type: integration (connected app events)

Fires on an external event (new Gmail message, new calendar event, PostForMe social post or account changes, etc.). **Always call `LOCAL_NOTIS_LIST_INTEGRATION_TRIGGERS` first** — it returns providers, connected toolkits, valid `triggerName`s, each trigger's `config_schema`, and the user's `connectedAccountId`s. Never invent a provider, trigger name, or account id; use the exact values it returns. If the toolkit has multiple connected accounts, ask which one. PostForMe supports post created, updated, deleted, publish-result-created, and account-updated events; account-created is intentionally unavailable because integration cards target an existing account.

The trigger catalog is authoritative. Once the event and account are resolved, call `LOCAL_NOTIS_INSERT_AUTOMATION` directly with the returned values. **Do not call `COMPOSIO_SEARCH_TOOLS` between listing triggers and inserting the automation**: PostForMe events are provider webhook events, not Composio action tools, and the native insert tool is already known.

```json
{
  "trigger_type": "integration",
  "name": "Auto-file new emails",
  "prompt": "A new email arrived. Classify it with /email-triage and file the action items.",
  "integration_trigger_config": {
    "provider": "composio",
    "toolkit": "GMAIL",
    "triggers": [
      {
        "provider": "composio",
        "toolkit": "GMAIL",
        "triggerName": "GMAIL_NEW_GMAIL_MESSAGE",
        "config": { "label": "inbox" },
        "connectedAccountId": "ca_xxx"
      }
    ]
  }
}
```

PostForMe example:

```json
{
  "trigger_type": "integration",
  "name": "Notify on new LinkedIn posts",
  "prompt": "Summarize the new social post in one sentence.",
  "channel": "manager",
  "integration_trigger_config": {
    "provider": "postforme",
    "toolkit": "LINKEDIN",
    "triggers": [
      {
        "provider": "postforme",
        "toolkit": "LINKEDIN",
        "triggerName": "social.post.created",
        "connectedAccountId": "spc_xxx",
        "config": {}
      }
    ]
  }
}
```

### Trigger type: database (Notis record change)

Fires when records in a native Notis database are added or changed. Use `LOCAL_NOTIS_DATABASE_LIST_DATABASES` and `LOCAL_NOTIS_DATABASE_GET_DATABASE` (see the `notis-query` skill) to resolve the real `database_id` and the exact `property_id`s before building the config — never guess them.

The config is `{ database_id, root }`, where `root` is a condition tree. Each condition's `event` is one of `page_added` (record inserted), `any_property_edited` (any property changed), or `property_edited` (a specific property changed, requires `property_id` + `comparator`). Comparators depend on the property kind (e.g. `equals`, `changed_from_to`, `contains`, `greater_than`, `before`). `changed_from_to` needs `from_value` + `to_value`; value-based comparators need `value`.

```json
{
  "trigger_type": "database",
  "name": "Notify on task done",
  "prompt": "A task was just marked Done. Run /task-followup to add a note and check for follow-ups.",
  "database_trigger_config": {
    "database_id": "tasks-db-id",
    "root": {
      "kind": "group",
      "operator": "and",
      "children": [
        {
          "kind": "condition",
          "event": "property_edited",
          "property_id": "prop_status",
          "comparator": "changed_from_to",
          "from_value": "In Progress",
          "to_value": "Done"
        }
      ]
    }
  }
}
```

### Running, verifying, updating

- `LOCAL_NOTIS_RUN_AUTOMATION` fires immediately (good for a test) and returns a `run_id`.
- `LOCAL_NOTIS_LIST_AUTOMATION_RUNS` shows whether each run produced a delivered message (`delivery_detected`) — use it to confirm an automation actually works.
- `LOCAL_NOTIS_UPDATE_AUTOMATION` changes any field except `trigger_type`; set `status` to `paused`/`active` to disable/enable. Automations synced from a team template (`automation_template_id` present) lock `name` and `prompt` — tell the user to duplicate it to edit.

---

## The skill-as-business-logic pattern

This is the core of the paradigm: **put logic in a skill, point an automation at it.**

**Creating the skill: use `notis-skill-creator`.** Whenever the business logic needs to live in a new (or updated) skill, follow the `notis-skill-creator` skill — it is the source of truth for the authoring workflow: defining the `name`/`description`, structuring `SKILL.md` (and optional `scripts/`/`references/`/`assets/`), validating the frontmatter, and saving directly into Notis with `LOCAL_NOTIS_CREATE_SKILL` (`name`, `description`, and `skill_md` or `bundle_url`). Do not hand-roll skill creation here; defer to `notis-skill-creator` for the details, then come back and wire the automation to it.

Worked example — "Every Monday, summarize last week's closed deals and post to Slack":

1. **Logic → skill.** If no skill covers it, author one by following `notis-skill-creator` and saving it with `LOCAL_NOTIS_CREATE_SKILL`. The skill `SKILL.md` holds the real procedure: which database to query, how to filter to last week's closed deals, and the summary format.
2. **Trigger + delivery → automation.** Create a `schedule` automation whose `prompt` cites the skill, and set the delivery channel on the `channel` field — not in the prompt:

   ```json
   {
     "trigger_type": "schedule",
     "name": "Weekly deal recap",
     "cron_expression": "0 9 * * 1",
     "prompt": "Run /weekly-deal-recap for last week and produce the summary.",
     "channel": "slack",
     "channel_account_id": "channel_slack:acme#T123"
   }
   ```

   The cron carries the "every Monday"; the channel carries "to Slack". The prompt carries neither.
3. **When the trigger fires**, Notis injects the cited skill's full `SKILL.md` as the workflow and executes it, then delivers the output to the configured channel. The automation stayed thin; the logic stayed reusable.

Use the same pattern for webhook, integration, and database automations: the trigger differs, but the `prompt` should still hand off to a skill for any non-trivial work. Reach for an inline prompt only when the action is a single, self-evident instruction.

---

## House rules

- **Plain language to the user.** Talk about "a reminder", "a weekly automation", "the Slack channel", "the Tasks database" — not tool names, `trigger_type` values, or raw JSON. Build and validate the payloads internally.
- **Delivery is the channel, never the prompt.** Set where output goes via `channel`/`channel_account_id`. Keep "send to…", "post to…", "email me…", "reply in thread" out of the automation `prompt`.
- **No recurrence wording in the prompt.** The schedule lives in the trigger. A prompt that says "every morning" or "set up a daily…" risks the agent creating another automation instead of doing the work. Write the prompt as one present-tense action.
- **Discover before you ask.** Resolve picker-backed values yourself before asking the user: channel account (when multiple), integration toolkit/trigger/connected account (`LOCAL_NOTIS_LIST_INTEGRATION_TRIGGERS`), and database id + property ids (`LOCAL_NOTIS_DATABASE_LIST_DATABASES` / `LOCAL_NOTIS_DATABASE_GET_DATABASE`). One match → confirm; several → offer the choices; none → ask or defer.
- **Never invent identifiers.** Integration providers, `triggerName`s, `connectedAccountId`s, `database_id`s, and `property_id`s must come from discovery, not memory.
- **Resolve the schedule.** A schedule trigger needs a concrete cron expression; a one-time trigger needs a real future timestamp with timezone. Do not create a scheduled item with the timing unresolved.
- **Dedupe.** List existing reminders/automations first and remove duplicates rather than stacking near-identical ones.
- **Confirm, then create.** Recap the trigger and the action in one short plain-language line, get a yes, create it, then surface the portal URL (and webhook URL, if any).
- **Right primitive.** Static message → reminder. Work on a trigger → automation. Reusable logic → skill cited by the automation. When in doubt between a one-time reminder and a one-time automation, ask whether the future action is fixed text or actual work.
