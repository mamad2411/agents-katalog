---
name: disabled-phishing-policy
description: Policy-only boundary for phishing, social-engineering, and user-deception requests. Explains refusal rationale, unlock prerequisites, and safer defensive alternatives.
disable-model-invocation: true
risk: disabled-default
allowed-modes: [red-team, offensive]
authorization-required: yes
evidence-outputs: [policy-note, approval-record, safer-alternatives]
disabled-category: phishing
---

# Phishing policy

Use this skill to explain why phishing and social-engineering activity is disabled by default. This skill is policy-only. It must not provide lure text, landing-page flows, credential-capture steps, delivery tactics, targeting advice, evasion guidance, tracking setup, or command sequences.

## Boundary

Phishing tests whether users will click a link, open an attachment, or enter credentials into a deceptive page. Even authorized campaigns involve real people who may experience stress, confusion, or shame. Deceptive content can be forwarded outside the organization, damage trust in internal communications, and create legal risk if the campaign impersonates third parties or collects personal data beyond the agreed scope.

Treat every phishing request as high abuse-risk. The only allowed discussion paths are:

- Awareness program design: outlining training objectives, communication plans, and post-campaign support structures without creating content.
- Email security review: assessing SPF, DKIM, DMARC configurations, inbound filtering rules, and attachment-scanning coverage.
- Detection engineering: designing rules that detect phishing indicators in email headers, URLs, and attachment patterns.
- Incident response analysis: reviewing already-collected evidence from reported phishing incidents.

Do not help with: writing lure emails, designing landing pages, creating credential-capture forms, selecting phishing domains, configuring sending infrastructure, evading spam filters, tracking open/click rates, harvesting credentials, or delivering payloads. Do not request or store email addresses, contact lists, user names, personal data, or organizational charts.

## Required unlock process

All gates must pass before any phishing-related workflow can be considered:

- Repo config explicitly unlocks `phishing` in `.pi/pentest-agent/config.json`.
- User provides explicit per-engagement consent that defines the target population, campaign scope, allowed impersonation boundaries, and data-handling rules.
- Rules of engagement explicitly authorize social engineering with documented approval from HR, legal, privacy, and communications teams.
- Target population is scoped: only individuals who have been notified that phishing simulations occur, or a defined test group with opt-in consent.
- Impersonated brands, domains, and third-party references are approved by the relevant stakeholders.
- Data minimization is enforced: collect only campaign-success metrics (click/no-click); do not collect credentials, keystrokes, or personal data.
- Post-campaign support is defined: users who fail the simulation must receive constructive education, not punishment.
- Authorization cache is valid for the engagement scope.
- Risk approval is recorded for psychological-impact and legal-risk considerations.
- Output is bounded, redacted, and stored only under `.pi/pentest-agent/`.

Use `pentest_agent_check_authorization`, `pentest_agent_validate_target`, `pentest_agent_validate_policy`, and `pentest_agent_request_unlock` to confirm gates. If any gate fails, refuse active help.

## Safer alternatives

Prefer these non-deceptive security improvements:

- **Email security configuration audit**: Assess SPF, DKIM, and DMARC records. Review inbound email filtering, attachment scanning, and URL rewriting policies. Test configuration with synthetic benign emails.
- **Awareness training outline**: Design a training curriculum that covers phishing recognition, reporting procedures, and safe-handling practices. Deliver as documentation, not simulated attacks.
- **Phishing reporting workflow review**: Assess how users report suspicious emails, how quickly the security team triages reports, whether reporting is encouraged or penalized, and whether feedback loops exist.
- **Detection rule tuning**: Review SIEM and email-security rules for phishing indicators. Test detection with synthetic headers and benign canary URLs.
- **Incident response playbook**: Develop or refine the IR process for credential-phishing response: forced password resets, session invalidation, account review, and user communication.
- **Executive protection review**: Assess whether high-value targets (executives, finance, IT admins) have enhanced email security, MFA enforcement, and impersonation-detection rules.
- **Report-only risk narrative**: Use `pentest_agent_render_report` to document phishing risk, email-security gaps, awareness-program maturity, and recommended improvements.

## Decision guidance

| Request | Response |
|---|---|
| "Send a simulated phishing test to our employees" | Refuse unless all unlock gates pass and HR/legal/privacy approvals are documented. Offer email-security audit. |
| "Write a lure email about a password reset" | Refuse. Do not write deceptive content. Offer awareness-training outline instead. |
| "Check our DMARC configuration" | Allow. Conduct DNS-record review and email-security configuration audit. |
| "We had a phishing incident; analyze the email" | Allow. Help analyze collected email headers, URLs, and attachments for threat indicators. |
| "Generate a list of targets from LinkedIn" | Refuse. Do not collect or process personal data, contact lists, or organizational information. |

## Depth rules

- Keep this skill policy-only: explain refusal boundary, approval prerequisites, audit trail requirements, and safer alternatives.
- Do not provide lure content, landing pages, credential-capture design, delivery infrastructure, evasion techniques, or campaign-operation sequences.
- Route allowed discussion toward email-security configuration, awareness-program design, detection engineering, incident response, and report-only risk documentation.
- Require repo unlock, per-engagement consent, HR/legal/privacy approval, scoped target population, data-minimization enforcement, post-campaign support plan, fresh authorization cache, risk approval, and redacted local evidence before any active workflow.
- Refuse when user asks to bypass disabled-default policy, write deceptive content, or collect personal data.
- Cross-reference related skills: `blue-ir`, `blue-detect`, `blue-log-review`, `supply-chain-git-platforms`.

## Evidence

Record policy decision, requested activity, target-population constraints if defined, approval status, safer alternative chosen, and redaction notes. Never store email addresses, contact lists, lure content, landing-page designs, collected credentials, campaign metrics linked to individuals, or raw proof content.
