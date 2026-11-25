---
name: productize-group-decision-making-quality-review
description: >-
  Review and design a group decision-making process for product, strategy, roadmap, launch, or
  operating decisions. Use when the user needs to prevent groupthink, polarization,
  conformity, authority bias, shared-information traps, or weak dissent before a group
  decides.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Group Decision Making Quality Review

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

- **Skill**: `group-decision-making-quality-review`
- **Lifecycle**: Align
- **Category**: Decision Making
- **Primary artifact**: Group decision-making quality review with risk audit, information plan, discussion process, voting rule, roles, and decision record

Use this skill when the decision will be made or heavily influenced by a group. The output
should improve decision quality by designing the process, not by writing a generic meeting
agenda.

Route to `meeting-outcome-planning-and-stakeholder-alignment` when the user primarily needs
a meeting plan. Use this skill when the risk is group decision failure.

## Decision-Making Principles

- Consensus without conflict often means relevant viewpoints are being ignored.
- Groupthink favors acceptance over correctness and weakens option testing.
- Group polarization can push a group toward a more extreme version of its initial leaning.
- Conformity, authority bias, common information effect, and sequential revelation can distort
  which evidence gets heard and how strongly it is weighted.
- Private information collection, private voting, challenger roles, explicit dissent,
  and sequence control improve decision quality.
- Process design should fit the goal: reduce conformity when accuracy matters, or increase
  commitment when alignment is the primary objective after a decision is made.

## Workflow

1. Define the group decision, decision owner, participants, stakes, and timeline.
2. Identify initial leaning, power dynamics, authority cues, and information asymmetry.
3. Audit groupthink, polarization, conformity, authority, common-information, and sequence risks.
4. Design the collection, discussion, dissent, voting, and commitment process.
5. Specify roles: decider, facilitator, challenger, evidence owner, dissent owner,
   and recorder.
6. Define decision output, confidence, unresolved dissent, and follow-up review.

## Output Contract

Return:

```markdown
# Group Decision Making Quality Review

## 1. Decision And Group Context
Decision:
Decision owner:
Participants:
Initial leaning:
Stakes:
Deadline:

## 2. Group Decision Risks
Groupthink:
Group polarization:
Conformity:
Authority bias:
Common-information effect:
Sequential revelation / anchoring:
Hidden agendas or incentives:

## 3. Information Collection Plan
Private inputs:
Shared evidence:
Disconfirming evidence:
Base rates:
Unknowns:

## 4. Discussion Process
Opening frame:
Order of speakers:
Challenger:
Dissent mechanism:
Conflict before consensus:
Breaks or private reflection:

## 5. Voting And Decision Rule
Private vote:
Public commitment:
Decision rule:
Tie or escalation rule:
Decision owner override:

## 6. Roles
Facilitator:
Decider:
Evidence owner:
Dissent owner:
Recorder:

## 7. Final Decision Record
Decision:
Rationale:
Confidence:
Unresolved dissent:
What would change the decision:
Review date:
```

## Failure Modes

- Writes a meeting agenda without addressing group decision risks.
- Treats consensus as proof of correctness.
- Omits private input, dissent, or sequence controls when conformity risk is high.
- Fails to name the decider and decision rule.
