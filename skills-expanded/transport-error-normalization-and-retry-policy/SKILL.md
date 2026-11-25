---
name: transport-error-normalization-and-retry-policy
description: "Normalize transport failures into one retry policy so streaming bridges, sockets, and remote clients fail predictably instead of improvising recovery."
metadata:
  author: ychampion
---

# SKILL: Transport Error Normalization and Retry Policy
**Domain:** remote-bridge  
**Trigger:** Use when a remote or bridge transport can fail in multiple ways and callers need one consistent rule for retrying, surfacing, or terminating.  
**Source Pattern:** Distilled from reviewed bridge transport, reconnect, and capability-broadcast error-handling implementations.

## Core Method
Translate transport-specific failures into one normalized error shape before making retry decisions. Classify each failure by whether it is transient, backoff-retryable, user-correctable, or terminal. Attach the normalized reason, any retry delay hint, and whether the caller should preserve or reset session state. Make every higher-level caller consume that normalized contract instead of branching on raw websocket, SSE, HTTP, or stream-library errors directly.

## Key Rules
- Normalize errors at the transport boundary, not separately in every caller.
- Distinguish retryable failures from terminal ones using explicit categories rather than string matching in downstream code.
- Carry retry delay hints and session-reset requirements in the normalized shape.
- Keep retries bounded and deterministic so reconnect storms do not amplify failures.
- Preserve the original cause for logging, but expose a stable contract to callers.

## Example Application
If a bridge can fail due to temporary disconnects, protocol mismatches, or authentication errors, convert those into one transport result object that says whether to retry, how long to wait, and whether the client must rebuild its session before reconnecting.

## Anti-Patterns (What NOT to do)
- Don’t let each reconnect path interpret raw transport exceptions differently.
- Don’t treat all failures as retryable; protocol or auth errors usually need a different terminal path.
- Don’t lose the original cause entirely when you normalize the outward error shape.
