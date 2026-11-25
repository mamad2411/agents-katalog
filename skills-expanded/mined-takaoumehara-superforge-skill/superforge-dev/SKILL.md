---
name: superforge-dev
description: >
  Build multi-component features by decomposing the work and dispatching
  subagents, assigning a model tier per subtask. Splits work into tasks with
  one outcome, a proof line, and a listed set of files — so parallel safety is
  decidable rather than hoped for — and proposes Subagents versus Agent Teams
  versus a scripted Workflow topology, including the trap that a workflow
  agent inherits the session's model unless the script assigns one per stage.
  Also covers the schema: the shared foundation every parallel run depends on,
  and the part of a product that gets harder to change as it succeeds —
  identity, money, deletion, migrations run against data you cannot restore.
  Use when the user says "implement", "build this feature", "execute the
  plan", "in parallel", "dispatch agents", "split this up", "which model
  should", "use a workflow", "database", "schema", "migration", "実装して",
  "作って", "並列で", "サブエージェント", "タスクに分けて", "どのモデルで",
  "スキーマ", "DB設計", "マイグレーション", or runs /superforge-dev.
license: MIT
metadata:
  author: Takao Umehara
  version: "5.1"
compatibility: >
  Standalone.
  Reads and writes docs/plan.md. The schema section informs superforge-secure and superforge-ship.
  Parallel dispatch requires a subagent mechanism; without one it runs the same loop sequentially.
  The workflows/ scripts require Claude Code v2.1.154+; everywhere else the same loop runs as prose.
---

# Superforge Dev — Multi-Agent Building & Model Tiering Engine

Use this skill when implementing multi-component features, executing complex build plans, or dispatching subagents. It ensures optimal model tiering and agent topology selection.

---

## 0. Split the work before choosing anything else

Topology and model tier are decisions about *how* to run tasks. They cannot
rescue a bad split, and a bad split is where unattended runs actually fail —
agents that conflict, duplicate, or wait.

A task is well-formed only when it has **one outcome, a proof line, a listed set
of files it will touch, and no question left to ask.** The file list is not
bookkeeping; it is what makes the next rule decidable:

> **Two tasks may run in parallel only if the set of files they write does not
> intersect.** Not "probably do not conflict" — listed, and disjoint.

Shared foundations — schema, shared types, design tokens, the route table, a
dependency upgrade, any rename — run **alone and first**, then fan out. Most
failed parallel runs are one of those done concurrently with its dependants.

The never-parallel table, how to find the dependencies a file list cannot show,
how much context to hand each agent (both too little and too much fail, in
different ways), what to do when a subtask fails — **revert before retry** — and
when not to split at all → **`references/decomposition.md`**.

**The schema is the shared foundation that runs first and alone**, and it is
also the one part of a product that gets *harder* to change as the product
succeeds — code with no users can be rewritten in an afternoon, a table with
real rows cannot. The decisions that are cheap now and expensive later (IDs,
timestamps, money, deletion, the ownership chain every authorization check
reads), the three causes of every data performance problem, and how to run a
migration against data you cannot restore → **`references/data-design.md`**.

---

## 1. Agent Topology Proposal (Subagents · Agent Teams · Workflow)

Before dispatching, evaluate and **explicitly notify the user** of the recommended structure:

- **Subagents Pattern (Default — Low Token Cost)**: Use for isolated, modular tasks (building components, fixing bugs, writing tests). One-way dispatch.
- **Agent Teams Pattern (Interactive — High Token Cost)**: Use when cross-perspective debate is required (architecture trade-offs, multi-agent debate).
- **Workflow (Scripted — Claude Code only)**: Use when the work-list is already known and larger than about five items, when the same orchestration will run again, or when something must be judged by an agent that did not produce it. The loop and the intermediate results live in a script, so §0's parallel-safety rule and §3's ledger are executed rather than trusted. Three are shipped in `workflows/` → **`references/workflow-graphs.md`**

*Notification Template*:
> *"Proposing **Subagents Pattern** (Sonnet 5 workers) for fast, token-efficient execution. Say 'use Agent Teams' if you prefer interactive multi-agent debate, or 'use a workflow' to run it as a script."*

**The one thing that must not be got wrong:** every agent inside a workflow runs
on the *session's* model unless the script sets one per stage. A workflow with no
tiering does not merely fail to save — it takes whatever `/model` happens to be
and multiplies §2's waste by the agent count. Generation is volume (Sonnet),
adjudication is judgment (Opus), bookkeeping is routine (Haiku); if a script does
not show that split, it is not ready to dispatch.

---

## 2. Model Tier Classification (Claude 5 & Multi-LLM)

### Golden Rule for Claude 5:
> **"判断は Opus 5, 量は Sonnet 5, 雑務は Haiku 4.5, 持久戦は Fable 5"**

| Subtask Nature | Claude 5 | Gemini Env | Codex Env | Kimi Env | Effort |
|---|---|---|---|---|---|
| **Tier A (Judgment & Architecture)**: System architecture, PRD, code review, security | `Opus 5` | `3.6-flash` | `Codex Sol` | `K3 Max` | `high`/`xhigh` |
| **Tier A (Unattended Long Runs)**: Overnight builds, 10+ step refactoring | `Fable 5` | `3.6-flash` | `Codex Sol` | `K3 Max` | `high` |
| **Tier B (Volume Implementation)**: Feature workers, UI components, primary QA | `Sonnet 5` | `3.6-flash` | `Codex Terra` | `K3 High` | `medium` |
| **Tier C (Routine Closed Tasks)**: Rote tests, log formatting, symbol renaming | `Haiku 4.5` | `3.6-flash` | `Codex Luna` | `K3 Standard` | `low` |
| **Tier D (Pure Text Processing)**: Offload via local `gemini` CLI | — | — | — | — | `low`/`medium` |

---

## 3. Dispatch Protocol

0. **Print the plan before spending anything.** A table with one row per task —
   model, effort, *why that tier*, and the files it may write — plus the wave
   order and the agent count broken down by model. This is the only way the
   user can see whether the tiering this suite promises is actually happening,
   and it is the human-in-the-loop point. **Print it and continue; do not ask
   for approval** — the point is that stopping is possible, not required. Then
   record what actually ran, including retries and any tier that changed
   mid-run → **`references/dispatch-ledger.md`**.
1. **Explicit Versioning**: When dispatching `Fable 5` for long runs, ensure library versions (e.g. Next.js 15, Tailwind v4) are explicitly declared in the prompt or `CLAUDE.md`.
2. **Self-Contained Subagent Context**: Provide complete file paths, acceptance criteria, and background context to every subagent.
3. **Verification Gateway**: Run tests and verify diffs before accepting subagent output.

---

## Deeper reference

**`references/decomposition.md`** — the unit of a task and the two smells that
say it is not one yet, the parallel-safety rule and the never-parallel table,
finding the dependencies a file list cannot show (signatures, fixtures,
migration order), what to hand each agent and the boundary to state explicitly,
the subtask-failure table, and when splitting costs more than it saves.

**`references/data-design.md`** — modelling the nouns the user actually says,
the ownership chain that authorization depends on, the choices that are cheap
now and expensive later, missing indexes / N+1 / unbounded reads, additive
migrations with a tested rollback, and what "deleted" has to mean.

**`references/dispatch-ledger.md`** — the before-table and the after-record:
model and reason per task, what each agent may write, the wave order, the agent
count by model, and the rule against silently upgrading a tier mid-run. Also
what may honestly be said about cost, and what may not.

**`references/autonomous-run.md`** — preconditions for an unattended run, the
build/review/prove/repair loop, what to decide alone versus what must stop the
run, and the morning report format. Read it before any long or overnight run.

**`references/workflow-graphs.md`** — when the orchestration should be a script
rather than prose: the default-model trap that makes an untiered workflow worse
than no workflow, why a wave is a barrier and a barrier is usually the wrong
default, the four things a workflow cannot do (starting with: it cannot stop to
ask you anything), what the three-wave cap does and does not limit, and the three
workflows shipped in `workflows/`. Read it before writing or running one.

Split first, then run: `decomposition.md` produces the task list that
`autonomous-run.md` executes, or that `workflows/superforge-dev-waves.js`
executes as a script.

## Artifact

Write and maintain `docs/plan.md`: checkbox tasks, each with a **proof line**
naming the command or observation that shows it is done, **the files it may
write**, and the wave it belongs to. Tick the box and append to the progress log
after every task, then write the file. A run that dies at task 7 must resume at
task 8 from disk alone.

## Running to the end

Once the direction is agreed, do not stop to ask. Resolve open questions with
a defensible default, log it under `Assumptions made`, and continue. Stop only
for irreversible loss, spending money, missing credentials, or the goal itself
being wrong — and even then, keep working on everything not blocked by it.

## Delegate when a sharper skill is installed

`writing-plans`, `prd-generator`, `architecture-spec` (planning) ·
`dispatching-parallel-agents`, `subagent-driven-development`,
`executing-plans` (dispatch) · `repo-cleanup` · `ci-cd-setup`,
`logging-setup`, `error-monitoring` · `vercel:*` (deploy).
