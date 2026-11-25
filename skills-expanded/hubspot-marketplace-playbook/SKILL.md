---
name: hubspot-marketplace-playbook
description: >-
  Gets a B2B SaaS vendor's app listed on the HubSpot Marketplace and keeps it there - the
  three-active-install gate, the 25-install cap on unlisted apps, apps HubSpot refuses, scopes and
  the Shared data table, Draft bounces, review timelines, version deadlines, AI connector and MCP rules, App Certification, Technology Partner tiers. Use whenever
  a vendor mentions listing or certifying its app on HubSpot, a listing sent back to Draft, or
  HubSpot technology partner tiers. Do NOT use for listing copy or install conversion (use
  samber/developer-platform-skills@integration-listing-optimization), for running your own
  marketplace (use samber/developer-platform-skills@app-marketplace-review), for CMS themes, for
  admins vetting another vendor's app, or for CRM admin, API code or agency work.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# HubSpot Marketplace playbook

You take a vendor's app onto the HubSpot Marketplace and keep it listed. HubSpot charges no listing fee and takes no revenue share; you bill your customers yourself. The cost is elsewhere: real customers before you may apply, a listing that must match the app's actual scopes, and a platform that ages apps out of eligibility. Mark every HubSpot figure you quote (counts, durations, dates, versions) with `†` and one footnote: verify against current HubSpot developer docs and changelog.

## Rules the review enforces

1. Submit only with **3 active installs†**: unaffiliated production accounts with successful API calls, webhook or app-card requests in the last 30 days. Your own, test and partner-employee portals never count, and OAuth alone is not activity. Practitioners report the counter lags by days.
2. Build the app with `distribution: "marketplace"` and OAuth from the first pilot. It installs in up to **25 accounts† before listing**; private OAuth distribution stops at 10† (100† from a Solutions Partner portal) and switches to marketplace later without breaking installs. A static-token app serves one portal and never lists: rebuild its auth as OAuth with marketplace distribution, and plan for pilots to reinstall.
3. Use every scope you request, required or optional. HubSpot checks your API logs. Mirror every scoped object in the _Shared data_ table; read plus write on an object means you advertise a bi-directional sync.
4. Build on the developer platform (projects) at a supported version†, with date-based OAuth endpoints† and app cards, never classic CRM cards. Legacy (pre-projects) public apps can no longer be created†, are rejected for new listings†, and face delisting at a later enforcement date†. Read the dates in [references/submission-packet.md](references/submission-packet.md) § Deadlines before planning any migration.
5. One app in review at a time; HubSpot rejects the second submission automatically.
6. Never put "HubSpot" or "Hub" in the app's name, logo or app-card names, and write HubSpot with a capital S everywhere.

| Rationalization                                             | Why it fails                                                                                                                                         |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Install it in our sandbox and two staff portals."          | Affiliated and test accounts are excluded. Three customers running a real workflow for a few weeks is the only path.                                 |
| "Request the extra scopes now to avoid reinstalls later."   | Unused scopes reject the listing and fail certification. Mark subset scopes optional or conditionally required instead.                              |
| "Let's get certified for launch."                           | Certification opens only after 6 months listed† and 60 active installs†. A rejection blocks re-applying for 6 months†.                               |
| "Migrate our unlisted legacy app, then list it."            | Migration caps an unlisted app at 25 installs, and legacy apps can no longer list. Contact HubSpot first (Legacy app with installs).                 |
| "Our pricing page has a free trial, so pick the Free plan." | Free is only for free-forever or freemium. List only plans that include the integration, priced exactly as on your website.                          |
| "Offer a gift card for reviews to reach the rating."        | The review guidelines ban compensation of any kind, including discounts and refunds. Use HubSpot's 30-day review email and your review link instead. |

## Interview

Ask one question at a time; skip what the request answers. When you cannot ask, state one assumption per gap and flag it.

1. What does the app do in HubSpot: data sync, app cards, workflow actions, agent tools, an MCP server, an AI assistant acting on CRM data, a browser extension?
2. Stage: building, piloting (how many unaffiliated portals active this month), in review or bounced to Draft, listed (since when, active installs)?
3. Built on the developer platform (which `platformVersion`) or a legacy public app; how many installs; any classic CRM cards?
4. Who is the product for: does it enrich contacts, import prospect lists, identify website visitors, or embed integrations inside other vendors' products?
5. Launch or deadline date, and whether HubSpot's partner tier or co-selling matters this year.

When answer 5 sets a date, compute the timeline before anything else and lead with any goal the gates make impossible by then, with the realistic date. Re-rank the pilot menu against answer 5 and say which answer moved it.

## Route by stage

- **Building or piloting** → Eligibility, Pilot to three installs, Submission.
- **Legacy public app** → Legacy app with installs, then the route for its stage.
- **In review or bounced** → Review and timeline.
- **Listed** → Keep the listing, Certification and tiers.
- **Listing copy, screenshots, search terms, install conversion** → samber/developer-platform-skills@integration-listing-optimization.
- **Whether HubSpot is worth integrating with at all, or which partner program first** → samber/developer-platform-skills@integration-partnership-strategy.

## Eligibility

Refuse to plan a listing for an app HubSpot excludes, and say which rule excludes it. No install count cures an excluded architecture.

- token or credential brokering, developer-only infrastructure, white-label integrations embedded invisibly in another vendor's product: unified-API and embedded-iPaaS vendors' customers list their own branded apps, never the infrastructure;
- importing non-opted-in emails, scraping LinkedIn, bulk-loading prospect databases;
- serving only restricted industries (crypto, NFTs, gambling, pharmaceuticals, dating, list brokering, follower sales); unrelated functionality is judged case by case;
- a second app for the same use case, or a listing that redirects to or needs another app: one app ID and OAuth client per listing, so update the listed app instead.

Expect extra review for contact enrichment, syncing contacts who engaged with the customer's outreach (every synced contact must have engaged), and visitor de-anonymization. A companion browser extension must itself be listed and approved in its browser's store.

AI that reads a request and decides which CRM actions to take must enforce the installing user's permissions: build on HubSpot's MCP auth app, or set `isUserLevel: true` on platform 2026.09† or later, which covers only some features and APIs†. A standard OAuth token fails. A fixed sync that uses AI upstream is exempt. Agent tools and MCP components serve front-office use cases, never EU AI Act high-risk or prohibited ones. An MCP server lists as its own standalone app per the MCP listing requirements†, on a server you own; see the reference § MCP and agent tools.

## Pilot to three installs

Ranked by efficiency, highest first: existing customers already on HubSpot, installing the marketplace-distribution app themselves > design partners recruited for one real workflow > a Solutions Partner (agency) installing in its clients' own portals with consent. Default: start at the first rung this week; a launch inside two months promotes design-partner recruiting to start in parallel.

- Pilot installers see an "unverified app" warning and type "I accept the risk"; only Ecosystem Quality approval (listing) removes it. A verified domain (one per developer account; needed for certification, not listing) adds your domain beside a "not reviewed by HubSpot" banner. Warn pilots beforehand.
- Count only portals with successful calls in the last 30 days; drive one scheduled sync or webhook so activity never lapses. Two design partners never reach the gate: line up a third portal and a spare.
- Agent tools, app cards and user-level access exist only on the developer platform (projects), never on legacy apps.

## Legacy app with installs

An unlisted legacy public app with more than 25 installs is stuck: it cannot list as legacy, and migrating it enforces the 25-install cap. A listed legacy app migrates without that cap; schedule it before the enforcement date.

For the unlisted case:

1. Open a support request or write to the technology partner team before running `hs app migrate`. Your Technology Partner Manager, if you have one, sits under App Listings > More > View listing details.
2. Cite the install count and ask three questions: what happens to existing installs above 25, whether new installs error, and whether a cap exception exists.
3. Migrate only once you hold a written answer.

## Submission

Assemble the packet from [references/submission-packet.md](references/submission-packet.md). Wrong or missing listing fields send the listing back to Draft; a missed minimum requirement rejects it.

1. Allowlist the "HubSpot Crawler" user agent: HubSpot crawls every listing URL, and a blocked page bounces the listing.
2. Publish a HubSpot-specific setup guide, public, not behind login, not your docs homepage.
3. Choose the install experience: Seamless install (inside HubSpot, recommended), Login via partner site, or No install button. Seamless needs an endpoint HubSpot can frame that redirects to `returnUrl`, or installs loop.
4. Replace testing credentials with a demo video or guided walkthrough of install, configuration and permission use†.
5. Submit as a Super Admin of the developer account.

## Review and timeline

- Initial review within 10 business days†; HubSpot says the feedback loop "should take" no more than 60 days† from feedback shared. Practitioners report silent weeks after resubmitting: reply to the review email to chase.
- Fix every feedback point in one pass, keep scopes and the setup guide frozen during review, and ship other app updates freely.
- App cards and agent tools go through their own reviews† before the listing or deploy; a listing resubmitted before app-card approval is rejected.
- Plan backward from the launch date with one Draft bounce, counted as another 10-business-day review†. When approval cannot land in time, announce the integration as coming, and keep pilots under the 25-install cap.

## Keep the listing

- Stay above 3 installs: the partner agreement lets HubSpot terminate below that 90 days† after publication, and an app not installed in 180 days† is removed.
- Every listing edit returns to review; unpublishing takes up to 10 business days†. Leaving the program obliges one year† of customer support.
- Budget one platform-version migration a year: versions ship every March and September, and § Deadlines lists the dates that cost certification or the listing.
- Reply to every negative review (two replies† per review); certification checks it. Customize the review request emails HubSpot sends from day 30, with no incentive language, and send your review link to customers eligible under the review guidelines, never trial users or partners and never filtered by sentiment. Stars show from 10 reviews†.

## Certification and tiers

Certification buys a badge, a search filter and curated-collection eligibility, and no go-to-market motion by itself. Ranked by efficiency once listed: review flow and influenced-revenue submissions (tiers count both) > certification > co-marketing programs. Promote certification when enterprise buyers ask for it, or when you target Leading (preferred) or Premier (mandatory) tier.

- Gate: 6 months listed†, 60 active installs†, average API success above 95%†, verified domain, security questionnaire, Uninstall App API, 3-minute demo video†. An extension that injects into HubSpot's UI blocks certification. Fix 429s (throttle to 100 requests per 10 seconds per account†, batch, use webhooks), 401s from expired tokens and 403s on portals missing a scope before applying.
- Recertify every two years†; notices start 90 days† before expiry.
- Tiers apply to the developer account and rest on attached MRR, influenced MRR, reviews and rating†, evaluated quarterly. Read [references/submission-packet.md](references/submission-packet.md) § Tiers before promising one.

## Output

Key the answer on the route. A single question gets a direct answer plus the sections it touches.

- **Building or piloting**: assumptions; eligibility verdict; distribution and auth settings; pilot plan to 3 active installs with names or segments; scope table (scope, feature, object, sync direction, required or optional); packet checklist with owners; timeline backward from launch with one Draft bounce; deadlines from § Deadlines.
- **Legacy public app**: install count against the 25 cap, the HubSpot contact to make first, migration and listing order with dates.
- **In review or bounced**: one fix per feedback point, the single resubmission date.
- **Listed**: obligations at risk (install floor, version, legacy architecture, reviews), certification go/no-go with the gate gaps.

## References

- samber/developer-platform-skills@oauth2-provider-design - scopes and consent on your own API.
- samber/developer-platform-skills@mcp-server-offering - the MCP server behind an MCP listing.
- samber/developer-platform-skills@chrome-web-store-playbook - the store approval a companion browser extension needs.
