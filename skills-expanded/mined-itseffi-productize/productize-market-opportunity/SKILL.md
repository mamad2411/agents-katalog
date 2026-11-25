---
name: productize-market-opportunity
description: >-
  Identify, compare, and choose market opportunities for a venture, product, technology, or
  innovation. Use when a founder, entrepreneur, product team, or innovator is choosing which
  market to enter, picking a primary customer segment, evaluating whether a technology has
  better use cases, deciding whether to pivot, comparing growth options, framing a venture for
  investors, or asking variants of "which market should I target", "is this the right
  opportunity", "where should I focus", "should I pivot", or "what else could this be used
  for". Produces filled-in opportunity canvases for the Market Opportunity Set, Attractiveness
  Map, Focus Portfolio Map, and Focus Strategy. Default to this skill when the question is
  where to play rather than how to play.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Market Opportunity

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

- **Skill**: `market-opportunity`
- **Lifecycle**: Strategize
- **Category**: Venture / 0-1
- **Primary artifact**: Market Opportunity venture brief with target segment, wedge, assumptions, and validation path

Create the complete four-part market opportunity artifact set for choosing where a
venture, technology, product, or innovation should play.

Use neutral terms such as `canvas`, `opportunity artifact`, `strategy surface`, or the
artifact names below.

## Argument Hint

`<venture, technology, product, opportunity set, or blank-template request>`

## Usage

```text
/market-opportunity $ARGUMENTS
```

## Required Artifacts

For any complete request, create all four artifacts unless the user explicitly asks for
only one:

1. **Opportunity Overview Canvas**: the three-part overview with opportunity set,
   attractiveness map, and focus portfolio map.
2. **Opportunity Set Builder**: abilities -> applications -> customers -> market
   opportunities.
3. **Attractiveness Evaluator**: potential and challenge ratings for each market
   opportunity.
4. **Focus Portfolio Planner**: primary market opportunity, backup options, growth
   options, and pursue/keep/store decisions.

Load `references/canonical-canvases.md` before creating blank templates, filled
templates, printable layouts, or tables. It defines the exact fields and structure.

Load `references/rating-and-decision-rules.md` before rating opportunities,
classifying map zones, or recommending primary, backup, and growth options.

Load `references/output-formats.md` when the user asks for Markdown, HTML, PDF,
slides, visual canvases, or printable templates.

## Workflow

### 1. Establish the Input Mode

Determine whether the user wants:

- **Blank canvas set**: empty structured artifacts for a team to fill in.
- **Filled canvas set**: completed artifacts from a venture/product/technology idea.
- **Opportunity review**: critique or improve an existing opportunity set.
- **Strategy decision**: choose the primary opportunity and portfolio options.
- **Printable artifact**: create visual HTML/PDF/slide-ready canvases.

If context is missing, ask only for the smallest useful missing piece:

- The venture, product, technology, or core ability.
- Candidate applications.
- Candidate customer groups.
- Existing evidence for demand, market size, economics, implementation, timing, and risks.

### 2. Generate the Market Opportunity Set

Identify the venture's core abilities or technological elements first. Describe them
independent of the envisioned product.

Then generate combinations:

```text
market opportunity = application + customer segment
```

Segment customers precisely. Avoid broad labels like "enterprises" or "consumers"
unless the user has no better information.

### 3. Evaluate Attractiveness

For each market opportunity, rate:

- **Potential**
  - Compelling reason to buy.
  - Market volume.
  - Economic viability.
- **Challenge**
  - Implementation obstacles.
  - Time to revenue.
  - External risks.

Use the four-level rating scale:

```text
Low / Mid / High / Super High
```

Then place each opportunity on the attractiveness map:

- **Gold Mine**
- **Quick Win**
- **Moon Shot**
- **Questionable**

### 4. Design the Focus Portfolio

Choose one **Primary Market Opportunity** based on attractiveness and strategic fit.

For other attractive opportunities, assess relatedness to the primary opportunity:

- **Product relatedness**: shared technological competences, required resources,
  and necessary networks.
- **Market relatedness**: shared customer values and benefits, sales channels, and
  word-of-mouth paths.

Classify each option:

- **Growth Option**: attractive and useful for creating additional value.
- **Backup Option**: attractive and does not share major risks with the primary path.
- **Storage**: documented but not worth active preservation now.

Make one of three action decisions for each option:

- Pursue now.
- Keep open.
- Place in storage.

The final strategy must keep at least one credible backup option and one credible
growth option open unless the available evidence makes that impossible. If impossible,
say what evidence or opportunity generation is missing.

### 5. Tie Strategy to Execution

For completed strategy outputs, include implications for:

- Product and technology modularity.
- IP and defensibility.
- Hiring and capability development.
- Stakeholder and investor alignment.
- Brand and market communication.
- Experiments, assumptions, and learning loops.
- Business Model Canvas, Value Proposition Canvas, and Lean Startup integration when
  the user asks for execution planning.

## Output Rules

- Preserve the canonical field names and rating scales from the reference files.
- Do not collapse the framework into SWOT, generic market sizing, or a feature
  prioritization matrix.
- Be explicit about assumptions and evidence gaps.
- Use tables for editable outputs.
- For visual outputs, use the same four-artifact structure and neutral artifact titles.
- Do not copy long passages from source PDFs. Use the exact operational labels and
  schemas, with original wording for explanations and recommendations.
