# CLAUDE.md

**See [AI_RULES.md](./AI_RULES.md) for development standards and conventions.**

This project uses **bun** as the package manager and script runner (no lockfile is committed, so it isn't obvious from a glance). Use `bun run <script>` (e.g. `bun run dev`, `bun run build`, `bun run check`), not npm. Note that `bun run build` fires the `prebuild` hook, which runs four gates: `lint:i18n` (message-key naming), `lint:routes` (route pages compose primitives and components — see `docs/adr/0006-route-pages-compose.md`), `lint:ui` (primitive-first UI — see `docs/adr/0007-primitive-first-ui.md`) and `lint:api` (the generated API types match the backend contracts — see `docs/adr/0010-backend-contracts-generate-frontend-types.md`). Run a gate directly, e.g. `bun run lint:routes`, to see violations without a full build.

After changing a backend DTO or endpoint, rebuild the backend (`./mvnw package` rewrites each service's `openapi/openapi.yaml`) and run `bun run gen:api` in `anotame-web`; commit both.