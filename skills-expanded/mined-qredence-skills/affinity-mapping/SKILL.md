---
name: affinity-mapping
description: "Groups raw qualitative data (research notes, survey verbatims, support tickets, interview quotes) into a bottom-up affinity map -- clustering related observations before naming themes, rather than sorting into pre-defined buckets. Use for open-ended research synthesis where categories aren't known in advance."
---

# Affinity Mapping

## Purpose
Synthesize raw qualitative data bottom-up: group related individual observations first, then name the themes that emerge -- rather than sorting into categories decided in advance.

## Operating Role
Act as a Figma design-file producer for this specific skill. Create or structure the requested artifact in the file when enough context exists; otherwise return the smallest useful plan and ask only for blocking inputs.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Synthesizing open-ended research (interview notes, support tickets, survey verbatims) where the right categories aren't known yet

## Required Inputs
- The raw data source (pasted notes, a connected doc/spreadsheet, or existing loose stickies)
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Use existing sticky positions or colors as weak signals, not hard categories. Cluster by meaning first, then name themes.
- Create 3-8 actionable themes unless the evidence strongly requires more.

## Workflow
1. Convert each discrete observation/quote into its own individual note if not already atomized -- one idea per note, not paragraphs.
2. Do a first pass grouping notes that feel directly related, without naming groups yet -- resist jumping to categories too early.
3. Once initial small clusters form, look for clusters that are really the same underlying idea and merge them; split any cluster that's actually two different ideas.
4. Only after clustering is stable, name each cluster with a theme label that captures the shared idea, written from the user's point of view where possible (e.g. "Users do not trust the price until checkout", not "Pricing").
5. Note the frequency (how many observations) per theme, since this is often useful signal for prioritization, while flagging that frequency in qualitative data is not the same as prevalence in the full user base.
6. Surface tensions or contradictions between themes explicitly (e.g. "some users want more automation, others want more control") rather than smoothing them over.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Keep source traceability -- each theme should be able to point back to the specific observations that formed it.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return the created or proposed Figma structure first, then list assumptions, variants/states covered, and follow-up decisions. If changes were applied, include exactly what changed.
- Skill-specific format: Clusters laid out spatially with theme labels, plus a written summary: theme -> frequency -> representative quote/observation.
