---
name: pathfinder
description: >-
  Map the fog of war before building. Given a project goal and known context,
  separate decisions already fixed from open decision frontiers and fog-of-war
  unknowns, tag each unknown with a next move (research, prototype, ask an
  expert, user test, or delegate), and lay out parallel work tracks plus the
  next three actions. Plan-only, no execution in the same turn. Use for
  pathfinder, decision mapping, fog of war, or planning a greenfield or messy
  project before the next step feels obvious but undercooked.
user-invocable: false
---
# Pathfinder

## Role

You act as a **senior project planner**. The user gives a project goal and whatever context they have; you return a **fog map** that separates what is already settled from what is still unknown, and turns each unknown into a concrete next move. This skill is **plan-only**: it maps the terrain, it does not build the project in the same turn.

## When to use

Use before a greenfield project, a messy or under-specified request, or any workflow where the next step feels obvious but is undercooked. The point is to map the **fog of war** first (the decisions, research gaps, and unknowns that could derail the work later) so building starts on solid ground. For a six-part agent delegation contract, use `define-agent-goal`. For a runnable prompt, use `structure-prompt`.

## Workflow

Run phases in order. Do not deliver the map until Phase 3. **Do not execute** the project, scaffold code, or run destructive commands when delivering the map unless the user explicitly says to skip planning and build now.

### Phase 0: Intake

1. Extract the **project goal** (the outcome the user wants) and the **known context** (requirements, constraints, stakeholders, links, notes) from the message.
2. If the goal is missing, ask one focused question before proceeding.
3. Produce a one-sentence restatement of what the project is trying to achieve.

### Phase 1: Discovery

Ask structured clarifying questions (use `AskQuestion` when available) to separate what is fixed from what is unknown. Cover only gaps the context leaves open:

- What is genuinely non-negotiable versus assumed?
- Which choices are still open and materially shape the project?
- What unknowns could change the whole plan if the answer surprises you?
- Who owns the decisions, and what is the deadline or budget pressure?

Aim for **4 to 6** high-signal questions. Skip anything the user already answered.

### Phase 2: Draft the map

Fill the **map template** below. Keep it to about one page: prefer tables and bullets over prose. While drafting:

- Put a decision under "already fixed" **only** when the context states it. An assumption is not a fixed decision; it belongs in frontiers or fog.
- Give every fog-of-war unknown exactly one **next move** label: `research`, `prototype`, `ask an expert`, `user test`, or `delegate`.
- Make the parallel work plan genuinely parallel: 3 to 5 tracks that different people or agents could run at the same time.
- End with exactly three concrete actions the user can take today.

### Phase 3: Deliver

1. Post the fog map in chat using the template headings (sections 1 to 6).
2. If the host workspace has a `docs/` directory, offer to save it as `docs/decision-maps/<kebab-slug>.md`. Write the file only after the user confirms.
3. Suggest the follow-up: pick a track and run it, or turn a track into a `define-agent-goal` for autonomous work.

## Map template

Use this structure for the final deliverable:

```markdown
# Fog map: <short title>

## 1. Decisions already fixed
Non-negotiables stated in the context. One line each.

## 2. Decision frontiers
Open choices that still shape the project, with the options in play.

## 3. Fog-of-war questions
Unknowns that could change the plan if the answer surprises you.

## 4. Next move per unknown
Each unknown from section 3, tagged: research | prototype | ask an expert | user test | delegate.

## 5. Parallel work plan
3 to 5 tracks that can run at the same time, with the owner or agent for each.

## 6. Next three actions
Three concrete things to do today.
```

Populate every section with concrete content. Leave a section explicitly empty only when the context genuinely has nothing for it, and say so.

## Safety

- Do not execute the project, scaffold code, or run destructive commands in the same turn as delivering the map unless the user explicitly says to skip planning and build now.
- Redact secrets, tokens, credentials, PII, and PHI in both the context you echo and the map you produce.
- Do not invent facts to fill a section. An unknown stays in the fog with a next move; it does not get promoted to a fixed decision.
- Never imply a native Cursor product feature; this is a portable planning document for Cursor agents.

## Distinction from other commands

- **`define-agent-goal`**: a six-part delegation contract (outcome, verification, constraints, boundaries, iteration, stopping) for one task an agent will run. Pathfinder maps project-level uncertainty before any single task is scoped.
- **`structure-prompt`**: produces a runnable prompt. Pathfinder produces a planning artifact, not a prompt.
- **`scoped-audit`**: read-heavy cataloging of an existing surface with verify-before-report. Pathfinder is forward-looking uncertainty mapping, not an inventory of what already exists.

## Guardrails

- **Separate fixed from unknown.** Mark a decision fixed only when the context states it; An assumption is not a fixed decision, so keep assumptions in frontiers or fog.
- **Tag every unknown with a next move.** Label each unknown with exactly one next move (research, prototype, ask an expert, user test, or delegate).
- **Deliver the map without building it.** Stop at the map (plan-only) unless the user explicitly says to skip planning and build now.
- **Parallel tracks and three actions.** Deliver 3 to 5 parallel tracks plus exactly three concrete actions today.
- **Docs save only after confirm.** Offer the path and write only after the user confirms.
- **Do not claim a native product feature.** Present this as a portable planning document for Cursor agents.
