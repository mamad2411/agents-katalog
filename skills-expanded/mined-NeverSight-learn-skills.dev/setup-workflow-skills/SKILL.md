---
name: setup-workflow-skills
description: Sets up an `## Agent orientation` block in AGENTS.md/CLAUDE.md so the engineering skills know this repo uses Beads for issue tracking. Run before first use of `to-tasks`, `to-prd`, `tdd`, `improve-codebase-architecture`, or `zoom-out`.
disable-model-invocation: true
---

# Setup Workflow Skills

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker** — this workflow uses Beads. Setup auto-detects if it exists and flags a todo if it doesn't.
- **Agent orientation** — creates or updates the `## Agent orientation` block in AGENTS.md/CLAUDE.md to point to `CONTEXT.md` and `ISSUE_TRACKER.md`

This is a prompt-driven skill, not a deterministic script. Explore, check for Beads, present findings, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- Check if Beads CLI is available: `command -v bd`
- Look for Beads markers: `beads.config.json`, `beads/` directory, `.beads/` configuration
- `AGENTS.md` and `CLAUDE.md` at the repo root — does either exist? Is there already an `## Agent orientation` section in either?
- `ISSUE_TRACKER.md` at the repo root — does it already exist?
- `CONTEXT.md` or `CONTEXT-MAP.md` at the repo root (to determine single vs multi-context)

### 2. Present findings

Summarise what's present and what's missing. **Include the Beads setup status:**

- **Beads CLI available + project initialized** — Beads is ready. Proceed to write.
- **Beads CLI available + project not initialized** — Beads CLI is installed but `bd init` hasn't been run yet. The write phase will initialize it.
- **Beads CLI not available** — The Beads CLI needs to be installed. The write phase will install it and then initialize the project.

### 3. Determine context layout and confirm

Confirm the layout (this affects the Agent orientation block):

- **Single-context** — one `CONTEXT.md` + `docs/adr/` at the repo root. Most repos are this.
- **Multi-context** — `CONTEXT-MAP.md` at the root pointing to per-context `CONTEXT.md` files (typically a monorepo).

Then show the user a draft of the entire `## Agent orientation` block to add/update in whichever of `CLAUDE.md` / `AGENTS.md` is chosen (see step 4 for selection rules). 

The content comes from:
- **Single-context:** entire contents of [domain-single-context.md](./domain-single-context.md)
- **Multi-context:** entire contents of [domain-multi-context.md](./domain-multi-context.md)

Let them edit before writing.

**Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create — don't pick for them.

Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa) — always edit the one that's already there.

If an `## Agent orientation` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

**Then copy the template:**

- Copy [issue-tracker.md](./issue-tracker.md) → `ISSUE_TRACKER.md` at the repo root

**If Beads CLI is not available:**

Run the command:
```
curl -fsSL https://raw.githubusercontent.com/gastownhall/beads/main/scripts/install.sh | bash
```

This installs the Beads CLI system-wide.

**If Beads project initialization is needed:**

Run the command: `bd init --stealth --non-interactive`

This will create `beads.config.json` and the necessary Beads directory structure in this project.

### 4. Done

Tell the user the setup is complete. If Beads CLI was installed or the project was initialized, confirm what ran successfully. The `## Agent orientation` block is now in place, and downstream skills (`to-tasks`, `tdd`, etc.) will have the context they need.
