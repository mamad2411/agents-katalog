---
description: Phase 4 helper for w-task — generate test file skeletons with layer-aware import boilerplate (unit / integration / graphql / bullmq / nestjs / nextjs) from impact.md, so TDD starts with structured RED, not blank files.
argument-hint: <task-slug>
allowed-tools: Bash, Read, Write, Edit
---

# w-test-stubs

Read `impact.md § Affected Files` and create test file skeletons for each, using
the boilerplate appropriate to each affected file's layer.

Reads `.claude/workflow.yaml`:
- `project.test_layers` (e.g. `[unit, integration, graphql, bullmq]`)
- `project.test_command`
- `project.codegraph.*` — when a CodeGraph index is usable, Step 0 finds the tests that
  already cover the change

---

## Inputs

- `$1` — task slug

Reads `<state_root>/<task-slug>/impact.md`.

---

## Step 0 — Existing coverage (CodeGraph)

*Runs when `state.yaml.codegraph` is `ready` or `stale`, or when w-task passes an
affected-test list.*

```bash
codegraph affected <files from impact.md § Affected Files> --depth 5 --quiet
```

Every path returned is a test that **already exercises code in scope**. For each:

- **Extend it** — add the new cases to that file. Do not create a parallel stub for
  the same subject; two half-covering suites for one unit is worse than one, because
  neither run tells you the subject is covered.
- Record it in the summary as `extended` rather than `created`.

Only files with no covering test proceed to Step 1.

Without CodeGraph, the layer-glob conventions below decide the target path, and an
existing file at that path is preserved (never overwritten) as before.

---

## Step 1 — Classify each affected file

For each entry in § Affected Files, classify the layer based on path / suffix:

| Pattern | Layer |
|---------|-------|
| `*.service.ts` / `*.utils.ts` / `*.lib.ts` | unit |
| `*.resolver.ts` / `*.graphql.ts` / `@Query` decorator | graphql |
| `*.processor.ts` / `bullmq`, `queue` in path | bullmq |
| `*.controller.ts` / `*.handler.ts` | nestjs |
| `*.tsx` / `app/**/page.tsx` | nextjs |
| `*.spec.ts` / `*.test.ts` (already exists) | skip — already a test |
| `*.e2e-spec.ts` / `__tests__/integration` | integration |

If the layer detected is NOT in `project.test_layers`: skip that file or fall
back to `unit`.

---

## Step 2 — Pick boilerplate

Use the boilerplate matching the file's layer. Default templates:

### unit (Jest/Vitest, no NestJS)
```ts
import { describe, expect, it, vi, beforeEach } from 'vitest'; // or jest equivalents
import { <ClassOrFn> } from './<file-stem>';

describe('<ClassOrFn>', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should <behaviour>', () => {
    // arrange
    // act
    // assert
    expect(true).toBe(false); // RED
  });
});
```

### graphql (NestJS + GraphQL)
```ts
import { Test, TestingModule } from '@nestjs/testing';
import { <Resolver> } from './<file-stem>';
import { <Service> } from './<service-stem>';

describe('<Resolver>', () => {
  let resolver: <Resolver>;
  let service: jest.Mocked<<Service>>;

  beforeEach(async () => {
    const moduleRef: TestingModule = await Test.createTestingModule({
      providers: [
        <Resolver>,
        { provide: <Service>, useValue: { /* mocked methods */ } },
      ],
    }).compile();

    resolver = moduleRef.get(<Resolver>);
    service = moduleRef.get(<Service>);
  });

  it('should <operation behaviour>', async () => {
    expect(true).toBe(false); // RED
  });
});
```

### bullmq (NestJS + queue processor)
```ts
import { Test, TestingModule } from '@nestjs/testing';
import { Job } from 'bullmq';
import { <Processor> } from './<file-stem>';

describe('<Processor>', () => {
  let processor: <Processor>;

  beforeEach(async () => {
    const moduleRef: TestingModule = await Test.createTestingModule({
      providers: [<Processor>],
    }).compile();
    processor = moduleRef.get(<Processor>);
  });

  it('should process job <name>', async () => {
    const job = { data: {} } as Job;
    await expect(processor.process(job)).rejects.toThrow(); // RED
  });
});
```

### nestjs (controller/service)
```ts
import { Test, TestingModule } from '@nestjs/testing';
import { <Controller> } from './<file-stem>';

describe('<Controller>', () => {
  let controller: <Controller>;

  beforeEach(async () => {
    const moduleRef: TestingModule = await Test.createTestingModule({
      controllers: [<Controller>],
    }).compile();
    controller = moduleRef.get(<Controller>);
  });

  it('should <behaviour>', () => {
    expect(true).toBe(false); // RED
  });
});
```

### nextjs (React component / server action)
```ts
import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import <Component> from './<file-stem>';

describe('<Component>', () => {
  it('should render <element>', () => {
    render(<<Component> />);
    expect(screen.queryByText('<text>')).toBeNull(); // RED
  });
});
```

### integration (real DB / external services)
```ts
import { Test } from '@nestjs/testing';
import { PrismaService } from 'src/database/prisma.service';
import { AppModule } from 'src/app/app.module';

describe('<Feature> integration', () => {
  let app: INestApplication;
  let prisma: PrismaService;

  beforeAll(async () => {
    const moduleRef = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();
    app = moduleRef.createNestApplication();
    await app.init();
    prisma = app.get(PrismaService);
  });

  afterAll(async () => {
    await app.close();
  });

  it('should <end-to-end behaviour>', async () => {
    expect(true).toBe(false); // RED
  });
});
```

---

## Step 3 — Locate test file path

For source `src/modules/<m>/<file>.<ext>`:
- Same-dir convention: `src/modules/<m>/<file>.spec.<ext>`
- Sibling-dir convention (if project uses `__tests__/`):
  `src/modules/<m>/__tests__/<file>.spec.<ext>`

Detect convention by looking at existing `*.spec.*` files near the affected file.

---

## Step 4 — Write stubs

For each classified file, write the stub (skip if test file already exists —
do NOT overwrite). Replace `<placeholder>` tokens with extracted class/function
names.

---

## Step 5 — Run tests → confirm RED

```bash
<test_command> 2>&1 | tail -30
```

If RED state confirmed (tests fail because assertions are intentionally wrong):
print summary.

If tests pass unexpectedly (no RED): warn — assertions were not strict enough.
Pause for developer.

---

## Step 6 — Report

```
Test stubs written:
  Layer: unit       — N files
  Layer: graphql    — N files
  Layer: bullmq     — N files
  ...
Total: N stubs

Test command run: <command>
State: RED ✗ (confirmed) | unexpected PASS (review needed)

Run /w-task to start RED→GREEN cycle.
```
