---
name: shadcn-registry
description: >-
  Scaffold and operate a self-hosted (private) shadcn component registry — distribute your own components, blocks, hooks and tokens as JSON-over-HTTP via `npx shadcn`, framework-agnostic and without MCP, wiring registry cssVars to design-token-pipeline outputs so tokens and components ship together. It PACKAGES already-built components rather than designing or compiling them. Triggers: "self-hosted/private shadcn registry / publish my components / reuse design system across projects / registry.json / 自建 shadcn registry / 私有组件库 / 跨项目共享组件 / 内部 UI 组件 registry".
license: MIT
---

# Self-Hosted shadcn Registry

Distribute **your own** design system — components, blocks, hooks, lib utils, and design tokens — as a
private registry that any project consumes with `npx shadcn add <url>`. shadcn's registry is just
**JSON over HTTP**: framework-agnostic, free, OSS, no MCP, no lock-in. This skill scaffolds the
registry and wires it to your compiled tokens.

## 0. When to Use / When NOT to Use

**Use this skill when** the task is to:
- Stand up a private/internal/self-hosted shadcn registry to reuse one design system across many repos.
- Publish your own components/blocks/hooks so other projects (or clients) install them via the CLI.
- Ship your design tokens + components together (one `shadcn add` pulls the component AND its cssVars).
- Distribute a whole design system in one command (`registry:style` / `registry:base`).

**Do NOT use this skill for** (route elsewhere):
| Task | Goes to |
|---|---|
| Design/author the actual component visuals | L3 style (`taste`/`luxury`) + `frontend-design@official` + `vercel:shadcn` |
| Compile the design tokens (DTCG → CSS vars / Tailwind) | `design-token-pipeline` (U1) — this skill *packages* its output |
| Build many product surfaces from a chassis | `uiux-surface-builder` (U3) — it *consumes* this registry |
| Pick a palette / brand visual | `theme-factory` / `brandkit` |

> **Boundary**: `design-token-pipeline` produces `build/css/variables.css`; L3 + `frontend-design`
> author the components. THIS skill takes those finished artifacts and makes them **installable** across
> projects. It does not invent components or tokens.

## 1. Architecture at a Glance (dots & lines)

```
  your design system (already built)
   ├── components/ui/*.tsx        (authored via L3 + frontend-design + vercel:shadcn)
   ├── hooks/*.ts  lib/*.ts
   └── build/css/variables.css    (compiled by design-token-pipeline U1)
        │
   ┌────┴──────────────────────────────────┐
   │ registry/                              │  ← THIS skill scaffolds:
   │   registry.json                        │     - registry.json (the index)
   │   <item>.tsx source files              │     - one registry-item per component/block/token-style
   └────┬──────────────────────────────────┘
        │  ◇ npx shadcn build  (validates + flattens)
        ▼
   public/r/*.json   (one flat JSON per item; the wire format)
        │  ◇ host it (static / Vercel / GitHub raw / any HTTP)
        ▼
   consumed by ANY project:
   npx shadcn add https://your-registry.com/r/button.json
   — or namespaced —  components.json { "registries": { "@you": "https://your-registry.com/r/{name}.json" } }
                       npx shadcn add @you/button
        │
        ▼
   lands components + cssVars into the consuming project (uiux-surface-builder U3 pulls these)
```

## 2. The Two Schemas

### 2.1 `registry.json` — the index (one per registry)

```json
{
  "$schema": "https://ui.shadcn.com/schema/registry.json",
  "name": "acme",
  "homepage": "https://acme.com",
  "items": [
    { "name": "button",  "type": "registry:ui",    "title": "Button",  "description": "Primary action button.",
      "files": [{ "path": "registry/ui/button.tsx", "type": "registry:ui" }],
      "dependencies": ["@radix-ui/react-slot"], "registryDependencies": [] },
    { "name": "use-toast", "type": "registry:hook", "title": "useToast",
      "files": [{ "path": "registry/hooks/use-toast.ts", "type": "registry:hook" }] }
  ]
}
```

Top-level fields: `$schema` · `name` · `homepage` · `items[]` · optional `include[]` (compose nested registries).

### 2.2 Per-item fields (each object in `items[]`, or its own `registry-item.json`)

| Field | Purpose |
|---|---|
| `name` | Item id → resolves to `/r/<name>.json` and `@registry/<name>` |
| `type` | `registry:ui` · `registry:component` · `registry:block` · `registry:lib` · `registry:hook` · `registry:style` (whole design system) · `registry:page`/`registry:file` |
| `title` / `description` | Human metadata |
| `files[]` | `{ "path": "...", "type": "...", "target"?: "..." }` — `target` overrides install destination |
| `dependencies[]` | npm packages to install (e.g. `["zod","@radix-ui/react-slot"]`) |
| `registryDependencies[]` | other registry items to pull first — shadcn names (`"button"`) OR full URLs to cross-registry items |
| `cssVars` | `{ "theme": {...}, "light": {...}, "dark": {...} }` — **where your design tokens ride along** (§4) |
| `css` | raw CSS / `@layer` rules to merge into the consumer's stylesheet |
| `tailwind` | Tailwind config extensions (legacy v3 consumers) |

> **`type: "registry:style"`** is the one-command full-system distributor: it bundles cssVars + tailwind
> + a set of `registryDependencies`, so `shadcn add @you/your-style` installs your ENTIRE design system
> (tokens + base components) into a fresh project in a single command. This is the "ship the whole chassis"
> button the UPGRADE-MAP calls "复用自有设计系统".

## 3. Build + Host + Consume (concrete CLI)

> **Cross-platform note (Windows/win32)**: every command below is `npx`/`pnpm dlx` and runs identically
> in PowerShell and Bash. Use the project-local CLI; do not install shadcn globally.

### 3.0 Init (in the registry-host project)
```bash
npx shadcn@latest init           # creates components.json (the registry host can itself be a Next.js app)
# pnpm:  pnpm dlx shadcn@latest init
```

### 3.1 Author the registry
Scaffold `registry.json` + put each component's source under `registry/<type>/<name>.tsx`.
Copy the template from `templates/shadcn-registry/` (see §6) and fill in your items.

### 3.2 Build (validate + flatten)
```bash
npx shadcn@latest build                      # reads registry.json → writes public/r/*.json
npx shadcn@latest build --output ./static/r  # custom output dir
# pnpm:  pnpm dlx shadcn@latest build
```
`build` validates every item against the schema and emits one flat JSON per item (the wire format).
If `build` is missing, the fix is `npx shadcn@latest` (the CLI ships `build`) — do not assume it exists.

### 3.3 Host the `public/r/` directory over HTTP
Any static host works — the registry is just JSON files:
- **Vercel / Netlify**: deploy the host project; `public/r/*.json` is served at `https://<domain>/r/<name>.json`.
- **GitHub (no deploy)**: commit `public/r/` and serve via raw URL `https://raw.githubusercontent.com/<org>/<repo>/<branch>/public/r/<name>.json`.
- **Local dev**: `next dev` → `http://localhost:3000/r/<name>.json`.
- **Private registry**: shadcn supports auth headers / query tokens in the registry URL for gated access
  (e.g. `https://reg.acme.com/r/{name}.json?token=${REGISTRY_TOKEN}`) — keep the token in an env var, never commit it.

### 3.4 Consume from any project
```bash
# Direct URL (no config):
npx shadcn@latest add https://acme.com/r/button.json

# Namespaced (recommended for repeated use) — add once to the consumer's components.json:
#   { "registries": { "@acme": "https://acme.com/r/{name}.json" } }
# then:
npx shadcn@latest add @acme/button
npx shadcn@latest add @acme/dashboard-block

# Register a namespace via CLI instead of editing components.json by hand:
npx shadcn@latest registry add @acme=https://acme.com/r/{name}.json

# Ship the WHOLE design system into a fresh project (registry:style item):
npx shadcn@latest add @acme/acme-style
```
`{name}` in the namespace URL resolves to the per-item file (`@acme/button` → `…/r/button.json`).

## 4. Wiring to design-token-pipeline (U1) — tokens + components ship together

The registry's `cssVars` field is the bridge: when a consumer runs `shadcn add @you/<item>`, shadcn
merges those vars into the consumer's `:root` / `.dark`. Keep them in sync with the U1 token build so a
single install delivers both the component AND its design tokens.

**Pattern A — author a `registry:style` item whose `cssVars` mirror the U1 semantic layer:**
```json
{
  "name": "acme-style",
  "type": "registry:style",
  "title": "Acme Design System",
  "cssVars": {
    "theme":  { "--radius": "0.625rem", "--font-sans": "Geist, sans-serif" },
    "light":  { "--background": "oklch(1 0 0)", "--primary": "oklch(0.62 0.19 260)" },
    "dark":   { "--background": "oklch(0.14 0 0)", "--primary": "oklch(0.70 0.16 260)" }
  },
  "dependencies": ["tailwindcss"],
  "registryDependencies": ["button", "card", "input"]
}
```
> These `--background` / `--primary` / `--radius` names are exactly shadcn's expected CSS-var contract.
> Map your U1 **semantic** tokens (`color.action.primary`, `radius.card`) onto these shadcn names — do it
> ONCE here so every consuming project gets the same theming.

**Pattern B — keep cssVars generated, not hand-maintained:** have the U1 build emit a snippet of shadcn-named
vars (a small Style Dictionary `css/variables` platform with `selector: ":root"` + a `.dark` platform), and
paste/automate that into the `registry:style` item's `cssVars`. The U1 CI guard (`git diff --exit-code build/`)
then also protects the registry's token values from drift.

| U1 output | Registry field | Effect on consumer |
|---|---|---|
| `build/css/variables.css` (`:root` + `[data-theme="dark"]`) | `cssVars.light` / `cssVars.dark` | install merges tokens into consumer theme |
| semantic token names | shadcn var names (`--primary`, `--background`, `--radius`) | one mapping, reused everywhere |
| `--duration-*` / `--ease-*` (motion tokens) | `cssVars.theme` | motion-engineering recipes in consumer read them |

## 5. CI for the registry
```bash
# package.json scripts (host project)
# "registry:build": "shadcn build",
# "registry:check": "shadcn build && git diff --exit-code public/r/"
```
`git diff --exit-code public/r/` fails CI if someone hand-edits a flattened `/r/*.json` instead of the
source `registry.json` — same source-of-truth discipline as U1's token build.

## 6. Template scaffold
A ready-to-fill scaffold lives at `~/.claude/templates/shadcn-registry/`:
```
templates/shadcn-registry/
├── README.md                 # how to copy + fill + build + host + consume
├── registry.json             # index with example ui / block / hook / style items (placeholders)
├── registry/
│   ├── ui/button.tsx         # example registry:ui item source
│   ├── blocks/stat-card.tsx  # example registry:block item source
│   └── hooks/use-mounted.ts  # example registry:hook item source
├── components.example.json   # consumer-side namespaced-registries snippet
└── package.example.json      # registry:build / registry:check scripts
```
Copy it into your registry-host project, replace `acme`/placeholders with your names, point `cssVars` at
your U1 tokens, then `npx shadcn build`.

## 7. Hard Rules
- ✅ **Source of truth = `registry.json` + the source files.** `public/r/*.json` are build artifacts — never hand-edit.
- ✅ Run `npx shadcn build` after any item change; guard `public/r/` with `git diff --exit-code` in CI.
- ✅ Map design tokens to shadcn's var contract **once** (in a `registry:style` `cssVars`), sourced from U1.
- ✅ For private registries, put the access token in an env var inside the registry URL — **never commit it**.
- ✅ Always emit the install/build command before assuming the CLI is present (`npx shadcn@latest …`).
- ❌ Do not design components here — that is L3 + `frontend-design` + `vercel:shadcn`.
- ❌ Do not compile tokens here — that is `design-token-pipeline`; this skill packages its output.
- ❌ Do not reach for an MCP server or a paid component host — the registry is free JSON-over-HTTP.
- ❌ Do not point consumers at the raw `registry.json` for install — they install the built `/r/<name>.json`.

## 8. References
- shadcn registry — Getting Started: https://ui.shadcn.com/docs/registry/getting-started
- registry.json schema: https://ui.shadcn.com/schema/registry.json
- registry-item.json schema: https://ui.shadcn.com/schema/registry-item.json
- Namespaced registries / components.json `registries`: https://ui.shadcn.com/docs/registry/namespace
- shadcn theming (CSS-var contract `--primary`/`--background`/`--radius`): https://ui.shadcn.com/docs/theming
- Pairs with: `design-token-pipeline` (U1 token source) · `uiux-surface-builder` (U3 consumer) · `vercel:shadcn`
