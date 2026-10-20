# BMAD Plugin Project Conventions

## Runtime

This project uses **Bun** as its JavaScript runtime and package manager.
All scripts use `bun run <script>`. For local tooling (biome, tsc), use
`./node_modules/.bin/<tool>` — never npx or bunx.

## Available Scripts

| Script | Command | Description |
| --- | --- | --- |
| prepare | `bun run prepare` | Install husky git hooks |
| typecheck | `bun run typecheck` | Type-check all TypeScript (no emit) |
| lint | `bun run lint` | Biome lint + format check |
| lint:staged | `bun run lint:staged` | Biome lint + auto-fix staged files |
| validate | `bun run validate` | Upstream coverage validation (agents, skills, content, naming) |
| sync | `bun run sync` | Sync upstream content to plugin |
| sync:dry | `bun run sync:dry` | Dry-run sync (preview changes) |
| sync:source | `bun run sync:source <id>` | Sync a single upstream source |
| generate:agents | `bun run generate:agents` | Generate agent .md files from upstream YAML |
| generate:skills | `bun run generate:skills` | Generate SKILL.md files from upstream workflows |
| generate:manifest | `bun run generate:manifest` | Generate _shared/agent-manifest.csv from plugin agent files |
| sync-all | `bun run sync-all` | Run sync → generate:agents → generate:skills in sequence |
| bump-core | `bun run bump-core` | Bump plugin version for new core BMAD-METHOD release |
| bump-module | `bun run bump-module -- --source <id>` | Bump plugin version for new external module release |
| update-readme | `bun run update-readme` | Update README version badge |
| test | `bun run test` | Run tests |
| release | `./scripts/release.sh [version]` | Full release workflow (see Release below) |

## Upstream Sync

When upstream repos release new tags, sync them into the plugin:

```sh
# Core BMAD-METHOD release
bun run bump-core                       # fetch latest tag, bump to v<core>.0
bun run bump-core -- --tag v6.0.2       # pin to specific tag
bun run bump-core -- --dry-run          # preview only
bun run sync-all                        # sync + generate agents + generate skills

# External module release (tea, bmb, cis, gds)
bun run bump-module -- --source tea              # fetch latest tag, increment .X
bun run bump-module -- --source gds --tag v0.1.7 # pin to specific tag
bun run bump-module -- --source tea --dry-run    # preview only
bun run sync-all -- --source tea                 # sync + generate for one source

# Verify
bun run typecheck && bun run lint
```

Both bump scripts fetch tags, update the upstream version file, update all 4
plugin version files (.plugin-version, package.json, plugin.json, marketplace.json),
and update README badges. Core bumps reset .X to 0; module bumps increment .X by 1.

## Release

Run from **dev** branch with clean working tree:

```sh
./scripts/release.sh                  # release current version (full run)
./scripts/release.sh 6.0.0-Beta.9.0  # bump version first, then release
./scripts/release.sh --after-ci       # finish release after CI passes
```

Two phases: **prepare** (bump → beads sync → release branch → PR → wait for CI)
and **finish** (merge → tag → GitHub release → return to dev).

If CI is slow to register or fails, the script saves state to `.release-state`
and exits with instructions. Fix the issue, then `--after-ci` completes Phase 2.

## Git Workflow

- **main** is for releases only — never commit directly to main
- **dev** branch accepts PRs from feature branches
- PRs target **dev**, not main
- When merging PRs to dev: **do not squash** — preserve individual commits
- Releases: merge dev → main (unidirectional)
- One branch per module/story

## BMAD Agent Naming

Two distinct names for each agent:

| Term | Source | Example | Used for |
|------|--------|---------|----------|
| **Agent name** | Filename (without `.md`) | `quick-flow-solo-dev` | Invocation, delegation, code references |
| **Personnel name** | `name` field in frontmatter or heading | Barry | Documentation, user-facing display |

The agent name (filename) is the canonical identifier. Personnel names add personality but are optional in tables.

### Current Agents

| Agent (filename)        | Personnel  | Module | Role                         |
| ----------------------- | ---------- | ------ | ---------------------------- |
| analyst                 | Mary       | Core   | Business Analyst             |
| pm                      | John       | Core   | Product Manager              |
| ux-designer             | Sally      | Core   | UX Designer                  |
| architect               | Winston    | Core   | System Architect             |
| sm                      | Bob        | Core   | Scrum Master                 |
| dev                     | Amelia     | Core   | Developer                    |
| tea                     | Murat      | TEA    | Test Architect               |
| quinn                   | Quinn      | Core   | QA Engineer                  |
| tech-writer             | Paige      | Core   | Technical Writer             |
| quick-flow-solo-dev     | Barry      | Core   | Quick Flow Solo Dev          |
| bmad-master             | —          | Core   | Orchestrator                 |
| agent-builder           | Bond       | BMB    | Agent Building Expert        |
| module-builder          | Morgan     | BMB    | Module Creation Master       |
| workflow-builder        | Wendy      | BMB    | Workflow Building Master     |
| brainstorming-coach     | Carson     | CIS    | Brainstorming Facilitator    |
| creative-problem-solver | Dr. Quinn  | CIS    | Problem-Solving Expert       |
| design-thinking-coach   | Maya       | CIS    | Design Thinking Coach        |
| innovation-strategist   | Victor     | CIS    | Innovation Strategist        |
| presentation-master     | Caravaggio | CIS    | Presentation Expert          |
| storyteller             | Sophia     | CIS    | Master Storyteller           |
| game-architect          | Cloud Dragonborn | GDS | Principal Game Systems Architect |
| game-designer           | Samus Shepard | GDS | Lead Game Designer           |
| game-dev                | Link Freeman | GDS   | Senior Game Developer        |
| game-qa                 | GLaDOS     | GDS    | Game QA Architect            |
| game-scrum-master       | Max        | GDS    | Game Dev Scrum Master        |
| game-solo-dev           | Indie      | GDS    | Elite Indie Game Developer   |

## Automation First

Script everything repeatable — never do manually what a script can do.

- Full sync pipeline → `bun run sync-all [--source <id>]` (preferred)
- Agent files → `bun run generate:agents [--source <id>]`
- Skill files → `bun run generate:skills [--source <id>]`
- Sync content → `bun run sync [--source <id>]`
- All scripts support `--source <id>` and `--dry-run` flags
- When something breaks, **fix the script** — don't work around it manually
- All scripts are **idempotent** — running them twice produces the same result.
  Always run a script twice to verify idempotency after making changes to it

## Session Completion

When ending a work session, complete ALL steps below. Work is NOT complete until
`git push` succeeds.

1. File issues for remaining work
2. Run quality gates (if code changed)
3. Update issue status — close finished work
4. Push to remote:
   ```sh
   git pull --rebase
   bd sync
   git push
   git status  # must show "up to date with origin"
   ```
5. Verify all changes committed AND pushed

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds

<!-- BEGIN BEADS INTEGRATION -->
## Issue Tracking with bd (beads)

**IMPORTANT**: This project uses **bd (beads)** for ALL issue tracking. Do NOT use markdown TODOs, task lists, or other tracking methods.

### Why bd?

- Dependency-aware: Track blockers and relationships between issues
- Git-friendly: Dolt-powered version control with native sync
- Agent-optimized: JSON output, ready work detection, discovered-from links
- Prevents duplicate tracking systems and confusion

### Quick Start

**Check for ready work:**

```bash
bd ready --json
```

**Create new issues:**

```bash
bd create "Issue title" --description="Detailed context" -t bug|feature|task -p 0-4 --json
bd create "Issue title" --description="What this issue is about" -p 1 --deps discovered-from:bd-123 --json
```

**Claim and update:**

```bash
bd update <id> --claim --json
bd update bd-42 --priority 1 --json
```

**Complete work:**

```bash
bd close bd-42 --reason "Completed" --json
```

### Issue Types

- `bug` - Something broken
- `feature` - New functionality
- `task` - Work item (tests, docs, refactoring)
- `epic` - Large feature with subtasks
- `chore` - Maintenance (dependencies, tooling)

### Priorities

- `0` - Critical (security, data loss, broken builds)
- `1` - High (major features, important bugs)
- `2` - Medium (default, nice-to-have)
- `3` - Low (polish, optimization)
- `4` - Backlog (future ideas)

### Workflow for AI Agents

1. **Check ready work**: `bd ready` shows unblocked issues
2. **Claim your task atomically**: `bd update <id> --claim`
3. **Work on it**: Implement, test, document
4. **Discover new work?** Create linked issue:
   - `bd create "Found bug" --description="Details about what was found" -p 1 --deps discovered-from:<parent-id>`
5. **Complete**: `bd close <id> --reason "Done"`

### Auto-Sync

bd automatically syncs via Dolt:

- Each write auto-commits to Dolt history
- Use `bd dolt push`/`bd dolt pull` for remote sync
- No manual export/import needed!

### Important Rules

- ✅ Use bd for ALL task tracking
- ✅ Always use `--json` flag for programmatic use
- ✅ Link discovered work with `discovered-from` dependencies
- ✅ Check `bd ready` before asking "what should I work on?"
- ❌ Do NOT create markdown TODO lists
- ❌ Do NOT use external issue trackers
- ❌ Do NOT duplicate tracking systems

For more details, see README.md and docs/QUICKSTART.md.

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds

<!-- END BEADS INTEGRATION -->
