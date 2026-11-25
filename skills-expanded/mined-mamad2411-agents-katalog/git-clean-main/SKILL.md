---
name: git-clean-main
description: "Keep AI tooling files (.claude, .codex, .cursor, .windsurf, .augment, .kiro, .cline, .roo, .gemini, etc.) on dev branch but exclude them from main/master. Use when managing branches, creating PRs to main, merging to main, or setting up a repo's branch strategy for AI-assisted development. Triggers on git merge/PR operations targeting main or master."
agents: [claude, codex, cursor, windsurf, augment, kiro, cline, roo, gemini, amazonq, copilot, continue, aider, cody, devin, trae, junie, tabnine, bolt, v0, replit, codeium, aide]
---

# Git Clean Main

Branch strategy that keeps AI development artifacts on `dev` while maintaining a clean `main`/`master` free of AI tooling files.

## When to Use

Use this skill when:

- Creating a PR from `dev` to `main`/`master`
- Merging feature branches into `main`/`master`
- Setting up a new repo's branch strategy
- The user mentions keeping main clean or separating AI files

Do NOT use this skill when:

- Working entirely within `dev` or feature branches
- The project explicitly wants AI files in main

## The Problem

AI-assisted development generates tooling files that are valuable for development but don't belong in production branches:

```
# AI Agent Platforms
.claude/          ← Claude Code skills, commands, settings
.codex/           ← Codex/OpenAI configuration
.augment/         ← Augment Code
.devin/           ← Devin (Cognition AI)
.bolt/            ← Bolt.new
.v0/              ← Vercel v0
.replit/          ← Replit AI

# AI-Enhanced IDEs
.cursor/          ← Cursor editor state
.windsurf/        ← Windsurf (Codeium)
.trae/            ← Trae (ByteDance)
.kiro/            ← Kiro (Amazon)
.junie/           ← Junie (JetBrains)
.aide/            ← Aide IDE

# AI Coding Assistants
.cline/           ← Cline
.roo/             ← Roo Code
.continue/        ← Continue.dev
.cody/            ← Sourcegraph Cody
.aider/           ← Aider
.copilot/         ← GitHub Copilot
.tabnine/         ← Tabnine
.codeium/         ← Codeium
.gemini/          ← Google Gemini
.amazonq/         ← Amazon Q Developer

# Config & Rules Files
openspec/         ← OpenSpec change proposals and specs
skills-lock.json  ← Installed skills lock file
AGENTS.md         ← OpenAI Codex agent instructions
.cursorrules      ← Cursor rules
.cursorignore     ← Cursor editor ignore
.windsurfrules    ← Windsurf rules
.clinerules       ← Cline rules
.roomodes         ← Roo Code modes
.aider.conf.yml   ← Aider config
.aiderignore      ← Aider ignore
```

These files should live on `dev` where AI tools use them, but `main`/`master` should stay clean.

## Strategy

```
main/master ─────●────────●────────●──────── Clean (no AI files)
                 ↑        ↑        ↑
dev ─────●───●───●───●────●───●────●──────── Has AI tooling files
         │       │        │
feature/ ─┘       └────────┘                  Branch from dev
```

- `dev` is the primary working branch — all AI tooling files live here
- `main`/`master` receives clean merges with AI files excluded
- Feature branches are created from `dev` and merged back to `dev`

## Setup: `.gitignore` on `main`/`master`

On the `main`/`master` branch, add these entries to `.gitignore`:

```gitignore
# AI tooling (kept on dev, excluded from main)

# AI Agent Platforms
.claude/
.codex/
.augment/
.devin/
.bolt/
.v0/
.replit/

# AI-Enhanced IDEs
.cursor/
.windsurf/
.trae/
.kiro/
.junie/
.aide/

# AI Coding Assistants
.cline/
.roo/
.continue/
.cody/
.aider/
.copilot/
.tabnine/
.codeium/
.gemini/
.amazonq/

# Config & Rules Files
openspec/
skills-lock.json
AGENTS.md
.cursorrules
.cursorignore
.windsurfrules
.clinerules
.roomodes
.aider.conf.yml
.aiderignore
```

This ensures that even if AI files somehow get staged, they won't be committed on `main`.

## Setup: Merge Script

When merging `dev` → `main`, use this workflow to strip AI files:

```bash
#!/bin/bash
# merge-to-main.sh — Merge dev into main excluding AI tooling files

set -e

AI_FILES=(
  # AI Agent Platforms
  ".claude"
  ".codex"
  ".augment"
  ".devin"
  ".bolt"
  ".v0"
  ".replit"
  # AI-Enhanced IDEs
  ".cursor"
  ".windsurf"
  ".trae"
  ".kiro"
  ".junie"
  ".aide"
  # AI Coding Assistants
  ".cline"
  ".roo"
  ".continue"
  ".cody"
  ".aider"
  ".copilot"
  ".tabnine"
  ".codeium"
  ".gemini"
  ".amazonq"
  # Config & Rules Files
  "openspec"
  "skills-lock.json"
  "AGENTS.md"
  ".cursorrules"
  ".cursorignore"
  ".windsurfrules"
  ".clinerules"
  ".roomodes"
  ".aider.conf.yml"
  ".aiderignore"
)

# Switch to main and merge dev
git checkout main
git merge dev --no-commit --no-ff

# Remove AI tooling files from the merge
for item in "${AI_FILES[@]}"; do
  if [ -e "$item" ]; then
    git rm -rf --cached "$item" 2>/dev/null || true
    rm -rf "$item" 2>/dev/null || true
  fi
done

# Commit the clean merge
git commit -m "merge dev into main (AI tooling files excluded)"

# Switch back to dev
git checkout dev
```

## Setup: GitHub Actions (Optional)

For automated clean merges via CI:

```yaml
# .github/workflows/clean-merge.yml
name: Clean Merge to Main

on:
  workflow_dispatch:
  push:
    branches: [dev]

jobs:
  clean-merge:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/dev'
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Configure git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

      - name: Clean merge to main
        run: |
          git checkout main
          git merge dev --no-commit --no-ff || true

          # Remove AI tooling files
          AI_ITEMS=".claude .codex .augment .devin .bolt .v0 .replit"
          AI_ITEMS="$AI_ITEMS .cursor .windsurf .trae .kiro .junie .aide"
          AI_ITEMS="$AI_ITEMS .cline .roo .continue .cody .aider .copilot .tabnine .codeium .gemini .amazonq"
          AI_ITEMS="$AI_ITEMS openspec skills-lock.json AGENTS.md .cursorrules .cursorignore .windsurfrules .clinerules .roomodes .aider.conf.yml .aiderignore"
          for item in $AI_ITEMS; do
            git rm -rf --cached "$item" 2>/dev/null || true
            rm -rf "$item" 2>/dev/null || true
          done

          # Only commit if there are changes
          if ! git diff --cached --quiet; then
            git commit -m "merge dev into main (AI tooling excluded)"
            git push origin main
          fi

          git checkout dev
```

## PR Workflow

When creating a PR from `dev` to `main`:

1. **Create PR normally** — the PR will show AI files as changed
2. **Before merging**, ensure the target branch `.gitignore` excludes AI files
3. **After merge**, verify AI files are not present on `main`:
   ```bash
   git checkout main
   ls -la .claude .codex .augment .cursor .windsurf .cline .roo .kiro .gemini openspec skills-lock.json 2>&1
   # Should show "No such file or directory" for all
   ```

Alternatively, create the PR from a temporary clean branch:

```bash
# Create a clean branch from dev
git checkout -b clean/release-to-main dev

# Remove AI files
git rm -rf \
  .claude .codex .augment .devin .bolt .v0 .replit \
  .cursor .windsurf .trae .kiro .junie .aide \
  .cline .roo .continue .cody .aider .copilot .tabnine .codeium .gemini .amazonq \
  openspec skills-lock.json AGENTS.md .cursorrules .cursorignore .windsurfrules .clinerules .roomodes .aider.conf.yml .aiderignore \
  2>/dev/null
git commit -m "chore: remove AI tooling files for main merge"

# Push and create PR to main
git push origin clean/release-to-main
gh pr create --base main --title "chore: merge dev to main" --body "Clean merge excluding AI tooling files"
```

## Files to Exclude

| File/Directory | Purpose | Keep on dev | Exclude from main |
|---------------|---------|-------------|-------------------|
| **AI Agent Platforms** | | | |
| `.claude/` | Claude Code skills, commands, settings | Yes | Yes |
| `.codex/` | Codex / OpenAI configuration | Yes | Yes |
| `.augment/` | Augment Code | Yes | Yes |
| `.devin/` | Devin (Cognition AI) | Yes | Yes |
| `.bolt/` | Bolt.new | Yes | Yes |
| `.v0/` | Vercel v0 | Yes | Yes |
| `.replit/` | Replit AI | Yes | Yes |
| **AI-Enhanced IDEs** | | | |
| `.cursor/` | Cursor editor state | Yes | Yes |
| `.windsurf/` | Windsurf (Codeium) | Yes | Yes |
| `.trae/` | Trae (ByteDance) | Yes | Yes |
| `.kiro/` | Kiro (Amazon) | Yes | Yes |
| `.junie/` | Junie (JetBrains) | Yes | Yes |
| `.aide/` | Aide IDE | Yes | Yes |
| **AI Coding Assistants** | | | |
| `.cline/` | Cline | Yes | Yes |
| `.roo/` | Roo Code | Yes | Yes |
| `.continue/` | Continue.dev | Yes | Yes |
| `.cody/` | Sourcegraph Cody | Yes | Yes |
| `.aider/` | Aider | Yes | Yes |
| `.copilot/` | GitHub Copilot | Yes | Yes |
| `.tabnine/` | Tabnine | Yes | Yes |
| `.codeium/` | Codeium | Yes | Yes |
| `.gemini/` | Google Gemini | Yes | Yes |
| `.amazonq/` | Amazon Q Developer | Yes | Yes |
| **Config & Rules Files** | | | |
| `openspec/` | Change proposals, specs, designs | Yes | Yes |
| `skills-lock.json` | Installed skills versions | Yes | Yes |
| `AGENTS.md` | OpenAI Codex agent instructions | Yes | Yes |
| `.cursorrules` | Cursor rules | Yes | Yes |
| `.cursorignore` | Cursor editor ignore | Yes | Yes |
| `.windsurfrules` | Windsurf rules | Yes | Yes |
| `.clinerules` | Cline rules | Yes | Yes |
| `.roomodes` | Roo Code modes | Yes | Yes |
| `.aider.conf.yml` | Aider config | Yes | Yes |
| `.aiderignore` | Aider ignore | Yes | Yes |
| **Keep on Both** | | | |
| `CLAUDE.md` | Claude Code project instructions | **Keep** | **Keep** |

> **Note**: `CLAUDE.md` is typically kept on both branches as it serves as project documentation too. Exclude it only if you prefer.

## Recommended Scope

- **Scope**: Global (applies to any AI-assisted project)
- **Install**: `npx skills add skingford/skills --skill git-clean-main -g -y`
