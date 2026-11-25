---
name: store-review-preflight
description: Preflight a mobile app before App Store or Google Play submission. Audits the codebase, build config and store metadata against the Apple App Review Guidelines, Apple build requirements (privacy manifests, required-reason APIs, SDK signatures, Xcode/SDK minimums) and Google Play policies (Data safety, target API, account deletion, permissions, Families), then writes an evidence-backed rejection-risk report. Use when the user is about to submit, asks "will this pass review", "is the app ready for the App Store / Play", "check store compliance", got a rejection or an ITMS-/Play Console error, is preparing TestFlight external testing or a production release, or ships an Expo, React Native, Capacitor, Flutter or native iOS/Android app.
---

# Store Review Preflight

Audit the app **before the reviewer does**. Every finding is a **rule** (a policy clause) or a **gate** (a binary build/upload requirement), backed by **evidence** from the repo, the build artifact, the store console or the listing.

Output: a report built from `assets/report-template.md`. The audit is read-only: never upload, submit, publish, or run store CLIs.

## Ground rules

1. **Evidence or ❓.** A verdict needs a file path and line, a command output, a user-confirmed console value, or a listing quote. No evidence → ❓ Unverified, with the exact thing to check.
2. **Cite the rule ID** for every finding (`Apple 5.1.1(v)`, `Play: User Data → Account deletion`).
3. **Respect confidence tags.** Rows tagged `T` come from training knowledge, not from a page read on 2026-11-05. Re-open the live source (URLs in `references/00-method.md` §4) before issuing 🔴 on a `T` row.
4. **Conservative verdicts.** Prefer 🟠 over a false 🟢 and over a false 🔴. Never promise approval: reviewers apply judgement.
5. **Hand off depth.** Privacy disclosures, consent and SDK data flows belong to the `privacy-audit` skill when installed; this skill checks only that the disclosures exist, are consistent with the code, and satisfy the store rule.

## Workflow

### Step 1 — Frame the target

Record: platforms (iOS, Android, both), stack (see `references/01-signals.md` §1), first submission vs update, developer account type (individual vs organization: it changes Apple 5.1.1(ix) and the Google testing requirement), monetization model, audience age, regions. Ask the user for unknowns in **one** batch.

Then read what the project already has: `docs/`, `store/`, `fastlane/`, store and compliance notes, and scripts named like `*check*`, `*store*`, `*review*`. Treat documented mitigations as claims to **verify**, not as findings and not as proof (a fallback contact address, a feature flag, a pre-submission script that is never run automatically).

Feature flags and `EXPO_PUBLIC_*`/env switches decide which code ships. Their production values live in the build environment (K): list each flag that gates a store-relevant feature and ask the user for its production value.

**Done when** all seven items are written down or listed as open questions, existing store/compliance documents are listed, and each store-relevant flag has a value or an open question.

### Step 2 — Inventory capabilities

Read `references/01-signals.md`. Search the repo for each capability signal and fill the capability table (found / not found + path).

**Done when** every capability row has a status and, if found, at least one path.

### Step 3 — Run the gates

Gates fail uploads or builds regardless of reviewer opinion. Read `references/apple-06-technical-gates.md` for iOS and `references/google-02-technical-gates.md` for Android. Run the commands each gate lists; mark gates that need a build artifact as ❓ and hand the user the exact command.

**Done when** every gate is 🟢, 🔴 or ❓-with-command.

### Step 4 — Triage rules

Open the triage matrix in `references/00-method.md` §5. For each capability found in Step 2, list the rule IDs it triggers and the reference files that hold them.

**Done when** every found capability maps to rule IDs, and every not-found capability category is recorded as ⚪ with a reason.

### Step 5 — Assess triggered rules

Read **only** the triggered files:

| File | Covers |
|---|---|
| `apple-01-safety.md` | Guideline 1: content, UGC, kids, health, developer info |
| `apple-02-performance.md` | Guideline 2: completeness, metadata, hardware, software requirements |
| `apple-03-business.md` | Guideline 3: In-App Purchase, subscriptions, other payment methods, crypto |
| `apple-04-design.md` | Guideline 4: copycats, minimum functionality, spam, extensions, Sign in with Apple |
| `apple-05-legal.md` | Guideline 5: privacy, data use, health, kids, location, IP, gambling, VPN |
| `google-01-policies.md` | Play Developer Program Policy: content, user data, permissions, families, monetization, ads |
| `07-common-rejections.md` | Field patterns behind most rejections, with the fix |

Check each triggered row: pass / fail / uncertain, with evidence and citation.

**Done when** every triggered rule has a verdict, evidence and citation.

### Step 6 — Console and listing checklist

Code cannot show App Store Connect or Play Console state. Walk `assets/console-checklist.md` with the user (screenshots or exports are fine). Draft reviewer notes from `assets/review-notes-template.md`.

**Done when** every checklist row is verified, user-confirmed, or listed as unknown.

### Step 7 — Report

Fill `assets/report-template.md`. Order the fix list: upload-blocking gates, then 🔴 rules, then 🟠, then metadata, then 🟡. Every 🔴 and 🟠 carries a concrete fix and an effort estimate (S/M/L).

**Done when** no 🔴/🟠 finding lacks a fix, and the report states what it could not verify.

## Reference navigation

Read `references/00-method.md` first in every run: verdict scale, evidence classes, freshness protocol, triage matrix.

Stack-specific traps (Expo config plugins, Capacitor native projects, WebView wrappers, OTA updates) live in `references/08-stack-notes.md`. Non-store regulation that blocks a release (EU DSA trader status, US state age-assurance laws, accessibility) lives in `references/09-regulatory-gates.md`.
