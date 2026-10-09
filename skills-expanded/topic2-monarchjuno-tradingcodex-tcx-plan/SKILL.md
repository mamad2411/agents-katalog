---
name: tcx-plan
description: "Clarify an ambiguous TradingCodex mandate before immediate or recurring work by asking focused questions and preserving scope, constraints, action boundaries, approval posture, and stop conditions. Use when the user explicitly asks to plan, scope, or stress-test investment work, or when a missing choice in a schedule or automation would materially change the result or authority boundary. Clear recurring requests should use tcx-automate directly."
---

# Plan Workflow

Use this skill to turn a vague or execution-sensitive request into a compact
user mandate. The mandate feeds `$tcx-workflow` for immediate runs and
`$tcx-automate` for recurring runs. It is conversation context, not a
server-generated plan, semantic lane, selected team, role ceiling, or DAG. Head
Manager still interprets the live request, begins the lightweight analysis run,
and dynamically chooses or revises exact fixed roles from accepted evidence.

## Procedure

1. Restate the user's objective, subject scope, time or as-of horizon, requested
   output, and whether the work is immediate or recurring.
2. Extract binding constraints: symbols or universe when supplied, Strategy or
   account scope when explicitly selected, allowed actions, blocked actions,
   approval posture, evidence requirements, stop conditions, and schedule when
   recurring.
3. Ask only for missing fields whose answer would materially change the result,
   suitability, action authority, automation arming, or stop condition. Leave
   analytical decomposition and role choice to `$tcx-workflow`.
4. Preserve explicit prohibitions in the user's own terms. Do not translate
   them into a keyword classification, fixed role list, or default team.
5. Write reader-facing questions, summaries, and the `Workflow Mandate` in the user's language from the original request unless the user explicitly asks for another language.
6. Produce a compact `User Mandate` with the fields below, then hand off:
   - immediate investment work: `READY_FOR_DYNAMIC_ANALYSIS`
   - recurring workflow: `READY_FOR_AUTOMATION_PREFLIGHT`
   - missing material fields: `NEEDS_CLARIFICATION`
   - server/build request: `SERVER_OR_BUILD_HANDOFF`
   - unsafe or unsupported request: `BLOCKED_BY_SCOPE`

## Question Discipline

- Ask at most three focused questions at a time.
- Do not assign a default analytical category, stage sequence, or analyst team to
  a broad request. Ask only when unresolved scope would materially change the
  requested outcome; otherwise let Head Manager begin with the smallest useful
  question.
- Do not block general research on broker, account, or profile details that are
  irrelevant to the requested output.
- Require explicit answers for order drafting, paper execution, live execution, account/broker scope, pre-approved mandates, and recurring schedules.
- If automation is requested, require schedule, blocker policy, and expiry or rearm condition before `READY_FOR_AUTOMATION_PREFLIGHT`.

## Mandate Shape

Return this shape in prose or compact YAML:

```yaml
user_mandate:
  status: READY_FOR_DYNAMIC_ANALYSIS
  objective: ""
  requested_output: ""
  subject_scope: []
  as_of_or_horizon: ""
  recurring: false
  schedule: ""
  explicit_strategy_or_account_scope: ""
  investor_context_needed: []
  broker_scope: ""
  allowed_actions: []
  blocked_actions: []
  approval_model: ""
  evidence_requirements: []
  preflight_checks: []
  stop_conditions: []
  unresolved_questions: []
```

Keep field names, file paths, symbols, tickers, source names, and quoted source
text in their natural/original form. Do not add role candidates, stages, a lane,
or a server workflow id. `begin_analysis_run` owns the durable request hash and
sealed Brain, Strategy, and Investor Context provenance; it does not persist
this raw mandate.

## Hard Stops

- Do not dispatch subagents, choose a role team, produce investment analysis,
  approve orders, execute orders, or register automations.
- Do not create or imply a server-side semantic plan, lane, task queue, or DAG.
- Do not turn natural language into approval or execution authority.
- Do not ask for raw secrets or direct broker/API access.
- Do not widen a user's mandate while resolving ambiguity.
