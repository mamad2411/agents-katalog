---
name: site-planner
description: Plans a scroll-driven 3D website before any generation happens — decides section structure, content depth, and 3D treatment based on the product itself, or clones the structure/effects/positioning of a reference site if one is provided. Hands off a structured site plan to whichever technique skills (video-scroll-effect, 3d-scene-effect, pointer-follow-effect, click-navigate, physics-play, hybrid-2d3d, cursor-trail, and any others installed) own each section. Use this BEFORE those skills when the user gives a brief for a new 3D scroll site — this is the planning step, not the builder.
---

# Site-Planner — plans the site before anything gets built

## What this does
Two very different jobs live here, chosen by whether the user supplied a reference site:

**No reference given → reason from the product.** Don't default to a fixed template.
Figure out what THIS specific product actually needs to sell itself, and let that
determine section count, content depth, and 3D treatment — not a lookup table.

**Reference given → clone structure, not content.** Fetch the reference site, extract
its section structure, positioning, and visual/motion language. Reuse all of that.
Generate fresh content and copy for the new product — never reuse the reference's
actual text or pixel-perfect specifics.

## Step 0 — Intake (one batched turn, before anything else)
Before planning, ask for whatever the user's original brief didn't already answer —
batched into ONE turn, not asked one at a time:
1. **Site type/purpose**: informational | marketing/commercial | ecommerce/product-sales
   | portfolio | event/launch | other (free text).
2. **Product/theme**, if not already clear from the brief.
3. **Any must-have pages/sections** (optional — the director still reasons about what's
   needed beyond whatever the user lists here; this is a floor, not a ceiling).
4. **Reference URL**, if any — this absorbs what used to be a separate Step 1 check
   into the same batch, since we're already asking multiple things up front.
Skip any question the brief already answered plainly — don't re-ask what's already
known. If the `AskUserQuestion` tool is available in this environment, use it to
present these as structured choices; otherwise ask as a short numbered list in one
chat message. This is the only intake stop — once answered, move straight to planning
(Step 2a/2b) without further back-and-forth until the Step 2c review.

## Step 1 — Route by reference URL
- If Step 0 surfaced a URL to reference/clone: go to "Reference-site mode."
- If not: go to "Creative mode."

## Step 2a — Creative mode (no reference)
Reason about the specific product, not its category alone — informed by Step 0's
answers (site type, product/theme, any must-have pages):
- What does someone actually need to know before buying/using THIS thing?
  A car needs specs, trims, maybe safety ratings. A single-origin coffee needs
  origin story, roast profile, maybe brewing guidance. A dev tool needs feature
  breakdown, maybe a pricing tier comparison. Let the answer drive section count —
  don't force every site into the same number of sections.
- Let the site TYPE from Step 0 shape structure, not just content: an ecommerce site
  needs product/pricing sections and a clear path to purchase; a portfolio needs a
  work-index and contact; an informational site can lean more editorial
  (`hybrid-2d3d`-heavy) and less spectacle-heavy; a marketing/launch site earns the
  most full-bleed cinematic/world real estate.
- Fold in any must-have pages from Step 0 as required sections, then add whatever else
  the product itself needs beyond that floor.
- Pick 3D treatment(s) freely among the *implemented* techniques (see "Available
  techniques" below) — not from a rigid one-technique-per-site rule. Different
  sections of the same site can and should use different treatments (e.g.
  photorealistic frame-scrub hero + procedural 3d-scene-effect feature section +
  a pointer-follow-effect showcase section) so similar briefs don't all produce the
  same skeleton.
- Avoid repeating the same structure/treatment choice on every run for similar
  briefs — vary defensible details so two similar briefs don't produce identical
  skeletons.
- Output a site plan (see "Site plan format" below).

## Step 2b — Reference-site mode
- Fetch the reference URL with `web_fetch`.
- Extract from the returned content: section types and their order, layout/
  positioning patterns, color palette (from inline styles/CSS if visible), any
  detectable motion/scroll effects, and general content tone — but not the
  actual copy/text itself.
- If `web_fetch` fails or returns unusable content (e.g. JS-rendered site with
  no meaningful HTML): tell the user plainly, ask whether to retry with a
  different URL or proceed in creative mode instead. Never silently fall back.
- Map the reference's effects to available techniques (video-scroll-effect for
  frame-scrub video, 3d-scene-effect for scroll-driven procedural 3D, pointer-follow-effect
  for cursor-reactive hero/showcase moments, click-navigate for a hotspot/product-tour
  feel, physics-play for a playful draggable-objects moment, hybrid-2d3d for an
  editorial/content-dense section, cursor-trail for an atmospheric/brand moment) —
  approximate, don't require an exact technical match to whatever the reference
  actually uses.
- Output a site plan using the reference's structure/style, with content
  generated fresh for the new product.

## Available techniques
The `technique` field is a list, not a fixed set — new techniques get added
here as they're implemented as skills. Currently implemented:
- **`video-scroll-effect`** — canvas frame-scrub video, driven by scroll progress.
  Best for photorealistic/cinematic subjects where real footage sells it. Supports a
  single `motion` (orbit/turntable, fly-through, reveal/explode, abstract, plus the
  richer named set in its own SKILL.md: molten-birth, frozen-time, bloom, descent,
  light-reveal) or an optional multi-`beats` chaptered scrub within one section — see
  `video-scroll-effect/SKILL.md` for the full pattern table and `beats`/`loopBack` format.
- **`3d-scene-effect`** — real-time Three.js scene, camera/geometry driven by
  scroll progress. Best for procedural/abstract subjects, or as a zero-cost
  fallback when only a static image is available (`motion: "image-plane"`).
- **`pointer-follow-effect`** — real-time Three.js scene, camera/geometry driven by
  CURSOR position (scroll still pins the section and drives overlay copy).
  Best for hero/showcase sections where desktop delight is a bonus — touch
  devices get a static fallback pose, so don't route mobile-essential content
  here exclusively.
- **`click-navigate`** — real-time Three.js scene with clickable hotspots that
  tween the camera to named waypoints. Best for a "tour a few angles/features"
  moment (showroom feel); works identically on touch and desktop.
- **`physics-play`** — real-time Three.js + cannon-es rigid-body objects the
  visitor can drag and throw on a floor plane. The most interactive technique
  and the heaviest to render — use at most one per site.
- **`hybrid-2d3d`** — flat editorial layout (real headline/paragraph/stats,
  normal document flow, NOT pinned) with a smaller inline auto-rotating 3D
  object. Best for content-dense sections, or to break up a site that would
  otherwise be wall-to-wall full-bleed sections.
- **`cursor-trail`** — canvas-2D particle trail following the cursor, scroll
  still drives the overlay copy. Atmospheric/brand-mood technique, not a
  product-showcase one — content shouldn't depend on the trail itself since
  it degrades to ambient drift on touch/reduced-motion.
Only pick from this list — see "Known gotchas" below for what to do if none fit.

## Site plan format
- `sections` length and `type` values are NOT fixed — decide per Step 2a/2b.
- Each section's `technique` decides which skill builds it — one of the
  "Available techniques" above.

{
"brand": "...",
"palette": { "accent": "#...", "bg": "#...", ... },
"sections": [
{ "type": "hero", "id": "hero", "nav_label": "Home", "technique": "video-scroll-effect", "motion": "orbit", "content_brief": "..." },
{ "type": "specs", "id": "specs", "nav_label": "Specs", "technique": "3d-scene-effect", "motion": "procedural-morph", "content_brief": "..." },
{ "type": "showcase", "id": "showcase", "nav_label": "Explore", "technique": "pointer-follow-effect", "motion": "orbit", "content_brief": "..." },
{ "type": "story", "id": "story", "nav_label": "Story", "technique": "hybrid-2d3d", "motion": "abstract", "content_brief": "..." },
...
]
}

- Every section MUST have a stable `id` (kebab-case, used as the `<section id="...">`
  attribute) and a short `nav_label` (1-2 words, what a visitor would click to jump
  there — e.g. "Movement", "Durability", not the internal `type` value verbatim).
  The nav bar is built directly from this list — don't add a section without a
  nav_label, and don't invent nav items that don't correspond to a real section.
- Each section MAY carry a `user_asset` field (a path/reference the user supplied
  during the Step 2c review below) — when present, the executing skill's asset step
  (`asset-generator`) prefers it explicitly over generating anything new for that section.


## Known gotchas
- A "creative" plan still needs to be buildable — don't invent a 3D technique that
  isn't in "Available techniques" above, i.e. doesn't exist as an implemented skill.
- web_fetch may return raw HTML for server-rendered sites but little/nothing useful
  for heavily JS-rendered ones — treat sparse results as a signal to ask the user
  rather than inventing structure from a near-empty fetch.

## Step 2c — Plan review (one combined checkpoint, before any building)
Once Step 2a/2b produce a candidate plan, present it for review BEFORE any
generation/build work starts — this is the only interactive stop between intake and a
finished, deployed site. Show, in one message:
- **Palette** — swatches as hex + a short note on where each is used (accent,
  background, etc.).
- **Page/section list** — nav label, technique, one-line description of what each
  section contains, in order.
- **Per-section asset plan** — which sections will get Higgsfield-generated visuals
  vs. which the user could supply their own image/video for instead. Ask once, here —
  never per-section during the build itself. Anything the user offers becomes that
  section's `user_asset`.
- **Total estimated Higgsfield credit cost** across every section that will need
  generation (this is the same confirmation that credit-spending would otherwise
  require — surfaced here instead of as a separate later stop; see "Before invoking
  video-scroll-effect specifically" below, which this step supersedes as the actual
  confirmation point).
- Ask plainly: "anything to change — palette, page count/order, nav labels, or swap in
  an asset for any section — before I start building?"
Revise and re-show only if the requested changes are substantial (e.g. a different
section altogether); small edits (a color swap, a supplied asset) can just be applied
and confirmed in the same reply. Proceed to Step 3 once the user confirms or has no
further changes.

## Step 3 — Hand off (call directly)
Once the plan is confirmed at Step 2c, invoke each technique skill the plan uses (any
combination of the "Available techniques" above) in the same conversation turn
sequence — no separate command needed, and no further user confirmation between here
and a finished deploy: Step 2c already covered plan approval and credit cost, so
building proceeds straight through once confirmed there.

### Grouping sections by skill
Partition `plan.sections` by their `technique` field — one bucket per distinct
technique value used in the plan (any combination of the 7 in "Available
techniques" above), each bucket's sections in plan order. A single project can
and often will use several of these skills for different sections of the same
page — that's expected, not an error case.

### Routing when only static images are available
If a section has no video source (no Higgsfield access, no user-supplied clip)
and only a static photo is available: route that section to 3d-scene-effect with
`motion: "image-plane"`, NOT to video-scroll-effect. A flat photo has no real
motion for video-scroll-effect's frame-scrub to extract — 3d-scene-effect's
texture-mapped-plane approach produces genuine camera-driven parallax instead,
at zero cost. Only route to video-scroll-effect when real video (generated or
user-supplied) exists. Tell the user this rerouting is happening and why,
rather than silently switching techniques.

### Disclosing plan deviations (mandatory, checked by build-reviewer)
Any section whose ACTUALLY-BUILT technique differs from what Step 2c approved — for
any reason: video generation failed after its one retry, Higgsfield video access
wasn't available, or anything else — MUST appear, by name, under a dedicated
`⚠️ Plan deviations` heading in the final delivery message. This is not optional and
not satisfied by mentioning it in passing inside a longer description sentence — it
needs its own clearly-labeled section so it can't be missed. Each entry states:
- The section name/id.
- Planned technique → actual technique.
- Why (the reason reported by the executing skill, e.g. video-scroll-effect's Step 4
  stop condition).
- Whether credits were spent on the failed/skipped attempt, so the user knows whether
  the credit estimate shown at Step 2c was charged for something that didn't ship.
If zero deviations occurred, omit this section entirely — it only appears when
something actually changed from what was approved. `build-reviewer`'s
`plan_deviations` field (see its own doc) is the enforcement mechanism: read it before
declaring the build done, and relay every entry here verbatim, not paraphrased down to
nothing.

### Routing to pointer-follow-effect
Only route a section to `pointer-follow-effect` if its content still lands
acceptably for visitors on touch devices — that section's 3D motion goes
static on any device without a fine pointer, but its overlay copy still
renders on scroll like normal. Good fits: hero/showcase moments where the
parallax is a bonus, not the only way the section communicates anything.
Avoid it for sections carrying content a mobile-majority audience needs to
actually receive (e.g. core spec/pricing sections) — use 3d-scene-effect or
video-scroll-effect there instead, since those techniques work identically
regardless of pointer capability.

### Routing to physics-play
This is the heaviest technique (WebGL + a physics step every frame) — route at
most one section per site to it, and avoid pairing it on the same page with
several other WebGL-heavy sections (3d-scene-effect, pointer-follow-effect,
click-navigate) unless the target audience is known to be on capable devices.
Good fit: a single playful "try it" moment, not a load-bearing content section.

### Routing to cursor-trail
Same touch/no-pointer caveat as pointer-follow-effect — the trail itself degrades to
ambient drift on devices without a fine pointer or under reduced motion, so
don't make a section's only content dependent on the cursor trail actually
appearing. Good fit: atmospheric/brand-mood sections, section transitions —
not sections carrying product specifics.

### Routing to click-navigate and hybrid-2d3d
Both work identically regardless of device or pointer capability — safe
defaults with no special mobile caveat. `click-navigate` suits a "tour a few
angles/features" moment; `hybrid-2d3d` suits content-dense sections, or
breaking up a site that would otherwise be wall-to-wall full-bleed sections.

### Execution order
1. Invoke the *first* skill needed (whichever owns the first section in `plan.sections`)
   with the full ordered list of sections it owns, plus:
   - `plan.brand`, `plan.palette` (shared across all sections)
   - The connected folder / project slug, so all sections land in the same project
     rather than each skill starting a fresh project directory.
2. That skill builds/generates for each of its sections into the shared project folder
   (per its own SKILL.md — templates copied once, sections appended to
   `SCRUB_SECTIONS`, `WORLD_SECTIONS`, `PARALLAX_SECTIONS`, `EXPLORE_SECTIONS`,
   `PHYSICS_SECTIONS`, `HYBRID_SECTIONS`, or `TRAIL_SECTIONS` as applicable).
3. Invoke each remaining skill the plan uses, in the same way, into the *same*
   project folder — each should find the templates already copied and just add its
   own section-registry entries and `<section>` markup alongside what earlier skills
   already built.
4. Only ONE skill should actually run its deploy step (Step 7/6, depending on the
   skill) — whichever skill owns the LAST section in `plan.sections` runs it, after
   every other skill's generation work is complete. Tell every other invoked skill
   explicitly to skip its own deploy step.

### Building the nav bar
The nav bar is built ONCE, from the full `plan.sections` list, by whichever skill
executes FIRST (before any section-specific work) — not duplicated per section, and
not owned by whichever skill happens to be invoked last. Pass the full ordered list
of `{id, nav_label}` pairs from all sections (regardless of which skill builds that
section) to the first-invoked skill, so nav links can point at sections built by any
of the technique skills on the same page.


### Before invoking video-scroll-effect specifically
Credit-cost confirmation already happened at Step 2c (sum ~54 credits per 1080p clip
across every section needing generation, shown and confirmed there) — don't ask again
here. If a section's `user_asset` was supplied during Step 2c, `video-scroll-effect`
skips generation for it entirely per its own Step 1b.

### If a section's technique doesn't match any implemented skill
This shouldn't happen if Step 2a/2b constrained treatment choices correctly, but if it
does: don't guess or invent an unimplemented technique. Tell the user which section is
unclear and ask whether it should be reassigned to one of the "Available techniques"
listed above.