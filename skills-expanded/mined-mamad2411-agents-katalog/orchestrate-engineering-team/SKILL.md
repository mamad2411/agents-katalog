---
name: orchestrate-engineering-team
description: Coordinate a hierarchical project-local engineering team across delivery and exploration work. Use when starting or resuming a work item, preserving context across sessions, decomposing complex goals, dispatching Development, Test, Review, or Architecture agents, maintaining progress and materials, or recording user-confirmed goals and decisions without treating agent notes as project facts.
license: MIT
compatibility: Requires Codex with native subagent support plus workspace read access and permission to write .agent-work; role capability boundaries are advisory, not runtime isolation.
metadata:
  author: HandsomeGanzige
  version: "0.1.0"
---

# Orchestrate Engineering Team

Use hierarchical work item workspaces as the shared control surface between the user and AI. Keep the workflow lightweight. Do not introduce detailed gates, roles, or process rules that the user has not discussed and accepted.

## Use the workspace structure

Store agent work under:

```text
.agent-work/
|-- index.md
`-- work-items/
    `-- <work-item>/
        |-- index.md
        |-- materials/          # optional
        `-- children/           # optional
            `-- <child>/
                `-- index.md
```

Treat each work item as a folder and its `index.md` as the single entry point. Create `materials/` and `children/` only when needed. Copy `assets/work-item-index.md` for a new work item and `assets/workspace-index.md` when the root index does not exist.

## Decide whether to create a work item

Create a work item for a delivery goal, not for each conversation, branch, or implementation step.

Create one when the work needs goal discussion, multiple stages, later resumption, maintained todos or materials, collaboration, or explicit progress tracking. Skip it for a small one-pass change or explanation that does not need context recovery.

Continue using the existing work item while follow-up work serves the same outcome. Create a new top-level work item when the outcome is independent.

## Create a work item

1. Discuss the goal and expected result with the user before writing them as confirmed facts.
2. Create `.agent-work/work-items/<work-item>/index.md` after the user confirms them.
3. Set the initial phase according to the work type.
4. Start with a small todo path based on the current understanding and refine it during execution.
5. Add the top-level work item to `.agent-work/index.md`.

Do not modify production code for a formal delivery work item until its goal and expected result are confirmed.

## Maintain authority boundaries

Treat these sections as user-confirmed project intent:

- Confirmed goal
- Expected result
- Confirmed decisions

Propose changes to those sections in conversation first. Write them only after explicit user agreement.

Let the AI maintain these sections autonomously:

- Current progress
- Todo
- Child work items
- Pending discussion
- Context and materials
- Verification
- Result

Use `Pending discussion` for discoveries, questions, and possible decisions. Do not present them as accepted decisions.

## Distinguish delivery and exploration

Use the same workspace structure for both types. Set `type` to `delivery` when the goal is a delivered project outcome. Set it to `exploration` when the goal is to answer a question or test an idea.

For exploration, define the expected result as a conclusion, prototype, or evidence rather than a production implementation. If the idea becomes a delivery goal, create a related delivery work item instead of silently changing the exploration work item.

## Run a delivery work item

Use four natural stages without detailed gates:

1. Align: discuss and confirm the goal and expected result, then create the workspace.
2. Explore: read relevant project facts, add useful material pointers, and form the initial todo path.
3. Progress: execute the current todo, maintain the recovery snapshot, split complex work when needed, and discuss decisions when they arise.
4. Close: record the result and remaining work, report to the parent when applicable, and remove a completed top-level item from the root active index.

Let the user own the goal and necessary decisions. Let the AI progress autonomously between those discussion points.

## Run an exploration work item

Use four natural stages:

1. Frame: confirm the question to answer rather than assuming an implementation.
2. Explore: inspect relevant project facts and run the smallest useful experiment or prototype when needed.
3. Conclude: record evidence, the conclusion, and remaining uncertainty.
4. Close or convert: finish when no more exploration is useful, or create a related delivery work item when the idea should be implemented.

Treat exploration as delivering understanding and delivery work as delivering a project outcome. Do not silently convert an exploration work item into a delivery work item.

## Decompose complex work recursively

Keep simple execution steps as todos in the current work item. When a todo needs independent context, multiple stages, or substantial materials, promote it to a child workspace under `children/<child>/index.md`.

Record the parent in the child index. Keep only the child link, current status, and concise result summary in the parent index. Let the child maintain its own progress, todos, verification, and materials. When it completes, let the Main Agent report its result back to the parent and update the parent todo.

A child work item may refine only the confirmed parent outcome. The AI may create an in-scope child autonomously as execution organization. Put any new or expanded delivery outcome in `Pending discussion` instead.

## Maintain the root index

Use `.agent-work/index.md` as the lightweight project entry point. List only active and paused top-level work items. Discover children through their parent indexes rather than duplicating the full tree in the root index.

Let the AI update the root index when a top-level work item is created, paused, resumed, or completed. Keep all details in work item indexes.

## Maintain local materials

Use an optional `materials/` directory for useful task-local artifacts that do not belong in project source or authoritative project documentation. Examples include research reports, diagrams, API samples, data samples, long test evidence, comparison tables, and temporary prototypes.

Treat `Context and materials` as a navigation index. For each pointer, record where to read and why it matters. Do not load every local material by default.

## Maintain a recovery snapshot

Treat each work item index as a recovery snapshot, not an execution log. It should let another AI quickly recover the confirmed goal, recent completion, current work, next action, children, pending discussion, and required materials.

Update the snapshot when a todo or child completes or becomes blocked, the execution direction changes, an important material is discovered, or the work is about to pause, hand off, or finish.

- Keep exactly one todo in progress when work is active.
- Replace stale progress instead of preserving a chronological transcript.
- Refine todos progressively as understanding improves.
- Record outcomes and evidence, not private reasoning or tool-call transcripts.
- Add implementation subtasks when they remain within the confirmed outcome.

## Treat project code as the source of truth

Use work item workspaces as temporary working context, not long-term project memory. Treat code, tests, types, configuration, and authoritative project documentation as project facts.

When an index conflicts with the project, follow the project facts and correct the index. Do not create or promote separate AI long-term memory. Express durable constraints in executable or implementation-adjacent project artifacts whenever practical.

## Resume work

1. Read `.agent-work/index.md` to locate the relevant top-level work item.
2. Read its `index.md` and follow child links until reaching the active work item.
3. Read only the project facts and local materials referenced for the current todo.
4. Restate the confirmed goal, current progress, and next action briefly.
5. Continue unless the workspace conflicts with project facts; record and raise any conflict.

## Coordinate role agents

Keep the Main Agent as the single coordinator, user interface, result collector, and maintainer of all workspace indexes. Subagents receive bounded work and return structured results; they do not change the confirmed goal, accept decisions, or maintain overall task state.

Use these core roles:

- Development Agent: implement a defined development goal from the current todo, confirmed decisions, and relevant project facts.
- Test Agent: independently design and perform suitable verification, then report evidence, gaps, and unverified risks without silently fixing implementation code.
- Review Agent: independently inspect goal alignment, defects, project fit, scope drift, and maintainability. Keep this role separate from testing.
- Architecture Agent: for complex needs, combine project facts, confirmed preferences, constraints, and relevant external practices to produce alternatives, tradeoffs, and a recommended proposal. Treat its output as a proposal until the user confirms it.

Add domain specialists only when the work needs them; do not make project-specific roles universal.

## Load role profiles

Read `references/agent-profiles.yaml` before dispatching a specialized subagent. Treat it as the registry for role routing, the Role Skill path, context boundaries, write scope, capability expectations, and return fields.

- Treat `enforcement: advisory` literally. The profile documents intended capability boundaries but does not prove runtime isolation.
- Check whether the required capability classes are available before dispatch. If a required capability is unavailable, report it in the task package and either narrow the expected output or let the role return `blocked`; do not silently broaden permissions.
- Make exactly the selected Role Skill effective for the subagent. If the current native spawn schema exposes a typed Skill attachment, use it. Otherwise, put the Role Skill name and path at the start of the bounded task message and explicitly require the subagent to read the entire Role Skill before beginning its task.
- Keep project facts out of Role Skills. Supply current facts through the bounded task package and material pointers.
- Do not let a role profile override the authority boundaries in this skill.

## Orchestrate actual subagents

Treat this skill as explicit authorization to use available native subagent tools for documented, nontrivial work. Do not simulate delegation by merely adopting several role voices. If no subagent runtime is available, state that limitation and fall back to sequential role execution without claiming that agents were spawned.

Before progressing a complex current todo:

1. Analyze the critical path and identify concrete bounded work that can proceed independently.
2. Keep the immediate blocking step local when delegating it would only cause the Main Agent to wait.
3. When one or more independent work items exist, create their child workspaces, load the appropriate role profiles, prepare task packages, and call `spawn_agent` for the selected roles.
4. Spawn multiple agents in the same round when their work is independent. Do not force parallelism for tightly coupled work.
5. Continue useful non-overlapping coordination or work while agents run. Wait only when their result is required for the next integration step.
6. Collect each result, update its child index, summarize it in the parent index, and route any follow-up work.
7. Close completed agents when they are no longer needed.

At dispatch time, inspect the native spawn tool schema exposed by the current runtime. Call only fields that schema documents; do not copy a fixed payload or invent options from another runtime version. Prefer bounded context or isolation controls only when the exposed schema provides them. If it supports a typed Skill attachment, attach the selected Role Skill that way. Otherwise, begin the bounded task message with the Role Skill name and path plus an explicit instruction to read the entire file and follow it before starting the task. The runtime-exposed schema is the source of truth.

If the subagent runtime, selected profile, or Role Skill is unavailable, state the limitation and use an explicit sequential fallback only when useful. Do not claim that a specialized agent was spawned or that MCP and tool isolation was enforced.

For coding workers, assign explicit file or module ownership with disjoint write scopes. Tell each worker that other agents may be working in the codebase and that it must not revert their changes.

The Main Agent must perform this delegation check for every nontrivial active work item. When suitable independent work exists, it must actually spawn subagents rather than defaulting to doing all work itself.

## Route work by expected output

Choose a role from what the current todo needs to produce rather than starting every role mechanically:

- Use Architecture when the todo needs a design proposal.
- Use Development when it needs code changes.
- Use Test when it needs behavioral verification and evidence.
- Use Review when it needs an independent quality and alignment check.

For nontrivial delivery work with code changes, dispatch Development first. After Development returns, normally dispatch independent Test and Review in parallel. Add Architecture only when unresolved design, substantial tradeoffs, or external-practice research is needed. Small one-pass work may remain local. For exploration, invoke only the roles needed for research, prototyping, or evidence.

## Dispatch bounded task packages

Give each subagent a bounded task package using `assets/subagent-task-packet.md`. Include the role, current todo, expected output, relevant confirmed context, material pointers, allowed scope, required capabilities, and known unavailable capabilities. Attach the Role Skill named by the selected profile. Do not pass the entire conversation by default.

Tailor context to the role:

- Architecture receives the problem, project constraints, confirmed preferences, relevant project facts, and research direction.
- Development receives the current todo, confirmed design, allowed change scope, and implementation materials.
- Test receives the expected result, verification target, changed surface, and available verification methods.
- Review receives the confirmed goal and decisions, code changes, and relevant project facts.

Require each subagent to return its status, result, role evidence, evidence or involved files, unavailable capabilities, discovered problems, unresolved matters, and suggested next action. Let the Main Agent integrate the result and maintain workspace indexes.

## Decide completion from combined evidence

Do not treat Development completion as work item completion. Let Development report implementation, Test report verified behavior and gaps, and Review report quality or alignment findings. Let the Main Agent decide the current todo status from their combined evidence.

For in-scope problems, add or refine todos and route the work back to the appropriate role. Return to the user only when resolving the problem requires a change to the confirmed goal or an important decision.

Route blocking Test or Review findings back to Development as a new or refined todo. Put Architecture proposals and their decision points in `Pending discussion`; do not promote them to confirmed decisions without user agreement.

## Project subagent results into work state

Do not paste complete subagent conversations or reports into an index. Let the Main Agent project useful results into the workspace:

- Update progress and todos from implementation results.
- Put new questions or scope changes in `Pending discussion`.
- Add useful code, document, or local artifact pointers to `Context and materials`.
- Summarize current Test evidence and gaps in `Verification`.
- Turn blocking Review findings into todos and retain non-blocking advice only when it has future value.

Keep only the current useful verification state, not full test logs. Store unusually useful detailed evidence under `materials/` and link it from the index.

## Communicate through the Main Agent

Use conversation for goal alignment, necessary decisions, meaningful stage summaries, and final conclusions. Use workspace indexes for continuous progress and context. Keep subagent execution as an internal implementation detail.

Do not forward every subagent step or request confirmation for every small todo. Let the Main Agent synthesize results and report concise work state at meaningful stage changes, raise decisions when needed, and finish with the outcome, verification state, and remaining issues.
