---
name: tech-advisor
description: Use this when the user is unsure about which tools, libraries, or languages to use.
---

# Technical Advisor Principles

## For Beginners
When the user is a beginner, prioritize **Stability** and **AI-Support** over performance.
- **Web Apps**: Recommend **Next.js (App Router)** + **Tailwind CSS** + **Supabase**. (Reason: Easiest "batteries included" stack).
- **Data/AI Apps**: Recommend **Python** + **Streamlit** or **FastAPI**.
- **Mobile**: Recommend **React Native (Expo)**.

## Decision Making
- Never suggest a tool just because it is "new" or "trendy."
- Always check if the tool has good documentation and a large community.
- If the user needs a database, suggest **Supabase** or **Firebase** (Backend-as-a-Service) to avoid complex server management.

## Coding Standards
- **Zero Tolerance for `any`**:
  - **Rule**: You must NEVER use the `any` type in TypeScript.
  - **Why**: It defeats the purpose of TypeScript and hides bugs.
  - **Fix**: Define a proper interface (e.g., `interface ApiReponse { result: string }`) or use `unknown` if the shape is truly dynamic.
  - **Hooks**: When mapping data in a React Query hook, ensure the `.map((item) => ...)` has the correct inferred type. Do not cast `(item: any)`.

## Stack Generation
When a stack is chosen, you must be able to list the exact terminal commands to install it (e.g., `npx create-next-app@latest`).
## Delegation Logic (Heavy vs. Light)
You must follow the **Antigravity-First** principle to maximize speed and minimize token overhead.

### 1. The Rubric
- **LIGHT (Antigravity Directly)**: 
  - UI Tweaks (CSS/NativeWind, Colors, Text).
  - Documentation (README, Specs, Reviews).
  - Single-file logic bugs or type fixes.
  - Verification & Codebase audits.
- **HEAVY (Spawn Child Agent)**:
  - New multi-file features or complex scaffolding.
  - Deep architectural refactors.
  - Specialized long-running research.

### 2. Forbidden Delegations
- **NEVER** use `browser_subagent` for general coding or review tasks. It is ONLY for browser-specific automation (e.g., testing on web, taking screenshots).
- **NEVER** spawn a child agent for documentation or simple UI fixes.
- **NEVER** use `read_url_content` for local file system paths. For local files, ALWAYS use `view_file` or `view_file_outline`.