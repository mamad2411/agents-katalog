---
name: blind-spot-pass
description: >-
  Run a pre-build blind spot pass before the agent builds anything. Treat the
  user's prompt as the map and the real project as the territory: classify gaps
  across known knowns, known unknowns, unknown knowns, and unknown unknowns
  (with deps, edge cases, and blast radius under unknown unknowns); ask 5 to 10
  high-leverage interview questions; two-step halt before build; optional
  red-team intensity when the user asks to challenge the plan. Plan-only, no
  execution in the same turn. Use for blind spot pass, find unknowns,
  assumption interview, or before writing, coding, or speccing when the prompt
  may be incomplete.
user-invocable: false
---
# Blind spot pass

## Role

You run a **blind spot pass** before building. The user gives a rough plan, goal, or prompt; you treat it as the **map** and the real project as the **territory**. You classify what is known and unknown across four quadrants, then ask the highest-leverage interview questions so building does not start on hidden assumptions.

This skill uses a **two-step handshake**: (1) deliver the pass and wait for pass approval; (2) build only after a later explicit **execute now** (or equivalent), or when the user explicitly says to skip the pass and build now. **Pass approval is not build.** This skill is **plan-only** on delivery and on pass approval.

## When to use

Use before writing, coding, product specs, or any build where the prompt may be incomplete. Run this when the user wants to **find unknowns** or surface unstated context before the agent acts. For a greenfield fog map with parallel tracks, use `pathfinder`. For a six-part delegation contract, use `define-agent-goal`. For a runnable prompt, use `structure-prompt`. For a technical audit of a **step-by-step implementation plan**, use a **dedicated plan-preflight skill, not this one**.

## Intensity

| Intensity | When |
|-----------|------|
| **standard** (default) | Always, unless the user requests red-team |
| **red-team** | Only when the user asks to challenge, break, or red-team the plan |

There is no `light` mode. Detection phrases for red-team include: challenge, break, red-team, red team, find why this fails, stress-test the ask.

Under **red-team**, still deliver the four-quadrant pass and interview questions. Actively seek reasons the *map* (ask) fails, and push harder on §4 sub-bullets and high-leverage questions. Do **not** replace the pass with a free-form principal-engineer risk report or a step-by-step plan audit (that is plan-preflight skill work).

## Workflow

Run phases in order. Do not deliver the pass until Phase 3. **Do not execute** the task, scaffold code, or run destructive commands when delivering the pass, when the user only approves the pass, or unless the user explicitly says to skip the pass and build now.

### Phase 0: Intake

1. Extract the **rough plan** (goal, constraints, audience, deliverables, links, notes) from the message.
2. If the plan is missing, ask one focused question before proceeding.
3. Produce a one-sentence restatement of what the user wants built and for whom.
4. Set intensity to **standard**, or **red-team** if the user asked to challenge / break / red-team the plan.

### Phase 1: Discovery

Ask structured clarifying questions (use `AskQuestion` when available) only for gaps the plan leaves open:

- Who is the audience and what does success look like for them?
- What is explicitly out of scope?
- What constraints (time, stack, compliance, dependencies) are implied but unstated?
- What decisions would most change structure, architecture, scope, workflow, or quality if answered differently?

Aim for **4 to 6** high-signal questions before drafting. Skip anything the user already answered.

### Phase 2: Draft the pass

Fill the **pass template** below. Keep it to about one page: prefer tables and bullets over prose. While drafting:

- Treat the user's prompt as the **map**; infer the **territory** (real constraints, stakeholders, edge cases) that the map may omit.
- Populate **all four quadrants**. Mark a quadrant as thin only when the context genuinely has nothing for it, and say so.
- Under **§4 Unknown unknowns**, always include the three required sub-bullets (Dependencies, Edge cases, Blast radius). Mark a sub-bullet **N/A** only when genuinely empty.
- Do not invent facts to fill a quadrant or §4 sub-bullet. Label inference as inference (prefer unknown knowns plus a confirming question); keep genuine unknowns in unknown unknowns.
- Rank **5 to 10 interview questions** by leverage: prefer questions whose answers would materially change structure, architecture, audience, scope, workflow, or quality.
- If intensity is **red-team**, bias questions and §4 toward failure modes of the ask, still inside the pass template.

### Phase 3: Deliver

1. Post the blind spot pass in chat using the template headings (sections 1 to 5), including §4 sub-bullets.
2. End with the **two-step approval handshake** (use this wording):

   > **Approve or edit this pass before I build.** I will not start until you confirm.
   >
   > After you approve the pass, say **execute now** (or equivalent) in a later message to begin the work. Pass approval alone is not permission to build.

3. If the host workspace has a `docs/` directory, offer to save it as `docs/blind-spot-passes/<kebab-slug>.md`. Write the file only after the user confirms.
4. Suggest the follow-up: answer the interview questions, then run `define-agent-goal`, `requirement-to-implementation`, or explicit **execute now** in a new turn.
5. Stop. Do not start building until a later **execute now**, or an explicit skip-the-pass-and-build instruction.

If the user later replies only "approved" or "LGTM" on the pass, acknowledge and **stop**. Do not build until they say **execute now** (or explicitly skip the pass and build).

### Follow-up builds (after the pass)

When the user continues building in a later turn (after **execute now**), maintain an **Implementation notes** section in your responses or in the host doc. Log each material assumption you make (what you assumed, why, and what would change if wrong). Update the log as assumptions shift.

## Pass template

Use this structure for the final deliverable:

```markdown
# Blind spot pass: <short title>
Intensity: standard | red-team

## 1. Known knowns
What the user clearly specified. One line each.

## 2. Known unknowns
Questions the user raised but did not answer.

## 3. Unknown knowns
Likely unstated context the user probably holds (audience, constraints, prior art, politics).

## 4. Unknown unknowns
Risks, edge cases, dependencies, or decisions not yet considered.

### Dependencies
Missing prerequisites, undocumented deps, or ordering hazards. Or **N/A**.

### Edge cases
Unexpected states, error paths, empty inputs, or failure modes of the ask. Or **N/A**.

### Blast radius
Side effects, coupling, or scope that could spread if the map is wrong. Or **N/A**.

## 5. High-leverage questions
5 to 10 interview questions, ranked by how much the answer would change
structure, architecture, audience, scope, workflow, or quality.
```

Populate every section with concrete content. Leave a quadrant explicitly thin only when the context genuinely has nothing for it, and say so. §4 sub-bullets are required; use **N/A** only when genuinely empty.

## Safety

- Do not execute the task, scaffold code, or run destructive commands in the same turn as delivering the pass, or after pass approval alone, unless the user explicitly says to skip the pass and build now, or later says **execute now**.
- Redact secrets, tokens, credentials, PII, and PHI in both the plan you echo and the pass you produce.
- Do not invent facts to fill a quadrant or §4 sub-bullet. An inference belongs in unknown knowns with a question that confirms it.
- Never imply a native Cursor product feature; this is a portable planning document for Cursor agents.
- Do not morph this pass into a step-by-step implementation-plan audit (plan-preflight skill).

## Distinction from other commands

- **`pathfinder`**: greenfield **fog map** with decision frontiers, next-move tags per unknown, parallel tracks, and next three actions. Blind spot pass uses the **four-quadrant** model and a pre-build **interview**, not parallel project tracks.
- **`define-agent-goal`**: six-part **delegation contract** (outcome, verification, constraints, boundaries, iteration, stopping) for one autonomous task. Blind spot pass surfaces **what the prompt omitted** before any Goal is written.
- **`structure-prompt`**: produces a **runnable prompt**. Blind spot pass produces a planning artifact and interview questions, not a finished prompt.
- **`scoped-audit`**: read-heavy cataloging of an existing surface. Blind spot pass is forward-looking assumption surfacing before building something new.
- **Plan-preflight (dedicated skill, not this one)**: technical audit of a **step-by-step implementation plan** (deps in the plan, architecture anti-patterns, safer alternatives). Blind spot pass audits the **ask** (map vs territory), not a finished build plan.

## Guardrails

- **Classify all four quadrants.** Populate every quadrant explicitly, marking thin quadrants when the context is sparse.
- **Require §4 Dependencies, Edge cases, and Blast radius.** Include all three sub-bullets, or mark **N/A** when genuinely empty; do not invent facts.
- **Ask high-leverage questions, not trivia.** Ask 5 to 10 questions ranked by leverage on structure, architecture, audience, scope, workflow, or quality.
- **Stay a blind spot pass.** Use **standard** unless they ask for red-team / challenge / break; stay map/territory and point them at a dedicated plan-preflight skill, not this one.
- **Two-step handshake: pass approval is not build.** Acknowledge and wait for a later **execute now** (unless they explicitly skip the pass and build now).
- **Implementation notes after execute now.** Maintain an Implementation notes section logging each material assumption (what, why, and what would change if wrong).
- **Docs save only after confirm.** Offer the path and write only after the user confirms.
- **Do not claim a native product feature.** Present this as a portable planning document for Cursor agents.
