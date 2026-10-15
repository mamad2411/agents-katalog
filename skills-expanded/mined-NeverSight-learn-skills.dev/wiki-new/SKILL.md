---
name: wiki-new
description: >
  Set up a new Obsidian knowledge base with the LLM Wiki pattern. Use when
  the user wants to create a wiki, second brain, personal knowledge base,
  initialize a vault, or says "onboard", "set up", "new wiki", or "new vault".
allowed-tools: Bash Read Write Glob Grep
---

# Personal Wiki — Onboarding Wizard

Set up a new Obsidian knowledge base using the LLM Wiki pattern. The LLM acts as librarian — reading raw sources, compiling them into a structured interlinked wiki, and maintaining it over time.

## Wizard Flow

Guide the user through these 3 steps. Ask ONE question at a time. Each step has a sensible default — the user can accept it or provide their own value.

### Step 1: Vault Name

Ask:
> "What would you like to name your knowledge base? This will be the folder name."
> Default: `second-brain`

Accept any user-provided name. This becomes the folder name and the title in the CLAUDE.md config.

### Step 2: Vault Location

Ask:
> "Where should I create it? Give me a path, or I'll use the default."
> Default: `~/Documents/`

Accept any absolute or relative path. Resolve `~` to the user's home directory. The final vault path is `{location}/{vault-name}/`.

### Step 3: Domain / Topic

Ask:
> "What's this knowledge base about? This helps me describe the vault's purpose."
>
> Examples: "AI research", "competitive intelligence on fintech startups", "personal health and fitness"

Accept free text. Use this to write a one-line domain description for the CLAUDE.md config.

## Post-Wizard: Scaffold the Vault

After collecting all answers, execute these steps in order:

### 1. Create directory structure

Run the onboarding script, passing the full vault path:

```
bash <skill-directory>/scripts/onboarding.sh <vault-path>
```

This creates all directories and the initial `wiki/index.md` and `wiki/log.md` files.

### 2. Generate CLAUDE.md

Read the template from `<skill-directory>/references/agent-configs/claude-code.md`.

Replace the placeholders:

- `{{VAULT_NAME}}` → the vault name from Step 1
- `{{DOMAIN_DESCRIPTION}}` → a one-line description derived from Step 3
- `{{WIKI_SCHEMA}}` → read `<skill-directory>/references/wiki-schema.md` and insert everything from `## Architecture` onward

Write the generated CLAUDE.md to the vault root.

### 3. Update wiki/log.md

Append the setup entry:

```
## [YYYY-MM-DD] setup | Vault initialized
Created vault "{{VAULT_NAME}}" for {{DOMAIN_DESCRIPTION}}.
```

### 4. Print summary

Show the user:

1. **What was created** — directory tree and CLAUDE.md
2. **Required next step** — install the Obsidian Web Clipper browser extension:
   > Install the Obsidian Web Clipper to easily save web articles into your vault:
   > https://chromewebstore.google.com/detail/obsidian-web-clipper/cnjifjpddelmedmihgijeibhnjfabmlf
3. **How to start** — open the vault folder in Obsidian, clip an article to `raw/`, then run `/wiki-ingest`

## Reference Files

These files are bundled with this skill and available at `<skill-directory>/references/`:

- `wiki-schema.md` — canonical wiki rules (single source of truth for CLAUDE.md config)
- `agent-configs/claude-code.md` — CLAUDE.md template

## Next Steps

After setup is complete, the user's workflow is:

1. **Clip articles** to `raw/` using the Obsidian Web Clipper
2. **Ingest sources** with `/wiki-ingest` — processes raw files into wiki pages
3. **Ask questions** with `/wiki-query` — searches and synthesizes from the wiki
4. **Health-check** with `/wiki-lint` — run after every 10 ingests or monthly
5. **Discover connections** with `/wiki-explore` — find cross-domain patterns
6. **Get inspired** with `/wiki-spark` — generate creative prompts from your wiki
