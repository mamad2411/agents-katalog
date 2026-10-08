---
name: dev-deepinit
description: Deep codebase initialization — generate hierarchical AGENTS.md / CLAUDE.md context files for a new project so engineering agents have full context from session start.
---

# Dev Deepinit

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer.

Deep codebase initialization. For a new project, generate hierarchical AGENTS.md / CLAUDE.md context files that give engineering agents full project context from session start — instead of forcing them to re-discover the codebase every session.

## Use When
- Onboarding a new project to EvoNexus
- Existing project lacks AGENTS.md / CLAUDE.md / project context docs
- After a major refactor that invalidates existing context docs

## Do Not Use When
- Project already has comprehensive context docs
- Trivial / experimental codebases (overhead not worth it)

## Workflow

### Phase 1 — Discovery
Delegate to `@scout-explorer`:
- Map the directory structure
- Identify the language(s), framework(s), build tools
- Find entry points (main files, package scripts, CI configs)
- Find test setup
- Find existing docs (README, ARCHITECTURE.md, etc.)

### Phase 2 — Synthesis
- Project purpose (1-2 sentences)
- Tech stack
- Architecture overview
- Key directories with their purpose
- Build / test / run commands
- Conventions detected (naming, error handling, imports)
- Known gotchas (from comments, TODOs, recent commits)

### Phase 3 — Generation
Create the hierarchical context:

```
{project-root}/
├── CLAUDE.md          # Top-level project context (this is what Claude reads first)
├── AGENTS.md          # Detailed context for engineering agents
└── docs/
    └── architecture/
        └── [C]project-overview-{date}.md
```

### Phase 4 — Verification
- `@oath-verifier` reads the new context docs and confirms they're accurate

## Output Files

### CLAUDE.md (top of project)
```markdown
# {Project Name}

[1-2 sentence purpose]

## Tech Stack
- Language: ...
- Framework: ...
- Build: ...

## Quick Commands
- Build: `...`
- Test: `...`
- Run: `...`

## Architecture
[high-level overview]

## Conventions
[detected patterns]
```

### AGENTS.md (detailed context)
```markdown
# Engineering Context

## Module Map
- `src/auth/` — authentication
- `src/db/` — database layer
- ...

## Key Files
- `src/main.ts:42` — entry point
- ...

## Patterns
[deep convention notes]

## Gotchas
[known pitfalls]
```

## Pairs With
- `@scout-explorer` (Phase 1)
- `@quill-writer` (writes the actual docs)
- `@oath-verifier` (Phase 4 verification)
