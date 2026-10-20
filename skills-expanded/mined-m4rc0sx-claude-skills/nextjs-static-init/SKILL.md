---
name: nextjs-static-init
description: Bootstrap a new Next.js project for STATIC EXPORT deployed on GitHub Pages — no API routes, no server runtime, all pages pre-rendered at build time. Strict TypeScript / ESLint / Prettier / Tailwind 4 baseline with `output: "export"`, basePath handling, unoptimized images, `.nojekyll`, and a GitHub Actions deploy workflow. Use whenever the user asks for a Next.js project that "ships to GitHub Pages", "is a static site", "has no backend", or "deploys to gh-pages".
---

# Next.js static export → GitHub Pages

Apply this skill end-to-end whenever the user wants a Next.js site that compiles to plain HTML/CSS/JS and is served by GitHub Pages. The configs below are designed to work together — don't pick and choose; deviations have to be justified in the PR that introduces them.

## What "static export" means in Next 16

`output: "export"` makes `next build` emit a fully static `out/` directory. **No Node runtime is needed in production.** Every page must be pre-rendered at build time. This intentionally removes a lot of Next features:

| Works on static export | Does NOT work |
|---|---|
| Server Components (rendered at build) | API routes / Route Handlers |
| `generateStaticParams` | Server Actions |
| `generateMetadata` (build-time) | `cookies()`, `headers()`, `draftMode()` |
| `<Image>` with `unoptimized: true` | Default `<Image>` optimization endpoint |
| `sitemap.ts`, `robots.ts` (Next serialises them) | `middleware.ts` (no edge runtime) |
| MDX, static `fetch()` with `cache: "force-cache"` | `revalidate` other than `false` |
| React Compiler | Incremental Static Regeneration |
| Client Components | Streaming SSR |

If any of those right-column features are needed, this is the wrong skill — push the user to Cloudflare Pages or Vercel, which support full Next.js.

## Before you start

Verify with **Bash** that the user has the right tooling. **Always check current versions first** — the pinned numbers below were correct when this skill was written and drift over time. If `node`, `pnpm`, `next`, etc. have moved on, use the newer versions; do not downgrade to match this file.

```bash
# Node LTS — currently 24 (active LTS through Oct 2027 as of writing)
node --version

# pnpm — install via corepack so the version stays repo-pinned
corepack --version && pnpm --version

# git and (recommended) gh
git --version && gh --version
```

If Node is missing or wrong LTS:
```bash
fnm install --lts && fnm use lts-latest
# or: nvm install --lts && nvm use --lts
```

If pnpm is missing:
```bash
corepack enable
corepack prepare pnpm@latest --activate
```

Then ask the user (one short prompt) for:
- **Project name** (e.g. `myapp-static`).
- **Target directory** (default `./<name>`).
- **Deployment URL shape** — see Step 1.

## Step 1 — Decide the deployment URL shape

GitHub Pages has three deployment shapes that change the config later:

| Shape | URL | `basePath` | `assetPrefix` |
|---|---|---|---|
| User / org pages | `https://<user>.github.io` | unset | unset |
| Project pages | `https://<user>.github.io/<repo>` | `/<repo>` | `/<repo>/` |
| Custom domain (CNAME) | `https://example.com` | unset | unset |

Ask the user which one applies. This decision propagates into `next.config.ts` (Step 9) and SEO URLs (Step 14).

## Step 2 — Scaffold

```bash
pnpm create next-app@latest <project-name> \
    --typescript \
    --eslint \
    --tailwind \
    --app \
    --src-dir \
    --import-alias '@/*' \
    --turbopack \
    --no-experimental-https \
    --use-pnpm
```

`cd` into the project. The boilerplate `create-next-app` emits is a starting point; the next steps **replace** the ESLint config, Prettier config, and `tsconfig.json`. Do not preserve the boilerplate values "to be safe".

## Step 3 — Pin Node and pnpm versions

Lock the toolchain so collaborators (and CI) land on the same versions:

```bash
node --version | sed 's/^v//' > .nvmrc
```

Then in `package.json`, next to `"name"`:

```json
{
  "packageManager": "pnpm@<version-from-shell>",
  "engines": { "node": ">=22 <25" }
}
```

(Bump the engines range as new LTS lines land.)

## Step 4 — `tsconfig.json`

Write **exactly** this — `create-next-app`'s default is much laxer and will mask real bugs:

```json
{
  "compilerOptions": {
    "target": "ES2023",
    "lib": ["ES2023", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "jsx": "preserve",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "moduleDetection": "force",
    "resolveJsonModule": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules", ".next", "dist", "out"]
}
```

Non-negotiables baked in: `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `verbatimModuleSyntax`, `noPropertyAccessFromIndexSignature`. They produce real warnings on real bugs and force discipline at every boundary.

Warn the user that shadcn-generated components occasionally fail under `exactOptionalPropertyTypes`; the workaround is to let the prop flow through `...props` rather than passing it explicitly.

## Step 5 — ESLint flat config

Install:
```bash
pnpm add -D eslint @eslint/js typescript-eslint \
    eslint-config-next \
    eslint-plugin-jsx-a11y \
    eslint-plugin-react \
    eslint-plugin-react-hooks \
    eslint-plugin-react-compiler \
    eslint-config-prettier
```

Write `eslint.config.mjs`:

```js
// @ts-check
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import next from "@next/eslint-plugin-next";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import reactCompiler from "eslint-plugin-react-compiler";
import a11y from "eslint-plugin-jsx-a11y";
import prettier from "eslint-config-prettier/flat";

export default tseslint.config(
  { ignores: [".next/", "node_modules/", "dist/", "out/"] },
  js.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  ...tseslint.configs.stylisticTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        projectService: { allowDefaultProject: ["*.mjs", "*.js"] },
        tsconfigRootDir: import.meta.dirname,
      },
    },
    plugins: {
      "@next/next": next,
      react,
      "react-hooks": reactHooks,
      "react-compiler": reactCompiler,
      "jsx-a11y": a11y,
    },
    settings: { react: { version: "detect" } },
    rules: {
      ...next.configs.recommended.rules,
      ...next.configs["core-web-vitals"].rules,
      ...react.configs.recommended.rules,
      ...react.configs["jsx-runtime"].rules,
      ...reactHooks.configs.recommended.rules,
      ...a11y.configs.recommended.rules,
      "react-compiler/react-compiler": "error",
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_" },
      ],
      "@typescript-eslint/consistent-type-imports": [
        "error",
        { fixStyle: "inline-type-imports" },
      ],
      "@typescript-eslint/no-misused-promises": "error",
      "@typescript-eslint/no-floating-promises": "error",
      "@typescript-eslint/switch-exhaustiveness-check": "error",
      "react/jsx-key": ["error", { checkFragmentShorthand: true }],
    },
  },
  prettier, // MUST be last — disables stylistic rules Prettier owns
);
```

In Next 16, `next lint` was removed. Use `pnpm lint` (the ESLint CLI directly). The skill's `package.json` scripts reflect that.

## Step 6 — Prettier 3

Install:
```bash
pnpm add -D prettier @ianvs/prettier-plugin-sort-imports prettier-plugin-tailwindcss
```

Write `.prettierrc.json`:

```json
{
  "semi": true,
  "singleQuote": false,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2,
  "arrowParens": "always",
  "endOfLine": "lf",
  "plugins": [
    "@ianvs/prettier-plugin-sort-imports",
    "prettier-plugin-tailwindcss"
  ],
  "importOrder": [
    "<BUILTIN_MODULES>",
    "<THIRD_PARTY_MODULES>",
    "",
    "^@/(.*)$",
    "",
    "^[./]"
  ],
  "importOrderParserPlugins": ["typescript", "jsx", "decorators-legacy"],
  "importOrderTypeScriptVersion": "5.0.0"
}
```

**Plugin order matters.** `prettier-plugin-tailwindcss` must be **last** so it runs after the import sorter and sees the final import-sorted source.

Write `.prettierignore`:
```
.next
node_modules
dist
out
pnpm-lock.yaml
public/
```

## Step 7 — Tailwind 4

`create-next-app --tailwind` scaffolds Tailwind via the `@tailwindcss/postcss` plugin. Confirm:

- `postcss.config.mjs` references `@tailwindcss/postcss` (no separate `tailwindcss` plugin entry).
- **No `tailwind.config.{js,ts}` file exists.** Tailwind 4 reads configuration from `globals.css` via `@theme`. If a `tailwind.config.*` was scaffolded, delete it.
- `src/app/globals.css` starts with `@import "tailwindcss";`.

Keep design tokens in **one** `@theme inline { ... }` block in `globals.css` so changing a token propagates everywhere (HSL/OKLCH primitives in `:root` and `.dark`, semantic aliases inside `@theme inline`).

If using `tailwind-merge` with custom typography or color tokens, **extend** the merger so it knows your custom class groups:

```ts
// src/lib/utils.ts
import { type ClassValue, clsx } from "clsx";
import { extendTailwindMerge } from "tailwind-merge";

const twMerge = extendTailwindMerge({
  extend: {
    classGroups: {
      "font-size": [
        { text: ["display-xl", "display-lg", "body-md", "body-sm", "button-md"] },
      ],
    },
  },
});

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

## Step 8 — VS Code settings

Write `.vscode/settings.json` (commit it):

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "[typescript]": { "editor.defaultFormatter": "esbenp.prettier-vscode" },
  "[typescriptreact]": { "editor.defaultFormatter": "esbenp.prettier-vscode" },
  "[json]": { "editor.defaultFormatter": "esbenp.prettier-vscode" },
  "[jsonc]": { "editor.defaultFormatter": "esbenp.prettier-vscode" },
  "[css]": { "editor.defaultFormatter": "esbenp.prettier-vscode" },
  "eslint.useFlatConfig": true,
  "eslint.workingDirectories": [{ "mode": "auto" }],
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,
  "tailwindCSS.experimental.classRegex": [
    ["cn\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"],
    ["cva\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"]
  ]
}
```

Recommended VS Code extensions (`.vscode/extensions.json`):
```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss"
  ]
}
```

## Step 9 — `package.json` scripts

Replace the scripts block:

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "preview": "pnpm build && npx serve@latest out --listen 3001",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest",
    "e2e": "playwright test",
    "check": "pnpm format:check && pnpm lint && pnpm typecheck"
  }
}
```

`pnpm preview` serves the built `out/` locally — the only honest way to test a static export, because `next start` lies (it runs a Node server). Always test on `serve` before pushing. `pnpm check` is the consolidated pre-push command.

## Step 10 — `next.config.ts`

Replace the scaffolded `next.config.ts` with:

```ts
import type { NextConfig } from "next";

// Set ONLY for the "project pages" shape (https://<user>.github.io/<repo>).
// Leave empty for user/org pages and custom-domain deployments.
const repo = ""; // e.g. "my-project"

const config: NextConfig = {
  output: "export",
  reactCompiler: true,
  // GitHub Pages serves /foo/ from /foo/index.html; opting in to
  // trailing slashes everywhere keeps URLs consistent and prevents
  // redirect chains.
  trailingSlash: true,
  // GitHub Pages has no image optimizer. Either accept un-optimized
  // images (simple) or wire a custom loader (Cloudflare Images,
  // Imgix, etc.). Default to unoptimized; revisit if LCP regresses.
  images: { unoptimized: true },
  ...(repo
    ? {
        basePath: `/${repo}`,
        assetPrefix: `/${repo}/`,
      }
    : {}),
};

export default config;
```

Tell the user: **do not** hand-add `useMemo` / `useCallback` / `React.memo` going forward — React Compiler memoises everything that can be memoised. Only re-introduce manual memoisation when the compiler explicitly logs that it skipped a component AND the profiler shows it matters.

If `basePath` is set, anything that builds URLs by hand (sitemap entries, OG image absolute URLs, JSON-LD `@id`s, schema.org `url` fields) MUST include it. Centralise the base URL in one constant (see Step 12).

## Step 11 — Sweep for runtime-only patterns

Tell the user up front, before they start writing pages, what static export forbids:

- **No `app/api/` directory.** Route Handlers do not execute on Pages — they error at build time. If data is needed, fetch it at build inside Server Components or pre-generate JSON files in `public/`.
- **No `middleware.ts`** at the project root. No edge runtime here.
- **No Server Actions** (`"use server"` files or inline `action={...}` on forms).
- Every `app/**/[slug]/page.tsx` MUST export `generateStaticParams()` returning every slug to pre-render, and ideally `export const dynamicParams = false;` so a missing slug 404s at build time rather than at request time.
- `not-found.tsx` files render into `out/404.html`; GitHub Pages serves them for any missing path automatically.

If the user later wants something static export can't do, the migration is to deploy on Cloudflare Pages or Vercel — not to hack around the limitation.

## Step 12 — Env validation (recommended)

Static export means **all env is build-time**. There is no `process.env.SECRET` available in the deployed site; every value baked in at build is visible in the bundle. Plan accordingly: only `NEXT_PUBLIC_*` values, only non-secret config.

Install:
```bash
pnpm add @t3-oss/env-nextjs zod
```

Skeleton `src/lib/env.ts`:

```ts
import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

// Set this to the URL Pages will serve from (Step 1).
// Examples:
//   "https://<user>.github.io"
//   "https://<user>.github.io/<repo>"
//   "https://example.com"
export const SITE_URL = "https://example.com";
export const BASE_PATH = ""; // or "/<repo>" — must match next.config.ts

export const env = createEnv({
  server: {
    // Static export — no server runtime. Leave empty.
  },
  client: {
    NEXT_PUBLIC_SITE_URL: z.string().url().default(SITE_URL),
  },
  experimental__runtimeEnv: {
    NEXT_PUBLIC_SITE_URL: process.env.NEXT_PUBLIC_SITE_URL,
  },
});
```

Import `env`, `SITE_URL`, and `BASE_PATH` from this module everywhere — never reach for `process.env.*` directly.

## Step 13 — Custom domain (only if applicable)

If the user has a custom domain pointed at Pages via CNAME:

```bash
mkdir -p public
printf 'example.com\n' > public/CNAME
```

The CNAME file gets copied verbatim into `out/`, GitHub Pages reads it and issues a Let's Encrypt cert automatically (allow up to ~24 h on first setup).

Also confirm DNS:
- **Apex domain** (`example.com`): `A` records to GitHub's four Pages IPs (`185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`).
- **Subdomain** (`www.example.com`): `CNAME` to `<user>.github.io`.

## Step 14 — `.nojekyll`

GitHub Pages defaults to processing the output through Jekyll, which strips files and folders starting with an underscore (Next emits `_next/`). Tell Pages to skip Jekyll:

```bash
mkdir -p public
touch public/.nojekyll
```

The empty file is intentional — its presence is the signal.

## Step 15 — GitHub Actions deploy workflow

The modern path is "Pages source: GitHub Actions" (set this once in Settings → Pages → Source: GitHub Actions). No `gh-pages` branch needed.

Write `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [<default-branch>]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version-file: .nvmrc
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm check
      - run: pnpm build
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: out

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

Notes:
- Replace `<default-branch>` with whatever `git symbolic-ref --short HEAD` reports after `git init` (typically `main` or `master`). Do not hard-code one — it has to match the user's actual default.
- `concurrency` with `cancel-in-progress: false` queues deploys instead of cancelling them — losing a deploy half-way is worse than waiting.
- `pnpm check` (format + lint + typecheck) gates the deploy; broken commits never reach production.
- `node-version-file: .nvmrc` keeps CI in lockstep with local — Step 3 already wrote `.nvmrc`.

## Step 16 — SEO files

`sitemap.ts` and `robots.ts` work under static export — Next serialises them to `out/sitemap.xml` and `out/robots.txt` at build time. **They will not auto-detect the deployment URL**; use `SITE_URL` from `src/lib/env.ts`.

`generateMetadata` (build-time) works the same as on a Node deploy. Use it; don't write `<Head>` by hand. Same for `app/icon.tsx`, `app/apple-icon.tsx`, `app/opengraph-image.tsx`, and `app/manifest.ts` — they all evaluate at build.

## Step 17 — Verify locally before the first push

```bash
pnpm install
pnpm format    # write any pending formatting
pnpm check     # format:check + lint + typecheck
pnpm build     # emits out/
pnpm preview   # opens http://localhost:3001
```

In the browser, click through every route and check:
- **No 404s** on static assets in the Network tab (asset prefix correct).
- **Internal links** navigate without a full reload (trailing-slash configured).
- **Images render** (either `unoptimized: true` is set or a custom loader works).
- **`view-source:` on any page** shows the actual HTML, not just a `<div id="__next">` shell — confirms SSR-at-build-time worked.
- **Zero XHR/fetch calls** in the Network tab going to `/api/*` on your own origin. If there are, either you left an API route in or you're calling one — both are deploy-breaking under static export.

## Step 18 — First commit + push

```bash
# Pull the canonical Node.gitignore (overwrites the one create-next-app
# scaffolded). Append the static-export build directory afterwards —
# the upstream Node.gitignore does not know about `out/`.
curl -sLo .gitignore https://raw.githubusercontent.com/github/gitignore/main/Node.gitignore
printf '\n# Next static export output\nout/\n' >> .gitignore

git init
git add -A
git commit -m "chore: initial static Next.js scaffold for GitHub Pages"
git remote add origin git@github.com:<user>/<repo>.git
git push -u origin HEAD
```

`git init` (no `-b` flag) honours `init.defaultBranch` from git config — works for `main`, `master`, or anything else. `git push -u origin HEAD` pushes whatever the current branch is named, so the same command works on either.

Update the workflow's `branches: [<default-branch>]` from Step 15 to match the actual branch name reported by `git symbolic-ref --short HEAD` before pushing — otherwise the workflow never fires.

Then in the GitHub UI: **Settings → Pages → Build and deployment → Source: GitHub Actions**. The workflow runs on push to your default branch and completes in ~2 min on a small project.

## Anti-patterns the skill is built to prevent

- **`any`** in `.ts` / `.tsx`. Use `unknown` and narrow with type guards or zod.
- **`as` casts** without a justification comment, or `satisfies` where it would fit.
- **`useMemo` / `useCallback` / `React.memo`** added by hand under React Compiler.
- **`process.env.*`** accessed directly outside `src/lib/env.ts`.
- **Server secrets** baked into a static export. There is no secret on a static site; if it ends up in the bundle, it is public.
- **`tailwind.config.{js,ts}`** files in Tailwind 4 projects.
- **`next lint`** in Next 16 (it was removed).
- **`next start`** to "test the build" — it lies; use `pnpm preview` (serve).
- **API routes, middleware, Server Actions, `cookies()`, `headers()`** — none of them survive `output: "export"`.
- **Hand-rolled URLs** that ignore `BASE_PATH` when deploying to the project-pages shape.
- **Relaxing `tsconfig` strictness** to get something to compile.

## Things this skill does NOT cover

- Multi-environment deploys (staging vs production). For a personal static site, `main` is production; if previews per branch are needed, switch to Cloudflare Pages or Vercel.
- Custom image loaders. Mentioned but not implemented — wire one only if `unoptimized: true` measurably hurts LCP.
- Authenticated content. Static export cannot do this; if it's needed, this is the wrong skill.
- E2E testing (Playwright). Scripts are present but config / CI integration is left to the project.

## When this skill goes stale

- Check `node --version` against the active Node LTS (https://nodejs.org/en/about/previous-releases).
- Check `pnpm create next-app --version` for current Next major. Next 16 was current at skill creation; static export semantics moved between 13 and 14 (the old `next export` CLI command was removed in favour of `output: "export"`).
- `actions/deploy-pages` and `actions/upload-pages-artifact` major versions change every ~year. Verify the latest at https://github.com/actions/deploy-pages before reusing.
- Check `tseslint`, `eslint-plugin-react-compiler`, and Tailwind major versions — when any of them bump major, audit this skill before reusing it.
- If GitHub Pages eventually supports Functions or edge runtime, revisit whether full SSR/ISR becomes viable here and split this skill apart.
