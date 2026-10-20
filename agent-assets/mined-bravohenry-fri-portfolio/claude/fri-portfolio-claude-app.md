# app/
> L2 | Parent: /CLAUDE.md

## Members

layout.tsx: Root shell — `<html>` + `<body>`, Google Fonts CDN link, global CSS import, metadata (title, favicon)
page.tsx: Homepage — viewport-locked 3-column dashboard grid assembling all `@/components/home/*` components
diary/page.tsx: Diary list page — SSG, renders all diary entries via `EntryList`
diary/[slug]/page.tsx: Single diary entry page — SSG with `generateStaticParams`, renders one entry via `EntryPage`
weekly/page.tsx: Weekly list page — SSG, renders all weekly entries via `EntryList`
weekly/[slug]/page.tsx: Single weekly entry page — SSG with `generateStaticParams`, renders one entry via `EntryPage`
api/chat/route.ts: POST handler — proxies chat messages to Minimax M2.7 with streaming SSE, FRI system prompt

## Architecture Notes

- Viewport lock (`overflow-hidden h-screen w-screen`) lives on the homepage wrapper div in `page.tsx`, NOT in `layout.tsx`
- This allows future content pages (diary, weekly) to scroll normally while sharing the same root layout
- `favicon.ico` was deleted — we use `/public/favicon.png` via metadata.icons

[PROTOCOL]: Update this file when routes are added/removed, then check parent CLAUDE.md
