---
name: nestjs-config
description: NestJS configuration and environment management best practices. Use when configuring a NestJS app — ConfigModule, environment variables, typed config, or env validation. Triggers on ConfigModule, ConfigService, process.env, registerAs, or .env handling.
license: MIT
metadata:
  author: nestjs
  version: "1.0.0"
---

# NestJS Configuration

Best practices for configuring a NestJS application with `@nestjs/config` (v10/v11),
based on the official documentation (https://docs.nestjs.com/techniques/configuration).
Each rule pairs an incorrect example with the official correct pattern. Priorities run
from security and fail-fast correctness (CRITICAL) down to ergonomics and performance.

## When to Apply

Reference these guidelines when:
- Registering `ConfigModule.forRoot()` in the root/app module
- Reading environment variables anywhere in the app (services, providers, `main.ts`)
- Validating environment at boot with Joi or class-validator
- Grouping related config with `registerAs()` namespaces and typed access
- Handling secrets, `.env` files, and `.env.example`
- Reviewing or refactoring how a NestJS app reads configuration

## Rules

| Impact | Rule | Summary |
|--------|------|---------|
| CRITICAL | `no-secrets-in-repo` | Keep secrets in env/secret manager; commit only `.env.example` |
| CRITICAL | `validate-env-schema` | Validate env at boot so misconfig fails fast |
| HIGH | `global-config-module` | `ConfigModule.forRoot({ isGlobal: true })` once, at the root |
| HIGH | `configservice-over-process-env` | Inject `ConfigService`; don't read `process.env` scattered everywhere |
| MEDIUM | `namespaced-typed-config` | `registerAs()` namespaces + typed access for grouped config |
| MEDIUM | `type-safe-get` | Type `get<T>()` / use `infer: true` to avoid `undefined` surprises |
| LOW | `cache-config` | `cache: true` for performance; mind env-file load order |

## How to Use

Read the individual rule file for the explanation and before/after example:

```
rules/no-secrets-in-repo.md
rules/validate-env-schema.md
rules/global-config-module.md
rules/configservice-over-process-env.md
rules/namespaced-typed-config.md
rules/type-safe-get.md
rules/cache-config.md
```

Each rule file contains:
- A short explanation of why it matters, tied to the official docs
- An **Incorrect** example (the antipattern)
- A **Correct** example (the official pattern)

All examples target `@nestjs/config` for NestJS v10/v11 and avoid deprecated APIs.
