---
name: rename-layers-batch
description: "Batch-renames a large set of layers according to a rule (pattern, content-based inference, or find/replace) in one pass, reporting every change made. Use for quick, mechanical bulk renaming, as a lighter-weight companion to the more comprehensive naming-convention-enforcer."
---

# Rename Layers Batch

## Purpose
Apply a mechanical bulk rename across many layers in one pass, based on a clear rule.

## Operating Role
Act as a Figma design-file cleanup specialist for this specific skill. Prefer precise, reversible, scoped changes with previews for bulk edits.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- A large number of layers need the same kind of rename (e.g. all "Rectangle N" icons renamed by content, or a consistent find/replace across many names)
- For a deeper structural naming pass (conventions across types of layers), use naming-convention-enforcer instead

## Required Inputs
- The exact rule: a find/replace pattern, a content-based rule ("name each icon after what it depicts"), or a prefix/suffix pattern to apply
- The scope (selection, page, or file)
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Default to selection scope. If nothing is selected, ask before touching the whole page.
- Use preview mode for large batches; apply only clearly mechanical renames.

## Workflow
1. Identify every layer in scope matching the rule's trigger condition (e.g. still has a default name, or matches the find pattern).
2. Apply the rule mechanically and consistently: same find/replace logic, same inference logic, or same prefix/suffix pattern for every matched layer.
3. Skip (and report) any layer where the rule is ambiguous (e.g. content-based naming for an icon that's unclear what it depicts) rather than guessing.
4. Present the full before -> after list for confirmation before applying at large scale (more than roughly 20 renames); apply directly for small batches.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Do not rename layers outside the specified scope, even if they also match the rule, without confirming scope expansion first.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return a preview or change log with before/after values, skipped ambiguous items, and any breaking-change risk. Keep the report short enough to act on immediately.
- Skill-specific format: A before -> after table of every rename made, plus a separate list of layers skipped due to ambiguity.
