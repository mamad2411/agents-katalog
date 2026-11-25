---
name: apply-template
description: Apply the ai-env agentic development environment template to the current repo, with intent-preserving merge for existing files
---

# Apply ai-env Template

Apply the agentic development environment template to the current repository.

**Argument:** optional path to ai-env clone. No argument = clone from GitHub (primary path).

---

## Phase 0 — Pre-flight

### Clean working tree check
Run `git status --porcelain`. If there are uncommitted changes, warn the user and ask whether to proceed or stash first. A dirty tree makes it hard to review what the template changed.

---

## Phase 1 — Source Resolution & Discovery

### Locate template source
1. If an argument was provided, use that path and verify it's a clean git checkout
2. If NO argument was provided, clone from GitHub:
   `git clone --depth 1 https://github.com/camacho/ai-env.git /tmp/ai-env-template` and use that
3. If the default local path `~/projects/camacho/ai-env` exists and no argument was given, prefer the GitHub clone (ensures latest version)
4. If all fail, tell the user and stop

### Read manifest
Read `apply-template.manifest.json` from the template source directory. This classifies every file as `copy_if_absent`, `smart_merge`, or `skip`.

### Scan target
Check which `copy_if_absent` and `smart_merge` files already exist in the current repo (cwd).

For `copy_if_absent` files that already exist in the target: these will be smart-merged (not skipped) to pick up any new template additions while preserving target customizations.

### Present plan
Show the user a summary:
```
Template Application Plan:
  Source: <path>
  Target: <cwd>

  Copy (new):        N files — <list>
  Smart merge (new): N files — <list of smart_merge files not in target>
  Smart merge (both): N files — <list of smart_merge files in both>
  Merge (existing copy_if_absent): N files — <list>
  Skipped:           N files (template-specific)

Proceed?
```
Wait for confirmation before continuing.

---

## Phase 2 — Copy

For each entry in `copy_if_absent`:
- **Directories** (entries ending with `/`): `mkdir -p` the target directory, then copy all files recursively. Skip individual files that already exist.
- **Files**: if the file does NOT exist in the target, copy it verbatim. If it exists, apply the same smart merge logic as Phase 3 (the file has diverged from template — preserve target intent while adding template additions).

Also ensure these directories exist even if empty:
- `ai-workspace/plans/`
- `ai-workspace/decisions/`

---

## Phase 3 — Smart Merge

For each file in `smart_merge`, read BOTH the template version and the target version (if it exists). If the target file doesn't exist, just copy the template version. If both exist, merge according to the rules below.

### AGENTS.md — Semantic Merge
- **Understand intent:** read both versions completely. Identify the purpose of each section.
- **Keep from target:** `## Stack`, `## Commands`, `## Architecture`, `## Gotchas` — preserve these sections entirely
- **Add from template if missing:** `## Agent Roles & Dispatch`, `## Protected Files`, `## Conventions`, `## Workflow Reference`, `## Context Loading Rules`
- **Resolve duplicates:** if both have a section with the same heading, favor the template version for structural/convention sections, favor the target for project-specific sections
- **Update:** the title line — replace the project name with the target repo's directory name
- **Preserve:** any custom sections the target has that aren't in the template
- **Cohesion check:** after merge, read the result and verify sections don't contradict each other

### tsconfig.json — Deep Merge
- **Start from template base** as the foundation
- **Deep merge `compilerOptions`:** overlay target's compilerOptions on top of template's. Target wins on collision.
- **Preserve from target:** `include`, `exclude`, `references`, and any other top-level keys
- **Inject if missing:** these strict options from the template: `strict`, `noUncheckedIndexedAccess`, `verbatimModuleSyntax`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `noFallthroughCasesInSwitch`
- **Surface conflicts:** if template and target have contradictory values for the same option (e.g., `strict: true` vs `strict: false`), present the conflict to the user for resolution
- **Cohesion test:** after merge, verify `compilerOptions` don't have contradictory flags (e.g., `module: "commonjs"` with `verbatimModuleSyntax: true`)

### .claude/settings.json
- **Preserve from target:** all existing `permissions.allow` and `permissions.deny` entries, `defaultMode`
- **Union merge:** `permissions.deny` arrays — add template entries not already present (deduplicate)
- **Union merge hooks:** for each hook event (PreToolUse, PostToolUse, etc.), keep all target hooks. Add template hooks only if no hook with the same `matcher` already exists in the target
- **Preserve:** any other keys the target has (disabledMcpjsonServers, enabledPlugins, etc.)

### package.json
- **Preserve from target:** `name`, `version`, `description`, `main`, `type`, `dependencies`, `repository`, `license`, `author` — everything except scripts and devDependencies
- **Merge scripts:** add any scripts from template that don't exist in target. Target wins on collision.
- **Merge devDependencies:** add packages from template that aren't in target's devDependencies (commitlint packages, lefthook, @biomejs/biome, typescript). Never remove or downgrade existing deps.
- **Add if missing:** `engines`, `packageManager`

### biome.json
- **Preserve from target:** all existing rules, `files` config, `formatter` config
- **Add if missing:** linter rules from template that don't exist in target
- **Never remove** any rule the target already has

### .gitignore
- **Union merge:** combine every unique line from both files, deduplicated
- **Preserve:** section comments (lines starting with `#`) and blank line groupings from both files
- **Order:** target's lines first, then new lines from template appended at the end under a `# ai-env template` comment

### skills-lock.json — Union Merge
- **Union merge `.skills` object:** combine all skill entries from both template and target. Each entry has `source` (git URL or local path, depending on `sourceType`), `sourceType` (`"git"` or `"local"`), and `computedHash` (SHA-256 integrity hash).
- **Template wins on conflict:** if the same skill name exists in both, use the template's entry (`source`, `sourceType`, `computedHash` all come from the template)
- **Never remove:** target skills not in the template are always preserved — projects may have custom skills
- **Top-level `version`:** keep the higher integer from either side (this is the lockfile schema version, not a skill version — individual skills do not have version fields)
- **Post-merge:** after writing the merged lockfile, instruct: "Run `npx skills install -a claude-code -a codex` to materialize any newly added skills for both agents"

Example merge logic:
```
Template:                                Target:
{ "version": 1, "skills": {             { "version": 1, "skills": {
    "validate": {                            "validate": {
      "source": "git@...ai-skills.git",       "source": "git@...ai-skills.git",
      "sourceType": "git",                     "sourceType": "git",
      "computedHash": "abc..."                 "computedHash": "abc..."
    },                                       },
    "reflect": {                             "custom-lint": {
      "source": "git@...ai-skills.git",       "source": "local",
      "sourceType": "git",                     "sourceType": "local",
      "computedHash": "def..."                 "computedHash": "xyz..."
    }                                        }
}}                                       }}

                    ↓ merged result:
{ "version": 1, "skills": {
    "validate":    { ... },  ← kept (same in both)
    "custom-lint": { ... },  ← preserved (target-only)
    "reflect":     { ... }   ← added from template
}}
```

### Directories: `.claude/agents/`, `.claude/rules/`, `.claude/skills/`
- **Recurse** into each directory
- **New files:** copy from template
- **Existing files:** apply semantic merge — understand the intent of both versions, preserve target customizations, add missing template sections

---

## Phase 4 — Post-Apply

1. Create `ai-workspace/.template-version` with content:
   ```
   version: <manifest version>
   applied: <ISO 8601 timestamp>
   source: <template source path>
   ```

2. **Dependency check:** if devDependencies were added to package.json, detect the package manager (pnpm-lock.yaml → pnpm, yarn.lock → yarn, package-lock.json → npm) and ask: "New devDependencies added. Run `<pm> install`?"

3. **Workflow warning:** if any `.github/workflows/` files were copied, check for the secret:
   ```bash
   if command -v gh &> /dev/null && gh secret list 2>/dev/null | grep -q "CLAUDE_CODE_OAUTH_TOKEN"; then
     # Secret exists — no warning needed
   else
     warn: "GitHub workflows added. You'll need to set CLAUDE_CODE_OAUTH_TOKEN as a repo secret (Settings → Secrets → Actions)."
   fi
   ```

4. **Hook warning:** if `.claude/settings.json` references hook scripts at `~/.claude/hooks/`, check if each script exists on disk. Warn about any missing ones.

5. **Dotfiles sync:** Ask the user if they want to install user-level configs:
   ```
   ai-env includes user-level configs for Claude and Codex (hooks, skills, profiles).
   Install them? Run: $AI_ENV_ROOT/dotfiles/sync.sh push
   (where $AI_ENV_ROOT is the template source directory)
   This copies dotfiles/claude/ → ~/.claude/ and dotfiles/codex/ → ~/.codex/
   ```
   If they agree, run `"$TEMPLATE_SOURCE/dotfiles/sync.sh" push` from the template source directory (not cwd).

6. **Auto-add post-setup todos via TodoWrite:**
   - "Update AGENTS.md — fill in Stack, Commands, Architecture, Gotchas for your project"
   - "Update .claude/agents/ descriptions to reference your project"
   - "Run `$TEMPLATE_SOURCE/dotfiles/sync.sh push` to deploy user-level configs (if not done above)"
   - "Review .claude/settings.json hooks and adjust paths for your environment"

7. **Summary:** print a list of all files created, merged, and skipped.

---

## Phase 5 — Context Migration (prompted, not automatic)

This phase scans for ALL existing AI context, memory, and configuration in the target repo and walks the user through migration interactively. **Never delete or overwrite context automatically** — every action requires explicit user confirmation.

### Discovery scan

Check ALL of the following locations. If **none** have content, skip this phase entirely with a message: "No existing AI context found — skipping migration."

**Project-scoped (in repo):**
- `ai-workspace/MEMORY.md` — project memory (check if it has content beyond the seed template)
- `ai-workspace/plans/` — existing plans (especially `.done.md` completed plans)
- `ai-workspace/decisions/` — existing ADRs
- `ai-workspace/scratchpad.md` — working notes
- `ai-workspace/workflow.md` — custom workflow (may differ from template)
- `.claude/skills/` — pre-existing skills (not from this template run)
- `.claude/agents/` — pre-existing agent definitions
- `.claude/rules/` — pre-existing rules
- `.claude/settings.json` — project permissions, hooks, deny rules
- `.claude/settings.local.json` — local-only overrides (not checked in)
- `.codex/config.toml` — Codex configuration with profiles
- `CLAUDE.md` — existing Claude instruction file
- `AGENTS.md` — existing universal instruction file
- `GEMINI.md` — Gemini-specific instructions (if present)
- `.cursorrules` or `.cursor/rules/` — Cursor-specific rules (if present)
- `.claudeignore` / `.codexignore` — existing context exclusions
- `.github/workflows/claude.yml` or `claude-code-review.yml` — existing CI workflows

**User-scoped (outside repo — read-only, inform user):**
- `~/.claude/projects/<path-encoded-cwd>/memory/` — Claude Code auto-memories for this project
  - Path encoding: replace `/` with `-`, e.g., `-Users-patrickcamacho-projects-myapp`
  - Each `.md` file has frontmatter with `name`, `description`, `type` (user/feedback/project/reference)
- `~/.claude/projects/<path-encoded-cwd>/MEMORY.md` — auto-memory index for this project
- `~/.claude/CLAUDE.md` — user's global instructions (may reference project patterns)
- `~/.claude/hooks/` — global hook scripts that project hooks may duplicate
- `~/.claude/agents/` — global agent definitions that project agents may shadow
- `~/.claude/commands/` — global slash commands (catchup, reflect, etc.)
- `~/.claude/plugins/` — installed plugins (check `enabledPlugins` in settings)

### Present findings

Show the user a categorized summary:
```
Context Migration — Found <N> items across <M> locations:

  Memory:
    - ai-workspace/MEMORY.md (42 lines, last updated 2026-03-15)
    - ~/.claude/projects/.../memory/ (6 files: 2 user, 2 feedback, 2 project)

  Plans & Decisions:
    - ai-workspace/plans/001-feature.done.md (completed, immutable)
    - ai-workspace/decisions/001-architecture.md

  Skills:
    - .claude/skills/deploy/SKILL.md (custom, not in template)
    - .claude/skills/validate/SKILL.md (CONFLICTS with template version)

  Agents & Rules:
    - .claude/agents/implementer.md (customized from template)
    - .claude/rules/feature-branches.md (matches template)

  Configuration:
    - .claude/settings.json (12 allow rules, 3 hooks, 2 deny rules)
    - .codex/config.toml (custom profiles: review, deploy)

  Instruction Files:
    - CLAUDE.md (project-specific, references @AGENTS.md)
    - AGENTS.md (customized — 5 sections differ from template)

  CI Workflows:
    - .github/workflows/claude.yml (existing, may need permission updates)

  User-scoped (informational):
    - ~/.claude/projects/.../memory/feedback_testing.md
    - ~/.claude/hooks/post-edit-format.sh (also referenced in project settings)
```

Wait for user to review before proceeding to migration steps.

### 1. Memory — ai-workspace/MEMORY.md

If both template and target have `ai-workspace/MEMORY.md` with real content:

**Merge strategy** (semantic, not line-by-line):
1. Read both files completely. The template MEMORY.md has this seed structure:
   ```markdown
   # Project Memory
   > Living document updated by /reflect after each task. 200-line limit.
   > Last updated: —

   ## Key Decisions
   ## Implementation Status
   ## Gotchas
   ```
2. Preserve ALL content from the target's MEMORY.md — this is accumulated project knowledge
3. If the target is missing sections from the template seed (Key Decisions, Implementation Status, Gotchas), add them as empty sections at the end
4. If the target has extra sections not in the template, keep them
5. Update the header comment to include the template's `> Living document...` line if missing
6. Present the merged result and ask the user to confirm

**If only target has content:** keep it, add missing template sections.
**If only template has content:** copy the seed template (fresh start).

### 2. Memory — Claude Code auto-memories (~/.claude/projects/)

These are user-scoped and managed by Claude Code's built-in memory system. They live outside the repo and are NOT migrated automatically. Instead, inform the user:

- List each memory file with its `name`, `type`, and `description` from frontmatter
- Explain: "These are Claude Code's per-project memories stored at `~/.claude/projects/.../memory/`. They persist across sessions and inform Claude's behavior for this project."
- Ask: "Are any of these stale or incorrect? I can flag them for your review but won't modify them during template application."
- If any `project` or `reference` type memories contain information that should be in `ai-workspace/MEMORY.md` instead (so other agents can see it), suggest the user move that content manually

### 3. Plans and decisions

- **Completed plans** (`*.done.md`): Always preserve — these are immutable records. Inform the user they exist.
- **Active plans** (no `.done.md` suffix): Ask if still in progress or should be marked done.
- **ADRs**: Always preserve — immutable after commit. Check if any reference patterns that the template changes (warn if so).
- **Templates** (`TEMPLATE.md`): Replace with template version if different (these are scaffolding, not content).
- **scratchpad.md**: If non-empty, ask user whether to preserve, archive, or reset.
- **workflow.md**: If target has a custom workflow that differs from template, present both and ask which to keep (or merge).

### 4. Skills

For each skill directory in `.claude/skills/`:

- **Not in template** (custom skill): Keep as-is. Inform user it's preserved.
- **Same name as template skill** (e.g., both have `validate/SKILL.md`):
  - Diff the two versions
  - Present the differences to the user
  - Options: keep target version, replace with template, or merge (user reviews merged output)
- **Template has new skills** not in target: These were already copied in Phase 2. Just inform the user.

### 5. Agents, rules, and commands

For each file in `.claude/agents/` and `.claude/rules/`:

- **Same file exists in both:** Diff them. If target has customizations (model changes, extra instructions, project-specific context), present the diff. Default: keep target version for agents (they're often customized), keep template version for rules (they're more structural).
- **New from template:** Already copied in Phase 2. Inform user.
- **Target-only (custom):** Preserve. Inform user.

Check for shadowing between global and project agents:
- If `~/.claude/agents/architect.md` and `.claude/agents/architect.md` both exist, note that the project version takes precedence.

### 6. Settings and permissions

For `.claude/settings.json`:
- This was already smart-merged in Phase 3. Summarize what was added/changed.
- Specifically call out:
  - **Hooks:** List which hooks exist in both global (`~/.claude/settings.json`) and project. Per the hook placement rule: global hooks = personal workflow, project hooks = codebase contract. Warn if the same hook appears in both (unnecessary duplication of expensive hooks).
  - **Deny rules:** Any new deny patterns from the template
  - **Allow rules:** Any new allow patterns (user should review these)
  - **Plugins:** If `enabledPlugins` or `disabledMcpjsonServers` are present, list them

For `.claude/settings.local.json`:
- Never touch. Inform user it exists and what it contains.

For `.codex/config.toml`:
- If target has custom profiles, preserve them. Merge any new template profiles that don't collide.

### 7. Instruction files (CLAUDE.md, AGENTS.md, GEMINI.md, .cursorrules)

- **AGENTS.md:** Already merged in Phase 3. Summarize what sections were added/preserved.
- **CLAUDE.md:** If target has a custom CLAUDE.md that doesn't just `@AGENTS.md`:
  - Read it. Identify project-specific instructions vs boilerplate.
  - Preserve project-specific content. Add template boilerplate sections if missing.
- **GEMINI.md:** If present, inform user. Template doesn't provide one — this is the user's custom file. Preserve.
- **.cursorrules:** If present, inform user that AGENTS.md is the preferred universal format. Ask if `.cursorrules` content should be merged into AGENTS.md or kept separately.

### 8. CI workflows

If `.github/workflows/claude.yml` or `claude-code-review.yml` existed before template application:
- Diff with template versions
- Call out permission differences (`contents: read` vs `write`, missing `allowed_tools`)
- Present upgrade path if target workflows have weaker permissions

### 9. Context exclusions (.claudeignore, .codexignore)

- `.claudeignore`: Handle separately from `.gitignore`. Check if target has one. If so, union-merge (same strategy as `.gitignore`). If not, copy template version.
- `.codexignore`: If present, preserve. Template doesn't provide one.

### Summary prompt

After presenting all findings, ask:
```
Ready to apply these migration decisions? (y/n)

You can also:
  - "skip" to skip migration entirely (all files from Phases 2-4 are already applied)
  - "details <item>" to see the full diff for any item above
```

**Key principle:** This phase is informational and advisory. The user has final say on every decision. Present what exists, explain what the template expects, and recommend — but never act without confirmation.

---

## Re-application

When running on a repo that already has `ai-workspace/.template-version`:
- `copy_if_absent` files are smart-merged if present (picks up template additions while preserving customizations)
- `smart_merge` files are always re-merged (this is how template updates flow)
- If the user passes `--force`, overwrite `copy_if_absent` files completely instead of merging
