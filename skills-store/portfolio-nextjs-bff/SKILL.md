---
name: portfolio-nextjs-bff
description: "Implement Next.js UI, server rendering, and BFF transport boundaries."
---

# portfolio-nextjs-bff

Read frontend/AGENTS.md and relevant installed Next.js documentation before framework changes. Prefer Server Components where appropriate; client components own interactive UI/3D behavior.

Use route handlers for HTTP/SSE proxy boundaries and Server Actions for appropriate UI mutations. Keep backend URLs/credentials server-side; distinguish current direct-browser chat from the target BFF. Handle stream cancellation, errors and terminal state.

Follow existing Tailwind CSS configuration; do not invent a tailwind.config.ts requirement. Feature-local components/hooks are supported. Commands from frontend: npm run lint, npm run typecheck, npm run test:stories, npm run build. Check scripts and prerequisites before claiming execution.
