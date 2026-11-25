---
name: productize-innovation-decision-making-heuristics
description: >-
  Design tailored decision-making heuristics for uncertain innovation work. Use when the user
  needs simple decision rules for product bets, discovery, investment, pivot, prioritization,
  or opportunity selection in noisy and changing contexts.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Innovation Decision Making Heuristics

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

- **Skill**: `innovation-decision-making-heuristics`
- **Lifecycle**: Think
- **Category**: Decision Making
- **Primary artifact**: Innovation decision-making heuristic playbook with context fit, tailored rules, exceptions, and feedback loop

Use this skill when a team needs a practical decision rule, not a one-off recommendation.
The output should help the team decide repeatedly under uncertainty while avoiding arbitrary
or off-the-shelf rules.

## Decision-Making Principles

- Heuristics are useful shortcuts when the environment is noisy, dynamic, uncertain, or
  time-sensitive and more information does not necessarily clarify direction.
- Heuristics fail when applied blindly, when nuance matters, or when the environment is stable
  enough for more complete analysis.
- Effective heuristics should come from the user's real business challenge, constraints,
  evidence, and observed feedback.
- A good heuristic makes tradeoffs explicit: speed versus accuracy, exploration versus focus,
  safety versus moonshot, and learning versus commitment.
- Heuristics must be reviewed and refined through practical experience.

## Workflow

1. Identify the recurring decision type and the context in which it appears.
2. Classify the environment: noisy/dynamic/uncertain, stable, time-sensitive, multi-factor,
   politically loaded, or high-stakes irreversible.
3. Define what the heuristic should optimize: learning, speed, risk control, focus, upside,
   user value, revenue, retention, or strategic fit.
4. Identify where naive heuristics could fail.
5. Create 3-5 tailored decision rules with explicit triggers and exceptions.
6. Add a feedback loop so the rule can improve after use.

## Output Contract

Return:

```markdown
# Innovation Decision Making Heuristics

## 1. Recurring Decision
Decision type:
Who decides:
Frequency:
Time pressure:
Stakes:

## 2. Decision Environment
Context:
Noise / uncertainty:
Information quality:
Reversibility:
Stable analysis possible:

## 3. What The Rules Should Optimize
Primary objective:
Secondary objective:
Tradeoff to accept:
Tradeoff to avoid:

## 4. Heuristic Failure Risks
Where shortcuts help:
Where shortcuts fail:
Bias risks:
Escalation or sunk-cost risk:

## 5. Tailored Decision Rules
Rule 1:
Use when:
Exception:
Evidence needed:

Rule 2:
Use when:
Exception:
Evidence needed:

Rule 3:
Use when:
Exception:
Evidence needed:

## 6. Feedback And Refinement
Signal to track:
Review cadence:
Who updates the rule:
When to retire the rule:
```

## Failure Modes

- Provides generic principles instead of concrete decision rules.
- Creates rules that ignore the user's actual uncertainty, constraints, and feedback loops.
- Treats heuristics as always good or always bad rather than context-dependent.
- Omits exceptions and review mechanisms.
