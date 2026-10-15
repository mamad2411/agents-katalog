---
name: playcademy-update-standards
description: Fetch the latest Playcademy team standards and apply them to this repo's AGENTS.md. Handles first-time setup (creating AGENTS.md, integrating with existing agent files) and subsequent updates (replacing the team standards block in place). Run this whenever the team announces updated standards.
---

# Update Playcademy Standards

Fetch the latest Playcademy team standards from the canonical repo and apply them to this repo's `AGENTS.md`.

## Source of Truth

The standards live in the `superbuilders/playcademy-skills` repo under `standards/`.

Fetch them by running the colocated script:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/fetch-standards.sh
```

The output is the **standards content** — use it verbatim in the steps below.

If the script fails, it will print an error to stderr. The most likely cause is the developer needs to run `gh auth login`. Do not fall back to cached or hardcoded content.

## Workflow

### 1. Fetch the latest standards

Run the command from "Source of Truth" above and capture the output.

### 2. Check if setup has been done before

Look for `AGENTS.md` at the repo root and check whether it contains the markers:

```
<!-- playcademy:standards:start -->
<!-- playcademy:standards:end -->
```

- **Markers found** → go to step 4 (update path).
- **No markers or no file** → go to step 3 (setup path).

### 3. First-time setup

This step runs once per repo.

#### 3a. Survey existing agent files

Check for:

```
AGENTS.md
CLAUDE.md
.cursorrules
.cursor/rules/**
.github/copilot-instructions.md
.windsurfrules
CONVENTIONS.md
```

Read any that exist.

#### 3b. Create or integrate

**No existing agent files:**
Create `AGENTS.md` from the scaffold below.

**Existing `AGENTS.md` without Playcademy markers:**
Append the standards block (with markers) to the end of the file. Do not modify existing content.

**Existing `CLAUDE.md` but no `AGENTS.md`:**
`CLAUDE.md` is Claude-specific; `AGENTS.md` is the tool-agnostic team standard.

1. Create `AGENTS.md` from the scaffold below.
2. If `CLAUDE.md` has repo-specific content beyond what the standards cover, keep it and add `@AGENTS.md` as the first line so it inherits the standards. Explain this layering to the developer.
3. If `CLAUDE.md` only has generic instructions that the new `AGENTS.md` now covers, suggest the developer delete it — but do not delete it yourself.

**Other tool-specific files (`.cursorrules`, etc.):**
Leave them alone. Create `AGENTS.md` alongside them. Suggest the developer migrate to `AGENTS.md` over time, but don't do it for them.

After setup, continue to step 5.

### 4. Update existing standards

Replace everything between the markers (inclusive) with:

```markdown
<!-- playcademy:standards:start -->
## Playcademy Team Standards

These rules are shared across all Playcademy game repos. Do not remove or weaken them.

{fetched standards content}

<!-- playcademy:standards:end -->
```

Do not touch anything outside the markers.

### 5. Report

Tell the developer:
- Whether this was first-time setup or an update
- What changed (new file, updated section, no changes needed)
- If first-time: what existing files were found and how they were handled
- Remind them to review and commit

Do **not** commit the changes.

## Scaffold

When creating a fresh `AGENTS.md`:

```markdown
# AGENTS.md

Instructions for AI coding agents working in this repository.

<!-- playcademy:standards:start -->
## Playcademy Team Standards

These rules are shared across all Playcademy game repos. Do not remove or weaken them.

{fetched standards content}

<!-- playcademy:standards:end -->
```

The developer can add their own sections above or below the markers.
