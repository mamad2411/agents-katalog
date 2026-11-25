---
name: kos
description: Use this skill when the user wants to set up a new Kodex OS Layer 1 vault (the LLM Wiki layer) from scratch. Triggers include phrases like "set up kos", "create a new kos vault", "initialize my Kodex Wiki", or any first-time setup request. This skill walks the user through naming the vault, choosing a location, scaffolding the directory structure (raw/ with FL/FR/FS memo book conventions, wiki/ with all six subdirectories, output/), installing SCHEMA.md, and wiring up their AI agent. Do not use this skill if a vault already exists — use kos-ingest, kos-query, or kos-lint instead. Do not use for Layer 0 (Field Notes), Layer 2 (Notion), Layer 3 (Archive), or Layer 4 (Trello) setup.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
---

# KOS — Onboarding Wizard

Set up a new KOS vault: an Obsidian-compatible knowledge base implementing Kodex OS Layer 1. The LLM acts as librarian — reading raw sources, compiling them into a structured interlinked wiki, and maintaining it over time.

## Wizard Flow

Guide the user through these 5 steps. Ask ONE question at a time. Each step has a sensible default — the user can accept it or provide their own value.

### Step 1: Vault Name

Ask:
> "What would you like to name your knowledge base? This will be the folder name."
> Default: `kos-vault`

Accept any user-provided name. Validate: lowercase letters, digits, and hyphens only (kebab-case, per SCHEMA.md Section 6.1). If the user provides a name with spaces or capitals, suggest the kebab-case equivalent and confirm.

### Step 2: Vault Location

Ask:
> "Where should I create it? Give me a path, or I'll use the default."
> Default: `~/Documents/`

Accept any absolute or relative path. Resolve `~` to the user's home directory. The final vault path is `{location}/{vault-name}/`.

**Before proceeding:** check whether the resolved path already exists. If it does AND it contains a `SCHEMA.md` at its root, stop and tell the user:

> "There's already a KOS vault at this path. I won't overwrite it. If you want to start fresh, delete or move the existing folder first. If you want to work with the existing vault, use `/kos-ingest`, `/kos-query`, or `/kos-lint`."

Do NOT proceed with scaffolding if a vault is detected.

**3. How to start** — the Field Notes-aware workflow:

> Open the vault folder in Obsidian (File → Open Vault as Folder).
>
> When you're ready to add your first sources, create a folder under `raw/` for each Field Notes book you start transcribing:
>
> ```bash
>   mkdir -p raw/Field-Logs/FL-vol-001    # First Field Log book (daily log)
    mkdir -p raw/Field-Research/FR-vol-001    # First Field Research book (catchall)
    mkdir -p raw/Field-Studies/FS-vol-001    # First Field Study book (only when a subject earns one)
> ```
>
> Drop transcribed pages in as `page-001.md`, `page-002.md`, etc. Web clippings go anywhere under `raw/` — `raw/clippings/` is a common choice.
>
> Then run `/kos-ingest` and the LLM will process them into your wiki, creating matching `wiki/books/` pages automatically the first time it sees a new volume folder.
>
> **About archiving:** when a memo book is full and you place it in a Layer 3 archive envelope, mark its `wiki/books/<volume>.md` page with `status: archived` and optionally move it into `wiki/books/_archived/`. The `raw/<volume>/` folder is never moved or deleted — it stays as the immutable source. See SCHEMA.md Section 3.3 for the full archiving workflow.

### Step 4: Agent Config

Auto-detect which agent is running this skill:

| Detected via | Agent |
|---|---|
| Skill is being run by Claude Code | Claude Code |
| Environment indicates Codex | Codex |
| `.cursor/` exists in working directory | Cursor |
| `GEMINI.md` convention is in use | Gemini CLI |
| Otherwise | Ask the user |

State it clearly:
> "I'm running in **[Agent Name]**, so I'll generate a **[config file]** for this vault."

Then ask:
> "Do you use any other AI agents you'd like config files for? Options: Claude Code, Codex, Cursor, Gemini CLI — or skip."

Skip the agent that was auto-detected. Generate configs for all selected agents.

### Step 4.5: Existing or Fresh?

Ask:
> "Are you starting a fresh KOS vault, or do you already have an archive of Field Notes books with their own volume numbers?"
> 1. **Fresh** — I'm starting from scratch today
> 2. **Archived** — I have existing books with established volume numbers

If **Fresh**: the scaffolding script will pre-create `raw/FL-vol-001/` and `raw/FR-vol-001/` so the user has somewhere obvious to drop their first transcribed page. Skip `FS-vol-001/` since Field Study books only appear during Phase II — Data Extraction when a subject earns its own book.

If **Archived**: the scaffolding script will not pre-create any volume folders. The user already knows their volume numbers (e.g., they may be starting at `FL-vol-047`) and will create folders matching their existing books.

Pass the answer to `onboarding.sh` as a `--starter-mode=fresh` or `--starter-mode=archived` flag.

### Step 5: Optional CLI Tools

Ask:
> "These tools extend what the LLM can do with your vault. All optional but recommended:"
>
> 1. **summarize** — summarize links, files, and media from the CLI
> 2. **qmd** — local search engine for your wiki (helpful as it grows past ~100 pages)
> 3. **agent-browser** — browser automation for web research
>
> "Install all, pick specific ones (e.g. '1 and 3'), or skip?"

---

## Post-Wizard: Scaffold the Vault

After collecting all answers, execute these steps in order. If any step fails, stop and report — do NOT continue with a half-built vault.

### 1. Create directory structure and stub files

Run the onboarding script with the full vault path:

```bash
bash <skill-directory>/scripts/onboarding.sh <vault-path>
```

This creates:
- `raw/`, `raw/Field-Logs/`, `raw/Field-Research/`, `raw/Field-Studies/`, and `raw/assets/`
- `wiki/sources/`, `wiki/books/`, `wiki/entities/`, `wiki/concepts/`, `wiki/synthesis/`, `wiki/questions/`
- `output/`
- Stub `wiki/index.md` with all six section headers
- Stub `wiki/log.md`

Verify the script exits with status 0 before proceeding.

### 2. Install SCHEMA.md

Copy `<repo-root>/templates/SCHEMA.md` to `<vault-path>/SCHEMA.md`. This is the contract; without it, all other skills fail.

```bash
cp <skill-directory>/../../templates/SCHEMA.md <vault-path>/SCHEMA.md
```

(Adjust the path based on how skills resolve relative paths in the runtime environment. The `templates/` directory is at the KOS repo root, parallel to `skills/`.)

Verify the file copied successfully.

### 3. Generate agent config file(s)

For each selected agent, read the corresponding template from `<skill-directory>/references/agent-configs/` and write the rendered output:

| Agent | Template | Output File | Output Location |
|---|---|---|---|
| Claude Code | `claude-code.md` | `CLAUDE.md` | Vault root |
| Codex | `codex.md` | `AGENTS.md` | Vault root |
| Cursor | `cursor.md` | `kos.mdc` | `<vault>/.cursor/rules/` |
| Gemini CLI | `gemini.md` | `GEMINI.md` | Vault root |

Replace these placeholders in each template:

- `{{VAULT_NAME}}` → vault name from Step 1
- `{{DOMAIN_DESCRIPTION}}` → one-line description from Step 3
- `{{SCHEMA_PATH}}` → `./SCHEMA.md` (relative path from vault root)

The agent config templates must NOT embed SCHEMA.md's contents. They should reference it: "Read `./SCHEMA.md` for the full schema and operation rules." This keeps SCHEMA.md as the single source of truth — if the user edits SCHEMA.md, the agent picks up the change without the config drifting.

For Cursor specifically: ensure `<vault>/.cursor/rules/` exists before writing.

### 4. Append the setup entry to `wiki/log.md`

Use SCHEMA.md Section 3.9's format:

```markdown
## YYYY-MM-DD HH:MM — setup

- **Operation:** setup
- **Vault:** {{VAULT_NAME}}
- **Schema version:** 1
- **Agent configs:** CLAUDE.md, AGENTS.md (etc.)
- **Notes:** Vault initialized for {{DOMAIN_DESCRIPTION}}.
```

### 5. Install CLI tools (if selected)

For each tool the user selected in Step 5:

- summarize: `npm i -g @steipete/summarize`
- qmd: `npm i -g @tobilu/qmd`
- agent-browser: `npm i -g agent-browser && agent-browser install`

After each install, verify with `<tool> --version`. Report success or failure for each — installation failures should not abort the wizard, since the tools are optional.

### 6. Print summary and next steps

Show the user:

**1. What was created** — the directory tree, SCHEMA.md, and config files.

**2. Required next step** — install the Obsidian Web Clipper:

> Install the Obsidian Web Clipper to easily save web articles into your vault:
> https://chromewebstore.google.com/detail/obsidian-web-clipper/cnjifjpddelmedmihgijeibhnjfabmlf
>
> Configure it to save to: `<vault-path>/raw/`

**3. How to start** — the Field Notes-aware workflow:

> Open the vault folder in Obsidian (File → Open Vault as Folder).
>
> When you're ready to add your first sources:
>
> - **Daily log pages** (Field Log) go in `raw/Field-Logs/FL-vol-001/page-001.md`, etc.
> - **Research/catchall pages** (Field Research) go in `raw/Field-Research/FR-vol-001/`
> - **Subject study pages** (Field Study) go in `raw/Field-Studies/FS-vol-001/`
> - **Web clippings** go anywhere under `raw/` — `raw/clippings/` is a common choice.
>
> Then run `/kos-ingest` and the LLM will process them into your wiki.

---

## Reference Files

These files are bundled with this skill at `<skill-directory>/`:

- `scripts/onboarding.sh` — directory scaffolding and tool checks
- `references/agent-configs/claude-code.md` — CLAUDE.md template
- `references/agent-configs/codex.md` — AGENTS.md template
- `references/agent-configs/cursor.md` — Cursor rules template
- `references/agent-configs/gemini.md` — GEMINI.md template

Note: SCHEMA.md is NOT in this skill's references — it's at the repo root in `templates/SCHEMA.md`. There is one canonical schema, and it lives in `templates/`. The wizard copies it into each new vault during scaffolding (Post-Wizard Step 2).

---

## Next Steps

After setup, the user's workflow is:

1. **Capture** — write in Field Notes memo books (Layer 0)
2. **Transcribe & clip** — scan or transcribe pages into `raw/F[LRS]-vol-XXX/`; clip articles to `raw/`
3. **Ingest** — run `/kos-ingest` to process raw files into wiki pages
4. **Query** — run `/kos-query` to ask questions against the wiki
5. **Lint** — run `/kos-lint` after every ~10 ingests to catch gaps
