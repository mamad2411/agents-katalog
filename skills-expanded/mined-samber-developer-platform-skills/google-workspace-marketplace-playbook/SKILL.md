---
name: google-workspace-marketplace-playbook
description: >-
  Gets a SaaS vendor's Google Workspace integration through Google OAuth app verification and
  onto the Google Workspace Marketplace - Gmail, Drive and Chat scope choice, the CASA security
  assessment, listing review, admin domain-wide install, changes after listing. Use whenever a
  vendor mentions publishing a Workspace add-on, Gmail or Drive integration, or Chat app, the
  "Google hasn't verified this app" screen, the 100-user cap, CASA, restricted scopes, or a
  rejected Marketplace review. Do NOT use for listing copy (use
  samber/developer-platform-skills@integration-listing-optimization), for your own API's OAuth
  (use samber/developer-platform-skills@oauth2-provider-design), or for internal-only apps.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Google Workspace Marketplace playbook

You take a vendor's Google Workspace integration through Google's two gates and keep it there: OAuth app verification (Google Trust & Safety) and Marketplace listing review (Marketplace team). Scope choice decides the cost of both, so settle it before anything else. Mark every Google figure you quote with `†`: verify it against current Google docs, because Google renamed the security assessment's levels and moved verification timelines within a year.

## Rules the gates enforce

1. **The scope tier sets the bill.** Non-sensitive: brand verification only. Sensitive: verification, up to 10 days†. Restricted: verification over several weeks† plus a paid third-party CASA assessment, renewed every 12 months†, whenever restricted data can reach your servers.
2. **Request only scopes your shipped features call**, each with a written reason a narrower scope fails. Take the `.readonly` variant when the feature never writes. "Future proofing" is a policy breach, not a convenience.
3. **Declare identical scopes in three places**: code or manifest, Marketplace SDK, consent screen (Data Access). Any drift shows users the unverified-app screen or a second consent prompt, a top rejection cause.
4. **The listing cannot be approved before OAuth verification completes.** Run both in parallel; the slower one sets the date.
5. **Limited Use binds data from every sensitive or restricted Workspace scope** (Gmail, Drive, Chat, Calendar, Sheets, Meet): only for user-facing features, no ads, no human reading without the user's consent for specific data, no training or improving AI models beyond that user's own personalized model. Show an in-app disclosure right before consent, and request consent in context for each agentic capability (MCP tool, skill) before it first touches user data.
6. **Domain install removes the consent prompt, never the verification.** After an admin installs an approved Marketplace app domain-wide, users must never see a consent prompt again: listing policy.

| Rationalization                                           | Why it fails                                                                                                                                                                               |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| "Take `drive` / `gmail.readonly` now, narrow later."      | Restricted scopes trigger CASA and weeks of review; narrowing later is another verification round. Start narrow (table below).                                                             |
| "Admins install it domain-wide, so we skip verification." | Domain-install-only apps skip brand verification only; sensitive and restricted scopes still need verification, and a public listing needs it regardless.                                  |
| "Set the consent screen to Internal to dodge review."     | Internal works only for users of the organization owning the Cloud project. A multi-customer SaaS cannot use it, and an Internal app fails Marketplace review.                             |
| "Book CASA Tier 2 with a lab now."                        | Google now assigns AL1 or AL2† (older pages and labs still say Tier 2 or 3); you cannot pick it, self-scans are deprecated, and Trust & Safety emails you when to start, as the last step. |
| "Customer mailboxes will improve our model."              | Banned under Limited Use for anything beyond that user's personalized model; the demo video must show explicit consent even for that.                                                      |
| "Unpublish the old app to retire it."                     | Unpublish does not reliably cut existing users; only deleting the Cloud project does, and that also kills every OAuth client in it. Delete only a project holding nothing else.            |

## Interview

Ask one question at a time; skip what the request answers. When you cannot ask, state one assumption per gap and flag it.

1. What runs where: your web app calling Google APIs, a Workspace add-on (Gmail, Calendar, Drive, Docs, Sheets, Slides, Meet), an Editor add-on, a Chat app, a Drive app? Also a Chrome extension calling Google APIs?
2. Which Google data do the features read or write, and does any of it reach your servers or an AI model?
3. Who installs: Workspace admins for whole organizations, individual users, or both?
4. Stage: building, in verification (which stage), in Marketplace review, rejected, or listed and changing scopes? Launch date?
5. Who owns the Google Cloud project: an organization resource with two or more owners, or one person's account?

Answer 2 decides the scope ladder. Answer 4's date re-ranks it: inside 6 weeks, restricted scopes leave the launch set when they serve secondary features, and the date moves when the core product needs them. A "one person" answer to 5 makes moving the project into an organization step one.

## Route by stage

- **No verification needed**: personal use, Testing status with named test users, service-account access to your own data, or an Internal app used only inside the project's organization. Otherwise an app showing sensitive or restricted scopes unverified caps at 100 users† over the app's lifetime, with no reset, until verified.
- **Building** → Scope ladder, Do you need a listing, Sequence.
- **In verification or review, or rejected** → Sequence; fix every point in the review document, then resubmit once.
- **Listed** → Changes after listing.
- **Chrome extension packaging and Chrome Web Store review** → samber/developer-platform-skills@chrome-web-store-playbook. The Google API scopes that extension requests still pass through this skill's verification.
- **Listing copy, screenshots, install conversion** → samber/developer-platform-skills@integration-listing-optimization.

## Scope ladder

Ranked by efficiency, highest first. Build the table of feature → API method → minimum scope → tier before any listing work. Scopes below are examples: read each API's scope page for its tier.

- **Non-sensitive, contextual** (cheapest, days): Drive `drive.file` with the Google Picker (files the user opens or picks); Gmail add-on `gmail.addons.current.message.action` and `gmail.addons.current.action.compose` (the open message only); `gmail.labels`; Chat `chat.bot` (app authentication); `drive.install` for Drive "Open with".
- **Sensitive** (verification up to 10 days†, no assessment): `gmail.send`, `gmail.addons.current.message.readonly`/`.metadata`, most Calendar and Contacts scopes.
- **Restricted** (weeks† plus CASA every year): `mail.google.com`, `gmail.readonly`, `gmail.modify`, `gmail.compose`, `gmail.metadata`, `gmail.settings.basic`, `drive`, `drive.readonly`, `drive.metadata.readonly`, `drive.activity`, `chat.messages`, `chat.messages.readonly`. The order starves this rung, yet it is the only way to sync a whole mailbox or Drive. Take it when the core product (backup, search, analytics across all mail or files) cannot exist without it, and only for an app type Google permits for that API (list in [references/submission-packet.md](references/submission-packet.md)).

Effort ordering: restricted > sensitive > non-sensitive. Value ordering can invert: whole-mailbox features exist only on the restricted rung. Compliance cost: restricted adds a yearly lab assessment, and Google may raise the assigned level as users grow†.

CASA applies when restricted data can reach a server outside Google. Apps Script add-ons with no outbound scope (`script.external_request`) have been treated as local clients and spared it (practitioner reports, not Google policy). An add-on that calls your backend needs that scope, so a SaaS add-on rarely qualifies.

## Do you need a listing

Ranked by efficiency for a B2B vendor:

1. **Verified OAuth client, no listing**: your web app connects Gmail, Drive or Calendar after verification. Verification removes the unverified-app screen; each user still consents, and admins who restrict access mark your OAuth client ID Trusted. Neither replaces verification. Publish that ID in admin-facing docs.
2. **Public listing, Individual + Admin install** (default): admin domain install without per-user consent, any surface inside Workspace (add-on, Chat app, Drive "Open with"), and self-serve discovery. Adds Marketplace review on top of verification. Chat apps allow only this setting.
3. **Public listing, Admin Only install**: when the app works only domain-installed; signed-in end users no longer find it in search.

Before promising Marketplace billing or featuring, read the packet's Pricing and Featuring sections: Google bills nothing, and featuring cannot be bought.

Visibility and piloting:

- **Private listings** serve only the publisher's own organization, never customers.
- **Visibility** (public or private) is permanent once saved. A consumer Gmail account can publish only public.
- **Pilot before approval** through OAuth Testing status with named test users (tester warning, user cap, short-lived tokens†). Switch to In production before submitting: Testing status is a named rejection cause.
- **The Testing route reaches customers only through your web app's own OAuth flow.** Users at customer companies get an add-on or Chat app only after public approval.
- **Draft testers** on a public listing must be Gmail accounts, so Workspace-domain customers cannot preview it.

## Sequence

1. Put the Cloud project inside an organization with two owners and billing enabled, before saving visibility; reuse the app's existing project. Listing, verification and CASA all key on it. Apps Script add-ons must move off their default project to a standard one. A published private app stays with its original organization when its project moves. Lose the last owner and only a support case recovers the listing.
2. Brand verification: homepage and privacy policy on a Search Console-verified domain, same privacy URL on homepage and consent screen. Publish branding within 7 days† of passing.
3. Data access request in the Verification Center: scopes, per-scope justifications, demo video. Packet in [references/submission-packet.md](references/submission-packet.md).
4. Restricted only: answer Trust & Safety's CASA email, pick an authorized lab, collect the Letter of Validation.
5. In parallel: enable the Marketplace SDK (not the Marketplace API), configure integrations, scopes, install setting and developer details; build the store listing; give reviewers a test account with sample data. Pre-check the app against the per-integration review criteria in the packet.
6. Handle granular consent: users may grant only some scopes, so detect missing ones and re-prompt per feature. Reviewers reject apps that break on a partial grant.
7. Submit. Budget 2-4 weeks† end to end for sensitive scopes (practitioner reports; Google says Marketplace review takes "several days"), longer for restricted. Answer Trust & Safety mail fast: the review pauses until you reply.

## Changes after listing

- Re-enter Marketplace review: new integration type, new host app on a Workspace add-on, any App Details field (name, language, short or detailed description). Graphics and links publish from a draft.
- New sensitive or restricted scope: new OAuth verification first. Ship it live before approval and users see the unverified-app screen. Domain-installed customers' admins must authorize the new scopes in the Admin console; Google documents individual prompts until then, while the listing policy forbids re-prompting admin-installed users. Tell each admin in advance and release once they grant.
- Moving an integration into another listing loses its user counts and reviews, can cut existing users' access, and needs scope re-verification on the target project.
- Annual: CASA revalidation 12 months† after the letter date; keep Owner and contact emails current, or renewal notices go nowhere.

## Output

- **Building**: assumptions; scope table (feature, method, scope, tier, justification) with the ladder rung chosen and why; listing verdict and install setting; dated plan from the launch backward with one rejection round; owners per packet item.
- **Rejected or stuck**: one fix per review-document point, the single resubmission date, what pauses the clock.
- **Listed and changing**: the change classified (draft only, Marketplace review, OAuth re-verification, CASA), the admin re-grant notice.

## References

- samber/developer-platform-skills@oauth2-provider-design - the issuer side of scopes, consent and app verification, for your own API.
- samber/developer-platform-skills@app-marketplace-review - designing review for your own marketplace, the operator's chair.
