---
name: engagement-scoping
description: Drive the pre-engagement scoping conversation and produce the scope statement, Rules of Engagement, authorisation letter, and communications plan. Use when the user mentions kickoff, scoping a pentest, drafting ROE, rules of engagement, scope statement, authorisation letter, get-out-of-jail letter, communications plan, blackout window, escalation matrix, ROE drift, third-party hosting carve-out, social-engineering allowance, time-window restrictions, or evidence-handling rules.
---

# Engagement Scoping

Pre-engagement scoping driver — produce the four core engagement documents from a structured conversation.

## Library root

`$PENTEST_LIBRARY` — caminho absoluto deste repositório clonado (definido pelo instalador; veja INSTALL.md).

Walk `00-engagement/01-pre-engagement.md` end-to-end. The four documents to produce:

1. `templates/scope-statement-template.md`
2. `templates/roe-template.md`
3. `templates/authorization-letter-template.md`
4. `templates/communications-plan-template.md`

## How to operate

1. Read `00-engagement/01-pre-engagement.md` to surface every gate the methodology requires.
2. Drive a structured conversation, group by group. Don't ask one question at a time — batch by topic:
   - **Scope group:** assets (FQDN, IP/CIDR, app builds, cloud accounts, AD domains, mobile bundles), in-scope vs out-of-scope, third-party hosting carve-outs, data-classification limits.
   - **Engagement type group:** assessment type (web/API, mobile, infra, AD, cloud, wireless, physical, red team, IoT/OT, AI/LLM), test perspective (anon, low-priv, privileged, cross-tenant), authentication artefacts.
   - **Time group:** start/end window, daily blackout windows, change-freeze overlap, holiday calendar.
   - **Allowance group:** social engineering yes/no, denial-of-service yes/no, destructive payloads yes/no, credential stuffing/spraying yes/no, exploit-code execution yes/no.
   - **People group:** white team, trusted agents, escalation matrix, SOC notification level (transparent / blue-team-aware / dark).
   - **Communications group:** primary + backup channels, cadence, critical-finding threshold, kill-switch procedure.
   - **Evidence group:** PII handling, data-residency, evidence-storage location, retention period, chain-of-custody requirements.
   - **Legal group:** authorisation signer, indemnification, liability cap, jurisdiction, regulatory considerations (PCI, HIPAA, GDPR, SOX, FERPA, NIS2, DORA).
3. After collecting answers, populate the four templates in order: scope → ROE → authorisation letter → comms plan. Return them as filled Markdown.
4. Flag missing or ambiguous answers BEFORE producing documents — ROE drift is the most common cause of engagement disputes.
5. Special rules:
   - Physical / red-team engagements: authorisation letter MUST be signed by an officer with apparent authority and travel with every tester at all times.
   - OT / ICS engagements: ROE must explicitly enumerate permitted operations per device class — default to passive observation.
   - Production data: capture metadata only unless ROE explicitly permits sample extraction.
   - Cloud engagements: confirm provider acceptable-use rules (AWS self-attest, Azure RoE, GCP customer-perspective).

## When NOT to use

- Active testing in progress → use the type-specific `pentest-*` skill.
- Finding write-up → `pentest-finding-writer`.
- Retest → `engagement-retest`.

## Pre-conditions

- Master Services Agreement (or equivalent contract) signed.
- Client point-of-contact identified.

## Output

Four Markdown documents, ready for review:

1. **Scope Statement** (in-scope assets, perspectives, exclusions).
2. **Rules of Engagement** (allowances, time windows, communications, escalation, kill switch, evidence handling).
3. **Authorisation Letter** (signed by authorised officer, contact numbers, valid date range).
4. **Communications Plan** (channels, cadence, critical-finding threshold, escalation matrix).

## References inside the library

- `00-engagement/01-pre-engagement.md`
- `templates/scope-statement-template.md`, `templates/roe-template.md`, `templates/authorization-letter-template.md`, `templates/communications-plan-template.md`
- `frameworks/ptes.md`, `frameworks/nist-sp-800-115.md`
