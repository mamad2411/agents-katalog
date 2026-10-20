---
name: figma-quarterback
description: Coordinate a high-fidelity Figma-to-code workflow for screens, layouts, drawers, dialogs, or component groups. Use when Codex receives one or more Figma URLs or node IDs and must decide how to extract exact design intent, split work into reusable components, route implementation safely, and keep conversion and apply work aligned with the local design system and verification constraints.
---

# Figma Quarterback

Coordinate the full Figma workflow instead of jumping straight to code. Treat this skill as the entrypoint when the request is large enough that extraction quality, component boundaries, or implementation order will decide whether the result drifts.

Prefer the existing Figma plugin skills for raw tool usage:
- Use `figma` / `figma:figma-implement-design` for direct design-to-code reads.
- Use `figma:figma-use` before any write action inside a Figma file.
- Use `figma:figma-generate-design` when the user wants code or a description pushed back into a Figma screen.
- Use `figma:figma-generate-library` when the job is tokens, component library structure, or design-system buildout inside Figma.
- Use `figma:figma-code-connect` when the user wants code components mapped back to Figma components.
- Use this skill to decide sequencing, guardrails, and handoff contracts.

## Workflow

1. Frame the request before touching code.
- Classify the target as `layout`, `screen`, `dialog`, `drawer`, or `component-set`.
- List every requested state up front: desktop/mobile, open/closed, active/inactive, empty/loaded, hover/focus if relevant.
- Record the expected output: docs only, component implementation, full page implementation, or Figma update.

2. Build an extraction-first plan.
- Run `$figma-design-extract` when component boundaries, states, tokens, regions, or traps are not already explicit.
- Ask it for an implementation contract, not a narrative summary.
- Do not let coding start while critical inputs are still ambiguous.

3. Decide whether the work is single-pass or wave-based.
- Use a single pass only for one isolated component with clear states.
- Use waves for layouts, compound surfaces, or any request with shared primitives.
- Typical wave order: setup tokens and dependencies, independent components, dependent composites, final composition.

4. Route implementation to `$figma-convert-apply`.
- Pass only stable facts: target files, reusable components, exact states, tokens, asset rules, and verification expectations.
- Require explicit note of what is reused versus what is new.
- Require responsive behavior to be stated as props, variants, or breakpoint rules before editing.

5. Enforce a completion receipt.
- Surface type and target nodes used.
- State matrix actually implemented.
- Files changed.
- Reuse decisions.
- Verification performed.
- Known degradations or manual checks still required.

## Routing Matrix

Route by user intent, not by whichever skill sounds closest.

- `Extract design truth from Figma`:
  Use `$figma-design-extract` plus the raw Figma read skills. This is the default lane for unclear or multi-node requests.
- `Implement code from an already stable design contract`:
  Use `$figma-convert-apply`. Keep quarterback ownership only if multiple waves or surfaces must stay coordinated.
- `Implement code directly from a Figma URL with minimal orchestration`:
  Use `figma:figma-implement-design` when the task is narrow and component-scoped.
- `Write or update a screen inside Figma from code or a page description`:
  Use `figma:figma-generate-design`, and make sure `figma:figma-use` is loaded before any write action.
- `Create or repair a design system inside Figma`:
  Use `figma:figma-generate-library`, optionally paired with `figma:figma-use` for file writes.
- `Map code components to Figma components`:
  Use `figma:figma-code-connect`.
- `Generate design-system rules for the repo`:
  Use `figma:figma-create-design-system-rules`.
- `Need both code changes and Figma updates`:
  Stay in quarterback mode. Extract once, implement code, then route the finalized structure back through the appropriate Figma write skill.

## Routing Rules

Use `$figma-design-extract` first when:
- The request references a whole screen, layout, or multiple Figma nodes.
- Desktop and mobile differ materially.
- You suspect hidden traps such as raster art, transparent roots, local-only fonts, or reused components with different props.
- The codebase already contains related UI and you need an exact reuse map.
- The user eventually wants either code changes or write-back to Figma, but the design truth is still not stable.

Use `$figma-convert-apply` directly when:
- The extraction contract already exists in the conversation or docs.
- The task is mostly implementation and verify.
- The state set is small and already agreed.

Stay in quarterback mode when:
- Multiple files or surfaces must stay consistent.
- You need to re-scope the work because the extracted design is larger than the original ask.
- Verification failure suggests the issue is in the plan rather than the code.
- The job spans both repo implementation and Figma write-back.
- You must coordinate design-system work, page generation, and code-connect mapping in one run.

## Figma Built-Ins

Use the built-in Figma skill set explicitly instead of recreating its job in prose:

- `figma`:
  Base read lane for Figma context retrieval and design-to-code assistance.
- `figma:figma-implement-design`:
  Best for turning one Figma component or screen into production code when orchestration overhead is small.
- `figma:figma-use`:
  Mandatory before any write operation inside a Figma file.
- `figma:figma-generate-design`:
  Best for pushing a full page, screen, or layout from code or description back into Figma.
- `figma:figma-generate-library`:
  Best for tokens, component libraries, themes, and design-system foundations in Figma.
- `figma:figma-code-connect`:
  Best for creating or maintaining Code Connect mappings.
- `figma:figma-create-design-system-rules`:
  Best for repo-specific design rules that help future Figma-to-code work.

## Handoff Contract

Hand off to downstream work with this structure:

- `Surface`: layout, screen, drawer, dialog, or component.
- `Node scope`: exact file key and node IDs, plus any parent or sibling nodes consulted.
- `States`: one flat list with dimensions or viewport assumptions.
- `Reuse map`: existing component, extend existing component, or build new.
- `Tokens`: colors, spacing, radii, typography, shadows, and gradients that matter.
- `Asset policy`: raster/vector URLs, masks, backgrounds, icons, and whether approximation is forbidden.
- `Verification`: structural, CSS, visual, or manual comparison.
- `Stop conditions`: missing assets, font mismatch, degraded baseline, or unresolved design ambiguity.
- `Next skill`: the exact downstream skill or built-in Figma lane to invoke next.

## References

- Read [references/pipeline.md](references/pipeline.md) for the operating model.
- Read [references/triage.md](references/triage.md) when deciding split, reuse, and wave order.
- Read [references/builtin-routing.md](references/builtin-routing.md) when the request mixes extraction, code implementation, Figma writes, library work, or code-connect.
