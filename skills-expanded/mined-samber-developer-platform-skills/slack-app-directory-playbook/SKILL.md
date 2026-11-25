---
name: slack-app-directory-playbook
description: >-
  Gets a B2B SaaS or developer-tools vendor's Slack app approved on the Slack Marketplace
  (formerly Slack App Directory) and keeps it listed - the active-workspace install gate, apps
  Slack refuses, per-scope justifications, Security & Compliance and AI disclosures, review
  timelines, updates to a locked live app, delisting triggers. Use whenever a vendor mentions
  submitting a Slack app, a returned Slack submission, Slack scope review, or listing vs
  staying unlisted for a commercial Slack app. Do NOT use for listing copy or install
  conversion (use samber/developer-platform-skills@integration-listing-optimization), for
  reviewing apps on your own marketplace (use
  samber/developer-platform-skills@app-marketplace-review), for a company's own internal
  apps, for admins vetting another vendor's app, or for Slack bot code.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.2"
---

# Slack App Directory playbook

You take a vendor's Slack app through Slack Marketplace review and keep it there. Approval hinges on three things a capable team still gets wrong: a real install base before submitting, scopes justified one by one, and an app reviewers can install without your help. Mark every Slack figure you quote (thresholds, durations, rate limits) with `†` and a footnote: verify against current Slack Marketplace docs, because Slack changed its install gate twice in a year.

## Rules the review enforces

1. Submit only with **10 or more active workspaces†** (used in the last 28 days, sandboxes excluded) and keep that count through the whole review: Slack blocks the submission below it. The suitability list pairs that count with 10 weekly active users†; the hard block is the workspace count. Pilot as an unlisted distributed app until then.
2. Request only scopes for features that exist today. Reviewers approve what they can test; a scope "for the roadmap" gets the submission returned.
3. Default to the bot token; user-token scopes pass only when the app must act as that user.
   - Ineligible: `identity.*`, `search:read`, `read`, `post`, `client`, `workflow.steps:execute`, `triggers:*`.
   - Partner program only: `admin.*`.
   - Enhanced review: `*:history`, `files:read`, `canvases:read`, `search:read.*`, `conversations.connect:write`, user-token `groups:write`, `groups:write.invites`, `mpim:write`.
4. Give reviewers a way to install the app themselves, plus test accounts with dummy data on your service and every third-party service it connects. They cannot log into any Slack workspace, yours included.
5. Never claim the app is certified, endorsed or approved by Slack: the Marketplace Agreement forbids implying endorsement, and Slack calls its security review "not a certification".

| Rationalization                                            | Why it fails                                                                                                                                                                                                                      |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Five workspaces was the bar."                             | It was, from August 2025 until July 2026. Slack moved it back to 10 and blocks submissions below it.                                                                                                                              |
| "Add the scopes now so customers never have to reinstall." | Untestable scopes return the submission. Mark non-core scopes optional instead, and plan the reinstall message.                                                                                                                   |
| "We'll stay unlisted; it's just a directory."              | Slack's API terms name the Marketplace the only channel for commercial apps, new installs of unlisted ones get 1 request/minute and 15 objects† on `conversations.history` and `conversations.replies`, and listing costs no fee. |
| "Customers can create their own app from our manifest."    | Slack's API terms count templated custom apps for a commercial product as commercial distribution: list instead.                                                                                                                  |
| "Approval in two weeks, launch on the 15th."               | Functional review takes up to 10 weeks† for a new app and cannot be expedited. Approval and publishing are separate: submit early, publish on launch day.                                                                         |
| "Share our demo workspace login with the reviewer."        | Reviewers cannot access Slack workspaces. Send the install link, a video, and service test accounts.                                                                                                                              |

## Interview

Ask one question at a time; skip what the request already answers. When you cannot ask, state one assumption per gap and flag it.

1. What does the app do inside Slack (notifications, slash commands, shortcuts, Home tab, unfurls, AI agent, MCP tools, workflow steps), and which Slack data does it read or write?
2. Stage: building, unlisted pilot (how many active workspaces), submitted (preliminary, functional, returned), or listed and planning a change?
3. Launch date, and whether an event or announcement is pinned to it.
4. Does any feature send Slack data to an LLM, or is the product an automation platform connecting other services?
5. Do target customers run Enterprise Grid or Slack Connect channels?

Re-rank the install-gate menu against answer 3 and say which answer moved it. A yes to answer 5 makes org-ready deployment and Slack Connect behaviour part of the review: test both before submitting.

## Route by stage

- **Building** → Eligibility, Environments as code, Scopes, Submission packet, Review stages and timeline.
- **Unlisted pilot** → the same four, starting with the install count.
- **Submitted or returned** → Review stages and timeline; fix every point before resubmitting.
- **Listed** → Changes after listing, Keep the listing, Visibility.
- **Listing copy, screenshot order, install conversion** → samber/developer-platform-skills@integration-listing-optimization.
- **Selling through AgentExchange private offers or unified billing** → samber/developer-platform-skills@salesforce-appexchange-playbook. Salesforce's April 2026 AgentExchange merge† added discovery and optional billing paths; it published no change to the Slack review or its zero listing fee.

## Eligibility

Check the idea against Slack's unsuitable list before building anything else. Refuse to plan a submission for an app that:

- exports or backs up message data, bulk-deletes, or self-destructs messages;
- does nothing inside Slack, only offers Sign in with Slack, embeds Slack elsewhere, or is a Slack client;
- trains LLMs on Slack data, runs unexplained or non-aggregate sentiment analysis, lets AI take consequential decisions without human review, or infers protected characteristics;
- moves money, crypto or NFTs, or shares sensitive financial or health data in Slack;
- runs downloaded scripts or terminal commands from Slack, or lets several users share one third-party service account;
- is a coded workflow (Deno SDK), or circumvents admin controls or the free plan's 90-day history limit.

An app whose only feature is an MCP server for Slackbot can list, with `mcp:connect` required, when its tools deliver meaningful work inside Slackbot conversations. A thin, vaguely described or failing tool set is what Slack rejects.

Clear the install gate by ranked efficiency, highest first: existing customers already asking for Slack, as an unlisted pilot > design partners recruited for the pilot > staff or partner teams on their own paid workspaces. Sandboxes never count; never rely on your own build or test workspaces, since reviewers expect the app proven where it was not built. A launch inside three months promotes design-partner recruiting to start this week. Pilot installs of history-reading features run at the unlisted rate limit: drive them from events, or warn pilot customers.

## Environments as code

Keep the app manifest in your repository and apply it with `apps.manifest.update` or the Slack CLI. Never edit app settings by hand: one templated file rebuilds dev and staging apps identical to production.

1. Keep one manifest template. Change only these per environment: display name, slash commands (`/acme-dev`, so two apps can share one workspace), and the redirect, request and event URLs.
2. Create three apps from it:
   - `<app>-dev`: distribution off, so it installs only in your development workspace or a developer sandbox.
   - `<app>-staging`: distribution on, never listed. Send its install link only to reviewers and pilot testers.
   - production.
3. Give each app its own signing secret, client secret and token store. Never share tokens between environments.
4. Apply manifests from CI with an app configuration token. It expires after 12 hours†: rotate it with `tooling.tokens.rotate` and store the refresh token.
5. Before every resubmission, diff the template against the live app (`apps.manifest.export`). That diff is the change list reviewers test.

## Scopes

Build the scope table before writing any listing copy: it decides eligibility, review depth and how many reinstalls you will force later.

1. List every Web API method and event the shipped features call.
2. Map each to its minimum scope; prefer the bot token; drop duplicates across bot and user tokens.
3. Write one justification per scope saying how the app uses it, never what the scope does. Examples in [references/submission-packet.md](references/submission-packet.md).
4. Search, indexing and "catch me up" features: fetch messages when needed instead of storing copies, and name the Real-time Search or MCP use case in the justification. Slack rarely approves broad history access for bulk indexing. The Real-time Search API† serves listed and internal apps only: pilot through events or the throttled history methods, switch after approval, and describe both paths in the submission notes.
5. Mark scopes that only enhance the core experience as optional (`bot_optional`, `user_optional`). Never move a core scope there to lighten the consent screen.
6. Check the privacy model: no user sees a private channel, message, file or action Slack would hide from them, including guests and Slack Connect members.
7. Automation platforms:
   - check the plan with `team.billing:read` right after OAuth and revoke the token on free workspaces;
   - never expose the Slack token to your users, and never share one user's Slack authorization with others;
   - request no user-token `*:history` or `files:read` to collect data, and block templates that export, back up or bulk-delete Slack data.

## Submission packet

Assemble it from [references/submission-packet.md](references/submission-packet.md): listing fields, landing, support and privacy pages, test information, video, Security & Compliance answers, AI and MCP disclosures, and the in-app checks reviewers run. Write the Security & Compliance answers for the customer's security team: they are self-certified and shown on the listing, where admins read them before approving the app. Remove test slash commands and clear the automated checks before submitting.

## Review stages and timeline

- **Automated checks** at submission: fix and submit.
- **Preliminary**†: listing, links, scope reasons, install access; up to 10 business days. Every resubmission here resets your queue position, so fix all feedback in one pass.
- **Functional**†: a reviewer installs and tests; up to 10 weeks new, 6 weeks for updates. Resubmitting keeps your place.
- Common return causes, each a written guideline: an unneeded scope, missing onboarding or "help" replies, a privacy policy silent on Slack data, a landing page that is a doc or repository.
- Read the current estimate on the submission page, plan backward from the launch date with one returned round (count it as another preliminary cycle), and publish when you choose after approval. When approval cannot land before the launch, announce the integration as coming to the Slack Marketplace, take pilot sign-ups, and publish on approval. Never drive general-audience installs to the unlisted app.

## Changes after listing

The live app is locked: configuration, features and scopes change only through a resubmission.

- Display info, pricing, languages and existing URLs: resubmit, no demo needed.
- New features or scopes, rewrites included: resubmit with a video and the staging app from Environments as code, which reviewers can install. The live listing stays up meanwhile.
- Never put an unreviewed scope in the live install URL: installs fail. After approval, update the OAuth URL and ask existing workspaces to reinstall through App Home or a message.
- Irreversible switches:
  - token rotation: refresh within 12 hours†, persist each new refresh token, enable it on the staging app first;
  - the move from classic to granular permissions, which forces every workspace to reinstall;
  - Deactivate Public Distribution, which uninstalls the app from every other workspace. A listed app cannot use it.
- Discontinuing: give Slack 10 days' written notice†, remove the listing in Published app settings, tell customers, delete the app to revoke its tokens.

## Keep the listing

Slack contacts you on broken support or privacy links, user complaints, uninstall or error spikes, or an unused app. Silence gets the app delisted while Slack retries; a reply that resolves the issue keeps or restores the listing. Slack delists without notice on a broken landing page or install flow, an abandoned app, or a substantial change shipped without review. A security review can arrive at any time; unanswered security issues can cost you your tokens.

1. Answer support within 2 business days†; keep developer, support and security contacts current; keep a second collaborator on the app.
2. Do not count on Slack for install analytics: track installs and uninstalls yourself (OAuth install ledger, `app_uninstalled`).
3. Subscribe to the platform changelog and adopt new security features.

## Visibility

Ranked by efficiency, highest first: the `slack-app-id` meta tag on every page of your domain (app suggestions when your links are shared, minutes of work, compounding) > direct install from the listing (an hour, plus onboarding for installers without an account) > Add to Slack in your product's settings > asking Slack to feature the app. Featuring is one-shot and editorial, so the order starves it; promote it when a launch with public material is coming.

## Output

Key the answer on the route. A single question gets a direct answer plus the sections it touches.

- **Building, Unlisted pilot**: assumptions, one per missing answer; eligibility verdict and install-gate plan; scope table (scope, token, methods, feature, justification, required or optional, enhanced review); packet checklist with an owner per item; timeline backward from launch with one returned round; post-listing obligations and irreversible switches.
- **Submitted or returned**: one fix per feedback point, the single resubmission date, the queue effect.
- **Listed**: the change classified (no demo, demo plus staging app), staging plan, reinstall message, obligations at risk.

## References

- samber/developer-platform-skills@integration-listing-optimization - listing copy, media order, install conversion.
- samber/developer-platform-skills@oauth2-provider-design - the issuer side of scopes and consent, for your own API.
- samber/developer-platform-skills@mcp-server-offering - the MCP server behind a Slackbot MCP listing.
- samber/developer-platform-skills@atlassian-marketplace-playbook - the same vendor job for a Jira or Confluence app on the Atlassian Marketplace.
- samber/developer-platform-skills@microsoft-appsource-playbook - the Teams store and Microsoft Marketplace equivalent, when the same chat app also ships to Teams.
