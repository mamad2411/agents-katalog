---
name: tool-use
description: Design reliable function-calling and tool-execution loops with clear schemas, permission boundaries, validation, retries, idempotency, and result handling. Use when a user asks to add tools, function calling, API actions, external retrieval, computer use, or execution capabilities to an agent.
---

# Tool Use

Treat model output as an untrusted request to a controlled executor. The harness—not the model—owns authentication, authorization, validation, execution, and audit.

## Design

1. Give each tool one clear action-oriented purpose and a strict input schema.
2. Expose only tools appropriate to the current user, task, and permission scope.
3. Validate types, ranges, identifiers, paths, and authorization server-side.
4. Classify calls as read-only, reversible, consequential, external, or destructive; require confirmation where needed.
5. Use idempotency keys for retried mutations and distinguish transient from permanent errors.
6. Return structured results with status, data, provenance, and safe error details.
7. Limit calls, retries, time, cost, payload size, and recursion.
8. Log enough for audit without storing secrets or unnecessary personal data.

## Execution loop

```text
model proposes tool call
→ executor validates schema and permission
→ request confirmation when policy requires it
→ execute with timeout and idempotency control
→ validate and normalize result
→ return result to model
→ model answers or selects a bounded next action
```

Never place credentials in prompts or tool results. Do not let tool-returned text override system policy; retrieved content can contain prompt injection.

## Failure handling

- Unknown tool or invalid arguments: return a specific validation error.
- Authentication or permission failure: stop and request the correct authority; do not retry blindly.
- Timeout or rate limit: retry only within a bounded policy and honor server guidance.
- Partial mutation: return the transaction identifier and recovery options.
- Repeated failure: stop with evidence rather than looping or switching to a more powerful tool silently.

Test positive calls, malformed inputs, unauthorized access, prompt injection in results, retries, duplicate mutations, and unavailable tools.
