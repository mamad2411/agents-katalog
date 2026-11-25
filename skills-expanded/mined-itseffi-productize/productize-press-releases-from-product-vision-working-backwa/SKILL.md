---
name: productize-press-releases-from-product-vision-working-backwards
description: >-
  Press releases from product vision (Working Backwards). Use when the user needs a product
  workflow for presentation & communication related to press releases from product vision
  (working backwards). Trigger terms: storytelling, press-release, working-backwards,
  product-strategy, communication, influence.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Press releases from product vision (Working Backwards)

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

- **Skill**: `press-releases-from-product-vision-working-backwards`
- **Lifecycle**: Align
- **Category**: Marketing
- **Primary artifact**: Press releases from product vision (Working Backwards) stakeholder narrative with audience, message, risks, asks, and follow-up owner

Use this skill to run the Productize prompt contract for **Press releases from product vision (Working Backwards)**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{PRODUCT_OR_SERVICE}}
- {{TARGET_PERSONAS}}
- {{FEATURES_USPS}}
- {{COMPANY_CONTEXT}}
- {{PROBLEMS_GOALS}}
- {{EVIDENCE_METRICS}}
- {{AUDIENCES_CHANNELS}}
- Optional: {{LAUNCH_DATE_PRICING_AVAILABILITY}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: Press releases from product vision (Working Backwards).
Success metric:
- Produces a credible Working Backwards-style launch press release that is specific and evidence-backed.
- Includes exactly two quotes (executive + customer/partner) and at least one concrete proof point.
- Clearly states availability/pricing/requirements and a direct call to action.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs; if required launch details are missing, use bracketed placeholders like `[CITY]`, `[DATE]`, `[STAT]`.
- If placeholders are used, append a short `Fill These Gaps` checklist once after the release.
- Output must be Markdown only (no XML/JSON wrappers).
- Target length: 350-550 words (plus Media Contact block).
- Tone: visionary but plain-spoken, AP-style clarity, active voice, short paragraphs.
- Avoid hype words (for example `revolutionary`, `game-changing`) unless in quotes.
- Include at least one concrete proof point (metric, benchmark, ROI, independent signal, certification, or analyst note).
- Include exactly two quotes:
  - one executive quote (vision/why now),
  - one customer/partner quote (outcome/benefit).
- Use the structure labels in `FORMAT` verbatim.
- Convert each feature into a clear user/business outcome.
- No unverifiable regulated claims, no competitor bashing, no guaranteed-future promises.

FORMAT
Return exactly this structure:

# [Product Name]
Subhead: [One-line value proposition]

Dateline: [CITY], [STATE/PROVINCE], [COUNTRY] — [MONTH DAY, YEAR]

**Lede (Intro, 2-3 sentences):**
[Announcement summary with who/what/for whom/outcome]

**Body Paragraph (What it does & why it matters):**
[How it works, why now, and executive quote]

**Feature Highlights:**
- [Feature 1]: [What it is] -> [Outcome]
- [Feature 2]: [What it is] -> [Outcome]
- [Feature 3]: [What it is] -> [Outcome]
[Optional features 4-6]

**Evidence & Context:**
[At least one concrete proof point with precise number/signal]

**Customer/Partner Quote:**
"[Outcome-focused quote]," said [Name, Title, Company].

**Availability, Pricing, Requirements:**
- Availability: [Date/Region/Tiers]
- Pricing: [Model/Currency/Tiers]
- Requirements: [Integrations/devices/plans/compliance prerequisites]

**Call to Action:**
[Learn more/contact/demo links]

**Boilerplate:**
[Company background, mission, and relevant credibility]

**Media Contact**
[Name] — [Title]
Phone: [Number] • Email: [Email]
Press Kit: [Link]

[Optional: Fill These Gaps
- [Missing item 1]
- [Missing item 2]]

FAILURE
- Required section labels from `FORMAT` are missing, renamed, malformed, or incomplete.
- Word count is materially outside 350-550 (excluding Media Contact).
- Not exactly two quotes, or quotes are not executive + customer/partner types.
- No concrete proof point is included.
- Feature bullets do not translate to outcomes.
- Placeholder gaps exist but `Fill These Gaps` is missing.
- Output contains XML/JSON wrappers.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
