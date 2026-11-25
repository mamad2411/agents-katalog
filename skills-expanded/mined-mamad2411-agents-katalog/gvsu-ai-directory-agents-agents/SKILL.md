# LakerAI Directory - Agent Rules & Guidelines

This file defines the project-scoped rules and instructions for Google Antigravity agents working on this codebase.

## Project Environment & Stack
*   **Framework**: Next.js 15.5 (App Router), React 19, Tailwind CSS.
*   **Database & Services**: Firebase Firestore, Storage, and Authentication.
*   **Deployment**: Firebase App Hosting.
*   **Firebase Project**: `studio-3913196954-d2b0d` (configured in `src/firebase/config.ts`).

## Style Guidelines
*   **Primary Brand Color**: GVSU Blue (`#0032A0`) for navigation, accents, and branding.
*   **Secondary/Card Background**: Light grey-blue (`#ECF0F2`).
*   **Accent Color**: Vibrant purple (`#601EE3`) for interactive call-to-actions.
*   **Typography**: `Literata` (serif) for headings, `Inter` (sans-serif) for body text.

## Administration Permissions Whitelist
Only users with these emails should be granted admin routing/privileges:
*   `indrajis@mail.gvsu.edu`
*   `vanharkj@gvsu.edu`
*   `vanharkj@mail.gvsu.edu`
*   `joseph_email_here@gvsu.edu`

## AI Flow Integration
*   The project uses **Genkit** (`@genkit-ai/google-genai` and `genkit`) for AI flows.
*   All Genkit flows are located under `src/ai/flows`.
*   Ensure that any local runs are supplied with a `GEMINI_API_KEY` via `.env`.
