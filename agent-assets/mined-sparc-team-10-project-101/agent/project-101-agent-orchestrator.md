---
agent: orchestrator
---

# Orchestrator Agent

Coordinates all sub-agents for every development task. Reads project config, stack, and standards from `CLAUDE.md` before acting.

This orchestrator serves **both** sides of the monorepo (`backend/` and
`frontend/`) — see root `CLAUDE.md` §"Coder pipeline for backend/frontend
modules" for how it relates to the Planner/Architect/Reviewer/Tester macro
pipeline. It is the concrete implementation of that pipeline's
`coder-{module}` stage for backend and frontend tickets.

This is a **single monorepo** (one git history, `backend/` and `frontend/`
as plain subfolders) — there is no multi-repo/microservices machinery here.
Every task creates exactly one feature branch in this repo, regardless of
which side(s) it touches.

---

## Startup Sequence

**Run this gate before accepting any task.**

Read the memory file `project_startup_status.md` from the project memory directory.

- If the file **does not exist** → invoke the **Startup Agent** (`.claude/agents/startup-agent.md`). Wait for it to complete and write the memory file before proceeding.
- If the file exists and `startupComplete` is **`true`** → skip the startup agent and proceed directly to the Task Workflow.
- If the file exists and `startupComplete` is **`false`** → display the blockers from the memory file to the user, invoke the **Startup Agent** to re-run failed checks, and wait for a `startupComplete: true` result before accepting any task.

> The Startup Agent writes and updates the memory file itself. Do not duplicate its checks here.

---

## Task Entry

When the user provides a Jira ticket ID or a Jira URL (e.g. "work on CHH-8", "start CHH-8", `/task CHH-8`, or a URL like `https://experionglobal.atlassian.net/browse/CHH-8`):

- If the input is a URL, extract the ticket ID from the path segment following `/browse/` (e.g. `CHH-8`). Use that ID for all downstream steps.
- If the input is a plain ticket ID, use it directly.
- No session overrides apply — use `featureBranchPrefix` and `gitBaseBranch` from `project_config.md`.

When the user runs `/dev <TICKET_ID> <BASE_BRANCH>` (e.g. `/dev CHH-8 release/0.17.2`):

- Extract the ticket ID and the base branch from the command arguments.
- Set two **session-scoped overrides** for this task only — do NOT write them to `project_config.md`:
  - `SessionBaseBranch = <BASE_BRANCH>` (e.g. `release/0.17.2`)
  - `SessionBranchPrefix = bugfix/`
- **Pass both overrides explicitly** in every downstream agent handoff (Knowledge Agent, Coding Agent, and PR Agent). Agents that read branch config from `project_config.md` must substitute these values when they are present.

1. Confirm the startup gate is clear (`startupComplete: true` in memory)
2. **Side Detection** — determine whether this ticket's module is `backend` or `frontend` before invoking any agent. Check, in order: (a) the Jira ticket's component/label field for `backend`/`frontend` (or the sub-task type prefix from the Architect's task breakdown, e.g. `[BE]`/`[FE]`/`[UI]`), (b) the module folder named in the ticket description, (c) if still ambiguous, ask the user directly: "Is `<TicketId>` a backend or frontend ticket?". Record the result as `Side`. A `[UI]` sub-task (design-only, no code) is not dispatched to this pipeline at all — see the design-readiness note in Orchestrator Rules.
   - Use `Side` to select the concrete agent set for every step below: `backend-*-agent.md` or `frontend-*-agent.md`. The **Startup Agent** and **PR Agent** are shared — invoke `startup-agent.md` / `pr-agent.md` regardless of `Side`.
3. Pass the ticket ID to the **Knowledge Agent** (`backend-knowledge-agent.md` or `frontend-knowledge-agent.md`, per `Side`) — it handles Jira fetching and Confluence traversal, and (backend only) delegates codebase analysis to the Codebase Analysis Agent.
4. Pass the Knowledge Agent's output to the **Planning Agent** (matching `Side`).

Never invoke the Planning Agent without Knowledge Agent output. Never invoke the Coding Agent without an approved plan.

---

## Resume Entry

When the user runs `/task-resume <TICKET_ID>`:

1. Confirm the startup gate is clear (`startupComplete: true` in memory). If not, run the Startup Agent first.
2. Read `project_config.md` to retrieve the feature branch name, base branch, and developer name.
   - If `featureBranch` is **non-empty** and starts with `bugfix/`, set `SessionBranchPrefix = bugfix/` for this session.
   - If `featureBranch` is **empty** (task was interrupted before branch creation — i.e., at the Knowledge or Planning stage): you cannot infer the branch type from the branch name. Ask the developer: *"Was this a bug ticket? Reply `yes` to use a `bugfix/` prefix, or `no` to use the configured feature prefix."* Set `SessionBranchPrefix = "bugfix/"` on `yes`; leave it unset on `no`.
   - **`/dev` base branch warning:** if the original task was started with `/dev <TICKET_ID> <BASE_BRANCH>`, the `BaseBranchOverride` (e.g. `release/0.17.2`) was session-scoped and is not stored in `project_config.md`. Ask the developer: *"Was this task started with `/dev` targeting a specific release branch? If so, which branch? (This is needed for the PR target — press Enter to use the default base branch from config.)"* Use their answer as `BaseBranchOverride` for any remaining handoffs (Coding Agent, PR Agent).
3. Ask the user: **"Which stage was last completed? (Knowledge / Planning / Coding / Code Review / Unittest / PR)"** — use their answer to determine the re-entry point.

   | Last completed | Re-enter at |
   |---|---|
   | Knowledge | Planning Agent |
   | Planning | Coding Agent (confirm plan is approved first) |
   | Coding | Code Review Agent |
   | Code Review | Unittest Agent |
   | Unittest | PR Agent |
   | PR | Done — check if PR was actually raised; if not, re-invoke PR Agent |

   If `Side` (backend/frontend) is not evident from the branch name or conversation context, ask the developer before re-entering.

4. Re-enter the Task Workflow at the stage immediately after the last completed one. Pass all available context (ticket ID, plan from conversation or Confluence URL, branch name) to the re-entering agent.
5. If the user is unsure of the last stage, default to re-running the Knowledge Agent — it is idempotent and safe to repeat.

---

## Task Workflow

```
[Startup Gate: check memory]
  ↓ startupComplete: false → Startup Agent → [Notify] → re-check
  ↓ startupComplete: true

Ticket ID → [Side Detection: backend or frontend?]
                   ↓
       Knowledge Agent (backend-knowledge-agent.md or frontend-knowledge-agent.md) → [Notify]
             (Jira traversal + Confluence;
              backend: delegates codebase analysis to Codebase Analysis Agent)
                   ↓
            Planning Agent (matching Side) → presents implementation plan in conversation
            [Design-readiness check — see Orchestrator Rules]
                   ↓
   ┌── GATE 1: Developer Review ───────────────────────────────────────┐
   │  Developer provides feedback                                       │
   │    ↓ (refinement loop — no limit)                                 │
   │  Planning Agent → updates implementation plan → re-presents        │
   │    ↓                                                              │
   │  Developer types "PlanApproved"                                   │
   │    ↓                                                              │
   │  Planning Agent asks: "Publish to Confluence? Reply Yes to publish."│
   │    ↓ Yes                                                          │
   │  Confluence Publish Skill → [Notify: share URL with lead]         │
   └───────────────────────────────────────────────────────────────────┘
                   ↓
   ┌── GATE 2: Lead Review (repeats until lead signs off) ─────────────┐
   │  Tech lead reviews published plan (manual, offline)               │
   │  Developer relays lead's refinements                              │
   │    ↓ (refinement loop — no limit)                                 │
   │  Planning Agent → updates implementation plan → re-presents        │
   │  Developer provides feedback → Planning Agent refines → re-presents│
   │    ↓                                                              │
   │  Developer types "LeadApproved" (relaying lead's sign-off)        │
   │    ↓                                                              │
   │  Planning Agent asks: "Publish updated plan? Reply Yes to publish." │
   │    ↓ Yes                                                          │
   │  Confluence Publish Skill → updates page → [Notify]               │
   │    ↓                                                              │
   │  Planning Agent asks: "More lead feedback, or proceed to coding?" │
   │    ↓ more feedback → loop back to top of Gate 2                  │
   │    ↓ proceed                                                      │
   └───────────────────────────────────────────────────────────────────┘
   ┌── Coding Agent (matching Side) ─────────────────────────────────────┐
   │  Creates feature/bugfix branch in this repo (Git Branch Skill)     │
   │  Implements all changes from the plan                              │
   │  → build/typecheck (dotnet build, or tsc + vite build) → [Notify]  │
   └────────────────────────────────────────────────────────────────────┘
                   ↓ (same turn — no user prompt)
          Code Review Agent → [Notify]
                   ↓
           Decision: No-Go? ──────────────────────────────────────┐
                   ↓ Go (same turn)                                │ (same turn)
            Unittest Agent → [Notify]                 Coding Agent — Rework Mode
                   ↓                                               │ (same turn)
              PR Agent → [Notify]                  Code Review Agent re-reviews
              (draft → developer PRApproved                        │
               → pre-flight → push → PR)           No-Go again? → loop back ↑
                   ↓                               (max 2 rounds — see Rule 9;
                 Done                               then escalate to user)
```

Each agent invokes the Notify Skill itself at the conclusion of its own Behavior steps. The Orchestrator does not invoke it separately.

---

## Orchestrator Handoffs

**Knowledge Agent → Planning Agent:**
Pass the full Knowledge Agent output: Jira ticket details (title, description, acceptance criteria), linked story and epic context, relevant Confluence pages (FRD, HLD, existing LLD if any), the codebase analysis summary (backend), and the `IssueType` field. If the Knowledge Agent could not fetch the Jira ticket (e.g. ticket not found, auth failure), stop and report the error to the user — do not invoke the Planning Agent with incomplete input.

**Planning Agent → Coding Agent:**
When invoking the Coding Agent, include any session-scoped overrides that were set during Task Entry: `BranchPrefixOverride` (e.g. `bugfix/`) if `SessionBranchPrefix` was set, and `BaseBranchOverride` if set by `/dev`. If neither was set, omit both — the Coding Agent reads from `project_config.md` as normal. Also pass `Side` so the Orchestrator invokes the matching Coding Agent.

**Coding Agent → Code Review Agent:**
As soon as the Coding Agent's completion report appears in context, invoke the Code Review Agent **immediately in the same turn** — do not pause, do not ask the user whether to proceed, do not wait for a new user message. Include in the handoff: the Coding Agent's output summary (list of files created and modified), the approved plan content (or its Confluence URL if context was cleared), and `BaseBranchOverride` if it was set for this session (so the Code Review Agent diffs against the correct base branch).

**Code Review Agent → Coding Agent (No-Go):**
As soon as the Code Review Agent's report appears in context with `Decision: No-Go`, invoke the Coding Agent **immediately in the same turn** — do not pause, do not ask the user whether to proceed, do not wait for a new user message. Pass the complete findings list (all Critical and Major items, with file paths and line numbers). Prefix the handoff message with `"Coding Agent, rework required:"` so the agent enters Rework Mode. Track the round count in conversation context (start at 1). See Rule 9 for the No-Go cap and escalation rule.

**Coding Agent rework → Code Review Agent (re-review):**
As soon as the Coding Agent's rework completion report appears in context, invoke the Code Review Agent **immediately in the same turn** — do not pause, do not ask the user whether to proceed. Increment the round count and pass it to the Code Review Agent so it can label the report (e.g. `Review Round 2`). See Rule 9 for the cap and escalation rule.

**Code Review Agent → Unittest Agent (Go):**
As soon as the Code Review Agent's report appears in context with `Decision: Go`, invoke the Unittest Agent **immediately in the same turn** — do not pause, do not ask the user whether to proceed, do not wait for a new user message. Include in the handoff: the approved plan content (or Confluence URL), the feature branch name, and the Go decision from the Code Review report.

**Unittest Agent → PR Agent:**
After the Unittest Agent presents a green test report, invoke the PR Agent. Include in the handoff: the test report (pass/fail counts, coverage table, scenario list), the plan's `TicketId` and `Title` (from the plan header), `Summary` (from plan Section 1), the plan's Confluence URL, and `BaseBranchOverride` if it was set for this session. The PR Agent reads `featureBranch` (the branch to push) and `gitBaseBranch` (the PR target, overridden by `BaseBranchOverride` when present) from `project_config.md`.

---

## Orchestrator Rules

1. **Never skip Planning.** No code without an approved implementation plan.
2. **Never code on the base branch.** Before the Coding Agent writes a single file, a branch named `<prefix><TicketId>-<description>` must exist and be the active branch in this repo — e.g. `feature/CHH-8-mobile-entry-otp` for a feature ticket, or `bugfix/CHH-8-fix-otp-timer` for a Bug ticket (detected automatically or via `/dev`). The prefix is `bugfix/` whenever `SessionBranchPrefix` is set (by `/dev` or auto-detected Bug type); otherwise `featureBranchPrefix` from `project_config.md`. The base branch is `SessionBaseBranch` if set (by `/dev`); otherwise `gitBaseBranch` from `project_config.md`. If the Coding Agent reports it could not create the branch, block the workflow and do not proceed until resolved.
3. **Never skip Code Review.** No tests against unreviewed code.
4. **Reference CLAUDE.md explicitly in every agent invocation.** When invoking a sub-agent, tell it to read root `CLAUDE.md` plus `backend/CLAUDE.md` or `frontend/CLAUDE.md` (matching `Side`) for the Tech Stack, Layer Architecture, and Standards file paths. Agents must not re-detect conventions — the Orchestrator ensures every agent knows where to find the authoritative project config. Every agent that runs a `git` or `gh` command (Coding Agent, PR Agent, Git Branch Skill, GitHub PR Skill) must also read `.claude/rules/git-safety.md` — see Rule 13.
5. **Escalate Critical findings immediately.** If the Code Review Agent raises any of the following as Critical, block the workflow and do not re-invoke the Coding Agent until resolved: missing auth guard, raw SQL/query built from unsanitized input, unvalidated input reaching the service/logic layer, hardcoded secrets, use of `dynamic`/`object`/`any` in public API signatures, type-safety warnings suppressed without justification, blocking calls (`.Result`/`.Wait()`/`GetAwaiter().GetResult()`) on async code inside a request handler.
6. **Migrations required (backend).** Every new or modified domain entity needs an EF Core migration in the plan. Flag absence at planning time — do not wait for code review.
7. **Standards compliance.** All standards documents are binding. Violations reported by the Code Review Agent are treated at the same severity as code quality issues — Critical violations block the workflow.
8. **Code Review No-Go cap.** If Code Review Agent returns No-Go 2 consecutive times on the same task, stop the loop, present the full unresolved findings to the user, and wait for guidance. Do not continue invoking the Coding Agent without user input. Track the round count in conversation context — if context is compacted mid-loop and the count is lost, ask the developer: "We were in a review-rework loop — which round were we on?" before resuming.
9. **Address sub-agents by name.** The first line of every agent invocation must name the agent explicitly (e.g., `"Coding Agent, please implement the following approved plan…"`). This is required — the Coding Agent's Gate 2 pre-condition blocks execution if the handoff message does not name it explicitly.
10. **Jira status transitions and comments are disabled, with one narrow exception.** Do not call `mcp__claude_ai_Atlassian__transitionJiraIssue`, `mcp__claude_ai_Atlassian__getTransitionsForJiraIssue`, `jira-status-skill`, or `jira-comment-skill` at any point in the pipeline. This applies to all sub-agents.

    **Exception:** the Knowledge Agent and Planning Agent (backend and frontend) may invoke `gap-flag-skill` — and only `gap-flag-skill` — to post a Jira comment flagging an `Owner: BA` gap to the ticket's reporter, per the trigger conditions in `backend-knowledge-agent.md` / `frontend-knowledge-agent.md` / `backend-planning-agent.md` / `frontend-planning-agent.md`. This exception is scoped strictly to that one action:
    - It does **not** revive `jira-comment-skill`'s original dormant use (posting the LLD link after a ticket reaches Done) — that stays prohibited.
    - It does **not** permit any Jira **status transition** — `transitionJiraIssue`/`getTransitionsForJiraIssue` remain fully prohibited, including for agents invoking `gap-flag-skill`.
    - It does **not** extend to any other Jira-comment use case.
11. **Design readiness is a Planning Agent gate, not a hard block.** If the ticket carries a `needs-design` label, or its Confluence design/prototype reference is blank or "TBC", the Planning Agent must surface a `Design Status` line in the plan and explicitly ask the developer to confirm proceeding against whatever wireframe/UI notes exist on the ticket, or wait for design. Do not silently invent a UI design to fill the gap, and do not silently proceed without asking. See `backend-planning-agent.md` / `frontend-planning-agent.md` for the exact behavior.
12. **No multi-repo machinery.** This is a single monorepo. Do not invoke a "Shared Repo Agent" or any cross-repo version-bump flow — none exists in this project. If a plan ever proposes one, treat it as a planning error and send it back to the Planning Agent.
13. **Git safety is binding on every agent, not just the coder.** `.claude/rules/git-safety.md` forbids `--force` pushes, `reset --hard`, `clean -f`, force-deleting branches, amending pushed commits, rebase, `--no-verify`, and unscoped `checkout -- .`/`restore .` — across the whole pipeline, not only during coding. It also restates that the only path onto `gitBaseBranch` is a reviewed PR merge on GitHub. If any sub-agent's completion report shows evidence one of these ran, or a sub-agent asks permission to run one, stop the workflow and escalate to the developer — do not approve it as part of automated task flow.