---
name: write-unit-tests
description: Use when writing isolated unit tests (mocked deps, no DB) for CQRS handlers, services, or DTOs. Mock factories, a handler testing-module helper, DTO validation, the AAA pattern, entity builders. TS/NestJS/Jest examples.
metadata:
  last-updated: 2026-06-20
  author: Ken Nguyễn <ntnpro@gmail.com>
---

## When to use

Reach for this when writing **isolated unit tests** — fast tests that mock every dependency
(DB, buses, external services) and never boot the app. Use it for CQRS command/query/event handlers,
service classes, and request-DTO validation, or to stand up the unit-test harness in a new service.

**Two test layers — don't confuse them:**

| Layer | Boots app? | DB | Use for | Doc |
|---|---|---|---|---|
| **Unit** (this doc) | no | all mocked | handler/service/DTO logic in isolation, fast | here |
| **Integration / e2e** | yes | real test DB | the use-case through the real transport/HTTP boundary | [write-service-code](./write-service-code.md) §8 |

A repo runs one or both (two jest projects — see below). **Follow your repo's established setup:**
some repos test integration-only (the global *HTTP-layer testing rule* — skip a unit test if an
integration test already pins the contract); others keep a full unit layer. Don't bolt a unit layer
onto an integration-only repo (or vice versa) without agreeing it with the team.

Examples use a neutral `listing` domain; `<Module>`/`<Entity>` are placeholders.

## Steps

### 1. Layout & file naming

```
test/unit/
  test-utils.ts                  # all mock factory functions (§3)
  helpers/
    validate-dto.ts              # flattenValidationErrors helper (§4, Pattern 3)
  factories/
    index.ts                     # re-exports every builder (one-line imports)
    listing.factory.ts           # buildListing, buildListingWithItems, ...
    factories.smoke.spec.ts      # smoke test that every builder runs
  modules/<module>/
    <module>-service.spec.ts     # service tests
    <module>-commands.spec.ts    # command handlers
    <module>-queries.spec.ts     # query handlers (split -simple / -complex if large)
    <module>-events.spec.ts      # event handlers
    dto-validation.spec.ts       # DTO validation
```

| Testing | File |
|---|---|
| Service | `<module>-service.spec.ts` |
| Command handlers | `<module>-commands.spec.ts` |
| Query handlers | `<module>-queries.spec.ts` (or `-simple` / `-complex`) |
| Event handlers | `<module>-events.spec.ts` |
| Mixed CQRS handlers | `<module>-handlers.spec.ts` |
| DTO validation | `dto-validation.spec.ts` |
| Controller | `<module>-controller.spec.ts` |

Specs mirror `src/modules/<module>/`. Split a spec past ~800 lines by complexity. Import mocks from
the relative `../../test-utils`, never an absolute path.

### 2. Jest config — two projects

One config, two projects so `unit` and `integration` run (and are selectable) separately:

```js
const sharedConfig = {
  moduleFileExtensions: ['js', 'json', 'ts'],
  transform: { '^.+\\.(t|j)s$': ['@swc/jest', { /* decorators on */ }] },
  moduleNameMapper: { /* '@org/<lib>': '<rootDir>/libs/<lib>/src', ... (mirror tsconfig paths) */ },
};
module.exports = {
  rootDir: './', maxWorkers: '50%', testTimeout: 30_000,
  collectCoverageFrom: ['./src/**/*.(t|j)s'],
  coveragePathIgnorePatterns: ['.module.ts', '<rootDir>/src/config/*', '<rootDir>/src/main.ts', '.mock.ts'],
  projects: [
    { ...sharedConfig, displayName: 'unit', setupFiles: ['reflect-metadata'],
      testMatch: ['<rootDir>/test/unit/**/*.spec.ts'] },
    { ...sharedConfig, displayName: 'integration', setupFilesAfterEnv: ['./test/setup-app.ts'],
      testRegex: 'test.e2e.ts' },
  ],
};
```

- `setupFiles: ['reflect-metadata']` on the **unit** project — NestJS decorator metadata without
  bootstrapping the app. `setupFilesAfterEnv: ['./test/setup-app.ts']` on **integration** boots the
  app once (the [write-service-code](./write-service-code.md) §8 harness).
- Run one file: `pnpm jest --selectProjects unit --testPathPattern '<your-file>'`.

### 3. Shared mock factories (`test/unit/test-utils.ts`)

One module of small factory functions keeps specs fast and identical. The reusable core (copy as-is;
chain methods return `this`, terminal methods return configurable defaults):

```ts
import { EventBus, CommandBus, QueryBus } from '@nestjs/cqrs';
import { ConfigService } from '@nestjs/config';
import { Test, TestingModule } from '@nestjs/testing';
import { DataSource } from 'typeorm';
import { Type } from '@nestjs/common';

export function createMockQueryBuilder(getOneResult?: any, getOneOrFailResult?: any) {
  const qb: Record<string, jest.Mock> = {};
  for (const m of ['select','addSelect','where','andWhere','orWhere','innerJoin','leftJoin',
    'innerJoinAndSelect','leftJoinAndSelect','orderBy','addOrderBy','skip','take','limit','offset',
    'groupBy','having','setParameter','from','update','set','insert','into','values','withDeleted','distinct']) {
    qb[m] = jest.fn().mockReturnValue(qb);          // chain → return self
  }
  qb.getOne = jest.fn().mockResolvedValue(getOneResult ?? null);
  qb.getOneOrFail = jest.fn().mockResolvedValue(getOneOrFailResult ?? getOneResult);
  qb.getMany = jest.fn().mockResolvedValue([]);
  qb.getManyAndCount = jest.fn().mockResolvedValue([[], 0]);
  qb.getCount = jest.fn().mockResolvedValue(0);
  qb.getRawOne = jest.fn().mockResolvedValue(null);
  qb.getRawMany = jest.fn().mockResolvedValue([]);
  qb.execute = jest.fn().mockResolvedValue(undefined);
  return qb;
}

export function createMockRepository() {
  return {
    findOne: jest.fn(), findOneBy: jest.fn(), find: jest.fn(),
    findAndCount: jest.fn().mockResolvedValue([[], 0]),
    save: jest.fn().mockImplementation((e: any) => Promise.resolve(e)),
    create: jest.fn().mockImplementation((e: any) => e),
    insert: jest.fn().mockResolvedValue({ identifiers: [{ id: 'mock-id' }] }),
    update: jest.fn().mockResolvedValue({ affected: 1 }),
    delete: jest.fn().mockResolvedValue({ affected: 1 }),
    count: jest.fn().mockResolvedValue(0),
    createQueryBuilder: jest.fn(),
  };
}

export function createMockEntityManager(): Record<string, jest.Mock> {
  const em = { ...createMockRepository(), getRepository: jest.fn().mockReturnValue(createMockRepository()),
    transaction: jest.fn() } as Record<string, jest.Mock>;
  em.transaction.mockImplementation(async (cb: any) => cb(em));   // tx → calls back with the EM
  return em;
}

export function createMockDataSource(queryBuilder?: Record<string, jest.Mock>) {
  const qb = queryBuilder ?? createMockQueryBuilder();
  const manager = createMockEntityManager();
  manager.createQueryBuilder.mockReturnValue(qb);
  return {
    createQueryBuilder: jest.fn().mockReturnValue(qb),
    getRepository: jest.fn().mockReturnValue(createMockRepository()),
    transaction: jest.fn().mockImplementation(async (cb: any) => cb(manager)),
    manager,
  };
}

export const createMockLogger = () => ({ info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn(), verbose: jest.fn(), log: jest.fn() });
export const createMockEventBus = () => ({ publish: jest.fn(), publishAll: jest.fn() });
export const createMockCommandBus = () => ({ execute: jest.fn() });
export const createMockQueryBus = () => ({ execute: jest.fn() });
export const createMockQueue = () => ({ add: jest.fn(), process: jest.fn(), on: jest.fn(), getJob: jest.fn(), close: jest.fn() });
export const createMockConfigService = (overrides: Record<string, any> = {}) => {
  const defaults = { 'app.baseUrl': 'http://localhost:3000', 'app.env': 'test', ...overrides };
  return { get: jest.fn().mockImplementation((k: string) => defaults[k]) };
};
export const mockProvider = (token: any, value: any) => ({ provide: token, useValue: value });

// One CQRS handler, all common deps pre-wired. Add only the providers your handler needs.
export async function createHandlerTestingModule<H>(Handler: Type<H>, extraProviders: any[] = []) {
  const qb = createMockQueryBuilder();
  const dataSource = createMockDataSource(qb);
  const eventBus = createMockEventBus(), commandBus = createMockCommandBus(), queryBus = createMockQueryBus();
  const configService = createMockConfigService(), logger = createMockLogger();
  const module = await Test.createTestingModule({
    providers: [
      Handler,
      mockProvider(DataSource, dataSource),
      mockProvider('winston', logger),               // winston is injected by the string token 'winston'
      mockProvider(EventBus, eventBus), mockProvider(CommandBus, commandBus), mockProvider(QueryBus, queryBus),
      mockProvider(ConfigService, configService),
      ...extraProviders,
    ],
  }).compile();
  return { module, handler: module.get(Handler), qb, dataSource, eventBus, commandBus, queryBus, configService, logger };
}
```

**Domain-service mocks: one per service, same shape** — a plain object of `jest.fn()`s. Keep them in
`test-utils.ts` so every spec shares them:

```ts
export const createMockListingService = () => ({
  getListingById: jest.fn(),
  publishListing: jest.fn().mockResolvedValue(undefined),
  // ...one jest.fn() per public method
});
```

### 4. The three patterns

**Pattern 1 — CQRS handler (the fast path).** `createHandlerTestingModule` wires DataSource, the
three buses, ConfigService, and the logger; you add only the rest.

```ts
import { PublishListingHandler, PublishListingCommand } from '../../../../src/modules/listing/commands/publish-listing';
import { ListingService } from '../../../../src/modules/listing/listing.service';
import { AppNotFoundException } from '@org/infra-exception';
import { createHandlerTestingModule, createMockListingService, mockProvider } from '../../test-utils';

describe('PublishListingHandler', () => {
  let handler: PublishListingHandler;
  let qb: ReturnType<typeof import('../../test-utils').createMockQueryBuilder>;
  let listingService: ReturnType<typeof createMockListingService>;

  beforeEach(async () => {
    listingService = createMockListingService();
    ({ handler, qb } = await createHandlerTestingModule(PublishListingHandler, [
      mockProvider(ListingService, listingService),
    ]));
  });
  afterEach(() => jest.resetAllMocks());

  it('publishes when the listing exists', async () => {
    // Arrange
    qb.getOne.mockResolvedValueOnce({ id: '1', status: 'DRAFT' });

    // Act
    const result = await handler.execute(new PublishListingCommand('1'));

    // Assert — specific value, not toBeTruthy()
    expect(result.status).toBe('PUBLISHED');
  });

  it('throws when the listing is missing', async () => {
    qb.getOne.mockResolvedValueOnce(null);

    await expect(handler.execute(new PublishListingCommand('missing'))).rejects.toThrow(AppNotFoundException);
  });
});
```

**Pattern 2 — service (manual TestingModule).** Services have more deps; build the module with
`mockProvider`. The repository token is `getRepositoryToken(Entity)`; the logger token is the string
`'winston'`.

```ts
const qb = createMockQueryBuilder();
const repo = createMockRepository(); repo.createQueryBuilder.mockReturnValue(qb);
const module = await Test.createTestingModule({
  providers: [
    ListingService,
    mockProvider(DataSource, createMockDataSource(qb)),
    mockProvider(getRepositoryToken(Listing), repo),
    mockProvider('winston', createMockLogger()),
    // ...other deps
  ],
}).compile();
const service = module.get(ListingService);
```

**Pattern 3 — DTO validation.** `plainToInstance` + `validate` + a `flattenValidationErrors` helper
that mirrors the API's error shape:

```ts
// test/unit/helpers/validate-dto.ts
export function flattenValidationErrors(errors: ValidationError[]): Record<string, Record<string,string>|null> {
  const data: Record<string, any> = {};
  const walk = (errs: ValidationError[], parent?: string) => errs.forEach((e) => {
    const key = parent ? `${parent}.${e.property}` : e.property;
    if (e.constraints) data[key] = e.constraints;
    else if (e.children?.length) walk(e.children, key);
  });
  walk(errors);
  return data;
}

// spec
it('rejects an empty body', async () => {
  const dto = plainToInstance(CreateListingRequestDto, {});
  const data = flattenValidationErrors(await validate(dto, { whitelist: true }));

  expect(data).toMatchObject({ title: { isNotEmpty: expect.any(String) } });
});
```

### 5. Entity builders (`test/unit/factories/`)

In-memory builders (they do **not** touch the DB — that's the integration layer's job). Constructor
+ spread overrides + a sensible default for every field; override only what the test asserts. Use a
faker lib for incidental values.

```ts
export function buildListing(overrides: Partial<Listing> = {}): Listing {
  return new Listing({
    id: overrides.id ?? uuidv4(), status: ListingStatus.DRAFT, title: faker.commerce.productName(),
    price: 10, currency: 'SGD', isDeleted: false, createdAt: new Date(), updatedAt: new Date(),
    ...overrides,
  });
}
```

Re-export every builder from `factories/index.ts` (one-line imports), and keep a
`factories.smoke.spec.ts` that just calls each builder so a drifted default fails fast.

### 6. jest.mock patterns

Place `jest.mock()` **after imports, before `describe`** (Jest hoists them; this is the convention).

```ts
// timezone-sensitive: keep the real lib but pin plugins
jest.mock('dayjs', () => { const d = jest.requireActual('dayjs'); d.extend(jest.requireActual('dayjs/plugin/utc')); d.extend(jest.requireActual('dayjs/plugin/timezone')); return d; });
// stub a couple of shared utils, keep the rest real
jest.mock('../../../../src/shared/utils', () => ({ ...jest.requireActual('../../../../src/shared/utils'), getDeepLink: jest.fn().mockResolvedValue('https://x.test') }));
```

### 7. Assertions & cleanup

- **QueryBuilder:** `expect(qb.where).toHaveBeenCalledWith('listing.id = :id', { id: '1' })`,
  `expect(qb.getOne).toHaveBeenCalled()`.
- **Events:** `expect(eventBus.publish).toHaveBeenCalledWith(expect.any(ListingPublishedEvent))` or
  `expect.objectContaining({ listingId: '1' })`.
- **Transactions:** the mock `dataSource.transaction()` calls back with `dataSource.manager` — set
  `dataSource.manager.findOne.mockResolvedValueOnce(...)` then assert `dataSource.manager.save`.
- **Cleanup:** `afterEach(() => jest.resetAllMocks())` — `resetAllMocks` (not `clearAllMocks`) so
  implementations reset too and tests don't pollute each other.
- AAA, one Act, faker, `it.each` for branch variants, and specific-value matchers
  (`toBe`/`toMatchObject`/`toEqual`/`arrayContaining`) — same as
  [write-service-code](./write-service-code.md) §8 and [code-conventions](./code-conventions.md) §4.

## Verification

- A spec sits in `test/unit/modules/<module>/` with the naming convention; imports mocks from
  `../../test-utils`; uses `createHandlerTestingModule` (handlers) or manual `Test.createTestingModule`
  (services).
- Entity data comes from `../../factories` builders; incidental values from faker.
- Every spec ends with `afterEach(() => jest.resetAllMocks())`.
- Tests cover happy path + error/not-found + business edge cases, asserting **specific** values.
- `pnpm jest --selectProjects unit --testPathPattern '<file>'` passes; coverage report run on new code.

## Related

- [write-service-code](./write-service-code.md) — §8 is the integration/boundary layer (real DB);
  the rest is the production code these tests exercise.
- [structure-a-backend-service](./structure-a-backend-service.md) — module/handler/DTO layout the
  specs mirror.
- [code-conventions](./code-conventions.md) — AAA, faker, `it.each`, matchers.
- `CLAUDE.md` — *Testing Rules / HTTP-layer testing rule* (when a repo is
  integration-only and skips the unit layer).
