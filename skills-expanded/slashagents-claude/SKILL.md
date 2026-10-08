# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**SlashAgents** is a curated collection of 53 battle-tested Claude Code extensions (16 slash commands, 35 subagents, 2 skills) designed to help developers **stay in flow**.

**Core Value:** Claude Code extensions that preserve creative momentum - whether doing generic workflow tasks (PR management, CI orchestration) or structured BMAD development (epic workflows).

**Project Type:** Documentation/distribution project - NO CODE TO WRITE. Only file organization, metadata standardization, and documentation.

## Repository Structure

```
SlashAgents/
├── LICENSE                      # MIT License
├── README.md                    # Single comprehensive documentation
├── VALIDATION.md                # Pre-release testing checklist
├── .gitignore
├── commands/                    # 16 slash commands (users copy to ~/.claude/commands/)
│   ├── pr.md, ci-orchestrate.md, test-orchestrate.md, commit-orchestrate.md
│   ├── parallel.md, epic-dev.md, epic-dev-full.md, epic-dev-init.md
│   ├── epic-dev-epic-end-tests.md, coverage.md, code-quality.md
│   ├── create-test-plan.md, user-testing.md, nextsession.md
│   ├── usertestgates.md, test-epic-full.md
│   └── lib/                     # Shared libraries (dependency-analyzer.md, failure-handler.md)
├── agents/                      # 35 subagents (users copy to ~/.claude/agents/)
│   ├── unit-test-fixer.md, api-test-fixer.md, database-test-fixer.md, e2e-test-fixer.md
│   ├── linting-fixer.md, type-error-fixer.md, import-error-fixer.md, security-scanner.md
│   ├── epic-story-creator.md, epic-story-validator.md, epic-test-generator.md
│   ├── epic-implementer.md, epic-code-reviewer.md
│   ├── pr-workflow-manager.md, parallel-orchestrator.md, digdeep.md
│   └── ... (browser executors, CI agents, testing agents)
└── skills/                      # 2 skills (users copy to ~/.claude/skills/)
    ├── pr-workflow/
    └── safe-refactor.md
```

**Important:** Distributable tools are at ROOT level, NOT in `.claude/`. Users copy these folders to their `~/.claude/` (global) or project `.claude/` folder.

**Ignored (development only):**
- `_bmad/` - BMAD framework helper
- `.claude/` - Local BMAD commands for this repo
- `docs/` - Planning documents (PRD, architecture, epics)
- `CLAUDE.md` - This guidance file

## Tool Dependency Tiers

| Tier | Description | Examples |
|------|-------------|----------|
| **Standalone** | Works with zero configuration | `/pr`, `/nextsession`, `/commit_orchestrate` |
| **MCP-Enhanced** | Requires specific MCP servers | `/ci_orchestrate` (`github` MCP) |
| **BMAD-Required** | Requires BMAD framework installed | `/epic-dev`, `/epic-dev-full`, `/epic-dev-init` |
| **Project-Context** | Requires relevant project files | `unit-test-fixer`, `api-test-fixer` |

## Documentation Standards

### Description Voice
- **MUST** start with present-tense verb
- **MUST** be under 60 characters
- Examples: "Fixes CI failures automatically", "Manages pull request workflows"

### Prerequisite Notation
| Tier | Format |
|------|--------|
| Standalone | — (em dash) |
| MCP-Enhanced | `server-name` MCP |
| BMAD-Required | BMAD framework |
| Project-Context | descriptive text |

### File Naming
- All files: **kebab-case**, lowercase
- Commands: `{action}-{target}.md` (e.g., `ci-orchestrate.md`)
- Agents: `{role}-{specialization}.md` (e.g., `unit-test-fixer.md`)

## Implementation Phases

1. **Phase 0: Audit** - Verify MCP names, file names, tier assignments, cross-references
2. **Phase 1: Setup** - Create repository with root files
3. **Phase 2: Content** - Copy tools, rename to kebab-case, update metadata
4. **Phase 3: Documentation** - Create VALIDATION.md and README.md
5. **Phase 4: Validation** - Run checklist, conduct First-Use Test (2-3 cold testers)
6. **Phase 5: Release** - Publish to GitHub

## Key Documents

- `docs/prd.md` - Product Requirements Document (28 FRs, NFRs)
- `docs/architecture.md` - Architectural decisions and patterns
- `docs/epics.md` - 4 epics, 22 stories for implementation
- `docs/project_context.md` - Critical rules for AI agents
- `docs/BMAD-SYNC.md` - **How to sync with BMAD-METHOD PR #1213**

## Critical Rules

- **NO hardcoded paths** - tools must work across any project
- **Shared libs in commands/lib/** - dependency-analyzer.md, failure-handler.md used by orchestrators
- **NO modifications to tool logic** - only metadata and filename changes
- **First-Use Test required** - 2-3 people must cold-install before release

## CI Runner Quick Reference

| Setting | Value |
|---------|-------|
| **Runner Name** | `macos-runner-1` |
| **Install Path** | `~/cc-agents-runner/` |
| **Service Name** | `actions.runner.Autopsias-slashagents.macos-runner-1` |

```bash
# Check status
cd ~/cc-agents-runner && ./svc.sh status

# Start runner
cd ~/cc-agents-runner && ./svc.sh start

# Stop runner
cd ~/cc-agents-runner && ./svc.sh stop
```
