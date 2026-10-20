# AGENTS.md — Teensurance T-Crew

Users interact with a single primary assistant, **T**, which routes internally to specialist agents. Users never select an agent directly. GUARD sits above every agent and every proposed action.

Rule: **AI explains. Rules establish requirements.** No agent may fabricate a regulatory, legal, or insurance fact.

## Agent contract (schema)

Every agent must define, in machine-readable form:

- `agent_id`, `name`, `purpose`, `objective`
- `eligible_roles`, `activation_conditions`
- `required_inputs`, `authoritative_sources`
- `available_tools`, `allowed_actions`, `prohibited_actions`
- `data_permissions`, `minor_data_permissions`, `parent_permission_requirements`
- `driving_state_permissions`
- `evidence_requirements`, `completion_criteria`
- `escalation_conditions`, `handoff_targets`
- `safety_classification`

## Agent state machine

```
NOT_ASSIGNED → ASSIGNED → ASSESSING → MISSING_INFORMATION → READY
  → IN_PROGRESS → AWAITING_VERIFICATION → VERIFIED → COMPLETED → HANDOFF
```

Also supported: `BLOCKED`, `EXPIRED`, `REQUIRES_PARENT`, `REQUIRES_OFFICIAL_SOURCE`, `REQUIRES_HUMAN_REVIEW`.

Every meaningful agent action is persisted for auditability. Hidden chain-of-thought is never persisted — only a concise decision rationale/provenance where needed.

## MVP agents

| Agent | Role | Core question |
|---|---|---|
| **VIBE** | Journey / navigation intelligence | "Where am I and what's next?" |
| **READY** | Permit / pre-driving preparation | What do I need before I can start? |
| **ACE** | Driving, insurance and foundational learning | What should I understand before I act? |
| **MILES** | Supervised driving-session logging and hour progress | Log and track supervised practice |
| **CRUZE** | Pre/post-drive practice planning and skill development | What should today's practice focus on? |
| **GO** | Licensing milestone guidance | Am I ready for the next licensing step? |
| **COVER** | Parent-facing insurance preparation and education | What should we understand before we buy? |
| **GUARD** | Safety kernel — sits above all agents | Is this action allowed right now? |

## Reserved, not yet implemented

`STACKS` (cost intelligence), `PERKS` (savings opportunities), `RYDES` (vehicle intelligence), `XP` (achievements), `MINT` (financial readiness), `LAUNCH` (independence transition). Architect extension points for these; do not build them out in the MVP.

## GUARD — safety kernel

GUARD is a deterministic policy layer, not merely an LLM prompt. Every proposed agent action passes through GUARD and receives one of:

```
ALLOW | DEFER | REQUIRE_PARENT | REQUIRE_CONSENT | REQUIRE_VERIFICATION
| REQUIRE_OFFICIAL_SOURCE | ESCALATE | DENY
```

GUARD evaluates driving state, user age, role, jurisdiction, data sensitivity, consent, guardian relationship, agent permission, notification policy, evidence requirement, regulatory boundary, and safety classification, and writes an auditable `SafetyDecision` record for every evaluation.

## Orchestration pattern

```
User → T → Intent/Context → GUARD → Specialist Agent
     → Domain Service / Tool → Deterministic Rules → Result
     → GUARD → T Explanation
```

The LLM never has direct, unrestricted database access. All state-changing actions go through domain services and deterministic rules; agents propose, GUARD authorizes, services execute.

## Human / authority escalation boundaries

T never impersonates:

- an official source of regulatory truth,
- a parent/guardian decision-maker,
- a supervisor,
- a licensed insurance professional,
- a driving instructor,
- a government authority, or
- emergency services.

Each of these is modeled explicitly as an escalation target, not folded into T's own voice.
