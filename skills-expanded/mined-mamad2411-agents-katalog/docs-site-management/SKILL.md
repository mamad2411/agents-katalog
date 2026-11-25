# Docs Site Management

## Purpose
Manages the AstroJS + Starlight docs site structure, versioning, and validation.

## Role
Technical Writer

## Phase
Cross-phase (ongoing every sprint)

## Triggered By
Ongoing; release tag creation triggers version snapshot.

## Inputs
- Current docs site content under `apps/docs/src/content/`

## Process
Manages AstroJS + Starlight + starlight-versions plugin.

### Version Snapshot Convention
- During sprint: Technical Writer writes to `internal/latest/`.
- On release tag: CI copies `internal/latest/` → `internal/v{X}.{Y}.{Z}/`.
- Frozen after snapshot — never modified.
- `starlight-versions` plugin auto-generates version selector UI.

### Structure to Maintain
```
apps/docs/src/content/
├── internal/
│   ├── latest/          ← Technical Writer always writes here
│   │   ├── architecture/
│   │   ├── api-reference/
│   │   ├── schemas/
│   │   ├── runbooks/
│   │   ├── development/
│   │   └── releases/
│   └── v{X}.{Y}.{Z}/   ← frozen snapshot per release
└── public/              ← future public docs
```

### Validates Every Sprint
- No broken internal links
- All sidebar navigation entries have corresponding files
- Version selector works correctly
- Search indexes updated

## Outputs
Maintained docs site structure; validated navigation and links each sprint.

## Quality Gates
- [ ] All writes during sprint go to internal/latest/
- [ ] Frozen version snapshots never modified after creation
- [ ] No broken internal links
- [ ] Sidebar navigation matches actual files

## References
- `.claude/skills/technical-writer/schema-documentation/SKILL.md`
- `.claude/skills/technical-writer/api-reference-documentation/SKILL.md`
- `.claude/skills/technical-writer/architecture-documentation/SKILL.md`
