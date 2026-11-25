---
name: chrome-web-store-playbook
description: >-
  Gets a B2B SaaS or developer-tools vendor's companion Chrome extension through Chrome Web
  Store review and keeps it published - permission scoping, reviewer access to login-gated
  features, the Privacy practices tab, violation IDs such as Purple Potassium, permission
  changes in updates, rollout and rollback, publisher-account security, per-customer and
  enterprise distribution. Use whenever a vendor mentions publishing a Chrome extension, a
  Chrome Web Store rejection or takedown, the item limit, or white-label builds for
  customers. Vendor side only: not IT admins, Firefox AMO, Edge Add-ons or code. Do NOT use for VS Code or JetBrains extensions (use
  samber/developer-platform-skills@ide-extension-offering) or listing copy (use
  samber/developer-platform-skills@integration-listing-optimization).
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Chrome Web Store playbook

You take a vendor's companion extension through Chrome Web Store review and keep it live. Review reads three things against each other: the code, the declared permissions, and what the listing and Privacy tab claim. Any mismatch is a rejection. Mark every figure and every practitioner-reported behaviour you quote with `†`: verify against current Chrome Web Store docs, which changed the item limit and badges in 2026.

## Rules review enforces

1. Request the narrowest permission per feature. Reviewers assume you use every permission; an unused one (`tabs` beside broad host access or `activeTab`, `cookies` for `document.cookie`) returns **Purple Potassium**. Never add a permission for a feature not yet shipped.
2. Ship all extension logic inside the package. Remote config, data and images are fine; a CDN `<script>`, `eval` of fetched code, or an SDK that lazy-loads scripts returns **Blue Argon**. An iframe or sandboxed page showing your web app is exempt, but its behaviour must still be reviewable and disclosed.
3. Minify at most, never obfuscate (**Red Titanium**). Legacy polyfills and old async helpers have been flagged†: target modern Chrome.
4. Let the reviewer reach every feature. A login wall without credentials returns **Yellow Magnesium**.
5. One narrow single purpose. A CRM sidebar plus a tab manager is two extensions; an extension that only opens your web app is banned (**Yellow Lithium**).
6. Make the Privacy tab, the privacy policy and the code say the same thing, including analytics, error reporting, local storage and `chrome.storage.sync`. Page URLs count as browsing activity: collect them only for a user-facing feature the listing describes, disclose before collecting, get consent, send over HTTPS.
7. Appeal each violation once†; frivolous appeals can cost future appeal rights. Clarify through support first, then appeal with evidence.

| Rationalization                                    | Why it fails                                                                                                                                              |
| -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "`<all_urls>` so it works on any customer's site." | Broad hosts get the slowest review and the scariest install warning. See Host access.                                                                     |
| "Review takes 1-3 days, launch Tuesday."           | Google states a few days to a few weeks†; queues reached 3-4 weeks† in April 2026. Stage approved builds and publish on launch day.                       |
| "Pending too long, cancel and resubmit."           | Google staff warned in 2026 that cancelling resets your queue position†. Cancel only to replace a broken package; escalate to support after three weeks†. |
| "Add the new permission in the next update."       | A permission with a new install warning disables the extension for every user until they accept. Optional permissions do not.                             |
| "One public listing per customer, rebranded."      | Duplicate experiences violate repetitive content, across affiliated publishers too; abuse of the exceptions costs the account. See Distribution.          |
| "We'll publish one extension per product line."    | New publishers get two extension slots† by default; consolidate or request an increase first.                                                             |

## Interview

Ask one question at a time; skip what the request answers. When you cannot ask, state one assumption per gap.

1. What does the extension do, on which sites (your app's domains, customers' domains, any page), and must it run without a click?
2. Does any feature need a login, paid plan, SSO or corporate network?
3. Stage: first submission, in review, rejected or taken down (which violation ID, go to When it goes wrong), or live and changing?
4. Who installs it: self-serve users, or customer IT pushing it to managed browsers (Google Admin, or another management tool)? Any customer needing its own branded build?
5. Launch date, and current seven-day active users (partial rollout needs over 10,000†)?

## Host access

Layer it; `content_scripts.matches` counts as host access too, so moving `<all_urls>` there narrows nothing.

1. Required host permissions: your own origins only.
2. Customer or third-party sites, ranked by efficiency (review speed and install conversion per unit of engineering), highest first:
   1. `activeTab` for click-triggered features.
   2. Optional host permissions for the customer's domain, requested from a user gesture, then `scripting.registerContentScripts`.
   3. A per-customer build with that host required (Specific Host exception; a separate item, slot and review per customer).
   4. Broad host patterns.
3. Broad patterns earn their place only when the single purpose spans every page (a page annotator); justify it explicitly. They draw in-depth review and the "read and change all your data" warning.

Force-install grants required permissions silently, but optional hosts still prompt each user. When customer IT pushes the extension and it must run on their domain without a click, choose between one Enable click per user and the per-customer build; test the choice on a managed profile.

## Submission

Build the packet from [references/submission-packet.md](references/submission-packet.md): permission-to-feature map, Privacy tab answers, test instructions, labelled variant text, violation IDs, appeal template.

1. Account: a dedicated company mailbox (the developer email never changes; a personal-address account moves only by a new account plus an item transfer request), mandatory 2-Step Verification, Trader declared with company details (shown publicly in the EU), teammates as members with roles, never one shared login.
2. Upload a package built by CI, manifest at root, version higher than the last. Fix pre-submission install test failures before submitting.
3. Fill the Privacy tab: single purpose sentence, one justification per permission naming the user-facing feature, remote code answer, data types, Limited Use certification, privacy policy URL. Put the Limited Use statement on your own site.
4. Fill Test instructions: a permanent seeded demo tenant, no SSO-only, MFA or expiring trial, steps to each feature, server allowlists open to reviewers. Show an "account required, sign in" state in the extension too.
5. Untick auto-publish to stage. An approved build waits up to 30 days†, then reverts to draft. When approval may miss a fixed date, demo a local build and announce the listing as coming.
6. After first publish, opt in to Verified CRX Uploads (Account security).

## Updates and releases

- Every update is fully reviewed; the live version stays until the new one publishes.
- Stage new access as optional permissions behind an in-product "Enable" button. Promote to required only in a major version, after testing the upgrade by packing two CRX versions locally. Test force-installed fleets separately: users there cannot disable or remove the extension.
- Partial rollout (over 10,000† seven-day users): set before submitting; raising the percentage needs no review; one at a time; unavailable for the version that follows a warning or takedown.
- Rollback: republishes the previous version under a new version number within minutes, no review, discards pending submissions. During a partial rollout it returns to the last version published to 100%, possibly two versions back. Keep storage migrations backward compatible across both.

## Account security

In December 2024 a phished employee granted a malicious OAuth app Chrome Web Store publish access; no 2-Step Verification prompt fired, and the attacker's update passed review and reached installs with no hold.

1. Opt in to Verified CRX Uploads: every later package must be a CRX signed with your private key, so CI switches from zip to signed CRX. Keep the key in CI secrets or an HSM, never in the Google account; a lost key takes up to a week† to replace.
2. Publish from CI through the Chrome Web Store API with a dedicated service account, never a person's OAuth token. Its one scope grants full publish rights: guard it like a production secret.
3. Restrict third-party app access in your Workspace so no unverified app can obtain the Chrome Web Store scope; tell staff store policy emails never need OAuth consent.
4. Alert on any published version CI did not produce; keep a rollback runbook.

## Distribution for B2B

Ranked by efficiency, highest first:

1. **One public or unlisted item for every tenant**: your brand in the store; the extension loads each tenant's logo, name and domains after sign-in. Customer IT force-installs it by extension ID with any browser management tool. Unlisted serves customers who refuse public items. One item, one review per release.
2. **Private publishing to the customer's organization**: needs a customer managing Chrome through Google Admin. Their admin approves your link, then sees and force-installs the item. Each item is a separate build to review, with the domain statement from the reference; it stays published but cannot update if the customer revokes approval, so agree an owner or transfer it to them through support.
3. **Unlisted white-label build per customer**: only when the customer's own name must appear in Chrome. Sent to that client only, exception statement in the description and single purpose field (text in the reference).
4. A separate public listing per customer: banned as repetitive content.

The order starves per-customer store branding; promote rung 3 only when a contract requires it. Whether private or unlisted items count toward the item limit is undocumented: ask support before scaling rungs 2-3. Test a beta with trusted testers or a private item; a public beta item needs "BETA" in the title, the beta statement and the production URL in the description.

## When it goes wrong

- **Rejected**: listing and live version stay, but the violation can trigger re-review of the live version; fix every cited point in one resubmission.
- **Warning**: 7-30 days† to ship a fix while the item stays live. Periodic re-review against current policy can warn a version nobody changed.
- **Takedown**: listing 404s; after weeks unresolved, Chrome disables existing installs and tells users, who may re-enable. Ship the fix through normal submission.
- **Appeal**: from the dashboard item or account page (repetitive content through the support form), once, with a permission-to-feature map, code references and a screen recording.

## Output

- **First submission**: assumptions; host-access layers; permission-to-feature map; Privacy tab answers; test instructions; account checklist; timeline back from launch with one rejection round.
- **Rejected or taken down**: violation ID, cause, fix, resubmit or appeal decision.
- **Live and changing**: permission impact (warning or not), rollout and rollback plan, security gaps.

## References

- samber/developer-platform-skills@integration-listing-optimization - listing copy, screenshots, install conversion.
- samber/developer-platform-skills@ide-extension-offering - VS Code and JetBrains extensions.
- samber/developer-platform-skills@app-marketplace-review - designing review for your own marketplace.
- samber/developer-platform-skills@api-integration-surface-strategy - whether a browser extension belongs in the surface roadmap.
- samber/developer-platform-skills@oauth2-provider-design - the sign-in flow the extension calls on your own API.
