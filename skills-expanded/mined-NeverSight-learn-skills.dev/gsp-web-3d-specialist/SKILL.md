---
name: gsp-web-3d-specialist
description: "Use when implementing browser-first 3D game work after the route and backend are already chosen."
---

# Game Web 3D Specialist

## Goal
Turn a browser 3D backend decision into a concrete implementation path with explicit camera, focus, HUD, and performance rules.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present 3D implementation guidance in conversation.
- **minimal** or **full**: write or update `docs/game-studio/backend-implementation.md`.

## Use when
- the chosen backend profile is `web-3d-preview`
- the project needs browser 3D or hybrid 3D plus UI planning
- the team wants concrete implementation guidance without a top-level engine lock-in

## Use
- `../../shared/reference/backend-profiles.md`
- `../../shared/reference/browser-3d-specialist.md`
- `../../shared/checklists/ui-ux-hard-rules.md`

## Cover
- recommended 3D route archetype and why
- camera, gameplay, menu, and modal focus ownership
- pointer-lock or free-look policy when relevant
- HUD layer decision and readability protection
- performance budget assumptions
- asset complexity and feedback budget
- top implementation risks

## Important
Browser 3D must be concrete about control-state ownership and readability.
Do not treat 3D as an excuse to skip UI/UX rigor.
