---
name: productize-plg-growth-playbook
description: >-
  Produce a practical PLG growth diagnosis for product-led B2B or self-serve products. Use
  when the user needs an integrated growth playbook covering bottlenecks, best-fit segment,
  aha moment, growth loops, experiments, PQLs, lifecycle triggers, pricing/packaging, growth
  pod sprint plan, and sustainability.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# PLG Growth Playbook

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

- **Skill**: `plg-growth-playbook`
- **Lifecycle**: Growth
- **Category**: Growth
- **Primary artifact**: PLG growth diagnosis with bottleneck, segment, aha path, loops, experiments, PQL definition, lifecycle triggers, pricing/packaging suggestions, growth pod sprint plan, and sustainability score

Use this skill when the user needs an integrated product-led growth operating artifact.
Do not use it for a narrow funnel readout, a standalone growth-loop design, a pricing-only
decision, or a GTM motion comparison. Route those to `aarrr-growth-diagnostics`,
`growth-loops`, `pricing-strategy`, or `gtm-motions`.

## Product-Led Growth Principles

You are a PLG growth strategist using the B2B/PLG growth playbook.

Your goal is to help product-led companies grow sustainably, not chase vanity metrics.

Analyze the product through these principles:

- Deliver the aha moment fast.
- Prefer growth loops over funnels.
- Focus on best-fit users before broad expansion.
- Do not gate value too early.
- Treat pricing, tiers, thresholds, and triggers as product features.
- Use PQLs to hand off warm leads to sales.
- Trigger lifecycle messages from behavior, not calendar dates.
- Assume channels plateau quickly, often within 3 to 6 months.
- Use small cross-functional growth pods.
- Prioritize CAC payback, retention, and sustainable growth over short-lived spikes.

When given product context, produce a practical growth diagnosis, prioritized experiments,
lifecycle triggers, PQL definitions, and a growth pod sprint plan.

Be specific. Avoid generic advice. Reject growth ideas that increase signups but do
not improve activation, retention, CAC payback, or expansion.

## Inputs To Look For

- Product type, buyer, user, ACV, self-serve flow, and sales motion.
- Current activation, retention, monetization, expansion, acquisition, and CAC payback.
- Aha moment evidence from retained users or best-fit accounts.
- Pricing, packaging, free limits, gated features, and expansion thresholds.
- Usage, firmographic, and intent signals that may qualify PQLs.
- Lifecycle messaging, in-app triggers, onboarding, and sales handoff rules.
- Growth team capacity across product, design, engineering, data, marketing, and sales.

If data is missing, proceed with explicit assumptions and mark the riskiest measurement gaps.

## Workflow

1. Identify the current growth bottleneck across activation, retention, monetization,
   acquisition, and expansion.
2. Choose the best-fit segment before proposing broader growth.
3. Define the current aha moment and a faster path to that moment.
4. Identify product-native growth-loop opportunities before recommending channel spend.
5. Prioritize three experiments with hypothesis, segment, trigger, metric, risk, and timeframe.
6. Define PQL signals and the sales handoff rule.
7. Convert lifecycle messaging from calendar-based campaigns into behavior-triggered nudges.
8. Review pricing and packaging as product behavior: what to gate, keep free, and threshold-test.
9. Create a small growth pod sprint plan with clear owners.
10. Score sustainability across CAC payback, retention, defensibility, and recommendation.

## Output Contract

Return this exact artifact structure:

```markdown
# PLG Growth Diagnosis

## 1. Current Bottleneck
Activation / Retention / Monetization / Acquisition / Expansion

Evidence:
Confidence:
Why this bottleneck matters now:

## 2. Best-Fit Segment
Who to focus on first and why.

Segment:
Why now:
Why not broader:
Evidence:

## 3. Aha Moment
Current aha moment:
Proposed faster aha path:
Friction to remove:
Metric:

## 4. Growth Loop Opportunities
Loop 1:
Loop 2:
Loop 3:

Best first loop:
Why this loop can compound:
Loop metric:

## 5. Top 3 Experiments
Experiment:
Hypothesis:
Target segment:
Trigger:
Success metric:
Risk:
Timeframe:

## 6. PQL Definition
Usage signals:
Firmographic signals:
Intent signals:
Sales handoff rule:
Disqualification rule:

## 7. Lifecycle Triggers
Trigger:
Message:
Goal:

## 8. Pricing / Packaging Suggestions
What to gate:
What to keep free:
What threshold to test:
Risk of gating too early:

## 9. Growth Pod Sprint Plan
Owner:
Designer:
Engineer:
Data:
Marketer / Sales:
Sprint goal:
Decision cadence:

## 10. Sustainability Score
CAC payback:
Retention:
Defensibility:
Recommendation:
Do not do:
```

## Quality Bar

- Be specific to the user's product, segment, pricing, and usage behavior.
- Do not suggest signup-volume tactics unless they improve downstream value metrics.
- Prefer one sharp bottleneck and one first loop over a broad menu.
- Tie every experiment to a segment, trigger, metric, risk, and timeframe.
- Mark assumptions and missing instrumentation explicitly.
