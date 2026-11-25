---
name: productize-roadmap-update
description: >-
  Update, create, or reprioritize a product roadmap. Use when adding an initiative, deciding
  what moves to make room, shifting priorities after new information, moving timelines after a
  dependency slip, or building a Now/Next/Later view.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Roadmap Update

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

- **Skill**: `roadmap-update`
- **Lifecycle**: Strategize
- **Category**: Stakeholder Communication
- **Primary artifact**: Roadmap decision memo with options, tradeoffs, and updated Now/Next/Later plan

Update, create, or reprioritize a product roadmap.

## Argument Hint

`<update description>`

## Usage

```text
/roadmap-update $ARGUMENTS
```

## Workflow

### 1. Understand Current State

If a project tracker is connected, pull roadmap items, status, owners, target dates, overdue work, at-risk items, and recently completed work.

If no tracker is connected, ask the user to paste or describe the roadmap in any format.

### 2. Determine Operation

Identify the requested operation:

- **Add item**: gather name, description, priority, effort, timeframe, owner, dependencies, and what moves to make room.
- **Update status**: not started, in progress, at risk, blocked, completed, cut. For at-risk or blocked, capture blocker and mitigation.
- **Reprioritize**: ask what changed, apply a framework if useful, and show before/after.
- **Move timeline**: ask why, identify downstream impacts, and flag hard-deadline risks.
- **Create roadmap**: ask timeframe, format, goals, themes, and initiative list.

### 3. Choose Format

Use the format that fits the audience:
- Now / Next / Later for broad communication.
- Quarterly themes for strategy alignment.
- OKR-aligned roadmap for metric-backed planning.
- Timeline view for execution planning with dependencies.

### 4. Generate Roadmap Summary

Include:
- Status overview: counts in progress, completed, at risk, blocked.
- Roadmap items grouped by timeframe or theme.
- Risks and dependencies with owners and need-by dates.
- Changes this update: added, removed, reprioritized, timeline shifts, status changes.

Use tables where helpful.

### 5. Prioritization Tools

Use only when they clarify tradeoffs:
- RICE: Reach x Impact x Confidence / Effort.
- MoSCoW: Must, Should, Could, Won't.
- ICE: Impact x Confidence x Ease.
- Value vs Effort: quick wins, big bets, fill-ins, avoid.

## Rules

- Roadmaps are capacity-constrained. When adding something, ask what comes off or moves.
- Surface dependency risk early.
- Communicate changes by naming what changed, why, what tradeoff was made, and who is affected.
- Do not create false precision for work that is still directional.
