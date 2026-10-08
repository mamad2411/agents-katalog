# Olas — coding rules for AI assistants

This project uses Olas (controller-tree architecture). Business logic lives
in pure-TypeScript controllers; React components are thin renderers.

## Hard invariants

- Business logic — fetching, mutations, derivation, multi-step flows — lives
  in controllers (`defineController((ctx) => api)`), not in components.
- React components subscribe via @kontsedal/olas-react hooks (`useRoot`, `use(signal)`,
  `useQuery`, `useField`). They never call `fetch`, never own a query or
  mutation, never hold long-lived state.
- Controller factories are SYNCHRONOUS. Async work goes inside `ctx.cache`,
  `ctx.mutation`, or `ctx.effect` callbacks. `defineController(async ...)`
  silently breaks construction-rollback — never write it.
- Fetchers (`fetcher`) and mutation `mutate` functions receive an
  `AbortSignal`. Forward it to every network call (`fetch`, `axios`,
  `ctx.deps.api.*`). Not forwarding is a bug.
- Every primitive created on `ctx` (effects, child controllers, fields,
  queries, mutations, emitters) is auto-disposed with the controller. Don't
  write manual cleanup.

## Testing

Test controllers in pure Node, no jsdom:

    import { createTestController } from '@kontsedal/olas-core/testing'
    const { api, dispose } = createTestController(myController, { deps: fakes })
    // call api.someMethod(), assert against api.someSignal.peek()
    dispose()

`@kontsedal/olas-core/testing` is reserved for test files (`*.test.ts`, `*.spec.ts`).
Don't import it from production code.

Run with `pnpm vitest run packages/<name>/tests/<file>.test.ts`.

## Common gotchas

- `Field<T>.value` returns `T`. `Form.value` and `FieldArray.value` return
  `ReadSignal<T>`. They are NOT symmetric — branching code must handle both.
- `ctx.field('')` infers `Field<''>` from the empty-string literal. Annotate
  as `ctx.field<string>('')`.
- Per-query optimistic updates use `query.setData(...key, updater)`. The
  `onMutate` returns the snapshot; `onError` calls `snapshot.rollback()`.
  Automatic rollback fires only on abort, not on normal errors.

## Where to look

- `SPEC.md` — authoritative API contract (cite as `§N.M`).
- `API.md` — every exported type, signature, and usage example.
- `RECIPES.md` — reusable composables (`useDebounced`, `usePagination`,
  `useSubmit`, `useInlineEdit`, `useTail`, `useRealtimePatcher`).
- `BACKLOG.md` — open work. Append follow-up ideas here, never in SPEC.md.
