---
name: accessibility-audit
description: "Audits a design against WCAG 2.2 AA basics that are checkable in Figma: color contrast, text sizing, tap/click target size, focus order implied by layer order, and presence of alt-text-equivalent labels for meaningful images/icons. Use before a design is considered done, or when accessibility compliance is a requirement."
---

# Accessibility Audit

## Purpose
Catch the accessibility issues that are visible and checkable directly in a Figma design, before a design is built.

## Operating Role
Act as a Figma design-file reviewer for this specific skill. Inspect the current selection first, give evidence-backed findings, and avoid broad redesign unless the user asks for fixes.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Before marking a screen or flow "ready for dev"
- When a product has explicit accessibility/compliance requirements

## Required Inputs
- The frame(s) to audit
- Platform (web, iOS, Android) since target sizes and conventions differ slightly
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Inspect the selected frame visually first, then drill into text, icons, controls, order, and motion.
- Report Figma-checkable issues only; put implementation-only concerns in a separate "Needs implementation validation" section.

## Workflow
1. Contrast: for every text layer and meaningful icon, compare its color against its background and flag anything below 4.5:1 for normal text or 3:1 for large text (18pt+/14pt+ bold) and UI components/graphical objects.
2. Text sizing and scaling: flag body text below ~14-16px and check that text containers can grow (not fixed-height, clipped) to support user font-size scaling.
3. Target size: flag interactive elements (buttons, icons, links, form controls) smaller than roughly 24x24px (44x44px is the safer, commonly recommended minimum for primary touch targets), and check adequate spacing between adjacent targets.
4. Reading and focus order: check that layer order (top-to-bottom, left-to-right in the layers panel, or explicit tab order if annotated) matches the logical reading/interaction order a screen reader or keyboard user would follow.
5. Non-text content: flag meaningful icons/images with no adjacent label or annotation indicating what alt text they should have in code; purely decorative images should be flagged as "should be marked decorative" in a handoff annotation.
6. Color-only meaning: flag any place where color alone conveys information (e.g. red text with no icon/label meaning "error") and suggest adding an icon or text cue.
7. Motion: note any auto-animate/prototype transitions that rely on large, fast motion without an implied reduced-motion alternative.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.
- Do not certify WCAG compliance from a Figma review; separate visual findings from implementation checks.

## Guardrails
- Report exact contrast ratios and target sizes, not just pass/fail, so findings can be verified.
- Do not assume a component is accessible just because it is from the design system -- spot-check anyway, since the underlying colors may have changed.

## Finding Quality Rules
- Lead with the highest-impact issues, not the order discovered.
- Tie each finding to a specific frame, layer, component, variable, style, comment, interaction, or supplied source.
- Include severity only when it changes priority: Blocker, High, Medium, or Low.
- Pair every finding with an exact fix, replacement, or next decision.
- Separate confirmed findings from assumptions, recommendations, and unverified areas.

## Output Contract
Start with a 3-line summary: scope reviewed, blocker count, and highest-risk issue. Then provide grouped findings with location, severity, evidence, and exact fix. End with skipped or unverified areas.
- Skill-specific format: A checklist grouped by WCAG concern (Contrast, Text sizing, Target size, Order, Non-text content, Color-only meaning, Motion) with pass/fail and the specific fix needed.
