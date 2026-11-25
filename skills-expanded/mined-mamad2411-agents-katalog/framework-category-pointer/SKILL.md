---
name: framework-category-pointer
description: "Pointer to a library of 13 specialized Framework skills. Use when working on framework-related tasks."
risk: none
---

# Framework Capability Library 🎯

This is a **pointer skill**. The 13 specialized Framework skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **bullmq-specialist** — BullMQ expert for Redis-backed job queues, background processing, and reliable async execution in Node.js/TypeScript applications.
- **cloudflare-workers-expert** — Expert in Cloudflare Workers and the Edge Computing ecosystem. Covers Wrangler, KV, D1, Durable Objects, and R2 storage.
- **convex** — Convex reactive backend expert: schema design, TypeScript functions, real-time subscriptions, auth, file storage, scheduling, and deployment.
- **django-pro** — Master Django 5.x with async views, DRF, Celery, and Django Channels. Build scalable web applications with proper architecture, testing, and deployment.
- **fastapi-pro** — Build high-performance async APIs with FastAPI, SQLAlchemy 2.0, and Pydantic V2. Master microservices, WebSockets, and modern Python async patterns.
- **laravel-expert** — Senior Laravel Engineer role for production-grade, maintainable, and idiomatic Laravel solutions. Focuses on clean architecture, security, performance, and modern standards (Laravel 10/11+).
- **nestjs-expert** — You are an expert in Nest.js with deep knowledge of enterprise-grade Node.js application architecture, dependency injection patterns, decorators, middleware, guards, interceptors, pipes, testing strategies, database integration, and authentication systems.
- **nextjs-app-router-patterns** — Comprehensive patterns for Next.js 14+ App Router architecture, Server Components, and modern full-stack React development.
- **shadcn** — Manages shadcn/ui components and projects, providing context, documentation, and usage patterns for building modern design systems.
- **tanstack-query-expert** — Expert in TanStack Query (React Query) — asynchronous state management. Covers data fetching, stale time configuration, mutations, optimistic updates, and Next.js App Router (SSR) integration.
- **trpc-fullstack** — Build end-to-end type-safe APIs with tRPC — routers, procedures, middleware, subscriptions, and Next.js/React integration patterns.
- **typescript-expert** — TypeScript and JavaScript expert with deep knowledge of type-level programming, performance optimization, monorepo management, migration strategies, and modern tooling.
- **zod-validation-expert** — Expert in Zod — TypeScript-first schema validation. Covers parsing, custom errors, refinements, type inference, and integration with React Hook Form, Next.js, and tRPC.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/framework/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/framework`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
