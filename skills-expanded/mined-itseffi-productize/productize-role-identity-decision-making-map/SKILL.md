---
name: productize-role-identity-decision-making-map
description: >-
  Map how role identity, organizational identity, in-group/out-group dynamics, and role
  expectations shape a product or innovation decision. Use when the user needs to understand
  why stakeholders decide according to role pressure, identity, or social context.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Role Identity Decision Making Map

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

- **Skill**: `role-identity-decision-making-map`
- **Lifecycle**: Align
- **Category**: Decision Making
- **Primary artifact**: Role identity decision-making map with stakeholder roles, logic of appropriateness, social context risks, decision impact, and process adjustments

Use this skill when a decision is being shaped by roles, identity, group membership, or
organizational self-image. It is especially useful for cross-functional product decisions,
innovation resistance, transformation work, roadmap tradeoffs, and decisions where people
argue from their "hat" rather than from the evidence.

## Decision-Making Principles

- People classify situations through role identities and expected role behavior.
- Role identity creates a "logic of appropriateness": what someone feels they should do
  because of their function, hierarchy, profession, or organizational role.
- Role salience changes with context, timing, habits, incentives, and pressure from others.
- Cross-functional teams are not automatically better decision makers; role conflict can
  reduce integration or produce defensive information processing.
- Organizational identity can guide good decisions, but strong identity can block innovation
  and strategic change.
- Social categorization creates in-groups and out-groups, changing trust, similarity,
  evidence weighting, and willingness to support change.

## Workflow

1. Define the decision and stakeholders.
2. Identify each stakeholder's formal role, informal role, salient identity, and expected behavior.
3. Map role pressure, incentives, status risk, and identity threat.
4. Identify in-group/out-group dynamics and organizational identity constraints.
5. Predict how each role identity will search for, interpret, and weight information.
6. Recommend role reframing, process changes, and evidence framing to improve the decision.

## Output Contract

Return:

```markdown
# Role Identity Decision Making Map

## 1. Decision Context
Decision:
Decision owner:
Stakeholders:
Why role identity matters:

## 2. Role Identity Map
| Stakeholder | Formal role | Informal role | Salient identity | Expected role behavior | Decision pressure |
| --- | --- | --- | --- | --- | --- |
| [row] | [row] | [row] | [row] | [row] | [row] |

## 3. Logic Of Appropriateness
Role-based assumptions:
Unwritten rules:
What each stakeholder feels they must protect:
Role segmenters vs integrators:

## 4. Social Context Risks
In-groups:
Out-groups:
Identity threat:
Organizational identity constraint:
Innovation resistance:

## 5. Decision Impact
Information each role will seek:
Information each role may discount:
Likely alliances:
Likely blockers:
Where evidence may be distorted:

## 6. Decision Process Adjustments
Role reframing:
Different hats to assign:
Private input needed:
Evidence framing:
Psychological safety needs:
Decision owner move:

## 7. Recommendation
Best next move:
Who to pre-wire:
What to say:
What to avoid:
```

## Failure Modes

- Reduces stakeholder behavior to power/interest only, ignoring role identity and social context.
- Treats cross-functional participation as automatically sufficient.
- Speculates about motives without grounding in role, incentive, behavior, or context.
- Omits organizational identity and in-group/out-group effects.
