---
name: engagement-management
description: Engagement-lifecycle management — pre-engagement scoping, ROE drafting, authorisation letters, threat modeling, CVSS scoring, finding write-up, executive summary, technical report, retest scoping, remediation validation. Use when the user mentions scope a pentest, ROE template, rules of engagement, get-out-of-jail letter, authorisation letter, scope statement, communications plan, blackout window, escalation matrix, threat modeling, STRIDE, PASTA, attack tree, threat actor profile, CVSS scoring, finding template, executive summary, technical report, retest, remediation validation, regression coverage, engagement kickoff, or evidence chain of custody.
---

# Engagement Management

Cross-cutting lifecycle skill. Apply `00-engagement/` from the pentest-templates library.

## Library root

`$PENTEST_LIBRARY` — caminho absoluto deste repositório clonado (definido pelo instalador; veja INSTALL.md).

## When to use

The user is:
- Scoping a new engagement.
- Drafting Rules of Engagement.
- Preparing authorisation documents.
- Building a threat model.
- Writing findings / report sections.
- Planning a retest.
- Reviewing remediation evidence.

## Phase order (lifecycle)

1. **Pre-engagement** (`00-engagement/01-pre-engagement.md`) — authorisation, scope, ROE, regulatory considerations, communications plan, tooling pre-flight. Templates:
   - `templates/scope-statement-template.md`
   - `templates/roe-template.md`
   - `templates/authorization-letter-template.md`
   - `templates/communications-plan-template.md`
2. **Threat modeling** (`00-engagement/02-threat-modeling.md`) — assets, trust boundaries, threat actors, STRIDE per boundary, ATT&CK chains, prioritisation. Template: `templates/threat-model-template.md`.
3. **Reporting** (`00-engagement/03-reporting.md`) — two-audience structure (executive + technical), CVSS, finding clustering, attack-chain narratives, quality gate. Templates:
   - `templates/finding-template.md`
   - `templates/executive-summary-template.md`
   - `templates/technical-report-template.md`
4. **Retest** (`00-engagement/04-retest-and-remediation.md`) — re-scope, retest methodology, regression detection, posture trajectory. Template: `templates/retest-report-template.md`.

## How to operate

1. **Scoping conversation** — open `00-engagement/01-pre-engagement.md` and walk every gate. Common drift sources: third-party hosting carve-outs, time windows, social-engineering allowance, evidence-handling rules.
2. **ROE drafting** — start from `templates/roe-template.md`; resolve every `<placeholder>`. For physical / red-team engagements, never deliver without authorisation letter signed by an officer with apparent authority.
3. **Threat modeling** — STRIDE per trust boundary; map ATT&CK chains; produce a prioritised target list that maps back to the assessment-type checklist (`pentest-web-api`, `pentest-active-directory`, etc.).
4. **Findings** — use `templates/finding-template.md`. Stable IDs from the library (e.g., `WEB-AUTHN-04`) become finding citations. CVSS at report time, not at discovery.
5. **Report quality gate** — apply the checklist in `00-engagement/03-reporting.md` before delivery. Critical findings notified live, not at report time.
6. **Retest** — re-execute exactly the validation steps from each finding's `Methodology`. Document regression evidence in `templates/retest-report-template.md`.

## When NOT to use

- Active testing in progress → use the type-specific skill (`pentest-web-api`, `pentest-cloud`, etc.).
- Generic security-policy writing — this skill is engagement-specific.

## Pre-conditions

- Master Services Agreement (or equivalent contract) signed.
- Client point-of-contact identified.

## OPSEC / Risk

- ROE drift is the most common cause of engagement disputes — invest time in clarity.
- Authorisation letters travel with testers at all times during physical engagements.
- Sensitive client artefacts in reports — quality gate before delivery.
- Critical findings notified live, not at report time.

## References inside the library

- Phase files: `00-engagement/01-pre-engagement.md` to `04-retest-and-remediation.md`.
- Templates: all of `templates/`.
- Frameworks: `frameworks/ptes.md`, `frameworks/nist-sp-800-115.md`, `frameworks/osstmm.md`.
