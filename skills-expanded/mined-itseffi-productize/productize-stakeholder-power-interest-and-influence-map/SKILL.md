---
name: productize-stakeholder-power-interest-and-influence-map
description: >-
  Stakeholder Power–Interest & Influence Map. Use when the user needs a product workflow for
  stakeholder management related to stakeholder power–interest & influence map. Trigger terms:
  stakeholder-management, influence, internal-politics, communication.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Stakeholder Power–Interest & Influence Map

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

- **Skill**: `stakeholder-power-interest-and-influence-map`
- **Lifecycle**: Align
- **Category**: Decision Making
- **Primary artifact**: Stakeholder decision influence map with power-interest matrix, influence pyramid, role identity risks, engagement plan, and mitigations

Use this skill to run the Productize prompt contract for **Stakeholder Power–Interest & Influence Map**.

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
Produce a high-quality deliverable for: "Stakeholder Power–Interest & Influence Map".
Success metric:
- Completes all required tasks and decision logic from the prompt instructions.
- Output is specific, evidence-based, and actionable.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required analysis steps, sections, or validation logic.
- Keep recommendations/outputs grounded in the input context; avoid generic filler.
- Build a stakeholder strategy output from initiative context and stakeholder details.
- If critical stakeholder context is missing, ask exactly 3 targeted questions; if still unclear, state assumptions and proceed.
- Produce:
- A Power-Interest 2x2 matrix with named stakeholders per quadrant.
- An Influence Pyramid (Top/Middle/Base) including informal power roles (gatekeepers, super-connectors, executive assistants where relevant).
- High-power stakeholder profiles covering goals/metrics, concerns/risks, preferred comms style, and political risks.
- Decision-making profile covering role identity, expected role behavior, likely information filters, in-group/out-group dynamics, and susceptibility to role pressure when relevant.
- A tailored engagement plan per high-power stakeholder (cadence/channel, format/owner, key message, quick win, fallback).
- A plan to inform/mobilize high-interest low-power stakeholders.
- Success signals/metrics and top 3 prioritized political pitfalls with mitigations.

FORMAT
Return exactly this structure:

Power-Interest Matrix
| Quadrant | Stakeholders |
| --- | --- |
| High Power / High Interest | [names] |
| High Power / Low Interest | [names] |
| Low Power / High Interest | [names] |
| Low Power / Low Interest | [names] |

Influence Pyramid
- Top: [names + rationale]
- Middle: [names + rationale]
- Base: [names + rationale]

High-Power Profiles
| Stakeholder | Goals & Success Metrics | Likely Concerns/Risks | Role Identity / Expected Behavior | Preferred Communication Style | Political Risks for Me |
| --- | --- | --- | --- | --- | --- |
| [row] | [row] | [row] | [row] | [row] | [row] |

Decision-Making Influence Risks
- Role pressure: [who may decide from role expectation rather than evidence]
- In-group / out-group effects: [groups and likely interpretation gap]
- Authority or conformity risk: [risk and mitigation]
- Common-information risk: [shared info that may crowd out unique evidence]

Engagement Plan
| Stakeholder | Cadence & Channel | Format | Owner | Key Message | Quick Win | Fallback |
| --- | --- | --- | --- | --- | --- | --- |
| [row] | [row] | [row] | [row] | [row] | [row] | [row] |

Advocacy Plan (High-Interest / Low-Power)
- [how to inform]
- [how to mobilize advocacy]

Success Signals & Metrics
- [signal/metric]

Risks & Mitigations
1. [pitfall + mitigation]
2. [pitfall + mitigation]
3. [pitfall + mitigation]

Assumptions
- [assumption or "None"]

FAILURE
- Any required section/table is missing or materially incomplete.
- High-power stakeholders are not profiled and mapped to tailored engagement actions.
- Informal influence is ignored or unsupported.
- Role identity, in-group/out-group effects, or group decision influence risks are ignored when relevant.
- Top 3 political pitfalls and mitigations are missing, unprioritized, or generic.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.

## Extended Reference

Load `references/extended-reference.md` when the request mentions `power interest grid`, `stakeholder communication plan`, `raci`, `escalation path`. Use this reference material to sharpen this Productize skill.
