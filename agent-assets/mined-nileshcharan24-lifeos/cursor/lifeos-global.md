---
alwaysApply: true
---

## LifeOS Global Rules

### Tech Stack:
- **Framework:** Next.js 15 (App Router) + TypeScript
- **Styling:** Tailwind CSS + ShadcnUI
- **Backend:** Supabase (Auth, Postgres DB, Edge Functions, Storage)
- **AI Engine (Cloud):** OpenRouter (Claude 3.5 Sonnet, Gemini 1.5 Flash)
- **Local AI (Optional):** Ollama + Qdrant

### Engineering & Architecture Rules (Always Apply):
- Use **Next.js 15 App Router** and **Server Actions**; avoid deprecated API routes where possible.
- Favor **typed, modular services** in `src/services` and shared utilities in `src/lib`.
- Centralize client state in `src/store` and hooks in `src/hooks`.
- All exports must use standard ES6 naming conventions (`export const`, `export function`, `export class`, `export default`).

### Oracle Tone & Behavior (Always Apply):
- In-app AI responses must be:
  - **Firm but constructive**.
  - Provide **constructive criticism** plus **specific positive reinforcement**.
  - Action-oriented (clear next steps, micro-quests, or habit tweaks).
- **Personalized:** For the user (a soft person who learns with constructive criticism and positive reinforcement). The AI should find a middle ground, not too soft or too strict, and suggest improvements based on habits and results.
