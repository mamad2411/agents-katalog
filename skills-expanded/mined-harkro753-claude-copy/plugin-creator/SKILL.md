---
name: plugin-creator
description: >
  Build, validate, and distribute Claude Code plugins — the packaged form of
  skills, agents, hooks, MCP/LSP servers, monitors and `bin/` executables, with
  a `.claude-plugin/plugin.json` manifest and optionally a `marketplace.json`
  catalog. Use this whenever the user wants to make, package, ship, share, or
  publish an extension: "turn this into a plugin", "make this a Claude
  extension", "package my skills", "publish to a marketplace", "share this with
  my team", "convert .claude/ into a plugin", "plugin.json", "marketplace.json",
  "/plugin install". Also use when a plugin already exists and something is
  wrong with it — components not loading, skills not showing up, hooks not
  firing, `claude plugin validate` failing. Reach for this even when the user
  says "skill" but describes distribution (versioning, install, teammates,
  GitHub), because that is a plugin, not a bare skill.
---

# plugin-creator — build and ship a Claude Code plugin

**In:** skills/agents/hooks you already have, or an idea for some.
**Out:** a directory that `claude plugin validate` passes, that loads under
`claude --plugin-dir`, and that a stranger can install.

A plugin is just a directory with a known shape. Almost everything that goes
wrong is the shape being slightly off, and the CLI will tell you — so the whole
job is: build the shape, run the validator, load it for real, fix what it says.

## First decide: does this need to be a plugin at all?

| | Standalone `.claude/` | Plugin |
|---|---|---|
| Invocation | `/hello` | `/my-plugin:hello` |
| For | one project, personal, experiments | sharing, versioning, reuse across projects |

If the user is customizing one repo for themselves, `.claude/skills/<name>/SKILL.md`
is the whole answer and a plugin is packaging they will never use — say so and
stop. Convert to a plugin when someone else has to install it.

Reach for `skill-creator` instead when the work is *authoring one skill's
content* (what it says, how it triggers, evaluating it). This skill is about the
container. They compose: write the skills with `skill-creator`, ship them with
this.

## The loop

Everything here is verifiable, so never hand-reason about whether a layout is
right — run the command.

```bash
claude plugin init <name> --with skills agents hooks   # scaffold (optional)
python3 scripts/preflight.py ./<path>                  # layout + sources
claude plugin validate ./<path> --strict               # manifest JSON
claude --plugin-dir ./<path>                           # load it for real
```

1. **Scaffold or lay out the directories.** `claude plugin init <name>` writes a
   working skeleton to `~/.claude/skills/<name>/` — which auto-loads next
   session as `<name>@skills-dir` with no install step, so it is the fastest way
   to iterate. `--with skills agents hooks mcp lsp output-style channel` adds
   examples of each. For a plugin that lives in a repo instead, create the
   directories yourself (layout below) — `init` always targets the skills dir.
2. **Write the manifest**, if you need one. It is optional: with no manifest,
   components are auto-discovered from default locations and the name comes from
   the directory. Add one when you want metadata (version, author, license) or
   non-default component paths.
3. **`claude plugin validate`.** Wrong-typed fields are errors; unrecognized
   fields are warnings that still load. Use `--strict` before publishing so a
   typo'd key (`skill` for `skills`) fails instead of silently doing nothing.
4. **Load it: `claude --plugin-dir ./<path>`.** Confirm skills appear under
   `/help`, agents under `/context`, and that hooks actually fire.

**`validate` is a manifest linter, not a plugin checker — this is the part that
catches people out.** Measured against the real CLI, all three of these pass
with exit 0:

- components nested inside `.claude-plugin/` (the plugin loads nothing)
- a marketplace entry whose `source` path does not exist (every install breaks)
- any component file being missing, malformed, or empty

And a plugin with a root `SKILL.md` and no manifest **fails** validation
(`No manifest found in directory`) even though it is valid at runtime. So a
green `validate` means "the JSON is well-formed", nothing more.

`scripts/preflight.py` covers exactly that gap — nesting, unresolvable
marketplace sources, missing `SKILL.md`, absent frontmatter, a manifest key
shadowing its default directory, `bun` hooks, hardcoded paths. Run it *and*
`validate`; they check disjoint things. Neither replaces loading the plugin, so
never report a plugin as working on the strength of either alone.
5. **Iterate with `/reload-plugins`** rather than restarting — it picks up
   skills, agents, hooks, and plugin MCP/LSP servers. Monitors need a restart.

Use `claude plugin details <name>` to see the component inventory and projected
token cost — the honest answer to "what does installing this actually cost the
user's context", which is worth checking before you ship something large.

## Layout

The one mistake worth memorizing: **only `plugin.json` goes inside
`.claude-plugin/`.** Every other directory sits at the plugin root. Components
nested under `.claude-plugin/` are silently not found — nothing errors, they
just never appear, which reads like "my skill doesn't work" rather than "my
directory is one level too deep".

```
my-plugin/
├── .claude-plugin/plugin.json   # manifest, and nothing else
├── skills/<name>/SKILL.md       # skills
├── agents/<name>.md             # subagents
├── hooks/hooks.json             # hooks
├── workflows/                   # workflow scripts
├── output-styles/ · themes/     # styles, colour themes
├── monitors/monitors.json       # background watchers
├── .mcp.json · .lsp.json        # MCP and LSP servers
├── bin/                         # executables added to Bash PATH
├── settings.json                # defaults (only `agent`, `subagentStatusLine`)
└── scripts/ · LICENSE · README.md · CHANGELOG.md
```

A plugin shipping exactly one skill can put `SKILL.md` at the root with no
`skills/` directory and no manifest field — it loads as a single-skill plugin,
named from the frontmatter `name`. Use `skills/` the moment there might be two.

Note `CLAUDE.md` at a plugin root is **not** loaded as context. Instructions
reach Claude through skills, agents and hooks — nothing else. Putting guidance
in a plugin `CLAUDE.md` is a common way to write documentation that never loads.

## The manifest

`name` is the only required field. It sets the namespace: every skill becomes
`/<name>:<skill>`, every agent `<name>:<agent>`.

```json
{
  "$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json",
  "name": "my-plugin",
  "displayName": "My Plugin",
  "version": "1.0.0",
  "description": "What it does — shown in the plugin manager",
  "author": { "name": "…", "email": "…", "url": "…" },
  "homepage": "…", "repository": "…", "license": "MIT",
  "keywords": ["…"]
}
```

**Set `version` deliberately.** With it, users only update when you bump it.
Without it, git-distributed plugins fall back to the commit SHA and *every
commit is a new version* — which turns routine pushes into update prompts for
everyone who installed it.

Full field list, component path fields and their replace-vs-extend rules, the
`${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_DATA}` variables, `userConfig`,
`defaultEnabled` and dependencies are in **`references/manifest.md`** — read it
when writing anything beyond the fields above.

## Components

Per-component specifics — hook events and the `hooks.json` shape, agent
frontmatter, MCP/LSP config, monitors, `bin/`, and the path-variable rules that
decide whether a bundled script can find itself — are in
**`references/components.md`**. Read it when adding a component type you have
not shipped before.

Two rules that cut across all of them, because they are the difference between a
plugin that works on your machine and one that works on anyone's:

- **Never hardcode a path to plugin files.** Use `${CLAUDE_PLUGIN_ROOT}` — the
  install directory differs per user and changes on every update. It resolves in
  skill and agent content, hook and monitor commands, and the documented fields
  of MCP and LSP servers.
- **Never write state into the plugin directory.** It is a versioned cache and
  the old version is deleted about two weeks after an update. Anything that must
  survive — installed dependencies, caches, generated files — goes in
  `${CLAUDE_PLUGIN_DATA}`.

## Distribution

A plugin becomes installable when it is listed in a marketplace: a repo with
`.claude-plugin/marketplace.json` naming the marketplace, its owner, and its
plugins with a `source` each (relative path, `github`, `url`, `git-subdir`, or
`npm`).

```bash
claude plugin validate .                      # validates marketplace.json too
claude plugin marketplace add ./path          # test locally first
claude plugin marketplace add owner/repo      # what your users will run
claude plugin install <plugin>@<marketplace>
claude plugin tag                             # git tag {name}--v{version}
```

Always add the marketplace from a local path and install from it before pushing
— it is the only way to catch a `source` that points somewhere wrong, and the
failure mode after publishing is everyone else's broken install.

The full marketplace schema, every `source` variant, `metadata.pluginRoot`,
private/team hosting, `renames` for when you rename or drop a plugin, and
version resolution are in **`references/marketplace.md`**.

## When something does not load

Work down this list before theorizing — in practice it is almost always the
first item:

1. **Directories inside `.claude-plugin/`?** Only `plugin.json` belongs there.
   `validate` will not catch this — it passes clean while nothing loads.
2. **`claude plugin validate --strict`** — a misspelled manifest key is a
   warning, not an error, so a plugin with a `skill` key loads and simply has no
   skills. `--strict` is what turns that into a failure (exit 1).
3. **Manifest key shadowing a default folder.** Declaring `commands`, `agents`,
   `workflows`, `outputStyles`, `themes` or `monitors` *replaces* the default
   directory. If both exist, the folder is ignored — `claude plugin list` warns.
   `skills` is the exception: it adds to the default scan.
4. **`claude plugin details <name>`** to see what actually got loaded, rather
   than what you believe you wrote.
5. **Hook not firing?** Check the command resolves under `${CLAUDE_PLUGIN_ROOT}`
   and that the interpreter exists on the target machine — the scaffold uses
   `bun`, which most users will not have. `node` or `python3` is the safer
   default for anything you distribute.
6. **Skill invisible but the plugin loads?** Plugin skills are namespaced.
   It is `/my-plugin:hello`, never `/hello`.

## Converting existing `.claude/` configuration

Copy `commands/`, `agents/` and `skills/` to the plugin root as-is. Hooks are
the one thing that moves: the `hooks` object from `settings.json` goes into
`hooks/hooks.json` — same format, new home.

Then remove the originals from `.claude/`. Project and user `.claude/agents/`
override same-named plugin agents, so the plugin's version stays dead until the
original is gone. Skills do not override — you get both `/name` and
`/plugin:name`, which is merely confusing rather than broken.
