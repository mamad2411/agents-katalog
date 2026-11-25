---
name: llm-retry-with-typed-error-formatting
description: Wrap LLM calls in a 3-attempt exponential-backoff retry that re-raises auth errors immediately (don't retry 401/403), and on final failure formats a user-actionable message based on error type and HTTP status (529 overload, APIConnectionError, etc).
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [llm, retry, backoff, error-handling, anthropic]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/services/llm_client.py
imported_at: 2026-04-18T00:00:00Z
---

# LLM Retry with Typed Error Formatting

## When to use
You're calling provider SDKs (Anthropic, OpenAI) and want a uniform "retry transient failures, surface useful error" path. AuthenticationError and any guardrail block must propagate immediately — they won't get better with retries.

## How it works
- Hard-coded `max_attempts=3` and `backoff_seconds = 1.0; backoff_seconds *= 2` between tries.
- `AuthenticationError` re-raised as `RuntimeError("...check your API key in env or .env...")` — no retries.
- `GuardrailBlockedError` propagates unchanged (caller-relevant).
- All other exceptions retried; on final failure, a custom formatter inspects the type name and `status_code` to produce a user-actionable message ("Anthropic API is overloaded (HTTP 529) after multiple retries. Try again in a few seconds.").

## Example
```python
def invoke(self, prompt_or_messages):
    self._ensure_client()
    system, messages = _normalize_messages(prompt_or_messages)
    # ... apply guardrails ...

    backoff_seconds = 1.0
    max_attempts = 3
    last_err = None
    for attempt in range(max_attempts):
        try:
            response = self._client.messages.create(...)
            break
        except AuthenticationError as err:
            raise RuntimeError(
                "Anthropic authentication failed. Check ANTHROPIC_API_KEY in your environment or .env."
            ) from err
        except GuardrailBlockedError:
            raise
        except Exception as err:
            last_err = err
            if attempt == max_attempts - 1:
                raise RuntimeError(_format_anthropic_retry_error(err)) from err
            time.sleep(backoff_seconds)
            backoff_seconds *= 2
    else:
        raise RuntimeError("LLM invocation failed without a concrete error") from last_err
    return LLMResponse(content=_extract_text(response))


def _format_anthropic_retry_error(err: Exception) -> str:
    name = type(err).__name__
    status = getattr(err, "status_code", None)
    if name == "APIConnectionError":
        return "Anthropic API connection failed after multiple retries. Check network access and try again."
    if status == 529:
        return "Anthropic API is overloaded (HTTP 529) after multiple retries. Try again in a few seconds."
    return f"Anthropic API request failed after multiple retries: {name}."
```

## Gotchas
- The `else` on the for-loop is reachable only if the loop never breaks — useful as a "no concrete error captured" defensive path.
- Don't retry on auth errors; the user has to fix the env. Retrying makes the misconfig look like a flaky network.
- Guardrail errors must propagate at the same priority as auth — they're an explicit user-policy block, not a transient failure.
- Re-resolve API key on each call (`_ensure_client`) so a key rotated mid-process is picked up without restarting.
