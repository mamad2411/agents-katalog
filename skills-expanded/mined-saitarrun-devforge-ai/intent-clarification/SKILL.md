---
name: intent-clarification
description: Extract explicit and latent user goals, resolve ambiguous requests, detect unstated business constraints, and map natural language intents to concrete engineering execution paths.
version: 1.0.0
---

# User Intent Comprehension & Goal Alignment Skill

This skill guides agents to accurately decipher what the user **actually needs** versus what they literally asked for, preventing misalignment before code is written.

---

## 1. Intent Deconstruction Framework (The 4-Layer Lens)

Whenever a user provides a prompt or feature request, analyze it through four concentric layers:

```
[Layer 1: Literal Request]       → "Add a login screen"
          ↓
[Layer 2: Underlying Objective]  → User needs secure session management and user identification
          ↓
[Layer 3: Latent Requirements]   → Password reset, OAuth/SSO, session invalidation, CSRF protection
          ↓
[Layer 4: Non-Functional Drivers]→ Enterprise compliance, low latency, zero-downtime migration
```

---

## 2. Ambiguity Detection & Resolution Matrix

If a prompt contains ambiguous or high-entropy phrasing, immediately classify and address the gap:

| Ambiguity Pattern | Example User Phrasing | Resolution Action |
|---|---|---|
| **Vague Scope** | *"Make it faster"*, *"Make it look modern"* | Quantify targets: Ask for specific p95 latency targets (e.g. <100ms) or UI design references. |
| **Architectural Ambiguity** | *"Connect to external data"* | Determine sync vs async (Webhook vs Polling vs Kafka) and error retry semantics. |
| **Missing Failure Modes** | *"Send email when user signs up"* | Clarify transactional reliability: Should signup fail if the email provider is down? |
| **Implicit Authorization** | *"Admins can manage team members"* | Ask if roles are static or configurable (RBAC vs ABAC). |

---

## 3. High-Fidelity Confirmation Protocol

When clarifying intent with the user:
1. **Replay Understandings with Options**: Present the extracted mental model back in plain language with concrete trade-offs.
2. **Proactively Suggest Industry Defaults**: Never present open-ended confusion; provide a solid (Recommended) option.
3. **Check for Unintended Side-Effects**: State potential impacts on existing workflows (e.g., *"Note: Enabling MFA will require updating the mobile login flow"*).

```markdown
**Intent Confirmation Example:**
"I understand you want to add **team workspace sharing**.
- **Primary Goal**: Allow users to invite team members with specific roles (Admin/Member/Viewer).
- **Recommended Default**: We'll use RBAC with invite links expiring in 48 hours and tenant-isolated data queries.
Does this match your intended vision?"
```
