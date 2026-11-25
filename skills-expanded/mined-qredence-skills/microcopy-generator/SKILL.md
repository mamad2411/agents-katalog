---
name: microcopy-generator
description: "Drafts microcopy -- button labels, empty states, error messages, tooltips, confirmation dialogs, form hints -- for a specific screen or component, matching a stated (or inferred from existing content) voice and tone. Use when placeholder text needs to become real, ship-ready copy."
---

# Microcopy Generator

## Purpose
Draft real, ship-ready microcopy for specific UI moments, matching the product's existing voice.

## Operating Role
Act as a Figma design-file producer for this specific skill. Create or structure the requested artifact in the file when enough context exists; otherwise return the smallest useful plan and ask only for blocking inputs.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- A screen has placeholder copy that needs to become final
- A new state (error, empty, confirmation) needs copy drafted from scratch

## Required Inputs
- The specific element(s) needing copy and their exact context (what triggered this state, what the user should do next)
- The voice/tone to match -- infer it from existing finished copy elsewhere in the file if not explicitly given, and state the inferred voice before proceeding
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Generate copy in sets of 2-3 high-quality options only when alternatives are useful. Prefer precise UI copy over clever copy.

## Workflow
1. Read existing finished copy in the file (not placeholders) to infer voice: formality, use of contractions, humor level, sentence length, and terminology choices already established.
2. For each element needing copy, write to the specific pattern's best practice: buttons as a specific verb + object ("Save changes", not "Submit"), error messages that state what happened and how to fix it (not just "Something went wrong"), empty states that explain what will appear and how to get there, tooltips that add information not already visible, confirmation dialogs that state the specific consequence of the action.
3. Respect any known length constraints (character counts from content-inventory, container width) and note if the best copy does not fit and a container change would be better than truncation.
4. Keep terminology consistent with what's used elsewhere in the file (e.g. do not introduce "delete" in one place and "remove" in another for the same action).
5. Provide one primary option per element; offer 1-2 alternates only where tone is genuinely ambiguous or the user asked for options.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Never invent copy that implies a feature, policy, or promise not otherwise confirmed (e.g. do not write "your data is never shared" unless that's an established, accurate claim).

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return the created or proposed Figma structure first, then list assumptions, variants/states covered, and follow-up decisions. If changes were applied, include exactly what changed.
- Skill-specific format: A list of element -> drafted copy (plus alternates where relevant), with the inferred voice stated up front.
