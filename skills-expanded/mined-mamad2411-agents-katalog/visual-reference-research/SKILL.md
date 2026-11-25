---
name: visual-reference-research
description: Autonomously research visual references through Browser Harness and turn them into a dated, traceable reference brief. Use before designing interfaces, websites, campaigns, decks, videos, or visual assets when the direction needs evidence or inspiration.
---

# Visual Reference Research

Build a focused reference brief before committing to a visual direction. This is research, not permission to copy a composition, brand, or asset.

Stamp every brief with the current `YYYY-MM`. Separate the user's primary reference from a small contemporary market set. The primary reference defines the requested direction; the market set—normally two or three directly relevant examples—tests whether that direction still reaches paid-quality expectations in the current month. A reference can be visually strong and still be incomplete by current standards.

## Route through the local library

When available on the current workstation, open `file:///C:/Users/jomor/Desktop/refe%20webfonts/index.html` with Browser Harness and treat it as an optional routing catalog. The workflow must also work without this local index.

Browser Harness (the `blop-browser` CLI) is required for this workflow. Use it to open the catalog and every reference page, take a semantic snapshot before acting, interact through returned element references, and take a fresh snapshot after navigation. Do not replace it with Playwright, Chrome DevTools, generic web search, raw HTTP fetching, or a shell-launched browser. If Browser Harness is unavailable, stop the research stage, report the missing capability, and do not select or claim references from an unobserved interface. Keep research read-only unless the user authorizes an external action.

For a visible desktop session, first maximize the physical Browser Harness window, then query or set the largest useful viewport before judging composition (`1920×1080` on the current Oruka workstation). Window maximization and viewport sizing are separate mandatory checks. If Harness lacks a maximize action, the host OS window API may only maximize the identified Harness-owned window; browsing and evidence capture remain in Harness. A non-maximized visible window invalidates reference selection. A homepage is not inspected from its first frame alone. Capture the initial viewport and a full-page overview, then traverse from header to footer with semantic scroll or keyboard actions. At every material composition transition, take a fresh snapshot and screenshot. For each section with motion or layout change, capture at least two screenshots at the same viewport—entry/before and settled/after—separated by a recorded time interval or semantic action. Compare position, opacity, scale, clipping, active state, and z-order; one static screenshot never proves motion. Inspect hover, focus, sticky, reveal, parallax, ticker, carousel, and scroll-linked states when present; never infer motion from a static screenshot.

Build an element inventory for every serious candidate: page zones, navigation behavior, hero mechanism, product proof, unique visual device, CTA pattern, section transitions, background and surface changes, typography roles, recurring components, interaction states, scroll choreography, and footer resolution. Use Browser Harness text/attribute extraction when it adds evidence, but do not copy third-party source code or assets. A reference cannot be selected as the primary direction until this walkthrough and inventory are complete.

## Choose sources by job

- Savee: art direction, imagery language, editorial composition, and moodboards.
- Refero: real product screens, interaction patterns, and complete flows. Prefer its MCP search when configured.
- 21st.dev or Aceternity UI: implementation-ready React, Tailwind, shadcn, and motion primitives. Free and paid items coexist; do not incur cost.
- Openverse: openly licensed image or audio candidates. Verify the work's source license and attribution before use.
- The local catalog's specialist sources: typography, icons, color, illustration, web galleries, or UI flows when those are the actual need.

Mobbin, premium libraries, account creation, credit consumption, and paid downloads are never automatic fallbacks. Search-result thumbnails and inspirational images are references, not deliverable assets.

## Produce the brief

Collect a small diverse set of direct URLs, normally three to seven. For each, record what it contributes and whether it is inspiration, an implementation primitive, or a licensable asset candidate. Extract a coherent matrix covering:

- layout and information hierarchy;
- typography and spacing rhythm;
- palette, contrast, and surface treatment;
- imagery, iconography, and texture;
- motion and interaction behavior;
- patterns to avoid.

Synthesize the shared principles and deliberate exceptions into one reference brief. Do not assemble a Frankenstein design from isolated details. Include the search terms, platforms consulted, direct URLs, provenance or license status, and unresolved access limitations.

End the brief with two explicit sections:

- **Reference floor:** the mechanisms the result must reproduce or exceed.
- **Opportunity to win:** missing proof, content, responsiveness, accessibility, interaction, motion, or narrative that could make the result better. Every proposed addition needs an observable job; novelty and extra animation are not value by themselves.

Hand the brief to `design-loop`. Send actual image, icon, illustration, texture, audio, or video needs to `visual-assets`; a reference alone is not an asset source.
