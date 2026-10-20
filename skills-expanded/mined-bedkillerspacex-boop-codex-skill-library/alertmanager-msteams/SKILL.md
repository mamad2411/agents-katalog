---
name: alertmanager-msteams
description: >
  Route Prometheus Alertmanager notifications to Microsoft Teams for owned platforms:
  webhook connectors or Workflows, receiver config, templating, grouping/inhibition,
  secret hygiene, and quiet-hours patterns. Use when wiring Alertmanager → Teams channels
  or debugging missing/noisy adaptive cards — not for spamming external tenants.
---

# Alertmanager → Microsoft Teams

## Scope And Authorization

- **In scope:** Alertmanager and Teams workspaces your organization owns.
- **Out of scope:** Posting to Teams webhooks you do not control; using alerts for harassment.
- Store webhook URLs as secrets (they are bearer capabilities).
- Prefer non-prod channel for template experiments.
- Pair config-as-code with `code-quality-standards`.

## When To Use

- Sending Alertmanager alerts to a Teams channel.
- Migrating from Office 365 Incoming Webhook to Power Automate / Workflows URLs.
- Reducing noise via routes, group_by, inhibit_rules, and severity splits.
- Fixing broken JSON templates or HTTP 4xx from Teams.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Prometheus rule quality / promtool | prometheus skills / `observability-metrics-tracing` |
| On-call / SLO design broadly | SRE skills in catalog |
| PagerDuty/Opsgenie primary | those integrations’ runbooks |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Piece | Role |
| --- | --- |
| Alertmanager `receiver` | Named notification target |
| Webhook | Teams Incoming Webhook or Workflow HTTP URL |
| `route` tree | Match labels → receiver |
| `group_by` / intervals | Collapse flapping |
| `inhibit_rules` | Suppress info when critical fires |
| Template | Custom title/text/adaptive card JSON |

**Note:** Microsoft has been evolving connectors; confirm current webhook/workflow mechanism for your tenant.

## Workflow

### 1. Confirm scope and success criteria

1. Record Alertmanager version, Teams channel, severities, on-call expectations.
2. Success: firing/resolved messages visible; secrets not in git; critical path not dropped; noise acceptable.
3. Separate channels: `#alerts-critical` vs `#alerts-warn` optional.

### 2. Create Teams webhook securely

1. Create webhook/workflow in the target channel; copy URL once.
2. Store in secret manager / sealed secret: `TEAMS_WEBHOOK_URL`.
3. Restrict channel membership; treat URL as password.

### 3. Configure Alertmanager receiver

**Native webhook (simple text):**

```yaml
# alertmanager.yml (illustrative)
global:
  resolve_timeout: 5m

route:
  receiver: teams-default
  group_by: ["alertname", "namespace", "severity"]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - matchers: ['severity=critical']
      receiver: teams-critical
      continue: false
    - matchers: ['severity=~warning|info']
      receiver: teams-default

receivers:
  - name: teams-default
    webhook_configs:
      - url_file: /etc/alertmanager/secrets/teams_default_url
        send_resolved: true
        http_config:
          follow_redirects: true
  - name: teams-critical
    webhook_configs:
      - url_file: /etc/alertmanager/secrets/teams_critical_url
        send_resolved: true

inhibit_rules:
  - source_matchers: ['severity=critical']
    target_matchers: ['severity=warning']
    equal: ['alertname', 'namespace']
```

**Sidecar / bridge (common):** many teams use `prometheus-msteams` or similar to convert Alertmanager webhook payloads into Office connector JSON. If used:

```yaml
# Still point Alertmanager at the bridge, not directly at Teams if format requires
receivers:
  - name: teams
    webhook_configs:
      - url: http://prometheus-msteams:2000/alertmanager
        send_resolved: true
```

### 4. Template content (keep actionable)

| Field | Guidance |
| --- | --- |
| Title | `alertname` + severity |
| Text | summary/description annotations |
| Link | `generatorURL` or runbook annotation |
| Color | critical red / warning orange if card supports |

Ensure every critical alert has `annotations.runbook_url` or `playbook`.

### 5. Validate config and test

```bash
amtool check-config alertmanager.yml
# Or
alertmanager --config.file=alertmanager.yml --check-config 2>/dev/null || true

# Reload
curl -X POST http://localhost:9093/-/reload

# Send test alert (authorized staging AM)
amtool alert add test_alert severity=warning instance=test --annotation=summary='teams wiring test'
```

1. Confirm message in Teams; then resolve and confirm resolve post if enabled.
2. Check Alertmanager UI → Status for notification failures.

### 6. Noise and reliability

1. Tune `group_wait` / `group_interval` / `repeat_interval`.
2. Inhibit warning when critical open.
3. Silence API access controlled (RBAC/auth in front of AM).
4. Monitor `alertmanager_notifications_failed_total`.

### 7. Hand off

1. Document channels, secret locations, route diagram.
2. Rotate webhook URLs on personnel change or leak.
3. Keep alert rules ownership separate from Teams wiring.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Secrets | `url_file` / sealed secret | Webhook URL committed |
| Routing | Severity split + inhibit | Everything to one firehose |
| Content | Runbook link | Empty “Alert firing” |
| Test | amtool in staging | Test on customer channel only |
| Failures | Metric + dead-letter awareness | Silent drop |

## Output Checklist

- [ ] Teams webhook created and stored as secret
- [ ] Receivers/routes/inhibit configured
- [ ] Config validated (`amtool` / check)
- [ ] Test fire + resolve observed in channel
- [ ] Grouping/noise settings reviewed
- [ ] Failed notification metrics watched
- [ ] Runbook annotations present on critical rules
- [ ] Rotation/ownership documented
- [ ] `code-quality-standards` on config-as-code

## Rules

- Owned Alertmanager/Teams only.
- Webhook URLs are secrets — rotate if leaked.
- Prefer actionable, grouped alerts over raw dumps.
- Do not bypass inhibitions “temporarily” without expiry.
- Keep PII out of alert labels/annotations.
