---
name: trigger-registry
description: "Create, manage, and test reactive triggers (webhook & event-based). Triggers execute skills or routines in response to external events (GitHub push, Stripe payment, Linear issue, etc.). Use when user says 'create trigger', 'list triggers', 'novo trigger', 'webhook para', 'quando acontecer', 'trigger list', 'test trigger', or any reference to reactive event triggers."
metadata:
  author: evonexus
  version: "1.0"
---

# Trigger Registry — Reactive Event Triggers

Create and manage triggers that execute skills or routines in response to external events (webhooks, integrations).

## When to Use

- User wants to create a webhook endpoint: "cria um webhook para quando tiver push no GitHub"
- User wants to react to events: "quando alguem abrir issue no Linear, notifica no Discord"
- User wants to list/manage triggers: "lista os triggers", "desativa o trigger de deploy"
- User wants to test a trigger: "testa o trigger #3"

## API Reference

The dashboard backend exposes these endpoints:

| Method | Endpoint | Action |
|--------|----------|--------|
| GET | `/api/triggers` | List triggers (query: `?type=webhook\|event&source=github\|stripe\|...&enabled=true\|false`) |
| POST | `/api/triggers` | Create a new trigger |
| GET | `/api/triggers/<id>` | Get trigger details + last 20 executions |
| PUT | `/api/triggers/<id>` | Update trigger |
| DELETE | `/api/triggers/<id>` | Delete trigger + executions |
| POST | `/api/triggers/<id>/test` | Test trigger (simulate execution) |
| POST | `/api/triggers/<id>/regenerate-secret` | Regenerate webhook secret |
| GET | `/api/triggers/<id>/executions` | List executions with pagination |
| POST | `/api/triggers/webhook/<id>` | **Webhook receiver** (public, HMAC-validated) |

## Trigger Types

| Type | Description |
|------|-------------|
| `webhook` | Receives HTTP POST from external services (GitHub, Stripe, etc.) |
| `event` | Reacts to integration events (configured in YAML or UI) |

## Sources & Event Examples

| Source | Signature Header | Example Events |
|--------|-----------------|----------------|
| `github` | `X-Hub-Signature-256` | push, pull_request, issues, release |
| `stripe` | `Stripe-Signature` | charge.succeeded, customer.subscription.created, invoice.paid |
| `linear` | `X-Linear-Signature` | Issue (create/update), Comment |
| `telegram` | Token-based | message, callback_query |
| `discord` | Ed25519 | message_create |
| `custom` | `X-Webhook-Signature` | Any — user-defined |

## Action Types

| Type | Payload | When to Use |
|------|---------|-------------|
| `skill` | Skill name (e.g. `discord-send-message Deploy detectado`) | Running a Claude skill |
| `prompt` | Free-form prompt text | Running a raw Claude prompt |
| `script` | Script path relative to `ADWs/routines/` | Running an existing routine script |

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

### Creating a Trigger

1. **Understand the request** — extract what event, what action, which agent:
   - **Event source:** GitHub, Stripe, Linear, Telegram, Discord, custom
   - **Event filter:** which specific events to match (e.g., push to main, charge.succeeded)
   - **Action:** what to do when triggered (skill, prompt, or script)
   - **Agent:** which agent should handle the action

2. **Confirm with user** — show summary:
   ```
   Criar trigger:
   - Nome: Deploy Notification
   - Tipo: webhook
   - Source: github
   - Filtro: event=push, branch=main, repo=EvolutionAPI/evolution-api
   - Action: skill discord-send-message Deploy detectado na main
   - Agent: @pulse
   - Enabled: true

   Confirma?
   ```

3. **Create via API:**

   Use `from dashboard.backend.sdk_client import evo` — auto-handles URL + auth.

   ```python
   from dashboard.backend.sdk_client import evo
   trigger = evo.post("/api/triggers", {
       "name": "Deploy Notification",
       "type": "webhook",
       "source": "github",
       "event_filter": {"event": "push", "branch": "main", "repo": "EvolutionAPI/evolution-api"},
       "action_type": "skill",
       "action_payload": "discord-send-message Deploy detectado na main",
       "agent": "pulse-community",
       "enabled": True,
   })
   ```

4. **Show result** — display webhook URL and secret for configuration:
   ```
   Trigger criado!
   - ID: 1
   - Webhook URL: http://localhost:8080/api/triggers/webhook/1
   - Secret: abc123... (configure no GitHub webhook settings)
   ```

### Listing Triggers

```python
from dashboard.backend.sdk_client import evo
triggers = evo.get("/api/triggers")
```

Format as table: ID | Name | Type | Source | Status | Runs

### Testing a Trigger

```python
from dashboard.backend.sdk_client import evo
evo.post("/api/triggers/1/test")
```

### Common Templates

When user selects a source, suggest pre-built event filters:

**GitHub:**
- Push to main: `{"event": "push", "branch": "main"}`
- New PR: `{"event": "pull_request", "action": "opened"}`
- Issue opened: `{"event": "issues", "action": "opened"}`
- Release published: `{"event": "release", "action": "published"}`

**Stripe:**
- Payment succeeded: `{"event_type": "charge.succeeded"}`
- New subscription: `{"event_type": "customer.subscription.created"}`
- Invoice paid: `{"event_type": "invoice.paid"}`

**Linear:**
- Issue created: `{"event_type": "Issue", "action": "create"}`
- Issue updated: `{"event_type": "Issue", "action": "update"}`
