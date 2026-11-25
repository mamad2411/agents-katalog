---
name: omnidev-migration
description: Migrate existing repositories with provider-specific files (.claude, .cursor, etc.) to OmniDev's unified approach. Consolidates instructions, converts skills/commands to capabilities, and establishes a single source of truth.
---

# OmniDev Migration

This skill guides you through migrating repositories from provider-specific configurations to OmniDev.

## When to Use This Skill

- Repository has provider-specific files (`.claude/`, `.cursor/`, `AGENTS.md`, `.mcp.json`)
- User wants to unify multi-provider configurations
- Team wants a single source of truth for AI agent instructions

## Migration Workflow

### 1. Install OmniDev

```bash
npm install -g @omnidev-ai/cli
# or: bun install -g @omnidev-ai/cli
```

Verify: `omnidev --version`

### 2. Initialize in Repository Root

```bash
omnidev init
```

Creates:
- `OMNI.md` - Project instructions (source of truth)
- `omni.toml` - Configuration
- `.omni/` - Runtime directory (auto-gitignored)

### 3. Consolidate Instructions

**Migrate content FROM** (pick what exists):
- `CLAUDE.md`, `AGENTS.md`
- `.cursor/rules`, `.cursor/.cursorrules`
- `.claude/instructions.md`

**TO** `OMNI.md`:

```markdown
# Project Name

## Project Description
[2-3 sentences about purpose and functionality]

## Conventions
- Coding standards
- Style preferences
- Testing requirements

## Architecture
- Tech stack
- Key components
- Data flow patterns
```

**DO NOT migrate**:
- File tree listings
- Provider-specific tool configs
- Skills/commands (these become capabilities)

### 4. Convert Skills/Commands to Capabilities

#### Capability Structure

```
capabilities/
└── my-project-tools/
    ├── capability.toml      # Metadata
    ├── agents/              # Custom agents (optional)
    ├── commands/            # Commands (optional)
    ├── docs/                # Documentation (optional)
    └── rules/               # Behavior rules (optional)
```

#### capability.toml Template

```toml
[capability]
id = "my-project-tools"
name = "My Project Tools"
version = "1.0.0"
description = "Project-specific tools and workflows"

[capability.providers]
# Enable for specific providers
claude = true  # alias for claude-code
cursor = true
windsurf = true
```

#### Migration Steps

1. **Create capability directory**:
   ```bash
   mkdir -p capabilities/my-project-tools
   ```

2. **Convert existing skills/commands**:
   - `.claude/skills/*.ts` → `capabilities/my-project-tools/commands/`
   - Custom agents → `capabilities/my-project-tools/agents/`
   - Instructions → `capabilities/my-project-tools/rules/`

3. **Register in omni.toml**:
   ```toml
   [capabilities.sources]
   my-project-tools = "file://./capabilities/my-project-tools"

   [profiles.default]
   capabilities = ["my-project-tools"]
   ```

### 5. Migrate MCP Servers

**FROM** `.mcp.json` or `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    }
  }
}
```

**TO** `omni.toml`:
```toml
[mcp.filesystem]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
```

### 6. Update .gitignore

Add:
```gitignore
# OmniDev runtime
.omni/
omni.local.toml

# Generated provider files
CLAUDE.md
AGENTS.md
.cursor/rules
.cursor/.cursorrules
.cursor/mcp.json
.mcp.json
```

Keep in version control: `OMNI.md`, `omni.toml`, `capabilities/`

### 7. Remove Old Files from Git

```bash
# Remove generated files (will be regenerated)
git rm --cached CLAUDE.md AGENTS.md .mcp.json

# Optional: Remove old provider directories after migrating capabilities
# git rm --cached -r .claude/ .cursor/ .opencode/
```

### 8. Sync and Verify

```bash
omnidev sync    # Generate provider files
omnidev doctor  # Verify configuration
```

## Capability Organization Patterns

### Single Capability (Simple Projects)

```toml
[capabilities.sources]
project-tools = "file://./capabilities/project-tools"

[profiles.default]
capabilities = ["project-tools"]
```

### Multiple Capabilities (Complex Projects)

```toml
[capabilities.sources]
api-tools = "file://./capabilities/api-tools"
deploy-tools = "file://./capabilities/deploy-tools"
test-tools = "file://./capabilities/test-tools"

[profiles.default]
capabilities = ["api-tools", "deploy-tools", "test-tools"]
```

### Profile-Based Organization

```toml
[capabilities.sources]
shared = "file://./capabilities/shared"
frontend = "file://./capabilities/frontend"
backend = "file://./capabilities/backend"

[profiles.frontend-dev]
capabilities = ["shared", "frontend"]

[profiles.backend-dev]
capabilities = ["shared", "backend"]

[profiles.fullstack]
capabilities = ["shared", "frontend", "backend"]
```

## Common Migration Scenarios

### Cursor with .cursorrules
1. Copy project content to `OMNI.md`
2. Add `.cursor/rules` to `.gitignore`
3. Run `omnidev sync`

### Multiple Providers
1. Consolidate shared instructions into `OMNI.md`
2. Create provider-specific capabilities if needed
3. Use profiles to manage capability combinations

### Team Migration
1. One person completes migration
2. Commit `OMNI.md`, `omni.toml`, `capabilities/`, `.gitignore`
3. Team runs: `npm install -g @omnidev-ai/cli && omnidev sync`

## Troubleshooting

**Provider files not generated**: Run `omnidev doctor`, check active profile has capabilities

**MCP servers not working**: Verify `omni.toml` MCP config, check logs with `OMNIDEV_DEBUG=1 omnidev sync`

**Capabilities not loading**:
- Verify sources registered in `omni.toml`
- Check capabilities enabled in active profile
- Ensure file paths correct (use `./` prefix for local)

## Verification Checklist

After migration:
- [ ] `omnidev doctor` passes
- [ ] `omnidev sync` generates provider files
- [ ] Old provider files in `.gitignore`
- [ ] `OMNI.md` and `omni.toml` committed
- [ ] Capabilities load correctly
- [ ] MCP servers functional (if used)
- [ ] Team can reproduce setup
