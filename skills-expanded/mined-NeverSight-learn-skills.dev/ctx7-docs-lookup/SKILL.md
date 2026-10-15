---
name: ctx7-docs-lookup
description: Forces the use of ctx7 (context7 MCP) to consult official documentation when encountering repeated or unknown errors during coding, or when uncertain whether your knowledge accurately applies to the current project during planning. Triggers on any code implementation or planning situation, especially when errors repeat 2+ times or library/framework API usage is uncertain. Consult this skill whenever debugging errors, adopting new libraries, verifying API usage, writing config files, handling migrations, or any situation where checking official docs could prevent wasted effort.
---

# ctx7 Official Documentation Lookup Guide

## Why This Skill Exists

LLM training data contains outdated APIs, removed options, and behaviors that changed between versions. Relying solely on this knowledge leads to calling non-existent functions, using deprecated patterns, or generating code incompatible with the project's actual library versions. The result is wasted time debugging phantom issues and plans built on false assumptions.

ctx7 (context7 MCP) can query **official documentation matching the exact version** of libraries used in the current project. Work from facts, not guesses.

## When NOT to Use ctx7

Do not look up documentation for APIs and patterns you are fully confident about. ctx7 lookups cost time and tokens. If the answer is obvious and the API is stable, just write the code.

**Skip ctx7 when ALL of the following are true:**

- The API is well-established and has not changed across recent major versions (e.g., `useState`, `useEffect`, `fetch`, `Array.map`, basic DOM APIs)
- You are fully confident in the exact signature, behavior, and usage pattern
- The task does not involve version-specific features, recent additions, or framework-level APIs that change between releases
- There are no special constraints in the task (e.g., "serverless", "edge runtime", "cross-instance") that might require a specialized variant

Examples of when to **skip** ctx7:
- Writing a React component with `useState` and `useEffect`
- Using native `fetch`, `Promise`, `AbortController`
- Standard TypeScript patterns, basic HTML/CSS
- Well-known utility library APIs (lodash, date-fns basics)

Examples of when you **must** use ctx7:
- Framework-specific caching, routing, or rendering APIs (`use cache`, `revalidateTag`, App Router patterns)
- APIs that have changed in recent major versions (`forwardRef` in React 19, `@theme` in Tailwind v4)
- New or recently added APIs you haven't used before
- Configuration files for specific framework versions
- Anything where the task mentions deployment-specific constraints

**When in doubt, consider: "Has this API changed in any recent major version?" If yes, look it up. If no, just write the code.**

## Trigger Conditions

### Condition 1: Repeated Errors During Implementation

When writing or debugging code, ctx7 lookup is **mandatory** if any of the following occur:

- The same or similar error appears **2 or more times**
- The root cause of an error message is unclear
- The exact signature, options, or behavior of a library/framework API is uncertain
- An attempted fix did not work and the reason is unknown

Continuing to guess-and-retry in these situations is a waste of time. Stop and consult the official docs via ctx7 immediately.

### Condition 2: Insufficient Confidence During Planning

When building an implementation plan or making design decisions, ctx7 lookup is **mandatory** if any of the following apply:

- You are not confident your knowledge accurately applies to the library versions in the current project
- You are unsure whether a specific API or config option is available in the current version
- You lack confidence that the planned implementation will work correctly
- You are introducing a new library or using a feature for the first time
- The task involves migration or version upgrade work

Planning based on "this will probably work" can cause the entire plan to collapse during implementation. If you are not certain, check the docs first.

## How to Use context7

context7 can be accessed through multiple paths depending on your environment. Use whichever is available to you:

| Access Method | How |
|---|---|
| **MCP tools** | `mcp__context7__resolve-library-id` and `mcp__context7__query-docs` |
| **Skill** | Invoke the `find-docs` skill (if installed) |
| **Other integrations** | Any context7-compatible plugin, extension, or CLI tool available in your environment |

The important thing is not *how* you access context7, but that you **do** access it when the trigger conditions are met.

### Step 0: Understand the Project First

Before querying docs, check what you're actually working with:

1. Read `package.json` (or equivalent dependency file) to identify the **exact versions** of libraries in use.
2. Note the project's tech stack — framework, language, deployment target (serverless, edge, etc.).
3. Use version-specific library IDs when available (e.g., `/vercel/next.js/v15.1.8` instead of `/vercel/next.js`).

This context shapes your queries. A project on Next.js 15 with Vercel serverless deployment needs different docs than one on Next.js 14 with a Node.js server. Without this step, you may find correct documentation for the wrong version.

### Lookup Workflow

1. **Resolve the library ID** — identify the library you need docs for (e.g., "nextjs", "react", "prisma", "tailwindcss").
2. **Query the documentation** — look up the specific topic you need with a detailed, descriptive query. Include the version number and project context (e.g., deployment target, runtime) in your query when relevant.
3. **Evaluate the results** — check whether the docs confirm your approach or reveal a better/newer API.
4. **If results are insufficient, query again with different keywords** — a single query is often not enough. Rephrase, broaden, or narrow your search terms. Try at least 2-3 different queries before concluding that the information isn't available.

### Query Strategy: Don't Stop at the First Result

A common failure mode is querying once, getting a partial or irrelevant result, and then falling back to training data. This defeats the purpose of the lookup. Follow this escalation pattern:

1. **First query: direct and specific** — use the exact API name or feature you're looking for.
   - Example: `"updateTag revalidateTag cache invalidation"`
2. **Second query: broaden if needed** — if the first query misses, try related concepts or the feature category.
   - Example: `"cache invalidation server actions use cache"`
3. **Third query: search for what's new** — explicitly ask about new or changed APIs in the current version.
   - Example: `"new APIs next.js 15 caching breaking changes"`

Do not assume your first query covers everything. Libraries often have multiple APIs for similar tasks, and the one you don't know about may be the correct one for your use case.

### Verify Your Chosen API Is the Best Fit

After finding an API that works, ask yourself: **"Is there a more specific API designed for exactly this use case?"** General-purpose APIs often have specialized alternatives that handle edge cases better.

For example:
- `revalidateTag` works for cache invalidation, but `updateTag` exists specifically for read-your-own-writes scenarios
- `'use cache'` works for caching, but `'use cache: remote'` exists specifically for cross-instance cache sharing in serverless

If the task description mentions a specific constraint (e.g., "serverless", "immediate consistency", "cross-instance"), query the docs for that constraint explicitly before settling on a general solution.

### Tips for Effective Queries

- Be specific with your topic. "next.config.js cacheComponents" is far better than "config".
- Include key terms from the error message in your topic.
- Check the project's `package.json` or config files for the exact version first, then reference docs for that version.
- When the task has specific requirements (e.g., "shared across instances", "immediate invalidation"), include those requirements as keywords in your query.

## Self-Check Questions

If you can answer "yes" to any of these during work, you should use ctx7:

1. Is this not the first time I've seen this error? Am I hitting the same class of error repeatedly?
2. Am I confident this API/option/config behaves exactly this way in the current project's version?
3. Is the code I'm about to write the pattern recommended by the official docs?
4. Do I have concrete evidence that my planned approach will actually work?
5. Could there be a more specific API designed for exactly this use case that I'm not aware of?

## Important Notes

- ctx7 is a tool, not a silver bullet. After consulting the docs, you still need to adapt findings to the project's context.
- If documentation conflicts with the project's existing patterns or conventions, prioritize the project's established approach while using the docs as a reference to adjust.
- You do not need to use ctx7 for every API call. Querying things you already know with certainty is inefficient. The key is to use it when you **don't know**, when you **lack confidence**, or when **errors keep repeating**.
