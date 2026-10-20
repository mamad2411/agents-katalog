---
name: apc-website-factory
description: Run the APC-only celebrant website factory from source-bounded intake through local build, independent QA, approved collateral, provider handover, and evidence-backed sign-off. Use as the front door for a new Academy of Professional Celebrants celebrant website.
---

# APC Website Factory

This is the operating front door for a new Academy of Professional Celebrants (APC) celebrant website. It coordinates the full starter pack; it is not a thin shortcut to a generic template.

Read [`agents/router.md`](agents/router.md) first to select the stage, then read [`references/factory-operating-guide.md`](references/factory-operating-guide.md) in full before dispatching work. The router is compact by design; the guide defines the mandatory preflight, client pack, lane contract, approval gates, provider split, secret handling, proof standard, and final handover.

## First response

State only what is known:

- the client name and intake source;
- the intended local project path or the existing project path;
- the current gate and its missing facts, if any;
- the next local action; and
- the external actions that remain approval-gated.

Require a client/celebrant name and an intake source. If either is absent, ask one precise question. Do not infer a client repository, a domain, an email address, a credential, a testimonial, a qualification, or an approval.

## Mandatory read order

1. This skill's [factory operating guide](references/factory-operating-guide.md).
2. `/Users/jack/.agents/skills/apc-new-website/SKILL.md` for bootstrap, project-pack conventions, and delivery detail.
3. `Skills/celebrant-website-guidelines.md` for mandatory APC policy. It wins over generic/template guidance.
4. `/Users/jack/.agents/skills/apc-new-website/references/brand-media-and-email.md` before choosing logo, stills, video, or form-email work.
5. The project's `AGENTS.md`, intake, canonical docs, and current approval record.

`Skills/AI_WEBSITE_SYSTEM_GUIDE.md` is useful for structural, config-first architecture only. It does not prescribe client visual style and cannot override the celebrant guidelines, locked brief, or creative direction.

## Operating rules

- One Lead Agent owns scope, gates, dispatch, integration, conflicts, and the final evidence pack.
- The Builder alone changes website application source. Specialists may change only their declared assets, records, evidence, or implementation requests. Critics are read-only.
- A supplied client document is the source of factual truth. Expand only safe narrative framing; never invent facts, prices, credentials, testimonials, contact details, locations, domains, availability, third-party rights, or provider state.
- Treat images deliberately supplied by the client in their named website intake as authorised for use on that website. Record them as client-supplied and use them when technically and editorially suitable. A missing standalone rights statement is not a reason to omit them, replace them, or describe them as rights-blocked. Pause only for concrete contrary evidence, such as an explicit restriction, a watermark or licence conflict, an unclear source outside the client intake, or a specific privacy concern.
- Start from a bespoke `creative-direction.md` and one Codex Imagen Home-page anchor mock-up. The mock-up is an art-direction north star, not a pixel-perfect source or a substitute for real responsive implementation.
- Use deliberately original, personality-led work: strong backgrounds, broken grids, layered/asymmetric composition, visible motion, micro-interactions, purposeful parallax, and a video-led hero where a rights-safe clip serves the concept.
- Reusable mechanics are welcome: configurable video/poster/fallback handling, transform-based parallax, shared reveal primitives, responsive media focal points, component patterns, and intentional gradient techniques. Never reuse a prior client's composition, copy, identity, assets, exact palette, or provider configuration.
- Gradients are a design material, not a default skin. Use independently conceived tonal, radial, mesh, duotone, or contrast gradients where they improve mood, hierarchy, or legibility; do not reproduce another site's gradient composition.
- Keep native browser scrolling. Build readable text, working controls/forms, mobile stability, media fallbacks, and a low-cost reduced-motion path without flattening the visual idea.
- Do not deploy, publish, change DNS/email, create a mailbox, activate FormSubmit, upload to Drive, spend money, contact anyone, or retrieve/use provider credentials without Jack's exact approval of the present action.

## Start sequence

1. Create or reconcile the local project pack using `apc-new-website`.
2. Run the APC preflight and lock the brief/source reconciliation.
3. Create the creative direction and anchor mock-up, then dispatch non-overlapping Content and Asset & Media lanes.
4. Build locally, then run the independent Visual, Technical, and Integration Critics against rendered evidence.
5. Obtain website approval before starting collateral; obtain exact approval again for each provider action.
6. Route Cloudflare deployment/domain work, cPanel/FormSubmit email work, and Drive archival work to their separate specialist lanes. Collect live readback before claiming handover.

## Authority boundaries

- `cloudflare-deploy` (and the Cloudflare plugin when available) is the deployment/domain capability. It is not proof of mailbox delivery, FormSubmit activation, Drive upload, or completed handover.
- `cpanel-cloudflare-formsubmit-email-setup` is authoritative for cPanel mailbox creation, mail DNS, FormSubmit wiring/activation, and end-to-end enquiry delivery. The factory does not duplicate that procedure.
- `apc-drive-pdf-upload-archive` is authoritative for collateral cloud archival and readback.
- `celebrant-cloudflare` is a legacy reference only. Do not use its embedded webhook, Slack-post instruction, or broad email-routing instruction. Follow the operating guide's current provider split instead.

## Completion

Do not call a project handed over because it builds locally or because one deployment URL responds. Completion requires reviewable canonical documents, client-approved website state, local QA evidence, collateral evidence when requested, separately approved provider actions, current provider readbacks, archive proof, and final sign-off.
