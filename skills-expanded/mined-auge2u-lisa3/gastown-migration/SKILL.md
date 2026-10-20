# Gastown Migration Skill

This skill analyzes existing projects and structures them for [Gastown](https://github.com/steveyegge/gastown) — Steve Yegge's multi-agent workspace manager.

## Overview

The migration process transforms a project into Gastown-compatible structure:

```
project/
├── .gt/
│   ├── memory/
│   │   ├── semantic.json      # Permanent facts (tech stack, constraints)
│   │   ├── episodic.json      # Decisions with TTL (~30 days)
│   │   └── procedural.json    # Learned patterns
│   ├── beads/
│   │   └── gt-*.json          # Individual work items
│   └── convoys/
│       └── convoy-*.json      # Bundled work assignments
└── [existing project files]
```

## Commands

| Command | Purpose |
|---------|---------|
| `analyze` | Scan project, generate semantic memory |
| `beads` | Extract work items from TODOs, issues, PRDs |
| `convoy` | Bundle related beads into work assignments |
| `migrate` | Full migration (analyze + beads + convoy) |

## Phase 1: Analyze (Semantic Memory)

### Discovery Procedure

Scan these locations in order:

1. **Package files** (for tech stack detection)
   - `package.json` — Node.js runtime, framework, dependencies
   - `Cargo.toml` — Rust projects
   - `go.mod` — Go projects
   - `requirements.txt`, `pyproject.toml` — Python projects
   - `Gemfile` — Ruby projects

2. **Configuration files** (for service detection)
   - `.firebaserc`, `firebase.json` — Firebase
   - `wrangler.toml` — Cloudflare Workers
   - `vercel.json` — Vercel deployment
   - `docker-compose.yml`, `Dockerfile` — Containerization
   - `*.env.example` — Environment variables hint

3. **Documentation** (for project understanding)
   - `README.md` — Project description, setup instructions
   - `docs/` — Architecture docs, ADRs, PRDs
   - `CONTRIBUTING.md` — Development workflow
   - `CHANGELOG.md` — Project history

4. **Source structure** (for codebase understanding)
   - `src/`, `lib/`, `app/` — Main code directories
   - `tests/`, `__tests__/`, `spec/` — Test directories
   - `schemas/`, `migrations/` — Database schemas

### Output: semantic.json

```json
{
  "$schema": "semantic-memory-v1",
  "project": {
    "name": "my-app",
    "type": "web-application",
    "primary_language": "TypeScript",
    "description": "A task management app for teams"
  },
  "tech_stack": {
    "runtime": "Node.js 20",
    "framework": "Next.js 14",
    "database": "Neon PostgreSQL",
    "auth": "Firebase Auth",
    "deployment": "Vercel",
    "styling": "Tailwind CSS",
    "testing": "Vitest"
  },
  "personas": [
    {"name": "Team Lead", "needs": ["assign tasks", "track progress"]},
    {"name": "Developer", "needs": ["see my tasks", "update status"]}
  ],
  "constraints": [
    "Must support offline mode",
    "GDPR compliant data handling"
  ],
  "non_goals": [
    "Mobile native app (web-only for MVP)",
    "Enterprise SSO (future phase)"
  ],
  "evidence": {
    "last_scan": "2026-01-27T10:00:00Z",
    "files_analyzed": ["package.json", "README.md", "docs/PRD.md"]
  }
}
```

## Phase 2: Beads (Work Items)

### Extraction Sources

Scan for work items in:

1. **TODO comments** in source code
   - `// TODO:`, `# TODO:`, `/* TODO */`
   - `// FIXME:`, `// HACK:`, `// XXX:`

2. **GitHub Issues** (if `.git` exists)
   - Open issues via `gh issue list`
   - Labels map to bead type/priority

3. **PRD documents**
   - User stories with acceptance criteria
   - Feature requirements

4. **Backlog files**
   - `BACKLOG.md`, `TODO.md`
   - `docs/backlog/`, `docs/roadmap/`

5. **Existing roadmap outputs**
   - `scopecraft/EPICS_AND_STORIES.md`
   - `scopecraft/OPEN_QUESTIONS.md`

### Bead Schema

```json
{
  "$schema": "bead-v1",
  "id": "gt-abc12",
  "title": "Add user authentication",
  "type": "feature",
  "complexity": "L",
  "priority": "high",
  "status": "pending",
  "dependencies": [],
  "acceptance_criteria": [
    "User can sign up with email",
    "User can sign in with Google OAuth",
    "Session persists across page refresh"
  ],
  "evidence": {
    "source": "docs/PRD-auth.md",
    "line": 42,
    "extracted": "2026-01-27T10:00:00Z"
  },
  "metadata": {
    "epic": "User Management",
    "labels": ["auth", "security"]
  }
}
```

### Bead Types

| Type | Description |
|------|-------------|
| `feature` | New functionality |
| `bug` | Defect fix |
| `chore` | Maintenance, refactoring |
| `docs` | Documentation |
| `spike` | Research/investigation |

### Complexity Estimates

| Size | Description | Typical Duration |
|------|-------------|------------------|
| `XS` | Trivial change | < 1 hour |
| `S` | Small task | 1-4 hours |
| `M` | Medium task | 1-2 days |
| `L` | Large task | 3-5 days |
| `XL` | Epic-sized | 1-2 weeks |

### ID Generation

Bead IDs follow Gastown convention: `gt-<5-char-alphanumeric>`

Example: `gt-abc12`, `gt-xyz99`, `gt-m4n5p`

## Phase 3: Convoy (Work Bundles)

### Convoy Creation Rules

1. **Size**: 3-7 beads per convoy (optimal batch)
2. **Coherence**: Related beads grouped together
3. **Dependencies**: Respect bead dependency order
4. **Parallelization**: Independent convoys can run concurrently

### Convoy Schema

```json
{
  "$schema": "convoy-v1",
  "id": "convoy-001",
  "name": "Authentication Sprint",
  "description": "Implement core user authentication features",
  "beads": ["gt-abc12", "gt-def34", "gt-ghi56"],
  "assigned_to": null,
  "status": "pending",
  "created": "2026-01-27T10:00:00Z",
  "metadata": {
    "epic": "User Management",
    "estimated_days": 5
  }
}
```

### Bundling Strategies

1. **By Epic**: Group all beads from same epic
2. **By Dependency Chain**: Group dependent beads sequentially
3. **By Skill**: Group beads requiring similar expertise
4. **By Size**: Combine small beads, isolate large ones

## Quality Gates

### Analyze Gates

| Gate | Requirement |
|------|-------------|
| `semantic_valid` | semantic.json is valid JSON |
| `project_identified` | project.name is not null |
| `tech_stack_detected` | At least 2 tech_stack fields populated |
| `evidence_recorded` | files_analyzed has 1+ entries |

### Beads Gates

| Gate | Requirement |
|------|-------------|
| `beads_extracted` | At least 1 bead created |
| `beads_have_criteria` | All beads have acceptance_criteria |
| `beads_have_evidence` | All beads have evidence.source |
| `beads_valid_ids` | All IDs match `gt-[a-z0-9]{5}` |

### Convoy Gates

| Gate | Requirement |
|------|-------------|
| `convoy_created` | At least 1 convoy created |
| `convoy_size_valid` | All convoys have 3-7 beads |
| `convoy_beads_exist` | All referenced beads exist |

## Validation

Run validation with:

```bash
# Python validator
python plugins/lisa-loops-memory/hooks/validate_gastown.py

# Check specific phase
python plugins/lisa-loops-memory/hooks/validate_gastown.py --phase analyze
python plugins/lisa-loops-memory/hooks/validate_gastown.py --phase beads
python plugins/lisa-loops-memory/hooks/validate_gastown.py --phase convoy
```

## Integration with Gastown

After migration, Gastown Mayor can:

1. **Read Memory**: Load `.gt/memory/semantic.json` for project context
2. **List Beads**: Enumerate `.gt/beads/*.json` for available work
3. **Assign Convoys**: Create/assign convoys to Polecats
4. **Track Progress**: Update bead/convoy status as work completes

## Examples

See `examples/` directory for sample outputs:
- `examples/gastown/semantic.json`
- `examples/gastown/beads/`
- `examples/gastown/convoys/`
