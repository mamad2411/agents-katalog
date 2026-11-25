---
name: workers-best-practices
description: Reviews and authors Cloudflare Workers code against production best practices — covering async patterns, global state isolation, secret handling, compatibility flags, and TypeScript bindings. Use when writing new Workers, reviewing existing code for production readiness, or correcting violations of Cloudflare's canonical Workers patterns.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, wrangler_deploy, execute_command]
---

# Workers Best Practices

Reviews and authors Cloudflare Workers code against production best practices and runtime constraints.

Your knowledge of Cloudflare Workers APIs, types, and configuration may be outdated. **Prefer retrieval over pre-training** for any Workers code task — writing or reviewing.

## When to Use

- writing new Cloudflare Workers or refactoring edge handlers
- reviewing Workers code for production readiness and performance
- eliminating async floating promises, global state leaks, or secret violations
- enforcing dual-flag observability and streaming payload architectures
- generating and validating canonical Workers TypeScript bindings

## Core Rules

- **RETRIEVAL-FIRST**: Prefer retrieval over pre-training; verify API signatures and bindings against Cloudflare documentation.
- **OBSERVABILITY-DUAL-FLAG**: Mandatory dual observability in `wrangler.jsonc`: `"observability": { "enabled": true, "traces": { "enabled": true } }`.
- **STREAMING-MANDATE**: Stream large or unknown payloads via `ReadableStream` or `TransformStream`; never call `await response.text()` or `await response.json()` on unbounded external data.
- **STATE-ISOLATION**: Never store request-scoped data in module-level mutable variables; isolates are shared across concurrent requests.
- **ASYNC-LIFECYCLE**: Never use floating promises; bind all background tasks to `ctx.waitUntil()`. Never destructure `ctx` (e.g. `const { waitUntil } = ctx` breaks V8 context).
- **CRYPTO-HYGIENE**: Use cryptographic random values from Web Crypto (`crypto.randomUUID()`) instead of standard `Math.random()`.
- **TYPE-GENERATION**: Run `wrangler types` to generate typings automatically; hand-writing `interface Env` is strictly prohibited.
- **COMPAT-FLAGS**: Enable Node.js compatibility using `"compatibility_flags": ["nodejs_compat"]` in `wrangler.jsonc` when libraries require Node.js built-ins.
- **SMART-PLACEMENT**: Enable Smart Placement (`"placement": { "mode": "smart" }`) in `wrangler.jsonc` to route execution adjacent to backend data sources.
- **CPU-OPTIMIZATION**: Minimize isolate CPU time via `TextDecoder`, request coalescing, and profiling hot loops.

## Retrieval Sources

| Source | How to retrieve | Use for |
| :--- | :--- | :--- |
| Workers Best Practices | `https://developers.cloudflare.com/workers/best-practices/workers-best-practices/` | Canonical rules, patterns, anti-patterns |
| Workers Configuration | `https://developers.cloudflare.com/workers/wrangler/configuration/` | `wrangler.jsonc` fields, observability, placement |
| Wrangler Schema | `node_modules/wrangler/config-schema.json` | Binding shapes, allowed flags, types |
| Cloudflare Docs | Search tool or `https://developers.cloudflare.com/workers/` | API reference, compatibility dates/flags |

## Suggested Process

1. Inspect compatibility date and Node.js compat flags in `wrangler.jsonc`.
2. Verify dual observability is configured: `"observability": { "enabled": true, "traces": { "enabled": true } }`.
3. Run `wrangler types` to verify TypeScript bindings and eliminate hand-written `Env` definitions.
4. Review worker handlers for async execution blocks, verifying all background promises use `ctx.waitUntil()`.
5. Audit request scope structures, ensuring request-specific state is strictly scoped to the handler.
6. Verify payload handling to ensure unbounded streams are not buffered into memory with `response.text()`.
7. Audit crypto routines to ensure `crypto.randomUUID()` replaces any `Math.random()` invocations.

## Checklist

- [ ] Dual observability is enabled (`observability.enabled: true` and `observability.traces.enabled: true`).
- [ ] Compatibility date is pinned to a recent stable release ($\ge \text{2026-09-23}$).
- [ ] TypeScript typings match active Wrangler bindings via `wrangler types`.
- [ ] Request handlers avoid global mutable variables and module-level request caching.
- [ ] Async background tasks are wrapped in `ctx.waitUntil()` without destructuring `ctx`.
- [ ] Unbounded network responses are streamed using `ReadableStream` instead of `await response.text()`.
- [ ] Secrets and tokens are securely loaded via Wrangler secrets (not `.dev.vars` in commits).
- [ ] Smart Placement is enabled in `wrangler.jsonc` for database-adjacent routing.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/edge-deployment-spec.json`** — capture the runtime configuration, observability flags, bindings, secret names, and smoke test verifications. Set `produced_by_role` to `cloudflare-engineer`.

## Failure Modes

- **Observability disabled**: omitting `observability.traces.enabled` blinds operators during edge latency spikes and subrequest failures. Mitigation: enforce dual observability flags in CI linting.
- **Global mutable state**: a request-scoped variable is stored at module level, leaking across concurrent tenant requests. Mitigation: enforce handler-scoped state isolation; reject module-level mutable variables.
- **Floating promise**: an async call is started without `await` or `ctx.waitUntil()`, losing results and leaking isolate resources. Mitigation: wrap every async call in `await` or pass to `ctx.waitUntil()`.
- **Memory buffer exhaustion**: `await response.text()` called on unbounded external streams exhausts V8 isolate memory (128MB). Mitigation: pipe directly with `ReadableStream` or `TransformStream`.
- **Hand-written `Env` interface**: TypeScript bindings maintained by hand drift from live Wrangler resources. Mitigation: regenerate via `wrangler types` after every configuration edit.
- **`ctx` destructuring**: `const { waitUntil } = ctx` drops runtime execution context and throws invocation errors. Mitigation: always pass `ctx` intact and invoke `ctx.waitUntil()`.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: scope every review change strictly to Workers best-practices; reject unbounded alterations to business logic.
- **ASI03 Identity & Privilege Abuse**: secrets must be injected via `wrangler secret put`; never commit `.dev.vars` or inline tokens.
- **ASI04 Supply Chain**: validate all npm adapters and dependencies against trusted manifests before deployment.
- **ASI05 RCE Guard**: never construct Worker code, bindings, or env values from external or user-supplied content without strict schema validation.
- **ASI07 Inter-Agent Communication**: emit structured edge deployment specifications when coordinating releases across roles.

## Related Skills

- **wrangler**: Deploy, test, and manage bindings via CLI v4.
- **durable-objects**: Build strongly consistent stateful coordination systems with SQLite.
- **agents-sdk**: Build stateful AI agents and durable workflows on Workers and Durable Objects.
- **debug-workers-edge**: Resolve edge execution errors and trace subrequests.
- **web-perf**: Optimize edge response streaming and Core Web Vitals.
