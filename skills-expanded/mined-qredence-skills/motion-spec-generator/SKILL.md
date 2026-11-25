---
name: motion-spec-generator
description: "Defines and documents a precise motion spec (duration, easing curve, delay, properties animated) for key transitions in a flow, so the intended motion feel is captured explicitly rather than left to be reverse-engineered from a prototype. Use when documenting motion decisions for engineering handoff or design system consistency."
---

# Motion Spec Generator

## Purpose
Turn intended motion for key transitions into a precise, documented spec that can be implemented consistently.

## Operating Role
Act as a Figma design-file producer for this specific skill. Create or structure the requested artifact in the file when enough context exists; otherwise return the smallest useful plan and ask only for blocking inputs.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Documenting motion for developer handoff
- Establishing/updating a design system's motion guidelines

## Required Inputs
- The specific transitions/animations to spec (e.g. modal open/close, page transition, a component's micro-interaction)
- Any existing motion principles for the product (e.g. "quick and snappy" vs. "smooth and considered") to keep new specs consistent with
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Describe trigger, affected layers, properties, duration, easing, direction, and reduced-motion expectation for each motion moment.

## Workflow
1. For each transition, identify exactly which properties animate (position, opacity, scale, color, size) and their start and end values.
2. Choose duration deliberately based on the distance/size of the change and the transition's role: micro-interactions (hover, toggle) typically feel best fast (roughly 100-200ms), standard navigational transitions moderate (roughly 200-400ms), and larger/attention-drawing transitions slightly longer -- state the exact chosen value, not a vague range, and keep it consistent with any existing product-wide motion principle.
3. Choose an easing curve matching the motion's character: ease-out for elements entering/appearing (fast start, gentle stop feels responsive), ease-in for elements exiting, ease-in-out for elements moving between two on-screen states, and spring/bounce easing (with specific stiffness/damping or bounce/duration values) for anything meant to feel tactile or playful -- state exact curve parameters, not just a name, if the target platform needs them (e.g. cubic-bezier values for CSS).
4. Note any delay/stagger, especially for multi-element transitions (e.g. list items staggering in), including the exact per-item delay.
5. Note reduced-motion behavior: what should happen instead when a user has motion-reduction preferences enabled (usually: keep the state change, remove or shorten the animated transition).
6. Where the Figma prototype's Smart Animate or spring settings already exist, extract their actual values as the source of truth for the spec rather than re-guessing.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Give implementable exact values (ms, curve parameters) rather than only qualitative descriptions like "smooth" or "quick".

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return the created or proposed Figma structure first, then list assumptions, variants/states covered, and follow-up decisions. If changes were applied, include exactly what changed.
- Skill-specific format: A per-transition spec table: Transition | Properties animated | Duration | Easing | Delay/stagger | Reduced-motion behavior.
