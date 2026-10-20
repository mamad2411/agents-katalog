# Compliance Application Testing

## Purpose
Dynamic testing of running UAT environment to verify compliance controls are enforced at runtime (not just in code).

## Role
Security Engineer

## Phase
UAT (per story)

## Triggered By
`zap-baseline-scan` complete.

## Inputs
- `openspec/changes/{slug}/prd.md` compliance requirements

## Rationale
Code review catches implementation mistakes. Dynamic testing catches configuration mistakes and runtime behaviour that differs from code intent.

## Process

### Tests to Perform
- Auth bypass attempts: can endpoint be accessed without valid token?
- Scope enforcement: can a token access resources outside its scope?
- TLS verification: are all endpoints HTTPS only?
- CORS policy: are cross-origin restrictions working correctly?
- Rate limiting: is rate limiting enforced on public endpoints?
- Input validation: does server reject malformed inputs?

Tools: ZAP scripts + manual test cases from compliance requirements.

### Steps
1. Read compliance requirements from `openspec/changes/{slug}/prd.md`.
2. For each requirement, perform dynamic verification against UAT.
3. Findings → bug kanban card (compliance failures always critical severity).
4. All requirements verified → signal to PM: compliance testing complete.

## Outputs
Compliance dynamic-test results; bug cards for any failures.

## Quality Gates
- [ ] Every compliance requirement tested dynamically
- [ ] Auth bypass attempts performed
- [ ] All compliance failures create critical bug cards

## References
- `.claude/skills/security-engineer/zap-baseline-scan/SKILL.md`
- `.claude/skills/pm/prd-writing/SKILL.md`
