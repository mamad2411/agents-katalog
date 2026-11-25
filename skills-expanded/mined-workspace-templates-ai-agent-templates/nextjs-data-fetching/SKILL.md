---
name: nextjs-data-fetching
description: Chooses server components, caching and revalidation for each data need in the Next.js App Router, and fixes slow or stale pages.
---

# Next.js data fetching

Decide the freshness of each piece of data first; the code follows from that.

## Steps

1. Check the Next.js version in package.json and read its docs for caching defaults; they differ between 14 and 15 and later. Do not rely on memory.
2. For each data need ask: who sees it (everyone or one user), how fresh must it be (never changes, minutes, instant), and what changes it. Then choose:
   - Same for everyone and rarely changes: static, with `revalidate` seconds or tag-based revalidation.
   - Same for everyone but changes on events: tag the fetch and call `revalidateTag` or `revalidatePath` from the mutation.
   - Per user or per request (cookies, headers, searchParams): dynamic; keep it in a small component behind `<Suspense>`.
3. Fetch in server components with `async`/`await`. Start independent requests together with `Promise.all`; never await them in sequence. Pass promises down and unwrap them with `use` where useful.
4. Wrap slow sections in `<Suspense fallback>` with a `loading.tsx` so the shell streams first.
5. Deduplicate: call the same data function in several components freely, wrap non-fetch calls (ORM, SDK) in `cache()`.
6. Mutations use Server Actions or route handlers, validate input, and then revalidate the affected tags or paths.
7. Use client components only for interactivity. Fetch in them with a query library, and pass server-fetched initial data as props.
8. Check the build output: it lists which routes are static, dynamic or ISR. Confirm it matches the plan.

## Rules

- Never put secrets or server-only imports in client components; use `server-only`.
- Do not use `force-dynamic` to hide a caching bug.

## Report

A table of data, freshness choice, and invalidation, plus the build route summary.
