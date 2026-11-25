---
name: setup-artillery-cli-for-load-testing
description: >-
  Set up Artillery load testing for any project. Detects package manager and
  project type, creates a TypeScript test script (HTTP or Playwright browser),
  configures Artillery Cloud, and provides the run command. Use when the user
  wants to add load testing, performance testing, or browser-based load testing
  to their project.
compatibility: Requires Node.js/Bun (or npx). For Playwright path, requires a Chromium-capable environment.
metadata:
  author: artilleryio
  version: "1.0"
allowed-tools: Bash Read Write Glob Grep
---

# Artillery: Set up load testing for this project

You are setting up Artillery (https://artillery.io), a load testing tool, for this project. Follow the steps below. Ask the user questions at each decision point marked with DECISION.

## Step 1: Detect environment

Examine the project to determine:
- **Package manager**: Look for `package-lock.json` (npm), `pnpm-lock.yaml` (pnpm), `yarn.lock` (yarn), `bun.lockb` (bun). If none exist, this is a non-JS project — you will use `npx`.
- **Monorepo vs single service**: Look for `turbo.json`, `pnpm-workspace.yaml`, `lerna.json`, or `workspaces` in `package.json`.
- **Existing test infrastructure**: Look for `playwright.config.ts`, `tests/`, `e2e/`, or existing load test files.
- **Target**: Look for server startup scripts, `dev` commands, API routes, or a deployed URL.

## Step 2: Ask the user

DECISION — Ask these questions:

1. **What do you want to test?**
   - **(A) HTTP endpoints** — API routes, REST endpoints, GraphQL
   - **(B) Browser flows with Playwright** — user journeys, page loads, UI interactions

2. **What is the target URL?** (e.g. `http://localhost:3000`, `https://staging.example.com`). If you can infer it from the project config, suggest it.

3. **Do you have an Artillery Cloud account?** (free at https://app.artillery.io). If yes, ask for their API key (found in Settings > API Keys).

## Step 3: Install Artillery

Based on detected package manager:

| Package manager | Command |
|---|---|
| npm | `npm install -D artillery` |
| pnpm | `pnpm add -D artillery` |
| yarn | `yarn add -D artillery` |
| bun | `bun add -D artillery` |
| non-JS project | No install. Use `npx artillery@latest` to run. |

If the user chose **(B) Playwright**, also install Playwright browsers (the Playwright engine is included in Artillery — no separate package needed):

```bash
npx playwright install
```

## Step 4: Write the test script

Create the test as a **TypeScript file**. Place it at a sensible location (e.g. `load-tests/test.ts`, `tests/load/test.ts`, or alongside existing test files). Use `.ts` extension always.

### Path A: HTTP endpoint test

```typescript
import type { Config, Scenario } from "artillery";

export const config: Config = {
  target: "TARGET_URL",
  phases: [
    {
      duration: 30,     // seconds
      arrivalRate: 1,   // 1 new virtual users per second
      name: "warm_up",
    },
  ],
};

export const scenarios: Scenario[] = [
  {
    name: "SCENARIO_NAME",
    engine: "http",
    flow: [
      { get: { url: "/ENDPOINT" } },
    ],
  },
];
```

Adapt this template:
- Set `target` to the user's URL
- Replace `/ENDPOINT` with a real endpoint from the project (prefer GET, read-only)
- If the API needs auth headers, add `config.http.defaults.headers`
- For POST requests: `{ post: { url: "/path", json: { key: "value" } } }`
- Name the scenario descriptively based on what it tests

### Path B: Playwright browser test

```typescript
import type { Config, Scenario, PlaywrightTestFunction } from "artillery";

export const config: Config = {
  target: "TARGET_URL",
  phases: [
    {
      duration: 10,
      arrivalCount: 2,  // total 2 browser sessions over 10s (safe default)
      name: "smoke",
    },
  ],
  engines: {
    playwright: {},
  },
};

export const testFunction: PlaywrightTestFunction = async (page, vuContext, events, test) => {
  await test.step("Go to homepage", async () => {
    await page.goto("TARGET_URL");
    await page.waitForLoadState("networkidle");
  });

  await test.step("DESCRIBE_ACTION", async () => {
    // Add user interaction here:
    // await page.click('text=Sign In');
    // await page.fill('#email', 'test@example.com');
    // await page.waitForURL('**/dashboard');
  });
};

export const scenarios: Scenario[] = [
  {
    name: "SCENARIO_NAME",
    engine: "playwright",
    testFunction: "testFunction",
  },
];
```

Adapt this template:
- Fill in real page interactions based on the project's UI
- Keep virtual user count low (arrivalCount: 2-5) for first run
- Use `test.step()` to label each logical action — these show up in Artillery Cloud
- If the project has existing Playwright tests, reuse their selectors/patterns

## Step 5: Artillery Cloud setup (if user has API key)

If the user provided an API key, instruct them to set the environment variable:

```bash
export ARTILLERY_CLOUD_API_KEY=<their-key>
```

Or they can pass it inline with the run command using `--key`.

## Step 6: Give the run command

**Do NOT run the test.** Output the command for the user to run themselves.

Basic run:
```bash
npx artillery run ./path/to/test.ts
```

With Artillery Cloud recording:
```bash
npx artillery run --record ./path/to/test.ts
```

With inline API key:
```bash
npx artillery run --record --key <API_KEY> ./path/to/test.ts
```

Tell the user:
- The test will generate load against the target. Make sure the target is running.
- First run uses conservative settings (low arrivalRate/arrivalCount). They can increase after verifying it works.
- Results appear in the terminal. If `--record` is used, a link to Artillery Cloud dashboard will be printed.
- To scale up later, add more phases:
  ```typescript
  phases: [
    { duration: 30, arrivalRate: 5, name: "warm_up" },
    { duration: 60, arrivalRate: 5, rampTo: 50, name: "ramp_up" },
    { duration: 120, arrivalRate: 50, name: "sustained" },
  ]
  ```

## Reference: Artillery TypeScript script structure

- `export const config: Config` — target URL, phases, engine config, plugins
- `export const scenarios: Scenario[]` — array of test scenarios
- HTTP scenarios: set `engine: "http"`, then `flow` is auto-typed — `{ get: { url } }`, `{ post: { url, json } }`, `{ put: ... }`, `{ delete: ... }`, `{ log: ... }`, `{ think: ... }`, `{ loop: [...] }`
- Playwright scenarios: set `engine: "playwright"` and `testFunction: "functionName"`, export the function
- Playwright testFunction: `export const fn: PlaywrightTestFunction = async (page, vuContext, events, test) => { ... }` — all params auto-typed
- `test.step(name, fn)` — labels steps for reporting
- Types available: `import type { Config, Scenario, PlaywrightTestFunction } from "artillery"`
