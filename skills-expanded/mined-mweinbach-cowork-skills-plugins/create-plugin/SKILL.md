---
name: create-plugin
description: "Use when the user asks to create, author, scaffold, package, edit, or update a plugin — a bundle with a .cowork-plugin/plugin.json manifest that groups one or more skills and, optionally, MCP servers and app integrations. Triggers on: 'create a plugin', 'new plugin', 'author a plugin', 'edit a plugin', 'update a plugin', 'add a skill to a plugin', 'bundle these skills into a plugin', 'make a plugin.json', 'add an MCP server to a plugin'."
metadata:
  triggers: "create plugin, new plugin, author plugin, scaffold plugin, edit plugin, update plugin, plugin.json, cowork-plugin, bundle skills, mcp server plugin, package plugin"
---

# Create a plugin

A plugin is a directory with a `.cowork-plugin/plugin.json` manifest that bundles one or more
**skills**, and optionally **MCP servers** and **app integrations**. Plugins are discovered under
`<project>/.cowork/plugins/` and `~/.cowork/plugins/`. A plugin's bundled skills register as
`<plugin-name>:<skill-name>`.

## Manifest: the complete field set

`name` is the only required field; all others are optional. The manifest is **strict** — any key
not listed here makes the whole plugin fail to load. Full rules are in `references/schema.md`.

| Key | Purpose |
|-----|---------|
| `name` *(required)* | kebab-case plugin identifier |
| `version`, `description`, `license` | metadata |
| `author` | a string, or `{ name?, email?, url? }` |
| `homepage`, `repository` | URLs |
| `keywords` | array of strings |
| `skills` | path (or array of paths) to skills directories; default `./skills/` |
| `mcpServers` | **path** to a `.mcp.json` (default `./.mcp.json`) |
| `apps` | **path** to a `.app.json` (default `./.app.json`) |
| `interface` | UI metadata (`displayName`, `logo`, `category`, …) |

`mcpServers` and `apps` are **path strings**, never inline objects. Every declared path must
resolve **inside** the plugin root.

## Process

### 1. Decide what the plugin bundles
- **Skills** (the common case) — one or more `SKILL.md` directories.
- **MCP servers** — external tool servers, declared via a `.mcp.json` path
  (see `references/mcp-and-apps.md`).
- **Apps** — app integrations, declared via a `.app.json` path
  (see `references/mcp-and-apps.md`).

### 2. Choose the scope, then lay out the directory

**Decide scope first** — where the plugin is installed determines who can use it:

- **Global (user)** — `~/.cowork/plugins/`: available in every session.
- **Project** — `<project>/.cowork/plugins/`: available only in that project, and checked in so it
  travels with the repo.

Apply this rule:

- **In a chat (no project in context): always install the plugin as global** (`~/.cowork/plugins/`).
  Plugins created from a chat are global.
- **When working in a project: ask the user whether this should be a project plugin or a global
  one** — do not assume.

Then pick a **kebab-case** name (`^[a-z0-9]+(?:-[a-z0-9]+)*$`) and create the canonical layout under
the chosen plugins directory:

```
<plugin-name>/
├── .cowork-plugin/
│   └── plugin.json          # required manifest
├── skills/
│   └── <skill-name>/
│       └── SKILL.md         # one directory per bundled skill
├── .mcp.json                # optional (only if mcpServers is used)
└── .app.json                # optional (only if apps is used)
```

### 3. Write `.cowork-plugin/plugin.json`
`name` is the only required field. Add `description`, `version`, `author`, and an `interface` block
for good presentation. Set `skills` only to override the default `./skills/` path. Keep to the
fields in `references/schema.md` — the manifest is strict and rejects anything else. Copy from
`references/templates.md`.

### 4. Author each bundled skill
For every directory under `skills/`, write a `SKILL.md` by following the **`create-skill`** skill —
the same frontmatter rules apply (kebab-case `name` equal to the skill's directory name,
`description`, etc.). Invoke `create-skill` per skill rather than duplicating that guidance here.

### 5. Add MCP servers and/or apps (optional)
- For MCP servers: create a `.mcp.json` and set `"mcpServers": "./.mcp.json"`. Its exact format —
  stdio vs HTTP/SSE transports, auth, and how tools are namespaced as `mcp__<server>__<tool>` — is
  in `references/mcp-and-apps.md`. `mcpServers` is a path; the server map lives inside the
  `.mcp.json` file.
- For apps: create a `.app.json` and set `"apps": "./.app.json"`. Format in
  `references/mcp-and-apps.md`.

### 6. Validate — required before declaring done
Run the bundled validator against the plugin root and fix every error:

```bash
bun ~/.cowork/skills/create-plugin/scripts/validate-plugin.ts <path-to-plugin-root>
```

(Adjust the script path if installed in another tier.) It applies the same rules the loader applies:
strict manifest keys, kebab-case `name`, `mcpServers`/`apps` as path strings, every declared path
resolving **inside** the root, and each bundled `skills/*/SKILL.md` passing the skill checks. A
clean PASS means the plugin will load and its skills will register as `<plugin-name>:<skill-name>`.

### 7. If publishing through a marketplace, refresh source hashes
Marketplace catalogs may carry `sourceHash: "sha256:<64 hex chars>"` beside each plugin entry.
This is not a plugin manifest field. It belongs in `.agents/plugins/marketplace.json` and lets
Cowork detect opt-in updates without reinstalling automatically.

When editing a plugin in the `cowork-skills-plugins` marketplace repo:

1. Remove tracked provenance/noise from the published source root before hashing:
   `.cowork-plugin/install.json`, `.codex-plugin/install.json`, `.cowork-skill.json`, and
   `.DS_Store`.
2. Run the marketplace helper from the repo root:

   ```bash
   node scripts/update-source-hashes.mjs
   node scripts/update-source-hashes.mjs --check
   ```

3. Commit the plugin changes and the resulting `.agents/plugins/marketplace.json` hash update
   together. Do not hand-edit `sourceHash`; let the script compute it.

## Editing an existing plugin

To change a plugin, edit its files in place and re-validate:

1. **Locate it** under `<project>/.cowork/plugins/` or `~/.cowork/plugins/`.
2. **Edit the manifest** (`.cowork-plugin/plugin.json`). The schema stays strict — add only
   recognized keys (e.g. bump `version`, adjust `description` or `interface`); never introduce an
   unknown key.
3. **Add or remove a bundled skill** by creating or deleting a directory under `skills/`. Author any
   new `SKILL.md` with the `create-skill` skill; each skill's `name` must equal its directory name.
4. **Add or change MCP servers / apps** by editing `.mcp.json` / `.app.json` — or by creating the
   file and pointing `mcpServers` / `apps` at its path. See `references/mcp-and-apps.md`.
5. **On renaming.** Changing the manifest `name` changes how the plugin's skills are namespaced
   (`<name>:<skill-name>`); keep it kebab-case. Unlike a skill, a plugin's root directory name need
   not equal its `name`. Keep every declared path inside the root.
6. **Re-validate.** Run `scripts/validate-plugin.ts` against the plugin root and fix every error.
7. **Refresh marketplace hashes when applicable.** If the plugin is listed in
   `.agents/plugins/marketplace.json`, run `node scripts/update-source-hashes.mjs` and then
   `node scripts/update-source-hashes.mjs --check` from the marketplace repo root.

## Minimal manifest

```json
{
  "name": "my-plugin",
  "description": "What this plugin does.",
  "skills": "./skills/"
}
```

## Resources
- **`references/schema.md`** — the full `.cowork-plugin/plugin.json` format: every field, the
  `author`/`interface` sub-schemas, default paths, and the inside-root boundary rule.
- **`references/mcp-and-apps.md`** — bundling MCP servers (`.mcp.json`) and apps (`.app.json`):
  exact schemas, transports, auth, and worked examples.
- **`references/templates.md`** — minimal and full plugin layouts, copy-ready.
- **`scripts/validate-plugin.ts`** — the validator from step 6.
