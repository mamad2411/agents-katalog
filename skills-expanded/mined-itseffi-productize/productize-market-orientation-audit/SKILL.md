---
name: productize-market-orientation-audit
description: >-
  Audit whether an organization is truly market oriented using intelligence generation,
  intelligence dissemination, and responsiveness. Use for customer-centricity, marketing
  culture, organizational diagnosis, market sensing, and scorecard-based improvement plans.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Market Orientation Audit

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

- **Skill**: `market-orientation-audit`
- **Lifecycle**: Strategize
- **Category**: Marketing
- **Primary artifact**: Market Orientation Audit strategy memo with choices, tradeoffs, risks, and recommended next move

Use this skill when the user wants to diagnose how well an organization senses markets, shares customer/competitor insight internally, and acts on that insight.

Do not use it for brand health, campaign evaluation, or product-market fit unless the question is specifically about organizational market orientation.

## Core Model

Market orientation is an organization-wide culture and operating system for creating customer value. It has three dimensions:

- **Intelligence generation**: how the organization detects customer, competitor, collaborator, technology, and regulatory changes.
- **Intelligence dissemination**: how quickly and effectively insight spreads across functions.
- **Responsiveness**: how fast and well the organization acts on market intelligence.

## Scorecard

Use a 1-5 scale:

- 5 = Strongly agree
- 4 = Agree
- 3 = Neither agree nor disagree
- 2 = Disagree
- 1 = Strongly disagree

Each dimension has 8 items. Dimension scoring:

- 29-40 = High
- 20-28 = Moderate
- 8-19 = Low

Total scoring:

- 86-120 = High
- 60-85 = Moderate
- 24-59 = Low

### Intelligence Generation

1. We have interdepartmental meetings at least once a quarter to discuss market trends and developments.
2. We are quick to detect fundamental shifts in our industry, such as competition, technology, or regulation.
3. We periodically review the likely effect of environmental changes on customers.
4. We are fast to detect changes in customer product and service preferences.
5. People discuss customers' future needs with other functions or departments.
6. We do a lot of in-house market research.
7. We survey key customers at least once a year to assess product and service quality.
8. We meet key clients at least once a year to learn what products or services they will need in the future.

### Intelligence Dissemination

1. When something important happens to a major customer or market, the whole business knows quickly.
2. When one department learns something important about competitors, it quickly alerts other departments.
3. We would never ignore changes in customer product or service needs.
4. When customers want a product or service modification, involved teams make concerted efforts to respond.
5. We periodically review product or service development to ensure it aligns with key customer needs.
6. We have communication systems that speed dissemination of important customer-related information.
7. All functions and departments are responsive to each other's needs and requests.
8. When a customer complains or gives feedback, we quickly share it with anyone who can act on it.

### Responsiveness

1. It takes very little time to decide how to respond to competitor product or service changes.
2. We can implement new ideas, marketing plans, product redesigns, or service enhancements in a timely fashion.
3. Several functions periodically plan responses to changes in the business environment.
4. If a major competitor aggressively targeted a key customer, we would consider a response immediately.
5. We quickly act on customer complaints and feedback.
6. Customer-facing employees have latitude to solve customer problems without excessive red tape.
7. People here tend to talk more about opportunities than problems.
8. When we see a new opportunity to create customer value, we act quickly.

## Workflow

1. Collect scores from the user or run a facilitated self-assessment.
2. Compute dimension totals and total score.
3. Identify the weakest dimension and the lowest individual items.
4. Diagnose root causes across incentives, structure, tooling, decision rights, data access, rituals, and culture.
5. Translate findings into operating changes, not just research recommendations.
6. Define a 30/60/90-day improvement plan and measurement cadence.

## Output

Return:

- **Score Summary**: dimension scores, total score, high/moderate/low rating.
- **Pattern Diagnosis**: what the scores imply about market sensing, sharing, and action.
- **Lowest Items**: the specific behaviors causing the largest gap.
- **Organizational Hurdles**: structure, incentives, data, rituals, authority, culture.
- **Improvement Plan**: 30/60/90-day actions.
- **Operating Metrics**: indicators to track improvement.

## Quality Bar

- Do not equate customer-facing friendliness with market orientation.
- Treat market orientation as cross-functional.
- Separate collecting insight from acting on insight.
- Recommend concrete operating changes, not generic "talk to customers more" advice.
