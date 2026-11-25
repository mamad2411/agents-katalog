---
name: exception-handling
description: Patterns for ensuring system resilience by detecting failures (API errors, hallucinations, validation errors) and executing predefined fallback logic. Use when user asks to "handle agent errors", "add error recovery", "make my agent fault-tolerant", or mentions exception handling, graceful degradation, or retry logic.
---

# Exception Handling & Recovery

Exception Handling ensures that an agentic system degrades gracefully rather than crashing. In the nondeterministic world of LLMs, failures are common: models hallucinate, APIs time out, and outputs are malformed. This pattern wraps critical operations in "try/catch" blocks that trigger recovery agents or fallback strategies.

## Use Cases

-   **API Fallback**: "Primary model API failed? Switch to backup model API." or "Tool A failed? Try Tool B."
-   **Refusal Handling**: If the model refuses to answer (due to safety filters), catch the refusal and rephrase the prompt or explain why it can't answer.
-   **Validation Repair**: If JSON validation fails, pass the error back to the model to fix the syntax.

## Implementation Pattern

```python
def resilient_tool_call(tool_name, args):
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            # Try to execute the tool
            return execute_tool(tool_name, args)
            
        except RateLimitError:
            # Specific handling for known errors
            backoff_sleep(attempt)
            
        except ValidationError as e:
            # Self-Correction: Ask the model to fix its input
            print(f"Validation failed: {e}. Asking model to fix...")
            args = repair_agent.fix_inputs(tool_name, args, error=e)
            
        except Exception as e:
            # General fallback
            log_error(e)
            return fallback_strategy(tool_name)
            
    raise SystemError("Max retries exceeded")
```


## Examples

**Input**: An agent making API calls that sometimes time out.

```python
@retry(max_attempts=3, backoff=exponential(base=2))
def call_api(endpoint, payload):
    try:
        return requests.post(endpoint, json=payload, timeout=10)
    except Timeout:
        log.warning(f"Timeout on {endpoint}, retrying...")
        raise  # triggers retry decorator
    except RateLimitError as e:
        wait(e.retry_after)
        raise
    except FatalError:
        alert_human("Non-recoverable error — requires manual intervention")
        raise  # don't retry
```


## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Retries amplify the problem | Rate limit errors being retried too fast | Use exponential backoff with jitter; respect `Retry-After` headers |
| Agent silently swallows errors | Bare `except` clause | Always log the exception with full stack trace before handling |
| Cascading failures | No circuit breaker | Implement circuit breaker: after 5 failures, open circuit for 60s |
| Human escalation never fires | Alert threshold too high | Test alerting path in staging; set alerting on first fatal-class error |
