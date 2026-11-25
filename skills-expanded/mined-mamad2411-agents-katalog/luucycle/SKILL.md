---
name: luucycle
description: Orchestrator layer that decomposes a request, routes each task to the right skill, and dispatches workers on a model from the roster.
disable-model-invocation: true
---

# luucycle

An orchestration layer over the skills already installed in this repo: decompose a request into tasks, assign each a skill and a roster model, get the plan approved, then dispatch workers.

## Branches

| Trigger | Branch | File |
| --- | --- | --- |
| normal request | Full orchestration flow (steps below) | `SKILL.md` |
| "start", "begin", "démarrer", new feature | Kick off the alignment flow (grill → spec → tickets), then hand to the main flow | `START.md` |
| "init", "bootstrap", fresh environment | Install the skill library, bootstrap the roster | `INIT.md` |
| "add-cli", "add X" | Grow the roster with a new CLI/model | `ADD-CLI.md` |
| "ask-lucas", lost | Which branch or flow fits? | `ASK-LUCAS.md` |

## Steps

1. **Read the rules.** Open `RULES.md` and read it first, every run. Its rules are absolute and overrule everything below.

2. **Check the roster.** Open the roster at the repo root: `.agents/luucycle/ROSTER.md` (the directory holding `AGENTS.md` — never the skill folder, which `npx skills update` wipes). It is the single source of truth for available models. Do NOT delete models; toggle `Accessible: true|false`. If CLI flags (`Model Flag`, `Bypass Flag`) are missing for a command, run `--help` on that CLI to discover them, and update `.agents/luucycle/ROSTER.md` mid-process. To add a CLI or models to the roster ("add-cli"), run the branch in `ADD-CLI.md` instead. **Empty roster = blocking** (RULES rule 9): if no agent has `Accessible: true`, stop and propose the `add-cli` branch. For bootstrapping the skill library in a fresh environment ("init"), run the branch in `INIT.md` instead.

3. **Decompose and assign.** Break the request into tasks. Open `ROUTING.md` to find the correct skill for each task. Pick a model from the role's eligible list in `.agents/luucycle/ROLES.md` (repo root) - roles map task types to ordered agents; `.agents/luucycle/ROSTER.md` only holds the agent facts (command, flags, cost). Never hard-lock a role to a single agent: take the first `Accessible: true` agent on the list.
   - **Mandatory orchestration:** You MUST use the Orca orchestration skill (`orca-orchestration`) for coordinating workers.
   - **Fallback:** If the ideal model has `Accessible: false`, silently take the second best alternative without prompting.

4. **Confirm the plan.** RULES rule 1: present the task/skill/model table and wait for the user's explicit approval before any work.

5. **Load the skills, then dispatch.** Load the required skills so their instructions are in context. Read `.agents/luucycle/WARNINGS.md` (repo root) before the first `orca` command or any dispatch on a model you have not run recently - its failure modes (delivery acks, stalled workers, agy/cline quirks) apply from the first dispatch on. Then spawn one worker per task via the command and flags defined in the roster. Never do inline what a routed skill defines.

6. **Gatekeeper (UI Gate).** RULES rule 4: any interface-touching task ends at the impeccable Gatekeeper. The Gatekeeper's Verdict is absolute on the final state: the task is not done until it approves the UI.
   - **One gate per final state.** Review the diff only once it is fully merged; a verdict on an intermediate state is stale and must be discarded. After a CHANGES REQUIRED verdict, dispatch exactly one fix worker, then re-gate on the updated diff. Before trusting any gate verdict, confirm its report references code that still exists in the file (a report with dead line numbers is a replay, not a review).
   - **One fresh terminal per gate pass.** Re-using a gate worker's terminal replays its previous conversation and can re-emit the old verdict. Create a new terminal for every re-gate.

7. **Handle a missing, stalled, or dead worker.** When a worker for an assigned model crashes or cannot be created, stop that branch, fallback to the next best accessible model silently, and resume.
   - **Diagnose before waiting.** Before a long `check --wait`, verify the worker is alive: `worker-show` (heartbeat present) and `worker-read` (terminal `running`). A worker stuck at `stage: input_accepted` with no heartbeat since dispatch is dead - abandon it, `task-update --status ready`, then re-dispatch.
   - **Release, never abandon, a worker that is still working.** An abandoned dispatch rejects its `worker_done` and the report is lost. Wait for a live worker's report, then `worker-release`; abandon only a worker you have confirmed is dead.

## Completion Criterion

To avoid premature completion, you must explicitly list every dispatched worker's ID and its final status (`finished` or `paused`) in your final message. 
Finally, conclude the session with a **Retrospective**: critically analyze the orchestration workflow you just ran. Identify friction points, inefficiencies, or missing tools in the `/luucycle` process itself, and suggest concrete improvements to the user.
The skill is only complete when the exhaustive worker list is printed, every UI task has passed the Gatekeeper, and the Retrospective is delivered.

## Rules

`RULES.md` is the single source of truth for behaviour. Re-read it if anything here conflicts.
