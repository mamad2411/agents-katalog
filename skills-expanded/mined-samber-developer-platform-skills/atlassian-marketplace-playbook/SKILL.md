---
name: atlassian-marketplace-playbook
description: >-
  Takes a B2B SaaS vendor's Jira, Confluence or Jira Service Management
  app onto the Atlassian Marketplace and keeps it there - Forge vs Connect, Free vs Paid via
  Atlassian for a connector to a paid SaaS, payment-model locks, pricing and revenue share,
  approval prerequisites, major versions needing review and admin consent, Connect-to-Forge
  migration, Enterprise Certified (successor to Cloud Fortified), bug-fix SLAs. Use whenever
  a vendor mentions listing on the Atlassian Marketplace, a Marketplace Forge or Connect app,
  a stalled ECOHELP review, or applying for Cloud Fortified. Do NOT use for listing copy or
  search rank (use samber/developer-platform-skills@integration-listing-optimization), for
  Forge code, internal-only apps, Bitbucket, Compass or Trello apps, or buyers vetting apps.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Atlassian Marketplace playbook

You take a vendor's Jira, Confluence or JSM app through Atlassian Marketplace approval and keep it listed. The costly mistakes are architectural and commercial, made before submission: framework, payment model, licensing, and the scopes that later force review and admin consent. Mark every Atlassian figure (rates, SLAs, durations, dates) with `†` and a footnote: verify against current Atlassian developer docs, because Atlassian changed its framework, badge and revenue-share rules within one year.

## Rules that decide the plan

1. **Forge only.** The Marketplace accepts no new Connect apps, Connect-descriptor apps receive no updates, and Connect support ends on 31 Jan 2027†. Existing Connect vendors move to Forge on the same listing (`app.connect.key` in `manifest.yml`).
2. **Free or Paid via Atlassian (PvA).** Forge cloud apps get no Paid via Vendor option without Atlassian's written permission.
3. **Payment model changes are new versions, not toggles.** Free → PvA needs licensing enabled in the manifest, a new version, re-approval, and a major version each site admin must accept; existing installs count as unlicensed until the admin subscribes.
4. **A PvA license matches the host site's licensed user count.** Customers cannot license a subset of users.
5. **Every added scope, egress domain, remote or auth provider creates a major version.** Each major re-enters Marketplace review (questionnaire, scan, 5-10 business days†), and sites needing new permissions stay on the old major until their admin consents.
6. **No collected Atlassian API tokens.** Use OAuth 2.0 or Forge auth; apps storing user API tokens are refused unless Atlassian grants an exemption.

| Rationalization                                             | Why it fails                                                                                                                                                                                   |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Connect is faster, our backend already exists."            | Submission is closed and Connect support ends. Forge remotes call the same backend.                                                                                                            |
| "We'll get Cloud Fortified."                                | Cloud Fortified takes no new apps and is being phased out. Atlassian Enterprise Certified (AEC) replaces it: Forge-only, SOC 2 Type II or ISO 27001, accepted trust center, public bug bounty. |
| "List free, sell the Jira features from our site."          | Atlassian has published no ruling that an external plan unlocking the app's own features is allowed; it reads as Paid via Vendor. Ask before building billing.                                 |
| "Ship free now, switch to paid later."                      | The switch is a new version, a re-review and an admin-consented major; adoption stalls on sites that never accept it.                                                                          |
| "Ask for broad scopes now to avoid future consent prompts." | Reviewers check each scope against features, Ecoscanner flags unused ones, and AEC fails them.                                                                                                 |
| "Ship the security fix with the new integration."           | A release adding scope or egress is a major: it waits for review while the fix deadline runs.                                                                                                  |
| "Install our production build on our site to test."         | Every production install of a paid app is billed, yours included. Test in development or staging with `forge install --license active` (or `inactive`, `trial`).                               |
| "We'll ship a Data Center version for regulated customers." | New Data Center apps are closed† (Bitbucket excepted). Offer Forge with data residency, Atlassian Government Cloud or Isolated Cloud, each a separate app type and re-review.                  |

## Interview

Ask one question at a time; skip what the request answers. When you cannot ask, state one assumption per gap and flag it.

1. What does the app do inside Jira, Confluence or JSM, and does any of it work without an account on your SaaS?
2. Stage: not built, Connect app listed, Forge app submitted or returned, or listed on Forge?
3. Who pays today, and do you want to charge for the Atlassian app itself?
4. Do target buyers require data residency, no data egress, or a vendor security review?
5. Launch date, and whether an event is pinned to it.

Re-rank the menus below against answers 1, 4 and 5, and say which answer moved which option.

## Route by stage

- **Not built** → Architecture, Payment and pricing, Submission.
- **Connect app listed** → Connect migration, then Submission for the Forge version.
- **Submitted or returned** → Submission; fix every point in one pass.
- **Listed** → Versions and consent, Keep the listing, Trust ladder.
- **Listing copy, keywords, screenshots, reviews** → samber/developer-platform-skills@integration-listing-optimization.
- **Whether Atlassian is worth it at all** → samber/developer-platform-skills@integration-partnership-strategy.

## Architecture

For a vendor connecting its own SaaS, ranked by efficiency: Forge UI with Forge remotes to your backend > OAuth 2.0 (3LO) integration listed as not directly installable.

- **Forge UI + remotes** (default): in-product UI, OAuth, your existing backend.
- **3LO listing**: cheapest when the integration already runs on Atlassian OAuth with no UI inside Jira. No in-product surface, no path to AEC.
- Runs on Atlassian is out of reach for a connector: the badge requires no egress except analytics. Only a product living entirely on Atlassian compute and storage earns it, automatically. For buyers blocking on egress, offer data residency for remote data, disclosed egress and AEC.
- Declare every first-hop egress domain and its `inScopeEUD` flag correctly in the first version, with no broad wildcards: each later addition, or a false → true flip, is a major version.
- Budget Forge consumption billing: usage above each monthly free allowance is invoiced to the developer, free apps included.

## Payment and pricing

Atlassian's own texts conflict for a free app that needs a paid external account: the approval guideline asks for useful function "as is" and recommends Paid via Vendor, which Forge apps cannot use. Resolve it this way:

- Connector to your SaaS → **Free**, with some in-product value that works without an account (read-only panel, preview, sample data), and the paid account stated in the listing.
- Revenue from the Atlassian app itself → **PvA** from version one, licensing enabled, license checked in code (`context.license.active`, `filter.appIsLicensed` on triggers).
- Already listed Free → keep existing features free for a stated grace period and gate only new features behind the license.
- Any external plan touching Jira features → get Atlassian's ruling written on the ticket before building billing.

PvA mechanics: prices per host user count with lower per-user rates at higher counts, annual price at 10 times monthly†, Standard and Advanced editions (a new edition is a re-review), multi-instance pricing for Enterprise sites. Existing customers keep the old price for 60 days† after a change. Partner share: 83%† for Forge-only apps (no Connect module or Connect scope), 75%† otherwise, and 100% until $1M lifetime Forge revenue†.

## Submission

Clear the prerequisites first. Practitioners report most "Timeout" rejections come from unfinished prerequisites, not from the reviewer; ask on the ticket what timed out.

1. Confirm the submitter can open tickets in the Developer and Marketplace Support portal (ECOHELP); fix access through a support request.
2. Complete partner identity verification (KYC/KYB, one-time), the app security questionnaire, the Privacy & Security tab, and the payment profile.
3. Publish a privacy policy, End User Terms (Atlassian's customizable agreement is accepted), a DPA if you process personal data, and documentation linked from the listing.
4. Name the app "Name for Jira", never "Jira Name"; use a company email domain for PvA.
5. Enable sharing in the developer console, then submit. Put test credentials for your SaaS on the ticket. Once licensed or submitted, the app can no longer be shared by installation link: give testers a separate unlicensed copy.
6. Plan three weeks per round (official figures range from one week to 15 business days†) plus one returned round. The listing is locked in review; request copy changes on the ticket. A scan finding rejects the ticket: fix it, then resubmit.

Full packet, dates and tables: [references/submission-and-upkeep.md](references/submission-and-upkeep.md).

## Connect migration

1. Add Forge to the Connect app and list the Forge version on the same listing.
2. Front-load the first Forge version: every Forge-specific scope, remote and fetch permission the end state needs ships there without admin approval (except `read:chat:rovo` and scopes elevating beyond the Connect scopes). Afterwards, while any Connect module remains, the same additions need approval. Never change the Connect `baseUrl`, an auth provider, or free vs paid in that first version.
3. Remove every Connect module and Connect scope to reach the Forge share and AEC; removing Connect scopes and the Connect remote needs `forge version bulk-upgrade`. Suspended or access-token installs never auto-upgrade: contact them.

## Versions and consent

- Run `forge version bulk-upgrade` for majors that escalate no privilege, and rolling releases to ship code while consent is pending.
- Batch privilege-escalating changes into planned majors, with release notes telling admins why. Keep the previous major working and backport security fixes as minors.
- Removing egress is minor; removing a scope is still major.

## Keep the listing

- Fix security findings in time†: cloud Critical 10 days, High 4 weeks. A missed Critical hides the app from new installs; a missed High hides an unbadged app on day one, or strips badges and hides it after 15 days. Silence for 90 days hides the app; a failed threat assessment or exhausted contact can pause it for existing customers.
- Report a security incident within 24 hours†.
- Ship at least one version every 18 months†, or a compliance review starts.
- Support every paying customer through their paid term when retiring the app.

## Trust ladder

Ranked by value per effort: complete Privacy & Security tab with trust-center link (hours, read by every security reviewer) > public Marketplace bug bounty (a partner-funded reward pool, weeks of lead time, and every finding becomes an SLA-bound ticket; required for partner tiers) > AEC (SOC 2 Type II or ISO 27001, accepted trust-center provider, pen test, Statuspage, data residency for remotely stored data; months). The order starves AEC; promote it when enterprise deals stall on vendor security review and an audit is already under way.

## Output

The sections above supply the content; this section sets the shape. Key the answer on the route; a single question gets a direct answer plus the rules it touches. **Not built** and **Connect app listed** get:

1. Assumptions, one per missing interview answer.
2. Architecture and payment-model decision, each with the answer that drove it.
3. Irreversibles register: framework, payment model, licensing, scopes and egress at launch, app name; owner and date each.
4. Submission checklist with an owner per prerequisite; timeline backward from launch with one returned round.
5. Post-listing calendar with checks: approval within two rounds, share of installs on the latest major at 30 and 90 days, zero AMS tickets past due.

## References

- samber/developer-platform-skills@oauth2-provider-design - the issuer side of scopes and consent, for your own API.
- samber/developer-platform-skills@app-marketplace-monetization-model - the operator view of the billing rails you plug into.
- samber/developer-platform-skills@integration-health-monitoring - noticing when the Jira side of your integration breaks.
