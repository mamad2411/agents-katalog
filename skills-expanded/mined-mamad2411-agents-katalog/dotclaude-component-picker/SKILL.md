---
name: dotclaude-component-picker
description: Use when picking, vendoring, porting, or syncing agents, skills, commands, hooks, or rules from any upstream source (ECC = everything-claude-code, anthropic-skills, mcp-servers, wshobson/agents, or other external repos) into this dotclaude project's claudekit/ directory. Trigger on phrases like "pick X from ECC", "vendor this skill", "add agent from upstream", "port this component", "sync component from source", "import this hook", "bring in this rule from ECC", or any time the user references an upstream component to add to claudekit/. This skill covers the full 7-step pipeline: browse → evaluate → vendor → sidecar → preset → install → verify. Also trigger for upgrade or sync tasks ("check if X has updates", "sync X from upstream").
---

# dotclaude-component-picker

Full pipeline for picking a component from any upstream source and integrating it into `dotclaude`. Follow all 7 steps — each step's output feeds the next.

**Bundled references** (read when you need the full schema or deeper context):
- `references/sidecar.md` — sidecar schema, layout rules, dependency resolution, modify/upgrade workflows
- `references/presets.md` — preset schema, extends: semantics, settings_patch, install flags

---

## Upstream Sources

| Alias | Submodule path | Available component types |
|---|---|---|
| ECC | `upstream/everything-claude-code/` | agents, skills, commands, hooks, rules |
| anthropic-skills | `upstream/anthropic-skills/` | skills |
| mcp-servers | `upstream/mcp-servers/` | reference only |
| anthropic-cookbook | `upstream/anthropic-cookbook/` | reference only |

---

## Step 1 — Browse

First, bring the submodule to the latest remote state:

```bash
git submodule update --remote upstream/<alias>
```

Then survey what's available and what's already vendored:

```bash
# Available in upstream
ls upstream/<alias>/agents/
ls upstream/<alias>/skills/
ls upstream/<alias>/commands/
ls upstream/<alias>/hooks/

# Already vendored in claudekit
ls claudekit/agents/
ls claudekit/skills/
ls claudekit/commands/
ls claudekit/hooks/
```

Note: component name, whether it's a **folder** or **file** component, and whether it already exists in `claudekit/`. If it already exists, compare commits and decide whether to upgrade (see Upgrade workflow in `references/sidecar.md`).

---

## Step 2 — Evaluate

Read the component's primary documentation:
- **Skill folder**: read `SKILL.md` inside the folder
- **Agent / command / rule**: read the `.md` file
- **Hook**: read the script header / inline comments

Confirm before vendoring:
1. License is compatible — look for `LICENSE.txt` in the component folder or the upstream root
2. Not already vendored — if it is, compare commits (`pnpm sync <type>/<name>`) and decide whether to upgrade
3. External dependencies (python3, npm packages, binaries) — note them; they go in `dependencies.external`
4. Internal dependencies (other skills, hooks, agents this component requires) — note them; they go in `dependencies.required` or `dependencies.optional`

---

## Step 3 — Vendor

Get the upstream commit hash first — you need it for the sidecar:

```bash
git -C upstream/<alias> rev-parse HEAD
```

**Folder component** (skill with SKILL.md + assets, multi-file agent):
```bash
cp -r upstream/<alias>/<type>/<name>/ claudekit/<type>/<name>/
```

**File component** (single `.md` agent, single command, hook script):
```bash
cp upstream/<alias>/<type>/<name>.md claudekit/<type>/<name>.md
# or for shell scripts:
cp upstream/<alias>/<type>/<name>.sh claudekit/<type>/<name>.sh
```

---

## Step 4 — Sidecar

The sidecar records provenance and drives dependency resolution at install time. Read `references/sidecar.md` for the full schema — here's the quick version.

**Sidecar location:**
- **Folder component** → `SOURCE.yaml` **inside** the folder: `claudekit/<type>/<name>/SOURCE.yaml`
- **File component** → `<name>.source.yaml` **next to** the file: `claudekit/<type>/<name>.source.yaml`

**Minimal template** (see `references/sidecar.md` for all fields including tags/categories):

```yaml
# yaml-language-server: $schema=../../../presets/schema/sidecar.schema.json
source:
  repo: https://github.com/<org>/<repo>   # no trailing .git
  commit: <40-char-hex>                   # from `git -C upstream/<alias> rev-parse HEAD`
  path: <type>/<name>                     # path within upstream repo
  ref: main
imported_at: "<YYYY-MM-DD>"              # quoted — bare dates get parsed as Date objects
license: MIT
modified: false
modifications: null
notes: >-
  What the component does, key files, any quirks for future sync decisions.
dependencies:
  required:
    agents: []
    skills: []
    commands: []
    hooks: []
    rules: []
  optional:
    agents: []
    skills: []
    commands: []
    hooks: []
    rules: []
  external: []
tags: []
categories: {}
```

**External dependency format:**
```yaml
external:
  - name: python3
    type: system_binary       # npm | system_binary | python_pkg
    reason: "scripts/*.py require Python 3.9+"
  - name: claude
    type: system_binary
    reason: "calls claude -p via subprocess"
```

**After creating the sidecar**, verify it parses correctly:
```bash
pnpm typecheck
```

**If you later edit the vendored component**, set `modified: true` and add a `modifications:` description — this is how the sync tool knows the local copy diverges from upstream.

---

## Step 5 — Preset

Add the component to an existing preset or create a new one. Read `references/presets.md` for the full schema.

**Add to an existing preset** — edit the `.yaml` in `presets/`:
```yaml
components:
  skills:
    - <name>    # or agents:, commands:, hooks:, rules:
```

**Create a new preset** — copy an existing one as a template:
```bash
KIND=core   # or: framework, purpose
NAME=<preset-name>
cp presets/core/personal-baseline.yaml presets/$KIND/$NAME.yaml
cp presets/core/personal-baseline.md   presets/$KIND/$NAME.md
$EDITOR presets/$KIND/$NAME.yaml       # update name/kind/description/components/tags
```

Validate the preset:
```bash
pnpm validate <preset-name> --kind <core|framework|purpose>
```

---

## Step 6 — Install

```bash
# Into this project (.claude/ at repo root)
pnpm install:project <preset-name> --symlink --force

# Into user-level (~/.claude/)
pnpm install:user <preset-name> --symlink --force
```

`--force` overwrites in-place without creating `.bak` backups. `--symlink` keeps the installed component as a pointer back to `claudekit/` (edits to the source are immediately live).

> **Pitfall**: `pnpm install <preset>` is intercepted by pnpm as an npm install. Always use `pnpm install:project` or `pnpm install:user`.

If the preset has a `settings_patch` (e.g., hooks), the installer merges it into `.claude/settings.json` automatically. Check the result:
```bash
cat .claude/settings.json
```

---

## Step 7 — Verify

```bash
pnpm validate <preset-name> --kind <kind>
pnpm typecheck && pnpm test
```

Confirm the component exists at its expected target location:
- Project install: `.claude/<type>/<name>/` or `.claude/<type>/<name>.md` (symlink or copy)
- User install: `~/.claude/<type>/<name>/`

---

## Commit

One commit per vendor operation — keep them small and easy to revert:

```bash
git add claudekit/<type>/<name>/ presets/<kind>/<preset>.yaml presets/<kind>/<preset>.md
git commit -m "feat(<type>): vendor <name> from <upstream-alias>"
```

Conventional commits, English headers. Do not bundle multiple unrelated vendors in one commit.

---

## Upgrade an existing component

If a component is already in `claudekit/` and you want to pull upstream changes:

```bash
pnpm sync <type>/<name>          # shows diff between sidecar.commit and upstream HEAD
# Review diff, manually merge desired changes into claudekit/<type>/<name>/
# Then update sidecar: bump source.commit, set modified: true if diverged
pnpm typecheck && pnpm test
```
