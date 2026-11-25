---
name: productize-decision-rights-using-davci
description: >-
  Decision rights using DAVCI. Use when the user needs a product workflow for stakeholder
  management related to decision rights using davci. Trigger terms: decision-rights,
  product-ops, facilitation, governance, stakeholder-management.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Decision rights using DAVCI

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

- **Skill**: `decision-rights-using-davci`
- **Lifecycle**: Align
- **Category**: Operations
- **Primary artifact**: Decision rights using DAVCI stakeholder narrative with audience, message, risks, asks, and follow-up owner

Use this skill to run the Productize prompt contract for **Decision rights using DAVCI**.

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
Produce a high-quality deliverable for: Decision rights using DAVCI.
Success metric:
- Completes all required tasks and decision logic from the prompt instructions.
- Output is specific, evidence-based, and actionable.
- Output follows the required structure exactly.

CONSTRAINTS
- Use only provided inputs and clearly state assumptions when information is missing.
- Do not skip required analysis steps, sections, or validation logic.
- Keep recommendations/outputs grounded in the input context; avoid generic filler.
- Enforce DAVCI with hard rules:
- Exactly one `D` per decision.
- `A` is optional and cannot equal `D`.
- `V` is at most one person per domain (`Security`, `Legal`, `Privacy`, `Brand`, `Compliance`, `Other`) with a time-boxed window (default `48h` if missing).
- `C` and `I` use role names; keep `C <= 5`, `I <= 15`, and `C+I <= 20`.
- Every decision includes title, deadline (date + time), type, escalation, success test, and comms plan.
- Run rapid intake, split into 1-5 decision objects, assign DAVCI per object, and auto-correct rule violations immediately.
- Apply defaults when missing (`TBD` allowed), including fallback deadlines by urgency.
- For each decision object, output the exact DAVCI card fields plus a ready-to-send summary line.
- Handle edge cases (multi-team layering, multi-domain veto order, emergency windows, non-response, D handoff).
- Offer short follow-ups (calendar text, Slack draft, Jira/PR/design header snippet).

FORMAT
Return exactly this structure:

Kickoff:
Tell me the situation in 3-5 sentences and the hard deadline (date + time). Include the names/roles you think matter. I'll split it into the right decision objects and we'll assign DAVCI for each in under 30 minutes.

Rapid intake questions:
1. [Question 1]
2. [Question 2]
3. [Question 3]
4. [Question 4]
5. [Question 5]
6. [Question 6]
7. [Question 7]
8. [Question 8]

Decision objects:
- Object 1: [short name] - [why separate]; draft deadline [date/time]
- [Object 2..5 if needed]

Decision: [short title]
Context: [1-2 short sentences]
Deadline: [date and time]
Type: [Strategy|Scope|Design|Technical|Process|Risk|Commercial|Other]
D: [name, role]
A: [name, role] or "None"
V: [Domain - name, window hours]; [Domain - name, window hours]
C: [role/name]; [role/name]
I: [role/name]; [role/name]
Escalation: [name, role]
Success test: [single checkable sentence]
Comms: [channels + audience + timing]
Notes/Risks: [short list if any]

Decision summary:
Decision: [title]. D: [name]. Deadline: [date/time]. Veto windows: [domain - window]. Cs: [roles]. Escalation: [name]. Success test: [test]. Comms: [plan]. Reply with blockers within your window; otherwise we proceed.

Follow-ups:
- [15-minute review calendar text offer]
- [Slack post draft offer]
- [Jira/PR/design header snippet offer]

FAILURE
- DAVCI rule violations are not auto-corrected (`D` count, `A==D`, multi-holder veto domain, missing veto window, `C/I` caps).
- Missing required decision fields (deadline, type, escalation, success test, comms).
- Output does not include both DAVCI card(s) and decision summary line(s).
- Claims are generic or not grounded in provided inputs.
- Assumptions are used but not explicitly stated.
