---
name: ui-screen-audit
description: Reconstructs a UI screen the way a human eye actually perceives it — spatial layout and color first, as the stage everything else is judged against, then typography, information density, container-job fit, tappable elements, and navigation — before recursively descending into every screen it links to. Use whenever asked to review, audit, critique, redesign, or improve an existing UI screen or flow; to check whether a screen feels cluttered, fragmented, incoherent, or "off"; to evaluate button/control placement; or to systematically explore an app's UI across multiple screens or tabs. Trigger even without these exact words — "does this screen work," "why does this feel wrong," "check this design," "is this navigation good" all qualify. Includes risk-tiering guidance for auditing a large screen tree without exhaustively over-auditing every screen at equal depth.
---

# UI Screen Audit — Spatial-First Method

## Why this order, and why it has to be forced deliberately

A human eye perceives a screen's overall spatial composition — the arrangement, the color, the weight of things — before any conscious enumeration of individual elements. This is well-established: Gestalt principles (proximity, similarity, continuity, closure) describe exactly this perceptual grouping, and a published academic critique method, the Critical Design Strategy, explicitly stages evaluation as *overview first* (a holistic first impression) *then detail* (structured, itemized critique) — never the reverse.

Reading source code defaults to the opposite order — sequential, textual, top-to-bottom through the file — which is the natural mode for processing code but is not how a screen is actually experienced. Left unforced, this produces exactly the failure this skill exists to prevent: real problems (redundant controls, fragmented layouts, badge-stacking clutter) hiding in plain sight because each individual element, read in isolation, looks fine. The fix is not more care reading code — it's deliberately inverting the default order: **build the spatial picture first, and only then read for content.**

## An honest limitation, stated plainly

The actual state of the art for AI-based UI evaluation uses real screenshots fed to vision-language models — not source-code reading. When a real screenshot of the running screen is available, prefer it over everything in this skill; look at it the way the method below describes, but look at the real thing. This skill is a principled *workaround* for when no screenshot exists and the only available evidence is source code — genuinely useful, but a lower-fidelity substitute, not the ideal method.

**Also worth internalizing directly: even expert, professional heuristic evaluation is not a one-pass activity.** Nielsen's own research found a single evaluator catches only around 35% of real usability problems in an interface — which is precisely why professional practice uses three to five independent evaluators, never one. Expect this method to require multiple passes to reach real coverage, and treat a single pass as a floor, not a finish line.

---

## The method

### Stage 0 — Canonicality tracing: confirm the full chain before trusting any single file

**A real gap, found in practice, not theorized: multiple files with similar names can plausibly claim to be "the" screen for a given role or feature, and stopping at the first one found — even a real, working one — can mean describing something one layer removed from what's actually live, or worse, something genuinely orphaned.** This happened directly: a hook (`useTeacherDashboardSurfaces`) was traced and audited in full depth before confirming it was actually reachable from the router — it was, but only after tracing *through* a sibling gating layer (`useClassroomWorkspaceSurfaces`) that had gone unnoticed, one level up. A second, similarly-named file (`TeacherClassroomDashboard.tsx`, versus the real `TeacherDashboard.tsx`) turned out to be genuinely orphaned — exported from the package's public surface but referenced nowhere in the live render tree.

**Before Stage 1's spatial reconstruction, trace the complete chain from the confirmed router entry point down to the file under audit, one import at a time, and do not stop at the first plausible-looking match.** For every sibling or similarly-named file encountered along the way — a `useXSurfaces` next to a `useYSurfaces`, a `TeacherDashboard` next to a `TeacherClassroomDashboard` — explicitly check whether it's actually part of the same live chain (just one layer deeper) or a genuine orphan (grep for real external imports of it; an "archives" or "legacy" folder anywhere in the result is a strong, immediate signal). Only once the chain is confirmed complete and the file under audit is confirmed live does Stage 1 begin.

### Stage 1 — Set the stage: spatial layout and color, first, always

Before reading for any content or component identity, extract the actual layout properties from the code: flex direction, relative sizes, gaps, absolute vs. relative positioning, z-index/stacking, and the real color values used. Build this into an explicit spatial map — regions, their proportions, and their relationships to each other — not a list of component names. This map is the canvas every later judgment gets measured against; skipping it and going straight to content-reading is the single most common way real problems stay invisible.

**A specific, checkable sub-task within this stage: verify every spacing, type, and radius value traces back to a named token from the enforced scale — never a raw, one-off number.** A hand-typed arbitrary value (a raw hex color, an inline `padding: 13`) sitting next to token-based siblings is a concrete, mechanical signal of drift, exactly as real as a visual clutter problem — and it's cheap to check while the spatial map is already being built, not a separate pass. Where a screen must adapt across device sizes, confirm the value resolves from a breakpoint-keyed lookup table, not a runtime-computed ratio — an agent should only ever be selecting a named token, never deriving a number.

### Stage 2 — Within the stage: typography, job-count, density

Only once the spatial map exists, assess typography (which scale, content vs. chrome), and — critically — **job-count**: label each region by the conceptual job it performs (navigates time, selects what's shown, displays content, takes an action), not by component name, then group by job. Redundancy — multiple elements answering the same underlying question — is far easier to see once the spatial map already exists, because you can literally see two or more regions sitting in different places doing the same thing, rather than inferring it from a linear list.

### Stage 3 — Container-job match: the "boxes everywhere" check

For every region, ask what job it's actually doing: **browsing or comparing discrete, independent items** (cards are the right tool) or **conveying continuity, sequence, or relationship between things** (cards are the wrong tool, and using them anyway produces "Fragmented Information" — a named, real anti-pattern where the container itself breaks apart the relationship the person needs to perceive, and each card becomes an isolated island rather than part of a continuous journey). A linear flow, an onboarding sequence, or anything meant to feel like one connected experience should never be built from discrete bordered boxes — it needs a genuinely continuous visual treatment instead: a connected line, a flowing gradient, shared unbroken background, not walls between adjacent pieces of the same idea.

**Concrete, checkable signals, not just judgment calls:**
- If text needs to shrink below 14px to fit inside a container, that container is carrying too much — split it or simplify it, don't shrink text further.
- Shadows stacked on shadows, or borders stacked on borders, on the same small element is a real, named visual-competition anti-pattern — each additional layer fights the others for attention rather than adding clarity.
- More than one badge/indicator stacked on a single small target (an icon, an avatar) is the same problem at a smaller scale — extract each badge's actual information value; if one is nearly always true (redundant with something already communicated elsewhere on screen), remove it rather than shrink it further.

### Stage 4 — Tappable and navigational inventory

Within the now-understood spatial and typographic map, list every element that can be tapped or pressed.

### Stage 5 — Placement-alignment check

For each tappable element, ask whether its *placement* — not just its existence — makes sense given the Stage 1 spatial map: is a primary, frequently-used action buried or small; is a rarely-used control occupying prime, high-visibility real estate; does the element's position match how a person would actually expect to find it, given everything already known about the screen's composition.

### Stage 6 — Navigation list and recursive descent

Build the complete list of everywhere this screen can navigate to. For each destination, before moving on: **confirm the destination actually reads and uses whatever was sent to it** — params, IDs, selection state — not merely that the destination exists and renders without error. A screen "working" and a screen "correctly receiving what a specific tap intended to send it" are different, and only checking the former misses real bugs (a navigation call whose params are silently discarded downstream, so every choice in a selection list produces the same result regardless of which item was tapped, is exactly this class of bug, and it will not show up any other way). Then recurse: apply Stages 1 through 6 to each destination screen in turn, building out the full navigable tree.

---

## Risk-tiering — making this tractable at scale, not exhaustive by default

A full six-stage pass on every single screen in a large tree is not the goal, and treating it as the goal produces enormous cost for real but modest returns. Apply full depth where real signals indicate it's warranted, and a lighter pass everywhere else:

- **Full six-stage treatment** — screens with three or more distinct navigation targets (Stage 6's payload-tracing matters most here), screens with small elements carrying multiple stacked indicators (Stage 3's clutter check matters most here), and screens that are primary, frequently-used entry points rather than rare sub-screens.
- **Partial treatment (Stages 1–2 only, skip deep reconstruction)** — moderately complex screens without strong redundancy or clutter signals on first pass.
- **Light pass (existence-check only)** — low-traffic, structurally simple screens (a single static settings row, a rarely-visited legal page) where the cost of full treatment clearly outweighs the likely find.

Re-evaluate this tiering as findings accumulate — a screen that looked simple can reveal a real signal (an unusually large file, an unexpected number of navigation targets) that promotes it to full treatment mid-audit.

## Worked examples, from real findings

- **Stage 0 (canonicality tracing) caught:** two similarly-named surface-definition hooks, only one of which was the real live path — and only reachable by tracing one gating layer deeper than the first plausible match. A second, similarly-named screen file, checked the same way, turned out to have zero real references outside its own package's public exports — a genuine orphan, not a second live implementation.
- **Stage 1's token-drift check caught:** two states of one toggle control using two entirely unrelated, hand-typed hex colors, sitting in a file where a sibling component used a proper token-based color utility — a concrete, mechanical sign of drift between two different authoring practices in the same small area of the app, not a matter of taste.
- **Stage 2 (job-count) caught:** three separate, differently-named controls (a date navigator, a mode toggle, a scale selector) all answering some version of "when" — invisible to a plain existence check, since each one individually worked correctly.
- **Stage 3 (container-job / clutter) caught:** two emoji used as functional status badges stacked on one small icon circle, one of them (a "has history" indicator) redundant with a global control already established elsewhere on the same screen.
- **Stage 6 (navigation payload tracing) caught:** a classroom-selection list whose tap handler passed a specific classroom's ID onward — and nothing downstream ever read it, meaning every choice in the list silently produced the same result. Invisible to every earlier stage; only surfaced by following one specific tap all the way to whether its destination actually consumed what was sent.
