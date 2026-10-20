# Security Requirements Writing

## Purpose
Produces concrete testable security requirements for inclusion in the PRD, derived from threat-modelling and compliance-assessment.

## Role
Security Engineer

## Phase
Planning (Stage 5 — contributes to PRD)

## Triggered By
PRD drafting begins, `threat-modelling` and `compliance-assessment` done.

## Inputs
- `threat-modelling` findings
- `compliance-assessment` findings

## Process
1. Compile findings from `threat-modelling` and `compliance-assessment`.
2. Write security requirements in Given/When/Then format:
   ```
   Given: {attack scenario}
   When: {attacker attempts X}
   Then: {system must Y}
   ```
3. Categorise requirements:
   - Functional security (auth, validation, encryption)
   - Non-functional security (audit logging, rate limiting, monitoring)
   - Compliance requirements (tagged as Must Ship)
4. Add to PRD Security Requirements section.
5. Verify QA can write test cases from every requirement.

## Outputs
Security Requirements section of the PRD.

## Quality Gates
- [ ] All requirements in Given/When/Then format
- [ ] QA can write automated test from every requirement
- [ ] Compliance requirements clearly tagged Must Ship
- [ ] Requirements committed to PRD

## References
- `.claude/skills/security-engineer/threat-modelling/SKILL.md`
- `.claude/skills/security-engineer/compliance-assessment/SKILL.md`
- `.claude/skills/pm/prd-writing/SKILL.md`
