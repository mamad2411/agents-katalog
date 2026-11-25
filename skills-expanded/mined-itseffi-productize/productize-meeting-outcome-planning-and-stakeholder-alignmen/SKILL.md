---
name: productize-meeting-outcome-planning-and-stakeholder-alignment
description: >-
  Meeting Outcome Planning and Stakeholder Alignment. Use when the user needs a product
  workflow for stakeholder management related to meeting outcome planning and stakeholder
  alignment. Trigger terms: stakeholder-management, executive-communication,
  meeting-facilitation, org-politics, decision-making.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Meeting Outcome Planning and Stakeholder Alignment

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

- **Skill**: `meeting-outcome-planning-and-stakeholder-alignment`
- **Lifecycle**: Align
- **Category**: Decision Making
- **Primary artifact**: Decision meeting plan with objective, decider, stakeholder map, agenda, anti-groupthink controls, decision rule, and follow-up

Use this skill to run the Productize prompt contract for **Meeting Outcome Planning and Stakeholder Alignment**.

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
Produce a high-quality deliverable for: "Meeting Outcome Planning and Stakeholder Alignment".
Success metric:
- Completes all required tasks and decision logic from the prompt instructions.
- Output is specific, evidence-based, and actionable.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required analysis steps, sections, or validation logic.
- Keep recommendations/outputs grounded in the input context; avoid generic filler.
- Timebox intake and planning for PM meeting prep (default 5-15 minutes, ask only essential questions unless enough context already exists).
- Clarify outcome, decision need/decider, stakeholder map, risks/politics, constraints, and success criteria.
- Produce a copy-ready meeting plan that includes:
- TL;DR (`<=60` words).
- Meeting Brief with objective, type mix percentages (Information/Discovery/Discussion/Decision/Alignment), decision statement/decider, stakeholder map, time-boxed agenda, key messages/proofs, objections/counters, give-get plan, artifacts, and exit checklist.
- When a decision is required, include anti-groupthink mechanics: silent write or private input, private vote when appropriate, explicit dissent, challenger, sequence control for speaker order, and a clear decision rule.
- Follow-up Email template with objective recap, covered points, decisions, open items, notes/links, and next checkpoint.
- Async alternative plan when a meeting is unnecessary (with steps, owners, deadlines).
- Apply edge-case logic: missing decider, pure info-share closure, high conflict handling, explicit assumptions.
- End with a 5-item read-aloud checklist: Goal, Decision/Decider, Stakeholders, Agenda times, Next steps.

FORMAT
Return exactly this structure:

TL;DR
[<=60 words]

Meeting Brief
One-sentence objective: [text]
Type mix: Information [x]%, Discovery [x]%, Discussion [x]%, Decision [x]%, Alignment [x]%
Decision statement (if any): [text]. Decider: [name/role or None]
Stakeholder map:
| Attendee | Interest | Influence (H/M/L) | Likely concerns | Pre-wire plan |
| --- | --- | --- | --- | --- |
| [row] | [row] | [row] | [row] | [row] |
Agenda (time-boxed):
- 0-2 min: [text]
- [time]: [text]
- Final 3-5 min: [decisions/owners/dates or closure rationale]
Key messages & proofs:
- [bullet]
Likely objections & counters:
- [objection -> counter]
Decision quality controls:
- Private input: [yes/no + method]
- Challenger / dissent owner: [name/role]
- Speaker order / sequence control: [plan]
- Private or public vote: [method]
- Decision rule: [rule]
Give-get plan:
- [offer vs ask]
Artifacts:
- [artifact, owner, send time]
Exit checklist:
- [decision captured]
- [DRI named]
- [dates agreed]
- [risks logged]
- [follow-up owner]

Follow-up Email
Subject: [Outcome] - [Project/Topic], [Date]
Body:
- Objective recap: [text]
- What we covered: [bullets]
- Decisions: [decision / DRI / due date]
- Open items: [owner / next step / due date]
- Notes/Context: [links]
- Thank you & next checkpoint: [text]

If Meeting Is Unnecessary (Async Plan)
- [step, owner, deadline]

Assumptions
- [assumption or "None"]

Read-Aloud Checklist
1. Goal: [text]
2. Decision/Decider: [text]
3. Stakeholders: [text]
4. Agenda times: [text]
5. Next steps: [text]

FAILURE
- Any required section is missing or materially incomplete.
- Type mix percentages are missing or not approximately 100%.
- No decision/decider handling when decision is required, or no async plan when meeting is unnecessary.
- Decision meetings omit dissent, private input/voting, speaker-order control, or decision rule when groupthink/conformity risk is present.
- Final 5-item read-aloud checklist is missing.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
