---
name: bus
version: 1.0.0
description: Message bus communication — how agents talk to each other
uses: []
requires:
  tools: []
  env: []
security:
  risk_level: write
  capabilities:
    - bus:read
    - bus:write
  requires_approval: false
---

# Message Bus

Publish and consume messages on the file-based message bus for inter-agent communication. The bus enables asynchronous, decoupled communication between agents.

## Execution Model

This is a **builtin skill** (`handler: type: builtin`). When `bus_publish` is invoked, the executor appends a structured message to the appropriate channel file (`.os/bus/channels/{channel}.jsonl`). The tool schema in tool.yaml defines the external contract; the executor handles the file I/O directly.

## When to Use

- Publishing status updates to other agents
- Notifying that a PR was created and needs review
- Reporting review results back to the developer
- Broadcasting session start/end events
- Sending handoff context to another agent
- Publishing artifacts for other agents to discover

## Methodology

### 1. Choose the Right Channel

There are only 3 channels. **All shared work goes to `work`.**

| Channel | Purpose | Who Subscribes |
|---------|---------|---------------|
| `work` | All shared work — tasks, PRs, reviews, artifacts, handoffs | All agents (filtered by `listens_to` in identity.yaml) |
| `dm_{agent_name}` | Direct messages to a specific agent (e.g., `dm_developer`) | Only that agent |
| `system` | Lifecycle events, stop commands | All agents |

**Important**: Do NOT create topic-specific channels like `reviews`, `tasks`, or `artifacts`. All work messages go to `work`. Each agent's `listens_to` config in identity.yaml determines which message types it acts on.

### 2. Use Correct Message Types

Message types determine which agents process the message. Each agent declares what types it listens to in `identity.yaml` (`listens_to` field). Use specific types — not generic ones:

- `pr_created` (not `message`) — picked up by agents with `listens_to: [pr_created]`
- `review_completed` (not `update`) — picked up by agents with `listens_to: [review_completed]`
- `review_approved` (not `done`) — picked up by agents with `listens_to: [review_approved]`
- `task` — work assignments, picked up by agents with `listens_to: [task]`

### 3. Structure the Payload

Every message should include:
- **sender**: Your agent ID (so recipients know who sent it)
- **type**: Message type (so the right agent picks it up)
- **payload**: Relevant data (enough context to act on, not everything)

### 4. Verify Delivery

After publishing, confirm the message was written to the channel file. If the write fails, retry once before reporting an error.

## Output Format

```
## Bus Message Published

- Channel: [channel name]
- Type: [message type]
- Message ID: [generated ID]
- Timestamp: [ISO timestamp]
- Payload: [summary of payload content]
```

## Quality Criteria

- Messages use specific, descriptive types (not generic strings)
- Payload includes sufficient context for the receiver to act
- Sender field is always populated
- All shared work is published to the `work` channel (never to topic-specific channels)
- Direct messages use `dm_{agent_name}` channel (e.g., `dm_developer`)
- Messages are valid JSON
- No sensitive data (credentials, tokens) in message payloads

## Common Mistakes

- **Wrong message type**: Using `review_completed` when the review was approved (should be `review_approved`). Type determines routing — wrong type means the right agent never sees it.
- **Missing sender field**: Recipients need to know who sent the message for context and reply routing.
- **Overly generic types**: Using `update` or `message` instead of specific types like `pr_created`. Generic types don't trigger the right handlers.
- **Payload too large**: Including full file contents or diffs in messages. Reference the location instead — include paths, not content.
- **Payload too small**: Sending just a PR number with no context. Include enough information (title, summary, key files) for the receiver to start working.
- **Wrong channel**: Publishing to `reviews` or `tasks` instead of `work`. There is only one shared channel: `work`. All work messages go there. Use `dm_{name}` only for direct messages to a specific agent.
- **Polling too frequently**: Checking every second wastes resources. Poll at 5-second intervals (or use the configured interval).
- **Not tracking position**: Failing to record the last processed message ID leads to reprocessing messages after restart.

## Completion

A bus operation is complete when:
- The message is written to the correct channel file
- The message has a valid type, sender, and payload
- The write is confirmed (message appears in the file)
