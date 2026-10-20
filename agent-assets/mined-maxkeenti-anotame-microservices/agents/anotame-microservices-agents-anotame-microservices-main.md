# AGENTS.md

**See [AI_RULES.md](./AI_RULES.md) for development standards and conventions.**

This project uses **bun** as the package manager and script runner (no lockfile is committed, so it isn't obvious from a glance). Use `bun run <script>` (e.g. `bun run dev`, `bun run build`, `bun run check`), not npm. Note that `bun run build` fires the `prebuild` hook, which runs the `lint:i18n` naming gate.