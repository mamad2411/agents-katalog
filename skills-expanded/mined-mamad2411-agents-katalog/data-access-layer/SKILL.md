---
name: data-access-layer
description: Use when querying or mutating the database from the app — wrap Drizzle in server-only, tenant-scoped functions instead of calling the ORM from components, so every read/write is typed, testable, and isolation-safe.
---

# Data Access Layer

## Overview

Don't scatter ORM calls across components and route handlers. Put every query behind a **server-only data-access layer (DAL)**: small typed functions that take an explicit `orgId` and never return another tenant's rows. The rest of the app calls `getProjects(orgId)`, not `db.select(...)`. This centralizes tenant scoping, caching, and the place you write tests.

## When to use

- Any read or write to the database.
- You catch yourself importing `db` into a React component.
- You want one place to enforce "every query is scoped to the current org".

## The pattern

```ts
// src/server/services/projects.ts
import "server-only";
import { and, eq, desc } from "drizzle-orm";
import { db } from "@/server/db/client";
import { projects } from "@/server/db/schema";

export async function listProjects(orgId: string) {
  return db.select().from(projects)
    .where(eq(projects.orgId, orgId))
    .orderBy(desc(projects.createdAt));
}

export async function getProject(orgId: string, id: string) {
  const [row] = await db.select().from(projects)
    .where(and(eq(projects.id, id), eq(projects.orgId, orgId)))  // scope by BOTH
    .limit(1);
  return row ?? null;
}

export async function createProject(orgId: string, input: { name: string }) {
  const [row] = await db.insert(projects).values({ orgId, ...input }).returning();
  return row;
}
```

Callers (server components, actions, route handlers) pass the `orgId` resolved from the session — they never invent it.

## Why a DAL

- **Isolation by construction.** Lookups filter on `id AND org_id`, so a guessed UUID from another tenant returns `null`, not data.
- **Typed end-to-end.** `returning()` gives you the row type for free.
- **Testable.** Mock or seed the DB and test functions directly, no HTTP needed.
- **Cacheable.** Wrap reads in `cache()` / `unstable_cache` in one spot.

## Pitfalls

- **Calling `db` from components** — couples UI to the schema and risks shipping queries to the client. Always go through the DAL.
- **Lookups by `id` only** — `where(eq(projects.id, id))` without `orgId` is a cross-tenant read. Scope by both.
- **Returning raw rows with secrets** — strip sensitive columns (tokens, hashes) in the DAL.
- **N+1 in loops** — batch with `inArray` or a join instead of awaiting per item.
- **Forgetting `server-only`** — without it a refactor can pull DB code into the client bundle.

## Hand-off

A typed, tenant-safe query layer. `api-routes-and-validation` and Server Actions call it after validating input; `authorization-rbac` gates which functions a role may invoke.
