---
name: new-task
description: >-
  Author a tracker-ready task the way a business analyst would, and never let a
  contradictory one through. Turns an intake into structured requirements, runs a
  mandatory consistency audit, writes full Gherkin scenarios, and creates the
  ticket in the project's tracker. Also runs in audit mode against a ticket that
  already exists. Use for "create a task for X", "write this task up properly", "check this
  ticket for contradictions", or before any feature leaves the idea stage.
---

# New task — BA-grade authoring with a contradiction gate

Two modes. Pick from the request; when ambiguous, ask which one.

- **create** (default) — an intake becomes a tracker-ready task.
- **audit** — an existing ticket is checked and, on request, repaired.

The gate is the same in both: **a task with an unresolved blocking contradiction
never reaches the tracker.**

---

## Mode: create

### Step 1 — Capture the intake

Sources: a dictated or typed description, a pasted spec, a design link, a bug
report. Prefer the requester's own words for the goal so they recognise their
intent.

Before writing anything, ground yourself: read `CLAUDE.md` / `AGENTS.md`, grep
the code for the feature area, and check memory for prior decisions. Catching a
conflict with shipped behaviour is the whole point of doing this before planning.

**Figma intake — discover the whole flow, not just the one frame.** If the
intake is a redesign task, or includes a Figma link or a screenshot exported
from Figma, do not scope the task to that single frame. A requester who sends
one screen for "email confirmation" means the whole flow (sent, resend,
expired link, success, error), not literally one screen — and a task scoped to
one frame is how a dev ships one screen and stops. Use the Figma MCP tools to
find the rest before drafting requirements:

1. `get_metadata` on the frame's containing page/section to enumerate sibling
   frames that belong to the same flow.
2. `get_screenshot` (and `get_design_context` where the copy or state detail on
   a frame isn't obvious from the screenshot alone) on each discovered frame,
   so every state has a concrete visual to write requirements against.
3. Treat every discovered screen as its own functional requirement and its own
   Gherkin scenario in Step 4 — never require the requester to enumerate
   screens by name.

If the Figma file's structure genuinely doesn't group the flow (a flat page
with no clear section boundary), don't guess the boundary — list what you
found and ask the requester to confirm which frames belong to this task.

### Step 2 — Write the requirements

- **Goal** — one sentence: who gets what value.
- **In scope / Out of scope** — explicit boundaries, so the PR stays reviewable.
- **Actors and roles** — who each requirement applies to. A requirement that
  silently applies to every role is usually several requirements.
- **Functional requirements** — numbered, each a testable "When X, the system
  does Y". One behaviour per number.
- **Non-functional** — auth and permissions, realtime and offline behaviour,
  performance and scale, data retention, localisation, timezone (render in the
  viewer's timezone, and send notifications in the recipient's).
- **Failure behaviour** — required, not optional. For every functional
  requirement: error, empty, timeout, permission denied, concurrent action. A
  path that fails silently is a defect in the spec, not a detail to settle later.
- **Integration points** — endpoints, events, payload shapes, schema changes and
  migrations, and which clients must adopt them.
- **Behaviour analytics** — required, not optional. Name the events this feature
  emits: entering the flow, finishing it, failing it, and dropping out of it, with
  the properties an analyst needs to segment them. A feature nobody can measure
  after release is a feature nobody can argue about, so the events belong in the
  spec next to the acceptance criteria. Reuse the project's existing taxonomy and
  name events after mechanics the product actually has; a new event name is a
  decision, not a detail.
- **Open questions** — every assumption you had to make. Never invent a number:
  an unspecified limit, price or timeout is a question, not a decision.

### Step 3 — Consistency gate (mandatory)

Delegate to the `requirements-analyst` subagent. It returns a ranked report and a
verdict.

Do not skip this for "small" tasks: small tasks are exactly where an unstated
role or a missing error path hides. On `needs resolution`, surface the blocking
items, get decisions, fold them back in, and re-run. Only `ready-to-plan`
proceeds. Unresolved non-blocking items move into **Open questions** rather than
being dropped.

### Step 4 — Gherkin scenarios

If the project already has a BDD suite, match its layout, tags and phrasing
exactly, so the output can be dropped in without rewriting. Otherwise use:

```gherkin
Feature: <capability, not implementation>
  As a <role>
  I want to <outcome>

  Background:
    Given <the shared precondition>

  @smoke
  Scenario: <the happy path, stated as an outcome>
    When <action>
    Then <observable result>

  Scenario: <one per failure branch>
    When <action>
    Then <the exact error the user sees>
```

Rules that keep them usable:

- **Every failure branch from Step 2 gets its own scenario.** Covering only the
  happy path is the most common gap by a wide margin.
- Assert what the user observes (copy, route, state shown), never internal state.
- Quote exact UI copy. If the copy is undecided, that is an Open question.
- Use `Scenario Outline` with `Examples` when behaviour differs only by input,
  instead of copy-pasting near-identical scenarios.
- One scenario per role when permissions differ.
- Tag the critical path `@smoke` so it can be run as a subset.

### Step 5 — Create the ticket

Use whatever tracker the project actually uses (Notion, Linear, GitHub issues).
Check the repo's memory or config for the tracker and its schema rather than
assuming, and match the fields that project expects (status, area/component,
type). Default the status to the backlog column unless told otherwise.

Body order: **Requirement** (goal, scope, actors) → **Functional requirements** →
**Failure behaviour** → **Integration points** → **Acceptance criteria** (the
Gherkin, in a code block) → **Open questions**.

Hard rules for anything written to a shared tracker:

- No personal names or job titles in the body, and no AI attribution.
- **Show the draft and confirm before creating the ticket.** Writing to a shared
  board is outward-facing; the requester decides when it lands.

Report the ticket URL and the analyst's verdict together.

---

## Mode: audit

For a ticket that already exists.

1. Fetch it and reconstruct its implicit requirements. Hand-written tickets
   rarely have the structure, so restate what it actually asks for before judging.
2. Run `requirements-analyst` over it, same checks.
3. Additionally flag what create mode would have caught: missing failure
   behaviour, no acceptance criteria, an unstated role, an integration surface
   with no payload, wrong component field, and an epic masquerading as a task.
4. Report as `blocking contradictions` → `gaps` → `nits`, each with a concrete
   suggested resolution.
5. Only if asked, repair the ticket in place: add the missing sections and the
   Gherkin, preserving the original wording of the requirement itself. Never
   silently rewrite someone else's ticket; show what you intend to add first.

Auditing a backlog is a good use of parallel subagents, one ticket each, then a
merged report ordered by severity.

---

## Notes

- This skill ends at an agreed, tracker-ready task. It does not design or code.
  Hand off to `plan-task`, then `architect` for anything crossing a layer.
- The Gherkin written here is the contract the `qa` skill later verifies against,
  so keep both in the same words.
- If the intake is really several tasks, say so and split it, rather than writing
  one ticket with three goals.
