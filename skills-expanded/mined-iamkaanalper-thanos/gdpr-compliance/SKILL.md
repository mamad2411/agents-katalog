---
name: gdpr-compliance
description: GDPR compliance - data subject rights, lawful basis, DPIA, privacy by design, breach notification, consent management, cross-border transfers, PII masking. Grok-native with Production Contract.
when-to-use: When handling EU user data, building features with personal data, audits, or compliance reviews. Pair with compliance-expert or security-reviewer.
---

# GDPR Compliance Skill (Grok Port)

Patterns for building privacy-respecting systems. Focus on rights, minimization, security.

## Key Principles
- Lawful basis (consent, contract, legitimate interest) documented.
- Data minimization: only collect what's needed.
- Rights: access, rectification, erasure ("right to be forgotten"), portability, objection.
- DPIA for high-risk processing.
- Breach notification <72h.
- Privacy by design/default.
- Cross-border: SCCs or adequacy.

## Patterns
### Consent & Rights
- Granular consent, easy withdraw.
- Self-service portal for DSAR (data subject access requests).
- Erasure: cascade deletes, but retain for legal (with flags).

### Masking & Security
- PII tokenization or hashing where possible.
- Encryption at rest/transit.
- Access logging for all PII touches.
- Role-based, least privilege.

### Transfers
- No US-only without SCCs + TIA.
- Prefer EU regions.

## Grok Integration
- Use with compliance-expert agent.
- on_compliance_check hook.
- Pre-Flight: "Is this feature collecting PII? Lawful basis? DPIA needed?"
- Ledger for data flows in projects.
- Handoff: data map, rights impl, retention policy.
- Friction: log "forgot to log access" → compound for templates.
- Palace: store "chose X for consent mgmt because...".
- Compound: evolve better default privacy patterns.

## When to Use
- Any new data collection feature.
- Migrations involving user data.
- Audits or customer requests.
- Before cross-border features.

See security-review, preflight, compound. Always verify with legal for real GDPR; this is engineering patterns.
