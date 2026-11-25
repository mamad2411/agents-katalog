---
name: productize-design-system
description: >-
  Audit, document, or extend a design system. Use when checking for naming inconsistencies or
  hardcoded values across components, writing documentation for component variants, states,
  and accessibility notes, or designing a new pattern that fits the existing system.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Design System

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

- **Skill**: `design-system`
- **Lifecycle**: Design
- **Category**: Design
- **Primary artifact**: Design System UX/design review with findings, constraints, fixes, and acceptance checks

Manage a design system by auditing for consistency, documenting components, or designing new patterns.

## Argument Hint

`[audit | document | extend] <component or system>`

## Usage

```text
/design-system audit
/design-system document [component]
/design-system extend [pattern]
```

## Modes

### Audit

Use when the user wants a full or targeted review of design system consistency.

Check:
- Component naming consistency.
- Variant and state naming consistency.
- Token coverage for colors, typography, spacing, borders, shadows, and motion.
- Hardcoded values or arbitrary one-off styles.
- Missing states, variants, documentation, or accessibility notes.
- Components that overlap or solve the same problem inconsistently.

### Document

Use when the user wants documentation for an existing component.

Document:
- Purpose and when to use it.
- Variants, sizes, states, and props.
- Content guidance.
- Accessibility requirements.
- Do and do-not usage guidance.
- Framework-appropriate code examples if the implementation stack is known.

### Extend

Use when the user wants a new component or pattern that fits the existing system.

Define:
- The problem or system gap.
- Related existing components and why they are not enough.
- Proposed API, variants, states, and tokens.
- Accessibility behavior.
- Migration or adoption notes.
- Open questions that need design or engineering review.

## Components of a Design System

### Design Tokens

Atomic values that define the visual language:
- Colors: brand, semantic, neutral, and data colors.
- Typography: scale, weights, families, and line heights.
- Spacing: scale, component padding, layout gaps.
- Borders: radius and width.
- Shadows: elevation levels.
- Motion: durations and easings.

### Components

Reusable UI elements with defined:
- Variants such as primary, secondary, and ghost.
- States such as default, hover, active, disabled, loading, and error.
- Sizes such as sm, md, and lg.
- Behavior, interactions, and animations.
- Accessibility roles, names, and keyboard behavior.

### Patterns

Common UI solutions combining components:
- Forms: input groups, validation, submission.
- Navigation: sidebar, tabs, breadcrumbs.
- Data display: tables, cards, lists.
- Feedback: toasts, modals, inline messages.

## Principles

1. **Consistency over novelty**: The system exists so teams do not reinvent common UI.
2. **Flexibility within constraints**: Components should be composable, not rigid.
3. **Document the usable contract**: If a variant, prop, state, or accessibility behavior is not documented, teams will guess.
4. **Version and migrate**: Breaking changes need migration paths, deprecated aliases, or adoption guidance.

## Output: Audit

```markdown
## Design System Audit

### Summary
**Components reviewed:** [X] | **Issues found:** [X] | **Score:** [X/100]

### Naming Consistency
| Issue | Components | Recommendation |
|-------|------------|----------------|
| [Inconsistent naming] | [List] | [Standard to adopt] |

### Token Coverage
| Category | Defined | Hardcoded Values Found |
|----------|---------|------------------------|
| Colors | [X] | [X] instances of hardcoded hex |
| Spacing | [X] | [X] instances of arbitrary values |
| Typography | [X] | [X] instances of custom fonts/sizes |

### Component Completeness
| Component | States | Variants | Docs | Score |
|-----------|--------|----------|------|-------|
| Button | Complete | Complete | Partial | 8/10 |
| Input | Complete | Partial | Missing | 5/10 |

### Priority Actions
1. [Most impactful improvement]
2. [Second priority]
3. [Third priority]
```

## Output: Document

```markdown
## Component: [Name]

### Description
[What this component is and when to use it.]

### Variants
| Variant | Use When |
|---------|----------|
| [Primary] | [Main actions] |
| [Secondary] | [Supporting actions] |

### Props / Properties
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| [prop] | [type] | [default] | [description] |

### States
| State | Visual | Behavior |
|-------|--------|----------|
| Default | [description] | [behavior] |
| Hover | [description] | [interaction] |
| Active | [description] | [interaction] |
| Disabled | [description] | Non-interactive |
| Loading | [description] | [animation] |

### Accessibility
- **Role**: [ARIA role]
- **Keyboard**: [Tab, Enter, Escape behavior]
- **Screen reader**: [Announced as...]

### Do and Do Not
| Do | Do Not |
|----|--------|
| [Best practice] | [Anti-pattern] |

### Code Example
[Framework-appropriate code snippet.]
```

## Output: Extend

```markdown
## New Component: [Name]

### Problem
[What user need or system gap this component addresses.]

### Existing Patterns
| Related Component | Similarity | Why It Is Not Enough |
|-------------------|------------|----------------------|
| [Component] | [What is shared] | [What is missing] |

### Proposed Design

#### API / Props
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| [prop] | [type] | [default] | [description] |

#### Variants
| Variant | Use When | Visual |
|---------|----------|--------|
| [Variant] | [Scenario] | [Description] |

#### States
| State | Behavior | Notes |
|-------|----------|-------|
| Default | [Description] | [Notes] |
| Hover | [Description] | [Interaction] |
| Disabled | [Description] | Non-interactive |
| Loading | [Description] | [Animation] |

#### Tokens Used
- Colors: [Which tokens]
- Spacing: [Which tokens]
- Typography: [Which tokens]

### Accessibility
- **Role**: [ARIA role]
- **Keyboard**: [Expected interactions]
- **Screen reader**: [Announced as...]

### Open Questions
- [Decision that needs design review]
- [Edge case to resolve]
```

## Connected Tool Guidance

If a design tool is connected:
- Audit components directly in the design file for naming, variants, token usage, and layer structure.
- Pull component properties and layer structure for documentation.
- Compare proposed extensions against existing libraries before inventing new patterns.

If a knowledge base is connected:
- Search for existing component documentation and usage guidelines.
- Draft updates in the appropriate documentation format.

## Tips

- Start with an audit before deciding what to change.
- Document components while designing or updating them.
- Prioritize coverage over perfection: broad usable documentation is better than perfect docs for only a few components.
