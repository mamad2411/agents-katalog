---
name: productize-prds-from-industry-and-feature-specifications
description: >-
  PRDs from industry and feature specifications. Use when the user needs a product workflow
  for business analysis related to prds from industry and feature specifications. Trigger
  terms: pm, prd, requirements, documentation, business-analysis.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# PRDs from industry and feature specifications

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

- **Skill**: `prds-from-industry-and-feature-specifications`
- **Lifecycle**: Plan
- **Category**: Delivery
- **Primary artifact**: PRDs from industry and feature specifications delivery brief with scope, requirements, priorities, risks, and acceptance criteria

Use this skill to run the Productize prompt contract for **PRDs from industry and feature specifications**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{INDUSTRY}}
- {{COMPANY_NAME}}
- {{FEATURE_NAME}}
- {{DEVELOPMENT_STAGE}}
- {{CURRENT_KNOWLEDGE}}
- {{CURRENT_SOLUTION}}
</provided_inputs>

GOAL
Create a complete, implementation-ready PRD for `FEATURE_NAME` in the specified `INDUSTRY` and `DEVELOPMENT_STAGE`.
Success metric:
- Covers all required PRD sections with actionable detail.
- Aligns recommendations to current stage, known constraints, and existing solution context.
- Uses explicit assumptions where information is missing.
- Follows the required output structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip any required PRD section.
- Ground requirements in `CURRENT_KNOWLEDGE` and `CURRENT_SOLUTION`; do not contradict provided context without explicit rationale.
- Use the exact PRD heading/table structure specified in `FORMAT`.
- Keep requirements testable and implementation-oriented where possible.
- Maintain a professional, industry-appropriate tone.

FORMAT
Return exactly this structure:

<PRD>
# [Product Name]

## About
[High-level overview of the product and goal.]

## Market Insights
[Market context, competitors, trends, and target users.]

## Problem
[Core user problem, pain points, and why existing solutions are insufficient.]

## Solution
[Proposed AI product solution and how it addresses the problem.]

## Feature Prioritization
| Feature | Reach | Impact | Confidence | Effort | RICE Score | Priority |
|---------|-------|--------|------------|--------|------------|----------|
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

## Requirements
**Functional Requirements:**
- FR1:
- FR2:
- FR3:

**AI/ML Model Requirements:**
- MR1:
- MR2:
- MR3:

**Non-Functional Requirements:**
- NFR1:
- NFR2:
- NFR3:

## Challenges
[Key product, technical, data, and go-to-market challenges.]

## Positioning
| Use Case | Target User | Key Benefit | Differentiator |
|----------|-------------|-------------|----------------|
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

## Metrics
[Success metrics and north star metric.]

## Rollout Plan
- **Stakeholders & Communication**
  - [Stakeholder groups and communication plan]

- **Roll-out Strategy**
  - [Launch phases, gating criteria, and post-GA plan]
</PRD>

FAILURE
- Any required section/table/list item pattern from `FORMAT` is missing or materially incomplete.
- Content is generic and not grounded in provided inputs.
- Requirements are not actionable/testable.
- Development-stage alignment is missing.
- Required output schema is missing or malformed.
