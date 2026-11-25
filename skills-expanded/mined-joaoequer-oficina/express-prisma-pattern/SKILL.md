---
name: express-prisma-pattern
description: House pattern for Express + Prisma backends structured as manual Clean Architecture (controller → usecase → repository, wired by hand in a factory) — the real shape of two production Express + Prisma backends. Use whenever creating a new route, usecase or domain in an Express backend on this stack, even if the request is just "create the X endpoint" or "add the Y usecase".
---

# Express + Prisma — house pattern

Manual Clean Architecture, not a framework's DI container: every layer is a plain TS interface, wired by hand in a factory function. Confirmed by reading real code in two production backends (independent codebases, different Prisma majors, same controller/usecase/repository/factory shape) — the shell below is non-negotiable, do not invent a NestJS-style module system on top of it. The two repos diverge on *where* zod validation runs (see rule 4) — that's the one confirmed exception to "same shape", not an oversight.

## Per-feature structure

```
src/
├── controllers/<domain>/<action>-controller.ts   # implements Controller. Parses HttpRequest, calls the usecase, returns HttpResponse via helpers. Never imports Prisma.
├── usecases/<domain>/<action>-usecase.ts         # Business logic. execute(...). Depends on the repository INTERFACE, injected via constructor.
├── interfaces/
│   ├── controllers/controller.ts                  # shared Controller contract
│   ├── http/http-request.ts, http-response.ts     # shared request/response shape
│   └── repositories/<domain>-repository.ts        # repository contract + domain types
├── repository/<domain>/<domain>-repository.ts    # Prisma<Domain>Repository implements <Domain>Repository
└── main/factories/<domain>-factory.ts             # make<Action>Controller(): wires repository → usecase → controller by hand
```

## The shell (non-negotiable)

```typescript
// interfaces/controllers/controller.ts
export interface Controller<T = any> {
  handle(request: HttpRequest): Promise<HttpResponse<T>>;
}
```

```typescript
// controllers/area/area-controllers.ts
export class ListAreasController implements Controller {
  constructor(private readonly usecase: ListAreasUsecase) {}
  async handle(_request: HttpRequest): Promise<HttpResponse<AreaComContagem[]>> {
    return ok(await this.usecase.execute());
  }
}
```

```typescript
// main/factories/area-factory.ts — manual composition root, no DI container
const repository = new PrismaAreaRepository();
export const makeListAreasController = (): ListAreasController =>
  new ListAreasController(new ListAreasUsecase(repository));
```

Response shaping always goes through the shared helpers (`ok`, `badRequest`, `unauthorized`, `serverError`), never a raw `res.json()` inside the controller. Every `handle()` wraps its body in try/catch → `serverError(e)` — an uncaught throw inside a controller is a bug.

## The business-logic layer — one correct shape, one tolerated legacy shape

- **UseCase class** (`usecases/<domain>/<action>-usecase.ts`, `execute()` method, repository INTERFACE injected via constructor) — the only shape for new code. Matches the `List<Entity>Usecase` shape.
- **Legacy service function** (`services/<domain>/<domain>-service.ts`) — exists in older code in some repos (e.g. `<domain>-service.ts`), and it is not a lighter version of the same pattern: it imports the Prisma client directly, with no repository interface at all. This is debt, not a second accepted form — never model new code after it, and touching a neighboring line doesn't obligate rewriting it.

## Non-negotiable rules

1. **Controller never imports Prisma.** Not even the db client — if you're tempted, the logic belongs in the usecase or repository.
2. **Repository is always interface + implementation, in separate files** (`interfaces/repositories/<x>.ts` contract, `repository/<x>/<x>-repository.ts` with `Prisma<X>Repository implements <X>Repository`). No controller or usecase imports `PrismaClient`/the db client directly.
3. **Wiring happens in `main/factories/`, by hand.** No DI container, no decorators — a plain `make<X>Controller()` function that `new`s the chain.
4. **Validate with `zod`** (already a dependency in every repo on this stack) as the *first* thing that runs on `request.body`, before any business logic — confirmed in two different spots depending on the repo: in the controller before calling the usecase (e.g. `<domain>-controllers.ts`), or as the first step inside `usecase.execute()` (e.g. `Create<Entity>Usecase`). Match whichever placement the project already uses — check an existing feature before picking one — never split validation across both layers for the same feature. Manual `if (!field) return badRequest(...)` chains are legacy, not the model to copy into new code.
5. **Tenant/workspace isolation at the repository query** — same bar as `security-baseline.md`. Being Express instead of NestJS is not an exception.

## Source of truth for the model

Exact fields come from the project's data model document. If it's not there, stop and ask before inventing fields.

## Definition of done (per feature)

- [ ] Model in Prisma + migration applied
- [ ] Controller/usecase/repository/factory files created, wired through the factory
- [ ] Response goes through the shared http helpers, try/catch → serverError
- [ ] Validation via zod (not manual ad-hoc checks) as the first thing that runs, in whichever layer this project already validates at (controller or usecase — see rule 4)
- [ ] Lint and build clean
- [ ] Route registered in `main/routes/`
