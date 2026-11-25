---
name: productize-product-market-fit-cycle
description: >-
  Run the product-market fit cycle to decide whether a startup or product problem is product,
  positioning, or go-to-market. Use for PMF diagnosis, minimum viable segment, product
  hypothesis testing, startup iteration, learn-decide loops, and start-small expansion
  strategy.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Product-Market Fit Cycle

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

- **Skill**: `product-market-fit-cycle`
- **Lifecycle**: Growth
- **Category**: Growth
- **Primary artifact**: PMF cycle diagnosis with product, positioning, and go-to-market learning loop

Use this skill when the user needs to decide what to change next in the search for product-market fit.

Do not use it for pure growth funnel optimization after PMF, brand narrative work, or broad market selection unless the question is whether the product, positioning, or go-to-market should change.

## Core Cycle

Use this loop:

1. Start from the big vision.
2. Define the product hypothesis.
3. Identify the minimum viable segment (MVS): the narrow customer group that can prove the wedge.
4. Build the minimum viable business pieces:
   - positioning
   - MVP or product experience
   - go-to-market motion
5. Test with qualitative and quantitative evidence.
6. Analyze results using relevant metrics, often AARRR.
7. Learn what failed or worked.
8. Decide whether to modify:
   - product
   - positioning
   - go-to-market
   - segment
   - business model
9. Iterate, pivot, or expand.

## Start Small Before Expanding

Prefer a narrow MVS when uncertainty is high. The goal is not to prove the total addressable market first; it is to find a segment with a sharp pain, clear trigger, reachable channel, and strong evidence of value.

Use expansion only after the wedge shows repeatable value creation, retention, and a believable path to economics.

## Diagnosis Questions

Ask:

- Is the product solving a real problem for a specific segment?
- Is the positioning making the value obvious to that segment?
- Is the go-to-market motion reaching the right people at the right moment?
- Are users activating but not retaining?
- Are users retaining but not referring or paying?
- Are prospects interested but not converting?
- Are customers using it for a different job than expected?
- Is the segment too broad, too expensive to reach, or too weakly motivated?

## Workflow

1. State the current hypothesis: segment, job/problem, promise, product, GTM, business model.
2. Map evidence by type:
   - qualitative pull
   - usage/activation
   - retention
   - willingness to pay
   - referral/word of mouth
   - sales cycle and objections
3. Identify the weakest assumption.
4. Classify the likely issue:
   - product problem
   - positioning problem
   - go-to-market problem
   - segment problem
   - pricing/business model problem
5. Define the next loop: what to change, what to hold constant, what evidence will decide.
6. Give a stop/iterate/expand recommendation.

## Output

Return:

- **Current PMF Hypothesis**: segment, job/problem, promise, product, GTM, monetization.
- **Evidence Map**: what is known, unknown, and inferred.
- **PMF Diagnosis**: product, positioning, GTM, segment, or business model issue.
- **Minimum Viable Segment**: narrow segment definition and why it is the right wedge.
- **Next Experiment Loop**: change, hold constant, test method, metrics, timeline, decision rule.
- **Decision**: iterate, pivot, pause, or expand.
- **Expansion Logic**: only if evidence supports moving beyond the current MVS.

## Quality Bar

- Do not declare PMF from excitement, signups, press, or demos alone.
- Do not change product, positioning, and GTM all at once unless the current hypothesis is invalid.
- Keep the segment narrow enough that evidence is interpretable.
- Tie every recommendation to a decision rule for the next loop.
