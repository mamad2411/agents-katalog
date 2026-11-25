---
name: pattern-inter-agent-communication
description: Establish standardized asynchronous communication protocols, Agent Cards discovery, and JSON-RPC message contracts across distributed agents.
metadata:
  category: agent-architecture
  tier: enterprise
  chapter: 15
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Inter-Agent Communication (A2A) Pattern

## 1. Overview & Intent

Establish standardized asynchronous communication protocols, Agent Cards discovery, and JSON-RPC message contracts across distributed agents.

> **Intent & Scope:** Use for cross-system agent coordination where independent agent services collaborate across networks, cloud tenants, or organizations.

---

## 2. Architectural Blueprint

```
[Agent Service A] --(Discovery: GET /agent-card.json)--> [Agent Service B]
        |                                                       |
        +-----(JSON-RPC 2.0 Streaming Request / Event)--------->+
        <-----(Result Envelope / Intermediate Progress)---------+
```

---

## 3. Core Implementation Principles

- Publish self-describing Agent Cards containing name, version, capabilities, and input/output contracts.\n- Standardize on JSON-RPC 2.0 or REST event envelopes for network payloads.\n- Support both synchronous request-response and long-lived asynchronous streaming events.\n- Enforce mutual authentication (mTLS, API keys, or JWT tokens) across agent boundaries.

---

## 4. Reference Implementation Pattern

```python
from pydantic import BaseModel
from typing import Optional, Any

class AgentCard(BaseModel):
    name: str
    version: str
    description: str
    capabilities: list[str]
    endpoint: str

class AgentMessageEnvelope(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: dict[str, Any]
    id: str

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
