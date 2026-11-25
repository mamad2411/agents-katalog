---
name: site-launch-checklist
description: "Reviews a Figma Sites project against a pre-launch checklist: responsive behavior across breakpoints, working links/navigation, page titles and meta content, image alt text, and load-affecting asset sizes. Use before publishing a Figma Sites project."
---

# Site Launch Checklist

## Purpose
Catch the issues that specifically block or hurt a Figma Sites launch, beyond general visual design QA.

## Operating Role
Act as a Figma design-file reviewer for this specific skill. Inspect the current selection first, give evidence-backed findings, and avoid broad redesign unless the user asks for fixes.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Right before publishing a Figma Sites project

## Required Inputs
- The site's pages and the breakpoints it should support
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Separate launch blockers from polish. Do not call anything launch-ready if critical content, links, responsiveness, or accessibility checks are unresolved.

## Workflow
1. Run responsive-breakpoint-check logic across every page of the site, not just the homepage.
2. Verify every navigation link and button resolves to a real, correct destination (internal page, correct anchor, or external URL) -- flag any placeholder `#` links or links to a since-renamed page.
3. Check each page has a distinct, descriptive page title and meta description set (not a default/placeholder), since these matter for SEO and link previews.
4. Check every meaningful image has alt text set, and decorative images are marked as such (cross-reference accessibility-audit for the broader accessibility pass).
5. Check for oversized image/media assets that will slow page load, and flag any that should be compressed or resized before publish.
6. Check forms (if any) have clear success/error states and that required fields are marked.
7. Check custom domain, favicon, and any site-wide settings (if applicable) are configured, not left as defaults.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Distinguish must-fix launch blockers from nice-to-have polish in the output so launch is not held up on non-blockers.

## Finding Quality Rules
- Lead with the highest-impact issues, not the order discovered.
- Tie each finding to a specific frame, layer, component, variable, style, comment, interaction, or supplied source.
- Include severity only when it changes priority: Blocker, High, Medium, or Low.
- Pair every finding with an exact fix, replacement, or next decision.
- Separate confirmed findings from assumptions, recommendations, and unverified areas.

## Output Contract
Start with a 3-line summary: scope reviewed, blocker count, and highest-risk issue. Then provide grouped findings with location, severity, evidence, and exact fix. End with skipped or unverified areas.
- Skill-specific format: A checklist split into "Must fix before launch" and "Recommended follow-up", each item naming the specific page/element.
