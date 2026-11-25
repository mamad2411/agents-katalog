---
name: github-marketplace-playbook
description: >-
  Gets a vendor's GitHub App or GitHub Action listed on GitHub Marketplace and, for apps,
  selling there - free vs paid listing, publisher verification, marketplace_purchase
  billing duties, immutable pricing plans, enterprise buyers Marketplace cannot bill, the
  verified creator badge, delisting. Use whenever a vendor mentions GitHub Marketplace,
  listing a GitHub App, Marketplace paid plans, or selling through GitHub billing.
  Publisher side only; not for buying or allowlisting Marketplace apps as a customer. Do NOT
  use for building the action (use samber/developer-platform-skills@github-action-offering),
  repository growth (use samber/developer-platform-skills@github-engagement-playbook), or
  launch announcements (use samber/developer-platform-skills@app-marketplace-launch-marketing).
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# GitHub Marketplace playbook

You take a vendor's GitHub App or GitHub Action onto GitHub Marketplace and keep it there. Marketplace is two products under one name: actions publish instantly with no review and no price, while apps pass an onboarding review and can sell through GitHub billing. Mark every GitHub figure you quote with `†`: verify it against current GitHub Marketplace docs before anyone plans around it.

## Rules the platform enforces

1. Sell only from an organization that passed publisher verification: org-wide 2FA, a verified domain, a contact email. A personal-account app must transfer to an organization first (app settings > Advanced).
2. Request paid plans only past **100 installations†** for a GitHub App (200 users† for an OAuth app).
3. Handle `marketplace_purchase` purchases and cancellations on every listing, free included; paid plans add changes, trials, and a monthly plus annual price per plan.
4. Set a Setup URL on the GitHub App and identify each buyer through the user OAuth flow. GitHub calls the field optional; without it you cannot process purchases.
5. Keep the app public and generally available (no preview, no invite-only), and never steer users away from GitHub in the listing.
6. Never test purchases on the live listing. Use a second, public development app with a draft listing: plans published inside the draft can be bought as free simulations, plans saved as draft cannot.
7. Treat a published price as permanent: you can only retire a plan, buyers keep it at its price until they move, and GitHub cannot move them. Test prices in the draft listing or direct deals first.

| Rationalization                                     | Why it fails                                                                                                                                                                                                                                |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "We'll charge for the action on Marketplace."       | Actions carry no pricing. Sell the product the action calls.                                                                                                                                                                                |
| "Enterprise customers can buy us through GitHub."   | Invoiced enterprises cannot buy paid apps; in any enterprise, only an enterprise owner who is also an org owner buys, through the enterprise account. Keep a direct contract path.                                                          |
| "List free now, keep selling on our site."          | One GitHub note bans a free plan for a product sold elsewhere; another tolerates it until the paid gates are met. Large vendors list free-only and no enforcement is documented, but a new submission carries the risk: plan the paid plan. |
| "$29 per repository, as a per-unit plan."           | Docs describe per-unit as per user, yet the unit label is free text: live listings sell "x10 repositories" units with a quantity selector. Confirm the label with the onboarding expert; flat tiers are the fallback.                       |
| "Verified org badge, so we're verified everywhere." | Three different marks: org domain badge, app publisher badge, actions verified creator badge. Only the last passes "verified creators" Actions policies.                                                                                    |
| "Webhooks are enough to track subscriptions."       | GitHub never redelivers a failed delivery on its own. Sync periodically against the plan's account list.                                                                                                                                    |
| "Approval in two weeks."                            | GitHub publishes no review time; vendors report 3 weeks to over 2 months, and financial onboarding for a paid plan has stalled 10 more weeks.                                                                                               |

## Interview

Ask one question at a time; when you cannot ask, state one assumption per gap.

1. Action, GitHub App, OAuth app, or several? Owned by a personal account or an organization?
2. Installation count; how buyers pay (card, invoice, enterprise accounts); any Actions or app restrictions on their side.
3. Is the product sold outside Marketplace? Which plans and units?
4. Launch date, and whether an event is pinned to it.
5. Who builds and owns billing-event handling, and how many engineer-weeks are available?

Re-rank the listing menu against answers 2, 4 and 5, and say which answer moved it. Enterprise buyers (2) add a direct contract path and the action allowlist plan beside any rung.

## Route by stage

- **Action** → Action listings; contract, release, hardening → samber/developer-platform-skills@github-action-offering.
- **App, deciding** → Listing menu, then App gates. **Building** → App gates, Billing duties.
- **Submitted, no answer** → Review and timeline. **Listed or shutting down** → Changes after listing.
- **Copilot Extension listing** → GitHub App-based Copilot Extensions ended 2025-11-10† with their category; build an MCP server (samber/developer-platform-skills@mcp-server-offering). VS Code Copilot extensions → samber/developer-platform-skills@ide-extension-offering.

## Listing menu (GitHub Apps)

Ranked by efficiency, highest first: unlisted public app installed from your own site > free Marketplace listing > paid Marketplace plans.

- **Unlisted public app**: near-zero effort, no review, no fee; found only through your docs.
- **Free listing**: purchase and cancellation handling, the Setup URL flow, 30-day† data deletion, assets and an onboarding review; adds Marketplace search.
- **Paid plans** (starved: high value, high effort): verification, full billing flows, financial onboarding, a 5%† fee, payout at the end of the following month once a month reaches $500†, first payout up to 90 days† after registration. Promote when card-paying teams already self-serve past 100 installs†.
- Default: unlisted while answer 5 has no billing capacity; free listing once it does; paid when answer 2 shows card self-serve volume. Adding paid plans to a live free listing triggers verification and financial onboarding again: budget a second review.

## Action listings

- Publish from a public repository with one root `action.yml`; the owner accepts the Developer Agreement, the publisher uses 2FA. Instant, unreviewed.
- Pick the `name` once: no clash with another action, a GitHub account you do not own, a category or a GitHub feature. Archive a retired action's repository: deleting it frees the name for anyone.
- Plan for customer allowlists by default: admins add `owner/repo@*` or a full commit SHA, never a tag, which locked workflows do not match. The verified creator badge needs acceptance into GitHub's Technology Partner Program (established company, commercially available product, an NDA), then an email to partnerships@github.com; no timeline is published.
- A repository transfer keeps the listing and redirect but drops the badge unless the new owner is a verified creator.
- Delist by unchecking "Publish this Action to the GitHub Marketplace" on every published release.

## App gates

1. Make the app installable by any account; draft listings exist only for public apps.
2. Have an organization owner create the listing: the GitHub App manager role cannot.
3. Prove integration beyond sign-in: GitHub rejects apps that only authenticate.
4. Fill support and privacy URLs and named contact emails, which GitHub uses for payouts.
5. For paid plans, request publisher verification before submitting; an approved unverified app shows "App meets the requirements for listing" and cannot change pricing.
6. Write listing copy to GitHub's field rules in [references/listing-fields-and-events.md](references/listing-fields-and-events.md).

## Billing duties

Build these before submitting; the onboarding expert tests them. Event table and test setup in [references/listing-fields-and-events.md](references/listing-fields-and-events.md).

- Upgrades apply at once with proration; downgrades and paid cancellations arrive at the next cycle. Read `effective_date`, never the delivery time.
- Trials last 14 days†, one per buyer per product; grant paid access during the trial.
- On a cancelled paid plan, drop to your free plan if one exists: GitHub does not uninstall the app. On full cancellation, deactivate, revoke the token, delete customer data within 30 days†.
- Show plan, seats, trial days left and billing cycle in your app; link upgrades through the upgrade URL.
- Reconcile two entitlement sources per account, Marketplace and direct contracts; report double purchases to GitHub Support.

## Review and timeline

- Submit with "Request publish"; an onboarding expert replies by email. No published duration.
- Plan backward from launch: eight weeks for a free listing, two to four months for paid plans, since financial onboarding comes after review. When approval cannot land in time, launch the unlisted app with your own Install button, announce it as "coming to GitHub Marketplace", and list on approval.
- After four weeks of silence, open a GitHub Support ticket with app name, app ID, owner and submission date; the form has no Marketplace category, so file under Billing or Account. If a bot closes it, reply to the closure email to reach a human. Never click "Withdraw request": practitioners report it resets your place.

## Changes after listing

- Edit description and images freely; price changes follow rule 7, plus a migration message to buyers on the old plan.
- Removing a listing: give 30 days'† written notice under the Developer Agreement (legal-support@github.com), then "Delist this Listing". Subscriptions run to their cycle end, annual ones up to a year; the app cannot be deleted before then. Choose: serve every buyer to cycle end, or refund pro rata under your own terms, since GitHub refunds nothing.
- Keep support answering: GitHub may cut exposure or delist for poor support, and you should be able to report a confirmed security incident within 24 hours†.

## Output

Key the answer on the route; combine shapes when a request spans routes.

- **Deciding**: assumptions, one per gap; listing rung with its reason; enterprise-buyer path.
- **Building**: gate checklist with owner per item; billing event plan; test plan on the development app; dated timeline with review slack.
- **Listed**: change classified (free edit, retire-and-recreate, delist), buyer message, obligations at risk.

`†` Verify against current GitHub Marketplace documentation; GitHub has changed its fee and categories before.

## References

- samber/developer-platform-skills@integration-listing-optimization - listing copy, media order, conversion.
