---
name: productize-write-spec
description: >-
  Write a feature spec or PRD from a problem statement or feature idea. Use when turning a
  vague idea into a structured document, scoping goals and non-goals, defining success metrics
  and acceptance criteria, or breaking a big ask into phases.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Write Spec

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

- **Skill**: `write-spec`
- **Lifecycle**: Plan
- **Category**: Delivery
- **Primary artifact**: Feature spec or PRD with scope, success metrics, and acceptance criteria

Write a feature specification or product requirements document.

## Argument Hint

`<feature or problem statement>`

## Usage

```text
/write-spec $ARGUMENTS
```

## Extended Reference

Load `references/extended-reference.md` when the request mentions `create prd`, `8-section prd`, `feature spec`, `release planning`. Use this reference material to sharpen this Productize skill.

## Workflow

### 1. Understand the Feature

Accept a feature name, problem statement, user request, or vague idea.

Ask conversationally for the most important missing context:
- User problem and affected segment.
- Success metrics.
- Constraints, dependencies, deadlines.
- Prior attempts or related solutions.

### 2. Pull Context

If connected, search project tracker, docs, research, design files, and meeting notes for related work, requirements, mockups, decisions, and dependencies.

If tools are not connected, proceed from user-provided context and state assumptions.

### 3. Generate PRD

Include:
- **Problem Statement**: 2-3 sentences with user, pain, frequency, and impact.
- **Goals**: 3-5 measurable outcomes.
- **Non-Goals**: 3-5 out-of-scope items with rationale.
- **User Stories**: "As a [user], I want [capability], so that [benefit]."
- **Requirements**: P0, P1, P2 with acceptance criteria.
- **Success Metrics**: leading and lagging indicators with targets and measurement method.
- **Open Questions**: tagged by owner and blocking status.
- **Timeline Considerations**: hard deadlines, dependencies, phasing.

### 4. Acceptance Criteria

Use Given/When/Then or checklist format. Cover:
- Happy path.
- Error states.
- Empty states.
- Boundary conditions.
- Negative cases.

### 5. Scope Rules

- Be opinionated about v1 scope.
- If everything is P0, challenge it.
- Require scope addition to come with scope removal or timeline extension.
- Separate v1 from future considerations.
- Keep requirements behavior-focused, not implementation-prescriptive unless necessary.

## Output Rules

Use clear markdown headers and tables where helpful. Keep the spec skimmable. Open questions must be genuinely unresolved.
