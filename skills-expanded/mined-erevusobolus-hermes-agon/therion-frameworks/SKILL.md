---
name: therion-frameworks
description: "THERION Frameworks Domain - Next.js, Vue, Angular, SolidJS, Astro, Flutter, React Native/Expo, tRPC, Drizzle, Turborepo, monorepos"
version: 1.0.0
author: EREVUS Systems
license: AGPL-3.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [therion, frameworks, nextjs, vue, angular, solid, flutter, expo, mobile, trpc, drizzle, turborepo, monorepo, dart, jsx, tsx]
    homepage: https://erevus.space/projects/therion-protocol/
    related_skills: [therion-core, therion-delegator, therion-frontend, therion-backend, therion-support, therion-devops-cloud]
    hermes_integration:
      tools: [terminal, file, web, search, memory, session_search, skills, todo, cronjob, delegation]
      memory_tiers:
        - session: "Volatile - active framework configs, build errors, package versions"
        - project: "Persistent in MEMORY.md - project stack decisions, porting patterns, monorepo structure"
        - user: "Persistent - preferred tooling (npm/yarn/pnpm/bun), state management tastes, testing frameworks"
      mcp_servers:
        - name: npm-registry
          description: "Package lookup, version checks, dependency resolution"
        - name: framework-docs
          description: "Official docs scraping for Next.js, Vue, Angular, Solid, Astro, Flutter, Expo"
      cron_templates:
        - name: dep-update-check
          description: "Weekly dependency version check for monorepo packages"
          schedule: "0 9 * * 1"
      delegation_patterns:
        - pattern: framework-migration
          description: "Seq: therion-frameworks (source analysis) -> therion-frameworks (target scaffolding) -> therion-support (testing) -> therion-devops-cloud (deploy)"
        - pattern: fullstack-scaffold
          description: "Par: therion-frameworks (frontend) + therion-backend (API/db)"
      vision_use_cases:
        - "UI screenshot -> component code generation (React/JSX/TSX)"
        - "Design mockup -> responsive layout structure"
        - "Mobile app screenshot -> Flutter/Expo widget tree mapping"
---
# THERION Frameworks Domain (v1.0 - Hermes Native)

> **8 specialists. Every framework. Zero boilerplate.**

## Purpose

This domain covers all major frontend frameworks, mobile frameworks, and meta-framework tooling used in modern web and app development. When a user requests work involving any of the covered frameworks, load this skill and execute with the appropriate specialist mindset.

## Specialists

### THERION_NEXTJS_SPECIALIST
- **Primary**: Next.js 14+ (App Router, Server Components, Server Actions, Route Handlers)
- **Secondary**: React 18/19, RSC, Streaming SSR, ISR, Static Export, Middleware, Edge Runtime
- **Tools**: Pages Router (legacy), next/image, next/font, next/link, next/navigation, next.config, Turbopack, `next build` optimization
- **State**: Zustand, Jotai, TanStack Query, Context API, useOptimistic, useFormStatus
- **Auth**: NextAuth.js/Auth.js, Clerk, Lucia, supabase-auth
- **Deploy**: Vercel, Docker self-host, Node.js server, `output: "standalone"`
- **i18n**: next-intl, next-i18next

### THERION_VUE_SPECIALIST
- **Primary**: Vue 3 (Composition API, `<script setup>`, SFCs)
- **Ecosystem**: Nuxt 3, Pinia (state), Vue Router, Vite, Vitest, Nuxt Content, Nuxt DevTools
- **Meta-frameworks**: Nuxt with SSR, SSG, ISR, Hybrid rendering, Nitro server engine
- **Reactiveness**: ref, reactive, computed, watch, watchEffect, shallowRef, custom refs
- **Composables**: useFetch, useAsyncData, useState, useHead, custom composable patterns
- **Tooling**: Vite, unplugin-vue-components, unplugin-auto-import, vue-tsc
- **Styling**: UnoCSS, Tailwind CSS with Nuxt, SCSS, CSS Modules
- **Deploy**: Vercel (nuxt build), Netlify, Cloudflare Pages, Node server
- **i18n**: nuxt-i18n, vue-i18n

### THERION_ANGULAR_SPECIALIST
- **Primary**: Angular 17+ (Standalone components, Signals, control flow `@if/@for/@defer`)
- **Architecture**: Modules (NgModule) vs Standalone, lazy loading, route guards, resolvers, interceptors
- **State**: Signals (computed, effect, input, output, model), NgRx (Component Store, SignalStore, Store), NGXS
- **Forms**: Reactive Forms, Template-driven Forms, typed forms (Angular 14+)
- **SSR**: Angular Universal, Angular SSR (17+), Hydration, Deferrable Views
- **Tooling**: Angular CLI, esbuild builder, Angular DevTools, eslint + prettier
- **Testing**: Jasmine + Karma, Jest, Cypress component testing
- **Styling**: Angular CDK, Angular Material, PrimeNG, Tailwind CSS
- **RxJS**: Observable, Subject, BehaviorSubject, pipe operators, toSignal, toObservable

### THERION_SOLID_SPECIALIST
- **Primary**: SolidJS 1.x (Signals, JSX without VDOM, fine-grained reactivity)
- **Primitives**: createSignal, createEffect, createMemo, createResource, createStore, createContext
- **Flow**: Show, For, Index, Switch/Match, ErrorBoundary, Suspense, lazy
- **Ecosystem**: Solid Router, Solid Start (meta-framework), SolidUI, Hope UI, Kobalte
- **SSR**: Solid Start with Vinxi, streaming, islands architecture
- **Tooling**: Vite + solid plugin, TypeScript, eslint-plugin-solid
- **Integration**: tRPC client, TanStack Query (solid-query), tailwindcss
- **Porting**: React-to-Solid conversion patterns and pitfalls (no VDOM, effects vs useEffects)

### THERION_ASTRO_SPECIALIST
- **Primary**: Astro 4+ (Content Collections, View Transitions, Server Islands, Astro Actions)
- **Architecture**: Islands architecture, zero-JS by default, partial hydration
- **Frameworks**: Astro + React, + Vue, + Svelte, + Solid, + Lit, + Preact (multi-framework)
- **Content**: MDX, Content Collections, Astro DB, Astro Studio, Starlight (documentation)
- **Routing**: File-based, dynamic routes, endpoint routes, redirects, rewrites
- **Tooling**: `astro build`, `astro check` (TypeScript), integrations, adapters
- **Deploy**: Adapt to Vercel, Netlify, Cloudflare, Deno, Node, S3/static
- **Images**: `@astrojs/image`, built-in image optimization, Picture component
- **i18n**: astro-i18n, built-in i18n routing

### THERION_FLUTTER_SPECIALIST
- **Primary**: Flutter 3.x (Dart, Widgets, Material 3, Cupertino)
- **State**: Riverpod, Bloc/Cubit, Provider, GetX, `setState`, ValueNotifier, InheritedWidget
- **UI**: CustomPainter, AnimationController, Hero, TweenAnimationBuilder, Implicit animations
- **Navigation**: GoRouter, Navigator 2.0, auto_route, Beamer
- **Data**: flutter_riverpod + dio + retrofit, drift (SQLite), firebase, supabase-dart, graphql_flutter
- **Architecture**: Clean Architecture layers, Repository pattern, BLoC pattern, Riverpod + code generation
- **Build**: Android (Kotlin/Groovy), iOS (Swift), Web (dart2js), Desktop (Windows/macOS/Linux)
- **Tooling**: Dart devtools, flutter analyze, flutter test, golden tests, integration tests
- **CI**: Codemagic, GitHub Actions for Flutter, Fastlane
- **Packaging**: App Bundles (AAB), iOS IPA, `flutter build` profiles (-debug, -profile, -release)
- **Platform channels**: MethodChannel, Pigeon, FFI, dart:ffi

### THERION_MOBILE_SPECIALIST
- **Primary**: React Native / Expo SDK 50+ (Expo Router, EAS Build, dev-client)
- **Framework**: React Native 0.73+, Hermes engine, New Architecture (Fabric + TurboModules), Bridgeless
- **Expo**: expo-dev-client, expo-updates, EAS Build, EAS Submit, EAS Update, config plugins
- **Navigation**: Expo Router (file-based), React Navigation (native stack, tabs, drawer, deep linking)
- **State**: TanStack Query (React Query), Zustand, Jotai, Redux Toolkit, MMKV
- **UI**: NativeWind (Tailwind for RN), React Native Reanimated, Gesture Handler, Skia
- **Data**: Expo SQLite, WatermelonDB, Realm, Firestore, Supabase Realtime
- **Native**: Expo Modules API, expo-dev-client, custom native modules, expo-modules-core
- **Build**: EAS Build for iOS/Android, app config (app.json, app.config.js), iOS signing, Android keystores
- **Publishing**: App Store Connect, Google Play Console, EAS Submit, expo publish (Updates)
- **Maps**: expo-maps, react-native-maps, MapLibre
- **Push**: expo-notifications, Firebase Cloud Messaging, APNs
- **Over-the-air**: EAS Update, expo-updates, bundled assets
- **Monorepo**: Expo in Turborepo/Nx, shared packages, native module isolation
- **Testing**: detox (E2E), jest + @testing-library/react-native, Maestro

### THERION_FULLSTACK_ENGINEER
- **Primary**: Full-stack TypeScript with tRPC, Drizzle ORM, Turborepo monorepos
- **tRPC**:
  - tRPC v10/11 with React Query, SSR, SSG, server components (next-safe-action / server action integration)
  - Procedures: query, mutation, subscription, middleware (auth, logging, rate-limit)
  - Context: async request context, streaming, WebSockets
  - Adapters: Next.js (pages + app router), Express, Fastify, AWS Lambda, Vercel Edge
  - Validation: Zod schemas (input/output), inferred types end-to-end
- **Drizzle ORM**:
  - Drizzle Kit (migrations, push, introspect, studio)
  - Schema: relations (one-to-many, many-to-many), indexes, enums, composite keys
  - Queries: relational query builder, prepared statements, raw SQL, batch
  - Drivers: PostgreSQL (pg, @vercel/postgres, @neondatabase/serverless), SQLite (better-sqlite3, bun:sqlite), MySQL (mysql2)
  - Migrations: `drizzle-kit generate`, `push`, `migrate`, seeds, snapshots
  - Drizzle Studio: visual DB inspection, data editing
- **Turborepo / Monorepos**:
  - Turborepo v2: task orchestration, caching (remote + local), parallel execution, dependency graph
  - pnpm workspaces, npm workspaces, bun workspaces
  - Package conventions: `@repo/*` naming, shared configs (TypeScript, ESLint, Prettier, Tailwind)
  - Shared packages: `@repo/ui`, `@repo/db`, `@repo/auth`, `@repo/validators`
  - Task pipeline: build -> lint -> test -> typecheck order, dependsOn, outputs, inputs
  - Remote caching: Vercel Remote Caching, S3-compatible, local filesystem
  - Versioning: Changesets, semantic-release, conventional commits
  - Nx integration (hybrid: Nx for project graph, Turborepo for caching)
- **Stack integration patterns**:
  - Next.js + tRPC + Drizzle + Turborepo (the "T3 Turbo" stack)
  - Expo + tRPC + Drizzle shared types (mobile + web)
  - Astro + tRPC (API routes) + Drizzle (content + auth)
  - Solid Start + tRPC + Drizzle
  - Nuxt + tRPC (server routes) + Drizzle

## Framework cross-cutting concerns

### State management by framework
| Framework | Primary | Secondary |
|-----------|---------|-----------|
| Next.js/React | Zustand, TanStack Query | Jotai, Context |
| Vue/Nuxt | Pinia | provide/inject |
| Angular | Signals, NgRx SignalStore | NgRx Store |
| SolidJS | createSignal + createStore | - |
| Astro | server state (Astro DB) | framework-integrated |
| Flutter | Riverpod | Bloc, Provider |
| React Native | Zustand, TanStack Query | Redux Toolkit |

### Type safety patterns
- Always prefer `infer` types from tRPC + Zod for end-to-end safety
- Drizzle schema -> TypeScript types (automatic via `drizzle-kit`)
- Use `satisfies`, `as const`, `z.infer` for derived types
- Monorepo shared types: `@repo/validators` for Zod, `@repo/db` for Drizzle types
- React Query + tRPC: full type inference from server to client, no manual API types

### Build tooling matrix
| Framework | Bundler | Dev server | Build command |
|-----------|---------|------------|---------------|
| Next.js | Turbopack / Webpack | `next dev` | `next build` |
| Nuxt/Vue | Vite (default) | `nuxt dev` | `nuxt build` |
| Angular | esbuild (17+) | `ng serve` | `ng build` |
| SolidJS | Vite + solid | `solid-start dev` | `solid-start build` |
| Astro | Vite + astro | `astro dev` | `astro build` |
| Flutter | dart2js/Native | `flutter run` | `flutter build` |
| Expo/RN | Metro bundler | `expo start` | `eas build` |
| Turborepo | Nx/Vite/Webpack | `turbo dev` | `turbo build` |

### Package manager preferences
- **pnpm** — recommended for monorepos (strict isolation, workspace protocol, speed)
- **bun** — fastest installs, works with Turborepo, native TypeScript
- **npm** — standard, workspaces supported
- **yarn** — Berry/PnP with workspaces, less common

## Common patterns

### Project scaffolding (new project)
1. Ask: framework + state management + styling + package manager + monorepo yes/no
2. Generate: template or `create-*` CLI
3. Add: ESLint, Prettier, TypeScript strict, git hooks (husky + lint-staged)
4. If monorepo: initialize Turborepo + pnpm workspaces + shared configs
5. If tRPC: set up server adapter + client provider + Zod validation
6. If Drizzle: schema setup + first migration + seed script

### Migration patterns (framework to framework)
1. Analyze source: routing, state, data fetching, styling, auth
2. Map concepts: e.g. Next.js Pages Router -> App Router, Vue Options -> Composition, Angular NgRx -> Signals
3. Scaffold target: parallel project, incremental adoption
4. Port routes -> components -> state -> data layer -> auth
5. Validate: equivalent behavior, performance, bundle size

### Performance checklist
- Bundle analysis: `next build --analyze`, `nuxt analyze`, `ng build --stats-json`
- LCP optimization: image optimization, streaming SSR, deferred loading
- Hydration: Astro islands, React Server Components, Angular Deferrable Views, Solid fine-grained
- Bundle splitting: dynamic imports, route-level code splitting, component lazy loading
- Mobile: Hermes engine profiling, reduce bridge traffic (Fabric), native driver for animations

## Activation

This skill activates when:
1. User loads `therion-frameworks` directly
2. `therion-delegator` routes to frameworks domain (keywords: nextjs, vue, angular, solid, flutter, expo, mobile, trpc, drizzle, turborepo, monorepo, dart, jsx, tsx)
3. User mentions any of the 8 specialist names explicitly
4. Task involves multi-framework comparison, migration, or integration

**DEUS VULT.**

## References
- `references/framework-comparisons.md` — Detailed framework comparison tables
- `references/migration-guides.md` — Step-by-step migration patterns between frameworks
- `references/t3-turbo-template.md` — Full-stack T3 Turbo architecture reference
