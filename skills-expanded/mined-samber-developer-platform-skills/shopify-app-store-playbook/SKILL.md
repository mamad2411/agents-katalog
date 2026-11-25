---
name: shopify-app-store-playbook
description: >-
  Gets a B2B SaaS vendor's Shopify app approved, ranked and kept on the Shopify App Store -
  locked public vs custom distribution, Shopify billing for an already-billing SaaS,
  protected customer data, submission packet, review rounds and Paused cooldowns, Built for
  Shopify, ranking, review requests, quality checks. Use whenever a vendor mentions a Shopify
  app listing or review, a paused Shopify submission, Built for Shopify, Billing API vs App
  Pricing for a connector, or ranking on apps.shopify.com. Do NOT use for generic listing
  copy (use samber/developer-platform-skills@integration-listing-optimization), your own
  marketplace's review (use samber/developer-platform-skills@app-marketplace-review), a
  custom app for one client store, Theme Store themes, merchant setup, or app code.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Shopify App Store playbook

You take a vendor's Shopify app through App Store review and keep it ranked and listed. A SaaS company usually fails here on three things: it keeps billing Shopify merchants on its own Stripe, it picks a distribution method it cannot undo, and it plans a launch on a review queue that takes weeks per round. Mark figures from shopify.dev with `†` (Shopify changes requirements without notice and expects listed apps to meet new ones); mark forum and practitioner figures "reported".

## Rules the review enforces

1. Charge for anything the Shopify integration delivers through Shopify App Pricing or the Billing API. A Shopify staff forum post applies this to existing customers and limited-visibility apps too, and to the Shopify portion of a bundled plan; charges for non-Shopify integrations stay on your billing. Merchants must change plans without contacting support or reinstalling.
2. Choose public vs custom distribution once: Shopify never lets you switch. Custom apps serve one store or one Plus organization, skip review, cannot use Shopify billing, and never list. Keep a separate development app so the lock lands on the production app.
3. Install only from Shopify surfaces: authenticate before any UI on install and reinstall (Shopify-managed install with token exchange for embedded apps), then land in the app. Never ask for a shop domain or send merchants to sign up on your site first.
4. Build on the latest App Bridge with session tokens (works in incognito) and expiring offline access tokens†, required for every public app. New public apps also use the GraphQL Admin API only.
5. Request protected customer data before submitting: reading orders or customers is Level 1 and needs review; name, address, phone and email add Level 2 with data-protection reviews. Shopify refuses requests while the app is in review, and unapproved fields come back redacted.
6. Ask for reviews in neutral words only, never with incentives, gated features, or happy-user filtering. Shopify removes reviews and demotes or delists apps for it†.

| Rationalization                                                  | Why it fails                                                                                                                                                              |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "It's a free connector; customers pay our SaaS."                 | Shopify staff rejected exactly this (reported): a free connector into your paid service is in scope.                                                                      |
| "Existing customers keep their Stripe plan."                     | Earlier staff replies said yes; the latest staff clarification says no (reported). Get Partner Support's answer in writing before rebuilding or before relying on either. |
| "Limited visibility, invite-only, so billing rules don't apply." | Limited visibility still installs from an App Store URL: same review, same billing rule.                                                                                  |
| "Pilot as a custom app, make it public later."                   | The method is locked. A custom pilot means a second app, a second review, and reinstalling every pilot merchant.                                                          |
| "We'll ask for an exemption."                                    | Exemptions are rare (reported). Ask Partner Support before building, restate the answer in review notes; disputing a refusal is a cooldown trigger.                       |
| "Our SSO test account will do."                                  | Reviewers need credentials exempt from 2FA, OTP and SSO that keep working after publish. A missing login pauses the submission.                                           |

## Interview

Ask one question at a time; skip what the request already answers. When you cannot ask, state one assumption per gap.

1. What does the app do in Shopify, and does it need a paid account on your SaaS to deliver value?
2. How do customers pay you today, and what share of new customers would arrive from Shopify?
3. Stage: building, submitted, paused or returned, listed, or applying for Built for Shopify?
4. Launch date, and when the first real merchant must run it.
5. Which data does it read (orders, customer name, email, address), and does it touch the storefront or checkout?
6. Effort ceiling: engineer-weeks for embedded UI and Shopify billing, and who answers review emails within days.

Re-rank the distribution menu against answers 2, 4 and 6, and say which answer moved it.

## Route by stage

- **Building** → Distribution menu, Billing decision, Submission, Timeline.
- **Submitted, paused or returned** → Timeline and returned reviews.
- **Listed** → Ranking and reviews, Built for Shopify, Keep the listing.
- **Listing copy and media beyond Shopify's rules** → samber/developer-platform-skills@integration-listing-optimization.

## Distribution menu

- effort, lowest first: limited visibility then full == fully visible at approval > custom app per enterprise store (one app per customer, plus the later public app)
- time to first real-store install: custom app (days) > public app (after approval, weeks per round)
- reach: fully visible > limited visibility > custom

Default rung: a public app with limited visibility for the pilot, flipped to fully visible after launch. One review, installable from its App Store URL, hidden from search; switch any time.

- Go **fully visible at approval** when answer 4 wants App Store discovery on launch day.
- **Custom app** (starved: wins only on speed): promote when a real merchant must run it before approval can land, or one Plus organization funds the integration and refuses Shopify billing. Price in the second app, second review and reinstalls.
- When the request keeps every Shopify charge off Shopify, open with the verdict "closed to the App Store as planned", then plan the compliant version under a stated assumption. Delete the public rungs only once the vendor confirms it will not move that line.

## Billing decision

1. Price the Shopify integration as its own line: what does a merchant arriving from Shopify pay for it? Shopify publishes no formula for splitting a bundled plan: set the line yourself and explain it in the review notes.
2. Make the Stripe path unreachable from a Shopify install: a merchant with no SaaS account never sees your checkout, and a detected existing account pays the Shopify portion as Partner Support confirmed in writing. Reviewers fail apps where they can reach it (reported).
3. Default to Shopify App Pricing for a new app: plans in the Partner Dashboard, Shopify-hosted plan page, trials and proration handled. Once opted in, you cannot create new recurring Billing API charges†, and only apps without active paid merchants can opt in†. Choose manual pricing (Billing API) for the whole app instead when you need local-currency prices or usage caps†, or one-time charges†, which App Pricing lacks; decide before opting in.
4. Keep pricing only in the Pricing details section (requirement 4.2†): no prices in images, no "billed separately", no links to your pricing page. A suspension over "billed separately" wording was reported.
5. Budget fees:
   - Registration: once, $19†, needs a Manage financials role.
   - Revenue share: 0% on the first $1M† lifetime gross app revenue earned since 2025, counted across associated developer accounts, then 15%.
   - Revenue share past the threshold: 15% on everything after a $20M† App Store year or at $100M† company revenue.
   - Processing: 2.9%† plus tax, plus a regulatory fee in some countries.

## Submission

Assemble the packet from [references/submission-packet.md](references/submission-packet.md): configuration, listing fields, test access, screencast, protected data, embedded-app checks.

- Name: lead with your brand, add the category term within 30 characters†, never start with Shopify or another platform you integrate with; keep "Shopify" out of app URLs and the API contact email.
- Keep the TOML app name and the listing name similar; Shopify checks both.
- Run Shopify's AI self-review, then install from scratch on a development store, uninstall, reinstall, change plans.

## Timeline and returned reviews

Statuses: Draft > Submitted > Paused or Reviewed > Published; Withdraw is available at any time. Shopify publishes no SLA.

- Plan 2-3 rounds and 6-14 weeks to Published (reported; staff quoted about 30 days per review on the forum). Every resubmission slows review†; staff say resubmitting while queued sends you to the back.
- When approval cannot land before launch, announce the integration as coming to the Shopify App Store and onboard pilots on development stores.
- Read the Paused banner before planning:
  - **No date**: core requirements blocked testing. Fix every flagged item, mark each resolved (the dashboard blocks resubmission until then), then click Submit fixes.
  - **A date**: cooldown. You resubmit on that date. Triggers: issues unfixed after two exchanges, growing issue counts, silence, disputing an exemption refusal. Reported cooldowns run 2 weeks to a month and lengthen on repeats; only that app is affected.
- Reviewed: answer the reviewer's email; billing fixes need no resubmission†.
- Fix every flagged requirement in one pass and answer misreads in that requirement's notes. A reviewer stops at a blocking failure, so retest the whole path.

## Ranking and reviews

- **Shopify-published**: Built for Shopify and the "increased visibility" achievement boost search†; keyword-stuffed subtitles, stats, "best" claims and testimonials in the listing are banned†.
- **Reported**: exact phrase in the app title outweighs review count early; merchant engagement, uninstall rate and install velocity count. Say "reported" whenever you cite one.
- Request reviews only through App Bridge's Reviews API (`shopify.reviews.request()`), after a real milestone such as a first successful sync. It shows at most once per 60 days and 3 times a year†, never on mobile: never wire it to a button.
- Reply publicly to reviews, negative ones first.
- Store Ads (CPC, search, category, homepage) buy traffic; relevance lowers the price. Use them for launch weeks, never as a ranking strategy.

## Built for Shopify

Apply only when the Partner Dashboard Distribution page shows the prerequisites passing: 50 net installs from active paid-plan shops†, 5 reviews†, an unpublished rating floor, admin Web Vitals at p75 (LCP 2.5 s, CLS 0.1, INP 200 ms†, 100 calls in 28 days).

- SaaS connector blockers: an app home that is your existing web app shown unchanged, primary workflows or connection settings left on your site, a separate sign-up. Exception for contract-based B2B: onboarding first asks merchants to connect existing credentials, and offers Shopify-credential sign-up when you also sell self-serve.
- Category rules: ads, analytics, email, SMS and affiliate apps use Web Pixel extensions, never script tags; email, SMS and forms apps also sync customers both ways and accept Shopify segments†.
- Failing one criterion three times in a row suspends the application for three months†. Status lapses after 60 days† of failing automated criteria; annual reviews give 60 days to fix.

## Keep the listing

- Answer a quality-check email within 7 days† (silence demotes the app) and ship required changes within 30 days† (or face unpublishing).
- Migrate to expiring offline tokens before 2027-01-01†: non-compliant apps then lose their listing and new installs, and their old tokens get 403 errors from 2027-04-01†.
- Keep a support email on file and answer merchants yourself: Shopify does not support third-party apps.

## Output

Key the answer on the route; a single question gets a direct answer plus the sections it touches. Keep the `†` and "reported" labels in the answer, with a one-line legend.

- **Building**: assumptions; distribution rung with its reason; billing plan (what moves to Shopify billing, what stays, how the Stripe path stays unreachable); protected-data request; packet checklist with an owner each; dated timeline with two returned rounds.
- **Paused or returned**: banner type (no date or cooldown), one fix per flagged requirement, the notes to write, the resubmission date.
- **Listed**: ranking actions labelled published vs reported, review-request trigger, Built for Shopify gap list, deadlines at risk.

## References

- samber/developer-platform-skills@integration-listing-optimization - listing copy, media order, conversion.
- samber/developer-platform-skills@integration-partnership-strategy - whether Shopify earns an integration at all, before this playbook runs.
