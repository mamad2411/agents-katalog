---
name: team-intake
description: 'Run a virtual delivery team (triage, product owner, architect, engineer, QA, project manager, tech lead) over an incoming client request — on any project. Use when: a new feature/bug/change request comes in and needs to be understood, classified, and turned into a plan before any code is written; you have a file or folder describing what a client wants; you want intake/triage of a request; you need a technical plan AND a project-manager plan; or you want to know "have we seen this request before?" before acting. Produces a technical plan and a PM plan per request and remembers recurring issues (when the project has a defect catalog configured) so the team stops going in circles.'
---

# Team Intake

Runs a small **virtual delivery team** over an incoming request and produces
two plans:

- **`technical-plan.md`** — what to do in the code (for the engineer who
  builds it).
- **`pm-plan.md`** — request type, history, *where it's coming from*, and how
  to stop it recurring (the plan the user reviews).

It exists because delivery teams keep re-solving the same problems. A
persistent **PM memory** — this project's own request log and, if configured,
its defect-class catalog — lets the team recognize repeats and break the
cycle instead of patching again.

This skill takes one argument: the path to the intake base folder (holds the
request; an `intake/` subfolder is created inside it for the plans).
Optional — if it isn't given, ask for it (see Step 0).

This skill is an **orchestration**: you (the main agent) run the phases below
and delegate each role to a subagent. You are the delivery lead.

## The team (subagents bundled with this plugin)
| Agent | Role |
|-------|------|
| `intake-triage` | Ingest the request → normalized brief; gate on ambiguity |
| `intake-project-manager` | Classify type, reconstruct history, own PM memory + PM plan |
| `intake-architect` | System/design impact, options, risks |
| `intake-engineer` | Exact code change set, feasibility, gotchas |
| `intake-product-owner` | Value, scope, acceptance criteria, sign-off needs |
| `intake-qa` | How we verify done + regression test to add |
| `intake-tech-lead` | Synthesize architect+engineer+QA → the technical plan |
| `intake-client-liaison` | Translate internal sign-off items into a plain-language client approval sheet (on demand) |

> **Path note (plugin install):** this file was written assuming a standalone
> install (`~/.gemini/config/plugins/delivery-team/skills/team-intake/` + `~/.gemini/config/plugins/delivery-team/agents/`). If
> you installed this as an Antigravity plugin instead, every
> `~/.gemini/config/plugins/delivery-team/skills/team-intake/...` path below means "the same-named
> folder bundled alongside this `SKILL.md`", and each agent means "the matching
> `agents/<name>/agent.md` in this plugin's own `agents/` folder" — same
> relative layout, different root.

> **How to invoke each role:** these are subagents bundled with this plugin
> (each in `agents/<name>/agent.md`). Delegate to one by name — "delegate to
> the `intake-architect` subagent" / invoke `@intake-architect` — or let
> automatic delegation trigger it, since the main agent matches the task at
> hand to the subagent's `description`. If delegation misbehaves, fall back to
> running the task yourself using the role brief in `agents/<name>/agent.md` as
> your instructions. Always give the agent: the request-brief path, the output
> dir, and the PM's classification once known.

## Process

### Step 0 — Get the intake base folder (and the request inside it)
The provided folder is the **intake base folder**: it holds the request
materials *and* is where the plans get written (under an `intake/`
subfolder).

- If the user gave a folder path (as the skill argument or in the message),
  use it as the intake base folder. The request materials (ticket, email,
  doc, screenshots) live in this folder. (If they pointed at a single file
  instead, treat that file's parent folder as the base folder.)
- **If no folder was given, STOP and ask the user directly:** "Which folder
  should I work in? Point me at the folder that holds the request — I'll
  create an `intake/` subfolder inside it for the plans."
- Do not invent a request or a location.

### Step 1 — Set up the intake folder
- Derive a short `slug` from the request (kebab-case, ~3 words).
- Create `<intake-base>/intake/<YYYY-MM-DD>-<slug>/` and a `supporting/`
  subfolder inside it. Use today's date. **Never write the plans to the root
  of `<intake-base>`** — they always go under the `intake/` subfolder it
  creates.

### Step 2 — Triage (gate)
Delegate to `intake-triage` on the source → it writes `request-brief.md` and
returns a `READY` / `BLOCKED` verdict.
- If **BLOCKED**, surface its blocking questions to the user directly (plain
  conversational ask) and wait. **Do not run the rest of the team on a
  request nobody understands.**
- **Log every clarifying/blocking question and its answer** (see "Decision
  logging" below) — before you ask, record the question + dated context +
  options as `PENDING`; when the user answers, update it to `DECIDED` with
  their choice and any note. Then update the brief with the answers and
  proceed.

### Step 3 — Evaluate (parallel fan-out)
Delegate to these **four agents in parallel** (invoke them together). Give
each the `request-brief.md` path and the `supporting/` output path:
- `intake-product-owner` → `supporting/product-owner.md`
- `intake-architect` → `supporting/architect.md`
- `intake-engineer` → `supporting/engineer.md`
- `intake-qa` → `supporting/qa.md`

### Step 4 — Project Manager
Delegate to `intake-project-manager`. It reads the brief + the four
supporting files + **PM memory** (this project's own request-log and defect
catalog, if configured), classifies the request, reconstructs history,
writes `pm-plan.md`, and updates the request-log (and the defect catalog if
it's a repeat or a likely-repeat and the project has one). Capture its final
**request type** — the tech lead needs it.

### Step 5 — Technical plan
Delegate to `intake-tech-lead` with the brief, the three supporting files
(architect/engineer/qa), and the PM's classification → it writes
`technical-plan.md`.

### Step 6 — Report back
Summarize for the user in the chat:
- Request **type** and **"seen before?"** (cite the defect-catalog id if
  matched and this project has one configured).
- The PM's headline recommendation (esp. the cycle-breaker if recurring).
- The technical approach in 2–3 bullets.
- Any **PENDING / PARKED decisions** still open (from `decisions.md`).
- Links to `pm-plan.md`, `technical-plan.md`, and `decisions.md`.
Then ask whether to proceed to implementation (out of scope for this skill).

### Step 7 — Client approval sheet (optional, on demand)
When sign-off items need to go to a non-technical client, delegate to
`intake-client-liaison`. It reads `decisions.md`, `supporting/product-owner.md`,
and `technical-plan.md` and writes a plain-language `client-approval.md` (no
internal codes/jargon) plus a private `client-question-map.md` crosswalk so
the returned answers map back to the internal items/decisions. The client
only ever sees `client-approval.md`.

## Decision logging
Whenever a clarifying or blocking question goes to the user — at the Step 2
gate or anywhere a decision is genuinely the user's to make — record it so
the team keeps a readable history of *what we chose and why* (and never
re-litigates a settled call). Two places:

1. **Per request:** `<intake-base>/intake/<date>-<slug>/decisions.md` (from
   `templates/decision-log.md`) — the full, readable record. For each
   question capture, in this order: **the question**, **"where we're coming
   from"** (the dated history/context — current ask vs. what was decided
   before and when, and what conflicts), **the options offered**, and **the
   decision** (chosen option + verbatim user note + implications). Mirror the
   way it's presented in chat.
2. **Global:** append a one-line row to the decision-log (location per
   `PROJECT-CONTEXT.md`, else this skill's global fallback memory).

Write the entry as `PENDING` *before* asking; flip to `DECIDED` (or `PARKED`
if the user defers it to a stakeholder) once they answer. The PM reads the
decision-log during history reconstruction, so a question answered once
stays answered.

## Conventions
- **Intake base folder:** provided by the user (skill argument or message);
  if omitted, the skill asks for it. The request lives here and the
  per-request output is written under an `intake/` subfolder inside it —
  never at its root.
- **Output per request:** `<intake-base>/intake/<date>-<slug>/` containing
  `request-brief.md`, `pm-plan.md`, `technical-plan.md`, `decisions.md`, and
  `supporting/*.md`.
- **Templates:** `~/.gemini/config/plugins/delivery-team/skills/team-intake/templates/`.
- **PM memory:** location comes from `PROJECT-CONTEXT.md` if the project
  names one; otherwise `~/.gemini/config/plugins/delivery-team/skills/team-intake/memory/` (a
  cross-project fallback — defect catalog read first every run if the
  project has one configured; `request-log.md` and `decision-log.md`
  append-only).
- Investigation is read-only. This skill plans; it does not modify product
  code.

## The recurring trap this skill exists to catch
If this project has a defect-class catalog configured (`PROJECT-CONTEXT.md`),
a request that matches a known recurring pattern must be flagged by the PM,
and the technical plan must apply that pattern's durable fix (typically:
route content/logic through its canonical source rather than hand-editing one
path) — never quietly re-take a shortcut the catalog already proved doesn't
work. On a project with no catalog configured, this team still enforces the
general discipline (classify accurately, check for scope/requirement drift,
recommend systemic fixes over patches) — just without a documented history
to check against.
