---
name: consent-audit
description: Check that Tag Manager tags respect consent, covering a Consent Mode v2 default on Consent Initialization, consent settings on every ads and analytics tag, vendor pixels, and the site-side region logic. Use when the user says "consent mode", "GDPR/cookie banner check", "are tags respecting consent", "Consent Mode v2", "cookie consent audit", or before running ads to opt-in regions.
---

# Consent audit

Tags that fire before or without consent break the law in opt-in regions and, since Consent Mode v2, lose
remarketing and conversion modelling in Google Ads. This skill reads the container, classifies every tag, checks the
consent default, and gives the user's developers a short checklist for what Tag Manager can't see.

## When to use

- Before advertising to visitors in opt-in regions (for example the EEA and the UK).
- After a new consent banner (CMP), a new vendor pixel, or a `gtm-build` session.
- Ads shows Consent Mode warnings, or remarketing lists stopped growing.

## Inputs

- `account` with `gtmContainerId` set (check with `account_profile`; the `setup` skill adds it).
- The regions the site serves that require opt-in, and the consent banner in use.

## Steps

Call `account_profile` first. Consent rules: `guide("measurement")`; tag recipes and the publish checklist:
`guide("gtm")`.

1. **Inventory.** `gtm_list` with `entity: "tags"`, then `gtm_get` on every active tag for its `type`,
   `firingTriggerId` and `consentSettings`. Classify:
   - `awct` (Ads conversion), `sp` (Ads remarketing), `gclidw` (conversion linker): ads tags. All need
     `ad_storage`; conversion and remarketing tags also `ad_user_data`, remarketing also `ad_personalization`.
   - `googtag` (Google tag), `gaawe` (GA4 event): analytics tags, need `analytics_storage`.
   - `html`, `img` and community templates that load vendor pixels (social, affiliate, heatmap, chat): read their
     code; ad pixels need the ads types, analytics tools `analytics_storage`.
   - Google tags (`awct`, `sp`, `gclidw`, `googtag`, `gaawe`) read Consent Mode themselves: with a correct default
     they send cookieless signals while denied (advanced mode). Requiring consent on them (`consentStatus: "needed"`)
     blocks them fully (basic mode). Both are valid; it's the user's legal choice. Non-Google tags have no built-in
     check: `consentStatus` `notSet` or `notNeeded` on them means they fire regardless.
2. **Consent default.** Look for a tag that fires on the Consent Initialization trigger (built-in trigger ID
   `2147479572` in `firingTriggerId`): the CMP's template or a Consent Mode template. With `gtm_get`, check that it:
   - sets a default for all four Consent Mode v2 types: `ad_storage`, `analytics_storage`, `ad_user_data`,
     `ad_personalization`;
   - defaults to denied in opt-in regions (a region list on the default, or denied everywhere);
   - updates consent when the visitor chooses (the CMP's update call), and the banner itself loads.
   No such tag means either the site sets the default in code before the GTM snippet (ask the developers to confirm,
   step 4) or there is no default at all, which is a high finding. Only consent and CMP tags belong on Consent
   Initialization.
3. **Findings.** Table with severity, tag, type, current `consentSettings`, problem, fix:
   - **high**: no consent default; a vendor ad pixel with `notSet`/`notNeeded`; a tag on Consent Initialization or
     All Pages that sets cookies before the default; `ad_user_data` / `ad_personalization` missing from the default.
   - **medium**: Google tags in basic vs advanced mode not matching what the user intends; custom HTML that injects
     `gtag()` consent calls outside the CMP; `<noscript>` image pixels in the page source.
   - **low**: consent settings on tags that are paused anyway.
4. **Developer checklist** (what the container can't show):
   - The consent default runs before any tag: the GTM snippet or the in-code default comes first in `<head>`.
   - Region gate fails closed: grant only on an explicitly allowed region, never `region !== "<restricted>"`; an
     unknown or failed lookup means denied, and a guessed region is never persisted (cookie or storage).
   - `<noscript>` pixels can't be consent-gated: remove them in consent regions.
   - Vendor pixels hard-coded in the site move into Tag Manager so they inherit the consent gate.
   - The banner's choice reaches Tag Manager as a consent update (check in Tag Assistant's Consent tab).
5. **Fixes**, each a preview first and applied only after a yes:
   - Consent on an existing tag, recipe-built or not: always `gtm_upsert` with `entity: "tags"`, `id`, and only
     `consentSettings` in `resource` (the shallow merge keeps its parameters and triggers). Never `gtm_build` with an
     `id` for a consent change: an update replaces every setting the recipe doesn't model.
   - Types per tag: GA4 event tags (`gaawe`) need `analytics_storage`; Ads conversion tags (`awct`) need
     `ad_storage` and `ad_user_data`, plus `ad_personalization` when they feed remarketing. For an Ads tag:
     `resource: { consentSettings: { consentStatus: "needed", consentType: { type: "list", list: [{ type: "template", value: "ad_storage" }, { type: "template", value: "ad_user_data" }] } } }`.
   - A missing consent default: install the CMP's Tag Manager template on Consent Initialization (community
     templates are added in the Tag Manager interface), then configure it with `gtm_upsert`.
   - Review and publish as in the `gtm-build` skill: `gtm_versions` with `versionId: "workspace"` shown in full,
     `gtm_publish` with a dated name after a yes, rollback version noted, then `gtm_live_check`.

## Output

1. The tag inventory with classification and consent status.
2. The consent-default check (present / missing, types covered, region behaviour).
3. The findings table and the fixes applied (change IDs, published version).
4. The developer checklist.
5. The closing line: "This is a technical check, not legal advice."

## Never

- Never present the result as legal compliance; always close with "This is a technical check, not legal advice."
- Never grant consent by default in an opt-in region, or suggest region logic that fails open.
- Never remove or pause the consent banner's own tags.
- Never publish without showing the workspace diff and getting a yes.
- If the profile is read-only (no write tools), deliver steps 1–4 and tell the user that fixing needs
  `npx google-marketing-agent accounts set <alias> writes true` and an MCP client restart.
