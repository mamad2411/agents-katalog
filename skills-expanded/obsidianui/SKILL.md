---
name: obsidianui
description: "ObsidianUI animated React components (obsidianui.dev) for React/Next.js + Tailwind. Use for cursor effects, text reveals, marquees, scroll and 3D galleries, WebGL backgrounds, fancy buttons."
---

# ObsidianUI

MIT licensed, shadcn-compatible registry of animated React components. Source is copied into the project (no runtime package). Public reads need no key or account.

Base: `https://www.obsidianui.dev`

## Workflow

1. **Pick a component** from `references/catalog.md` (29 documented effects + 63 UI primitives). If the list may be stale, re-check `GET /r/registry.json` (`items[].name`). Never invent names; a 404 means it does not exist.
2. **Read its docs** (props, usage example): `curl -fsS https://www.obsidianui.dev/markdown/docs/{name}.md`
3. **Fetch the manifest**: `curl -fsS https://www.obsidianui.dev/r/{name}.json`. Read every `files[].content`, `files[].target`, `dependencies`, `docs`, `meta`.
4. **Install**, one of:
   - shadcn project: `npx shadcn@latest add "https://www.obsidianui.dev/r/{name}.json"`
   - or add to `components.json`: `"registries": { "@obsidian": "https://www.obsidianui.dev/r/{name}.json" }` then `npx shadcn@latest add @obsidian/{name}`
   - manual: write each file to its resolved target, install `dependencies` with the project's package manager.
5. **Resolve targets** via the project's `components.json` aliases: `@ui/` → `aliases.ui`, `@components/` → `aliases.components`, `@lib/` → `aliases.lib`, `@hooks/` → `aliases.hooks`. Example defaults: `@ui/button.tsx` → `src/components/ui/button.tsx`, `@components/block/hover-img.tsx` → `src/components/block/hover-img.tsx`. `public/` targets are relative to project root. **Never create literal `@ui` / `@components` folders.** Diff existing files before overwriting.
6. **Preserve** `"use client"`, CSS files/imports, shaders, hooks, local helpers.
7. **Replace demo assets**: `meta.remoteAssets` lists remote demo images/videos; swap for the user's own. `meta.requiredEndpoints` means the app must implement those endpoints itself.
8. **Verify** in the browser with real content, keyboard focus, `prefers-reduced-motion`, and mobile viewport. Copying is not testing.

## Prerequisites

React + Tailwind project (docs assume Next.js App Router, `src/`, `@/*` alias). Most components need a `cn` helper:

```ts
// src/lib/utils.ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)); }
```

Common deps: `motion clsx tailwind-merge lucide-react`. Heavy ones per component: `gsap`, `three`, `@react-three/fiber`, `@react-three/drei`, `lenis`, `@paper-design/shaders-react`.

## Other access paths

- Any page as Markdown: `Accept: text/markdown` header, or `/markdown/docs/{slug}.md`
- Index: `/llms.txt`; everything in one file: `/llms-full.txt` (~450 KB, avoid unless needed)
- OpenAPI: `/openapi.json`
- MCP: shadcn MCP (`npx shadcn@latest mcp init`) can browse the `@obsidian` registry. The repo also has a local stdio resource server (`git clone https://gitlab.com/Atharvsinh-codez/ObsidianUI.git && npm ci && npm run registry:build && npm run mcp`, resources at `obsidian://{name}`). No hosted MCP endpoint.

## Limits

Component library only: no backend, auth, storage, or hosting. Demo media keeps its own license. Keep MIT notice where required.
