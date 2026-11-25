---
name: lore-plugins-reference
description: Supplies the canonical facts about the LoreAI plugin ecosystem (packages, CLI surface, config locations, port 3207, the OpenCode V2 incompatibility) so an agent answers from source instead of memory. Use when you need a verified fact about any @loreai/* package, lore CLI subcommand, Lore config file, or the plugin's V1/V2 status; not for taking actions.
spec_hash: da5359ebac31
---

# Lore Plugins Reference

This skill is the shared fact base for the lore-plugins skill family. It states
facts and points at their source. It takes no action and orchestrates nothing —
`lore-plugins` (manage) and `lore-plugins-explain` cite it instead of restating
what fact files already cover.

## Facts to state, with their sources

Report each of these from its source, never from memory:

- **Packages.** Lore publishes `@loreai/opencode`, `@loreai/pi`,
  `@loreai/core`, `@loreai/gateway`, and the legacy alias `opencode-lore`.
  Source: the loreai root `README.md`.
- **Database.** A local SQLite database at `~/.local/share/lore/lore.db`
  (with `-shm`/`-wal`) holds conversations, distillations, long-term memory,
  entities, and embeddings. Source: root `README.md`.
- **Curated knowledge.** `.lore.md` at the repo root is the human-readable,
  version-controlled export. Source: root `README.md`.
- **Gateway.** `lore run` / `lore start` serve the gateway on port 3207
  (env `LORE_LISTEN_PORT`, host `LORE_LISTEN_HOST`). Source: `lore --help`.
- **OpenCode plugin V1/V2 status.** `@loreai/opencode` 0.40.0 imports
  `@opencode-ai/plugin` and exports the V1 plugin function (`LorePlugin`,
  with a `config` hook). It is a V1-shape plugin and does not run in OpenCode
  V2. Source: `packages/opencode/src/index.ts`.
- **Entry module export shape.** `packages/opencode/src/index.ts` exports only
  `LorePlugin` plus a same-reference default; helpers live in `./internal.ts`
  because the V1 loader invokes every function export. Source: the WARNING
  comment at the top of `index.ts`.

## How to use it

Open the upstream files named above when the fact matters mid-task and you do
not already hold it verified. State the source alongside the fact; when the
installed `lore` CLI or on-disk file disagrees with the repository, report both
and prefer the installed reality, flagging the divergence.

See `references/component-map.md` for the full component, path, and env-var
table.**Never** mutate anything while operating under this skill — it only
supplies facts; the manage skill owns actions.
