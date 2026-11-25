---
name: store-listing
description: Write or audit an app's store listing for the App Store and Google Play. Produces localized metadata (Italian and English first), keyword allocation, descriptions, a screenshot plan with captions, and user-facing release notes converted from a developer changelog, all lint-checked against store limits and policy. Use when the user asks for ASO, App Store Connect or Play Console text, app name, subtitle, keywords, short or full description, promotional text, screenshot captions, "What's New" or release notes, listing localization, keyword research, listing experiments, or to review an existing store listing before submission.
---

# Store Listing

Turn product truth into a listing that ranks for the right searches, converts, and passes review. Every claim traces to **evidence**; every field passes a **lint**.

Output: `listing.md` in the canonical format (`assets/listing-template.md`), plus the artifacts below. Audit mode returns `assets/audit-report-template.md`.

## Ground rules

1. **Claims need evidence.** Each factual statement maps to a row of the claims ledger (`assets/claims-ledger-template.md`). No row → delete the claim or mark ❓.
2. **No invented ASO data.** Volumes, difficulty, rank and uplift come from the user's tools. Without them, volume is *unknown* and ranking is by relevance and specificity. Never predict downloads.
3. **Lint before delivery.** Run `python3 scripts/lint-listing.py <listing.md> --banned "<project banned terms>"`; deliver only lint-clean text, or list the remaining warnings.
4. **Respect confidence tags.** `V` = read from the official page on 2026-11-05; `V*` = summarised; `T` = practice. Re-open the source (`references/00-method.md` §5) before a 🔴 on a `V*`/`T` row.
5. **Native per locale.** Write Italian and English from the audience's search phrases, not by translating.
6. **Read-only.** Deliver files and paste-ready text; never submit or edit a console.

## Workflow

Single-piece requests ("write the release notes") run Step 1, the relevant step, and Step 8.

### Step 1 — Frame

Record: mode (Create | Audit), stores, locales, product positioning sentence, audience, tone, category, **project banned terms** and required phrases, existing listing and constraints, ASO data available (Search Ads, Analytics, Play search terms, tools). Ask unknowns in one batch.

**Done when** all items are written down or listed as open questions, and banned/required terms are in a list the linter can read.

### Step 2 — Product truth and claims ledger

Read README, product docs, store/compliance notes and the shipped code paths. Fill the claims ledger with every claim you intend to make, and the claims that must never be made.

Cross-check claims about matching/ranking, data handling, safety and age against the privacy policy, Terms and store labels: the listing must not say less than the policy discloses nor contradict it.

**Done when** each planned claim has an evidence class and path (or ❓ with the owner who confirms it), policy-sensitive claims are cross-checked, and the never-claim list exists.

### Step 3 — Keyword research

Read `references/02-keyword-research.md`. Build candidates per locale from the ledger, the users' words and supplied data; score with the worksheet (`assets/keyword-worksheet.md`).

**Done when** every locale has ranked candidates, each tagged with relevance and a volume source or `unknown`.

### Step 4 — Field allocation

Allocate terms to fields using `references/01-field-specs.md` (limits, what each store indexes) and `02-keyword-research.md` §5–6.

**Done when** each locale has a field map within limits, with zero repeated words across Apple name, subtitle and keywords.

### Step 5 — Copy

Read `references/03-copywriting.md`, `06-localization-it-en.md` and `08-compliance-guardrails.md`. Write all text fields per store and locale into `listing.md`.

**Done when** the lint reports no errors, and every sentence maps to a ledger row.

### Step 6 — Screenshots and graphics plan

Read `references/04-screenshots-previews.md`. Fill `assets/screenshot-plan-template.md`: one message per frame, captions per locale, demo-data source, sizes per store, "never show" list.

If an asset pack already exists, verify dimensions, alpha, durations and locales with the commands in `04-screenshots-previews.md` §5b instead of trusting its README.

**Done when** frames 1–3 are understandable alone, every frame has a ledger id, required sizes for both stores are listed, and existing assets are verified or marked ❓.

### Step 7 — Release notes

Read `references/05-release-notes.md`. Choose the range, run `scripts/changelog-to-notes.py`, filter by user visibility, write notes per locale and store.

**Done when** every bullet matches a shipped change, limits hold (Apple 4000, Play 500 per language), and the source (changelog or git) and its freshness are stated.

### Step 8 — Lint and report

Run the linter, resolve errors, review warnings, run the cross-checks in `08-compliance-guardrails.md` §4 (billing, privacy label, age rating, moderation promises), then fill the report.

**Done when** lint shows 0 errors, every warning is fixed or justified in the report, and the report names the data it lacks (ASO data, console facts).

## Reference navigation

| File | Use |
|---|---|
| `00-method.md` | Modes, verdicts, evidence, freshness URLs |
| `01-field-specs.md` | Limits, indexing, graphics specs, variants (both stores) |
| `02-keyword-research.md` | Research, scoring, field allocation |
| `03-copywriting.md` | Field recipes, skeleton, trust, style |
| `04-screenshots-previews.md` | Plan, frameworks, specs, capture pipeline |
| `05-release-notes.md` | Changelog → notes, limits, templates, wiring |
| `06-localization-it-en.md` | Italian/English strategy, codes, quality checks |
| `07-experiments.md` | PPO, custom pages, Play experiments |
| `08-compliance-guardrails.md` | Apple 2.3 and Play Metadata rules for writers |

Hand-offs: compliance audit of the whole app → `store-review-preflight`; privacy label and Data safety consistency → `privacy-audit`.
