---
name: productize-stakeholder-moo-objections-and-product-derailment-risks
description: >-
  Stakeholder MOO objections and product derailment risks. Use when the user needs a product
  workflow for stakeholder management related to stakeholder moo objections and product
  derailment risks. Trigger terms: stakeholder-management, risk-management, product-strategy,
  communication.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Stakeholder MOO objections and product derailment risks

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

- **Skill**: `stakeholder-moo-objections-and-product-derailment-risks`
- **Lifecycle**: Align
- **Category**: Stakeholder Communication
- **Primary artifact**: Stakeholder MOO objections and product derailment risks stakeholder narrative with audience, message, risks, asks, and follow-up owner

Use this skill to run the Productize prompt contract for **Stakeholder MOO objections and product derailment risks**.

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
Produce a high-quality deliverable for: Stakeholder MOO objections and product derailment risks.
Success metric:
- Completes all required tasks and decision logic from the prompt instructions.
- Output is specific, evidence-based, and actionable.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required analysis steps, sections, or validation logic.
- Keep recommendations/outputs grounded in the input context; avoid generic filler.
- Apply MOO (Most Obvious Objection) analysis to stakeholder risk/derailment scenarios.
- First collect only essential context; ask concise follow-ups with a maximum of 5 questions total if needed.
- If sufficient context exists, produce:
- `BLUF` with top 3 stakeholder-voice MOOs, why obvious, confidence, and QBQ.
- Stakeholder objection mapping with objection type, MOO rank, QBQ, loss/gain framing, frequency x magnitude, evidence requested, counter-moves, and decision thresholds.
- Red-team drill questions, proof and pre-wire plan, executive one-slide summary, risk register, and vibe-check behaviors.
- Use plain, scannable language; label assumptions/uncertainties; prioritize obvious objections first; include numbers where possible.
- Ensure edge-case objections are covered (data quality, privacy, model eval/bias when relevant, scale/support load, contracts/channel conflict/cannibalization, change management, measurement validity).
- If context is insufficient, output only:
- A 5-question minimal follow-up.
- A clearly labeled provisional top-3 MOO guess.

FORMAT
Return exactly this structure:

If context is insufficient:
Minimal Follow-up (5 questions)
1. [question]
2. [question]
3. [question]
4. [question]
5. [question]
Provisional Top-3 MOO Guess (clearly labeled)
- [MOO 1]
- [MOO 2]
- [MOO 3]

If context is sufficient:
A) BLUF - Top 3 MOOs
- [stakeholder-voice objection + why obvious + confidence + QBQ]

B) Stakeholder Objection Map
| Stakeholder Group | Objection | Type | MOO Rank (1-5) | QBQ | Loss vs Gain | Freq x Magnitude | Evidence Asked | Counter-moves | Decision Threshold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [row] | [row] | [row] | [row] | [row] | [row] | [row] | [row] | [row] | [row] |

C) Red-Team Drill
- [5-10 sharp questions]

D) Proof & Pre-Wire Plan
Fast proof stack:
- [test]
Artifacts:
- [artifact]
Pre-wire scripts:
- Email/Slack template (<=120 words): [text]
- 60-sec live opener: [text]
- If-they-say-X, you-say-Y snippets (top 3): [text]

E) Executive Slide (1 slide)
Title: [text]
- Why now: [text]
- Top MOO + QBQ: [text]
- Evidence to date: [text]
- Next proof step + decision gate: [text]
- Ask (people/time/budget) + trade-offs: [text]

F) Risk Register
| Risk | Trigger | Early Warning Signal | Owner | Mitigation | Kill-switch |
| --- | --- | --- | --- | --- | --- |
| [row] | [row] | [row] | [row] | [row] | [row] |

G) Vibe Check
Behaviors to avoid:
- [item]
Grounded behaviors to show:
- [item]

FAILURE
- Does not follow the conditional output path (insufficient-context vs sufficient-context).
- Missing required MOO sections (`A` through `G`) when context is sufficient.
- Objection map lacks required fields (type, rank, QBQ, evidence, threshold, counter-moves).
- Red-team, proof/pre-wire, risk register, or vibe-check sections are missing or superficial.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
