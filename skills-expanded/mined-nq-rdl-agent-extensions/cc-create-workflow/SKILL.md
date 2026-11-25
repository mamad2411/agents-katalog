---
name: cc-create-workflow
license: CC-BY-4.0
description: >-
  Create, save, and reuse Claude Code dynamic workflows — JavaScript
  orchestration scripts that Claude writes and a runtime executes to fan out to
  many subagents at scale. Use when the user wants to build a workflow, automate
  a repeatable multi-agent process, codify an orchestration, or save a run for
  later. Also triggers on `ultracode`, `/workflows`, `.claude/workflows/`,
  `/deep-research`, "orchestrate subagents", "codebase audit", "large
  migration", "cross-checked research", or "make this a reusable command". The
  skill first decides whether a workflow is even the right tool (vs a subagent,
  skill, or agent team), then drives the author-and-save loop and the
  `.claude/workflows/` distribution rules.
argument-hint: "Describe the task to turn into a workflow (e.g. 'audit every API route for missing auth checks')"
compatibility: >-
  Requires Claude Code v2.1.154+ for dynamic workflows (on Pro, enable them in
  /config). Monorepo path-walking requires v2.1.178+. Before v2.1.160 the
  trigger keyword was `workflow` instead of `ultracode` (natural-language
  requests work in both). Checked against the workflows docs with Claude Code
  2.1.284 on 2026-09-29.
user-invocable: true
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

## User Input

```text
$ARGUMENTS
```

When the user invokes `/claude-code:create-workflow`, help them produce a saved,
reusable workflow for the task in `$ARGUMENTS`. If empty, ask what repeatable
multi-agent task they want to codify.

**Always run the decision gate first** — most tasks should *not* be a workflow.
Only proceed to authoring when the gate says a workflow is the right tool.

---

## Step 1 — Decision gate (do this before anything else)

A workflow is the heaviest of four primitives. The real difference is **who holds
the plan**. Steer the user to the lightest tool that fits.

| Use… | When | Plan held by |
|------|------|--------------|
| **Skill** | Reusable *instructions* one agent follows | Claude, following the prompt |
| **Subagent** | Offload one focused side-task; only the summary matters | Claude, turn by turn |
| **Agent team** | A few workers that must **talk to each other** / challenge findings | Lead + teammates, turn by turn |
| **Workflow** | **Repeatable, codified** fan-out to **dozens–hundreds** of agents | The **JavaScript script** |

Pick a **workflow** only when *all* of these hold:

- The orchestration is worth **codifying and rerunning** (a per-branch review, a
  recurring audit), not a one-off.
- The task needs **more agents than one conversation can coordinate** — bug
  sweeps across a repo, 500-file migrations, research cross-checked across many
  sources, drafting a plan from several independent angles.
- You want intermediate results to stay in **script variables**, keeping Claude's
  context holding only the final answer.

If the user just needs collaboration between a handful of agents, that's an
**agent team** (`/claude-code:agent-teams`). If they want reusable instructions,
that's a **skill** (`/claude-code:...` via the skill catalog). If it's a single
delegated lookup, that's a **subagent**. Say so and stop.

> Subagents are the worker primitive a workflow orchestrates; an agent team can
> reuse subagent *definitions* as teammate roles. Workflows don't "call skills" —
> the agents they spawn load skills by context, the same as any session.

## Step 2 — Frame the task for the runtime

Workflows have a fixed shape you must design *for*, not against:

- **The script coordinates; agents do the work.** The script itself has **no
  filesystem or shell access** — only its spawned agents read, write, and run
  commands. Frame the task as "fan out N agents, each does X, collect/compare
  results," not "the script edits files."
- **Codify a quality pattern, not just parallelism.** The payoff over plain
  subagents is repeatable structure: have agents **adversarially review** each
  other's findings, or draft a plan from several angles and weigh them, before
  reporting.
- **Stage gating needs separate workflows.** There is **no mid-run user input** —
  a run pauses only for agent permission prompts and, from v2.1.271, a
  usage-limit wait. For sign-off between stages, run each stage as its own
  workflow.
- **Respect the caps:** up to **16 concurrent agents** by default (fewer on
  low-CPU machines; `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` sets 1–256 on
  v2.1.269+), **4,096 items** per `parallel()`/`pipeline()` call, and **1,000
  agents total per run**. Scripts cannot use `import()`. Design the fan-out to
  fit.

## Step 3 — Have Claude write it

You don't hand-author the JavaScript — **Claude writes the script** from the task
description. Trigger it one of two ways:

- **Single task:** include the keyword **`ultracode`** in the prompt (or just say
  "use a workflow"). Example: `ultracode: audit every API endpoint under
  src/routes/ for missing auth checks`.
- **Whole session:** `/effort ultracode` — Claude plans a workflow for every
  substantive task until the session ends or you turn it off with
  `/effort ultracode off` (v2.1.284+, where Ultracode is a toggle; earlier
  versions drop back by choosing another effort level such as `/effort high`).

Claude shows the planned phases and asks to approve before running (the prompt's
frequency depends on permission mode; `Ctrl+G` opens the script, `Tab` edits the
prompt first). Iterate on the task description until a run does what you want.

> The run writes its script to a file under `~/.claude/projects/` and Claude gets
> the path — ask for it to read, diff, or edit the orchestration directly.

## Step 4 — Save for reuse

Once a run is good, save its script as a command: run `/workflows`, select the
run, press **`s`**, and `Tab` to pick the location:

| Location | Scope |
|----------|-------|
| `.claude/workflows/` | **Project — committed to the repo, shared with everyone who clones it** |
| `~/.claude/workflows/` | Personal — every project, only you |

Saved workflows run as `/<name>` and appear in `/` autocomplete alongside
built-ins like `/deep-research`. If a project and personal workflow share a name,
the **project** one wins.

**Monorepo (v2.1.178+):** saving to the project location writes to the closest
existing `.claude/workflows/` between your cwd and the repo root (or the repo root
if none exists). Workflows load from *every* `.claude/workflows/` along that path;
on a name clash the one nearest your cwd runs.

## Step 5 — Parameterize with `args`

A saved workflow reads invocation input from a global named **`args`**:

```text
> Run /triage-issues on issues 1024, 1025, and 1030
```

Claude passes the input as **structured data**, so the script calls array/object
methods on `args` directly — no parsing. If omitted, `args` is `undefined`.

---

## Distribution reality (important)

**Plugin workflows were verified on Claude Code 2.1.274** (the changelog does
not record the first supporting version). Store the JavaScript at the
plugin root under `workflows/`, or declare script paths in the manifest’s
`workflows` field. The plugin namespaces each script’s `meta.name`.
For this catalog, keep scripts in the owning canonical skill’s `scripts/` folder.
Register their packaged paths under `targets.claude.workflows` in the bundle.
Sync copies the scripts, and manifest generation validates their source paths.
Codex does not execute this runtime, so exclude Claude-only workflow entrypoints.

Project and personal `.claude/workflows/` locations remain supported. For saved
script edits, load `/workflow-authoring` first on Claude Code 2.1.248 or later.
The RDL executable example ships as `/rdl-team:house-style`.

## Cost & model

A run spawns many agents, so it can cost meaningfully more than doing the task in
conversation; runs count toward plan usage and rate limits. Before a large run:

- **Gauge on a slice first** — one directory, not the whole repo — and watch
  per-agent token usage in `/workflows`; stop anytime without losing completed work.
- Each agent's model follows the subagent model order (a model the script names
  for a stage counts as the per-invocation choice); with nothing else set it is
  the **session model**. Check `/model` before a big run, and ask Claude to
  route low-stakes stages to a smaller model.
- A run above 25 agents or 1.5M projected tokens shows an advisory
  `Large workflow` warning; the `workflowSizeGuideline` setting (v2.1.219+)
  sets the advisory size Claude aims for.

## Permissions

Spawned agents use your permission rules, so **pre-allowlist what the agents
need** before a long run. Launch approval, headless (`claude -p` / Agent SDK)
behaviour, and each agent's permission mode vary by mode and version — see
[workflows: approve the plan](https://code.claude.com/docs/en/workflows#approve-the-plan-before-it-runs).

## Turn workflows off

`disableWorkflows: true` in `~/.claude/settings.json` (or managed settings for an
org), the `CLAUDE_CODE_DISABLE_WORKFLOWS=1` env var, or the Dynamic workflows
toggle in `/config`. When disabled, bundled workflow commands vanish and
`ultracode` no longer triggers.

## Resumption

A relaunched run replays saved agent results, but a failed or changed agent reruns
every later agent. Whether a run survives leaving the session depends on how you
leave — see [resume after a pause](https://code.claude.com/docs/en/workflows#resume-after-a-pause).

---

## Verify against canonical source

Dynamic workflows are new and evolving (keyword, monorepo paths, and limits have
all changed across versions). When being wrong would mislead, verify against the
canonical docs: <https://code.claude.com/docs/en/workflows>. Related primitives:
[subagents](https://code.claude.com/docs/en/sub-agents),
[agent teams](https://code.claude.com/docs/en/agent-teams),
[plugins reference](https://code.claude.com/docs/en/plugins-reference).
