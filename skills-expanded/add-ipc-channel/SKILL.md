---
name: add-ipc-channel
description: Add or change a renderer-to-main IPC channel (a new window.studio call) end to end - main handler, preload, typed API, fixture classification and tests. Use when the renderer needs a new capability from the main process or core.
---

# Add an IPC channel

The renderer reaches main only through the fixed preload API. There is no generic
invoke, no eval and no filesystem access from the page; every capability is one named call.

## Files, in order

1. **Contract** - `src/shared/studio-api.ts`: add the method to `StudioApi` with exact
   parameter and result types. Put shared payload types in a `src/shared/*.ts` module
   (browser-safe: no `node:`, no `electron`, no imports from `src/main|preload|substrate`).
2. **Channel map** - `src/shared/ipc-channels.ts`: `"studio:my.thing": "myThing"` in
   `STUDIO_INVOKE_CHANNELS` and `"studio:my.thing": { id: string }` in `StudioInvokePayloads`
   (the payload the preload sends; the result is derived from `StudioApi`). A push stream
   from main is a `STUDIO_PUSH_CHANNELS` entry naming its `on*` call; a new UI event rides the
   existing `studio:event` push and is a `UiEventMap` key instead, and a new durable record is
   a `CustomEventMap` entry read through `studio:events` (the `add-event-type` skill). A method
   the harness calls is no channel either: it is a `HarnessHostApi` key in
   `src/shared/harness-api.ts` (docs/agent/recipes.md, Harness RPC method).
3. **Preload** - `src/preload/studio-bridge.ts`: one line in the returned object,
   `myThing: id => invoke("studio:my.thing", { id })`. Keep it a named call; a push stream
   uses `subscribe(channel, listener)` like `onTerminal`.
4. **Main** - the domain's registrar, `src/main/ipc/<domain>.ts` (composed by
   `src/main/index.ts`; a new domain gets its own `register<Domain>Ipc(handle, deps)` there):
   `handle("studio:my.thing", payload => core.myThing(payload.id));` with no payload
   annotation: `handle` takes the payload and result types from the map, wraps the result as
   `{ok,value}`/`{ok,error}` and runs the fixture guard. A registrar owns no state: it takes
   the core and anything else it needs as explicit `deps`. Push with `pushToRenderer`.
   Validate the payload at this boundary (types are not checked at runtime); resolve paths
   by realpath inside an owned root; never accept a PID, URL to open or absolute path from
   the page unless the channel exists for exactly that and is `native`.
   Put the logic in `StudioCore` (`src/main/studio-core.ts`) or the service under
   `src/main/core/` it delegates to, not in the handler, so it is testable in Node.
5. **Classify** - `src/main/dev/native-policy.ts`: add the channel to the fixture-safe list
   (no account, dialog, download, external app or network) or to the native list. Both lists
   are checked against the channel map, so an unclassified channel fails
   `npm run typecheck`; at runtime fixture profiles refuse it too.
6. **Renderer** - call `window.studio.myThing(...)` from the owning panel/hook.
7. **Docs** - if users can see the behaviour, update the owning `docs/product/*.md` page.

## Tests (red first)

- Behaviour: test the core method or module directly. `tests/helpers/core-lite.ts`
  (`coreLite()`) gives a real `StudioCore` without a harness; use
  `tests/helpers/studio-rig.ts` only when the harness loop must run.
- Handler wiring, when the handler does more than call the core (pushes, keep-awake, several
  calls): drive the registrar through the real typed `handle()` from `createIpcHandle` with
  recorders for its deps, as `tests/conformance/main-ipc.test.ts` does.
- Hostile input: a table of bad payloads (missing fields, traversal `../`, symlink escape,
  wrong types) asserting the call fails and nothing was written.
- Policy: `node --test tests/conformance/native-policy.test.ts tests/conformance/dev-policy.test.ts`.
- Contract: `npm run typecheck` (the map types both sides) and
  `tests/conformance/ipc-contract.test.ts` (the preload, main and the policy use exactly the
  map's channels).
- Rendered check when UI changed: the `verify-ui-via-dev-control` skill.

```sh
npm test -- tests/conformance/native-policy.test.ts tests/conformance/<your-area>.test.ts
npm run verify:architecture   # browser boundary
```

Do not add assertions that read `index.ts` or the preload as text; test behaviour.
