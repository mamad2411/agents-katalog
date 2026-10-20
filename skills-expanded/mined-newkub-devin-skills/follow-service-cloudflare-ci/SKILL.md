---
name: follow-service-cloudflare-ci
description: Use the Cloudflare CI SDK to run build, lint, test, typecheck on Workflows
argument-hint: "[scope]"
related:
  - follow-service-cloudflare
  - deploy-to-cloudflare
  - resolve-errors
  - follow-secret-manager
  - open-web-for-config-secret
---

## Goal

Create and run a CI pipeline on Cloudflare with the `CI SDK` and `Workflows` — from install dependencies, cache, build, lint, typecheck, test, without deploy

## Scope

Use for:
- Run CI on Cloudflare Workflows triggered by `artifact push` events
- Build, lint, typecheck, test in a sandboxed environment on Cloudflare
- Cache dependencies between CI steps with `cache.inputs`
- Self-healing CI with an AI agent that fixes broken steps (optional)
- Does not include deploying Worker/Pages — use `/deploy-to-cloudflare` or `/follow-service-cloudflare` for deploy

## Execute

### 1. Verify Prerequisites

> Goal: Check that the project is ready to use Cloudflare CI

1. Check `wrangler.jsonc` enables the `nodejs_compat` compatibility flag
2. Check the project has `package.json` and a lockfile (`bun.lock`, `pnpm-lock.yaml`, `package-lock.json`)
3. Check `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` for Wrangler
4. Use `/open-web-for-config-secret` if the keys are not yet in the secret manager

### 2. Install CI SDK

> Goal: Install `@cloudflare/ci` for the Workers runtime

Latest: `@cloudflare/ci@0.2.0` (verified 2026-09-16) — still a 0.x preview, the API may change

1. Run `bun add -D @cloudflare/ci` or `npm add -D @cloudflare/ci`
2. Verify `wrangler` version >= 4.68 to support the `events` field
3. Install `@cloudflare/workers-types` if using TypeScript

### 3. Define CI Workflow Worker

> Goal: Create the Worker that hosts the CI Workflow

1. Create the `ci/index.ts` or `workers/ci.ts` file
2. Import `CIWorkflow` and types from `@cloudflare/ci`:
   ```ts
   import { CIWorkflow } from '@cloudflare/ci';
   import type { CiContext, CiParams, CloudflareArtifacts } from '@cloudflare/ci';
   import type { WorkflowEvent, WorkflowStep } from 'cloudflare:workers';
   ```
3. Create a class extending `CIWorkflow`:
   ```ts
   export class CI extends CIWorkflow<CloudflareArtifacts, Bindings> {
     protected async pipeline(
       _event: WorkflowEvent<CiParams>,
       _step: WorkflowStep,
       ci: CiContext,
     ): Promise<void> {
       // define steps
     }
   }
   ```
4. Export the Worker entry with `export { CI }` or bind it in `wrangler.jsonc`

### 4. Define CI Steps

> Goal: Define install, build, lint, typecheck, test steps

1. Create the install step with cache:
   ```ts
   const deps = await ci.runner({
     name: 'install',
     command: 'bun install --frozen-lockfile',
     cache: { inputs: ['package.json', 'bun.lock'] },
   });
   ```
2. Run checks in parallel from the install result:
   ```ts
   await Promise.all([
     deps.runner({ name: 'lint', command: 'bun run lint' }),
     deps.runner({ name: 'test', command: 'bun run test' }),
     deps.runner({ name: 'typecheck', command: 'bun run typecheck' }),
     deps.runner({ name: 'build', command: 'bun run build' }),
   ]);
   ```
3. Use the lockfile matching the actual package manager (`pnpm-lock.yaml`, `package-lock.json`)
4. If any step fails → the Workflow stops and reports the error immediately

### 5. Configure Wrangler Events

> Goal: Trigger the CI Workflow when an artifact is pushed

1. Add the `events` field in `wrangler.jsonc`:
   ```jsonc
   {
     "name": "ci-worker",
     "main": "src/index.ts",
     "compatibility_date": "2026-09-01",
     "compatibility_flags": ["nodejs_compat"],
     "events": [
       {
         "type": "cf.artifacts.repo.pushed",
         "source": "*"
       }
     ]
   }
   ```
2. Filter repo/branch with the `source` pattern if needed
3. Run `wrangler deploy` to register the Workflow with the events

### 6. Set Up Artifacts Repo

> Goal: Connect the repo that needs to run CI

1. Verify the repo is pushed to Cloudflare Artifacts
2. Use `wrangler artifacts` or the dashboard to manage repos
3. Verify the `artifact push` event is sent to the CI Workflow

### 7. Monitor And Debug

> Goal: Monitor the CI run results

1. Use `wrangler workflows instances list` to view instances
2. Use `wrangler workflows instances logs <id>` to view logs
3. Use `wrangler tail` for real-time logs
4. Check errors with `/resolve-cicd` or `/follow-service-cloudflare`

### 8. Add Self-Healing (Optional)

> Goal: Let an AI agent help fix broken steps

1. Study the example at `https://github.com/cloudflare/ci/tree/main/examples/self-healing`
2. Add an agent step that consumes `CiRunnerFailureDiagnostics`
3. Use `isCiRunnerFailure` to detect failures then send them to the agent
4. Require the agent's pushed commit to be approved by the user before merge

## Rules

### 1. No Deploy

- This skill runs CI only, no deploy
- If deploy is needed, call `/deploy-to-cloudflare` or `/follow-service-cloudflare`
- Never write a deploy step in the CI Workflow under this skill

### 2. Idempotent Commands

- Every command in `ci.runner()` must be idempotent because Cloudflare Workflows has retry
- Never use commands with side effects that duplicate on retry

### 3. Cache Discipline

- cache inputs must point to the lockfile matching the actual package manager
- Verify the lockfile is not missing before commit
- If the lockfile changes → the install step reruns automatically

### 4. Security

- Use `/follow-secret-manager` for `CLOUDFLARE_API_TOKEN`
- Never hardcode credentials in `wrangler.jsonc` or CI code
- Use `vars` or `secrets` for account IDs and tokens

### 5. Compatibility

- Always enable `nodejs_compat` for `@cloudflare/ci`
- Use `wrangler` version >= 4.68 for the `events` field
- Use commands matching the package manager (`bun`, `pnpm`, `npm`)

- Use /resolve-errors if needed

## Merged Details

### references/package-manifest

#### Package Manifest



> Metadata of the primary package(s) this skill installs or covers. Update during `/update-devin-global-skills` or `/deep-review-codebase` runs.



##### Primary Package



| Field | Value |

|-------|-------|

| Package | `@cloudflare/ci` |

| Registry | `npm` |

| Latest Version | `0.2.0` |

| Release Date | `2026-09-03` |

| Verified | `2026-09-12` (date this file was last checked) |

| Author / Publisher | Cloudflare |

| License | `Apache-2.0` |

| Repository | `https://github.com/cloudflare/ci` |

| Website | `https://workers.cloudflare.com/` |

| Documentation | `https://github.com/cloudflare/ci#readme` |

| Releases / Changelog | `https://github.com/cloudflare/ci/releases` |



##### Install



```bash

bun add -D @cloudflare/ci

```



##### Secondary Packages



| Package | Registry | Latest | Notes |

|---------|----------|--------|-------|

| `wrangler` | `npm` | `4.131.1` | Required >= 4.68 for the `events` field in `wrangler.jsonc` |

| `@cloudflare/workers-types` | `npm` | `5.20260911.1` | TypeScript types for `WorkflowEvent`, `WorkflowStep`, `cloudflare:workers` |



##### Notes



- Breaking changes in latest major: `0.x` preview — API may change; requires `nodejs_compat` flag and Cloudflare Workflows + Artifacts

- Version pinned in SKILL.md: `0.2.0`

## Expected Outcome

- `@cloudflare/ci` installed and ready to use
- CI Workflow defined with install, build, lint, typecheck, test steps
- `artifact push` events trigger the CI run on Cloudflare Workflows
- Dependencies cached between steps
- CI logs inspectable via `wrangler`
- No deploy step in the CI Workflow
- Ready to hand off to `/deploy-to-cloudflare` if deploy is needed next
