---
name: i18n-system
description: Make an Astro 7 site on Cloudflare Workers Static Assets multi-language with core i18n routing — default locale at the root, prefixed secondary locales, a typed zero-dependency UI-string dictionary, localized content collections matching Sveltia CMS i18n structures, and hreflang alternate links with x-default. Use when adding a second language, translating a site, setting up locale routing or a language switcher, localizing content collections or CMS entries, or choosing an i18n library. Trigger on multi-language site, add Spanish and English versions, translate my Astro site, locale routing, language switcher, localized blog content, or hreflang. Explains why language detection and redirects are absent on a static Worker, why the sitemap i18n option is not the hreflang answer, and why astro-i18next and paraglide-astro are do-not-install. Not for the head component that renders the links (seo-aeo-schema), client editing setup (cms-self-edit), or composition (stack-integration-playbook).
---

# i18n-system

> Multi-language on this stack is Astro CORE i18n plus zero dependencies: the default locale lives at the root, secondary locales under a prefix, UI strings in one typed dictionary module, localized content in per-locale folders that Sveltia understands natively, and hreflang emitted as head links from the locale map. Every popular add-on library for this job is either dead, deprecated, or built for an SSR shape this stack deliberately avoids.

## Reference materials — load when relevant

This SKILL.md is the verdict and the five locked decisions. Load references only when their content is needed:

- `references/routing-and-urls.md` — load when configuring `i18n` in astro.config, structuring `src/pages` per locale, building the language switcher, or handling fallbacks and localized 404s.
- `references/ui-strings-dictionary.md` — load when wiring interface strings: the typed zero-dep dictionary, the Sveltia single_file data collection as an editorial knob, and the Paraglide escalation with its threshold.
- `references/localized-collections.md` — load when localizing markdown or data content: the multiple_folders layout shared by Astro and Sveltia, canonical_slug linking, and partial-translation honesty.
- `references/hreflang-and-detection.md` — load when emitting hreflang alternates (the seam with seo-aeo-schema) or when a brief asks for automatic language detection or redirects.

## Verdict

Astro's built-in `i18n` config is the entire routing layer — no integration, no library, no middleware. The default locale (this stack's briefs are usually es-MX) stays at the URL root and secondary locales get a path prefix (`prefixDefaultLocale: false`), so a site that adds a language keeps every existing URL. UI strings live in ONE typed dictionary module with zero runtime dependencies. Localized content collections use a folder per locale — the exact layout Sveltia CMS treats as first-class, so the site and the CMS agree on disk with no adapter. hreflang alternates, including `x-default`, are emitted as `link` elements in the head from Astro's locale-URL helpers — the map is this skill's; the head surface that renders it belongs to seo-aeo-schema. There is NO automatic language detection or redirect by default: on a static Worker every detection mechanism either does not run, costs money per hit, or does not exist on the Free plan.

## The five locked decisions

| # | Decision | Rule | Escalate or flip when |
|---|---|---|---|
| i1 | Routing | `prefixDefaultLocale: false` — default locale at root, others prefixed (`/en/…`) | The brand demands symmetric URLs, or 3+ locales with future detection needs |
| i2 | UI strings | Typed zero-dep dictionary module (the pattern Astro's own docs teach); optionally fed from a Sveltia single_file data collection so a client can edit strings | Beyond ~200 keys, heavy plurals or interpolation, or a translator workflow — escalate to Paraglide, never astro-i18next |
| i3 | Content | multiple_folders for markdown collections + single_file for data and strings | Preference for multiple_root_folders (also maps cleanly to both systems) |
| i4 | Detection | NONE — no server redirect, no Worker logic, no edge rule; an optional client-side banner is the ceiling | The site already ships a Worker `main` for another reason — then a 302 with a cookie and bot exemption becomes affordable (see the reference) |
| i5 | hreflang | Head `link rel=alternate hreflang` elements from `getAbsoluteLocaleUrlList()`, plus `x-default` pointing at the default locale — rendered by the seo-aeo-schema head component | A locale gains its own domain (out of scope on this adapter — see gotchas) |

## Gotchas that kill naive setups (verified)

- `i18n.domains` (locale-per-domain) is unusable on this stack — it requires `output: "server"` with ZERO prerendered pages (dedicated error `NoPrerenderedRoutesWithDomains`) and only the node or vercel adapters support it. Locale-per-domain here means separate deployments; treat any tutorial wiring `domains` as inapplicable.
- Browser-language detection via `Astro.preferredLocale` / `Astro.currentLocale` negotiation only exists ON-DEMAND (server-rendered routes). On a prerendered site those APIs cannot see the visitor. This is why i4 is NONE, not an oversight.
- Cloudflare cannot rescue detection cheaply either — the `accepted_languages` field exists only in Transform Rules (request header rewrites), NOT in Redirect Rules; Snippets are unavailable on the Free plan (quota 0). A Worker-based redirect turns every root hit into a billable invocation.
- `@astrojs/sitemap`'s `i18n` option emits `xhtml:link` alternates WITHOUT `x-default`, and its behavior on partially translated sites is undocumented (risk of alternates pointing at 404s). The head-link route is exact per page and supports x-default — that is why i5 lives in the head.
- Emit alternates ONLY for pages that exist in both locales. A page without a translation gets no hreflang block at all — an alternate to a 404 is worse than none.
- Fallback rendering (`i18n.fallback`) ships the DEFAULT locale's content under the secondary locale's URL. Use it consciously as a launch bridge, never as the permanent state — and never emit hreflang for a fallback-rendered page as if it were translated.

## Do-not-install tombstones

- `astro-i18next` — abandoned in beta (last publish 2023, still 1.0.0-beta.x). Most-linked tutorial result, dead in practice.
- `@inlang/paraglide-astro` — DEPRECATED by inlang; superseded by using `@inlang/paraglide-js` directly via its Vite plugin.

## Brand-voice boundary

A brand canon under the interchange contract defines voice as locale-bound rules (this stack's flagship contract is es-MX only). A second locale's copy is NOT a mechanical translation: fabricating brand voice in a new language is an owner decision, not a build step. Fixtures and staging mark secondary-locale copy as visible placeholders; a real launch waits for owner-ratified copy. Multi-locale voice tokens would be an upstream contract change, not a site-side workaround.

## Pins (verified 2026-08-17) and review-gates

| Pin | Value | Review-gate |
|---|---|---|
| Astro core i18n | ships with astro 7.2.2 — no package | Re-read the i18n routing section on the next Astro major; `routing` options have churned before |
| `@inlang/paraglide-js` | 2.24.1 (escalation path only — do not install by default) | Re-verify before first real use; its canonical setup assumes SSR middleware, the static-output path must be re-confirmed then |
| `astro-i18next` | do-not-use (1.0.0-beta.x, abandoned) | None — tombstone |
| `@inlang/paraglide-astro` | do-not-use (0.4.x, deprecated upstream) | None — tombstone |

## Limitations and out-of-scope

- Translation itself (who writes the words, machine translation policy, translator workflows) is an editorial process; this skill wires structure, not language.
- RTL locales add a layout dimension (logical properties, direction flips) this skill does not cover; treat an RTL brief as new scoping, not a routing tweak.
- The head component that renders hreflang links, canonical, and OG tags is seo-aeo-schema's surface — this skill only defines the locale-URL map it consumes.
- CMS editor setup, auth, and media are cms-self-edit; this skill only fixes the on-disk i18n structure both sides share.
