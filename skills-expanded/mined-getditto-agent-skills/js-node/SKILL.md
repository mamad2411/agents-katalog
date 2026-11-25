---
name: js-node
description: >
  Builds and troubleshoots Ditto JavaScript/TypeScript Node.js services, console tools and Electron main processes using @dittolive/ditto. Covers native binaries, persistent paths, process lifetime and shutdown. Not browser or React Native setup.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Ditto on Node.js

Use [js-sdk](../js-sdk/SKILL.md) for API contracts. This recipe owns Node deployment.

## Workflow

1. Inspect package.json, lockfile, Node version, OS and architecture. Use an active or
   maintenance Node LTS; the fixture uses Node 22+. For a new project pin the version the
   user asked for, or else the latest stable (npm `latest`, 5.2.0 when authored); keep an
   existing project's version. Preserve CommonJS/ESM conventions (`.mjs` or type:module for ESM).
2. Run the [minimal program](../js-sdk/assets/minimal-app.mjs) with a development offline
   license. For a service use the [runtime](../js-sdk/assets/runtime.ts) and a stable,
   writable absolute directory on a persistent volume. One owner per directory.
3. Server mode uses the customer's Portal URL plus a token provider. Await auth-handler
   installation; local data availability and remote auth are separate states.
4. Keep subscriptions for the service's data scope and retain observers. Parameterize
   queries. Serve decoded DTOs to HTTP clients; do not expose the Ditto object or keys.
5. Handle SIGINT/SIGTERM once: stop accepting work, await outstanding tasks, cancel
   listeners, await runtime.close, then allow process exit. Do not call process.exit
   before asynchronous cleanup finishes. Unhandled rejections must fail the service.
6. Restart and verify persistence; run a second peer with the same database identity
   and a different directory to prove synchronization, not just local inserts.

## Deployment traps

The package uses a native `.node` binding. The 5.2.0 distribution includes macOS ARM64,
Linux x64/ARM64, and Windows x64 binaries. Inspect package contents for an existing
release before promising a different architecture; do not copy a development machine's
node_modules to a different target. Use a compatible glibc Linux base; don't assume
Alpine/musl compatibility. Native bindings are not an edge-runtime/WASM substitute.

For bundling, externalize the SDK or retain its relative native-binary layout; verify
the actual deployed artifact starts on its target OS. Electron's main process owns
the store and communicates through a deliberately scoped IPC API; don't pass native
handles across processes. Avoid Node imports in shared React/web/native files.

Do not create a new instance per HTTP request, worker, hot reload, or job invocation
using the same path. For serverless ephemeral filesystems explicitly explain the
persistence/lifetime limitations before choosing this deployment.

## Verification

The repository's JS test harness runs the [minimal program](../js-sdk/assets/minimal-app.mjs) in CI. It
uses a disposable directory; production examples must choose an application data path.
No real customer backend or cloud resources are provisioned by this recipe.

Sources: <https://docs.ditto.live/sdk/latest/install-guides/js>,
<https://docs.ditto.live/sdk/latest/compatibility/nodejs> and the published package.
