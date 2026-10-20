---
alwaysApply: true
---

## LifeOS Project Manifesto

LifeOS is a **Second Brain** designed for a 21-year-old engineering student. It bridges **high-level AI coaching** with **low-level habit tracking**.

Core philosophy:

- Gamification: Real-life habits (**Quests**) earn XP. XP is spent on **Indulgences** (reels, snacks, etc.).
- The **Oracle**: An in-app AI guide that is constructive, firm, and analytical. It uses RAG to analyze journals, health data, and habit scores.
- **Dual-State Privacy**: 
  - Normal Mode: public / casual use.
  - Deep Mode: sensitive tracking (sobriety, mental health, private journals).
- **Holistic Tracking**: Academic attendance, fitness, and "Comfort Zone" challenges.

## Engineering & Architecture Rules

- Use **Next.js 15 App Router** and **Server Actions**; avoid deprecated API routes where possible.
- Favor **typed, modular services** in `src/services` and shared utilities in `src/lib`.
- Centralize client state in `src/store` and hooks in `src/hooks`.
- All exports must use standard ES6 naming conventions (`export const`, `export function`, `export class`, `export default`).

## Security Rules

- Always **review and harden security** for new functionality:
  - Add **rate limiting** based on both **IP** and **authenticated user** identity where applicable.
  - Enforce **strict Zod validation** on all external inputs (forms, server actions, webhooks, Supabase payloads).
  - **Never** hard-code secrets; **only** read API keys and secrets from environment variables.
  - Design features to be **OWASP-aligned** (XSS, CSRF, injection, auth, access control, logging).
- Prefer **server-side operations** (Server Components / Server Actions) over exposing sensitive logic to the client.

## Privacy & Deep Mode

- Always check the **Deep Mode** toggle state before rendering or returning `is_private` or otherwise sensitive data.
- In **Normal Mode**, hide, redact, or aggregate sensitive Deep Mode data.
- Ensure that logs, analytics, and error messages **never leak Deep Mode details**.

## Oracle Tone & Behavior

- In-app AI responses must be:
  - **Firm but constructive**.
  - Provide **constructive criticism** plus **specific positive reinforcement**.
  - Action-oriented (clear next steps, micro-quests, or habit tweaks).

