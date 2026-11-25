---
name: guardrails
description: Validate LLM outputs against constraints, detect hallucinations, enforce structured responses — use when any agent generates content, answers questions, or produces code
allowed-tools: [Read, Grep, Bash]
---

# Guardrails Skill

## When to Invoke

- **Auto-invoked** on any agent output validation context
- Any agent generates user-facing content
- Any agent produces code, SQL, or structured data
- Any agent answers factual questions
- After LLM completion, before delivery downstream

## Validation Pipeline

```
Agent Output
    ↓
Schema Check (structured output enforcement)
    ↓
Hallucination Score (threshold 0.85)
    ↓
Factuality Check (against source data / RAG context)
    ↓
Provenance Verification (RAG grounding validators)
    ↓
PII / Toxicity Filters
    ↓
[PASS] → Validated Output
[FAIL] → Retry with grounding OR Reject
```

## Key Thresholds

- **Hallucination score**: minimum 0.85 (below → retry with grounding)
- **Factuality score**: minimum 0.80 (below → reject)
- **Relevance score**: minimum 0.75 (below → retry)
- **Max retries**: 3 (after which reject with audit log)

## Hub Validators Used

| Validator | Purpose |
|-----------|---------|
| `hub://guardrails/hallucination_free` | Detects fabricated facts |
| `hub://guardrails/provenance_llm` | Verifies RAG grounding |
| `hub://guardrails/toxic_language` | Filters toxic content |
| `hub://guardrails/detect_pii` | Masks PII (email, phone, SSN) |

## Backend Integration

All LLM calls in `backend/` must go through `app.middleware.guardrails.guard_llm_call()`.

```python
from app.middleware.guardrails import guard_llm_call

validated = await guard_llm_call(
    llm.complete,
    prompt=user_query,
    source_context=rag_docs,
    schema={"type": "object", "properties": {"answer": {"type": "string"}}},
)
```

## Audit Trail

Every validation — pass or fail — is logged to the immutable audit trail with:
- attempt number
- status (pass/fail/retry/reject)
- hallucination, factuality, relevance scores
- failed validators list
- timestamp and correlation ID
