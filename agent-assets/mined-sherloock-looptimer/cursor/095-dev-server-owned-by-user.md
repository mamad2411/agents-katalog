---
description: "Dev server ownership: the user runs Next.js dev server; the agent never starts it."
globs: "**/*"
---

## Dev server ownership (mandatory)
- Do **not** run `npm run dev`, `next dev`, or start any long-running dev server process.
- Ask the user to run the dev server locally and provide the URL/port when runtime verification is needed.
- It is ok to run non-server commands like `npm run lint`, `npm test`, `npm run build`.

