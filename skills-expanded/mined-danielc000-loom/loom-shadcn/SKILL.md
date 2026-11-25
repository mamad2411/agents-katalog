---
name: loom-shadcn
description: Apply when a React + Tailwind project has a components.json (shadcn/ui's config file) — look up components via the mcp__shadcn tools before hand-writing UI, then add them with the project's own pinned CLI.
---

# loom-shadcn

Applies only when the project has a `components.json` at its root. If there is none, this skill
doesn't apply — don't run `shadcn init` on your own initiative.

1. **Look before you write.** Before hand-writing a UI primitive, use the `mcp__shadcn` tools
   (`list_items_in_registries`, `search_items_in_registries`, `view_items_in_registries`,
   `get_item_examples_from_registries`) to see what the project's registries already offer and how an
   existing component is built. The MCP is read-only — it never installs anything.
2. **Install with an explicit, pinned version — never `@latest`.** Match whatever version this
   project's own lockfile/package.json already pins for `shadcn`; if none exists yet, pick one explicit
   release and record it instead of floating on "latest". An unpinned CLI run resolves to whatever
   happens to be newest at that moment, silently.
3. **Dry-run before you write.** Prefer `shadcn diff`/`--dry-run` over blindly running the command the
   MCP's `get_add_command_for_items` tool returns, so you see what would change before committing to it.
4. **Stay inside the project's own registries.** Never `add` from a registry `components.json` doesn't
   already name — a third-party or `owner/repo` registry is an arbitrary code source — unless the task
   explicitly asks for it.
5. **Compose, don't fight the library.** See `references/rules.md` for the condensed implementation
   conventions (tokens, class-merging, spacing, variants, primitives, icons) and their attribution.

Component code only ever enters the repo through the CLI's own `add` command, run explicitly by you in
your normal shell — never through this skill's own loading.
