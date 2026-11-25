---
name: vis-product-design
description: "Adaptive product-design workflow suite that routes a request to the right focused mode and carries one shared PROJECT_CONTEXT through it: context setup and normalization, evidence research, three-direction ideation, screenshot or design-image to code, live URL recreation, UX and accessibility audit, prototype design QA with P0/P1 fixes, and share-ready handoff. Use when turning product ideas, screenshots, reference images, existing prototypes, or live URLs into reviewable responsive frontend experiences."
---

# Adaptive Product Design

Turn early product ideas, live URLs, screenshots, design images, and existing prototypes into reviewable, responsive frontend experiences. One request enters, the correct focused mode handles it, and `PROJECT_CONTEXT` stays consistent across modes.

## Global Rule

Never hard-code a project domain into reusable structure. Any project-varying value must be a `[PARAMETER]`, a data object, or configuration. Infer unspecified parameters from project context instead of forcing the user to fill every field.

## Mode Router

Read the mode file matching the request; route instead of duplicating mode instructions:

| Request | Mode | Reference |
| :--- | :--- | :--- |
| Setup, save, recall durable product/design references | user-context | `references/mode-user-context.md` |
| Normalize the current brief into minimum context | get-context | `references/mode-get-context.md` |
| Investigate current user friction or product behavior | research | `references/mode-research.md` |
| Explore distinct visual/product directions | ideate | `references/mode-ideate.md` |
| Screenshot or design image to frontend prototype | image-to-code | `references/mode-image-to-code.md` |
| Live URL to editable local prototype | url-to-code | `references/mode-url-to-code.md` |
| Critique UX, hierarchy, accessibility | audit | `references/mode-audit.md` |
| Validate a built prototype, close high-impact defects | design-qa | `references/mode-design-qa.md` |
| Publish or hand off a runnable prototype | share | `references/mode-share.md` |

Shared persona and parameter contract: `references/master-prompt.md`. Role personas: `references/persona-product-designer.md` and `references/persona-frontend-engineer.md`. Scaffoldable starting point for any build mode: `templates/prototype/`, optionally generated into an empty directory via `node scripts/bootstrap-prototype.mjs --root <target-dir>`.

## Compound Workflows

```text
New product idea        get-context -> ideate -> image-to-code -> design-qa
Screenshot to proto     get-context -> image-to-code -> design-qa
Live URL recreation     get-context -> url-to-code -> design-qa
Existing critique       get-context -> audit
Evidence-led redesign   get-context -> research -> ideate -> image-to-code -> design-qa
```

Run modes in order within one continuous engagement, passing the same normalized `PROJECT_CONTEXT` forward. A mode may be skipped only when its input does not exist or the user explicitly opts out.

## Execution Protocol

1. **Normalize first**: establish or load `PROJECT_CONTEXT` via get-context (and user-context when saved references exist) before any build or critique work.
2. **Route faithfully**: pick the mode table row matching the actual request; keep source fidelity for clone-style modes and direction diversity for ideation.
3. **Close the loop**: every build output passes design-qa before share; audit findings carry target, observation, severity (P0/P1/P2), confidence, and recommended fix.

## Checkable Completion Criteria

- [ ] A normalized `PROJECT_CONTEXT` exists before the first build or critique mode runs.
- [ ] The executed mode matches the request; mode-specific fidelity or diversity rules were followed.
- [ ] All project-varying content stayed `[PARAMETER]`, data, or config with zero hardcoded domain values.
- [ ] Build outputs passed design-qa with P0/P1 findings fixed and relevant checks re-run.
- [ ] Shared results reference only URLs or artifacts actually produced.
