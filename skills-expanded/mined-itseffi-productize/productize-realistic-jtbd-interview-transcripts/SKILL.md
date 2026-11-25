---
name: productize-realistic-jtbd-interview-transcripts
description: >-
  Realistic JTBD interview transcripts. Use when the user needs a product workflow for user
  research related to realistic jtbd interview transcripts. Trigger terms: user-research,
  jtbd, interviews.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Realistic JTBD interview transcripts

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

- **Skill**: `realistic-jtbd-interview-transcripts`
- **Lifecycle**: Discover
- **Category**: Discovery
- **Primary artifact**: Realistic JTBD interview transcripts research brief with evidence, insight clusters, assumptions, and next validation steps

Use this skill to run the Productize prompt contract for **Realistic JTBD interview transcripts**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- `{{PRODUCT_TYPE}}`: Product category to explore.
- `{{TARGET_AUDIENCE}}`: Core audience profile for the interview.
- `{{NUM_PARTICIPANTS}}`: Number of participants to include in the transcript.
</provided_inputs>

GOAL
Generate a realistic multi-participant JTBD interview transcript that surfaces the four forces of progress (push, pull, anxiety, habit) through natural conversation.
Success metric:
- Transcript is realistic, exploratory, and participant-driven.
- Conversation captures current behaviors, pain points, desired outcomes, switching concerns, and habits.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs; if details are missing, state assumptions briefly in the handover.
- Role-play both Product Designer and participants in a realistic dialogue.
- Product Designer behavior must be:
- Open-ended questioning.
- Follow-up on ambiguity and interesting signals.
- Encouraging elaboration.
- Non-leading and solution-neutral.
- Curious and empathetic tone.
- Cover these conversation phases naturally:
1. Introduction and warm-up.
2. Current solutions and pain points.
3. Desired outcomes and aspirations.
4. Concerns and hesitations about change.
5. Existing routines and habitual behaviors.
- Ensure all participants contribute meaningfully.
- Reveal the four JTBD forces implicitly through content, without naming them explicitly.

FORMAT
Return exactly this structure:

<transcript>
Product Designer: [Introduction and first question]

Participant 1: [Response]

Product Designer: [Follow-up question]

Participant 2: [Response]

[Continue until all participants contribute and the conversation feels complete.]
</transcript>

<handover>
This concludes the interview transcript. What specific aspects of the conversation would you like me to elaborate on or analyze further?
</handover>

FAILURE
- Output is missing either `<transcript>` or `<handover>`.
- Transcript does not include the Product Designer plus the requested number of participants.
- Conversation is generic, shallow, or fails to cover required interview phases.
- Product Designer asks leading/solution-prescriptive questions.
- Four JTBD force signals are not inferable from the dialogue.
- Participants do not contribute meaningfully or are not differentiated.
- Assumptions are required but not explicitly noted in handover.
