---
name: event-bus-automation-system
description: Per-workspace event bus + handler registry (prompt / webhook / event-log) that turns typed events (LabelAdd, SchedulerTick, SessionStatusChange, PreToolUse) into config-driven actions defined in automations.json.
category: automation
version: 1.0.0
version_origin: extracted
tags: [event-bus, automations, workflow, webhook, cron]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: packages/shared/src/automations/automation-system.ts
imported_at: 2026-04-18T00:00:00Z
---

# Per-workspace automation event bus

## When to use
- App where users should be able to say "when a session is labeled X, do Y" without writing code.
- You already emit typed events inside the app; you want to give users a config file that wires those events to side effects.
- Different workspaces should have independent automations (no global cross-talk).

## How it works
1. Define an `EventPayloadMap` - a typed record of every event name to its payload shape (`LabelAdd`, `LabelRemove`, `PermissionModeChange`, `FlagChange`, `SessionStatusChange`, `SchedulerTick`, `PreToolUse`, `PostToolUse`, `SessionStart`, `SessionEnd`).
2. Per workspace, instantiate a `WorkspaceEventBus` (typed `EventEmitter` with `on<K extends keyof EventMap>(event, handler)` + `emit<K>(event, payload)`).
3. On startup, parse `<workspace>/automations.json` into a typed `AutomationsConfig`, validate with a schema (`validateAutomationsConfig`).
4. Register handlers for each event kind, each subscribing to the bus:
   - `PromptHandler` - fires a new agent session with a prompt, supports `@mentions` + env var substitution (`$CRAFT_LABEL`, `$CRAFT_SESSION_ID`).
   - `WebhookHandler` - POSTs a JSON payload to a user-configured URL.
   - `EventLogHandler` - persistent audit trail under `<workspace>/automations-history.jsonl`.
5. Matchers use a regex or filtrex expression against payload fields (`matcher: "^urgent$"` or `cron: "0 9 * * 1-5"` for SchedulerTick).
6. `SchedulerService` runs a separate minute tick and emits `SchedulerTick` events so cron-driven automations live in the same bus.
7. Single `dispose()` call tears down handlers + bus + scheduler - no leaked timers.

## Example
```jsonc
// workspace/automations.json
{
  "version": 2,
  "automations": {
    "SchedulerTick": [
      { "cron": "0 9 * * 1-5", "timezone": "America/New_York",
        "actions": [{ "type": "prompt", "prompt": "Daily @github triage" }] }
    ],
    "LabelAdd": [
      { "matcher": "^urgent$",
        "actions": [{ "type": "prompt", "prompt": "Triage $CRAFT_SESSION_ID" }] }
    ]
  }
}
```

```ts
class AutomationSystem {
  eventBus = new WorkspaceEventBus();
  constructor(opts) {
    this.promptHandler   = new PromptHandler(this, opts);
    this.webhookHandler  = new WebhookHandler(this, opts);
    this.eventLogHandler = new EventLogHandler(this, opts);
    if (opts.enableScheduler) this.scheduler = new SchedulerService(this.eventBus);
  }
  emit<K extends keyof EventMap>(k: K, p: EventMap[K]) {
    this.eventBus.emit(k, p);
    this.eventLogHandler.record(k, p);
  }
}
```

## Gotchas
- Keep the event types in ONE file so they don't drift between emitter and listener.
- Schedule ticks should emit even when no automations subscribe - otherwise adding a cron rule requires restart.
- Regex matchers on user input are a footgun (ReDoS); consider length capping matcher strings.
- `env var substitution` needs to whitelist - don't let users expand `$CRAFT_API_KEY` from config.
