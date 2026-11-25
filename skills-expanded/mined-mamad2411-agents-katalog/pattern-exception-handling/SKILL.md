---
name: pattern-exception-handling
description: Architect resilient agents with multi-tiered fallback cascades, automatic parameter repair, exponential backoff, and circuit breakers.
metadata:
  category: agent-architecture
  tier: production
  chapter: 12
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Exception Handling & Fallback Pattern

## 1. Overview & Intent

Architect resilient agents with multi-tiered fallback cascades, automatic parameter repair, exponential backoff, and circuit breakers.

> **Intent & Scope:** Use in production environments prone to LLM rate limits, context overflow, schema parse errors, or flaky downstream APIs.

---

## 2. Architectural Blueprint

```
[Primary Tool / Model Call] --(Success)--> [Continue]
            |
         (Error)
            v
[Parameter Self-Repair] --(Success)--> [Retry]
            |
         (Fails)
            v
[Fallback Model / Mock Pipeline] --------> [Graceful Response]
```

---

## 3. Core Implementation Principles

- Never let unhandled raw LLM/API tracebacks bubble up to end users.\n- **Provide an explicit fallback hierarchy:** Primary Model -> Smaller Fallback Model -> Rule-Based Safe Default.\n- Implement exponential backoff with jitter on 429 and 503 HTTP status codes.\n- **Use circuit breakers:** trip open when an external tool fails repeatedly, preventing agent stalling.

---

## 4. Reference Implementation Pattern

```python
import time

def resilient_agent_execution(prompt: str, primary_client, fallback_client, retries: int = 3):
    for attempt in range(retries):
        try:
            return primary_client.generate(prompt)
        except Exception as e:
            if "RateLimit" in str(e) or attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            break
    # Fallback cascade to secondary model
    try:
        return fallback_client.generate(prompt)
    except Exception:
        return "I am currently experiencing service degradation. Please try again shortly."

```

---

## 5. Verification & Failure Modes

- **Verification Checklist:**
  - [ ] Inputs are validated via strict typed schemas before processing.
  - [ ] Error cascades and timeouts are bounded.
  - [ ] Intermediate artifacts and trace telemetry are logged.
  - [ ] Verification criteria are objectively evaluated before task completion.

- **Common Failure Modes:**
  - **Cascading Hallucination:** Unchecked intermediate model drift polluting downstream stages.
  - **Infinite Looping:** Lack of maximum iteration guards or convergence detection.
  - **Context Bloat:** Carrying unpruned conversational history or verbose tool errors across turns.
