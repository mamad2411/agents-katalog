---
name: productize-brand-equity-diagnostics
description: >-
  Diagnose brand health and brand equity using awareness, familiarity, associations, and Brand
  Asset Valuator dimensions. Use for brand performance, differentiation, relevance, esteem,
  knowledge, brand strength, brand stature, and brand portfolio diagnosis.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Brand Equity Diagnostics

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

- **Skill**: `brand-equity-diagnostics`
- **Lifecycle**: Strategize
- **Category**: Marketing
- **Primary artifact**: Brand Equity Diagnostics strategy memo with choices, tradeoffs, risks, and recommended next move

Use this skill when the user needs to assess whether a brand is healthy, distinctive, valuable, or at risk.

Do not use it for brand voice creation, creative campaign selection, or growth funnel diagnosis unless the task is explicitly about brand equity.

## Core Models

Brand equity comes from marketing effects uniquely attributable to the brand name. Diagnose it through:

- **Awareness and familiarity**: people know the brand and can recognize or recall it.
- **Associations**: people hold strong, favorable, and unique associations.
- **Behavioral reality**: customers are often apathetic, low-attention, and not deeply loyal.
- **Availability**: the brand is mentally and physically easy to notice and buy.

Use Brand Asset Valuator (BAV) as the main diagnostic frame:

- **Differentiation**: how distinct and meaningfully different the brand feels.
- **Relevance**: how appropriate and useful the brand is for the audience.
- **Esteem**: how respected and well-regarded the brand is.
- **Knowledge**: how familiar and understood the brand is.

Interpret:

- **Brand Strength** = Differentiation + Relevance. This is the future-facing signal.
- **Brand Stature** = Esteem + Knowledge. This is the current-status signal.

## BAV Quadrants

- **Leadership**: high strength, high stature. Defend distinctiveness and availability while avoiding complacency.
- **Unrealized or Emerging Potential**: high strength, low stature. Build awareness, distribution, credibility, and repetition.
- **Eroding Potential**: low strength, high stature. The brand is known but losing distinctiveness or relevance.
- **New or Unfocused**: low strength, low stature. Clarify meaning, audience, proof, and salience.

## Workflow

1. Clarify the category, audience, market, and competitor set.
2. Gather evidence: surveys, brand tracking, search, share of voice, reviews, win/loss, social listening, sales feedback, usage, pricing power.
3. Score or qualitatively rate awareness/familiarity, associations, differentiation, relevance, esteem, and knowledge.
4. Place the brand in the BAV quadrant.
5. Explain the main equity problem:
   - unknown
   - known but not distinctive
   - distinctive but not relevant
   - relevant but not respected
   - respected but not salient
   - strong but hard to buy
6. Recommend strategic actions for mental availability, physical availability, distinctive assets, association building, and proof.

## Output

Return:

- **Evidence Base**: what data was used and what is missing.
- **Brand Equity Snapshot**: awareness/familiarity and association diagnosis.
- **BAV Assessment**: D/R/E/K ratings with rationale.
- **Quadrant Placement**: leadership, unrealized/emerging potential, eroding potential, or new/unfocused.
- **Primary Equity Problem**: the root brand health issue.
- **Strategic Implications**: what to protect, build, fix, or stop doing.
- **Action Plan**: concrete moves across communications, product experience, distribution, distinctive assets, and measurement.
- **Tracking Metrics**: leading and lagging brand indicators.

## Quality Bar

- Do not assume customers want a deep relationship with the brand.
- Distinguish fame from esteem, and awareness from clear associations.
- Do not recommend "more content" unless it builds a specific association or availability gap.
- Tie brand actions to measurable equity dimensions.
