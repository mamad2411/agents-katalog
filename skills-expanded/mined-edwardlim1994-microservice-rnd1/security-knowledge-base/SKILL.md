# Security Knowledge Base

## Purpose
Living reference document that all other Security Engineer skills consult — current standards, known CVEs for this stack, past findings.

## Role
Security Engineer

## Phase
Cross-phase (maintained continuously)

## Triggered By
Sprint start, new CVE discovered, retro improvement action.

## Inputs
- Prior knowledge-base state
- CVE feeds, retro findings

## Process
Maintain `knowledge-base.md` in place, updating each section below as new information arrives. All other Security Engineer skills read this file before executing.

### Sections
1. **Applicable Standards** (always applied):
   - OWASP Top 10 (current year)
   - OWASP API Security Top 10 (current year)
   - General secure coding principles
2. **Stack-Specific CVEs**:
   - Active CVEs affecting Bun, gRPC-js, Apollo, Kafka, Authentik, Vault
   - Severity, affected versions, mitigation status
3. **Stack-Specific Gotchas**:
   - Known security pitfalls in this tech stack
   - Findings from previous sprints
4. **Domain-Specific Standards** (when applicable):
   - GDPR/PDPA: personal data handling
   - HIPAA: healthcare data (if applicable)
   - PCI-DSS: payment data (if applicable)
   - SOC 2: enterprise/B2B (if applicable)
   - NIST 800-63: authentication flows

## Outputs
`.claude/skills/security-engineer/knowledge-base.md` (updated in place)

## Quality Gates
- [ ] Updated at sprint start
- [ ] Updated when new CVE affects this stack
- [ ] All other security skills reference this before executing

## References
- `.claude/skills/security-engineer/sprint-dependency-audit/SKILL.md`
- `.claude/skills/security-engineer/threat-modelling/SKILL.md`
