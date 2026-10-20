# CLAUDE.md — nischay.live (v3 rebuild)

You are rebuilding Nischay's personal site from the ground up. It is a small, static, content-first
site with two signature pieces: an animated wireframe **wave hero** and an **Experience section drawn
as a git graph**. Read these before writing code, in this order:

1. `docs/SPEC.md`: what the site is for, the pages and sections, and the acceptance criteria.
2. `docs/DESIGN.md`: the visual system and the exact specs for the wave, the git graph and the
   case-study layout. Follow it; don't invent a new look.
3. `docs/CONTENT.md`: **the only source of truth for copy, facts and graph data.**
4. `docs/PLAN.md`: the build order. Work phase by phase and stop at each checkpoint.
5. `docs/mockups/`: screenshots of the approved design, if present. They are the visual reference,
   and DESIGN.md wins wherever the two differ.

## Hard rules

- **Never invent content.** No made-up metrics, testimonials, project names, dates, employers, or
  links. If something the page needs isn't in `docs/CONTENT.md`, render a visible `TODO` in dev
  and list it in your summary.
- **Job titles are exact.** The AMD role is "Intern (co-op)", never "Software Engineer at AMD".
  Don't describe AMD internal projects beyond what CONTENT.md says.
- **Every claim that can link to evidence does**: PRs, app store listings, repos.
- No lorem ipsum, stock photos, emoji, or decorative gradients.
- Keep dependencies minimal. **Don't add three.js, react-three-fiber, framer-motion, GSAP or a
  CMS.** The wave is a small Canvas 2D module (see DESIGN.md). Ask before adding any runtime
  dependency that isn't listed under Stack.

## Stack (decided)

- Next.js (App Router) + TypeScript (strict), **fully static** (`output: "export"`).
- Tailwind CSS v4, with design tokens as CSS variables (DESIGN.md), mapped via `@theme inline`.
- Content: typed data in `src/content/*.ts` (work, open source, timeline/graph, profile). MDX in
  `src/content/writing/*.mdx` for posts, using `@next/mdx` or `next-mdx-remote`, whichever works
  with static export.
- Fonts via `next/font/google`: Fraunces, Geist, JetBrains Mono.
- Code highlighting: Shiki, at build time.
- OG images: `next/og`, generated at build time.
- Hosting: Vercel, with `@vercel/analytics`.
- Package manager: pnpm.

## Reference repo (patterns only)

The owner's earlier agency site, `github.com/zeus2611/daksha` (private once archived), has useful
**patterns**: CSS-variable tokens mapped into Tailwind v4 `@theme inline`, a light/dark theme
provider, and a `work/[slug]` static-params case-study route. Borrow those patterns. **Don't** copy
its visual system: Syne/Inter fonts, amber on zinc, cursor glow, three.js heroes, Sanity, and
styled-components are all out.

## Working agreements

- Work on a new branch, `v3`. Keep git history. Delete the old app (including the Go service) on
  that branch only after Phase 1 builds.
- Commit per phase with clear messages.
- Before each checkpoint, run `pnpm lint && pnpm typecheck && pnpm build` and fix everything they
  report.
- When you're unsure about a design or content choice, ask. Don't guess.

## Commands (set these up in Phase 1)

```
pnpm dev        # local dev
pnpm build      # static export to /out
pnpm lint       # eslint
pnpm typecheck  # tsc --noEmit
```
