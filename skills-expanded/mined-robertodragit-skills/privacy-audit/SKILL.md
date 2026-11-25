---
name: privacy-audit
description: Audit an app, website or backend for personal-data compliance (GDPR, ePrivacy, children's privacy) and produce the store privacy disclosures from the code. Builds a data inventory from the codebase and SDKs, checks lawful basis, consent, transparency, rights, retention, account deletion, processors and international transfers, then drafts the privacy policy, Apple App Privacy answers plus PrivacyInfo.xcprivacy, and Google Play Data safety answers. Use when the user asks about GDPR, privacy policy, "what data do we collect", consent banner, cookies or tracking, ATT, Apple nutrition labels, privacy manifest, Play Data safety form, account deletion, data subject requests, DPA or sub-processors, analytics/SDK privacy impact, kids' privacy, or before a store submission or a client handover.
---

# Privacy Audit

Find what personal data the product really handles, then compare that **inventory** with what the product tells people (policy, labels, consent) and what the law asks.

Output: a report from `assets/report-template.md`, plus the drafts the user asked for (policy, store worksheets, manifest).

## Ground rules

1. **Inventory first.** Every claim ties to a row in the data inventory (`assets/data-inventory-template.md`). No inventory row, no finding.
2. **Evidence or ❓.** A verdict needs a path and line, a command output, a console value the user confirmed, or a vendor-doc citation. Otherwise ❓ with the exact thing to check.
3. **Respect confidence tags.** `V` = source read on 2026-11-05. `T-s` = statutory text from training knowledge (stable, low drift). `T` = training knowledge on practice, guidance or vendor behaviour: re-verify before 🔴.
4. **Protect real data.** Never print personal data, keys or tokens found in the repo. Cite variable names and paths only.
5. **State the role.** Record whether the audited party is controller, processor or joint controller for each processing activity; developers building for clients are usually processors and the client is the controller. Findings address the right party.
6. **Conservative verdicts, no legal conclusions.** The report is an engineering-level screening, not legal advice. Prefer 🟠 with a question over a confident 🔴 on judgement calls (lawful basis, necessity, legitimate interest).

## Workflow

### Step 1 — Frame

Record: product type (mobile, web, backend), stack, controller/processor role, audience (adults, minors, employees), regions of users, special data (health, biometrics, location, children), existing documents (privacy policy, RoPA, DPA), store distribution. Ask unknowns in **one** batch.

**Done when** each of those seven items is written down or listed as an open question.

### Step 2 — Build the data inventory

Read `references/01-detection-signals.md`. Search the repo for collection points, storage, outbound data flows and SDKs; read `references/06-sdk-catalog.md` for each SDK found. Fill `assets/data-inventory-template.md`.

**Done when** (a) every personal-data field, identifier and permission found has a row with category, source, purpose, recipient, location, retention (or "unknown") and evidence path, and (b) every third-party domain and SDK in the code appears in the vendor table.

### Step 3 — Lawful basis, consent and tracking

Read `references/02-gdpr-core.md` (bases, special categories, consent) and `references/03-eprivacy-consent-tracking.md` (device access, SDK consent gating). For each processing activity assign the Art. 6 basis (plus Art. 9 condition when special data) and test the consent mechanism in code.

**Done when** every activity has a basis and every SDK that stores or reads device identifiers is classified as strictly necessary, consent-gated, or gap.

### Step 4 — Transparency, rights, retention, deletion

Compare the privacy policy to the inventory (Art. 13 content). Read `references/08-rights-retention-deletion.md` and trace the account-deletion path through every system that holds the data.

**Done when** the policy-vs-inventory table has no unexplained row, and the deletion trace lists each system as deleted, anonymised, retained-with-reason, or gap.

### Step 5 — Vendors and transfers

Read `references/09-transfers-vendors.md`. For each vendor: role, DPA, data region, transfer mechanism.

**Done when** every vendor row carries role, DPA status, region and mechanism, or ❓ with the owner of the answer.

### Step 6 — Special regimes

Open `references/07-children-sensitive-ai.md` when the inventory shows minors, health, biometrics, precise location, third-party AI processing, employees, or user-generated content. For Italian users also open `references/10-italy-notes.md`.

**Done when** each triggered regime has verdicts with citations; each non-triggered regime is ⚪ with a reason.

### Step 7 — Store disclosures

Read `references/04-apple-privacy.md` and `references/05-google-data-safety.md`. Derive answers from the inventory into `assets/apple-privacy-worksheet.md`, `assets/play-data-safety-worksheet.md` and, for iOS, a manifest based on `assets/privacy-manifest.example.xcprivacy`. Compare with answers the user already submitted.

If the repo already contains store-declaration documents (e.g. `docs/compliance/`), diff them row by row against the worksheets: omissions (an optional field in the policy missing from the Play form) and category mismatches are the usual findings.

**Done when** both worksheets are complete and every difference from the live console answers and from in-repo declaration documents is a finding.

### Step 8 — Report and drafts

Fill `assets/report-template.md`. When requested, draft the privacy policy from `assets/privacy-policy-skeleton.md` using only inventory facts. Order findings: 🔴, 🟠, store-blocking disclosures, 🟡.

**Done when** every 🔴/🟠 has evidence, citation and a concrete fix with effort (S/M/L), and the report lists what could not be verified.

## Reference navigation

Read `references/00-method.md` first in every run: verdict scale, evidence classes, legal-status snapshot (as of 2026-11-05), scope limits.

| File | Use |
|---|---|
| `00-method.md` | Method, verdicts, legal snapshot |
| `01-detection-signals.md` | Where personal data hides in code, by stack |
| `02-gdpr-core.md` | GDPR articles as audit checks |
| `03-eprivacy-consent-tracking.md` | Device access, consent, SDK gating, ATT, UMP |
| `04-apple-privacy.md` | App Privacy labels, manifest, ATT, Apple data rules |
| `05-google-data-safety.md` | Data safety form, User Data policy, Families |
| `06-sdk-catalog.md` | What common SDKs collect and how to declare it |
| `07-children-sensitive-ai.md` | Minors, special data, location, AI processing |
| `08-rights-retention-deletion.md` | Rights handling, retention, deletion cascades |
| `09-transfers-vendors.md` | Roles, DPAs, regions, SCCs, DPF |
| `10-italy-notes.md` | Italian specifics |

Hand-offs: store review readiness → `store-review-preflight` (if installed); generative-AI transparency and prohibited practices → `ai-act-audit` (if installed).
