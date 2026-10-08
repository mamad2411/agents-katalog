---
description: Project Development Guidelines
globs: ["**/*"]
alwaysApply: true
---
# yoga-ai Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-04-15

## Active Technologies
- TypeScript **5.7** on **Node.js 20+** (Next.js runtime) + **Next.js 15** (App Router), **React 19**, **Tailwind CSS 3**, **Zod 3** (002-mvp2-ui-llm-refinement)
- **N/A** for this feature (ephemeral requests; no new durable store) (002-mvp2-ui-llm-refinement)
- **N/A** for user intake (ephemeral); optional in-memory cache for media URLs only (003-mvp3-dynamic-media-ui)
- TypeScript on **Node.js 20+** (Next.js runtime) + Next.js (App Router), React, **Zod**, existing GenOrchestrator adapter (004-mvp4-routine-data-corpus)
- **Git-tracked JSON + SVG** under `docs/` and `public/`; no user or corpus DB (004-mvp4-routine-data-corpus)

- TypeScript on **Node.js 20+** (Next.js runtime) + **Next.js** (App Router), **React**, **Tailwind CSS**, **Zod** (or equivalent) for JSON validation against [contracts](./contracts/), **GenOrchestrator** via a dedicated server-only adapter module (package name TBD when wired) (001-yoga-ai-mvp)

## Project Structure

```text
backend/
frontend/
tests/
```

## Commands

npm test; npm run lint

## Code Style

TypeScript on **Node.js 20+** (Next.js runtime): Follow standard conventions

## Recent Changes
- 004-mvp4-routine-data-corpus: Added TypeScript on **Node.js 20+** (Next.js runtime) + Next.js (App Router), React, **Zod**, existing GenOrchestrator adapter
- 003-mvp3-dynamic-media-ui: Added TypeScript on **Node.js 20+** (Next.js runtime) + **Next.js** (App Router), **React**, **Tailwind CSS**, **Zod**
- 002-mvp2-ui-llm-refinement: Added TypeScript **5.7** on **Node.js 20+** (Next.js runtime) + **Next.js 15** (App Router), **React 19**, **Tailwind CSS 3**, **Zod 3**


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
