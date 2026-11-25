---
name: stack-integration-playbook
description: Composition authority for the web-stack catalog — skills into ONE site, the site into the stack, and the recipes. Use when composing multiple skills, picking a brief's subset or archetype recipe, sequencing a full build, capturing leads, measuring the site, speeding up navigation, or drafting the privacy notice. Trigger on build the full site, in what order do I apply these skills, wire the stack together, which skills for a landing page, add a contact form, add analytics, track conversions, measure leads or real-user vitals, prefetch links, speculation rules, aviso de privacidad, or privacy notice template. Provides the canonical order, the seams, the stack map, and the recipes — forms, analytics, prefetching, legal, archetypes. Not for single capabilities — CSP goes to web-security-headers, CI gates to perf-ci-gates, A/B and redirects to edge-logic, external data to data-layer, every other capability to its owning skill; client intake and writing the site brief go upstream to client-discovery.
---

# stack-integration-playbook

> How the skills of the web-stack catalog compose into one real site, in what order, across which seams, and how that site connects to the rest of the stack (data, CI, deploys, secrets). Every claim here is field substance from the first composed build — the Furever integration fixture (8 skills, both CI gates green with active assertions, live branch-preview deploy, 2026-08-17) — not theory.

## Reference materials — load when relevant

This SKILL.md is the composition order and the omission rules. Load references only when their content is needed:

- `references/seams-and-gotchas.md` — load when wiring two or more skills together, when a composed build fails in a way no single skill explains, or when reviewing a composed site before shipping. The numbered cross-cutting seams with their field-proven failure modes.
- `references/stack-integration-map.md` — load when the site must touch anything beyond the web layer: external data, CI secrets, deploys, rebuild triggers, email, analytics.
- `references/recipes.md` — load when starting a new site composition (pick the closest archetype recipe — brand-heavy proven, lead-gen landing, catalog with self-edit, editorial/story), when a brief item smells like a customer portal (the client-portal frontier lives there), or when documenting a finished composition as a new recipe.
- `references/forms-lead-recipe.md` — load when the site needs a contact form or lead capture: the one-route native architecture (Astro Action + Turnstile + Supabase insert-only + native email + LFPDPPP consent), its knobs, gate amendments, and the flip conditions that would promote it to a skill.
- `references/analytics-recipe.md` — load when the site needs analytics, conversion tracking, or measurement: the events-layer architecture (Umami + attribute events + the server-side conversion event from the Action + exact CSP additions + env-gating + the aviso paragraph), the merit map with measured script weights, the GA4 tombstone, and the promotion triggers.
- `references/speculation-recipe.md` — load when speeding up navigation: Astro's stable prefetch as the default, manual Speculation Rules prerender as Chromium-only escalation with the MANDATORY analytics guard, why experimental.clientPrerender is not taught, and why Speed Brain does not apply to Worker-served routes.
- `references/legal-recipe.md` — load when the site needs an aviso de privacidad or a legal-compliance pass: the template with slots (TEMPLATE, NOT ADVICE — owner/lawyer-gated), the verified 2025 LFPDPPP frame, the short-notice-at-collection pattern, the no-banner posture, and the reform review-gates.

## TL;DR

- Compose in the canonical order below; each step consumes artifacts the previous step produced. Skipping a step is fine (Lego); reordering is not.
- A site composes the SUBSET its brief needs — no site takes every skill, and at most ONE visual skill per site, brief-justified, never by default.
- The seams between skills are where composed builds fail; the two worst failure modes are silent (a CI gate that asserts nothing, a shader that pegs CPU only on runners). Verify gates by reading their logs, not their color.
- Integration beyond the web (Supabase, Actions, Cloudflare, Infisical) is a map of contact points; the depth lives in the owning skill or a future wave skill.

## The Lego principle

The catalog is not a framework. Every site starts from its brief and pulls in only the skills that earn their place; a new skill widens the catalog's reach, never each site's payload. Three hard rules proven in composition:

- Foundation travels together. A site that ships at all wants tokens + security + perf gates + seo (steps 2–5). Omitting one of these needs a stated reason (an internal tool may skip seo; a prototype may skip gates — but then it is a prototype, not a deliverable).
- One visual skill maximum (motion-system reveals do not count as the visual — the visual is webgl-atmosfera OR signature-anim). Choose it from evidence in the brief or brand canon, not taste: the fixture chose WebGL because the canon carried an atmosphere-composition rule and no .riv asset existed — fabricating one would have violated owner-decides.
- Brand presence decides the entry point. A brand repo emitted under the interchange contract → start at step 1 (brand-canon-ingest). A plain tokens.json or no token source → skip step 1, start at step 2 (astro-css-tokens owns that path).

## Canonical composition order

Proven end-to-end on the fixture. Each row states the dependency that pins its position and when it can be omitted.

| # | Skill | Why it sits here | Omit when |
|---|---|---|---|
| 1 | brand-canon-ingest | Produces everything downstream consumes — token source, schemes.css, exact-file assets, fonts, provenance manifest. Runs the brand's own gate board as precondition, so a broken canon aborts before the site exists | No brand repo (plain tokens.json → start at 2) |
| 2 | astro-css-tokens | Compiles the token source (from 1 or standalone) into CSS vars + Tailwind theme; every later step styles against these vars | Never, if the site has any styling — this is the floor |
| 3 | web-security-headers | CSP must exist BEFORE features accrete: retrofitting hashes onto a built site is an audit; building under CSP is free. Every later skill (motion, visual, cms, JSON-LD) has a CSP clause | Rarely — an internal prototype behind auth |
| 4 | perf-ci-gates | Gates watch every subsequent addition; wiring them after the visual layer means discovering budget overruns at the end instead of per-commit | Prototype-only work with no CI |
| 5 | seo-aeo-schema | Needs the layout head (2) and CSP posture (3) settled; JSON-LD is CSP-exempt but the head component composes with the no-flash script hash | Sites that must not index (internal tools, gated apps) |
| 6 | motion-system | Consumes tokens (durations, easings from 2) and CSP (bundled-script hashes from 3); its budget lives under the gates (4) | Static-feel brief |
| 7 | ONE visual (webgl-atmosfera OR signature-anim) | The heaviest, riskiest layer goes in LAST among visuals, after gates exist to catch its cost; consumes token/scheme colors (1–2), CSP (3), budget (4), reduced-motion posture (6) | Brief does not justify it — the default is zero visual skills |
| 8 | cms-self-edit | Wraps content that already renders; its admin app-shell needs the _headers detach (3) and exclusion from the audited set (4) — both exist by now | Content is developer-edited |

The order is a dependency chain, not a ritual: 1 feeds 2, 2–3 feed everything, 4 must precede anything with a byte cost, 7 is last because it is the most likely to be cut when gates push back.

## Verification discipline for composed builds

Composition creates failure modes no single skill owns; these habits caught every one on the fixture:

- A green CI job is not evidence. Open the Lighthouse job log and confirm "Checking assertions against N URL(s)" ran, and that N is the page count you meant to audit. The assert step can crash, be swallowed by the action wrapper, and report green having asserted nothing (seam 4 in the seams reference).
- Verify the deployed artifact, not the local build: curl the live preview for the real header set (concatenated duplicates only appear there), the CSP meta, and the immutable cache header on hashed assets.
- Provenance is byte-exact or it is nothing: after ingest, re-hash the vendored files against the manifest; a formatter that touched one generated file breaks the chain silently (seam 8).
- Anything decorative that can fall back must be exercised in its fallback state at least once (kill the WebGL context, check the tokens gradient stands).

## Limitations and out-of-scope

- This skill does NOT own any single capability — each row of the order table has an owning skill; go there for setup, config shapes, and per-tool gotchas.
- Recipes carry two statuses stated in their headers: PROVEN (recipe 1, the brand-heavy fixture) and DERIVED (lead-gen landing, catalog with self-edit, editorial/story — every ingredient field-proven, the whole awaiting its first dedicated build). The skeleton in `references/recipes.md` is the contract for the next ones; the client-portal frontier documented there is a boundary, deliberately not a recipe.
- Every capability in the catalog has an owner as of v2; the map's remaining frontier entries (customer portals) are boundaries by decision, not gaps awaiting waves.
- The brief this playbook composes FROM is produced upstream by client-discovery (intake, capture, feasibility verdicts, deferrals); this playbook owns the feasibility FACTS that skill's verdicts cite.
- Nothing here is project-specific: accounts, IDs, and endpoints belong in the consuming project's own docs.
