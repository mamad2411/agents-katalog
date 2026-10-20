<!-- agent-notes: { ctx: "web/mobile monorepo scaffold workflow", deps: [CLAUDE.md], state: active, last: "sato@2026-02-12" } -->
Scaffold a web/mobile monorepo: $ARGUMENTS

You are setting up this repository as a web or mobile monorepo. Follow these steps:

## 0. Template Setup

Swap the storefront README for the project placeholder, move scaffolds into place, and clean up template-only files:

```bash
# Swap README: replace storefront with project placeholder
if [ -f README-template.md ]; then
  mv README-template.md README.md
fi

# Move stub docs from scaffolds/ to docs/ root
mv docs/scaffolds/*.md docs/ 2>/dev/null
rmdir docs/scaffolds 2>/dev/null

# Remove samples directory (only useful on the template repo itself)
rm -rf samples/ 2>/dev/null

# Remove template-specific ADRs (not relevant to inheriting projects)
rm -rf docs/adrs/template/

# Remove template research/comparison docs
rm -f docs/research/how-we-compare-*.md docs/research/agent-teams-comparison.md
rm -f docs/research/squad-vs-vteam-*.md docs/research/ux-gap-analysis-*.md
rm -f docs/research/what-*-can-learn-from-*.md docs/research/what-we-learn-from-*.md
```

## 1. Gather Requirements

Ask the user to choose their tech stack. Present these options:

**Monorepo tooling:**
- **Turborepo** — Fast, minimal config, great for TypeScript projects (Recommended)
- **Nx** — Feature-rich, powerful dependency graph, good for large teams
- **pnpm workspaces only** — Lightweight, no extra build orchestration layer

**Package manager:**
- **pnpm** (Recommended — fast, strict, disk-efficient)
- **bun** — Very fast, all-in-one runtime + package manager
- **npm** or **yarn**

**Frontend framework (ask which apps they need — could be multiple):**
- **Next.js** — Full-stack React, SSR/SSG, API routes (Recommended for web)
- **React + Vite** — Lightweight SPA, fast dev server
- **React Native / Expo** — Mobile apps sharing code with web
- **SvelteKit** — Svelte-based, lightweight alternative to Next.js
- **Other** — Let the user specify

**Styling:**
- **Tailwind CSS** (Recommended)
- **CSS Modules**
- **styled-components / Emotion**
- **Other**

**Additional options to ask about:**
- Shared UI component library package? (e.g., `packages/ui`)
- Shared config packages? (e.g., `packages/tsconfig`, `packages/eslint-config`)
- API layer? (tRPC, REST with OpenAPI, GraphQL)
- Database / ORM? (Prisma, Drizzle, none yet)
- CI pipeline (GitHub Actions)?
- Do they want Storybook for the component library?

## 2. Create an ADR

Once choices are made, create an ADR at `docs/adrs/` documenting:
- The chosen monorepo tooling, frameworks, and packages
- Why these were selected
- Trade-offs

## 3. Scaffold the Project

Based on the choices, create the project structure. General shape:

```
apps/
    web/                # Primary web app (Next.js, Vite, etc.)
        src/
        package.json
    mobile/             # (if requested) React Native / Expo app
        src/
        package.json
packages/
    ui/                 # (if requested) Shared component library
        src/
            index.ts
            Button.tsx  # Starter component
        package.json
    tsconfig/           # (if requested) Shared TypeScript configs
        base.json
        package.json
    eslint-config/      # (if requested) Shared ESLint config
        index.js
        package.json
package.json            # Root workspace config
turbo.json              # (if using Turborepo) Pipeline config
pnpm-workspace.yaml     # (if using pnpm)
tsconfig.json           # Root TypeScript config
```

### In all cases, also:
- Update `CLAUDE.md` with the chosen tech stack, workspace structure, and conventions
- Update `README.md` with project description, setup instructions, and workspace overview
- Add a root `.gitignore` appropriate for Node/TypeScript
- Create a starter test in each app
- Add `dev`, `build`, `test`, and `lint` scripts to root `package.json`
- If CI was requested, create `.github/workflows/ci.yml`
- Configure TypeScript strict mode
- Add agent-notes to all new files per `docs/methodology/agent-notes.md`

## 4. Verify

Install dependencies and run the build and test suite to confirm everything works. Fix any issues.

## 5. Summary

Tell the user what was created, the workspace structure, and the key commands.
