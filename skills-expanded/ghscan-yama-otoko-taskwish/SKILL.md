---
name: taskwish
description: Build or modify TypeScript TaskWish projects involving actors, actions, state, events, services, or multi-actor workflows.
---

# TaskWish

Keep `taskwish.ts` as the runnable project entrypoint. Organize each actor under `src/<service-name>/` with its actor definition in `<service-name>.ts`, one file per action, an `index.ts` service export, and a colocated `<service-name>.test.ts`. Do not use `actor.ts`, `<service-name>.actor.ts`, or `actor.test.ts` filenames.

An actor owns its domain state and commands. Coordinate workflows across actors through a dedicated actor that declares dependencies with `.use(...)` and calls them through `this.actions.<service>.<action>`.

Declare each actor-owned event directly inside that actor's `.scope(...)`, for example `Actor("IncidentOrchestrator").scope(Event("InvestigationRequested", { runId: "string" }))`. Use the local event name there; TaskWish qualifies it as `IncidentOrchestrator::InvestigationRequested`. Do not pre-qualify event names or collect event declarations in a separate `events` object before passing them to the actor.

Define public actions with `.on("Command", "actionName")`. Give command names enough domain context to stand on their own: prefer verb-and-noun names such as `addTodo`, `scheduleTodoReminder`, or `createCustomer` over vague names such as `add`, `record`, or `process`. Add `.input(...)` when the action accepts input. Define the input object inline in `.input({ ... })`; do not export, import, or spread standalone input definitions such as `intakeDefinition`. Repeat shared fields at each public action boundary so the complete contract remains visible there. Add `.meta(...)` to public commands so Console users can understand them: provide a concise `description`, and add `input` descriptions and examples when fields need guidance. Use lower camelCase names for every `Step(...)`, such as `validateInput` or `createCustomer`. Prefer multiple focused steps when an action has distinct phases or coordinates a workflow, and access earlier results through `this.<stepName>`. Keep truly atomic actions as one step instead of adding artificial stages. Let `State.List` generate primary IDs instead of supplying them when inserting records.

Format fluent actor and action definitions with a blank line between `.use(...)` and `.scope(...)` when both are present, and between the `.on(...)`, `.input(...)`, `.run(...)`, and `.meta(...)` action sections. Inside `.run(...)`, put a blank line between adjacent `Agent(...)` declarations.

Add Bun unit tests for public service behavior and multi-actor workflows. Exercise public actions with `Service.action.ctx({ ...mocks }).run(input)`. Mock default agents with `agent`, named agents with their configured names, and state with `state`; keep provider calls and persistent state out of unit tests. When importing a stateful actor still initializes its store, point `TW_DEFAULT_STORE_PATH` to a temporary directory before dynamically importing it, then restore the environment and remove the directory after the test so state cannot leak between runs.

Update `taskwish.ts` when a runnable scenario helps demonstrate a changed workflow. Run `bun run check` and `bun test` after changing actor contracts. Run `bun start` by default, or `npm run start:node` when specifically verifying Node.js compatibility.
