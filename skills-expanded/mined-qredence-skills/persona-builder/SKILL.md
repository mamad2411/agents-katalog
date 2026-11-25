---
name: persona-builder
description: "Builds a lightweight, evidence-grounded persona (or refreshes an existing one) from available research notes, interview data, or survey results for a specific project -- avoiding invented demographic detail not supported by the source data. Use when a project needs a shared reference point for who it's designing for."
---

# Persona Builder

## Purpose
Build a lightweight persona grounded in actual available research, for use as a shared reference point on a project.

## Operating Role
Act as a Figma design-file producer for this specific skill. Create or structure the requested artifact in the file when enough context exists; otherwise return the smallest useful plan and ask only for blocking inputs.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- A project needs an agreed reference point for who it is designing for
- Refreshing an existing persona against newer research

## Required Inputs
- The available research source (interview notes, survey data, support tickets, existing user research repository) -- this skill should not proceed from pure assumption; if no research exists, say so and suggest what minimal research would ground a real persona
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Ground personas in provided evidence. Do not invent demographics unless they are relevant and supported.

## Workflow
1. Extract from the source data: goals, common pain points, typical context of use (when/where/how the product is used), and any notable behavioral patterns that recur across multiple sources (not a single outlier data point).
2. Build the persona around behaviors and goals relevant to the project, not incidental demographic detail (age, name, stock photo) unless that detail is actually relevant to the design problem and supported by the data.
3. Include representative quotes from the source material where they exist, to keep the persona connected to real voices rather than reading as invented.
4. Note confidence level per major claim (well-supported across many sources vs. a single data point) so the team knows where the persona is on solid ground versus thin.
5. If multiple distinct user types emerge from the data, propose splitting into multiple personas rather than averaging into one that represents no one well.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Never invent a name, photo, or biographical detail presented as if it were real data -- if illustrative detail is added for readability, label it clearly as illustrative, not sourced.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return the created or proposed Figma structure first, then list assumptions, variants/states covered, and follow-up decisions. If changes were applied, include exactly what changed.
- Skill-specific format: Persona name (role-based, e.g. "The time-pressed approver") -> Goals -> Pain points -> Context of use -> Representative quotes -> Confidence notes.
