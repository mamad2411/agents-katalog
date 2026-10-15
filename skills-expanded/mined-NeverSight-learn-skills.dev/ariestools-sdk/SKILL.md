---
name: ariestools-sdk
description: Aries Tools shared TypeScript/JavaScript utility libraries from the sdk-js monorepo. Covers the @ariestools/sdk umbrella (assert, delay, fetch, hex, promise, storage, zod helpers, and other modules), specialist packages (express, storage-adapters, threads, testing, telemetry, crypto-auth, eth-address, pixel, json-rpc-engine), import conventions, optional peers, and migration from retired @xylabs/* names. Use when importing or choosing @ariestools/* utilities, wiring HTTP clients, storage adapters, workers, Express APIs, or Vitest matchers.
metadata:
  version: 0.1.3 # x-release-please-version
---

# Aries Tools SDK

Use the active packages from [`ariestools/sdk-js`](https://github.com/ariestools/sdk-js) under the `@ariestools/*` scope. Do not install retired `@xylabs/*` utility names for new work.

This skill builds on [xy-development](../xy-development/SKILL.md) and [xy-toolchain](../xy-toolchain/SKILL.md). Prefer existing repository dependencies and versions; pin according to the consuming repo.

**Skill identity.** When reporting which skills informed your work, format as `ariestools-sdk v<version>` from this file's `metadata.version`.

## References

### [Overview and install](overview.md)

Read first when choosing the umbrella vs specialist packages, installing `@ariestools/sdk`, interpreting peers (`zod`, OpenTelemetry), or migrating from `@xylabs/*`.

### [Umbrella modules](modules.md)

Read when picking a utility inside `@ariestools/sdk` (assert, delay, fetch, hex, promise, retry, storage, typeof, logger, …) or choosing a subpath export.

### [Specialist packages](packages.md)

Read when you need Express helpers, IndexedDB/Mongo adapters, threads/workers, testing matchers, telemetry, crypto-auth, eth-address, pixel, or json-rpc-engine — packages that are **not** fully replaced by the main umbrella install alone.

### [Fetch and HTTP](fetch.md)

Read when calling `fetchJson` / `FetchClient`, injecting a custom fetcher, or configuring Node HTTP caching with Undici (consumer-owned).

### [Conventions](conventions.md)

Read for import style, tree-shaking, platform-conditional modules, deprecations (telemetry re-exports, crypto polyfills), and how this monorepo relates to the `xy` toolchain.
