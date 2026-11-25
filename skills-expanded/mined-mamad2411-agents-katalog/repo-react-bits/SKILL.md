---
name: repo-react-bits
description: How to use React Bits (DavidHDev/react-bits, reactbits.dev), a library of 200+ animated React components (text animations, backgrounds, UI, micro-interactions) installed via shadcn or jsrepo, and its MIT + Commons Clause licence limits. Use when building a React/Tailwind front end that needs polished animation, or checking whether it can be used commercially.
---

# React Bits (`DavidHDev/react-bits`)

Licence: **MIT + Commons Clause** - you may use and modify it, including in your own products, but you may not **sell** the software itself (or a product whose value derives substantially from it) as-is. Read `LICENSE.md` and get legal advice for client resale. Cloned shallow at `/home/user/davidhdev/react-bits` (re-clone `git clone --depth 1 https://github.com/DavidHDev/react-bits`).

## What you get
Categories: Text Animations, Animations, Components, Micro, Backgrounds. Four variants per component: JS-CSS, JS-TW, TS-CSS, TS-TW. Free tools on the site: Background Studio, Shape Magic, Texture Lab.

## Install a component
```bash
npx shadcn@latest add @react-bits/BlurText-TS-TW
# or via jsrepo; each component page on reactbits.dev shows the exact command
```
Source lives in `src/` (Vite app, `wrangler.jsonc` for Cloudflare). Dependencies are minimal and tree-shakeable.

## Rules
1. Pick the TS-TW variant for TypeScript + Tailwind projects.
2. Respect `prefers-reduced-motion`; check each animated component with the `accessibility` skill.
3. Heavy WebGL backgrounds hurt mobile performance - measure with `react-performance`.

## Related
`ai-website-app-builders`, `frontend-design`, `ui-motion-design`, `react-patterns`.
