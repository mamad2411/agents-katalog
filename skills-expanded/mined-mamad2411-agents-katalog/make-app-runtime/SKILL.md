---
name: make-app-runtime
description: Use when generating, refactoring, reviewing, or debugging Make App project runtime structure, workspace manifests, Service runtime, local/dev scripts, build outputs, Docker/K8s image entrypoints, publish readiness, or packaging errors such as missing `apps/service/dist/server.js`. Covers `apps/` workspace contracts, `apps/ui/dist`, `apps/service` port/build/start contracts, runtime config file location, runtime artifact tests, and forwarded host/proto header preservation. Does not cover UI layout, authentication implementation, Make adapter env semantics, DSL modeling, Make CLI resource deployment, or canvas-table internals.
---

# make-app-runtime

Use this skill for Make App runtime and packaging contracts. These rules are intentionally strict because platform image entrypoints and publish artifacts should not vary per POC.

This skill owns project runtime structure, workspace manifests, build outputs, Service start entry, Service port baseline, runtime config file location, Docker/K8s runtime entry alignment, and publish-readiness checks.

It does not own UI layout (`makeui`), authentication implementation (`make-app-auth`), Make adapter environment variable semantics (`make-app-service`), DSL modeling (`makedsl`), Make resource deployment (`makecli`), or canvas-table behavior (`canvas-table-integration`).

## Quick start

1. Identify whether the task touches `apps/`, `apps/service`, `apps/ui/dist`, package scripts, Docker/K8s, image entrypoints, publish readiness, or a runtime error such as `Cannot find module '/app/apps/service/dist/server.js'`.
2. Preserve the platform image contract unless the user explicitly says the platform contract itself is changing.
3. Verify workspace manifests before source layout: `apps/package.json`, `apps/pnpm-workspace.yaml`, `apps/ui/package.json`, and `apps/service/package.json`.
4. Verify build artifacts before declaring ready: frontend `apps/ui/dist`, Service `apps/service/dist/server.js`.
5. Add or preserve a contract test for the Service runtime entry.

## Workspace contract

Generated or reorganized Make App projects use:

- `apps/ui`
- `apps/service`
- `apps/dsl`
- `apps/docs`
- `apps/packages/*` when shared packages are needed

Required workspace files:

- `apps/package.json`
- `apps/pnpm-workspace.yaml`
- `apps/ui/package.json`
- `apps/service/package.json`

`apps/pnpm-workspace.yaml` must include:

```yaml
packages:
  - "ui"
  - "service"
  - "packages/*"
```

`apps/package.json` must provide runnable scripts such as `app:ui`, `app:service`, `dev`, and `build`. `pnpm --filter` targets must match the actual package names, including scoped names.

## Frontend build contract

Frontend publish artifacts live in `apps/ui/dist`.

Generated or updated Vite config should set:

- `build.outDir: "dist"`
- `build.emptyOutDir: true`

Do not publish or configure static asset discovery against root `dist` or `apps/dist`.

## Service runtime contract

The platform image default Service entry is:

```text
/app/apps/service/dist/server.js
```

Therefore the default TypeScript Service contract is:

- source entry: `apps/service/src/server.ts`
- compiled entry: `apps/service/dist/server.js`
- production start script: `node dist/server.js`
- dev script may use `tsx watch src/server.ts`, but production start must not use `tsx`
- Service HTTP port: `3000`
- centralized runtime config entry: `apps/service/src/config.ts`

`apps/service/tsconfig.json` must compile the runtime source to that path:

```json
{
  "compilerOptions": {
    "rootDir": "src",
    "outDir": "dist"
  },
  "include": ["src/**/*.ts"],
  "exclude": ["src/**/*.test.ts", "test", "dist"]
}
```

`apps/service/package.json` must include scripts equivalent to:

```json
{
  "scripts": {
    "dev": "tsx watch src/server.ts",
    "build": "tsc -p tsconfig.json",
    "start": "node dist/server.js",
    "test": "vitest run"
  }
}
```

Do not leave Docker, K8s, makecli, package scripts, or docs pointing at `/app/apps/service/dist/server.js` unless `pnpm --filter <service-package> build` creates `apps/service/dist/server.js`.

If a legacy project intentionally uses a different Service entry or build tool, keep it only when all runtime references agree: Docker/K8s entrypoint, package `start`, docs, build output, and readiness tests.

## Service build contract test

Service-backed Apps should include a test that protects the runtime entry contract. The test may live in `apps/service/test/service-build-contract.test.ts` or the project's established test location.

It should assert:

- `apps/service/package.json` has a `build` script
- `apps/service/package.json` production start points to `node dist/server.js` when the platform image uses that entry
- `apps/service/tsconfig.json` uses `rootDir: "src"` and `outDir: "dist"`
- after build, `apps/service/dist/server.js` exists

Run the Service build before relying on that artifact:

```bash
pnpm --filter <service-package-name> build
test -f apps/service/dist/server.js
```

## Runtime config location and port

Service runtime environment reads are centralized in `apps/service/src/config.ts` for new projects. This skill only requires the config entry location and fixed port handling needed by runtime/startup. Make adapter variables such as `MAKE_API_BASE_URL`, `MAKE_SERVER_URL`, `MAKE_AUTH_BASE_URL`, and `MAKE_BUSINESS_BASE_URL` belong to `make-app-service`.

Service HTTP port is fixed to `3000`. Generated or refactored Service code, `.env.example`, docs, health checks, tests, CORS, and UI local Service base URL examples must align to `3000`.

If local `3000` is occupied during development, report the conflict. Do not silently change the Service contract port.

`make-app-runtime` does not decide which environment connects to which Make domain, gateway, or API host. Domain mapping, gateway routing, and secret injection belong to backend, operations, Make tooling, or deployed runtime config.

## Forwarded request headers

When Service forwards requests to a Make gateway and that gateway needs request-origin context, preserve or set standard forwarded headers:

- `X-Forwarded-Host`
- `X-Forwarded-Proto`

Do not hard-code environment domains in generated Service code. Use the incoming request context or the host runtime proxy contract.

## Readiness checks

Before reporting a Service-backed App as ready to publish or ready for user-domain access:

1. Run the workspace build that produces `apps/ui/dist`.
2. Run the Service build.
3. Verify `apps/service/dist/server.js` exists when the runtime entry points there.
4. Run the Service contract test.
5. If a start smoke is available, start the built Service with the production start script and verify it reaches the expected health or root response, then stop it.

Do not mark a Service-backed App ready based only on successful local `tsx src/server.ts` development startup.

## Common failure diagnosis

Error:

```text
Cannot find module '/app/apps/service/dist/server.js'
```

Treat it as a runtime contract failure:

- build did not run, or
- `src/server.ts` was missing, or
- `tsconfig` emitted somewhere else, or
- package `start` / image entry points to a file the build does not create.

Fix the build/start contract. Do not work around it by changing UI code or auth behavior.
