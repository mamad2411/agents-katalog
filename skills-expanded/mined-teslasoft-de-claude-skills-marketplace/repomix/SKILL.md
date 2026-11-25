---
name: repomix
description: |
  Pack codebases into AI-friendly XML/Markdown bundles for context loading.
  Supports auto-discovery, segmented bundles, compression. Use for code review,
  debugging, architecture understanding. Keywords: repomix, bundle, codebase, context.
triggers:
  - /repomix
  - /repomix pack
  - /repomix bundle
  - /repomix auto
  - /repomix status
  - /repomix help
  - pack codebase
  - bundle repository
  - codebase context
negative_triggers:
  - general file operations
  - git operations (use /collab)
  - simple text search
version: 2.0.0
author: Christian Kusmanow / Claude
last_updated: 2026-01-23
security:
  trust_model: Local files only, no external uploads
  confirmations:
    - Cleanup of old bundle files before regeneration
  notes: Security check enabled by default (secretlint)
---

# Skill: Repomix

Pack codebases into AI-friendly formats for context loading in Claude sessions.

## When to Use

- Preparing codebase context for AI code review
- Debugging complex issues across multiple files
- Understanding architecture of a new project
- Sharing codebase snapshots for collaboration
- Starting new Claude sessions with full project context

## When NOT to Use

- Simple file operations (use Read/Write tools)
- Git operations (use /collab)
- Searching for specific text (use Grep)

---

## Quick Start

```bash
# Pack current directory
bunx repomix

# Pack with compression
bunx repomix --compress

# Create Teslasoft bundles
/repomix bundle
```

---

## Commands

| Command | Action |
|---------|--------|
| `/repomix` | Load Repomix context and CLI reference |
| `/repomix pack` | Pack current directory |
| `/repomix pack --compress` | Pack with token compression |
| `/repomix auto` | Intelligent auto-discovery based on project type |
| `/repomix bundle` | Create all Teslasoft bundles |
| `/repomix bundle --vault` | Create vault bundle only |
| `/repomix bundle --web` | Create all web segment bundles |
| `/repomix status` | Show existing bundles and freshness |
| `/repomix help` | Show CLI quick reference |

---

## Bundle Storage

**Location:** `D:\TeamProjects\Teslasoft\.repomix-bundles\`

| Bundle | Content | ~Tokens |
|--------|---------|---------|
| `vault-bundle.xml` | Obsidian vault (goals, projects, resources) | 67K |
| `web-app.xml` | Core framework (base, common, layout) | 23K |
| `web-modules.xml` | Feature modules (api, dashboard, docs) | 32K |
| `web-e2e.xml` | Cypress E2E tests | 7K |
| `web-config.xml` | Build configs (nx, tsconfig) | 5K |

See [Bundle Workflow](references/bundle-workflow.md) for details.

---

## Output Formats

| Format | Flag | Use Case |
|--------|------|----------|
| XML | `--style xml` (default) | Best for LLMs |
| Markdown | `--style markdown` | Human-readable |
| JSON | `--style json` | Programmatic |

---

## Failure Modes & Recovery

| Issue | Recovery |
|-------|----------|
| Bundle too large | Use segmented bundles (`--web-app`, `--web-modules`) |
| Security warning | Review flagged files, use `--no-security-check` if safe |
| Token limit exceeded | Use `--compress` flag, filter with `--include` |
| Stale bundles | Run `/repomix bundle` to refresh |

---

## Security & Permissions

- **Required tools:** Bash (bunx commands)
- **Security check:** Enabled by default via secretlint
- **Confirmations:** Old bundles deleted before regeneration
- **Trust model:** Local files only, no external uploads

---

## Best Practices

1. Use segmented bundles for targeted context loading
2. Always compress large codebases (`--compress`)
3. Check bundle status regularly (`/repomix status`)
4. Start new sessions with fresh bundles for best results
5. Use task-specific bundles (e.g., web-e2e for E2E testing)

---

## References

- [CLI Reference](references/cli-reference.md) - Full command documentation
- [Bundle Workflow](references/bundle-workflow.md) - Bundle creation process
- [Auto-Discovery](references/auto-discovery.md) - Intelligent file selection
- [Teslasoft Integration](references/teslasoft-integration.md) - Project-specific workflows

---

## Metadata

```yaml
author: Christian Kusmanow / Claude
version: 2.0.0
last_updated: "2026-01-23"
change_surface: references/ (CLI updates, new bundle types)
extension_points: references/bundle-workflow.md (new bundle segments)
```

### Changelog

- **v2.0.0** (2026-01-23): SDL migration - Progressive disclosure structure
  - Split 796-line monolith into SKILL.md (~150 lines) + 4 references
  - Added YAML frontmatter with triggers and negative_triggers
  - Added security section and failure modes
- **v1.4.0** (2026-01-23): Segmented web bundles (82% token reduction)
- **v1.3.0** (2026-01-23): Added `bundle` and `status` commands
- **v1.2.0** (2026-01-23): Enhanced auto-discovery with project type detection
- **v1.1.0** (2026-01-23): Added `auto` argument for intelligent file selection
