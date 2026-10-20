---
name: nextjs-llms
description: >-
  Read and navigate Next.js documentation, the React framework.
  You MUST load this skill when working with Next.js.
license: MIT
---

# Next.js Docs

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

Next.js is the React framework for building full-stack web applications.

## WHEN TO USE

- When developing applications using the Next.js framework (App Router or Pages Router).
- When you need to look up documentation on Next.js routing, data fetching, rendering, server components, API routes, or caching.
- When you need syntax, usage examples, or version-specific details for Next.js 14, 15, or 16.

## WHEN NOT TO USE

- When working on a plain React application without Next.js (use `react-llms` instead).
- When the context is already sufficiently clear and you do not need to read the official Next.js documentation.

## Core Process

1. **Identify the Topic**: Determine which Next.js concept you need to look up (e.g., Server Components, Caching, App Router, Turbopack, or specific hooks like `useRouter`).
2. **Fetch the Documentation Index**: Read the primary `llms.txt` file from the References section below using an available web fetching tool.
3. **Locate Specific Documents**: Use the links provided in the index to fetch detailed documentation on the required topic.
4. **Apply Context**: Incorporate the fetched documentation into your task to ensure your code aligns with the official Next.js recommendations.

## Core Principles

- **Prefer Latest Docs**: Always fetch the latest documentation for the current active LTS unless working explicitly with a legacy version.
- **Agentic Loading**: Do not attempt to guess or hallucinate Next.js APIs; always fetch the documentation dynamically to stay up to date.

## References

To fully utilize this skill, you MUST read at least one of the links relevant to the current context:

- [Next.js](https://nextjs.org/llms.txt)
  MUST read for a Next.js documentation index.
  This link includes recent blog posts, documentation, support policy, etc.
- [Next.js Documentation](https://nextjs.org/docs/llms.txt): Complete Next.js documentation for LLMs.
  MUST read for reference and guides for Next.js
- [Full Next.js Documentation](https://nextjs.org/docs/llms-full.txt)
  MUST read when you need comprehensive documentation on Next.js APIs.
  MUST use a web reading tool that supports limits/pagination as this file is very large.
