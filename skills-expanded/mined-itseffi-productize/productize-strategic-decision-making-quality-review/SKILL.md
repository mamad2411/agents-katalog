---
name: productize-strategic-decision-making-quality-review
description: >-
  Review the quality of a strategic product, innovation, or operating decision. Use when the
  user needs a decision-making artifact that separates facts, assumptions, alternatives, bias
  risks, evidence gaps, and decision safeguards before choosing.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Strategic Decision Making Quality Review

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

- **Skill**: `strategic-decision-making-quality-review`
- **Lifecycle**: Think
- **Category**: Decision Making
- **Primary artifact**: Strategic decision quality review with decision frame, evidence map, option audit, bias risks, safeguards, and recommendation

Use this skill when the work is explicitly about improving a decision, not producing a
generic strategy memo. It is for strategic product, innovation, market-entry, roadmap,
investment, pivot, kill/continue, or executive operating decisions.

Do not use this skill when the user needs only a personal gut check, a decision-rights
RACI/DAVCI map, an A/B test readout, a narrow pre-mortem, or a stakeholder narrative.
Route those to the narrower Productize skill.

## Decision-Making Principles

- Treat decisions as experiments with incomplete information and often only one execution chance.
- Separate rational-choice assumptions from real decision-maker constraints: bounded rationality,
  imperfect information, overload, satisficing, unstable preferences, and future uncertainty.
- Identify when System 1 intuition is helpful pattern recognition and when it is unreliable.
- Use System 2 deliberately for irreversible, high-stakes, unfamiliar, or multi-factor decisions.
- Identify the decision context before applying tools: VUCA, noisy/dynamic innovation,
  stable market, time-sensitive, group-influenced, or politically loaded.
- Review common decision traps: base-rate neglect, representativeness, availability,
  anchoring, framing, confirmation, sunk cost, status quo, optimism, loss/risk aversion,
  and escalation of commitment.
- Improve decision quality with opposite-case reasoning, alternative hypotheses, stress tests,
  root-cause analysis, disconfirming evidence, base rates, explicit thresholds, and review loops.

## Workflow

1. Define the decision, owner, stakes, reversibility, deadline, and required artifact.
2. Separate facts, assumptions, unknowns, constraints, and subjective thresholds.
3. Identify candidate options and the implicit anchor or default option.
4. Audit bias and heuristic risks in the current framing.
5. Add base rates, counter-evidence, alternative hypotheses, and root-cause checks.
6. Create decision criteria and thresholds before recommending.
7. Recommend, defer, test, or ask for a blocking input.
8. Record what would change the decision later.

## Output Contract

Return:

```markdown
# Strategic Decision Making Quality Review

## 1. Decision Frame
Decision:
Decision owner:
Deadline:
Stakes:
Reversibility:
Context type:

## 2. Known / Assumed / Missing / Risky
Known facts:
Assumptions:
Missing evidence:
Risky leaps:

## 3. Options And Default Anchor
Option A:
Option B:
Option C:
Current default or anchor:
Why the default may be sticky:

## 4. Decision Trap Audit
Base-rate neglect:
Representativeness:
Availability:
Anchoring:
Framing / loss-gain presentation:
Confirmation:
Sunk cost / escalation:
Status quo:
Optimism:
Loss or risk aversion:

## 5. Decision Safeguards
Opposite case:
Alternative hypotheses:
Disconfirming evidence to seek:
Root-cause check:
Thresholds before deciding:
Decision review date:

## 6. Recommendation
Recommend / ask / defer / test:
Rationale:
Confidence:
What would change this decision:
Next action:
```

## Failure Modes

- Produces a generic strategy recommendation without auditing decision process quality.
- Treats the user's first framing as neutral rather than checking anchors, losses, defaults,
  and missing alternatives.
- Lists biases without connecting them to the specific decision and safeguards.
- Recommends before separating known facts, assumptions, missing evidence, and risky leaps.
