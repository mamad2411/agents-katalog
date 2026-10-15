---
name: plan-card
description: >
  Kanban card creation with codebase-informed Touch Points and conflict detection.
  Analyzes the codebase, scaffolds a card file, and adds it to the board via CLI.
  Works with any project that has docs/kanban/config.json.
  Usage: /plan-card "Add VTK 3D viewer for mesh visualization"
license: Apache-2.0
metadata:
  author: Dani
  version: "4.2"
  scope: [root]
allowed-tools: Read, Write, Glob, Grep, Bash, Task, AskUserQuestion
---

## Overview

`/plan-card "feature description"` creates a full Kanban card with codebase-informed Touch Points and conflict detection. It analyzes the codebase, scaffolds the card, and registers it on the board via the kanban CLI.

**CLI**: `npx tsx docs/kanban/cli/kanban.ts` (from project root)

**Full workflow:** `/plan-card "description"` → review card → `/sprint {ID}` → agent implements

---

## Step 0: Load project config

Read `docs/kanban/config.json`. Extract settings with these defaults:

| Setting | Config path | Default |
|---------|------------|---------|
| Project name | `project.name` | Git repo directory name |
| Main branch | `project.mainBranch` | `"main"` |
| Branch prefix | `project.branchPrefix` | `"feat/"` |
| Domains | `domains[]` | `[]` (use grep fallback) |
| Risk thresholds | `riskThresholds` | `{ "low": 400, "medium": 500 }` |
| Card ID style | `cardIdStyle` | `"SLUG_ONLY"` |
| Test command | `commands.test` | `""` |
| Browser dev commands | `commands.browserDev` | `{}` (empty object) |

**REQUIRED:** If `docs/kanban/config.json` does not exist, STOP immediately:

> Kanban board not initialized. Run `/kanban-init` first to set up the board,
> detect your main branch, and configure the project.

Do NOT proceed with defaults. Do NOT create config.json manually. The
`/kanban-init` skill handles detection (main branch, tech stack, domains) and
writes a correct config.

After loading config, validate critical fields:
- If `project.mainBranch` is missing/undefined: detect with
  `git symbolic-ref --short HEAD 2>/dev/null || echo main`
- If `project.branchPrefix` is missing/undefined: use `"feat/"`
- If `project.branchPrefix` does not end with `/`: append `/`

---

## Step 1: Parse input

Extract the feature description from the argument string.

If no argument is provided, ask the user: "What feature do you want to plan? Describe it in a sentence."

If the description is vague (< 3 words), ask clarifying questions before proceeding to codebase analysis.

---

## Step 2: Assign card ID

1. Check existing cards via CLI:
```bash
npx tsx docs/kanban/cli/kanban.ts list --json
```
Parse the response to get all existing card IDs across all columns (including done).

2. Derive an UPPERCASE slug from the description:
   - Extract key nouns/acronyms (e.g., "Add VTK 3D viewer" → `VTK-VIEWER`)
   - Use hyphens between words, max 3 words

**Card ID style** (from config `cardIdStyle`):
- `"PREFIX_SLUG"` → `P{N}-{SLUG}` (N = next available number)
- `"SLUG_ONLY"` → Just the slug (e.g., `KANBAN-PANEL`)

3. Verify uniqueness against the list response. If duplicate, the CLI will return a `DUPLICATE` error — propose an alternative slug and ask the user.

4. Check if a backlog card closely matches the description. If so, ask:
   - "Found existing backlog card: `{ID} — {TITLE}`. Create a new card, or promote this one?"
   - If promoting, use the existing ID.

---

## Step 3: Codebase analysis

Match keywords from the description against domains from `config.json`, then explore the relevant files to build the Touch Points table.

### Domain matching

Read the `domains[]` array from config. Each domain has:
- `keywords[]` — match against description (case-insensitive)
- `name` — domain label for reporting
- `globs[]` — files to explore

For each domain where any keyword matches the description, explore the glob patterns.

### Grep fallback (when no domain matches OR no domains configured)

Tokenize the description into significant words (skip common words: "add", "the", "a", "for", "with", "new", "to", "and", "or", "in"). For each token:
1. Grep the repo (skip `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `target/`)
2. Collect matching files, rank by match count
3. Take top 15 files

### Exploration process

For each matched file:

1. Glob to confirm it exists.
2. Read file headers (first 20 lines) + check line counts to understand scope.
3. Determine Action for each file:
   - **NEW** — file doesn't exist yet, will be created
   - **MODIFY** — existing file needs changes
   - **EVOLVE** — existing file gets substantially rewritten or renamed

### Risk assessment

Read `riskThresholds` from config (`low` and `medium` line counts).

| Condition | Risk |
|-----------|------|
| NEW files | None |
| MODIFY files < low threshold | LOW |
| MODIFY files between low and medium | MEDIUM |
| MODIFY files > medium threshold | HIGH (suggest splitting first) |

Build the Touch Points table with columns: Action, File, Risk, Lines.

---

## Step 4: Conflict detection

Check existing active cards for overlapping touch points:
```bash
npx tsx docs/kanban/cli/kanban.ts list --json
```

For each active card ID (not in done), read `docs/kanban/cards/{ID}.md` and parse its touch points table. Compare against new card's touch points.

### Conflict severity

| Condition | Severity |
|-----------|----------|
| Both cards mark same file as NEW | BLOCK — cannot work in parallel |
| Both cards MODIFY same file | WARN — add dependency note |
| One NEW + one MODIFY in same directory | CLEAR |
| No overlapping files | CLEAR |

Report the conflict status to the user as part of the card presentation.
If BLOCK conflict found, add dependency via `--dep` flag when registering.

---

## Step 5: Generate card

Load the card template. Resolution order:
1. `docs/kanban/assets/card-template.md` — project-specific template
2. The skill's own `assets/card-template.md` — generic fallback

Fill the template with:

- **CARD_ID**: From Step 2
- **TITLE**: Human-readable title derived from description
- **STATUS**: `BACKLOG` (default)
- **BRANCH**: `{branchPrefix}{lowercase-card-id}`
- **PRIORITY**: `P{N}` for PREFIX_SLUG style, `---` for SLUG_ONLY
- **DEPENDENCIES**: From conflict detection (Step 4), or `None`
- **SUMMARY**: 1-2 sentence description of the feature
- **CURRENT_STATE**: What exists today (from codebase exploration in Step 3)
- **SCOPE**: Numbered work streams derived from the analysis
- **TOUCH_POINTS**: Table from Step 3
- **ACCEPTANCE_CRITERIA**: Derived from scope items
- **VISUAL_VERIFICATION_STEPS**: When `commands.browserDev` exists and is non-empty, generate numbered steps using those commands. Each step should include: (1) a UI action to set up the state, (2) a screenshot or snapshot command, (3) what to look for in the result.
  - **Port**: Replace `{FRONTEND_PORT}` in browserDev commands with the worktree's assigned port (from sprint config), or `defaultPort` (1420) when running in the main repo.
  - **Cleanup**: The LAST step must ALWAYS be `npx agent-browser close` to release the port.
  - If `commands.browserDev` is not configured or empty: `_No browser dev mode configured._`
  - If the feature requires real PTY/backend to verify: note that browser dev mode has limited coverage and explain why.
- **MANUAL_VERIFICATION_STEPS**: Steps that need the real backend (PTY, native dialogs, clipboard, filesystem). If purely visual: `_All verification covered by browser dev mode above._`
- **AUTOMATED_TEST_STEPS**: If `commands.test` is non-empty, use it. If empty: `_No automated tests. Consider adding tests for: {suggest testable logic from scope}._`
- **DEFERRED**: Features explicitly out of scope for this card

Present the full rendered card to the user for review. Do NOT write any files yet.

---

## Step 6: User review

Ask the user with AskUserQuestion:
- **Write card** — Save to `docs/kanban/cards/` and register on board
- **Edit** — Apply changes first (ask what to change, re-present)
- **Cancel** — Discard and stop

If the user chooses "Edit", apply their requested changes to the card content and re-present. Repeat until they choose "Write" or "Cancel".

---

## Step 7: Write card + register on board

1. Write `docs/kanban/cards/{CARD_ID}.md` with the finalized card content.

2. Register on the board via CLI:
```bash
npx tsx docs/kanban/cli/kanban.ts add {CARD_ID} \
  --title "{TITLE}" \
  --column backlog \
  --branch "{branchPrefix}{lowercase-card-id}" \
  --priority "{PRIORITY}" \
  --dep "{DEP1},{DEP2}" \
  --description "{SHORT_DESCRIPTION}" \
  --short "{SHORT_ALIAS}" \
  --json
```

Verify `ok === true` in the response.

**Do NOT** create branches or worktrees here — that is `/sprint`'s job.

---

## Step 8: Commit + push to main

The card file and the board change MUST land on the main branch before the
user runs `/sprint`. Otherwise sprint creates the worktree from a main
branch that doesn't contain the new card.

1. Verify current branch is `{project.mainBranch}`:
   ```bash
   currentBranch=$(git symbolic-ref --short HEAD)
   ```

2. **If on the main branch**: commit and push silently.
   ```bash
   git add docs/kanban/cards/{CARD_ID}.md docs/kanban/board.json
   git commit -m "kanban: add {CARD_ID}"
   git push
   ```
   If `git push` fails (no remote, auth error), warn the user but do not
   fail the workflow — the card is on disk and on the board, the user can
   push manually.

3. **If on any other branch**: STOP and warn the user:
   > You're on `{currentBranch}`, not `{project.mainBranch}`. The card was
   > written and registered, but I did not commit it. Switch to
   > `{project.mainBranch}`, then run:
   >
   > ```bash
   > git add docs/kanban/cards/{CARD_ID}.md docs/kanban/board.json
   > git commit -m "kanban: add {CARD_ID}"
   > git push
   > ```
   >
   > Otherwise `/sprint {CARD_ID}` will create the worktree from a main
   > branch that doesn't contain this card.

   Do not auto-switch branches.

---

## Step 9: Report

```
Card created: {CARD_ID} — {TITLE}

  File:         docs/kanban/cards/{CARD_ID}.md
  Board:        Added to BACKLOG
  Touch Points: {N} files ({X} new, {Y} modify)
  Conflicts:    {CLEAR|WARN: details|BLOCK: details}

Ready to sprint? Run: /sprint {CARD_ID}
```

---

## Edge cases

| Scenario | Behavior |
|----------|----------|
| Card ID already exists | CLI returns DUPLICATE error — propose alternative slug |
| Backlog card matches description | Ask: promote existing or create new? |
| >15 Touch Points | Suggest splitting into 2 cards, ask user |
| Vague description (< 3 words) | Ask clarifying questions before exploring |
| BLOCK conflict found | Add dependency via `--dep` flag |
| No codebase matches for keywords | Card with minimal touch points + note "needs manual review" |
| User wants custom card ID | Accept any valid slug (uppercase, hyphens, 2-4 words) |
| Description matches multiple domains | Explore all matched domains, merge Touch Points |
| No config.json | STOP — tell user to run `/kanban-init` first |
| No card template in project | Use skill's own assets/card-template.md |
