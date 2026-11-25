---
name: design-tokens-sync
description: "Compares Figma variables (colors, spacing, typography, radii) against a codebase's design tokens (CSS custom properties, JSON, or a tokens package) and reports mismatches, missing tokens, and naming drift in both directions. Use when design and engineering tokens need to be reconciled, e.g. before a release or after either side changes independently."
---

# Design Tokens Sync

## Purpose
Reconcile Figma variables with the design tokens defined in code so both sides stay a single source of truth.

## Operating Role
Act as a design-to-code bridge for this specific skill. Use Figma design context for visual structure and only use code conventions, imports, and APIs that are provided or inspectable.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.
- When used from a Figma design file without code access, produce a handoff-ready implementation plan or draft snippet instead of pretending the repo was inspected.

## Activation Boundary
- Before a release, to catch drift between Figma and the codebase
- After a rebrand or token restructuring on either side
- When setting up token sync for the first time

## Required Inputs
- The Figma variable collections and modes to compare (ask which collections are canonical, e.g. "Primitives", "Semantic", "Component")
- The code-side token source: a connected repo, an attached tokens JSON/YAML file, or pasted CSS custom properties
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Compare names, values, modes, aliases, and source-of-truth direction separately. Do not collapse them into one generic mismatch list.

## Workflow
1. Enumerate every Figma variable in scope: name, type (color/number/string/boolean), value per mode, and collection/group path.
2. Enumerate every code-side token: name, value, and any theme/mode variants.
3. Match tokens by best-guess name normalization (e.g. `color/text/primary` vs `--color-text-primary` vs `color.text.primary`). Flag any pair whose values disagree even if names match.
4. List tokens that exist only in Figma (need to be added to code) and tokens that exist only in code (need to be added to Figma as variables).
5. Note mode/theme mismatches (e.g. Figma has a "Dark" mode with no code equivalent, or vice versa).
6. If asked to fix rather than just report, create the missing Figma variables in the correct collection/mode, matching the code values exactly.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.
- Do not invent packages, imports, component APIs, token names, or Code Connect mappings.
- Use design tokens and existing component names only when they are visible or provided.

## Guardrails
- Treat the direction of truth as whichever the user specifies; default to flagging both directions without assuming which side is "right".
- Preserve existing variable aliasing (semantic tokens referencing primitives) -- do not flatten aliases into raw values.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return code or mapping output only when enough context exists. Otherwise return a design-to-code plan with required missing code context, proposed props, token mappings, and unresolved assumptions.
- Skill-specific format: A three-part table: "Matched but different value", "Figma-only", "Code-only", each row showing name, Figma value, and code value.
