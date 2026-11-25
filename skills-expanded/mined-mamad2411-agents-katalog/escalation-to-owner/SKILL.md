# Escalation to Owner

## Purpose
Surfaces unresolvable decisions to Edward as a single consolidated list.

## Role
Shared — Tech Lead, PM, Security Engineer, Solution Architect, Release Manager

## Phase
Cross-phase

## Triggered By
Any role encounters a decision meeting escalation criteria.

## Inputs
- Decision context from the raising role
- Options considered and their trade-offs

## Process

### Escalation Criteria (escalate when ANY are true)
- Ambiguous requirement AC cannot resolve
- Conflicting priorities between Must Ship stories and sprint capacity
- Compliance requirement conflicting with functional requirement
- Security risk score 7-9 (Critical) on `shared/priority-scoring-model`
- Architectural decision with significant long-term trade-offs
- Budget or timeline implications beyond sprint scope
- Production incident requiring immediate decision
- Two roles irreconcilably disagree after discussion

### Do NOT Escalate
- Decisions resolvable by reading existing skills or CLAUDE.md
- Minor convention questions (check CLAUDE.md first)
- Technical implementation details within a role's domain

### Steps
1. Role identifies decision meets escalation criteria.
2. Documents escalation item in structured format.
3. PM collects all items from all roles.
4. PM consolidates into single escalation document.
5. PM surfaces to Edward at Stage 7 OR immediately if blocking.
6. Edward reviews and decides.
7. PM updates all affected artifacts with Edward's decision.
8. Resume blocked work.

## Outputs
```
# Escalation — Sprint v{X}.{Y}.{Z}
# Urgency: BLOCKING | NON-BLOCKING

## Item 1 — {short title}
Raised by: {role}
Context: {what happened, options considered}
Options:
  A) {option} — trade-offs: {trade-offs}
  B) {option} — trade-offs: {trade-offs}
Recommendation: {role's recommendation if any}
Blocking: {yes/no}
```

## Quality Gates
- [ ] All items documented with full context
- [ ] Options presented with trade-offs
- [ ] Blocking items flagged clearly
- [ ] Single consolidated document (never piecemeal)
- [ ] Edward's decision recorded after resolution

## References
- `.claude/skills/pm/planning-session-facilitation/SKILL.md` (Stage 7)
- `.claude/skills/shared/risk-logging/SKILL.md`
