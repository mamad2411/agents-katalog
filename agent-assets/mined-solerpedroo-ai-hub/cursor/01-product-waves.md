---
description: Product principles, locked stack, wave order, outlier features
alwaysApply: true
---

# Product and waves

Canonical: `docs/AI_Hub_Desktop_Escopo.md`, `docs/IMPLEMENTATION_PLAN.md`.

Core is **Context Compiler + AI Gateway + Project workspace**. Chat is the surface. Model is a replaceable plug.

## Locked stack

Electron + electron-vite, React, TypeScript, Tailwind, shadcn/ui, Zustand, Drizzle, better-sqlite3, keytar, pnpm + Turborepo.

MVP packages only: `apps/desktop`, `packages/shared`, `packages/db`, `packages/security`, `packages/ai-gateway`. Providers live **inside** `ai-gateway`. Do not add `memory` / `files` / `tools` / `ui` packages before their wave.

## Wave order

Implement in plan order. Hooks in schema are OK early; features are not.

- **W0–W8**: MVP (Windows ship, TTFT < 90s). Includes OpenRouter first-class, branching, receipts, spend caps, health, crash-safe stream, compiler v0.
- **W9–W10**: Import Hub + Portable Context Packet (MVP+).
- Later waves: mentions, artifacts, skills, privacy/firewall, Quick AI, council/router, run modes/HUD (W21), MCP, single agent, agent orchestration (W24), Ollama, sync, team.

Outlier features D1–D14 in the plan are **mandatory** in their waves. Do not implement agents or orchestration before their waves.

## Close gate

Do not mark a wave complete or start N+1 until `.cursorrules` §9 passes: independent review, Blocker/High fixed, `docs/reviews/WXX/` persisted (REVIEW + DIFF), required `docs/ADR/ADR-WXX-*.md` written, residual risks reported.

## Never

Silent model fallback. Hidden cost. Cloud account required for MVP. Voice/marketplace/sync before their wave. “Build the cool part first.” Closing a wave without review.
