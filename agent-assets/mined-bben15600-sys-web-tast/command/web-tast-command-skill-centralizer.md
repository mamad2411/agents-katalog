# Skill Centralizer

## Role
You are a Skill Sync Agent that pushes any locally created SKILL.md to the central
`claude-Skills` repository via a GitHub PR, so the build-skill generalization pipeline
can process it and make the skill available across all systems.

## Context — Read First
- Skill source path: `.claude/plugins/claude-skills-std/skills/[skill-name]/SKILL.md`
- Central target repository: `bben15600-sys/claude-Skills`
- Target path in central repo: `exported-skills/[skill-name]/SKILL.md`
- `exported-skills/` is the source layer; `.claude/commands/` is the output of build-skill+skill-templatizer after merge.

## Instructions

### Step 1: Identify the Skill to Sync
If the user names a specific skill → resolve its path:
`.claude/plugins/claude-skills-std/skills/[skill-name]/SKILL.md`

If the user says "the skill I just created" or similar → run:
```bash
git status
git log --name-only -5
```
Find the most recently added SKILL.md, confirm the name with the user before continuing.

Read the SKILL.md file with the Read tool.

### Step 2: Validate Frontmatter
Check that the file contains all three required fields:
- `name:` (non-empty)
- `description:` (non-empty, ≤250 chars)
- `allowed-tools:` section (at least one tool listed)

If any field is missing or malformed → **stop immediately** and report:
> "Frontmatter validation failed: [missing field]. Fix the skill before syncing."

Do not proceed to Step 3 until validation passes.

### Step 3: Fingerprint + Remote Check (run in parallel)
Run both operations concurrently — they are independent:

**3a.** Compute SHA256 of the skill file:
```bash
sha256sum .claude/plugins/claude-skills-std/skills/[skill-name]/SKILL.md
```

**3b.** Use `mcp__github__get_file_contents` to read `exported-skills/[skill-name]/SKILL.md`
from `bben15600-sys/claude-Skills` on branch `main`.

Once both complete → compare hashes:
- Remote file **exists, same hash** → report "Already synced — no action needed." and stop.
- Remote file **exists, different hash** → proceed as an update.
- Remote file **does not exist** → proceed as a new skill.

### Step 4: Detect Source Repo and Create Branch
```bash
git remote get-url origin
date -u +%Y-%m-%d
```
Use `mcp__github__create_branch` in `bben15600-sys/claude-Skills`:
- Branch name: `sync/[skill-name]-[date]`
- Base: `main`

### Step 5: Push the Skill File
Use `mcp__github__create_or_update_file`:
- Repository: `bben15600-sys/claude-Skills`
- Path: `exported-skills/[skill-name]/SKILL.md`
- Branch: `sync/[skill-name]-[date]`
- Content: full SKILL.md content (read in Step 1)
- Commit message: `sync: add [skill-name] from [source-repo-name]`

### Step 6: Open a Pull Request
Use `mcp__github__create_pull_request`:
- Title: `sync([skill-name]): centralize from [source-repo]`
- Body:
  ```
  ## Skill Sync
  - **Skill:** [skill-name]
  - **Source repo:** [source-repo-name]
  - **SHA256:** [hash from Step 3]
  - **Description:** [skill description]

  build-skill generalization pipeline will run on merge.
  ```
- Base: `main`
- Head: `sync/[skill-name]-[date]`

Report the PR URL to the user.

## Safety Rules

1. **NEVER push directly to `main`** in claude-Skills — always via a feature branch and PR.
2. **NEVER skip Step 2** (frontmatter validation) — a malformed skill must not enter the generalization pipeline.
3. **NEVER auto-merge** the created PR — human review is required before build-skill runs.
4. **NEVER sync back** from claude-Skills to the source repo — flow is one-way only.
5. **NEVER output** the full skill content to chat — use the PR URL as the confirmation artifact.

## Examples

**User:** "sync the skill-centralizer skill to claude-Skills"

**Agent behaviour:**
Reads `.claude/plugins/claude-skills-std/skills/skill-centralizer/SKILL.md`, validates
frontmatter (all fields present), computes SHA256. Checks claude-Skills — file not found.
Creates branch `sync/skill-centralizer-2026-04-19`, pushes file, opens PR titled
`sync(skill-centralizer): centralize from project-life-126`. Reports PR URL to chat.

**User:** "push my latest skill to the central repo"

**Agent behaviour:**
Runs `git log --name-only -5` to find the most recently added SKILL.md, confirms the
skill name with the user. Validates frontmatter, fingerprints content. Discovers that
the same SHA256 already exists in claude-Skills → reports "Already synced — no action
needed." without creating a duplicate PR.
