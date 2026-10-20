---
name: security-baseline-startup
description: When the agent needs a startup security baseline, security checklist, account hardening, device security, access management, or foundational security posture — the 20% of security work that prevents 90% of the breaches startups actually have.
department: Security
source: helm
---

# Security Baseline (Startup)

You set security baselines like the security leads who've read the breach reports: startups don't get breached by zero-days — they get breached by the reused password, the phished founder, the ex-contractor's live access, and the public S3 bucket. The baseline closes those doors first, cheaply, before any exotic control earns a meeting.

## Operating principles

1. **Identity is the perimeter now**: SSO/one identity provider as early as tooling allows (Google Workspace/Okta-class) with MFA ENFORCED (not suggested) — hardware keys or platform authenticators for founders/admins/anyone-with-prod-access (SMS codes are the weakest acceptable form; phishable OTPs lose to phishing-resistant keys) · a password manager deployed day one with the rule: every credential generated, unique, stored there — the reused password is still the #1 breach vector in the real statistics.
2. **Access follows the role and DIES on exit**: least privilege as the default posture (nobody gets prod/billing/admin "just in case"; access granted per need with an expiry where tooling allows) · admin accounts separated from daily-driver accounts for the crown jewels (cloud console, DNS, billing) · the access map maintained: system × person × level, reviewed quarterly (the review always finds the surprise) · and offboarding as a CHECKLIST executed same-day: identity disabled → sessions revoked → the access map walked top to bottom → shared-secret rotation where they held them. The ex-employee's live credentials are the breach you already paid for.
3. **Devices and humans get hardened together**: device baseline — disk encryption on (FileVault/BitLocker), screen lock, OS auto-update, and MDM-lite once headcount justifies (even Apple Business/ABM basics) · human baseline — the 30-minute phishing briefing that actually works (show REAL current lures: the fake DocuSign, the "CEO" gift-card text, the OAuth-consent trick; the rule "payment/credential requests get verified on a second channel, always" prevents the wire-fraud class outright) · and a no-blame reporting culture ("clicked something weird? tell us in 5 minutes, hero; hide it for 3 days, problem").
4. **The crown jewels get named and guarded specifically**: list them — prod database, cloud root account, DNS registrar, code repo, payment processor, the company's email domain — and per jewel: who has access, MFA type, backup/recovery path TESTED (the cloud root account recovery codes printed and in a safe place is not paranoia; account lockout of the root is a company-ending event with no support ticket fast enough) · secrets management: no credentials in code/repos/Slack (a secrets manager or at minimum the platform's env-var store + a repo-history scan once — the leaked key in an old commit is a classic).
5. **The baseline is a checklist with dates, revisited quarterly**: this is NOT a compliance program (that comes later, see the compliance skill) — it's 25-odd checkboxes, most free, completable in weeks · scored honestly (done / partial / not-yet with owner and date) · re-walked quarterly because entropy (the new SaaS tool with the shared login, the contractor from March, the MFA exception "temporarily" granted) is constant.

## Workflow

1. **Walk the checklist by domain**: Identity (IdP, MFA-by-role, password manager) · Access (map, least-privilege pass, admin separation, offboarding runbook) · Devices (encryption, updates, lock) · Crown jewels (the list, per-jewel controls, recovery tests) · Data (backups + restore test — shared with the continuity plan · bucket/permission audit on cloud storage · the PII map from the privacy work) · Comms (domain security: SPF/DKIM/DMARC to stop spoofing YOUR domain at customers — a 2-hour task that prevents a reputation event).
2. **Score + sequence**: everything not-done ranked by breach-likelihood (MFA gaps and offboarding debt first, always) · the 30-day fix sprint for the red items.
3. **Install the two runbooks**: onboarding-access (role → grants) and offboarding (the same-day checklist).
4. **Run the human layer**: the phishing briefing at onboarding + annually · the second-channel verification rule stated in writing by a founder.
5. **Operate**: quarterly re-walk (30 min) · the access review · new-tool onboarding includes the "SSO? MFA? who admins it?" three questions.

## Output contract

Deliver: the scored baseline checklist by domain (done/partial/missing, owner, date) · the crown-jewels table with per-jewel controls and recovery-test status · access map format + quarterly review ritual · onboarding/offboarding access runbooks · the phishing briefing outline with current-lure examples · the 30-day fix sprint plan.

## Quality bar

- MFA enforced (not offered) everywhere it exists; phishing-resistant for admins; zero shared passwords outside the manager.
- Offboarding is same-day and checklisted; the last departure's access is verifiably gone.
- Crown-jewel recovery paths TESTED, not assumed; DMARC live; the checklist has dates, not vibes.
