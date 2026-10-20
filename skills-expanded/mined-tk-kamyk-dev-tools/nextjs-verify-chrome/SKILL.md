---
name: nextjs-verify-chrome
metadata:
  stack: [nextjs]
description: Visually verify UI changes in the Next.js frontend using Chrome DevTools MCP — start the dev server, navigate, authenticate, screenshot, compare to Figma if available, test expected behavior, and re-run tests + build before claiming the change is done.
---

# Verify with Chrome MCP

Use Chrome DevTools MCP to visually verify the current UI changes in the Next.js frontend app.

1. Start dev server from the frontend root: `pnpm dev`
2. Navigate to the URL under test (default: `https://localhost:3000`); if the user supplied an argument, use that path.
3. Authenticate if needed (auth-provider BFF flow; credentials are in `.env.local` — if not present, ask).
4. Screenshot and compare with Figma if a Figma link is in the conversation.
5. Exercise expected behavior.

## After verification

If you encountered errors or visual discrepancies, fix and repeat until clean. Before claiming the change is done, run from the frontend root:

- `pnpm check-types`
- `pnpm lint`
- `pnpm test`
- `pnpm build`
