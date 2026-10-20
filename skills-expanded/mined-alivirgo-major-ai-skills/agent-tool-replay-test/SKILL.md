---
name: agent-tool-replay-test
description: "Replay recorded agent tool/LLM trajectories against deterministic fixtures to test argument validation, errors, idempotency, and side-effect boundaries—separate from live tool-selection quality."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-09-11"
tags: ["ai-workflows", "testing", "tool-calling", "record-replay", "cassette", "idempotency", "ci"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Agent Tool Replay Test AI Skill Guide (Claude)

## Overview & Engine Architecture

Live agents are expensive and flaky. **Record/replay at the SDK or tool boundary** gives deterministic CI: assert validation, error handling, and “must not call” policies without paying for tokens. Replay **does not** prove the model still chooses the right tools—that needs live/eval gates (`@prompt-regression-gate`).

Claude operates as a Principal Agent Test Architect for **cassettes**, **contract assertions**, **clock/ID freezing**, and **unknown-outcome** handling after timeouts.

```
┌─────────────────────────────────────────────────────────────┐
│  RECORD (once): LLM decisions ± tool results → cassette     │
│  REPLAY (CI): inject recordings; optionally run real tools  │
│  ASSERT: schemas, sequences, deny-lists, idempotency        │
└─────────────────────────────────────────────────────────────┘
```

---

## Scope

- Read tool contracts: **read-only vs mutating**.  
- Use project test runner + mocks; no production networks in `replay` mode.  
- Sanitize cassettes (no credentials)—`@ai-pii-redaction-review`.  
- Label coverage: **replay contract** ≠ **e2e model behavior**.

---

## Fixture matrix (minimum)

| Case | Expect |
| :--- | :--- |
| Success | Valid args → OK result |
| Timeout | Bounded retry policy; **unknown outcome** path |
| Permission denied | No side effect; surfaced error |
| Malformed tool JSON | Reject via `@llm-json-contract-check` |
| Partial failure | Compensating / reconcile logic |
| Unknown fields / bad IDs | Validation reject before dispatch |
| Mutating call | AuthZ + idempotency key before effect |
| Policy deny | Tool absent from allow-list never invoked |

---

## Determinism rules

- Freeze clocks/randomness; stable paths in prompts (no `uuid4()` in recorded args).  
- Modes: `record` | `replay` (CI; miss = fail, no network) | `passthrough`.  
- Prefer SDK-boundary recorders (OpenAI/Anthropic patch) over brittle raw HTTP VCR for agents.  
- Two styles: (A) stub tool results entirely; (B) replay LLM decisions but **execute** tools against safe stubs—pick explicitly.

---

## Timeout / idempotency (critical)

After a timeout on `charge`/`send_email`, state is **unknown**. Blind replay can duplicate. Require: idempotency keys, reconcile-before-retry, or human handoff (`@ai-human-handoff-contract`).

---

## Assertions to ship

- Tool sequence / `called_with` schemas  
- Forbidden tools never called  
- Budget/step caps  
- Cassette diff on prompt drift (fail or re-record deliberately)

---

## Deliverable

Fixtures + traces + “must not occur” assertions + explicit statement that selection quality is out of scope for pure replay.

## Related skills

`@llm-json-contract-check`, `@prompt-regression-gate`, `@agent-injection-boundary-test`, `@llm-cost-latency-benchmark`

## Agent Operational Directive

> **MANDATORY**: Keep replay offline in CI. Sanitize cassettes. Test validation and side-effect gates. Never blind-retry mutating calls after unknown outcomes. Separate replay coverage from model tool-selection evals.

## Sources

Cassette/agentverify/pytest-agentcontract/langchain-replay patterns; industry emphasis on SDK-level record/replay and idempotent mutating tools.
