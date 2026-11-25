---
name: nestjs-modules-di
description: NestJS module organization and dependency injection best practices. Use when writing or reviewing NestJS modules, providers, or DI wiring. Triggers on @Module, @Injectable, provider registration, injection scopes, dynamic modules, or circular dependencies.
license: MIT
metadata:
  author: nestjs
  version: "1.0.0"
---

# NestJS Modules & Dependency Injection

Best-practices reference for organizing NestJS applications into encapsulated feature modules and wiring providers through the IoC container correctly. Covers module boundaries, provider visibility, dynamic modules, injection scopes, custom provider tokens, and circular dependencies.

## When to Apply

- Designing or reviewing `@Module` structure and feature boundaries
- Registering providers and deciding what to `export`
- Building configurable libraries with `forRoot`/`forRootAsync`
- Choosing an injection scope (singleton vs REQUEST vs TRANSIENT)
- Wiring custom providers (`useClass`/`useValue`/`useFactory`) and injection tokens
- Resolving or avoiding circular dependencies
- Deciding whether a module should be `@Global()`

## Rules

- `feature-module-boundaries` - one module per feature/domain; keep providers encapsulated
- `export-shared-providers` - only providers listed in `exports` are visible to importing modules
- `dynamic-modules-forroot` - configure reusable modules via `forRoot`/`forRootAsync` returning `DynamicModule`
- `injection-scopes-default-singleton` - prefer default singleton scope; REQUEST scope bubbles up and hurts performance
- `custom-provider-tokens` - use `useClass`/`useValue`/`useFactory` with injection tokens and interfaces
- `constructor-injection` - prefer constructor injection over property injection
- `avoid-circular-dependencies` - restructure first; use `forwardRef` only as a last resort
- `global-module-sparingly` - reserve `@Global()` for truly cross-cutting modules (config, logger)

## How to Use

Read individual rule files in `rules/` for explanation + incorrect/correct examples.
