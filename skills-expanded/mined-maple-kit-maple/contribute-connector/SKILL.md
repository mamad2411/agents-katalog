---
name: contribute-connector
description: Scaffold a Maple connector from a template, run the shared contract suite against it, and emit its row for the capability matrix. Use when adding support for a new backend (a store, media, observability, identity, gate or classifier provider) or when an existing connector's tests need wiring.
---

# Contribute a connector

A connector is one file implementing plain Promise methods. This skill writes
that file, proves it against the shared contract, and produces the documentation
row so the matrix in `docs/connectors.md` cannot drift from the code.

## Before writing anything

Answer these four. Guessing here is what produces a connector that passes tests
and fails in a preview.

1. **Which kind?** `store`, `media`, `observability`, `identity`, `gate` or
   `classifier` — the six in `ConnectorKind`. A backend can be more than one;
   write one file per kind it fills.
2. **Which optional methods can the backend honestly support?** Omit the rest.
   An optional method that throws is worse than an absent one, because Maple
   degrades around absence and cannot degrade around a throw.
3. **Does the backend have read-your-writes?** If an append is not immediately
   visible to a list, the contract run needs `eventualConsistencyMs`, and the
   connector needs to say so in its documentation. This is the single most
   common source of a connector that works in tests and loses comments in use.
4. **Where do its credentials live?** Anything server-side is read on the SDK
   route and must never reach the overlay bundle. Never write a credential
   value into a file; inject it with `op run --env-file`.

Check the backend against the ones already ruled out in `docs/connectors.md`
before starting.

## Steps

1. **Read the contract.** `packages/core/src/connectors/types.ts` is the whole
   API. Read the interface for the kind being implemented, and
   `packages/core/src/testing/memory-store.ts` as the smallest thing that
   satisfies it.

2. **Copy the template.** Only a store has one: `templates/store.ts.template`.
   For any other kind, start from its interface in `types.ts` and the memory
   reference beside the contract (`memory-gate.ts`, `memory-classifier.ts`,
   `memory-media.ts`). Put it at `packages/core/src/connectors/<name>.ts`. The
   connector `name` is lowercase, hyphenated, and matches the filename.

3. **Implement.** Rules the contract enforces, so knowing them up front is
   cheaper than discovering them in a failure:
   - `list` returns `{ comments, cursor? }`. Omit `cursor` on the last page —
     never return an empty-string cursor.
   - `list` rejects a non-positive `limit` rather than substituting a default.
   - `append` assigns the id and returns the stored comment, with `status`
     defaulting to `"open"`.
   - `setStatus` rejects an unknown id. Resolving silently hides a bug.
   - Errors carry the backend's own message. Core maps them to
     `MapleStoreError` and decides what to retry; a connector that swallows an
     error takes that decision away.

4. **Wire the contract suite.** Create
   `packages/core/test/<name>.contract.test.ts`:

   ```ts
   import { runStoreContract } from "../src/testing/store-contract.js";

   import { myStore } from "../src/connectors/my-store.js";

   runStoreContract({
     name: "my-store",
     create: async () => ({ connector: myStore(testOptions), cleanup: () => reset() }),
   });
   ```

   `create` is called once per test and must hand back an isolated backend. A
   shared one leaks state between tests and turns a real failure into a flake.

   A gate runs `runGateContract` and a classifier `runClassifierContract`, both
   from the same directory and wired the same way. Media runs
   `runMediaContract`. Observability and identity have no contract suite yet;
   test those against msw directly.

5. **Mock every network call.** Handlers go in `packages/core/test/msw/`, one
   file per upstream. A connector tested only against a 200 is not tested
   against the API it will meet.

6. **Run the gates.** All four, in this order:

   ```
   pnpm test -- <name>
   pnpm lint
   pnpm typecheck
   pnpm test
   ```

7. **Emit the capability row.** Run this and paste the result into the matrix in
   `docs/connectors.md`:

   ```
   pnpm --filter @maple-kit/core exec node -e "
     import('./dist/connectors/index.js').then(({ capabilitiesOf }) =>
       import('./dist/connectors/<name>.js').then(({ myStore }) =>
         console.log(capabilitiesOf('store', myStore(sampleOptions)))))"
   ```

   Mark a method `~` rather than `✓` when it is implemented with a caveat, and
   write the caveat under the table. A `~` with no explanation is a `✗` that has
   not been admitted yet.

8. **Document the caveats.** Add a section to `docs/connectors.md` covering
   consistency, retention, credentials and anything the backend cannot do. The
   Datadog section is the worked example of the level of honesty expected.

## Definition of done

- The contract suite passes, including the eventual-consistency path where it
  applies.
- Every network call has an msw handler, including at least one error response.
- `pnpm lint && pnpm typecheck && pnpm test` pass.
- `docs/connectors.md` has the row and, where anything is marked `~`, the
  paragraph explaining it.
- A changeset describes the addition for the release notes.
