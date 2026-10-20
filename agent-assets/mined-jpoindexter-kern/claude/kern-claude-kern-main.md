# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What Is KERN

KERN is a codebase intelligence and design system enforcement tool for AI coding assistants. It scans your codebase (25 scanners), generates context files for 8 AI tools, and serves design systems via MCP. The core is deterministic (no LLM calls): file lookup + regex checking + BM25 search.

**Two modes:** Codebase intelligence works with any project (no preset needed). Design system enforcement requires an active preset.

## Development Commands

```bash
pnpm install            # Install all dependencies
pnpm build              # Build all packages (turbo)
pnpm test               # Run tests (vitest, 245 tests)
pnpm lint               # Lint all packages (turbo)
pnpm type-check         # TypeScript validation (turbo)
pnpm clean              # Remove all build artifacts + node_modules
```

Pre-commit hooks auto-run on commit (secrets check + lint-staged). Conventional commits required: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`.

## Monorepo Structure

```
packages/
├── core/           → @usekern/core (token loading, BM25, rule engine, zod schemas)
├── mcp-server/     → @usekern/mcp-server (21 tools + 6 resources, stdio)
└── cli/            → @usekern/cli (23 commands, 25 scanners, 8 format generators)
presets/
├── swiss-industrial/ → @usekern/preset-swiss-industrial (flagship preset)
└── 7 more presets    → material-design-3, apple-glass, ibm-carbon, github-primer, linear, shopify-polaris, typescript-strict
apps/
└── web/            → usekern.dev (Next.js 15, Supabase, dashboard)
```

### CLI Package Layout

```
packages/cli/src/
├── commands/         → 23 CLI commands (check, fix, guard, init, scan, sync, activate, deactivate, context-inject, exception, login, logout, status, telemetry, presets, push, install, docs, watch, transform, review, create, migrate)
├── scanners/         → 25 codebase scanners (framework, components, hooks, imports, etc.)
├── formats/          → 8 output format generators (AGENTS.md, CLAUDE.md, .cursorrules, etc.)
├── generator.ts      → Core AGENTS.md generator (universal format)
├── types.ts          → Aggregate ScanResult type
└── utils.ts          → Shared CLI utilities
```

### MCP Server Layout

```
packages/mcp-server/src/
├── tools.ts          → 6 design system tools (kern_system, kern_suggest, kern_component, etc.)
├── codebase.ts       → 6 codebase intelligence tools (kern_scan_project, kern_file_context, etc.)
├── scan.ts           → kern_scan tool (visual scan)
├── presets.ts        → kern_presets + kern_init tools
├── snapshots.ts      → 4 snapshot management tools
├── scraper.ts        → 2 web scraping tools
├── resources.ts      → 6 MCP resources
└── index.ts          → Server entry point, tool registration
```

## Repository Structure

- `architecture/INDEX.md` — Table of contents with implementation reading order.
- `architecture/PRODUCT.md` — Original monolithic spec (6,320 lines, kept as archive).
- `spec/KERN.md` — The KERN.md file format standard (what end users create).
- `CONTINUATION-PROMPT.md` — Summary of all decisions made, for resuming work in new sessions.

## Architecture Documentation

The spec is split into 13 focused documents in `architecture/`. Read in this order for Phase 1:

| #   | Document                                                                  | What to find there                                              |
| --- | ------------------------------------------------------------------------- | --------------------------------------------------------------- |
| 01  | [01-vision.md](architecture/01-vision.md)                                 | Problem, insight, architecture bet, two products/one engine     |
| 03  | [03-preset-format.md](architecture/03-preset-format.md)                   | Preset structure, tokens.json, rules.json, mode.ts spec         |
| 04  | [04-mcp-server.md](architecture/04-mcp-server.md)                         | MCP tool specs, BM25 algorithm, **zod schemas** (copy directly) |
| 06  | [06-technical-architecture.md](architecture/06-technical-architecture.md) | Package structure, hashmark contract, Tailwind v3/v4            |
| 05  | [05-cli-commands.md](architecture/05-cli-commands.md)                     | kern init/check/fix/scan/sync internals                         |
| 12  | [12-security.md](architecture/12-security.md)                             | Path traversal, preset validation, threat model                 |

## Key Architecture Decisions

1. **KERN presets ARE themed shadcn** — no custom component code for MVP
2. **BM25 ranking** for `kern_suggest` (not embeddings, not naive keywords)
3. **MCP server via stdio** — AI tools launch KERN as subprocess
4. **mode.ts generated from tokens.json** — `kern init` / `kern sync --mode` regenerates it
5. **Typography: hardcoded Tailwind values** — baked at generation time, not CSS variables
6. **Spacing: values-only API** — CSS variable values for arbitrary Tailwind brackets (`p-[${mode.spacing[4]}]`)
7. **Zod schemas are the authority** — all tool responses validated with `.parse()` before returning
8. **Tailwind v3/v4 dual support** — v4 uses CSS `@theme` directive instead of `tailwind.config.ts`
9. **@usekern/ npm scope**, usekern.dev domain
10. **Swiss-Industrial is flagship preset** — derived from indx project DNA
11. **One scan, every tool** — 25 scanners run once, 8 format generators output context for all AI tools
12. **Cache-based MCP** — codebase intelligence tools read from `.kern/cache.json` (fast, no re-scanning)

## Design Patterns (Enforced Across All Projects)

- `mode` object for design tokens (`mode.color.bg.*`, `mode.typography.*`, `mode.radius`)
- OKLCH color space everywhere
- 8-point grid (4px base) — `p-3`, `p-5`, `p-7` are banned
- Template-first architecture: never build custom page layouts
- `cn()` for all className merging
- Existing components before building new ones
- UPPERCASE UI labels with `>` prefix on buttons
