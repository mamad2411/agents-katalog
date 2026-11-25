---
name: localization-readiness
description: "Checks a design for issues that will surface once text is translated: fixed-width containers that will clip longer languages, RTL layout assumptions, concatenated/hardcoded sentence fragments, and untranslatable content baked into images. Use before sending a design or file for localization."
---

# Localization Readiness

## Purpose
Catch layout and content patterns that break once text is translated, before that translation actually happens.

## Operating Role
Act as a Figma design-file reviewer for this specific skill. Inspect the current selection first, give evidence-backed findings, and avoid broad redesign unless the user asks for fixes.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Before sending a file or flow for translation/localization
- When a product is expanding into new languages, especially RTL (Arabic, Hebrew) or long-average-length languages (German, Finnish) or CJK languages

## Required Inputs
- The target languages/locales, if known -- this changes which checks matter most (RTL vs length-expansion vs CJK line-breaking)
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Stress-test layouts for text expansion, format changes, bidirectionality, and ambiguous visuals. Separate design risks from engineering i18n risks.

## Workflow
1. Check every text container's resizing: fixed-width/fixed-height text layers should be flagged, since most languages run 20-35% longer than English and German/Finnish can run even longer; containers should hug or allow wrapping.
2. Check for hardcoded concatenation patterns (e.g. a sentence assembled from separate text layers like "You have " + [3] + " items") since word order varies by language -- flag these as needing to become a single translatable string with placeholders.
3. Check for text baked into images (e.g. a screenshot with UI text, an illustration with a label) and flag it as needing a real text layer or a per-locale asset instead.
4. If RTL locales are in scope, check that layout is built with auto layout/constraints that can mirror (rather than assets or layouts that assume strict left-to-right), and flag icons that imply direction (e.g. arrows, "back" chevrons) as needing mirrored variants.
5. If CJK locales are in scope, check line-height and font choices accommodate taller/denser glyphs, and that text is not relying on letter-spacing tricks that do not apply to CJK scripts.
6. Check date, number, and currency formats aren't hardcoded to one locale's convention in a way the code cannot override per locale.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Report each issue with the specific screen/layer, not general localization advice.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Start with a 3-line summary: scope reviewed, blocker count, and highest-risk issue. Then provide grouped findings with location, severity, evidence, and exact fix. End with skipped or unverified areas.
- Skill-specific format: A checklist grouped by risk type (Fixed-width containers, Concatenation, Text-in-images, RTL, CJK, Formats) with pass/fail and fix per item.
