---
name: shipping-ios-apps
description: Use when asked to take an iOS app from an idea all the way to a published App Store release ("build me an app that X and publish it", "take this idea live", "make and ship an app"), or to resume an app partway through that journey — branding, build, testing, design audit, store assets, or release.
disable-model-invocation: true
---

# Shipping iOS Apps

## Overview

Drive an app from one user prompt to a submitted App Store release through a **phase-gated pipeline that loops until each gate passes**. You orchestrate; the listed sub-skills do the work. The user gives the idea once, answers ONE decision batch, and the pipeline runs — it does not stop to ask again except for the gates they explicitly reserved.

**Iron rules:**
- Never skip a phase or declare a gate passed without its named evidence.
- Every failure loops back into its phase — a rejection, red test, or audit finding is a work item, never a stopping point.
- All state lives in `SHIP.md` at the repo root so any future session resumes mid-pipeline.

## Phase 0 — One decision batch (before anything else)

Load `brainstorming` to shape the idea, then ask the user ONE batch (AskUserQuestion, ~2 rounds max) covering **everything needed to reach submission without further questions**:

1. App name + bundle id + pricing (free/paid) + age-rating expectations
2. Scope cut for v1 (propose one; they approve/trim)
3. Privacy policy: URL they own, or approval to generate + host one they'll review
4. Release mode: submit-for-review automatically vs stop at upload; automatic-release-on-approval or manual
5. Which later gates they want to personally sign off (design look-and-feel, TestFlight on-device) vs delegate — **default: delegate, keep going**. Exception: the **release review page (Phase 7) is reserved by default** — the pipeline stops there for approval unless the user explicitly waives it here.

Write all answers into `SHIP.md`. These are standing authorizations — the point of this skill is the user does NOT get re-asked at each phase.

## The pipeline

| # | Phase | REQUIRED SUB-SKILL(s) | Exit gate (named evidence) |
|---|-------|------------------------|---------------------------|
| 1 | Branding | `brainstorming`; icon via image generation (Higgsfield) or vector; define theme tokens (colors/fonts) | Icon asset in repo, theme file, name/bundle id final in `SHIP.md` |
| 2 | Scaffold | house pattern: XcodeGen `project.yml`, SwiftUI, Swift Testing target, fastlane dir | `xcodegen && xcodebuild build` clean on an agent-created simulator |
| 3 | Build features | `tdd-workflow`, `swift-patterns`, `swift-testing`; `humanizer` on every user-facing string as it is written | Per feature: tests green first-class; whole suite green |
| 4 | Verification | `verify-app` (matrix + pre-commit/Stop hooks) | Matrix exists, hooks installed, **no ❌ rows on shipped features** |
| 5 | Design audit | `audit-app-design` (+ `emil-design-eng` for polish); `humanizer` for the copy sweep | Re-audit loop until **zero HIGH findings**; light+dark, Dynamic Type, empty states checked; **copy pass applied** |
| 6 | Store assets | `marketing-screenshots`; metadata (description/keywords/privacy answers); **`humanizer` on all store copy before it is written to `metadata/`** | Screenshots at current sizes in `fastlane/screenshots`; `metadata/` complete; **copy run through `humanizer`** |
| 7 | Release review page | Artifact tool (load `artifact-design` first) | Private HTML review page published + link sent; **user approved it** (or waived in Phase 0) |
| 8 | Release | `appstore-release` (read it BEFORE touching versions) | All five lane success markers, ending "Successfully submitted the app for review!" (or upload-only if chosen) |
| 9 | Review outcome | — | Approved → tag repo, close `SHIP.md`. Rejected → map every item to a fix, loop to the phase that owns it |

## Copy rule (applies to every phase that produces text)

**All text a user will ever read goes through the `humanizer` skill before it
ships.** That means in-app strings (buttons, labels, empty states, errors,
onboarding), the App Store description, subtitle, keywords, promotional text and
release notes, and the copy on the Phase-7 review page.

- Load `humanizer` and follow it; do not improvise a de-slopping pass.
- Run it as a **sweep over all strings at once**, not per-string as you type —
  the tells (uniform cadence, rule-of-three padding, repeated hype verbs) show up
  in the aggregate and are invisible line by line.
- The pass is a rewrite of **tone, never of facts**: it may not add a feature,
  number, or claim the original didn't make.
- Copy on brand-carrying surfaces (onboarding, App Store description, taglines)
  is a product decision — apply the rewrite but surface the before/after in the
  Phase-7 review page so the user can veto it.

## Pre-upload checklist (paid-for lessons — run BEFORE the first upload, every app)

- **Purpose strings for every linked SDK**, not just APIs you call: `strings`/grep the SDK binaries for `NSCamera`/`NSMicrophone`/`NSPhotoLibrary` etc. A voice SDK (LiveKit/ElevenLabs) pulls in camera APIs → ITMS-90683 processing kill.
- **PrivacyInfo.xcprivacy** for app + every extension (required-reason APIs: UserDefaults CA92.1, FileTimestamp C617.1) — missing ones cause SILENT processing kills (upload accepted, build never appears; the reason arrives only by email).
- `ITSAppUsesNonExemptEncryption: false`, orientations incl. `~ipad` (iPad-multitasking rejection), version bound to `$(MARKETING_VERSION)`/`$(CURRENT_PROJECT_VERSION)` in generated Info.plists.
- **Every sign-in provider, first run, fresh account, real device, iPhone + iPad** (2.1(a), a real rejection). Apple tests Apple/Google with a brand-new account; a first-time social user must land on onboarding, not an error. Headless proxy: orphan auth user via raw `/auth/v1/signup` → live smoke → profile row exists → delete. Full checklist in `appstore-release` Preflight 4c.
- **Blueprint ports: diff the backend, not just the code.** Triggers on `auth.users`, profile columns, RLS. one app had a profile trigger and a `subscription_tier` column; its port had neither — identical Swift, two rejections' worth of difference.
- **Demo account has durable full access and was signed into today.** Trials lapse between upload and review (real case: trial ended 2 days before the reviewer signed in). Review notes must describe the build being submitted.

## Release review page (Phase 7)

Before ANY upload or submit, publish one private HTML page (Artifact tool; load `artifact-design` before writing it) the user can open anywhere and skim in two minutes:

- App icon + name + version/build at the top
- The store screenshots exactly as they'll ship
- A screen-by-screen **flow walkthrough** of the real app: simulator captures in user-journey order with a one-line caption each
- Release notes + store metadata copy, verbatim

Embed images as data URIs (the artifact CSP blocks remote assets) and downscale/compress them (`sips`) to stay under the 16MB page cap. Send the link, then STOP until the user approves — unless they waived this gate in Phase 0. Their feedback items loop to the owning phase like any other finding; republish the page to the same URL after fixes.

## Loop semantics

- **Build loop:** red test → fix implementation → rerun. Never weaken the test.
- **Audit loop:** audit → fix HIGH+MEDIUM → re-audit. Exit only on zero HIGH.
- **Processing-rejection loop (post-upload email):** read the ITMS code, fix, **bump build number**, re-run the lane. A build Apple killed never appears in the build list — kill any lane stuck "waiting for the build to show up".
- **Review-rejection loop:** get the reviewer's **verbatim text and screenshots from the user first** — Apple's API cannot read Resolution Center, and a diagnosis without it fixes the wrong thing (real case: an entitlement bug was fixed and shipped as build 4 before the actual 2.1(a) cause was known). Then: quote it in `SHIP.md`, check `auth.users`/auth logs for what the reviewer's session actually did, map each item to its owning phase, fix, re-run that phase's gate, **live-verify the exact reviewer scenario**, attach the new build, and resubmit by `PATCH submitted: true` on the *original* `reviewSubmission` (a new one 409s). Reply draft goes to `AppStore/resolution-center-reply.txt` (humanizer pass) — the user pastes it; the API can't.

## SHIP.md (state file, repo root)

Phase checklist with gate evidence per row, the Phase-0 answers, rejection history, next action. Update it in the same commit as the work. On any new session: read `SHIP.md` first, resume at the first unpassed gate.

## Red flags — all mean "loop again", not "ship anyway"

| Rationalization | Reality |
|---|---|
| "UI looks fine, skip the audit" | Every audit of a 'fine' UI has found HIGH issues. Run it. |
| "Suite is green, skip verify-app" | Green ≠ verified; the matrix exists because two bugs shipped past green suites. |
| "Ask the user at each phase to be safe" | Phase 0 collected the authorizations. Re-asking breaks the contract of this skill. |
| "Submit now, add purpose strings if rejected" | Each processing kill costs a build number and ~30 min. Run the pre-upload checklist. |
| "Rejection = report to user and stop" | Rejections are loop input. Fix, bump, resubmit; report while doing so. |
| "Same code as the approved sibling app, so it's fine" | Same code on a different Supabase project failed review twice over (no profile trigger, no tier column). Diff the backend. |
| "Social sign-in is covered by the VM tests" | Those tests never reach production. The reviewer's first-run account will. Device tap or orphan-account smoke, every build that ships a provider. |
| "Skip SHIP.md, I'll remember" | Sessions end. The pipeline outlives your context window. |
| "The copy reads fine, skip `humanizer`" | Every sweep of 'fine' copy finds strings that read machine-written. The tells live in the aggregate rhythm, not in any one line. |
