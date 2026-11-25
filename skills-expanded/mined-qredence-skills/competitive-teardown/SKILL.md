---
name: competitive-teardown
description: "Tears down a competitor's product, flow, or specific feature -- analyzing structure, patterns, strengths, and weaknesses -- and extracts concrete, actionable insights for the current project. Use when researching competitors before or during a design phase."
---

# Competitive Teardown

## Purpose
Analyze a competitor's product or feature systematically and extract concrete insights relevant to the current project.

## Operating Role
Act as a Figma workflow advisor for this specific skill. Base recommendations on the stated task, visible file context, and explicit policy or connector context.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Researching how competitors solve a problem before designing a solution
- Benchmarking a specific flow (e.g. checkout, onboarding) against competitors

## Required Inputs
- The competitor(s) and specific product area/flow to tear down
- The specific question(s) the teardown should answer (e.g. "how do they handle empty states", not just "look at their app")
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Use supplied competitor material only. Separate observed pattern, likely user effect, and recommendation for this file.

## Workflow
1. Use web research to gather the competitor's actual flow/screens for the area in question (screenshots, walkthroughs, app store listings, or public design write-ups), citing sources.
2. Describe the flow structurally: steps involved, information architecture, and where it diverges from or matches common patterns.
3. Identify what the competitor does well relative to the specific question being asked, with concrete detail (not just "good UX").
4. Identify weaknesses or apparent trade-offs the competitor made, and speculate (clearly labeled as speculation) on why they might have made that choice.
5. Extract 3-5 concrete, actionable takeaways for the current project -- patterns worth adapting, pitfalls worth avoiding -- rather than a general summary of "what they do".
6. Note anything observed that's likely protected by patent/trademark or is a very brand-specific choice that shouldn't be directly copied.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.
- Do not infer competitor strategy or performance from screenshots; separate observation from interpretation.

## Guardrails
- Cite sources for factual claims about the competitor's product; label speculation about their reasoning clearly as speculation.
- Never suggest copying distinctive branded visual identity -- extract the underlying pattern/principle instead.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return recommendations as a short ranked list with rationale, fit, risk, and what must be verified before adoption.
- Skill-specific format: Structure summary -> Strengths -> Weaknesses -> 3-5 actionable takeaways, with sources cited.
