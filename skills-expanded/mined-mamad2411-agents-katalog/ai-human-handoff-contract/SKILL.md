---
name: ai-human-handoff-contract
description: "Define and test AI→human handoff as a versioned state machine with multi-signal triggers, review packets, approval binding, and no silent consent. Use for escalations, approvals, and irreversible agent actions."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-09-11"
tags: ["ai-workflows", "handoff", "escalation", "human-in-the-loop", "approval", "sla"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# AI Human Handoff Contract AI Skill Guide (Claude)

## Overview & Engine Architecture

Handoff is **architecture**, not a confidence fallback. Model confidence ≠ risk. Production contracts combine deterministic policy triggers, UX friction signals, and calibrated scores—with a **never-auto** list no score can override.

Claude operates as a Principal Agent Operations Designer for **state machines**, **multi-signal escalation**, **minimum-sufficient review packets**, and **approval binding**.

```
┌─────────────────────────────────────────────────────────────┐
│  Triggers → state (active|awaiting_review|approved|…)       │
│  → review packet → human transition → resume or stop        │
│  Silence / timeout ≠ approval                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Actions the contract must name

| Action | When |
| :--- | :--- |
| **Resolve** | Low risk, covered knowledge |
| **Clarify** | Ambiguous; budget N questions |
| **Route** | Wrong team/queue |
| **Escalate / approve** | Judgment, high stake, policy |
| **Stop** | Would require unauthorized guess |

---

## Triggers (multi-signal; per-intent thresholds)

- Explicit human request (always honor)  
- Policy/risk flags (refunds, legal, medical, money movement)  
- Loop detection (N turns unresolved)  
- Sentiment / severity / account tier / $ value  
- Tool/schema failure / citation verify fail  
- Calibrated confidence **per intent** (verify calibration first)  
- **Never-answer list** (hard escalate/stop)

Owner configures thresholds; agent must not self-approve.

---

## States & rules

`active → awaiting_review → approved|rejected|expired|cancelled`

- Define permitted tools per state (mutating tools blocked while awaiting).  
- Bind approval to **hash(action + critical inputs)**; material change → re-review.  
- Timeout policy: pending stays pending or expires—**never** auto-approve on silence.  
- Unavailable reviewer → fallback queue + user messaging.

---

## Review packet (minimum sufficient)

User goal · verified facts · evidence links · actions attempted · proposed action · uncertainty/risk reason · expiry/SLA · owner · workflow version. Minimize PII (`@ai-pii-redaction-review`). Prefer links over full transcript dumps.

---

## Tests required

Missing evidence · reviewer unavailable · conflicting approvals · expiry · cancel · duplicate notify · approval after input mutation · agent attempting self-approve.

---

## Deliverable

Versioned contract YAML/doc + eval cases + reviewer template. Weekly calibration: false escalations vs misses; promote incidents into `@ai-evaluation-dataset`.

## Related skills

`@prompt-regression-gate`, `@llm-json-contract-check`, `@ai-pii-redaction-review`, `@ai-citation-verification`

## Agent Operational Directive

> **MANDATORY**: Derive triggers from risk, not confidence alone. Block irreversible actions without bound approval. Silence is not permission. Agents cannot approve themselves.

## Sources

Human escalation architecture briefs; multi-signal CS handoff guides; per-intent confidence calibration playbooks; agent-led escalation patterns.
