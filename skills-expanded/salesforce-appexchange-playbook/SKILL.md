---
name: salesforce-appexchange-playbook
description: >-
  Takes a B2B SaaS product onto Salesforce AppExchange (increasingly AgentExchange) as
  an ISV - partner entry, listing type, managed 2GP choices that can never be undone, security
  review prep and resubmission, PADA, Checkout, GTM app or Channel Order App pricing, LMA
  licensing, re-reviews, push upgrades, OAuth mandates. Use whenever a vendor mentions
  AppExchange, AgentExchange, the Salesforce security review, a managed package it distributes,
  the Salesforce ISV program or PNR revenue share. Vendor side only. Do NOT use for listing copy,
  search rank or reviews (use samber/developer-platform-skills@integration-listing-optimization),
  for reviewing apps on your own marketplace (use
  samber/developer-platform-skills@app-marketplace-review), or for Apex/LWC code, internal-org
  packages or consulting listings.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Salesforce AppExchange playbook

You take a SaaS product onto AppExchange, whose newer pages say AgentExchange: a reviewed partner, a package or API integration, a security gate, and a revenue share. The expensive mistakes happen before the listing exists.

## Commitments you cannot undo

- **Listing type** (Packaged Solution, API, Consultant) is fixed at creation; moving from API to a package later means a new listing.
- **Namespace** is fixed to a 2GP package at creation and prefixes every component API name (`acme__Invoice__c`).
- **Promotion** to managed-released never reverses; only one beta per minor version can be promoted.
- **Beta installs** run only in scratch orgs and sandboxes and never upgrade. Pilot customers need a released version behind an installation key.
- **Global Apex** classes and global Visualforce components can never be removed. Most other released components can only be deprecated, after a Partner Support case enables removal. Mark internal-only custom settings, metadata types, labels and permissions protected: once released unprotected, they stay.
- **OAuth controls** on a Connected App or External Client App (ECA), once enabled, cannot be turned off. See [references/security-review-prep.md](references/security-review-prep.md) before switching them on.

| Rationalization                                                   | Why it fails                                                                                                                                                         |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "We'll pick a better namespace later."                            | It renames every API name customers and integrations reference. Pick the product brand once.                                                                         |
| "Make every service `global` so SIs and our add-ons can call it." | Global is permanent. Share code between your own packages in one namespace with `@namespaceAccessible`; expose only a small, versioned global facade to subscribers. |
| "Give the pilot the beta, we'll upgrade them."                    | Betas never reach production and cannot upgrade.                                                                                                                     |
| "We only call the Salesforce API, so no review."                  | API solutions pass the same review; your web app and APIs are tested with DAST.                                                                                      |
| "Ship the fix and the new feature in one resubmission."           | Any change beyond the flagged issues forces a full initial review and a new fee.                                                                                     |

## Interview

Ask one question at a time; skip what the request answers. When you cannot ask, state an assumption per gap and flag it:

1. What must run inside the customer's org: nothing (your SaaS calls Salesforce APIs), objects and UI, automation, Agentforce actions? Which editions do buyers run (Professional and Group reach the API only through a reviewed managed package with an API token)?
2. Stage: not a partner, registered, building, in review, returned or failed, listed?
3. Pricing: free, freemium, per seat, per org, usage-based, multi-year enterprise? Company country, customer countries?
4. Which endpoints authenticate users or move Salesforce data? Any Connected App today, in how many customer production orgs?
5. Target date for a first paid install, engineering weeks, security skills in-house.

Re-rank the menus below against answers 1, 3 and 5, and say which answer moved which option. When the date cannot be met by any path, count forward from today, give the realistic date, and name what fits the original one.

## Route by stage

- **Not a partner** → Decide, then apply at the Partner Community; a Partner Business Org (PBO) with LMA, COA and Dev Hub follows acceptance. Negotiate the PADA with the account manager while you build; listing approval and the signed PADA both precede publishing.
- **Building** → Package, then Security review from the first sprint.
- **In review, returned or failed** → Security review steps 4-7.
- **Listed** → Maintain; listing copy, rank and reviews go to integration-listing-optimization.
- **Whether Salesforce is worth it at all** → samber/developer-platform-skills@integration-partnership-strategy.

## Decide what to list and how to get paid

Packaging and price constrain each other, so decide both here. Default rung: API listing; move up to a managed 2GP package when answer 1 puts anything in the org or answer 3 needs Checkout or the GTM app.

| Path                                  | Fits                                                                                                                                             | Needs                                                                                                                                                                       | Money                                                                                                                            |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| API listing (Salesforce Platform API) | SaaS syncing over OAuth, nothing in the org                                                                                                      | review with DAST of your app and APIs; no Code Analyzer or Checkmarx                                                                                                        | bill outside Salesforce; paid apps report orders through the Channel Order App (COA)                                             |
| Managed 2GP + Checkout                | per seat or per org, one-time or monthly/annual subscription                                                                                     | company in US, UK or EU; not OEM; clickthrough PADA                                                                                                                         | 15% of net revenue + $0.30 per card payment                                                                                      |
| Managed 2GP + GTM app private offers  | seat-based deals with new US customers (Salesforce pages disagree on existing customers buying a new product: confirm with your account manager) | existing ISVforce partner, USD, PADA with GTM terms, by application; 12-month orders, NET30 ACH paid upfront, no auto-renew; COA contracts expand through COA until renewal | share per product in the Partner Product Catalog; net-new orders that qualify must use it                                        |
| Managed 2GP + COA (offline PADA)      | usage, tiers, multi-year or negotiated deals; Freemium; Paid Add-On Required                                                                     | Channel Order App order within one business day of each sale                                                                                                                | PNR set in your PADA, commonly 15% ISVforce (your app sold to Salesforce customers), 25% OEM (bundled with a Salesforce license) |

- A thin managed package carrying only the ECA counts as a managed package: Checkout and LMA licenses become available, Code Analyzer and Checkmarx apply.
- Free solutions pay no review fee and no share; paid ones pay $999 per initial, follow-up or periodic review (the wizard shows the current fee). Pages quoting $2,550 or $2,700 are outdated.
- Switching free ↔ paid, Checkout ↔ non-Checkout or pricing units sends the listing back to approval.
- The 1GP, unlocked and unmanaged packages are never options: review accepts only managed-released versions.
- The ladder starves **no listing**: an API integration sold directly carries no partner agreement or revenue share. Choose it when buyers never shop on AppExchange and no buyer runs Professional or Group edition.

## Package

1. Enable Dev Hub in the PBO; register the namespace in a Developer Edition org and link it.
2. Put packages that call each other in one namespace; give a product you might sell or spin off its own.
3. Keep Apex coverage at 75% or more with every trigger covered; versions built with `--skip-validation` or without `--code-coverage` cannot be promoted.
4. Certify Lightning Ready: mandatory for every new submission.
5. Submit major and minor versions for review. Patches, enabled by Partner Support case after a pass, are for hotfixes only: they cannot add or remove components.

## Security review

Timeline: verification 1-2 weeks, first test 3-4 weeks, each retest 2-4 weeks plus a new fee. Practitioners estimate half of first submissions fail and 4-9 months from signup to first paid install.

Prep ranked by first-pass odds per engineering day: Code Analyzer with CRUD/FLS fixes > sharing and SOQL-injection sweep > DAST of every in-scope endpoint > false-positive write-ups > test org, credentials and docs > office-hours slot. The last two cost hours, and a dead test org stalls verification.

1. Scan from the first sprint, not the week before submission.
2. Enforce CRUD/FLS on every query and DML (`WITH USER_MODE`, `AccessLevel.USER_MODE`), `with sharing` on every class, bind variables in SOQL.
3. Follow the data: any endpoint that authenticates the user or sends or receives Salesforce data is tested. Get written permission before scanning third-party endpoints.
4. Assemble the materials in [references/security-review-prep.md](references/security-review-prep.md), submit in the Partner Console wizard, pay the fee.
5. **Returned** (materials missing): fix and resubmit the same review, no fee; disagree with the feedback through Request a Second Look.
6. **Failed**: each finding is one example of a class; fix every instance across the solution. Change nothing else; keep package ID and namespace (API solutions create a new API solution), rescan, start a follow-up review, fee due. All findings false positives: attach the write-up to the failed review and resubmit, no fee.
7. No appeal exists for a failed test; Product Security office hours are the channel.

## Maintain

1. Build each new version on the last passed version, the highest managed-released one, as ancestor: it lists without a new review. A version cut before its ancestor passed does not; one cut during a re-review lists until that re-review fails.
2. Push upgrades: own test orgs, customer sandboxes for a week, then production in batches (50-100 of 1,000 at first), off-peak, never at customer quarter-end, 3-4 weeks after a major Salesforce release. Never auto-assign a new feature's permission set to existing users.
3. Test each of the three yearly Salesforce releases in preview sandboxes; move API calls off any version announced for retirement.
4. Expect periodic re-reviews, chosen by risk and time since listing, fee due; a failed one gives about 60 days. Keep the security contact on Company Info current: a missed re-review expires every version.
5. Unpaid revenue share or review fees also expire the review and pull the listing; file COA cancellations per the PADA, usually 30+ days before renewal (COA blocks them within 5 days).
6. Ask for reviews at customer success milestones, never for an incentive.

## Output

Key the answer on the route. A single question gets a direct answer plus the rows below it touches. **Not a partner** and **Building** get all of:

1. Assumptions, one line per missing interview answer.
2. Listing and payment path, with the interview answer behind it.
3. Irreversible-choice register: listing type, namespace, global API, protected components, pricing path, OAuth controls; owner and decision date each.
4. Security review plan: in-scope endpoints, scanners, top three risk classes, submission week.
5. Timeline: backward from the target date, or forward when infeasible, one failed review included.
6. Maintenance calendar: releases, re-review, OAuth controls, COA duties.

Mark every Salesforce figure (fees, shares, durations, dates) with `†` and a footnote: verify against current Salesforce partner docs before quoting it.

## References

- samber/developer-platform-skills@integration-listing-optimization - listing copy, media, AppExchange search rank, review velocity.
- samber/developer-platform-skills@oauth2-provider-design - OAuth behaviour your ECA and external app depend on.
- samber/developer-platform-skills@api-versioning-policy - deprecating your own API without stranding package users.
- samber/developer-platform-skills@app-marketplace-monetization-model - the operator view of the billing rails you plug into.
