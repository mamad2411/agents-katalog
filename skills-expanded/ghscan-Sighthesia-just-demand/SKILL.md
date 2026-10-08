---
name: just-demand-intake
description: Use when the user proposes a new goal, feature, bugfix, design, refactor, research item, UI request, or any unclear work that may become a formal work item. Shapes work into task-ready intake after socratic-clarification has handled requests, bugs, pivots from ordinary Q&A, and other material uncertainty.
---

# Workflow Intake

Clarify the user's need before exposing workflow mechanics.

## Core Rules

- Focus on the user's described outcome, expected behavior, anti-outcomes, constraints, and tradeoffs.
- Use `socratic-clarification` for progressive questioning before shaping new or ambiguous work.
- Do not outrank `socratic-clarification`. Intake starts after clarification has established the intended effect and direction for the current turn.
- When a later turn pivots from Q&A into a concrete request, bug, correction, or mismatch, route through `socratic-clarification` before intake.
- Keep the turn user-understandable, but do not use brevity as a reason to skip material uncertainty.
- Prefer the `question` tool for grouped decisions, approvals, and boundary capture when the answer can be expressed as concise options. Use free-text only for phenomena, nuanced descriptions, or answers that cannot be safely reduced to options.
- Do not discuss task packages, repo maps, JSONL, context injection, or subagent mechanics unless the user is explicitly designing those mechanisms.
- Treat intake as guidance; runtime plugins still enforce the workflow-entry gate for concrete requests without an active task.
- In no-plugin fallback mode, intake is the required next step after approved clarification when no formal task exists. Do not treat approval of an approach as permission to edit inline.

## Process

1. Restate the user's goal and suspected anti-outcome.
2. Identify the requirement type: UI, workflow, bugfix, architecture, docs, research, or implementation.
3. Extract what the user already specified.
4. Apply the final artifact from `socratic-clarification` when present.
5. Record confirmed expectations, remaining gaps, and non-blocking questions.
6. Promote to a formal work item only after required fields and approval are present.

If plugins are unavailable, disabled, or unstable, self-enforce this transition: after clarification approval, create/promote the intake before any write tool or execution subagent. Skill-only fallback is best-effort and cannot hard-block tools, so do not rely on a later plugin rejection to catch skipped intake.

Record clarification in user-language buckets that can later become task data:

- expected behavior
- actual behavior
- reproduction
- scope
- blocking questions
- non-blocking questions

Treat blocking questions as promotion blockers. Non-blocking questions may stay open if execution can still proceed safely.

## Final Artifact Requirements

For design and implementation work, the intake must include the final artifact before promotion:

- **Decision Card**: one-sentence intent, recommended default, reason, and the user's expected action
- **User Action**: what the user needs to do next, or "no action needed"
- **Recommended Default**: the path the agent recommends if the user does not care
- **Option Matrix**: compact comparison of real alternatives by best-for, pros, cons, and failure mode
- **Final Expected Effect**: user-visible outcome in user language
- **Approach Options**: 2-3 approaches with pros, cons, and practical failure modes; for UI/interaction work these must be meaningful user-visible alternatives, not placeholders
- **Chosen Approach**: selected approach with brief rationale
- **Final Implementation Plan**: ordered steps including verification
- **Minimum Viable Knowledge**: one-sentence explanations for unfamiliar terms or tradeoffs the user needs to decide
- **Touchpoints**: short concrete files/modules/components when known, plus explicit exclusions; this complements the formal `Scope` field and keeps user-facing scope readable
- **Visible Acceptance**: what the user can see, feel, or operate to confirm the result; routine tests/build/lint are mandatory agent work and should not dominate the first-screen approval card unless they fail or need user action
- **Visible Side Effect**: expected screen or operational side effects, not alternate unchosen approaches
- **Diagram Intent**: for flowcharts, architecture diagrams, state diagrams, data-flow/API diagrams, or other explanatory diagrams, what the diagram is meant to communicate
- **Diagram Acceptance**: what the user should be able to identify from the diagram, such as entry points, branches, boundaries, owners, states, transitions, sources, transforms, or destinations
- **Expression Side Effect**: what the diagram emphasizes, collapses, hides, or intentionally omits
- **Validation**: engineering checks and review steps for the task record or final report, secondary to visible acceptance in user-facing approval cards
- **Validation Card**: concise observable checks the user can scan before approval
- **Diagram**: small Mermaid or ASCII diagram when UI, workflow, state, process, or data shape would otherwise be ambiguous
- **Confidence**: high, medium, or low when it helps calibrate trust
- **Escalation Reason**: why this needs user input instead of safe agent decision
- **Approval**: explicit user approval of the final artifact

Promotion is blocked for design/implementation tasks when Final Expected Effect, Chosen Approach, Final Implementation Plan, or Approval are missing.

## Blocking Questions Policy

A question is blocking when guessing the answer could change implementation path, validation criteria, user-facing behavior, or acceptable scope. Blocking questions include unresolved choices about expected behavior, actual behavior, reproduction conditions, affected scope, anti-outcomes, data loss/risk tolerance, or which tradeoff the user prefers.

Do not demote a question to non-blocking just because a likely answer exists. Only proceed without asking when the user already answered it, the repository has an explicit durable decision, or the implementation is safely reversible and user-visible behavior will not change.

## Question Threshold

Ask implementation questions only when they affect:

- Product behavior or user-visible outcomes
- Architecture decisions or module boundaries
- Compatibility with existing systems or data
- Security, cost, or long-term maintenance

Do not ask about implementation details that are purely engineering preferences when they do not affect the above categories.

## Intake Recording Shape

When `socratic-clarification` has produced a final artifact, record it in this shape:

```text
Decision Card: <intent, recommended default, reason, user action>
User Action: <approve / choose / correct / no action needed>
Recommended Default: <agent's recommended path>
Option Matrix: <real alternatives by best-for, pros, cons, failure mode>
Final Expected Effect: <user-visible outcome>
Touchpoints: <short concrete files/modules/components when known, plus explicit exclusions>
Approach Options: <2-3 options with pros, cons, and failure modes>
Chosen Approach: <selected approach and rationale>
Final Implementation Plan: <ordered implementation and verification steps>
Minimum Viable Knowledge: <plain-language terms needed for the decision>
Visible Acceptance: <visible or operational checks the user can evaluate>
Visible Side Effect: <expected screen/operational side effects, or none>
Diagram Intent: <what an explanatory diagram is meant to communicate, if applicable>
Diagram Acceptance: <what the user can identify from the diagram, if applicable>
Expression Side Effect: <what the diagram emphasizes, collapses, hides, or intentionally omits>
Validation: <how the result will be checked>
Validation Card: <3-5 quick checks for user approval>
Diagram: <small Mermaid/ASCII diagram, or "not needed">
Confidence: <high|medium|low when useful>
Escalation Reason: <why user input is needed, or "none">
Approval: <explicit user approval or authorization>
```

Avoid vague placeholders:

```text
Approved.
TBD.
Do the obvious thing.
```

## Intake Recovery Shortcuts

`create-intake` only creates `.just-demand/state/intake/<intake-id>.md`. Before promotion, keep working in that same file.

Recovery recipe after `create-intake`:

1. Reopen the same intake markdown file; do not create a replacement intake.
2. Replace placeholders with the approved clarification artifact.
3. Keep unresolved items in `## Blocking Questions`; clear or move them only when resolved.
4. Promote only after the required sections below are no longer empty.

Hard promotion gates by work shape:

- design/implementation: `## Scope`, `## Final Expected Effect`, `## Chosen Approach`, `## Final Implementation Plan`, `## Approval`
- bug/mismatch: `## Scope`, `## Expected Behavior`, `## Actual Behavior`, `## Reproduction`

`## Decision Card`, `## User Action`, `## Recommended Default`, `## Option Matrix`, `## Touchpoints`, `## Approach Options`, `## Minimum Viable Knowledge`, `## Visible Acceptance`, `## Visible Side Effect`, `## Diagram Intent`, `## Diagram Acceptance`, `## Expression Side Effect`, `## Validation`, `## Validation Card`, `## Diagram`, `## Confidence`, `## Escalation Reason`, `## Current Understanding`, `## Anti-Outcome`, `## Decisions`, and open-question sections should also be updated when the clarification artifact provides them, but the fields above are the runtime hard gates.

Recovery recipe after failed `promote`:

1. Read the error text and note each named missing field or remaining blocker.
2. Update that same intake markdown file; do not touch `task.json` and do not create a second intake.
3. Fill the named sections from approved user intent; ask instead of guessing.
4. Clear `## Blocking Questions` only when each blocking item is actually resolved.
5. Rerun the same `just-demand . promote ...` command.

## Questioning Patterns

### Bug, regression, or expected-vs-actual mismatch

Drive toward this shape:

```text
Expected behavior: what should happen.
Actual behavior: what happens instead.
Reproduction: when or how it shows up.
Scope: who, what path, or which environments are affected.
Blocking questions: anything that prevents safe implementation.
```

Preferred prompts:

- "What did you expect to happen here?"
- "What happens now instead?"
- "Can you reproduce it reliably, and if so with which steps or conditions?"
- "Is this isolated or does it affect multiple paths/users/environments?"
- "Which missing detail would make us likely fix the wrong thing?"

For expected-vs-actual mismatches, do not make the user compose the deviation description. Default to leading with the two-stage option flow from `socratic-clarification` (Proactive Deviation Options): Stage 1 options to locate the deviation dimension, Stage 2 "currently X, want Y or Z" contrast options to pin the target state. Reserve free-text for reproduction and other open-ended phenomena.

For visual or interaction mismatches, record the solution shape explicitly when it affects the user-visible result. At minimum, consider:

- containment: clip, hide, mask, or delay drawing
- synchronized entrance: foreground follows the container's expansion, anchor, direction, or timing
- layout/reflow: spacing, anchoring, available size, or row reveal changes so content naturally fits

If the user objects to the feel of a fix, such as "裁剪效果不好" or "not synchronized", treat that as approach drift. The next intake/update should choose a new solution shape instead of continuing the same patch family.

### Feature, workflow, or implementation request

Drive toward this shape:

```text
Desired outcome: what should be true when done.
Scope: what is in and out.
Anti-outcome: what would feel wrong even if technically complete.
Blocking questions: unresolved choices that would change the implementation path.
Non-blocking questions: polish or preference details that can remain open.
```

Preferred prompts:

- "What should a successful result let you do that you cannot do now?"
- "What is the smallest acceptable scope for this pass?"
- "What should we explicitly avoid changing?"
- "Which choice would materially change the implementation path if guessed wrong?"
- "Which details are nice-to-have and can stay open until execution?"

Default to this low-reading-cost shape before asking the user to make a tradeoff:

```text
Decision card:
- Intent: <one sentence>
- Recommended default: <what the agent recommends>
- Why: <one practical reason>
- User action: approve, choose another option, or correct the intent
- Confidence: <high|medium|low when useful>
- Escalation reason: <why the user must decide, or none>

Option matrix:
| Option | Best for | Pros | Cons | Failure mode |

Minimum viable knowledge:
- <term>: <one sentence, only if needed>

For UI/layout/animation work, use a visible-effect card instead of a generic engineering-plan card:

Recommended: <one sentence describing the visible effect>

Current:
+-- <component/region> h=<current height> --+
| <current visible problem>                  |
+--------------------------------------------+

Target:
+-- <component/region> h=<target/content> ---+
| padTop=<value or existing variable>         |
| <primary content>                           |
| <secondary/revealed content>                |
| padBottom=<value or existing variable>      |
+--------------------------------------------+
<parent or surrounding region effect>

Touchpoints: `<file/module>` and `<component>`; not changing <explicit exclusion>.
Visible acceptance: <1-2 visible or operational checks>.
Visible side effect: <expected on-screen side effect, or none>.

Validation card:
- <observable checks; routine tests/build/lint are agent obligations and can be moved to optional detail unless failed>

Diagram:
- <small Mermaid/ASCII diagram when it reduces ambiguity, otherwise not needed>
```

For flowcharts, architecture diagrams, state diagrams, data-flow/API diagrams, or other explanatory diagrams, use a diagram-intent card instead of a generic engineering-plan card:

```text
Recommended: this diagram will show <core relationship/process/boundary/state/data direction>.

Current / problem:
+-------------+      ?
| A           | ---> |
+-------------+      |
  Missing boundary, owner, branch, state, or data direction

Target:
+-------------+   <relation/flow>   +-------------+
| A: role     |  ---------------->  | B: role     |
+-------------+                     +-------------+
       |                                   |
       +-- <owner / branch / state note> --+

Touchpoints: `<module/doc>` and `<diagram area>`; not changing <explicit exclusion>.
Diagram acceptance: <what the user can identify from the diagram>.
Expression side effect: <what is emphasized, collapsed, hidden, or intentionally omitted>.
```

Diagram acceptance cues:

- Flowchart: entry point, decision points, success path, failure/rollback path, terminal states.
- Architecture diagram: module boundaries, dependency direction, ownership, external systems, trust/security boundary when relevant.
- State diagram: states, transitions, triggers, guards, terminal/error states.
- Data-flow/API diagram: source, transform, destination, data owner, protocol/API boundary, trust/security boundary when relevant.

## Progressive Clarification Routing

When the user proposes a need, request, feature, design/refactor, bug report, symptom, phenomenon, vague correction, or expected-vs-actual mismatch, load `socratic-clarification` before shaping or promoting work. That skill owns progressive questioning, overlooked boundary discovery, final expected effect, and final implementation plan.

## Routing Rule

When the clarified work will consume long context, do not keep it in the main session after shaping. Promote it to a formal work item and route execution through `just-demand-*` subagents.

Typical triggers:

- multi-file implementation
- broad codebase reading
- complex UI or interaction work with many states
- extended verification or review
- research that would produce long notes or comparisons

Before any later implementation or verification phase begins, the promoted task must have its current task context files written. The main agent must not improvise by directly editing code from intake context alone.

## High-Detail Requests

For detailed UI or interaction requests, do not restart discovery. Use this pattern:

```text
Known: what the user already specified.
Gaps: the few details likely to cause drift.
Default: the agent's recommended behavior if the user does not care.
```

Before implementation, provide a low-reading-cost validation summary:

- One-sentence intent.
- Five-point quick check.
- Effect validation card when the request is visual or interaction-heavy.
- Simple diagram when layout, workflow, state, process, or data-flow shape is easier to validate visually than in prose.

For visual or interaction work, the validation card should include the intended motion/layout feel, the rejected anti-outcome, and whether any clipping/masking is a primary effect or only a safety guardrail.

For approval surfaces, prefer `Visible acceptance` and `Visible side effect` labels over broad `Validation` and `Risk` labels. Keep engineering verification in the task record or final report unless it failed or needs user action.

For diagram approval surfaces, prefer `Diagram acceptance` and `Expression side effect` labels over broad `Validation` and `Risk` labels. Keep engineering verification in the task record or final report unless it failed or needs user action.
