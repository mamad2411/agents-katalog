---
name: productize-netmba-competitor-analysis
description: >-
  NETMBA competitor analysis. Use when the user needs a product workflow for product strategy
  related to netmba competitor analysis. Trigger terms: strategy, competition, porter,
  competitor-analysis.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# NETMBA competitor analysis

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

- **Skill**: `netmba-competitor-analysis`
- **Lifecycle**: Strategize
- **Category**: Strategy
- **Primary artifact**: NETMBA competitor analysis strategy memo with choices, tradeoffs, risks, and recommended next move

Use this skill to run the Productize prompt contract for **NETMBA competitor analysis**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{OUR_COMPANY_BUSINESS_UNIT}}
- {{FOCAL_COMPETITORS}}
- {{GEOGRAPHY_SEGMENT}}
- {{TIME_HORIZON}}
- {{PROVIDED_DATA_AND_CONSTRAINTS}}
- {{DESIRED_DEPTH}}  # Brief | Standard | Deep
</provided_inputs>

GOAL
Produce a high-quality deliverable for: NETMBA competitor analysis.
Success metric:
- Produces a rigorous competitor analysis using Objectives, Current Strategy, Assumptions, and Capabilities.
- Converts analysis into ranked likely moves and actionable counter-moves.
- Keeps key claims auditable with explicit source tags and confidence levels.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs; if key fields are missing, state assumptions explicitly.
- Use Porter/NETMBA competitor model components explicitly:
  - Objectives, Current Strategy, Assumptions, Capabilities.
- Separate facts from inferences; mark inferred claims with `(Inference)` and source tags `[S#]` when indirectly supported.
- Quantify where possible; use ranges if exact values are unavailable.
- Add confidence level (`High/Med/Low`) with one-line justification in major sections.
- Keep all key claims auditable via `Evidence Pack` source tags.
- Use exact section headers from `FORMAT`; do not add extra sections.
- Depth handling:
  - `Brief`: cap around 600 words total.
  - `Standard`: normal detail.
  - `Deep`: expanded sub-bullets and richer tables.
- Include required tables:
  - Capabilities Heatmap,
  - Likely Moves Matrix,
  - Counter-Moves Plan.

FORMAT
Return exactly this structure:

1. Executive Snapshot (<=120 words)

2. Objectives (Future Goals)

3. Current Strategy

4. Assumptions

5. Capabilities (Resources & Weaknesses)

Capabilities Heatmap
| Capability | Rating (High/Medium/Low) | Evidence/Notes |
| --- | --- | --- |
| R&D |  |  |
| Cost position |  |  |
| Brand |  |  |
| Data assets |  |  |
| Channel strength |  |  |
| Supply chain |  |  |
| Regulatory savvy |  |  |
| Hiring velocity |  |  |

6. Likely Moves & Response Profile

Likely Moves Matrix
| Move | Likelihood (1-5) | Impact (1-5) | Earliest timing | Leading indicators |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

7. Implications for Us

Counter-Moves Plan
| Our move | Objective | Dependency | Owner | T-minus signals |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

8. Evidence Pack
- [S1] [Source title] ([Date])
- [S2] [Source title] ([Date])

9. Unknowns & Validation Plan

10. Appendix
- KPI table: [price levels, feature parity, share estimates, CAC/LTV clues if available]
- Timeline of notable moves (last 12-24 months)

FAILURE
- Any required section header/table from `FORMAT` is missing, malformed, or materially incomplete.
- One or more core model components (Objectives/Current Strategy/Assumptions/Capabilities) lacks concrete, testable claims.
- Likely moves are not logically connected to the four core model components.
- Key claims lack `[S#]` references to `Evidence Pack`.
- Confidence levels are missing in major sections.
- `DESIRED_DEPTH=Brief` output is materially overlong.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
