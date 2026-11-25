---
name: gdpr-mobile
description: GDPR on mobile — lawful basis per processing purpose, Data Subject Access Requests (DSAR), and deletion workflows. Use when shipping in the EEA / UK or any GDPR-aligned jurisdiction.
---

# GDPR on Mobile

## Instructions

GDPR is mostly a product / process problem, but the mobile app is where most user-facing obligations land (notice, consent, export, deletion).

### 1. Lawful Basis, Per Purpose

Never treat "consent" as the default. Map each processing purpose to one of:

| Basis | Example on mobile |
| ----- | ----------------- |
| Contract | Order processing, account management, the thing the user actually signed up for. |
| Legitimate interest | Fraud prevention, security logging, basic aggregate usage analytics (documented LIA required). |
| Legal obligation | Tax record retention, lawful intercept requirements. |
| Consent | Personalized ads, cross-device tracking, optional marketing comms. |
| Vital interest | Rare; emergency contact features, some health apps. |
| Public task | Rare outside government / public services. |

Maintain a short **Record of Processing Activities** (RoPA): for each field, a purpose + basis + retention + recipients. Your DPO / legal team will ask for this.

### 2. Data Subject Rights — What to Build

Ship these flows; don't gate them behind emailing support:

- **Access (Art. 15)** — export the user's data in a portable format.
- **Rectification (Art. 16)** — edit profile / corrections.
- **Erasure / "right to be forgotten" (Art. 17)** — account deletion.
- **Restriction (Art. 18)** — pause processing without deleting.
- **Portability (Art. 20)** — machine-readable export (JSON, CSV).
- **Objection (Art. 21)** — opt out of legitimate-interest processing.
- **Automated decisions (Art. 22)** — if you make them, provide a human-review path.

### 3. Export / DSAR Path

```kotlin
// Flow (any platform):
// 1. User taps Settings → Privacy → Download My Data.
// 2. Client posts /me/export; server enqueues a job.
// 3. Job gathers from all systems (primary DB, analytics, backups in scope, logs).
// 4. Server uploads a signed, time-limited URL; notifies the app.
// 5. User downloads a password-protected ZIP with JSON / CSV / attachments.
```

Implementation notes:

- Include **all** systems of record — analytics, support ticket, CRM, push tokens.
- 30-day regulatory window; target under 7 days operationally.
- Re-authenticate the user (password + MFA) before starting the export — DSARs are a phishing target.

### 4. Deletion Path

```kotlin
// Account deletion must be reachable in the app (Apple / Play require this as of 2022 / 2024).
// 1. Confirm identity and intent (password + "type my email" pattern).
// 2. Kick off async deletion job.
// 3. Immediately: invalidate tokens, sign the user out on all devices.
// 4. Within SLA: scrub PII from primary stores; anonymize analytics; delete backups per policy.
// 5. Retain only what a legal basis requires (tax records, fraud prevention), documented.
// 6. Email confirmation when deletion completes.
```

Hard requirements:

- **App Store Guideline 5.1.1(v)** and **Play Data Safety** both require in-app deletion.
- The path cannot be deeper than Settings → Account → Delete Account.
- "Deactivate" is not deletion; keep them as separate flows.

### 5. Data Retention

Per category, document the shortest defensible retention:

- Session & auth logs: 90 days unless under investigation.
- Analytics events: 14 months at Google Analytics' default; shorter is usually better.
- Crash reports: 90 days.
- Support tickets: 2–3 years after last interaction.

Run a scheduled job that enforces retention; don't rely on manual cleanups.

### 6. International Data Transfers

- After Schrems II, transfers outside the EEA need a valid mechanism (SCCs, adequacy decision).
- For US vendors, check Data Privacy Framework status at the point of each transfer — it has been litigated before.
- Document subprocessors and transfer mechanisms in your privacy policy.

### 7. Mobile-Specific Notices

- Show the privacy notice **before** first data collection, not buried in Settings.
- Material changes require active notice on next launch.
- iOS **Privacy Nutrition Labels** and **Privacy Manifests** (`PrivacyInfo.xcprivacy`) must match your real processing — mismatches are an App Store reject and a GDPR Art. 13 problem.
- Android Play **Data Safety** form must match the in-app disclosures.

### 8. Breach Notification

- 72-hour clock to the supervisory authority starts on awareness, not confirmation.
- Have an in-app path to notify affected users where required (Art. 34).
- Pre-write the runbook: who decides, who drafts, who presses send.

### 9. Vendor / SDK Management

Every SDK that handles personal data = a data processor.

- Sign a DPA (Data Processing Addendum) before integration, not after.
- Disable SDK features you don't use (many default to maximum collection).
- Review annually; SDKs change scope silently.

## Checklist

- [ ] A RoPA exists mapping each field to purpose, basis, retention, recipients.
- [ ] Each processing purpose has a lawful basis (not defaulted to consent).
- [ ] In-app account deletion is reachable within Settings → Account.
- [ ] In-app data export produces a complete, authenticated, machine-readable archive.
- [ ] A retention job enforces documented retention per data category.
- [ ] Subprocessors and international transfer mechanisms are listed in the privacy policy.
- [ ] iOS Privacy Manifest and Play Data Safety match the real processing.
- [ ] A breach notification runbook exists and has been rehearsed.
- [ ] Every SDK handling personal data has a signed DPA.
