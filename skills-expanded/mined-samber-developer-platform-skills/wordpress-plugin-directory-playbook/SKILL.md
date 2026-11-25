---
name: wordpress-plugin-directory-playbook
description: >-
  Gets a SaaS vendor's connector plugin approved on the WordPress.org plugin directory and
  kept there - where paid features may live (trialware vs service-side gating), the
  submitting account and permanent slug, the External services disclosure, the review queue,
  SVN tags and the release security review that can block a version, closures and reopening.
  Use whenever a vendor mentions submitting to WordPress.org, a pended plugin review, a
  freemium plugin on WordPress.org, a blocked release or its own closed plugin. Do NOT use
  for themes, plugin PHP code, premium plugins sold only off WordPress.org, listing copy on
  other marketplaces (use
  samber/developer-platform-skills@integration-listing-optimization), or Packagist and npm
  releases (use samber/developer-platform-skills@sdk-package-publishing).
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# WordPress.org plugin directory playbook

You take a vendor's connector plugin (a plugin that talks to the vendor's own service) through WordPress.org review and keep it listed. The volunteer Plugins Team rejects business-model and account choices more often than code: a locked pro feature, an agency's personal account, an undocumented call home. Mark every figure you quote with `†` and one footnote line: "† verify against the current developer.wordpress.org handbook and make.wordpress.org/plugins; the release process changes often."

## Rules the review enforces

1. **No trialware.** Nothing in the plugin is locked, greyed out, time-limited, quota-capped or sandbox-only until payment. Paid value may live in the service (plan, trial and quota enforced server-side, the plugin only displays them) or in an add-on sold outside WordPress.org. An API key that identifies the account to your service is fine; a key that unlocks local code is not.
2. **The service is real and documented.** A service that only validates license keys, code moved server-side to fake a service, or a storefront-only plugin is banned. The readme names each external service: what it is, what data is sent, when, plus terms and privacy links, your own service included.
3. **Consent covers the service only.** Installing and configuring a service plugin consents to calls that deliver that service. Install analytics, telemetry or anything unrelated needs a default-off opt-in.
4. **No remote code in wp-admin.** No iframed admin pages, no JS or CSS unrelated to the service from a CDN (fonts excepted), no updates or installs from your servers, no custom update checker. Your customer-facing widget may load from the service if documented; your admin UI library is not the service and ships in the plugin.
5. **Brand-first names belong to the brand owner.** Submit from the company's own WordPress.org account with a company-domain email. The slug is permanent after approval.
6. **Human contact.** Every committer has 2FA and an email a person reads. Auto-replies that continue after warnings can close every plugin the account owns.
7. **No credits or claims.** "Powered by" links in plugin code default off; output your service renders may carry your brand. Never imply the plugin guarantees GDPR, PCI or ADA compliance; describe what it assists with.

| Rationalization                                             | Why it fails                                                                                                                                                                                                                      |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "The Pro tab is visible but locked; that's just an upsell." | Shipped code disabled behind a license check is trialware. Practitioners report named-but-absent pro features in free code read the same way.                                                                                     |
| "The trial and free quota are counted in the plugin."       | Disabling features after a trial or quota is trialware. Grant the trial and count usage on your service; the plugin shows its answer.                                                                                             |
| "Embed our dashboard in an iframe; it's our own service."   | Guideline 8 bans iframes connecting admin pages. Build the settings screen locally and call your API.                                                                                                                             |
| "Our agency submits it and transfers later."                | A brand plugin from a personal or agency account gets flagged for trademark, and a brand-first slug is blocked for non-owners.                                                                                                    |
| "Submit two weeks before launch, approval takes 14 days."   | No queue jumping except security or legal. The queue has swung between near zero and about 1,050† plugins within months, and most plugins need several review rounds.                                                             |
| "Ping our API on activation to count installs."             | Install analytics is not the service: it needs opt-in. Count connections at OAuth or registration instead.                                                                                                                        |
| "Ship the hotfix and it reaches sites in minutes."          | Every release waits a cooldown of 6 hours† while an automated security review runs. A high score blocks that version; sites keep the previous one until a new release passes, and the listing stays up: a block is not a closure. |

## Interview

Ask one question at a time; skip what the request answers. When you cannot ask, state one assumption per gap and flag it.

1. What does the plugin do inside WordPress, and which parts run in your service versus locally in PHP or JS?
2. Which features are paid, and where is the plan enforced today?
3. Who will submit: which WordPress.org account, which email domain, and does the name start with your brand or someone else's?
4. Stage: not submitted, in review (paste the latest email), live, release blocked, or closed?
5. Launch date, and active installs if live (10,000† changes closure and transfer rules).

Re-rank the menu below against answers 1 and 2, and say which answer moved it: paid features that must run in PHP or JS on the site promote rung 2.

## Where paid value lives

Ranked by efficiency (value per unit of effort), highest first. Value = search reach, one-click install and core auto-updates.

1. **Directory connector, paid features enforced by your service.** One codebase, one review; limits returned by your API and shown as service messages. Default for a SaaS.
2. **Directory plugin plus a premium add-on sold on your site.** The add-on may carry its own updater and needs its own Plugin URI; the free plugin may link to it but never install it or hold its code. Starved by the ranking because it costs a second codebase and licensing; promote it when paid features must run locally inside WordPress.
3. **Self-hosted zip only.** No review, but no directory search or core updates. Use only when the product needs what the directory bans (remote code, iframed admin app).

Compliance cost: 1 and 2 pass review once written this way; any in-plugin lock reopens Guideline 5 on every release.

## Name, account and slug

1. Name the plugin `<Your brand> <job>` if you own the brand; otherwise `<Job> for <Their brand>`. Never start with another brand. Keep "wordpress" and "plugin" out of the slug, and never start the slug with `woo` (use `wc`).
2. Submit from the company account. Reply to the review email to fix a wrong account; never resubmit.
3. Check the slug in the confirmation email: you can change it once before approval, never after. The text domain and main file name must match the final slug.
4. Make every URL in headers and readme live before submitting; a service plugin also needs live terms and privacy pages.

## Submit and get through review

1. Run Plugin Check: an error in its Plugin Repo category blocks the upload. Zip under 10 MB†, no dev folders.
2. Assemble the readme and packet from [references/submission-packet.md](references/submission-packet.md).
3. Submit; only one plugin can be in review per account, and extra accounts to get around it get suspended.
4. Answer each review email in the same thread, fixing every point in one upload. A review still incomplete after 3 months† is rejected: resubmit, then reply in the old thread to continue it.
5. Plan the launch backward from the first review plus several fix rounds, each waiting about 10 business days† for a reply. Search lists a new plugin 6 to 14 days† after its first commit. If approval misses the launch, announce "coming to WordPress.org".
6. After approval, push code before launch: an approved plugin with no code for 6 months† can be closed and its name reassigned.

## Release flow

- SVN is a release channel, not your repository: code in `trunk/`, each release copied to `tags/<version>`, images in top-level `assets/`. Keep only the last one or two tags. The plugin goes live on the first commit, with no off switch except closing it.
- Deploy from CI with the account's separate SVN password, never the login password.
- Run Plugin Check, Security category included, before every tag: it also runs on every update you ship.
- Set `Stable tag` to a real tag, never `trunk`. Bump `Version` in the main file for every code change. A readme-only change (Tested up to) needs no version, unless Release Confirmation froze the tag; assets never need one.
- Turn on Release Confirmation. Its 24-hour delay† holds back automatic updates only, on recent WordPress versions.
- Budget the cooldown into every incident timeline. On a blocked release, fix the findings and ship a new version; an appeal by email is slower.

## Stay listed

- Support only the free plugin in WordPress.org forums; send paid-plan questions to your own channel. Opt into the Commercial label by email to get a support URL on the listing. Add support staff as Support Representatives, not committers.
- Never ask for, pay for or seed reviews; employees' conduct closes the owner's plugins.
- Never close to "pause": closing is meant to be permanent, and reopening requires a full current-standards review. Ship a fix, or mark the readme unsupported. Above 10,000† users, closing or transferring takes a written request to the Plugins Team.
- Closed for security: fix, pass Plugin Check's Security category, reply to the closure email.

## Search rank

The ranking code is open source (platform-published; weights change on deploy).

- **Text match:** title and slug weigh most, then author and contributors, then excerpt, description and tags. Only the first five tags count; more than 12 is spam under Guideline 12; never a competitor's name.
- **Multipliers:** active installs (log scale), resolved support-thread share, rating, plus decay after about six months without an update and with a stale Tested up to.
- **Effort order:** target long-tail integration phrases ("<their product> <your category>") > resolve every forum thread > keep Tested up to current > ship real releases. Head terms rarely move away from high-install plugins. Rapid-fire commits to look recent break Guideline 14.

## Output

- **Not submitted**: assumptions; paid-value verdict with the menu rung; name, account and slug; packet checklist with an owner each; timeline with review rounds.
- **In review**: one fix per reviewer point, then the reply.
- **Live, blocked or closed**: the cause, the next release or reply, and the obligations at risk.
- Close with the measure to watch: approval date, then connected sites as a share of active installs, and the resolved-thread share.

## References

- samber/developer-platform-skills@integration-listing-optimization - listing copy, screenshots and conversion across marketplaces.
- samber/developer-platform-skills@sdk-package-publishing - shipping your PHP SDK to Packagist, which the plugin may bundle.
