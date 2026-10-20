---
name: managing-aws-sqs
description: |
  Use when working with Aws Sqs — aWS SQS queue metrics, dead letter queue
  management, SNS subscription management, message attributes, and queue health
  monitoring.
connection_type: aws
preload: false
---

# AWS SQS/SNS Management Skill

Analyze and manage SQS queues and SNS topics with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated queue/topic names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. List SQS queues
aws sqs list-queues --output json | jq -r '.QueueUrls[]?'

# 2. Get queue attributes
aws sqs get-queue-attributes --queue-url "$QUEUE_URL" --attribute-names All --output json

# 3. List SNS topics
aws sns list-topics --output json | jq -r '.Topics[].TopicArn'

# 4. List SNS subscriptions
aws sns list-subscriptions --output json | jq '.Subscriptions[] | {TopicArn, SubscriptionArn, Protocol, Endpoint}'

# 5. Get queue URL by name
aws sqs get-queue-url --queue-name my-queue --output json
```

**Phase 1 outputs:**
- Queue URLs and ARNs
- Queue attributes (message count, DLQ config, visibility timeout)
- SNS topics and subscriptions

### Phase 2: Analysis (only after Phase 1)

Only reference queue URLs, topic ARNs, and subscription ARNs confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# SQS queue attributes helper — always use this
sqs_attrs() {
    local queue_url="$1"
    aws sqs get-queue-attributes --queue-url "$queue_url" --attribute-names All --output json
}

# SNS helper
sns_cmd() {
    aws sns "$@" --output json
}

# CloudWatch metric for SQS
sqs_metric() {
    local queue_name="$1" metric="$2" stat="${3:-Sum}" period="${4:-300}"
    aws cloudwatch get-metric-statistics \
        --namespace AWS/SQS \
        --metric-name "$metric" \
        --dimensions Name=QueueName,Value="$queue_name" \
        --start-time "$(date -u -v-1H +%Y-%m-%dT%H:%M:%S 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S)" \
        --end-time "$(date -u +%Y-%m-%dT%H:%M:%S)" \
        --period "$period" \
        --statistics "$stat" \
        --output json
}
```

## Anti-Hallucination Rules

- **NEVER reference a queue URL** without confirming via `list-queues` or `get-queue-url`
- **NEVER reference a topic ARN** without confirming via `list-topics`
- **NEVER assume DLQ configuration** — always check `RedrivePolicy` attribute
- **NEVER guess queue names** — always list first
- **NEVER assume FIFO vs Standard** — check queue attributes

## Safety Rules

- **READ-ONLY ONLY**: Use only list-*, get-queue-attributes, get-topic-attributes, CloudWatch metrics
- **FORBIDDEN**: send-message, delete-message, purge-queue, delete-queue, create-queue without explicit user request
- **NEVER receive messages from production queues** without explicit user request — messages become invisible
- **Use `--attribute-names All`** to get complete queue info

## Common Operations

### Queue Overview

```bash
#!/bin/bash
echo "=== SQS Queues ==="
for QUEUE_URL in $(aws sqs list-queues --output json | jq -r '.QueueUrls[]?' 2>/dev/null); do
    QUEUE_NAME=$(echo "$QUEUE_URL" | awk -F'/' '{print $NF}')
    ATTRS=$(sqs_attrs "$QUEUE_URL" | jq '.Attributes')
    echo "$QUEUE_NAME"
    echo "  Messages: $(echo $ATTRS | jq -r '.ApproximateNumberOfMessages')"
    echo "  In-flight: $(echo $ATTRS | jq -r '.ApproximateNumberOfMessagesNotVisible')"
    echo "  Delayed: $(echo $ATTRS | jq -r '.ApproximateNumberOfMessagesDelayed')"
    echo "  Type: $(echo $ATTRS | jq -r 'if .FifoQueue == "true" then "FIFO" else "Standard" end')"
done
```

### Dead Letter Queue Analysis

```bash
#!/bin/bash
echo "=== DLQ Configuration ==="
for QUEUE_URL in $(aws sqs list-queues --output json | jq -r '.QueueUrls[]?' 2>/dev/null); do
    QUEUE_NAME=$(echo "$QUEUE_URL" | awk -F'/' '{print $NF}')
    DLQ=$(sqs_attrs "$QUEUE_URL" | jq -r '.Attributes.RedrivePolicy // "none"')
    if [ "$DLQ" != "none" ]; then
        echo "$QUEUE_NAME -> DLQ: $DLQ"
    fi
done

echo ""
echo "=== DLQ Message Counts ==="
for QUEUE_URL in $(aws sqs list-queues --queue-name-prefix "*-dlq" --output json | jq -r '.QueueUrls[]?' 2>/dev/null); do
    QUEUE_NAME=$(echo "$QUEUE_URL" | awk -F'/' '{print $NF}')
    COUNT=$(sqs_attrs "$QUEUE_URL" | jq -r '.Attributes.ApproximateNumberOfMessages')
    [ "$COUNT" != "0" ] && echo "$QUEUE_NAME: $COUNT messages"
done
```

### SNS Topic Analysis

```bash
#!/bin/bash
echo "=== SNS Topics ==="
for TOPIC_ARN in $(aws sns list-topics --output json | jq -r '.Topics[].TopicArn'); do
    TOPIC_NAME=$(echo "$TOPIC_ARN" | awk -F':' '{print $NF}')
    ATTRS=$(aws sns get-topic-attributes --topic-arn "$TOPIC_ARN" --output json | jq '.Attributes')
    echo "$TOPIC_NAME"
    echo "  Subscriptions: $(echo $ATTRS | jq -r '.SubscriptionsConfirmed')"
    echo "  Pending: $(echo $ATTRS | jq -r '.SubscriptionsPending')"
done

echo ""
echo "=== Subscriptions ==="
aws sns list-subscriptions --output json | jq '.Subscriptions[] | {TopicArn: (.TopicArn | split(":") | last), Protocol, Endpoint: (.Endpoint | .[0:60]), SubscriptionArn: (if .SubscriptionArn == "PendingConfirmation" then "PENDING" else "confirmed" end)}'
```

### Queue Metrics

```bash
#!/bin/bash
QUEUE_NAME="${1:-my-queue}"

echo "=== Message Metrics (last 1h) ==="
sqs_metric "$QUEUE_NAME" "NumberOfMessagesSent" "Sum" | jq -r '.Datapoints | sort_by(.Timestamp) | .[-5:][] | "\(.Timestamp)\tSent: \(.Sum)"'

echo ""
sqs_metric "$QUEUE_NAME" "NumberOfMessagesReceived" "Sum" | jq -r '.Datapoints | sort_by(.Timestamp) | .[-5:][] | "\(.Timestamp)\tReceived: \(.Sum)"'

echo ""
echo "=== Age of Oldest Message ==="
sqs_metric "$QUEUE_NAME" "ApproximateAgeOfOldestMessage" "Maximum" | jq -r '.Datapoints | sort_by(.Timestamp) | .[-5:][] | "\(.Timestamp)\t\(.Maximum)s"'
```

## Output Format

Present results as a structured report:
```
Managing Aws Sqs Report
═══════════════════════
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

- **Message visibility**: Receiving messages makes them invisible — do not receive from production queues for analysis
- **DLQ messages**: DLQ messages need manual investigation and reprocessing — they are not retried automatically
- **FIFO ordering**: FIFO queues guarantee order within a message group ID, not globally
- **Batch size**: SQS returns max 10 messages per receive — account for this in throughput calculations
- **Long polling**: Use `WaitTimeSeconds=20` for efficient polling — short polling wastes API calls
- **SNS filter policies**: Messages not matching filter policies are silently dropped — check filters
