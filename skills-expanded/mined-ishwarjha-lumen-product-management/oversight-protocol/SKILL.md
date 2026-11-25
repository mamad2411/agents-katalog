---
name: oversight-protocol
description: Canonical oversight gate format, approval templates, Level 0–3 protocol definitions, timeout rules, and override handling. Reference when pausing for PM approval, issuing a Level 2+ gate, or processing an APPROVE/DECLINE/MODIFY response.
triggers:
  [
    "oversight", "approval", "approve", "decline", "modify", "gate",
    "level 1", "level 2", "level 3", "APPROVE", "DECLINE", "MODIFY",
    "human approval", "oversight gate", "pm approval",
  ]
---

## Oversight Levels

```
Level 0 — Automated
  Scope:   Daily SignalMonitor runs, event schema validation, churn score calculation
  Gate:    None — no PM interaction required
  Log:     Written to KG if Supabase connected

Level 1 — Advisory
  Scope:   Experiment design, feature prioritisation, pricing recommendation, OKR cascade
  Gate:    No approval required
  Override: PM can type OVERRIDE: [reason] within 24 hours
  Log:     Override logged to KG if Supabase connected
  Agents:  LaunchPad (readiness audit), PriceLogic, UXLayer, RoadMap, NorthStar (OKR cascade)

Level 2 — Approval Required (blocking)
  Scope:   Pricing changes to existing customers, segment pivot, feature deprecation, ethics clearance
  Gate:    Orchestrator pauses; PM must type APPROVE / DECLINE / MODIFY
  Timeout: 48-hour window; reminder sent at 24 hours; workflow holds indefinitely until response
  Agents:  DecideWell, GrowthIQ (financial incentives), OpsCommand (board deck / crisis comms)

Level 3 — Governance Approval (elevated)
  Scope:   AI feature ethics clearance, platform policy changes, third-party data sharing, bias audit failure
  Gate:    Named person from sign_off_required_by must respond; PM cannot self-approve Level 3
  Timeout: 72-hour window; DataLayer blocks the action if no response
  Agents:  DataLayer exclusively
```

---

## Oversight Gate — Display Format

When an oversight gate is reached, the Orchestrator pauses and displays:

```
[LUMEN] Approval Required · Level [N]

Workflow:         [workflow name]
Decision:         [what is being decided — one line]
Recommended:      [agent name] — [recommended action, one sentence]
Evidence:         [2-4 key values from context, separated by ·]
Evidence Quality: [HIGH / MEDIUM / LOW — reason in one clause]
Options considered: [n]
Key risk:         [pre-mortem top risk — one sentence]

Options:
  APPROVE           — [what happens if approved]
  DECLINE           — [what happens if declined]
  MODIFY: [instructions] — [which agent re-evaluates with PM instructions]

Expires: [48 hours (Level 2) / 72 hours (Level 3)]
```

---

## PM Response Handling

**APPROVE**
- Set gate status to `approved`
- Write `decision_log_entry` with status `"approved — PM confirmed"`
- Resume workflow from the gated step
- Confirm: "Approved. Continuing [workflow step]."

**DECLINE**
- Set gate status to `declined`
- Write `decision_log_entry` with status `"declined — [PM reason]"`
- Halt workflow step
- Surface any available alternative paths
- Confirm: "Declined. [Workflow step] is paused. [Alternative if available]."

**MODIFY: [instructions]**
- Re-run the gated agent with the PM's amendments
- Present updated output for re-approval
- Do NOT resume the broader workflow until the PM approves the modified output
- **Level 3 gates:** MODIFY instructions are passed to DataLayer only — no other agent re-runs until Level 3 clearance is granted

---

## Level 1 Override Format

Level 1 gates do not pause the workflow. The PM can override after the fact:

```
OVERRIDE: [reason]
```

The override is logged to the Knowledge Graph with the PM's reason. The agent output it overrides is marked `override: true` in the decision log.

---

## Gate Trigger Conditions by Agent

| Agent | Level | Trigger condition |
|-------|-------|-------------------|
| LaunchPad (open) | 1 | Always — readiness audit always requires PM review before proceeding |
| LaunchPad (close) | 2 | Always — post-launch monitoring plan requires approval |
| PriceLogic | 1 | evidence_quality = LOW; price change > 20%; net-new tier; existing customer pricing; revenue impact > ±15% |
| PriceLogic | 2 | Any pricing change affecting existing customers |
| RoadMap | 1 | Utilisation > 90%; blocked_by_commitment_flags non-empty; de-prioritisation of committed feature |
| UXLayer | 1 | accessibility_flags non-empty; trust calibration feature present; LOW evidence |
| NorthStar | 2 | North Star metric changing (north_star_change_flag = true) |
| DecideWell | 2 | Always — every DecideWell output requires PM approval before downstream agents proceed |
| GrowthIQ | 1 | NRR < 90%; at_risk_user_list > 5 accounts; financial incentives proposed; pql_alert = true |
| OpsCommand | 1 | Output is board_deck or crisis_communication_plan; external publication |
| OpsCommand | 2 | crisis_severity_score > 7 AND board or investor communication required |
| DataLayer | 3 | Always — every DataLayer governance checkpoint requires Level 3 clearance |

---

## Timeout and Escalation Rules

**Level 2 (48h window)**
- At 24h: Orchestrator re-surfaces the gate with a reminder
- At 48h: Gate is marked `timed_out`; workflow remains paused
- On resumption: PM must still APPROVE / DECLINE / MODIFY — timeout does not auto-approve

**Level 3 (72h window)**
- At 48h: DataLayer sends escalation to `sign_off_required_by` if Slack is connected
- At 72h: Gate is marked `timed_out`; workflow blocked until named approver responds
- PM cannot override a Level 3 timeout — must come from `sign_off_required_by`

---

## Decision Log Entry Format

Every gate response writes a `decision_log_entry` to the Knowledge Graph (if Supabase connected):

```
{
  "id": "gate-[uuid]",
  "workflow": "[W1–W6]",
  "agent": "[agent name]",
  "level": [1/2/3],
  "decision": "[APPROVE / DECLINE / MODIFY]",
  "status": "[approved / declined / modified — PM confirmed / PM modified]",
  "reason": "[PM-provided reason or override text]",
  "outcome_tracking_id": "[linked to decision for 30/60/90d follow-up]",
  "timestamp": "[ISO 8601]"
}
```

If Supabase is not connected: decision log is written to session context only and lost on session end.
