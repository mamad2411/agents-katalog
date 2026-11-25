---
name: productize-ai-product-evaluation-from-recommendation-canvas-framework
description: >-
  AI product evaluation from Recommendation Canvas framework. Use when the user needs a
  product workflow for decision making related to ai product evaluation from recommendation
  canvas framework. Trigger terms: pm, decision-making, ai-product, recommendation-canvas,
  strategy.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# AI product evaluation from Recommendation Canvas framework

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

- **Skill**: `ai-product-evaluation-from-recommendation-canvas-framework`
- **Lifecycle**: Think
- **Category**: Strategy
- **Primary artifact**: AI product evaluation from Recommendation Canvas framework decision-framing brief with issue tree, assumptions, options, and recommended next step

Use this skill to run the Productize prompt contract for **AI product evaluation from Recommendation Canvas framework**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- [No explicit variables declared; use provided context.]
</provided_inputs>

GOAL
Produce a complete, executive-ready AI Recommendation Canvas for a specific problem/persona, plus improvement suggestions and a go/no-go decision.
Success metric:
- Canvas is coherent, measurable, and defensible across business outcome, product outcome, solution hypothesis, and success metrics.
- Unknowns are explicitly marked; no invented facts.
- Includes 3-5 concrete improvement suggestions and a clear go/no-go recommendation.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required workflow:
  1. Gather/normalize available context and identify missing critical inputs.
  2. Tighten outcomes into SMART form.
  3. Build the canvas with explicit unknowns and assumptions.
  4. Add 3-5 improvement suggestions.
  5. Provide a go/no-go recommendation with rationale.
- If multiple personas exist, choose one primary persona and note secondary impacts.
- For regulated data, include compliance and data-minimization constraints.
- For generative AI use cases, include safety/evaluation/abuse-monitoring considerations.
- Distinguish risks to investigate (pre-decision) vs risks to monitor (post-decision).
- Keep language concise, outcome-first, and metric-linked.
- Do not invent facts; mark unknowns explicitly.

FORMAT
Return exactly this structure:

```md
# AI Recommendation Canvas

## Product Name
- [Concise, memorable name]

## Business Outcome
- [Direction][Metric][Outcome][Context][Acceptance Criteria]

## Product Outcome
- [Direction][Metric][Outcome][Persona context][Acceptance]

## The Problem Statement
### Problem Statement Narrative
- [Persona + context + constraints]
- [2-3 sentence first-person narrative]

## Solution Hypothesis
### Hypothesis Statement
- **If we** ...
- **for** ...
- **then we will** ...

### Tiny Acts of Discovery (Experiments)
- Viability: ...
- Value: ...
- Feasibility: ...
- Safety: ...

### Proof-of-Life (Success Criteria)
- Quantitative: ...
- Qualitative: ...
- Operational: ...

## Positioning Statement
### Value Proposition
**For** ...  
**that need** ...  
**[Product Name]** **is a** ...  
**that** ...

### Differentiation Statement
**Unlike** ...  
**[Product Name]** **provides** ...

## Assumptions & Unknowns
- ...

## Issues/Risks to Investigate (PESTEL)
- Political: ...
- Economic: ...
- Social: ...
- Technological: ...
- Environmental: ...
- Legal: ...

## Issues/Risks to Monitor (PESTEL)
- Political: ...
- Economic: ...
- Social: ...
- Technological: ...
- Environmental: ...
- Legal: ...

## Value Justification
### Is this Valuable?
- [Absolutely yes / Yes with caveats / No with alternatives / Absolutely no]

### Solution Justification (Executive-Ready)
1. Financial Impact — ...
2. Strategic Fit — ...
3. Customer Value — ...
4. Operational Feasibility — ...
5. Risk Mitigation — ...

## Success Metrics (SMART)
1. Efficiency — ...
2. Quality — ...
3. Adoption — ...
4. Financial — ...
5. Safety — ...

## What’s Next (Strategic Steps)
1. Data Readiness — ...
2. Prototype — ...
3. Pilot — ...
4. Scale — ...
5. Governance — ...
6. Commercialization — ...
```

<review>
1. [Improvement suggestion]
2. [Improvement suggestion]
3. [Improvement suggestion]
[Add 3-5 total]
</review>

<go_no_go_recommendation>
[Go / No-Go / Go with conditions] - [Brief rationale tied to outcomes, feasibility, and risk]
</go_no_go_recommendation>

FAILURE
- Canvas is not rendered as a single Markdown code block.
- Required canvas sections are missing or materially incomplete.
- Missing `<review>` section with 3-5 suggestions.
- Missing `<go_no_go_recommendation>` section.
- Claims are generic or not grounded in provided inputs.
- Unknowns/assumptions are present but not explicitly marked.
