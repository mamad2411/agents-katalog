---
name: generate-web-icons
description: Use when web app icon assets must be created or refreshed within the existing workspace design language and framework, with manifest-ready outputs and deterministic quality checks.
---

# Generate Web Icons

## Specialization

Use this skill to create or refresh web application icon assets while preserving the workspace's existing visual language, design tokens, and framework conventions.

This skill is specialized for icon-system execution and integration. It does not redefine brand direction or replace broader web UX strategy work.

## Objective

Produce a complete, framework-integrated web icon set that is visually consistent with the current product language and ready for browser, PWA, and platform-specific usage.

## Trigger Conditions

- A web app is missing required favicon, PWA, or touch icon assets.
- Existing icon assets are outdated after a design-system or brand refresh.
- A release needs deterministic icon coverage and manifest correctness evidence.
- Browser tab, install prompt, or pinned-icon rendering is inconsistent across target platforms.

## Scope Boundaries

In scope:

- Reuse of existing iconography rules, tokens, and shape language from the workspace.
- Creation of production icon assets and manifest/head integration updates.
- Deterministic quality checks for clarity, contrast, and scaling.

Out of scope:

- Inventing a new visual identity when none is approved.
- Reworking unrelated page layouts or component architecture.
- Broad UX research or visual-system redesign.

## Inputs

- Existing design language references: tokens, icon style rules, and brand constraints.
- Current framework and asset pipeline constraints (for example Next.js, Vite, or static hosting).
- Target platform matrix: desktop browsers, mobile browsers, installable PWA, and pinned surfaces.
- Existing icon files and manifest/head configuration paths.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Icon coverage matrix mapping each target use case to a concrete file.
- Production icon files exported in required formats and sizes.
- Updated integration points (`site.webmanifest`, HTML head links, and framework metadata config where applicable).
- Verification notes for cross-platform rendering, legibility, and contrast.
- Final recommendation: `ready`, `ready-with-exceptions`, or `blocked`.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Create baseline browser icons | `favicon.ico` and one scalable source icon are integrated and render correctly |
| L2 Delivery | Ship complete web + PWA icon set | Coverage matrix is complete and manifest/head integration is valid |
| L3 Hardening | Validate release-grade icon quality | Cross-device rendering checks and exception log are complete |
| L4 Expert Standardization | Establish reusable icon workflow | Reusable export and verification rubric is documented for future requests |

## Deterministic Workflow

1. Confirm orchestrator intake selected this skill based on icon-specific required outputs.
2. Lock in-scope platforms, existing design-language constraints, and required icon surfaces.
3. Audit current icon assets and identify missing or non-conforming files.
4. Build an icon coverage matrix with file names, dimensions, format, and usage target.
5. Generate or update icon source artwork without changing established design language.
6. Export required raster/vector variants and place them in the framework's expected paths.
7. Update manifest and head/framework metadata references to point to the new assets.
8. Validate legibility at small sizes and verify non-blurry rendering on high-DPI displays.
9. Run quality checks: contrast, maskable-safe area coverage, and fallback behavior when SVG is unsupported.
10. Publish verification notes and final recommendation.

## Icon Coverage Matrix Template

| Use Case | File | Format | Minimum Size | Notes |
|---|---|---|---|---|
| Browser favicon fallback | `favicon.ico` | ICO | 16, 32, 48 | Multi-size fallback for older browsers |
| Modern browser tab icon | `favicon.svg` | SVG | Scalable | Keep path count minimal for crisp rendering |
| Apple touch icon | `apple-touch-icon.png` | PNG | 180x180 | No transparency artifacts |
| PWA launcher icon | `icon-192.png` | PNG | 192x192 | Standard install surface |
| PWA launcher icon (large) | `icon-512.png` | PNG | 512x512 | Required by install flows |
| PWA maskable icon | `icon-maskable-512.png` | PNG | 512x512 | Keep critical glyphs inside safe zone |

## Integration Contract

- Ensure `site.webmanifest` includes accurate icon entries (`src`, `sizes`, `type`, and `purpose` when maskable).
- Ensure HTML or framework metadata links include favicon and touch-icon references.
- Ensure cache-busting behavior is addressed when replacing existing icon files.

## Quality Gate Checklist

- [ ] New icons match the existing design language and do not introduce new visual motifs.
- [ ] Key glyph remains identifiable at 16x16 and 32x32.
- [ ] PWA icons include standard and maskable variants.
- [ ] Manifest references resolve to real files with correct MIME-compatible extensions.
- [ ] No critical platform surface is missing an icon mapping.
- [ ] Exceptions (if any) include owner, rationale, and follow-up date.

## Orchestrator Collaboration Contract

- This skill runs only after `orchestrator` intake confirms icon creation or icon refresh as an explicit required output.
- If the request is primarily brand exploration or visual-system redesign, route to UX design flows instead of invoking this skill directly.
- If required outputs extend beyond icon scope, use phased routing so this skill owns only icon deliverables.

## Rejected Candidate Reasons

- `R1`: Request is not icon-specific.
- `R2`: Required output is design strategy, not icon asset execution.
- `R3`: Scope includes broader frontend work that should be owned by another phase.
- `R4`: Existing design language is missing and must be established first.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Preserve existing design language | Specialization + Scope Boundaries + Quality Gate Checklist |
| Produce complete icon asset set | Required Outputs + Icon Coverage Matrix Template |
| Framework-aware integration | Inputs + Integration Contract + Workflow steps 6 and 7 |
| Invoke only when needed | Trigger Conditions + Orchestrator Collaboration Contract |
| Deterministic closure | Final recommendation + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- The workspace already has an approved design language to follow.
- Framework metadata or head configuration is accessible for updates.

Trade-offs:

- Strict reuse of existing visual language improves consistency but limits exploration.
- Broad icon compatibility increases export and verification work, but reduces platform regressions.

Open blockers:

- Missing source icon artwork or missing token guidance can block deterministic execution.
- Unknown deployment caching behavior can hide icon updates after release.

Recommendation:

- Default to L2 for most feature work and escalate to L3 for release-bound icon changes.

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).
- Freshness threshold defaults to 30 days for active source checks.

## Worked Example

- [orchestrator-handoff-example.md](../../../.docs/changes/skill/examples/generate-web-icons/orchestrator-handoff-example.md)

## Pragmatic Stop Rule

Stop when every required icon surface has a mapped file, integration references are valid, and final recommendation status is explicit.

## Done Criteria

- Trigger conditions are satisfied.
- Required outputs are complete.
- Coverage matrix has no missing required icon surfaces.
- Recommendation status is explicit (`ready`, `ready-with-exceptions`, or `blocked`).
- Source catalog is current for this evaluation cycle.