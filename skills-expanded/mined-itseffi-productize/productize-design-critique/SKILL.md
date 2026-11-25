---
name: productize-design-critique
description: >-
  Get structured design feedback on usability, hierarchy, and consistency. Use when asked to
  review a design, critique a mockup, react to a screen, or provide feedback on a Figma link,
  screenshot, or description from exploration through final polish.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Design Critique

## Productize Preamble

Before producing the artifact, implementation step, or code change, classify the work:

- **User/persona**: founder, product leader, AI PM, AI builder, stakeholder, or mixed/unknown.
- **Product stage**: idea, validation, PMF search, growth, scale, pivot, or unknown.
- **Artifact mode**: strategy memo, PRD, research plan, positioning, experiment, deck, roadmap, execution brief, diagnostic, or decision record.
- **Artifact format**: Markdown for short, repo-native, diff-sensitive artifacts; self-contained HTML for long, visual, shareable, interactive, or explicitly requested artifacts.
- **Evidence standard**: what is known, assumed, missing, and risky.
- **Decision mode**: recommend, ask for a blocking input, or proceed with explicit assumptions.

Operating rules:

1. Do not produce generic product strategy filler. Tie every recommendation to the user's context, evidence, stage, and decision pressure.
2. Separate facts from assumptions. Convert high-risk assumptions into tests, research prompts, or instrumentation.
3. Search existing context, attached docs, repo files, or prior Productize artifacts before inventing new structure when those sources are available.
4. Ask only for inputs that materially change the output. If the next step is obvious, proceed and state assumptions.
5. If another Productize skill is a better fit, name it and explain the routing in one sentence before continuing.
6. Enforce the output contract for this skill. Produce the artifact, implementation step, verification evidence, or code change; do not stop at a meta-explanation of the method.
7. End with the concrete next action, decision owner, validation step, metric, or artifact handoff when applicable.
8. Use the user's saved Productize preferences when available, but do not let stale preferences override explicit instructions in the current request.
9. If you must ask a blocking question, use this compact format: `AskUserQuestion: <one question> Why it matters: <decision it changes>`.
10. Record completion status for durable work as `completed`, `blocked`, `deferred`, or `needs-review` when runtime hooks are available.

Artifact format policy:

- Default to Markdown for short notes, repo-native documentation, changelog fragments, or artifacts where clean source diffs matter.
- Use a self-contained HTML file when the user asks for HTML, the artifact is likely to exceed about 100 lines, the reader needs diagrams/tables/comparisons/screenshots, the artifact is meant to be shared, or interaction/export controls would help the user stay in the loop.
- Route by product job first, then choose the format. Do not create a generic HTML workflow when a Productize playbook, gate, or routed skill owns the work.
- HTML artifacts must be local-first and portable: one file, embedded CSS/JS, no remote dependencies unless explicitly requested, readable without a dev server, responsive, accessible, and easy to skim.
- Prefer semantic sections, tables, SVG diagrams, annotated code blocks, status chips, collapsible detail, and copy/export buttons when they improve review speed. Avoid decorative complexity that hides the decision.
- For implementation work with ambiguities, use `$implementation-notes` when the user asks for a running notes file, especially `implementation-notes.html` or `implementation-notes.md`.

Runtime hooks, if available:

- Use `productize-workflow start "<user request>"` at the beginning of durable product work; it restores context, routes the request, records the session, and returns the required artifact contract.
- Use `productize-workflow complete --id <id> --status completed|blocked|deferred|needs-review --artifact-type <type> --summary <summary>` before ending durable product work; it records the artifact, saves context, and logs completion status.
- Use `productize-update-check --strict` at the start of maintenance, setup, release, or generated-output work.
- Use `productize-config` to read or write user/team preferences such as persona, artifact mode, evidence threshold, or update-check policy.
- Use `productize-session-log` to record important workflow decisions.
- Use `productize-artifact-log` when a durable artifact is produced.
- Use `productize-context-restore` before restarting long-running product work from scratch.
- Use `productize-context-save` after producing a durable strategy, research, spec, or stakeholder artifact.
- Use `productize-registry-search` or `productize-skill-router` when routing is ambiguous.
- Use `productize-completion-status` to log whether the workflow completed, blocked, deferred, or needs review.

Telemetry standard:

- Keep telemetry local by default in `.productize/` or `PRODUCTIZE_STATE_DIR`.
- Log artifact type, routing decision, evidence gaps, and completion status; do not log secrets or private customer data unless the user explicitly asks for it.

Current skill metadata:

- **Skill**: `design-critique`
- **Lifecycle**: Design
- **Category**: Design
- **Primary artifact**: Design Critique UX/design review with findings, constraints, fixes, and acceptance checks

Give structured design feedback across usability, hierarchy, consistency, accessibility, and polish.

## Argument Hint

`<Figma URL, screenshot, or description>`

## Usage

```text
/design-critique $ARGUMENTS
```

## Inputs

Accept:
- Figma URL.
- Screenshot.
- File reference.
- Live or local page URL.
- Detailed design description.

If a Figma URL, browser URL, or file is available and the relevant tool is connected, inspect the artifact directly. Otherwise ask the user for the minimum design context needed.

Ask for:
- What the design is.
- Who it is for.
- Stage: exploration, refinement, final polish, or handoff.
- Optional focus: mobile, onboarding, checkout, navigation, visual polish, accessibility, or another specific area.

## Critique Framework

### 1. First Impression

Assess the first two seconds:
- What draws the eye first, and is that correct?
- What is the emotional reaction?
- Is the purpose immediately clear?

### 2. Usability

Check:
- Whether users can accomplish the intended goal.
- Navigation clarity.
- Obviousness of interactive elements.
- Step count and avoidable friction.
- Error, empty, loading, and edge states if visible.

### 3. Visual Hierarchy

Check:
- Reading order.
- Emphasis and priority.
- Typography scale and weight.
- Whitespace and grouping.
- CTA prominence.

### 4. Consistency

Check:
- Design system alignment.
- Spacing, color, radius, shadows, and typography consistency.
- Reuse of patterns for similar interactions.
- Naming and language consistency.

### 5. Accessibility

Do a practical pass:
- Contrast risk.
- Touch target size.
- Text readability.
- Form labels and instructions.
- Keyboard and screen reader risks if interaction can be assessed.

For a full WCAG audit, recommend `accessibility-review`.

## Feedback Rules

- Be specific: name the element and the issue.
- Explain why the issue matters to the user or task.
- Suggest an alternative, not just a criticism.
- Include what works well.
- Match feedback to design stage: early exploration gets directional feedback; final polish gets precise issues.
- Avoid generic taste comments unless they connect to purpose, brand, or usability.

## Output Format

```markdown
## Design Critique: [Design Name]

### Overall Impression

[1-2 sentence first reaction: what works and the biggest opportunity]

### Usability

| Finding | Severity | Recommendation |
|---|---|---|
| [Issue] | Critical/Moderate/Minor | [Fix] |

### Visual Hierarchy

- **What draws the eye first**: [Element] - [whether this is correct]
- **Reading flow**: [How the eye moves through the layout]
- **Emphasis**: [Whether the right elements are emphasized]

### Consistency

| Element | Issue | Recommendation |
|---|---|---|
| [Typography/spacing/color/component] | [Inconsistency] | [Fix] |

### Accessibility

- **Color contrast**: [Pass/fail/risk for key text]
- **Touch targets**: [Adequate size?]
- **Text readability**: [Font size, line height, density]
- **Assistive tech risks**: [Keyboard or screen reader risks if visible]

### What Works Well

- [Positive observation 1]
- [Positive observation 2]

### Priority Recommendations

1. **[Most impactful change]** - [Why and how]
2. **[Second priority]** - [Why and how]
3. **[Third priority]** - [Why and how]
```

## Connected Tools

If a design tool is connected:
- Pull the design directly and inspect components, tokens, typography, spacing, layers, and design-system consistency.

If user feedback or research tools are connected:
- Cross-reference critique against recent user feedback, usability findings, or support tickets.

If browser tooling is connected:
- Inspect live behavior, responsive layout, interaction states, focus order, and console errors.
