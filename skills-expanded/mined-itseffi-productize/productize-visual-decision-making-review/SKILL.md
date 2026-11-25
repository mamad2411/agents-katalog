---
name: productize-visual-decision-making-review
description: >-
  Review how visuals, charts, diagrams, canvases, dashboards, or slides may shape a product
  decision. Use when the user needs to identify visual bias, overconfidence, misleading
  emphasis, graph validity issues, or decision stickiness caused by the visual artifact.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Visual Decision Making Review

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

- **Skill**: `visual-decision-making-review`
- **Lifecycle**: Think
- **Category**: Decision Making
- **Primary artifact**: Visual decision-making review with salience map, decision value, visual risks, corrections, and decision recommendation

Use this skill when the visual itself is part of the decision-making risk. This is not a
chart-building skill. It reviews whether a visual artifact helps decision quality or creates
false confidence, hidden emphasis, misleading comparisons, or sticky first impressions.

Route to `data-visualization` when the user needs to choose chart types or create charts.
Use this skill when the question is whether the visual will distort or improve a decision.

## Decision-Making Principles

- Visuals expand working memory and can turn implicit information into a shared decision format.
- Repeated visual frameworks can improve pattern recognition and knowledge transfer.
- Visuals also create decision risks: detail can imply relevance, polish can imply correctness,
  formatting can hide weak evidence, and emphasized elements can blind the group to alternatives.
- Original visuals can become sticky anchors, especially in meetings and executive reviews.
- Cultural, language, and perception differences can change how a visual is interpreted.

## Workflow

1. Identify the decision the visual is meant to support.
2. Identify the visual type and what it makes salient.
3. Check whether the visual offloads complexity or oversimplifies the problem.
4. Audit validity, scale, labeling, uncertainty, source, and construction errors.
5. Identify emphasis, omissions, anchors, and overconfidence risks.
6. Recommend visual changes and decision-process safeguards.

## Output Contract

Return:

```markdown
# Visual Decision Making Review

## 1. Decision Context
Decision:
Audience:
Visual artifact:
Decision moment:

## 2. What The Visual Makes Salient
Main message:
Highlighted elements:
Hidden or de-emphasized elements:
Likely first impression:

## 3. Decision Value
Working-memory support:
Pattern recognition:
Shared format:
Knowledge transfer:

## 4. Visual Decision Risks
Relevance overconfidence:
Formatting illusion:
Validity / construction issues:
Robustness / stickiness:
Blind-sighting or emphasis risk:
Cultural or interpretation risk:

## 5. Corrections
Visual changes:
Evidence labels:
Alternative views:
Uncertainty or caveats:
Meeting safeguards:

## 6. Decision Recommendation
Use as-is / revise / replace / supplement:
Why:
Next action:
```

## Failure Modes

- Gives generic chart advice without analyzing decision impact.
- Treats polished visuals as reliable without checking evidence and construction.
- Fails to identify what the visual emphasizes and what it hides.
- Omits decision-process safeguards such as alternative views, caveats, or private review.
