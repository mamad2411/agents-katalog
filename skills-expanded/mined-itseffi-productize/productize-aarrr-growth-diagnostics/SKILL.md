---
name: productize-aarrr-growth-diagnostics
description: >-
  Diagnose product or startup growth using AARRR pirate metrics, CAC, LTV, channel
  performance, activation, retention, referral, revenue, and growth engine fit. Use for funnel
  leakage, growth bottlenecks, SaaS conversion, and go-to-market growth analysis.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# AARRR Growth Diagnostics

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

- **Skill**: `aarrr-growth-diagnostics`
- **Lifecycle**: Growth
- **Category**: Growth
- **Primary artifact**: AARRR growth diagnosis and prioritized growth action plan

Use this skill when the user needs to understand where growth is leaking and which part of the growth system should be fixed first.

Do not use it for broad market selection, brand narrative, or PMF loop decisions unless the immediate task is funnel diagnosis.

## Core Funnel

AARRR means:

1. **Acquisition**: people arrive or become aware enough to visit, install, inquire, or start.
2. **Activation**: people experience first value or reach the product's "wow" moment.
3. **Retention**: people come back and continue receiving value.
4. **Referral**: people invite, share, advocate, or create word-of-mouth.
5. **Revenue**: people pay, expand, renew, or create monetizable value.

Some businesses measure revenue before referral. Preserve the user's funnel order when it is intentional; otherwise use the sequence above.

## Unit Economics

Always inspect:

- **CAC**: customer acquisition cost. How much the business spends to acquire a customer or unit.
- **LTV/CLV**: lifetime value. How much revenue or gross profit the customer generates over time.
- **Payback**: time required to recover CAC.
- **Channel cost and quality**: volume, cost, conversion, and retained value by channel.

## Growth Engines

Classify the current or intended engine:

- **Sales-led**: human sales motion, qualification, pipeline, account expansion.
- **Marketing-led**: paid/owned/earned channels, content, campaigns, demand generation.
- **Product-led**: self-serve acquisition, activation, usage, expansion, virality.
- **Community-led**: community participation, advocacy, identity, peer learning, network effects.

## Workflow

1. **Map the funnel**
   - Define the exact event for each AARRR stage.
   - Use counts, rates, and time windows where possible.

2. **Find the bottleneck**
   - Compare stage conversion, drop-off, time-to-stage, and segment differences.
   - Identify whether the constraint is traffic quality, onboarding, value delivery, habit, monetization, or advocacy.

3. **Inspect channels**
   - Evaluate each acquisition channel by volume, cost, conversion, retained users, and revenue quality.
   - Watch for channels that look efficient at signup but fail at activation or retention.

4. **Check activation**
   - Define the first-value or "wow" moment.
   - Compare retained versus churned users by activation actions, timing, and sequence.

5. **Check retention**
   - Use cohort retention when available.
   - Distinguish product value failure from lifecycle communication, service, pricing, or expectation mismatch.

6. **Check referral**
   - Use viral growth factor:
     - X = percent of users who invite others
     - Y = average number of invites sent
     - Z = percent of invitees who accept
     - Viral factor = X * Y * Z

7. **Prioritize interventions**
   - Recommend fixing upstream only when downstream economics support it.
   - Do not scale acquisition into weak activation or retention.

## Output

Return:

- **Growth Model**: current engine and funnel definitions.
- **AARRR Scorecard**: counts, conversion rates, benchmark/target if known, confidence.
- **Leakage Diagnosis**: biggest bottleneck and evidence.
- **Channel Diagnosis**: volume, cost, conversion, quality, and CAC implications.
- **Unit Economics**: CAC, LTV/CLV, payback, and risks.
- **Activation/Retention/Referral Findings**: specific issues and opportunities.
- **Priority Moves**: ranked actions with expected mechanism, metric, owner if known, and time-to-signal.
- **Instrumentation Gaps**: missing events, cohorts, segments, or attribution.

## Quality Bar

- Do not optimize acquisition before checking activation and retention.
- Do not treat signups as success unless first value and retention are healthy.
- Separate vanity metrics from value metrics.
- Tie recommendations to measurable stage movement.
