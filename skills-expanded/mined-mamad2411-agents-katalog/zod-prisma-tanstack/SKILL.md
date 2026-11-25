---
name: zod-prisma-tanstack
description: Full-stack data-layer conventions for projects that use Prisma + Zod + TanStack Query, server actions, schema validation, query factories, hooks, fetchers, API routes, and TanStack Start Server Functions. Framework-agnostic; works with Next.js (App or Pages Router), TanStack Start (REST or RPC), Remix, Hono, Express. Use when creating domain features, adding endpoints, modifying the Prisma schema, writing hooks/queries, or reviewing data-layer code, or when bootstrapping these conventions in a project that does not yet follow them.
---

# Prisma + Zod + TanStack Query Stack

Use this skill when writing, reviewing, or modifying code in the data layer of a TypeScript app that uses **Prisma**, **Zod**, and **TanStack Query**: server-side data access, schema validation, query factories, hooks, API routes, or Prisma models.

TRIGGER when: creating new domain features, adding API endpoints, writing hooks/queries, modifying the Prisma schema, adding Zod validation, reviewing data-layer code, or the user asks to "set up the data layer / wire Prisma + Zod + React Query."

> **Stack assumed.** Prisma v5+, Zod v4 (v3 noted as legacy where APIs diverge), TanStack Query v5, TypeScript with `strict` + `noUncheckedIndexedAccess`. Framework-agnostic, Next.js App/Pages Router, TanStack Start (REST or RPC), Remix, Hono, and Express are all supported via the four §7 flavors. Database-agnostic except where called out (the `aggregateRaw`/`$geoNear` patterns in §1 are MongoDB-only; substitute `$queryRaw` + a SQL full-text index or PostGIS for SQL databases). Expanded prerequisites and bootstrap steps in §Prerequisites and §0.

> **Notation.** Wherever a path appears as `<server>/actions/`, `<types>/`, `<schemas>/`, `<queries>/`, `<hooks>/`, `<utils>/`, or `<constants>/`, treat it as a placeholder. Resolve to the project's existing structure (`src/server`, `app/lib`, `~/server`, `@/lib`, etc.). The **shape** of each layer is what matters; exact paths can vary.

> **Precedence.** These rules apply only where they don't contradict the project's own enforced rules, ESLint / Biome / Prettier configs, `tsconfig`, `CLAUDE.md` / `AGENTS.md`, contributing guides, or framework conventions. If a project rule conflicts, the project rule wins; defer to it and (if it makes sense) note the deviation in your PR description.

---

## Prerequisites

This skill assumes the project has, or is willing to add:

- **Prisma** v5+ (any supported database, Postgres, MySQL, SQLite, MongoDB, etc.). The `aggregateRaw` and `$geoNear` examples in §1 are MongoDB-only; substitute the equivalent raw-query API for other databases.
- **Zod v4** (preferred). Zod v3 is noted in a single footnote where APIs diverge (notably `z.enum()` vs `z.nativeEnum()` for enum-like objects), treat v3 as legacy. **Pin a version** in your project; mixing v3 and v4 is unsupported.
- **TanStack Query v5** (`@tanstack/react-query`), the conventions rely on `queryOptions()` / `infiniteQueryOptions()`, `useSuspenseQuery`, and the v5 cache-key model.
- **TypeScript** with `strict` and `noUncheckedIndexedAccess` recommended.
- A full-stack React framework that exposes some form of typed server entry point. §7 shows concrete examples for:
  - **Next.js App Router** (`<app>/api/**/route.ts`)
  - **TanStack Start** API routes (`createAPIFileRoute`) **and** Server Functions (`createServerFn`), the latter collapses the fetcher + REST-route layers into typed RPC.
  - **Next.js Pages Router** (`<pages>/api/*.ts`), legacy / maintenance mode.
  - The same shape adapts to Remix actions/loaders, Hono, Express, etc.
- A path-alias setup (`tsconfig` `paths` plus the bundler equivalent) so imports are root-relative, not `../../..`.

If any of these are missing, install the missing piece first or skip the affected section.

---

## 0. Bootstrap (use when the project lacks these conventions)

If the target project already follows this layering, skip and apply the rest in-place. Otherwise:

**Step 1, Pick locations** (record in `CLAUDE.md` / `AGENTS.md` / contributing guide):

- `<server>/actions/`, Prisma access, one file per domain.
- `<server>/db.ts`, exports the singleton `prisma` client.
- `<server>/functions/` *(TanStack Start, RPC flow only)*, `createServerFn` definitions, one file per domain.
- `<types>/`, shared TS types and `Prisma.GetPayload<...>` aliases.
- `<schemas>/`, Zod schemas, one file per domain plus a `common.ts`.
- `<queries>/`, TanStack Query options + keys, one file per domain.
- `<hooks>/`, domain hooks (`useArticles`, etc.).
- `<utils>/fetcher.ts` *(REST flow only)*, typed fetchers wrapping `fetch`. Skip if the project uses TanStack Start Server Functions exclusively.
- `<constants>/apiEndpoints.ts` *(REST flow only)*, single source of truth for API URLs. Skip if the project uses Server Functions exclusively.

**Step 2, Add the singleton Prisma client** (`<server>/db.ts`). Use the standard "global cache in dev, fresh in prod" pattern from the Prisma docs. Never `new PrismaClient()` ad-hoc.

**Step 3, Add `<utils>/fetcher.ts`** with three typed fetchers (§5). They wrap `fetch` and centralize error handling.

**Step 4, Add `<constants>/apiEndpoints.ts`** with a single nested `API_ENDPOINTS` object (§8). All URLs flow through this file.

**Step 5, Add `<types>/common.ts`** with the shared pagination/search prop interfaces (§2).

**Step 6, Add `<schemas>/common.ts`** with shared Zod primitives the project needs (color, image, money, etc.), see §3.

**Step 7, Pick the first domain and walk through the §9 checklist end-to-end.** Use it as the reference for subsequent domains.

Once these are in place, the rest of this document is the working spec.

---

## Full-Stack Data Flow

**Default flow (REST-style, works with any framework):**

```
Component (UI)
  → Hook                       (<hooks>/useX.ts)
    → Query Options + Keys     (<queries>/x.ts, `xKeys` + standalone `*Options` fns)
      → Fetcher                (<utils>/fetcher.ts, typed wrappers over `fetch`)
        → API Route            (Next App/Pages Router, TanStack Start `createAPIFileRoute`, Hono, etc.)
          → Server Action      (<server>/actions/x.ts, plain async Prisma wrappers)
            → Prisma → Database
```

**RPC-shortcut flow (TanStack Start Server Functions, Next.js Server Actions when used as RPC):**

```
Component (UI)
  → Hook                       (<hooks>/useX.ts)
    → Query Options + Keys     (<queries>/x.ts)
      → Server Function        (`createServerFn` / `"use server"` action, replaces fetcher + route)
        → Server Action        (<server>/actions/x.ts)
          → Prisma → Database
```

Every new domain feature must follow one of these chains. Never skip layers (e.g., do not call Prisma directly from a route handler or server function, and never call raw `fetch` from a component).

---

## 1. Server Actions (`<server>/actions/*.ts`)

> "Server actions" here means **plain async functions that wrap Prisma**, not Next.js `"use server"` Server Actions. The directive must **not** be added to these files.

### File Convention

One file per domain. Example surface:

```typescript
// <server>/actions/article.ts
import { type Prisma } from "@prisma/client";
import { prisma } from "server/db";
import { type FindManyProps, type SearchManyProps } from "types/common";
import { type ArticleFull } from "types/article";

type FindManyArticlesProps = FindManyProps<Prisma.ArticleWhereInput>;
```

### Standard Exports

| Export | Purpose |
|--------|---------|
| `IncludeXRelations` | `Prisma.XInclude` object defining related data to load |
| `findOneX` | `findFirst` with include |
| `findManyX` | `findMany` with pagination (`take`, `skip`) |
| `searchManyX` | Raw aggregation for full-text / geo / complex queries (DB-specific) |
| `countX` | Simple `.count()` wrapper |

### Include Relations Pattern

```typescript
export const IncludeArticleRelations: Prisma.ArticleInclude = {
  author: true,
  tags: true,
  comments: true
};
```

Nested relations:

```typescript
export const IncludeArticleDetailRelations: Prisma.ArticleInclude = {
  author: true,
  tags: true,
  comments: {
    orderBy: { createdAt: "asc" },
    include: { user: true }
  },
  category: { include: { parent: true } }
};
```

### findOne / findMany

```typescript
export async function findOneArticle({ searchQuery }: Pick<FindManyArticlesProps, "searchQuery">) {
  const article = await prisma.article.findFirst({
    ...(searchQuery && { where: searchQuery }),
    include: IncludeArticleRelations
  });
  return article;
}

export async function findManyArticles({ searchQuery, take = 10, page = 0 }: FindManyArticlesProps) {
  const articles = await prisma.article.findMany({
    where: searchQuery,
    take,
    skip: take * page,
    include: IncludeArticleRelations
  });
  return articles;
}
```

### searchMany with raw aggregation (MongoDB example, adapt per database)

Use raw aggregation for full-text search, geospatial queries, or complex pipelines that the typed Prisma API can't express. The MongoDB pipeline below is illustrative; for SQL databases use `$queryRaw` / a full-text index / a search engine instead.

```typescript
export async function searchManyArticles({
  searchText,
  take = 10,
  page = 0,
  language
}: SearchManyProps): Promise<{ articles: ArticleFull[]; totalArticles: number }> {
  let articles: ArticleFull[] = [];
  let totalArticles = 0;

  const rawData = await prisma.article.aggregateRaw({
    pipeline: [
      // Full-text match
      { $match: { $text: { $search: `"${searchText}"`, $language: language } } },
      {
        $facet: {
          data: [
            { $skip: take * page },
            { $limit: take },
            // Lookups for relations not satisfied by the aggregation alone
            { $lookup: { from: "Tag", localField: "tagIDs", foreignField: "_id", as: "tags" } },
            { $sort: { updatedAt: -1 } },
            // ID conversion: Mongo `_id` ObjectId → Prisma `id` string
            { $addFields: { id: { $toString: "$_id" }, updatedAt: { $toString: "$updatedAt" } } },
            { $project: { _id: 0 } }
          ],
          total: [{ $count: "totalItems" }]
        }
      }
    ]
  });

  // Safe extraction from raw aggregation
  if (Array.isArray(rawData)) {
    const { data, total } = (rawData as unknown as { data: ArticleFull[]; total: { totalItems: number }[] }[]).at(0) ?? {
      data: [],
      total: 0
    };
    if (Array.isArray(data)) articles = data;
    if (Array.isArray(total)) {
      const totalResults = total.at(0) ?? {};
      if ("totalItems" in totalResults && typeof totalResults.totalItems === "number") {
        totalArticles = totalResults.totalItems;
      }
    }
  }

  return { articles, totalArticles };
}
```

### count

```typescript
export async function countArticles({ searchQuery }: Pick<FindManyArticlesProps, "searchQuery">) {
  const total = await prisma.article.count({
    ...(searchQuery && { where: searchQuery })
  });
  return total;
}
```

### Geospatial Query (MongoDB-only)

```typescript
// Inside the MongoDB aggregation pipeline, before $facet:
{
  $geoNear: {
    near: { type: "Point", coordinates },
    distanceField: "dist.calculated",
    includeLocs: "dist.location",
    maxDistance: distance,
    spherical: true,
    key: "geometry"
  }
}
```

For PostGIS / MySQL spatial / SQLite R*Tree, use the equivalent SQL via `$queryRaw`. Do not try to force a Mongo pipeline shape onto SQL.

### Rules

- Always import `prisma` from a singleton (`server/db`), never `new PrismaClient()` in a domain file.
- Always import Prisma types: `import { type Prisma } from "@prisma/client"`.
- For `orderBy`, plain `"asc"` / `"desc"` literals are fine, modern Prisma types them as a string-literal union and `Prisma.SortOrder` resolves to the same shape. Pick one form and stay consistent within the file. (Note: `Prisma.SortOrder` is itself a generated TS `enum`. The components-hierarchy skill discourages authoring `enum`s, but consuming framework-generated ones is fine, that distinction matters.)
- Cast `aggregateRaw` results: `as unknown as T[]`, then extract safely (do not blindly trust the shape).
- Use `$facet: { data: [...], total: [...] }` for pagination in raw aggregations.
- For MongoDB: always `$addFields: { id: { $toString: "$_id" } }` and `$project: { _id: 0 }` so the shape matches Prisma's TS types.
- These are **plain async functions**, NOT Next.js `"use server"` actions. Do not add the directive.

---

## 2. Prisma Type Reuse (`<types>/*.ts`)

### GetPayload Pattern

```typescript
import { type Prisma } from "@prisma/client";

export type ArticleFull = Prisma.ArticleGetPayload<{
  include: {
    author: true;
    tags: true;
    comments: true;
  };
}>;
```

This infers the exact return type from the Include shape, keep it in sync with `IncludeXRelations`.

### Common Types (`<types>/common.ts`)

```typescript
export type DBCommonData = "id" | "createdAt" | "updatedAt";

// Helper: flatten a "translated text" record type into a plain string for update flows.
// Define your project's localized-text shape and substitute it here.
export type SimplifyTextProp<T> = {
  [K in keyof T]: T[K] extends LocalizedText | null ? string : T[K] extends LocalizedText ? string : T[K];
};

export interface PaginatedOptionsParams {
  page?: number;
  take?: number;
  allEntries?: boolean;
  private?: boolean;
  inactive?: boolean;
}

export interface FindManyProps<T = Record<string, string | boolean | null | number | object>>
  extends PaginatedOptionsParams {
  searchQuery: T;
}

export interface SearchManyProps extends PaginatedOptionsParams {
  searchText: string;
  language?: string; // optional, only relevant for multilingual projects
  userId?: string;
}

export interface GeoProps {
  coordinates: [number, number] | null;
  distance: number;
}
```

> Drop `language` / `SimplifyTextProp` if the project is single-language. Drop `GeoProps` if there are no geo features.

---

## 3. Zod Schemas (`<schemas>/*.ts`)

### File Convention

One file per domain. Three-schema pattern:

1. **Base schema**, validated Prisma model shape (minus system / relation-ID fields).
2. **Post schema**, wraps base for creation requests.
3. **Update schema**, flattened text + language selector for mutations *(only if the project is multilingual; otherwise the update schema is just `BaseSchema.partial()` or a hand-rolled subset)*.

### Shared Schemas (`<schemas>/common.ts`)

```typescript
import { z } from "zod";
// Import only the Prisma enums the project actually defines.
// Drop any of these primitives that the project doesn't need.

// ── Localized text (only for multilingual projects) ──
// Pick one language as the always-required default; mark the rest nullable.
export const Languages = z.object({
  en: z.string(),                   // example: English required
  es: z.string().nullable(),
  fr: z.string().nullable()
});
export const TextSchema = z.object({ text: Languages });

// ── Image ──
export const ImageSchema = z.object({
  imagesURLs: z.string().array(),
  main: z.boolean(),
  alt: z.string().nullable(),
  key: z.string()
});

// ── Color (hex) ──
export const ColorString = z.string().length(7).regex(/^#[0-9A-Fa-f]{6}$/);

// ── Money / pricing (example shape, adapt to your domain) ──
// export const PriceSchema: z.ZodType<Price> = z.object({ ... });

// ── Opening hours (example shape, adapt to your domain) ──
// export const OpeningHoursSchema = z.object({ ... });
```

### Complete Domain Schema Example

```typescript
// <schemas>/article.ts
import { type Article } from "@prisma/client";
import { z } from "zod";
import { type SimplifyTextProp, type DBCommonData } from "types/common";
import { ColorString, TextSchema } from "./common";

// Step 1: MinProps, strip system fields and relation IDs
export type ArticleMinProps = Omit<
  Article,
  DBCommonData | "authorId" | "tagIDs" | "categoryId"
>;

// Step 2: Base schema with `satisfies` for bidirectional Prisma↔Zod type safety
export const ArticleSchema = z.object({
  title: TextSchema,           // multilingual
  description: TextSchema,
  color: ColorString,
  active: z.boolean()
}) satisfies z.ZodType<ArticleMinProps>;

// Step 3: POST schema, wrap base in a named object
export const PostArticleParamsSchema = z.object({
  article: ArticleSchema
});
export type PostArticleParamsSchemaType = z.infer<typeof PostArticleParamsSchema>;

// Step 4: UPDATE schema, flatten translated text → string + add language selector
//          (multilingual projects only; otherwise use ArticleSchema.partial())
type ArticleSimplifiedProps = SimplifyTextProp<ArticleMinProps> & { language: string };

export const ArticleUpdateParamsSchema = ArticleSchema.omit({
  title: true,
  description: true
}).extend({
  title: z.string(),
  description: z.string(),
  language: z.string() // Zod 4: z.enum(YourLanguageEnum), Zod 3: z.nativeEnum(YourLanguageEnum)
}) satisfies z.ZodType<ArticleSimplifiedProps>;
export type ArticleUpdateParamsSchemaType = z.infer<typeof ArticleUpdateParamsSchema>;
```

### Rules

- Always use `satisfies z.ZodType<XMinProps>` for Prisma↔Zod bidirectional binding, TS will fail the build if Prisma and Zod drift apart.
- Use **`z.enum()`** for Prisma enums, never manual string unions.
  - **Zod 4:** `z.enum(YourPrismaEnum)`, the unified `enum` API accepts both string-literal arrays and TS-enum-like objects.
  - **Zod 3:** `z.nativeEnum(YourPrismaEnum)`, the `nativeEnum` form is required for object inputs; `z.enum()` only accepts string-literal arrays in v3.
- Use `z.coerce.number()` / `z.coerce.date()` / `z.coerce.string()` for type conversions from query strings or `FormData`.
- Multilingual create: nested `TextSchema` (`{ text: { ...langs } }`).
- Multilingual update: flat `z.string()` + `language` selector.
- `Omit<Model, DBCommonData | "...IDs">` to strip system / relation-ID fields. (For SQL projects, `*IDs` arrays are typically only Mongo many-to-many idioms; substitute the actual FK columns your schema uses.)
- POST schemas: wrap domain schema → `z.object({ article: ArticleSchema })`. Single-purpose, named.
- PUT schemas (multilingual): `.omit()` text fields, `.extend()` with flattened text + language. Single-language: `BaseSchema.partial()` or a hand-rolled subset.
- Infer types with `z.infer<typeof Schema>`, never manually duplicate the shape.

---

## 4. Query Options Functions (`<queries>/*.ts`)

### File Convention

One file per domain. Two exports:

1. **`xKeys`**, a frozen object that builds the cache-key hierarchy.
2. **One standalone `*Options` function per query**, each returns `queryOptions(...)` (or `infiniteQueryOptions(...)`). Call sites spread the result into `useQuery` so they can layer on per-call overrides (`select`, `throwOnError`, `enabled`, etc.).

This mirrors the canonical TanStack Query v5 shape:

```typescript
import { queryOptions } from "@tanstack/react-query";

function invoiceOptions(id: number) {
  return queryOptions({
    queryKey: ["invoice", id],
    queryFn: () => fetchInvoice(id)
  });
}

const invoiceQuery = useQuery({
  ...invoiceOptions(1),
  throwOnError: true,
  select: (invoice) => invoice.createdAt
});
```

### Key Builder Hierarchy

```
articleKeys.all              → ["articles"]                              ← broadest invalidation target
articleKeys.lists()          → ["articles", "list"]                      ← all paginated lists
articleKeys.list(params)     → ["articles", "list", params]              ← one paginated list
articleKeys.details()        → ["articles", "detail"]                    ← all details
articleKeys.detail(id)       → ["articles", "detail", id]                ← single item
articleKeys.searches()       → ["articles", "search"]                    ← all searches
articleKeys.search(params)   → ["articles", "search", params]            ← one search
```

Always compose from `articleKeys.all` so `invalidateQueries({ queryKey: articleKeys.all })` invalidates the whole domain. Use `as const` so the keys are readonly tuples, TanStack will infer narrower types and TS will catch accidental mutation.

### Complete Example

```typescript
// <queries>/article.ts
import {
  keepPreviousData,
  queryOptions,
  infiniteQueryOptions
} from "@tanstack/react-query";
import { API_ENDPOINTS } from "constants/apiEndpoints";
import {
  type GetArticleResponse,
  type GetArticlesResponse
} from "types/article";
import { type PaginatedOptionsParams } from "types/common";
import { getModelFetcher } from "utils/fetcher";

// Search params used by both the cache key and the options function.
export interface SearchArticleQueryProps extends PaginatedOptionsParams {
  searchText: string;
  filterOptions?: { authorId?: string; tag?: string };
}

// 1) Cache-key hierarchy ────────────────────────────────────────────────
export const articleKeys = {
  all: ["articles"] as const,
  lists: () => [...articleKeys.all, "list"] as const,
  list: (params: PaginatedOptionsParams) => [...articleKeys.lists(), params] as const,
  details: () => [...articleKeys.all, "detail"] as const,
  detail: (articleId: string) => [...articleKeys.details(), articleId] as const,
  searches: () => [...articleKeys.all, "search"] as const,
  search: (params: SearchArticleQueryProps) => [...articleKeys.searches(), params] as const
} as const;

// 2) Options functions ──────────────────────────────────────────────────
export function articleListOptions(params: PaginatedOptionsParams) {
  return queryOptions({
    queryKey: articleKeys.list(params),
    queryFn: () =>
      getModelFetcher<GetArticlesResponse>({
        url: API_ENDPOINTS.ARTICLES(),
        errorString: "Articles",
        queryParams: params
      }),
    placeholderData: keepPreviousData
  });
}

export function articleDetailOptions(articleId?: string | null) {
  return queryOptions({
    queryKey: articleKeys.detail(articleId ?? ""),
    queryFn: () =>
      getModelFetcher<GetArticleResponse>({
        url: API_ENDPOINTS.ARTICLE.SINGLE({ articleId }),
        errorString: "Article"
      }),
    enabled: !!articleId
  });
}

export function articleSearchOptions(params: SearchArticleQueryProps) {
  return queryOptions({
    queryKey: articleKeys.search(params),
    queryFn: () =>
      getModelFetcher<GetArticlesResponse>({
        url: API_ENDPOINTS.ARTICLES(),
        errorString: "Articles search",
        queryParams: { search: params.searchText, ...params.filterOptions, page: params.page, take: params.take }
      }),
    placeholderData: keepPreviousData
  });
}
```

### Call Sites (the override pattern)

Spread the options into `useQuery` and layer per-call concerns on top:

```typescript
const articleQuery = useQuery({
  ...articleDetailOptions(id),
  throwOnError: true,
  select: (response) => response.article // narrow / project the data
});

articleQuery.data; // typed as the projected shape
```

**Where do `staleTime` / `gcTime` / `retry` live?** Three valid layers, in order of preference:

1. **`QueryClient` defaults**, for app-wide policy (e.g., `staleTime: 60_000` for everything). Set once when constructing the client.
2. **The `*Options` function**, for **domain-wide** policy that differs from app defaults (e.g., articles are stable for 5 minutes, comments for 10 seconds). This is the natural place for "this resource has a known freshness window."
3. **The call site**, for **per-consumer** concerns: `select` (data projection), `throwOnError` (error-boundary integration), `refetchOnWindowFocus` overrides, or one-off `staleTime` boosts on a critical screen.

The earlier rule is: don't put **per-consumer** concerns (`select`, `throwOnError`) in the `*Options` function. **Domain-wide cache policy is fine there.** When in doubt, put it as high as it'll go.

### Infinite Query Pattern

```typescript
export function articleInfiniteSearchOptions(params: SearchArticleQueryProps) {
  const take = params.take ?? 10;
  return infiniteQueryOptions({
    queryKey: articleKeys.search(params),
    queryFn: ({ pageParam }) =>
      getModelFetcher<GetArticlesResponse>({
        url: API_ENDPOINTS.ARTICLES(),
        errorString: "Articles search",
        queryParams: { search: params.searchText, page: pageParam, take, ...params.filterOptions }
      }),
    initialPageParam: 0,
    getNextPageParam: (lastPage, _allPages, lastPageParam) =>
      lastPage.articles.length < take ? undefined : lastPageParam + 1,
    placeholderData: keepPreviousData
  });
}
```

### Prefetching / SSR

The same options functions work on the server with `queryClient.prefetchQuery` / `queryClient.ensureQueryData`:

```typescript
await queryClient.prefetchQuery(articleDetailOptions(id));
```

No duplication, no separate "server" variant.

### Suspense (`useSuspenseQuery`)

When the consumer is rendered under a `<Suspense>` boundary, prefer `useSuspenseQuery` / `useSuspenseInfiniteQuery` over `useQuery`. The same `*Options` functions feed both:

```typescript
import { useSuspenseQuery } from "@tanstack/react-query";

const { data } = useSuspenseQuery({
  ...articleDetailOptions(id),
  // `data` is non-nullable here, Suspense handles the loading state.
});
```

Notes:
- `useSuspenseQuery` requires `enabled` to be `true` at render time (it can't suspend on a "disabled" query). For optional-ID queries, gate the consumer at a higher level (don't render the component until you have the ID) instead of using `enabled: false`.
- Pairs naturally with the components-hierarchy skill's "wrap data-loading subtrees in `<Suspense>`" rule.

### Rules

- Always use `queryOptions()` / `infiniteQueryOptions()` from TanStack Query v5, gives strongly-typed `data` at the call site and lets `select` narrow the inferred type.
- One **`xKeys`** object + **standalone `*Options` functions** per domain, never bundle them into a method-bag object literal.
- Always use `API_ENDPOINTS` constants, no hardcoded URL strings.
- Always use the typed fetchers, no raw `fetch()`.
- Conditional queries: `enabled: !!id` when the ID may be null. The key still has to be a stable shape, pass `id ?? ""` to the key builder; TanStack won't run the fetcher when `enabled` is false.
- Pass the **whole params object** into the key builder so cache separation tracks every input. Don't spread params into the array, let the object be the leaf.
- Use `keepPreviousData` for paginated/search queries to prevent UI flicker.
- **Per-consumer** concerns (`select` projection, `throwOnError`, one-off cache overrides) live at the **call site**. **Domain-wide** cache policy (`staleTime`, `gcTime`, `retry`) belongs in the `*Options` function or the `QueryClient` defaults, see the layering note above.
- Key hierarchy must be composable: `all` is the prefix every other key extends.

---

## 5. Fetchers (`<utils>/fetcher.ts`), REST flow only

Skip this section if your project uses TanStack Start Server Functions exclusively, those replace the fetcher with a typed RPC call (`fetchArticlesFn({ data: params })`) and there's no JSON parsing or status-code handling for you to wrap.

For REST flows (Next.js App/Pages Router, TanStack Start API routes, Hono, Express, etc.), three typed fetchers wrap a single low-level `fetchWrapper` (or your project's equivalent that throws on non-2xx and parses JSON):

| Fetcher | HTTP Method | Params |
|---------|------------|--------|
| `getModelFetcher<Res>` | GET | `url`, `errorString`, `queryParams?`, `signal?` |
| `postModelFetcher<Res, Params>` | POST | `url`, `errorString`, `params` |
| `putModelFetcher<Res, Params>` | PUT | `url`, `errorString`, `params` |

`fetchWrapper` is the single chokepoint where status-code handling, JSON parsing, auth headers, and error normalization live. The three typed fetchers are thin generics on top.

### Rules

- Never call raw `fetch()` in components or hooks.
- Always use these typed fetchers.
- `getModelFetcher` serializes `queryParams` to `URLSearchParams` (supports arrays).
- Errors thrown from `fetchWrapper` are caught by TanStack Query and surface as `isError` / `error`.
- `errorString` is the prefix used in thrown error messages (e.g., `"Articles: 500 Internal Server Error"`), pass the resource name.
- Add `signal` plumbing for in-flight cancellation. TanStack passes one through `queryFn`:

  ```typescript
  queryFn: ({ signal }) =>
    getModelFetcher<GetArticlesResponse>({
      url: API_ENDPOINTS.ARTICLES(),
      errorString: "Articles",
      queryParams: params,
      signal
    })
  ```

  The fetcher passes `signal` to `fetch`, which aborts the request when the query is cancelled (component unmount, key change, etc.).

---

## 6. Hooks (`<hooks>/useX.ts`)

### File Convention

One hook per domain. **Options-bag** pattern, every input is optional, returned shape is uniform.

### Complete Example

```typescript
// <hooks>/useArticles.ts
import { type UseMutationOptions, useMutation, useQueryClient, useQuery } from "@tanstack/react-query";
import { API_ENDPOINTS } from "constants/apiEndpoints";
import { articleKeys, articleListOptions, articleSearchOptions } from "queries/article";
import { type PostArticleParamsSchemaType } from "schemas/article";
import { type PostArticleMutationResponse } from "types/article";
import { type PaginatedOptionsParams } from "types/common";
import { postModelFetcher } from "utils/fetcher";

interface UseArticlesProps {
  articlesSearchText?: string;
  articlesListOptions?: PaginatedOptionsParams;
  searchListOptions?: PaginatedOptionsParams;
  mutationOptions?: Pick<
    UseMutationOptions<PostArticleMutationResponse, Error, PostArticleParamsSchemaType>,
    "onSuccess" | "onError"
  >;
}

export function useArticles({
  articlesListOptions,
  searchListOptions,
  mutationOptions,
  articlesSearchText
}: UseArticlesProps = {}) {
  const queryClient = useQueryClient();

  // Mutations
  const createArticle = useMutation<PostArticleMutationResponse, Error, PostArticleParamsSchemaType>({
    mutationFn: (params) =>
      postModelFetcher({
        url: API_ENDPOINTS.ARTICLES(),
        errorString: "Articles",
        params
      }),
    async onSuccess(data, variables, context) {
      mutationOptions?.onSuccess?.(data, variables, context);
      await queryClient.invalidateQueries({ queryKey: articleKeys.all });
    },
    onError(error, variables, context) {
      mutationOptions?.onError?.(error, variables, context);
    }
  });

  // Queries, spread options, layer per-call concerns (`select` here projects the data shape)
  const articlesQuery = useQuery({
    ...articleListOptions({
      page: articlesListOptions?.page ?? 0,
      take: articlesListOptions?.take ?? 10
    }),
    select: (response) => response.articles
  });

  const searchQuery = useQuery({
    ...articleSearchOptions({
      searchText: articlesSearchText ?? "",
      page: searchListOptions?.page ?? 0,
      take: searchListOptions?.take ?? 10
    }),
    enabled: !!articlesSearchText,
    select: (response) => response.articles
  });

  // Return shape: data + loading/error + mutations
  return {
    createArticle,
    articles: articlesQuery.data ?? [],
    articlesIsLoading: articlesQuery.isLoading,
    articlesIsError: articlesQuery.isError,
    foundArticles: searchQuery.data ?? [],
    foundArticlesIsLoading: searchQuery.isLoading,
    foundArticlesIsError: searchQuery.isError
  };
}
```

### Rules

- Props interface: all optional, options-bag pattern.
- Consume queries by **spreading the `*Options` function result** into `useQuery` and adding per-call concerns (`select`, `throwOnError`, `enabled`) on top, never call `useQuery(articleListOptions(...))` without the spread when you need overrides.
- Use `select` to project / narrow the response shape so the hook's return values are already in their final form (`articlesQuery.data` is already the array, not the wrapper response).
- Mutation callbacks: `Pick<UseMutationOptions<Res, Error, Params>, "onSuccess" | "onError">` at minimum, most consumers need both. Add `onMutate` / `onSettled` only when a consumer asks for them.
- Always `queryClient.invalidateQueries({ queryKey: xKeys.all })` on mutation success.
- Always passthrough parent callbacks: `mutationOptions?.onSuccess?.(...)` and `mutationOptions?.onError?.(...)`.
- Return data with safe defaults (`?? []`, `?? null`).
- Return loading/error flags alongside data.
- Return mutation objects so consumers can read `isPending` / call `.mutate(...)`.
- Never duplicate server state into a client store (Redux/Zustand), TanStack Query is the server cache.

---

## 7. Server Entry Points (API Routes / Server Functions)

This is the **boundary** between client and server. Whatever framework the project uses, the same four steps happen here:

1. **Authenticate** if the route is private (read session, gate or 401).
2. **Validate** the input with Zod (`.parse(...)`), never trust raw input.
3. **Delegate** to a server action in `<server>/actions/*`, never call Prisma directly from the entry point.
4. **Return** a consistent shape: `{ articles, totalArticles }` for lists, `{ article }` for singles.

The example flavors below show this shape in four common frameworks. Pick the one your project uses.

### Flavor A, Next.js App Router (`<app>/api/**/route.ts`)

Default for new Next.js projects. Each HTTP method is its own exported function.

```typescript
import { NextRequest, NextResponse } from "next/server";
import { PostArticleParamsSchema } from "schemas/article";
import { findManyArticles, createArticle } from "<server>/actions/article";
import { auth } from "<server>/auth";

export async function POST(req: NextRequest) {
  const session = await auth();
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const { article } = PostArticleParamsSchema.parse(await req.json());
  const newArticle = await createArticle(article, session.userId);
  return NextResponse.json({ article: newArticle });
}

export async function GET(req: NextRequest) {
  const url = new URL(req.url);
  const page = Number(url.searchParams.get("page") ?? 0);
  const take = Number(url.searchParams.get("take") ?? 10);
  const articles = await findManyArticles({ searchQuery: {}, page, take });
  return NextResponse.json({ articles, totalArticles: articles.length });
}
```

### Flavor B, TanStack Start API Route (`<routes>/api/**/.ts`)

REST-style route in TanStack Start. Same surface as App Router, methods on a route definition.

```typescript
import { createAPIFileRoute } from "@tanstack/react-start/api";
import { json } from "@tanstack/react-start";
import { PostArticleParamsSchema } from "schemas/article";
import { findManyArticles, createArticle } from "<server>/actions/article";
import { getSession } from "<server>/auth";

export const APIRoute = createAPIFileRoute("/api/articles")({
  GET: async ({ request }) => {
    const url = new URL(request.url);
    const page = Number(url.searchParams.get("page") ?? 0);
    const take = Number(url.searchParams.get("take") ?? 10);
    const articles = await findManyArticles({ searchQuery: {}, page, take });
    return json({ articles, totalArticles: articles.length });
  },
  POST: async ({ request }) => {
    const session = await getSession(request);
    if (!session) return json({ error: "Unauthorized" }, { status: 401 });

    const { article } = PostArticleParamsSchema.parse(await request.json());
    const newArticle = await createArticle(article, session.userId);
    return json({ article: newArticle });
  }
});
```

### Flavor C, TanStack Start Server Function (`createServerFn`)

The RPC shortcut. **Replaces both the fetcher and the API route layers** with a typed function call. The query factory's `queryFn` invokes it directly, no `URL`, no `fetch`, no JSON serialization in your code (TanStack Start handles all of that).

```typescript
// <server>/functions/article.ts
import { createServerFn } from "@tanstack/react-start";
import { PostArticleParamsSchema } from "schemas/article";
import { findManyArticles, createArticle } from "<server>/actions/article";
import { authMiddleware } from "<server>/auth";
import { z } from "zod";

export const fetchArticlesFn = createServerFn({ method: "GET" })
  .validator(z.object({ page: z.number().default(0), take: z.number().default(10) }).parse)
  .handler(async ({ data }) => {
    const articles = await findManyArticles({ searchQuery: {}, ...data });
    return { articles, totalArticles: articles.length };
  });

export const createArticleFn = createServerFn({ method: "POST" })
  .middleware([authMiddleware])           // auth gate
  .validator(PostArticleParamsSchema.parse)
  .handler(async ({ data, context }) => {
    const newArticle = await createArticle(data.article, context.session.userId);
    return { article: newArticle };
  });
```

The query factory then uses the server function directly, no `<utils>/fetcher.ts` involved:

```typescript
// <queries>/article.ts (TanStack Start variant)
export function articleListOptions(params: PaginatedOptionsParams) {
  return queryOptions({
    queryKey: articleKeys.list(params),
    queryFn: () => fetchArticlesFn({ data: params }), // typed RPC call
    placeholderData: keepPreviousData
  });
}
```

This is the recommended path for new TanStack Start projects unless you need a public REST surface (third-party consumers, mobile clients).

### Flavor D, Next.js Pages Router (`<pages>/api/*.ts`), legacy

Pages Router is in maintenance mode. Only use this for projects that haven't migrated.

```typescript
import { serverProcedure } from "<server>/procedures";
import { PostArticleParamsSchema } from "schemas/article";
import { findManyArticles } from "<server>/actions/article";

const handler = serverProcedure({
  get: {
    errorMessage: "Articles",
    handler: async ({ req, res }) => {
      const { page, take } = req.query;
      // ... extract query params, call server actions
      return res.status(200).json({ articles, totalArticles });
    }
  },
  post: {
    private: true,
    errorMessage: "Articles",
    handler: async ({ req, res, session }) => {
      const { article } = PostArticleParamsSchema.parse(req.body);
      return res.status(200).json({ article: newArticle });
    }
  }
});

export default handler;
```

> `serverProcedure` is a stand-in for whatever typed handler / method dispatcher / `next-connect`-style router your project uses to avoid hand-rolling method branching in every file.

### Rules

- Always validate input with Zod (`.parse(...)` for App Router / Pages Router / API routes, `.validator(schema.parse)` for TanStack Start server functions). Never trust raw input.
- Auth-required entry points: check session at the top of the handler (App Router, Start API routes), via dispatcher gate (Pages Router), or via middleware (Start server functions).
- Call server actions from `<server>/actions/*`, **no direct Prisma in route files or server functions**.
- Return consistent shapes: `{ articles, totalArticles }` for lists, `{ article }` for singles.
- For TanStack Start projects, prefer **Server Functions over API routes** unless you specifically need a public REST surface, they collapse the fetcher and route layers into a single typed call.
- For multi-framework or REST-public projects, use API routes (App Router or Start `createAPIFileRoute`) so the contract is HTTP-shaped.

---

## 8. API Endpoints (`<constants>/apiEndpoints.ts`)

Single nested `API_ENDPOINTS` object with function helpers for dynamic paths:

```typescript
export const API_ENDPOINTS = {
  ARTICLES: () => "/api/articles",
  ARTICLE: {
    SINGLE: ({ articleId }: { articleId?: string | null }) => `/api/articles/${articleId}`
  },
  AUTHOR: {
    SINGLE: ({ authorId }: { authorId?: string | null }) =>
      `/api/authors/${authorId}`,
    ARTICLES: ({ authorId }: { authorId?: string | null }) =>
      `/api/authors/${authorId}/articles`
    // Nested resources compose from parent paths
  }
} as const;
```

### Rules

- All endpoints defined here, no hardcoded strings elsewhere in the codebase.
- Collection endpoints are functions: `ARTICLES()` (consistent call site, easy to extend with future params).
- Single-resource endpoints accept nullable params: `{ articleId?: string | null }`, matches the `enabled: !!id` pattern in queries. Note: when `articleId` is null, interpolation produces an ugly URL (`/api/articles/null`); this is benign because `enabled: false` prevents the fetch, but you'll see those URLs flash through key builders. If it bothers you, guard the path: `articleId ? \`/api/articles/${articleId}\` : ""`.
- Nested resources compose from parent functions.

---

## 9. New Domain Feature Checklist

When adding a new domain (e.g., `Widget`):

1. **Prisma schema**, add the model to `prisma/schema.prisma`, run the project's migration / push command.
2. **Types**, `<types>/widget.ts` with `Prisma.WidgetGetPayload<...>` + response types.
3. **Server actions**, `<server>/actions/widget.ts` with `IncludeWidgetRelations`, `findOneWidget`, `findManyWidgets`, `countWidgets` (and `searchManyWidgets` if full-text/geo is needed).
4. **Zod schemas**, `<schemas>/widget.ts` with `WidgetSchema`, `PostWidgetParamsSchema`, and `WidgetUpdateParamsSchema` (or `WidgetSchema.partial()` for single-language projects).
5. **API endpoints**, add to `<constants>/apiEndpoints.ts`.
6. **Server entry point**, pick the flavor matching your framework (§7):
   - Next.js App Router → `<app>/api/widgets/route.ts`
   - TanStack Start API route → `<routes>/api/widgets.ts` via `createAPIFileRoute`
   - TanStack Start Server Function → `<server>/functions/widget.ts` via `createServerFn` (skip step 5, no need for an `API_ENDPOINTS` entry, the function is its own contract)
   - Pages Router (legacy) → `<pages>/api/widgets/index.ts`
7. **Query options + keys**, `<queries>/widget.ts` with `widgetKeys` and standalone `*Options` functions (`widgetListOptions`, `widgetDetailOptions`, …).
8. **Hook**, `<hooks>/useWidgets.ts` consuming queries + mutations.
9. **Barrel export**, add hook to `<hooks>/index.ts` if the project uses barrels.

---

## 10. Anti-Patterns (Never Do)

- ❌ Raw `fetch()` in components/hooks, use the typed fetchers.
- ❌ Hardcoded API URLs, use `API_ENDPOINTS`.
- ❌ Server state mirrored into Redux / Zustand, TanStack Query is the server cache.
- ❌ Mixing `"asc"` literals and `Prisma.SortOrder.asc` enum values within one file, pick one form per file.
- ❌ Manual TS type duplication, use `z.infer<>` and `Prisma.GetPayload<>`.
- ❌ Direct Prisma calls in API route files or server functions, always go through `<server>/actions/*`.
- ❌ `"use server"` directive on data-layer functions, those are plain async, not Next.js Server Actions. (TanStack Start `createServerFn` similarly: keep the Prisma work in `<server>/actions/*`; the server function is just the entry point.)
- ❌ Calling Prisma directly from a `createServerFn` `.handler` body, same rule as API routes; delegate to `<server>/actions/*`.
- ❌ Skipping `.validator(schema.parse)` on a TanStack Start server function, the validator is the equivalent of `.parse(req.body)` in an API route.
- ❌ Non-composable query keys, always build from the domain `xKeys.all` prefix.
- ❌ Bundling queries into a single `xQueries` method-bag object, use the `xKeys` object + standalone `*Options` functions split.
- ❌ Putting **per-consumer** concerns (`select`, `throwOnError`, one-off overrides) inside the `*Options` function, those belong at the call site. Domain-wide cache policy (`staleTime`, `gcTime`, `retry`) is fine in the `*Options` function; see §4 "Where do `staleTime` / `gcTime` / `retry` live?".
- ❌ Missing `enabled` flag on queries that depend on a possibly-null ID.
- ❌ Missing `invalidateQueries` after a successful mutation.
- ❌ Skipping Zod validation on `req.body` / `req.json()`, never trust raw input.
- ❌ `new PrismaClient()` outside the singleton, leaks connections in dev (HMR) and tests.
- ❌ Spreading user input directly into `where` / `data` (`prisma.x.findMany({ where: req.query })`), always parse and project explicitly.
