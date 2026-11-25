---
name: productize-workshop-activity-design-from-problem-and-participant
description: >-
  Workshop activity design from problem and participant parameters. Use when the user needs a
  product workflow for design & prototyping related to workshop activity design from problem
  and participant parameters. Trigger terms: workshops, facilitation, brainstorming, product,
  ux.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Workshop activity design from problem and participant parameters

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

- **Skill**: `workshop-activity-design-from-problem-and-participant`
- **Lifecycle**: Design
- **Category**: Operations
- **Primary artifact**: Workshop activity design from problem and participant parameters UX/design review with findings, constraints, fixes, and acceptance checks

Use this skill to run the Productize prompt contract for **Workshop activity design from problem and participant parameters**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- {{PROBLEM}}
- {{PARTICIPANTS}}
- {{TIME_AVAILABLE}}
- {{PLATFORM}}
</provided_inputs>

GOAL
Produce a high-quality deliverable for: "Workshop activity design from problem and participant parameters".
Success metric:
- Produces 3-5 distinct workshop activity variants tailored to problem, participants, time, and platform.
- Each variant is facilitator-ready, includes exact timing, and is feasible within `{{TIME_AVAILABLE}}`.
- Variants include practical tradeoffs, inclusion mechanics, and clear runbooks.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs; if any input is incomplete, state explicit assumptions per variant.
- Generate 3-5 distinct variants.
- Do not use XML or JSON anywhere in the response.
- For each variant, total duration must be `<= {{TIME_AVAILABLE}}`, and timeline minute ranges must sum exactly to the stated total.
- Adapt mechanics by participant size:
  - `<=8`: whole-group flow with silent ideation first.
  - `9-20`: pods of 3-5 with rotating roles/report-outs.
  - `>20`: swarm + pods (4-6) + gallery walk + synthesis.
- Adapt logistics by platform:
  - `remote/hybrid`: breakout choreography and linked board flow.
  - `in-person`: room setup, physical materials, visible timing controls.
- Include inclusion and bias-mitigation mechanisms (silent write, timeboxing, anonymous voting, speaker rotation, accessibility notes).
- Include practical Miro runbook guidance for intermediate users; if in-person-only with no Miro, write `Not applicable`.
- Across the full set of variants, include at least:
  - one rapid ideation pattern,
  - one prioritization pattern,
  - one synthesis pattern.
- Keep language facilitator-ready and operational.

FORMAT
Return exactly this structure:

Here are multiple workshop activity variants designed to address the given problem(s):

### Variant X: *[Activity Name]*
**Assumptions**
- [Assumptions]

**Overview (2-3 sentences)**
- [Overview]

**Rationale**
- [Why it fits problem, participants, time, platform]

**Duration**
- **Total minutes:** [N]

**Timeline (minute-by-minute; sums to total)**
- 00:00-00:XX — [Step]
- 00:XX-00:YY — [Step]

**Facilitator Process**
1. [Concrete facilitator step with timing]
2. [Concrete facilitator step with timing]
- **Scaling notes:** [<=8 | 9-20 | >20 adaptations]
- **If time slips +/-10%:** [What to shorten/extend]

**Participant Process**
1. [What participants do]
2. [What participants produce/decide]

**Miro Setup & Runbook (intermediate)**
- [Board prep, frames, breakouts, timer, voting, mapping, export]
- [If not applicable: "Not applicable"]

**Inputs (bring to the workshop)**
- [Inputs]

**Outputs (created by the activity)**
- [Outputs]

**Pros**
- [Pros]

**Cons (with mitigations)**
- [Cons + mitigation]

[Repeat full variant structure for 3-5 variants]

FAILURE
- Opening line is missing or different from required text.
- Fewer than 3 or more than 5 variants are provided.
- Any variant exceeds `{{TIME_AVAILABLE}}` or timeline math does not sum to stated total.
- Output contains XML or JSON.
- Variant sections are missing required headings/items from `FORMAT`.
- Participant-size and platform adaptations are not reflected.
- Miro runbook is missing (or not marked `Not applicable` when appropriate).
- Required pattern coverage across the set (rapid ideation, prioritization, synthesis) is incomplete.
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
