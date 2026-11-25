---
name: init
description: Initialize a wiki vault — set up the three-layer structure (raw sources, compiled wiki, schema) for an LLM-maintained knowledge base. Supports multiple named wikis.
argument-hint: '[wiki-name] [--reset to reconfigure]'
disable-model-invocation: true
---

User's request: $ARGUMENTS

# Initialize Wiki

You are setting up an LLM-maintained knowledge base following Karpathy's LLM Wiki pattern. Run this wizard step by step. **Use the `AskUserQuestion` tool for every question** — do not ask questions in plain text.

## Step 0: Check Existing Configuration

Run:

```bash
cat "$HOME/.wiki/config.json" 2>/dev/null || echo "NOT_CONFIGURED"
```

**If config exists and `--reset` was NOT passed:**

Parse the config. If it uses multi-wiki format (`wikis` key), list all configured wikis:

```
Existing wikis:
  personal  — /path/to/personal-vault
  testing   — /path/to/testing-vault (default)
```

Use `AskUserQuestion` to ask:

> You have <N> wiki(s) configured. What would you like to do?

Options: `Add a new wiki` / `Reconfigure an existing wiki` / `Cancel`

If the config uses the single-wiki format (`base_dir` key), show it and offer: `Add another wiki` / `Reconfigure` / `Cancel`.

**If NOT configured (or user chose to add/reconfigure):** proceed to Step 1.

## Step 1: Wiki Name

Use `AskUserQuestion` to ask for a name:

> What should this wiki be called?
>
> The name is used to switch between wikis (e.g., `/wiki:ingest --wiki testing <source>`).
> Use a short, descriptive kebab-case name.
>
> Examples:
> - **personal** — your own knowledge base
> - **testing** — testing patterns and runbooks
> - **research** — research papers and notes
> - **team** — shared team knowledge

If `$ARGUMENTS` already contains a name (e.g., `/wiki:init testing`), use that and skip this question.

If this is the first wiki being configured (no existing config), suggest "default" as the name.

Store as `wiki_name`.

## Step 2: Vault Location

Use `AskUserQuestion` to ask for the vault path:

> Where should the **<wiki_name>** wiki be stored?
>
> This is typically an Obsidian vault directory. All wiki pages, raw sources,
> and the schema (CLAUDE.md) will be created here.
>
> 1. **Default** (`~/.wiki/<wiki_name>/`)
> 2. **Custom path** (Please provide the full absolute path below)

**Logic:**
- If the user selects "Default", set `base_dir` to `$HOME/.wiki/<wiki_name>/`.
- If the user selects "Custom path" or provides a path directly, use that input.
- If the path contains `~`, expand it using `$HOME`.

Store the final result as `base_dir`.

## Step 2.5: Set as Default (only when adding to an existing config)

**Skip this step** if this is the first wiki being configured (no existing config) — the first wiki is always the default.

If there is an existing config with other wikis, use `AskUserQuestion` to ask:

> Should **<wiki_name>** be set as the default wiki?
>
> The default wiki is used when `--wiki` is not specified and `WIKI` env var is not set.
>
> Current default: `<current_default_wiki_name>` (`<current_default_path>`)

Options: `Yes, set as default` / `No, keep <current_default_wiki_name> as default`

Store result as `set_as_default` (`"default"` or `""`).

## Step 3: Confirm

Use `AskUserQuestion` to show a summary and ask for confirmation:

> Ready to initialize wiki vault:
>
>   Wiki name: `<wiki_name>`
>   Vault path: `<base_dir>`
>   Default wiki: `<yes — this will be the default | no — keeping <current_default> as default>`
>   Config file: `~/.wiki/config.json`
>
>   Three-layer structure:
>     raw/     — Immutable source documents (articles, papers, assets)
>     wiki/    — LLM-compiled pages (entities, concepts, sources, synthesis)
>     CLAUDE.md — Schema defining conventions and workflows
>
> Proceed?

Options: `Yes, apply` / `No, cancel`

If the user cancels, exit with "Configuration cancelled. Nothing was changed."

## Step 4: Apply

Call the helper script to create the vault structure:

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/setup-wiki.sh" "<base_dir>" "<wiki_name>" "<set_as_default>"
```

Pass `"default"` as the third argument if the user chose to set this wiki as default. Pass `""` otherwise.

This creates:
- `~/.wiki/config.json` (creates or merges into existing — preserves other wikis)
- `raw/` with subdirectories
- `wiki/` with subdirectories, `index.md`, and `log.md`

## Step 5: Generate Schema

Read the schema template at `${CLAUDE_PLUGIN_ROOT}/references/schema-template.md`.

Extract the CLAUDE.md content from the template (the fenced markdown block) and write it to `<base_dir>/CLAUDE.md`.

## Step 6: Done

Once everything succeeds, say:

```
Wiki "<wiki_name>" initialized.

  Vault path: <base_dir>
  Default: <yes | no — run /wiki:init <wiki_name> to change>
  Config file: ~/.wiki/config.json

  Structure:
    raw/           — Drop source documents here
      articles/    — Web articles, blog posts
      papers/      — Research papers, reports
      assets/      — Images, diagrams, data files
    wiki/          — LLM-maintained pages
      index.md     — Content catalog
      log.md       — Operations changelog
      entities/    — People, organizations
      concepts/    — Ideas, frameworks
      sources/     — Source summaries
      synthesis/   — Cross-cutting analysis
    CLAUDE.md      — Schema and conventions

Run /wiki:ingest <source> to add your first source document.

To target this wiki from any command:
  --wiki <wiki_name>              flag on any /wiki: command
  WIKI=<wiki_name>                env var (name lookup)
  WIKI=<base_dir>                 env var (direct path)
```
