# Repo Referensi: google-labs-code/stitch-skills

Repo: https://github.com/google-labs-code/stitch-skills
Ref lokal: /Users/chaali0324/.agents/repo-refs/google-labs-code_stitch-skills
API: curl "localhost:27126/repos/readme?name=google-labs-code_stitch-skills"
Dibuat: 2026-09-16

## Cuplikan README
# google-labs-code/stitch-skills

Source: https://github.com/google-labs-code/stitch-skills
Fetched: 2026-09-16

## README
# Stitch Design Skills

A collection of agent skills and plugins for [Google Stitch](https://stitch.withgoogle.com), following the [Agent Skills](https://agentskills.io) open standard. Compatible with coding agents such as Codex, Antigravity, Gemini CLI, Claude Code, Cursor, and OpenCode (manual install).

## Quick Start

### 1. Install Plugins (Recommended)
The fastest way to set up the full Stitch plugin suite globally.

#### Codex

Add the Stitch Skills marketplace, then install the plugins you need.

<details open>
<summary><strong>Via CLI</strong> (recommended)</summary>

```bash
codex plugin marketplace add google-labs-code/stitch-skills --ref main \
  --sparse .agents/plugins \
  --sparse plugins/stitch-design \
  --sparse plugins/stitch-build \
  --sparse plugins/stitch-utilities
```

> [!TIP]
> The `--sparse` flags are optional — they limit the checkout to only the
> listed paths for a faster clone. Omit them to pull the entire repository.

</details>

<details>
<summary><strong>Via the Codex UI</strong></summary>

Navigate to **Settings → Plugin Marketplaces → Add** and fill in:

| Field | Value |
|---|---|
| **Source** | `https://github.com/google-labs-code/stitch-skills` |
| **Git ref** | `main` |
| **Sparse paths** | *(optional)* `.agents/plugins`, `plugins/stitch-design`, `plugins/stitch-build`, `plugins/stitch-utilities` |

</details>

Once the marketplace is registered, install any combination of:

- **`stitch-design`** — design-focused skills
- **`stitch-build`** — build and component skills
- **`stitch-utilities`** — utility and helper skills

#### Claude Code & Cursor

```bash
# Claude Code — installs into the current project
npx plugins add google-labs-code/stitch-skills --scope project --target claude-code
```

```bash
# Cursor — installs into the current workspace
npx plugins add google-labs-code/stitch-skills --scope workspace --target cursor
```

#### OpenCode

OpenCode does **not** use `npx plugins` / `npx skills` or the Codex/Claude marketplace layout.
Install skills and the Stitch MCP server manually:

**1. Skills** — copy the skill folders you need into a discoverable path:

```bash
# Project-local (recommended)
mkdir -p .opencode/skills
cp -R plugins/stitch-design/skills/generate-design .opencode/skills/generate-design
# repeat for other skills under plugins/*/skills/
```

OpenCode also discovers `.claude/s
