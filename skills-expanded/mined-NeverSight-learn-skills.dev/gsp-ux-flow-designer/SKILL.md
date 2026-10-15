---
name: gsp-ux-flow-designer
description: "Use when designing onboarding, menus, CTA hierarchy, and first-minute interaction flow for a game."
---

# Game UX Flow Designer

## Goal
Define the player-facing flow clearly enough that implementation does not drift into unreadable or frustrating UX.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present UX flow design in conversation.
- **minimal** or **full**: write `docs/game-studio/ux-flow.md`.

## Spec-driven compatibility
When `gsp-spec-driven-planning` is active, fold the UX flow decisions into `changes/<change-id>/design.md` instead of creating a separate durable doc by default.

## Must cover
- entry flow
- first 30 seconds
- start / restart / fail / success states
- pause or escape flow when relevant
- HUD priorities
- onboarding style
- readability and accessibility constraints
- critical feedback moments

## Hard rules
Use:
- `../../shared/reference/first-30-seconds.md`
- `../../shared/checklists/ui-feedback-checklist.md`
- `../../shared/checklists/ui-ux-hard-rules.md`

Explicitly decide:
- how the playfield is protected from overlay clutter
- what the persistent HUD budget is
- whether the project needs a dedicated UI layer for text-heavy or responsive UI
- how pause, menu focus, pointer lock, camera control, and gameplay input hand off control
- what mobile safe-area and thumb-zone constraints exist when relevant

## By quality target
- **first-playable**: first 30 seconds and essential affordances only
- **polished-prototype**: include title/start, retry, pause, success/failure flow, clearer UI rhythm, and explicit playfield/HUD rules
- **production-feature / live-patch**: preserve consistency with the existing product while improving the target flow

## Important
Do not stop at vague UX language.
Lock concrete player-facing rules that implementation can actually follow.
If critical UX flow details are still unknown, ask follow-up questions until the flow is explicit enough to implement with confidence.
