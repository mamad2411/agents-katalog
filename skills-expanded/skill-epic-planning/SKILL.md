---
name: skill-epic-planning
description: The lead's recipe for forming a planning team, running an adversarial debate with the plan-challenger, writing one plan markdown per Epic to the team's plans dir, surfacing it for user approval, and only THEN creating sprint Epic / Story / Task objects.
---

# Epic-planning skill — the planning protocol the lead runs before any sprint write

## When to invoke

The lead reaches for this skill when a user request maps to an
Epic-shaped slice of work — anything that would result in:

- ≥ 2 Stories on the sprint board, or
- 1 Story with ≥ 3 Tasks, or
- multi-day work, or
- the user explicitly asking for "a plan."

Trivial single-Task work (one quick edit, a status check, a
clarification) skips this skill — invoking it for a one-line fix
would burn more tokens than the work itself.

## Why this skill exists

Two failure modes the protocol guards against:

1. **Plans drift into "everyone agreed."** When the lead drafts
   from specialists' input alone, the synthesis biases toward
   what's easy to ship, not what's right to build. Without a
   challenger, the plan is half a research document.

2. **Sprint objects land before the user has seen the plan.**
   Today the auto-router takes a plan markdown and stamps it
   onto the board. Once the user spots a missing Story, the
   board already has the wrong shape and rework is expensive.

The protocol fixes both: a challenger always sits at the table,
and the user explicitly approves before any board write.

## Protocol — step by step

### 1. Restate + clarify

Before any dispatch, restate the user's intent in one sentence.
If genuinely ambiguous, ask **one** clarifying question — never
more. Don't decompose into tasks yet; that's step 5.

### 2. Identify roles

Look at the objective and write down the specialties this Epic
touches. Examples:

- "Add OAuth login" → frontend, backend, security
- "Migrate state.json to SQLite" → backend, data, ops
- "Build a Stripe webhook receiver" → backend, security,
  observability

Aim for 2-4 roles. More than that and the planning round becomes
a meeting; fewer and you're skipping a perspective.

### 3. Form the planning team

For each role, pick a teammate in this priority:

| Source | Tool | When |
|---|---|---|
| Already-hired teammate | (already on the team — just dispatch) | First — cheapest, no setup |
| Bundled seed persona | `lumi_team_dispatch_task` (one-shot) or persona MCP `hire_persona` (persistent) | When a built-in matches |
| Runtime persona | `lumi_persona_create_runtime` | Only when no built-in covers the role *and* the work justifies a new persona body (Epic-scale, not Story-scale) |

Look at the bundled personas before spawning new ones. The
catalogue covers most roles:

- Backend / data: `backend-architect`, `database-architect`,
  `python-pro`, `ai-engineer`
- Frontend: `frontend-developer`
- Infra / ops: `devops-troubleshooter`, `deployment-engineer`,
  `cloud-architect`, `incident-responder`, `performance-engineer`
- Security / compliance: `security-auditor`,
  `legal-compliance-advisor`
- Strategy / product: `product-writer`, `business-analyst`,
  `strategy-analyst`, `exec-communicator`
- Quality: `code-reviewer`, `test-automator`, `tdd-orchestrator`,
  `debugger`
- Docs / comms: `docs-architect`, `academic-writer`,
  `mermaid-expert`

### 4. Always include `plan-challenger`

Non-negotiable. The challenger is the team's designated skeptic;
its job is to find what's missing, risky, or over-engineered.
Without it, plans drift into the "everyone agreed" trap. The
challenger persona ships with Lumi — invoke it via
`lumi_team_dispatch_task` or hire it onto the team if you'll
plan multiple Epics together.

### 5. Run the planning round

Dispatch each specialist with the **objective + the role you
want them to cover**. Sample dispatch description for a
backend-architect on the OAuth Epic:

```
Objective: Add GitHub OAuth login to the Lumi dashboard.
Your role: backend. Outline the server-side flow — OAuth
callback handler, token storage strategy, session lifecycle,
how this composes with the existing local-auth users. Give me
acceptance criteria as bulleted lines. Don't write code yet;
this is planning.
```

Wait for each specialist's reply. Synthesise into a draft plan
that follows the markdown shape in step 7.

### 6. Adversarial round

Dispatch `plan-challenger` **last**, with the synthesised draft
as the body of the dispatch. Sample:

```
Plan draft below. Stress-test it. Find the risks, missing
scope, incompatible assumptions. Propose 0-2 alternatives
where the plan over-builds.

<paste the draft markdown verbatim>
```

The challenger returns the structured review:
**Strengths / Risks / Alternatives / Bottom line**.

If the bottom-line is *Approve as-is* or *Approve with small
fixes (n,n)*: integrate the small fixes into the plan and move
to step 7.

If *Send back: <X>*: re-dispatch the affected specialist(s)
with the gap as the prompt, integrate their replies, write the
plan. **One refinement round maximum.** Don't loop into
challenger ↔ specialists forever; if it's still contested after
round 2, surface that to the user as part of step 8 ("the team
is split on X — your call").

### 7. Write the plan markdown

One file per Epic at the **relative path** `plans/<epic-slug>-plan.md`.
The slug is the lowercase-hyphenated first 3-5 words of the
Epic title.

**Use the Write tool with a relative path.** The lead's `cwd` is
pinned to the team's `working_dir` (the platform handles this
via the cwd-fix plumbing), so writing to `plans/foo-plan.md`
lands at `<team-working-dir>/plans/foo-plan.md` — exactly where
the platform's plan scanner reads from. Do **NOT**:

- Use absolute paths (`/Users/foo/team/plans/...`) — those
  bypass the team's `working_dir` resolution
- Use placeholders (`<workdir>/plans/...`) — Write will create
  a literal `<workdir>/` directory, the scanner will miss it
- Write to `~/.lumi-lyra/plans/` directly unless the team has
  no `working_dir` (Personal team only — and even then, write
  relative `plans/foo-plan.md` since the cwd fallback handles it)

If the `plans/` directory doesn't exist, the Write tool will
create it as part of writing the file. No mkdir needed.

The platform's parser (`lumi_storage::plans`) expects this
exact shape:

```markdown
# <Epic title — H1>

## Goal
<One paragraph: what "done" looks like.>

## Critical files
- <path>:<line ref> — <why it matters for this Epic>
- …

## Step-by-step

### <Story 1 title — H3>
- <Task 1.1 — terse, executable>
- <Task 1.2>
- <Task 1.3 — acceptance criteria can be inline as
  "Acceptance: …" lines>

### <Story 2 title>
- <Task 2.1>
- <Task 2.2>

## Risks
- <plan-challenger-surfaced risk 1> — <mitigation>
- <risk 2> — <mitigation>
```

Each `### Story` becomes a Story on the board. Bullets under it
become Tasks. The parser does NOT deduplicate; if you write the
same Story title twice, you'll get two Stories. The parser
ignores any H2 sections other than `Goal`, `Critical files`,
`Step-by-step`, and `Risks` — feel free to add a `## Notes`
section for chat-side context that should NOT land on the board.

### 8. Present for approval

Reply to the user with:

1. The path of the file you just wrote (`<workdir>/plans/<slug>-plan.md`).
2. A one-paragraph summary: who reviewed it, what changed in the
   refine round, the headline risks the challenger surfaced.
3. An explicit yes/no question:
   **"Approve this plan and create the sprint objects?"**

Do **NOT** call `lumi_sprint_create` until the user explicitly
approves. The platform's auto-route on plan-mode is now gated
behind a UI toast — the user clicks `Approve & route to board`
and the platform handles the rest.

### 9. On approval — create the board

When the user clicks the in-toast approve action, the platform
calls `finish_plan_turn` and the parser creates the Epic +
Stories + Tasks. You don't need to dispatch a tool call yourself
in this path.

If the user approves verbally instead (e.g. "looks good, ship
it"), fall back to calling `lumi_sprint_create` directly: Epic
first, capture its id, then Stories with `parent_id=<epic_id>`,
then Tasks under each Story with `parent_id=<story_id>`. Set
`assignee_persona_id` on each Story to the specialist who'll
own it.

### 10. Start execution

Dispatch the first Story to its assignee. Move it to
`in_progress` on the board. Quote the first dispatch's reply
back to the user verbatim.

## Revision flow (when the user asks for a different plan)

Sometimes the user clicks **Revise** in the approval modal
instead of approving or rejecting. The platform sends you a
chat message starting with `📝 Revision requested for plan ...`
that carries:

- The user's feedback (what to change)
- The prior plan body verbatim
- The **exact target filename** for the revised plan
  (e.g. `plans/<base>-v2.md`)

How to handle it:

1. Re-use the planning team you already formed — don't hire a
   new round. The challenger especially must see the revised
   draft.
2. Re-dispatch only the specialists whose slices the feedback
   touches. Anything not touched stays as-is.
3. Re-dispatch `plan-challenger` over the revised draft. One
   refinement round max.
4. Write to the **exact filename** the platform gave you. Do
   not pick your own slug — the audit trail relies on the
   `-vN` versioning convention being respected.
5. Do **not** touch the prior version's file. The platform
   automatically marks it `superseded` once v2 exists.
6. In your reply, summarise the diff vs v1 — what changed,
   what stayed. The user uses this to decide approve / revise
   again / reject.

The approval gate still applies: don't call `lumi_sprint_create`.
The user clicks Approve on the new modal, the platform routes
the revised plan to a *new* Epic (v1's Epic, if any, is
untouched).

## What this skill does NOT do

- Doesn't run for trivial single-Task work.
- Doesn't double-route a plan that's already been approved (the
  router idempotency-checks by filename stem).
- Doesn't auto-assign teammates the user hasn't hired. Hiring
  decisions are surfaced to the user as part of step 8 ("I
  recommend hiring `security-auditor` for this Epic — confirm?").
- Doesn't replace the existing chat workflow for status checks,
  clarifications, or reactive work. This skill is for the
  forward-planning step only.

## Telltales that you're using the skill wrong

- You started writing code before the user approved → restart
  at step 1.
- The plan markdown has zero risks → you skipped the challenger
  or its review was empty. Re-dispatch with the draft.
- The plan markdown has 12 Stories → the Epic is too big. Split
  into 2-3 Epics, run the protocol per Epic.
- The user asked "is this still on track?" and you ran the full
  protocol → status checks don't need the protocol; just answer.
