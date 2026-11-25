---
name: productize-design-handoff
description: >-
  Generate developer handoff specs from a design. Use when a design is ready for engineering
  and needs a spec sheet covering layout, design tokens, component props, interaction states,
  responsive breakpoints, edge cases, and animation details.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Design Handoff

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

- **Skill**: `design-handoff`
- **Lifecycle**: Design
- **Category**: Design
- **Primary artifact**: Design Handoff UX/design review with findings, constraints, fixes, and acceptance checks

Generate comprehensive developer handoff documentation from a design.

## Argument Hint

`<Figma URL or design description>`

## Usage

```text
/design-handoff $ARGUMENTS
```

## Inputs

Accept:
- Figma URL.
- Screenshot.
- File reference.
- Live or local page URL.
- Detailed design description.

If a Figma URL, browser URL, or file is available and the relevant tool is connected, inspect the artifact directly. Otherwise work from the provided description or ask only for missing details that materially affect implementation.

Capture:
- What screen, feature, or component is being handed off.
- Target platform and tech stack, if known.
- Design system or token names, if known.
- Intended responsive breakpoints.
- Known edge cases or constraints.

## What to Include

### Visual Specifications

Document:
- Exact measurements for padding, margins, widths, heights, gaps, and alignment.
- Design token references for colors, typography, spacing, radius, shadows, and motion.
- Raw values only when tokens are unavailable, ideally with a suggested token mapping.
- Responsive breakpoints and behavior.
- Component variants and visual states.

### Interaction Specifications

Document:
- Click, tap, submit, cancel, and navigation behavior.
- Hover, focus, active, selected, disabled, loading, success, warning, and error states.
- Transitions and animations, including duration and easing.
- Gesture support such as swipe, pinch, long press, or drag when relevant.

### Content Specifications

Document:
- Character limits.
- Truncation, wrapping, and overflow behavior.
- Empty states.
- Loading states.
- Error states.
- Required copy, helper text, labels, and validation messages.

### Edge Cases

Document:
- Minimum and maximum content.
- Long internationalized strings.
- Slow or failed network responses.
- Missing, partial, or stale data.
- Permission and unauthenticated states where relevant.

### Accessibility

Document:
- Focus order.
- ARIA labels and roles.
- Keyboard interactions.
- Screen reader announcements.
- Touch target size.
- Contrast risks or requirements.

## Principles

1. **Do not assume silently**: If a value, state, or behavior is not specified, label it as an assumption or open question.
2. **Use tokens first**: Reference `spacing-md` instead of `16px` when the token is known.
3. **Show all states**: Include default, hover, active, focused, disabled, loading, error, and empty states when applicable.
4. **Describe the reason**: Explain important responsive or interaction decisions so engineers can make consistent tradeoffs.

## Output

```markdown
## Handoff Spec: [Feature/Screen Name]

### Overview
[What this screen or feature does, plus user context.]

### Layout
[Grid system, breakpoints, responsive behavior, spacing, alignment, and sizing rules.]

### Design Tokens Used
| Token | Value | Usage |
|-------|-------|-------|
| `color-primary` | #[hex] | CTA buttons, links |
| `spacing-md` | [X]px | Between sections |
| `font-heading-lg` | [size/weight/family] | Page title |

### Components
| Component | Variant | Props | Notes |
|-----------|---------|-------|-------|
| [Component] | [Variant] | [Props] | [Special behavior] |

### States and Interactions
| Element | State | Behavior |
|---------|-------|----------|
| [CTA Button] | Hover | [Background darkens or token changes] |
| [CTA Button] | Loading | [Spinner, disabled, preserves width] |
| [Form] | Error | [Border, message placement, focus behavior] |

### Responsive Behavior
| Breakpoint | Changes |
|------------|---------|
| Desktop (>1024px) | [Default layout] |
| Tablet (768-1024px) | [What changes] |
| Mobile (<768px) | [What changes] |

### Edge Cases
- **Empty state**: [What to show when no data exists]
- **Long text**: [Wrapping, truncation, tooltip, or expansion rules]
- **Loading**: [Skeleton, spinner, timeout, or progressive rendering behavior]
- **Error**: [Error state appearance and recovery action]

### Animation / Motion
| Element | Trigger | Animation | Duration | Easing |
|---------|---------|-----------|----------|--------|
| [Element] | [Trigger] | [Description] | [ms] | [easing] |

### Accessibility Notes
- [Focus order]
- [ARIA labels and roles needed]
- [Keyboard interactions]
- [Screen reader announcements]

### Open Questions
- [Question] - [Owner or decision needed]
```

## Connected Tool Guidance

If a design tool is connected:
- Pull exact measurements, tokens, component names, variants, and layer metadata from the design.
- Export or reference assets needed for implementation.
- Compare against the existing design system when possible.

If a project tracker is connected:
- Link the handoff to the implementation ticket if the user asks.
- Draft sub-tasks for layout, components, states, accessibility, and QA.

## Tips

- Share the Figma link to enable exact measurements, tokens, and component info.
- Mention edge cases such as "what happens with 100 items" so the handoff covers boundary behavior.
- Specify the tech stack so implementation notes can match the codebase.
