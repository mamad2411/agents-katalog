---
name: managing-google-pubsub
description: |
  Use when working with Google Pubsub — google Pub/Sub topic management,
  subscription health, dead letter policies, schema management, and message flow
  analysis.
connection_type: gcp
preload: false
---

# Google Pub/Sub Management Skill

Analyze and manage Google Pub/Sub with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated topic/subscription names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. List topics
gcloud pubsub topics list --project="$GCP_PROJECT" --format="table(name)"

# 2. List subscriptions
gcloud pubsub subscriptions list --project="$GCP_PROJECT" --format="table(name,topic,ackDeadlineSeconds)"

# 3. Describe a topic
gcloud pubsub topics describe "$TOPIC_NAME" --project="$GCP_PROJECT"

# 4. Describe a subscription
gcloud pubsub subscriptions describe "$SUB_NAME" --project="$GCP_PROJECT"

# 5. List schemas
gcloud pubsub schemas list --project="$GCP_PROJECT" 2>/dev/null
```

**Phase 1 outputs:**
- Topics and subscriptions
- Subscription configurations (ack deadline, DLQ, push config)
- Schemas in use

### Phase 2: Analysis (only after Phase 1)

Only reference topics, subscriptions, and schemas confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core Pub/Sub helper — always use this
pubsub_cmd() {
    gcloud pubsub "$@" --project="${GCP_PROJECT}" --format=json
}

# Cloud Monitoring metric for Pub/Sub
pubsub_metric() {
    local filter="$1"
    gcloud monitoring time-series list \
        --project="$GCP_PROJECT" \
        --filter="$filter" \
        --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
        --format=json
}
```

## Anti-Hallucination Rules

- **NEVER reference a topic** without confirming via `gcloud pubsub topics list`
- **NEVER reference a subscription** without confirming via `gcloud pubsub subscriptions list`
- **NEVER assume DLQ configuration** — always describe the subscription
- **NEVER guess schema names** — always list schemas first
- **NEVER assume push vs pull** — check subscription type

## Safety Rules

- **READ-ONLY ONLY**: Use only list, describe, snapshots list, schemas list, Cloud Monitoring queries
- **FORBIDDEN**: create, delete, publish, pull, seek, modify-ack-deadline without explicit user request
- **NEVER pull messages from production subscriptions** — they will be acknowledged
- **Use Cloud Monitoring** for message metrics instead of pulling

## Common Operations

### Topic & Subscription Overview

```bash
#!/bin/bash
echo "=== Topics ==="
pubsub_cmd topics list | jq '.[] | {name: (.name | split("/") | last), labels}'

echo ""
echo "=== Subscriptions ==="
pubsub_cmd subscriptions list | jq '.[] | {name: (.name | split("/") | last), topic: (.topic | split("/") | last), ackDeadlineSeconds, messageRetentionDuration, pushConfig: (if .pushConfig.pushEndpoint then .pushConfig.pushEndpoint else "PULL" end)}'
```

### Subscription Health

```bash
#!/bin/bash
SUB_NAME="${1:-my-subscription}"

echo "=== Subscription Details ==="
pubsub_cmd subscriptions describe "$SUB_NAME" | jq '{name, topic, ackDeadlineSeconds, messageRetentionDuration, deadLetterPolicy, retryPolicy, expirationPolicy, filter}'

echo ""
echo "=== Undelivered Messages (backlog) ==="
pubsub_metric "metric.type=\"pubsub.googleapis.com/subscription/num_undelivered_messages\" AND resource.labels.subscription_id=\"$SUB_NAME\"" | jq '.[0].points[0:5][] | {time: .interval.endTime, value: .value.int64Value}'

echo ""
echo "=== Oldest Unacked Message Age ==="
pubsub_metric "metric.type=\"pubsub.googleapis.com/subscription/oldest_unacked_message_age\" AND resource.labels.subscription_id=\"$SUB_NAME\"" | jq '.[0].points[0:5][] | {time: .interval.endTime, ageSeconds: .value.int64Value}'
```

### Dead Letter Queue Analysis

```bash
#!/bin/bash
echo "=== Subscriptions with DLQ ==="
pubsub_cmd subscriptions list | jq '[.[] | select(.deadLetterPolicy != null)] | .[] | {name: (.name | split("/") | last), deadLetterTopic: (.deadLetterPolicy.deadLetterTopic | split("/") | last), maxDeliveryAttempts: .deadLetterPolicy.maxDeliveryAttempts}'

echo ""
echo "=== DLQ Message Counts ==="
for DLQ_TOPIC in $(pubsub_cmd subscriptions list | jq -r '.[].deadLetterPolicy.deadLetterTopic // empty' | sort -u); do
    DLQ_NAME=$(echo "$DLQ_TOPIC" | awk -F'/' '{print $NF}')
    echo "--- $DLQ_NAME ---"
    pubsub_metric "metric.type=\"pubsub.googleapis.com/topic/send_message_operation_count\" AND resource.labels.topic_id=\"$DLQ_NAME\"" | jq '.[0].points[0:3][] | {time: .interval.endTime, count: .value.int64Value}' 2>/dev/null
done
```

### Schema Management

```bash
#!/bin/bash
echo "=== Schemas ==="
gcloud pubsub schemas list --project="$GCP_PROJECT" --format=json | jq '.[] | {name: (.name | split("/") | last), type, revisionId}'

echo ""
echo "=== Schema Details ==="
SCHEMA_NAME="${1:-my-schema}"
gcloud pubsub schemas describe "$SCHEMA_NAME" --project="$GCP_PROJECT" --format=json | jq '{name, type, definition}'

echo ""
echo "=== Topics with Schema Bindings ==="
pubsub_cmd topics list | jq '[.[] | select(.schemaSettings != null)] | .[] | {topic: (.name | split("/") | last), schema: .schemaSettings}'
```

## Output Format

Present results as a structured report:
```
Managing Google Pubsub Report
═════════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Pulling acknowledges**: Default pull acknowledges messages — use `--auto-ack=false` for debugging
- **Ack deadline**: Messages not acked within deadline are redelivered — check ackDeadlineSeconds
- **Message ordering**: Ordering requires ordering key — not all messages are ordered by default
- **DLQ max attempts**: Messages exceeding max delivery attempts go to DLQ — monitor DLQ topic
- **Subscription expiration**: Inactive subscriptions expire after `expirationPolicy` — check for expired subs
- **Push endpoint failures**: Push subscriptions retry with exponential backoff — check endpoint health
