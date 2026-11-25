---
name: productize-strategic-crux-diagnosis-and-strategy-design
description: >-
  Strategic crux diagnosis and strategy design. Use when the user needs a product workflow for
  product strategy related to strategic crux diagnosis and strategy design. Trigger terms:
  strategy, decision-making, prioritization, product, leadership.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Strategic crux diagnosis and strategy design

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

- **Skill**: `strategic-crux-diagnosis-and-strategy-design`
- **Lifecycle**: Strategize
- **Category**: Strategy
- **Primary artifact**: Strategic crux diagnosis and strategy design strategy memo with choices, tradeoffs, risks, and recommended next move

Use this skill to run the Productize prompt contract for **Strategic crux diagnosis and strategy design**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{CONTEXT_SCOPE}}
- {{CURRENT_STATE}}
- {{DESIRED_FUTURE}}
- {{TIME_HORIZON}}
- {{CUSTOMERS_JTBD}}
- {{UVP_TODAY}}
- {{COMPETITIVE_LANDSCAPE}}
- {{KEY_CONSTRAINTS}}
- {{ASSETS_STRENGTHS}}
- {{RISKS_NON_NEGOTIABLES}}
- {{USER_INSIGHTS}}
- {{UNIT_ECONOMICS}}
- {{STAKEHOLDERS_DECISION_RIGHTS}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: Strategic crux diagnosis and strategy design.
Success metric:
- Identifies the strategic crux with evidence-backed rationale.
- Proposes a leveraged strategy with explicit trade-offs and testable milestones.
- Provides a concrete execution plan with experiments, metrics, and risks.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs; if critical items are missing, ask up to 6 concise clarification questions first.
- Separate facts, assumptions, and inferences; label disconfirming evidence and uncertainties.
- Identify the crux and choose a leveraged strategy with explicit trade-offs.
- Provide options table, chosen strategy, 12–18 week moves, experiments, metrics, risks, and resources.
- If constraints make the goal infeasible, propose renegotiations with quantified trade-offs.

FORMAT
Return exactly this structure:

1) Executive Summary (<=200 words)

2) Strategic Narrative

3) Evidence Pack

4) Crux Definition

5) Options & Trade-offs
| Option | Core Bet | Expected Impact (with math) | Cost (money/teams) | Time-to-First-Signal | Risks | Reversibility | Why It Might Fail |

6) Chosen Strategy (Leverage Thesis)

7) Strategic Moves (12–18 weeks)
| Move | Owner | Start | End | Dependencies | Weekly Leading Indicator | Target | Risk & Mitigation |

8) Experiments to Prove/Disprove

9) Metrics & Monitoring

10) Risks, Preconditions, and Constraint Renegotiations

11) Resource Plan

12) Decision Log & Next Checkpoint

Appendices (tables)
1. Assumptions -> Tests Map: | Assumption | Test/Experiment | When | Owner | Decision Rule |
2. Roadmap (Quarter): | Week | Move | Deliverable | Confidence |
3. Stakeholder Map: | Stakeholder | Interest/Influence | What They Need to See |

FAILURE
- Any required section/table in `FORMAT` is missing, malformed, or incomplete.
- Crux is not explicitly defined or not tied to evidence.
- Options table is missing or lacks required columns.
- Moves lack owners, timeline, or leading indicators.
- Experiments lack hypothesis/metrics or stop/scale rules.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
