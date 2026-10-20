---
sap_id: SAP-017
version: 1.0.0
status: active
last_updated: 2025-11-05
type: reference
audience: claude_code
complexity: intermediate
estimated_reading_time: 8
progressive_loading:
  phase_1: "lines 1-180"   # Quick Start + Core Workflows
  phase_2: "lines 181-320" # Advanced Integration
  phase_3: "full"          # Complete including tips and pitfalls
phase_1_token_estimate: 3500
phase_2_token_estimate: 7000
phase_3_token_estimate: 9000
---

# chora-compose Integration (SAP-017) - Claude-Specific Awareness

**SAP ID**: SAP-017
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-05

---

## 📖 Quick Reference

**New to SAP-017?** → Read **[README.md](README.md)** first (5-min read)

The README provides:
- 🚀 **Quick Start** - Interactive modality selector script + quick starts for all 4 modalities
- 📚 **4 Modalities** - pip, MCP, CLI, Docker with <30 min time-to-first-success
- 🎯 **Decision Trees** - Role, use case, and team size-based modality selection
- 📊 **4 Role-Based Workflows** - Complete paths for developer, AI agent, team lead, DevOps
- 🔧 **Troubleshooting** - Import errors, MCP loading, selector issues

**This CLAUDE.md provides**: Claude Code-specific workflows using Bash (install/Docker), Write (configs), Read (verification).

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for integrating chora-compose.

### First-Time Session

1. Read [AGENTS.md](AGENTS.md) for generic chora-compose integration workflows
2. Use this file for Claude Code tool integration (Write for config, Bash for Docker, Read for verification)
3. Always test integration after configuration changes

### Installation Commands

```bash
# Install chora-compose
pip install chora-compose

# Configure MCP server (edit Claude Desktop config)
# macOS: ~/Library/Application Support/Claude/claude_desktop_config.json

# Start Docker services
docker-compose up -d
```

---

## Claude Code chora-compose Workflows

### Workflow 1: Installing and Configuring MCP Server with Write

```markdown
User: "Setup chora-compose MCP server for Claude Desktop"

Claude (Phase 1: Install Package - 0-10k tokens):
1. Install chora-compose:
   Bash: pip install chora-compose

   Output:
   Successfully installed chora-compose-1.0.0

2. Verify installation:
   Bash: chora-compose --version

   Output:
   chora-compose v1.0.0

Claude (Phase 2: Configure MCP - 10-30k tokens):
3. Identify config file location:
   # macOS
   config_path = "~/Library/Application Support/Claude/claude_desktop_config.json"

4. Read existing config:
   Read ~/Library/Application Support/Claude/claude_desktop_config.json

5. Update config to add chora-compose MCP server:
   Edit ~/Library/Application Support/Claude/claude_desktop_config.json
   # Add chora-compose to mcpServers section:
   {
     "mcpServers": {
       "chora-compose": {
         "command": "uvx",
         "args": ["chora-compose"],
         "env": {
           "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
           "OPENAI_API_KEY": "${OPENAI_API_KEY}"
         }
       }
     }
   }

Claude (Phase 3: Verify - 30-40k tokens):
6. Validate JSON syntax:
   Bash: cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | jq .

Claude (response to user):
"✅ chora-compose MCP server configured:
   - Installed: chora-compose v1.0.0
   - Config: ~/Library/Application Support/Claude/claude_desktop_config.json
   - MCP server: chora-compose (uvx command)
   - Environment: ANTHROPIC_API_KEY, OPENAI_API_KEY

   Next steps:
   1. Restart Claude Desktop to load MCP server
   2. Verify tools with: 'List available MCP tools'

   You'll see chora-compose tools: generate_content, validate_config, etc."

Result: MCP server configured, ready after Claude Desktop restart
```

---

### Workflow 2: Creating docker-compose.yml with Write

```markdown
User: "Create docker-compose.yml for chora-base project with PostgreSQL and Redis"

Claude (Phase 1: Create Compose File - 0-20k tokens):
1. Create docker-compose.yml:
   Write docker-compose.yml
   version: '3.8'

   services:
     app:
       build: .
       volumes:
         - .:/workspace
       environment:
         - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
         - OPENAI_API_KEY=${OPENAI_API_KEY}
       ports:
         - "8000:8000"
       depends_on:
         postgres:
           condition: service_healthy
         redis:
           condition: service_started

     postgres:
       image: postgres:15
       environment:
         POSTGRES_DB: chora
         POSTGRES_USER: user
         POSTGRES_PASSWORD: password
       ports:
         - "5432:5432"
       volumes:
         - postgres_data:/var/lib/postgresql/data
       healthcheck:
         test: ["CMD-SHELL", "pg_isready -U user"]
         interval: 10s
         timeout: 5s
         retries: 5

     redis:
       image: redis:7-alpine
       ports:
         - "6379:6379"
       volumes:
         - redis_data:/data

   volumes:
     postgres_data:
     redis_data:

Claude (Phase 2: Create Dockerfile - 20-40k tokens):
2. Create Dockerfile:
   Write Dockerfile
   FROM python:3.11-slim

   WORKDIR /workspace

   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       build-essential \
       && rm -rf /var/lib/apt/lists/*

   # Copy requirements and install Python dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy project files
   COPY . .

   CMD ["python", "main.py"]

Claude (Phase 3: Create .dockerignore - 40-50k tokens):
3. Create .dockerignore:
   Write .dockerignore
   .git
   __pycache__
   *.pyc
   .env
   .venv
   node_modules
   *.log
   .DS_Store

Claude (Phase 4: Verify Setup - 50-60k tokens):
4. Validate docker-compose.yml:
   Bash: docker-compose config

   Output:
   (Shows parsed YAML, validates syntax)

Claude (response to user):
"✅ Docker Compose setup created:
   - docker-compose.yml: 3 services (app, postgres, redis)
   - Dockerfile: Python 3.11 base
   - .dockerignore: Optimized build context

   Services configured:
   - **app**: Port 8000, volume mount for hot reload
   - **postgres**: Port 5432, persistent data, health check
   - **redis**: Port 6379, persistent cache

   Start services:
   ```bash
   docker-compose up -d
   docker-compose logs -f app
   ```"

Result: Complete Docker Compose setup ready to launch
```

---

### Workflow 3: Debugging Container Issues with Bash and Read

```markdown
User: "App container failing to start, debug the issue"

Claude (Phase 1: Check Service Status - 0-10k tokens):
1. Check all services:
   Bash: docker-compose ps

   Output:
   NAME     STATUS                  PORTS
   app      Exit 1
   postgres Up (healthy)            5432
   redis    Up                      6379

   # app service failed

Claude (Phase 2: Read Logs - 10-20k tokens):
2. Get app service logs:
   Bash: docker-compose logs app

   Output:
   app_1  | Traceback (most recent call last):
   app_1  |   File "main.py", line 5, in <module>
   app_1  |     import psycopg2
   app_1  | ModuleNotFoundError: No module named 'psycopg2'

   # Missing dependency

Claude (Phase 3: Fix Issue - 20-40k tokens):
3. Read requirements.txt:
   Read requirements.txt

4. Add missing dependency:
   Edit requirements.txt
   # Add: psycopg2-binary==2.9.9

5. Rebuild container:
   Bash: docker-compose build app

6. Restart service:
   Bash: docker-compose up -d app

Claude (Phase 4: Verify Fix - 40-50k tokens):
7. Check service status:
   Bash: docker-compose ps

   Output:
   NAME     STATUS     PORTS
   app      Up         8000
   postgres Up         5432
   redis    Up         6379

   # All services running

8. Verify app logs:
   Bash: docker-compose logs app | tail -10

   Output:
   app_1  | Server started on port 8000

Claude (response to user):
"✅ Container issue resolved:
   - Problem: Missing psycopg2 dependency
   - Fix: Added psycopg2-binary==2.9.9 to requirements.txt
   - Rebuilt app container
   - Status: All services now running ✅

   App accessible at: http://localhost:8000"

Result: Container issue diagnosed and fixed, services running
```

---

## Claude-Specific Tips

### Tip 1: Use Write for Config Files, Edit for Updates

**Pattern**:
```markdown
# Creating new file
Write docker-compose.yml
# (Full YAML content)

# Updating existing file
Read docker-compose.yml
Edit docker-compose.yml
# (Targeted changes)
```

**Why**: Write for creation, Edit for modifications preserves structure

---

### Tip 2: Validate YAML with Bash After Creation

**Pattern**:
```markdown
# After creating docker-compose.yml:
Bash: docker-compose config

# Validates syntax, shows parsed YAML
```

**Why**: Catches YAML syntax errors before runtime

---

### Tip 3: Use Bash for All Docker Operations

**Pattern**:
```markdown
# ✅ GOOD: Bash for Docker commands
Bash: docker-compose up -d
Bash: docker-compose logs app
Bash: docker-compose ps

# ❌ BAD: Trying other tools for Docker operations
# Docker commands require Bash
```

**Why**: Docker CLI requires shell execution

---

### Tip 4: Read Logs with tail for Recent Errors

**Pattern**:
```markdown
# Get recent logs only
Bash: docker-compose logs app | tail -20

# Follow logs in real-time
Bash: docker-compose logs -f app
```

**Why**: Recent logs show current state, full logs too verbose

---

### Tip 5: Use jq to Validate JSON Config Files

**Pattern**:
```markdown
# After editing claude_desktop_config.json:
Bash: cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | jq .

# Valid JSON returns formatted output
# Invalid JSON shows error
```

**Why**: Catches JSON syntax errors before Claude Desktop restart

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Validating YAML After Creation

**Problem**: Create docker-compose.yml but don't validate, fails on startup

**Fix**: ALWAYS validate with docker-compose config

```markdown
# After Write docker-compose.yml:
Bash: docker-compose config
# Shows parsed YAML, catches errors
```

**Why**: YAML syntax errors only caught at runtime otherwise

---

### Pitfall 2: Forgetting to Rebuild After Dependency Changes

**Problem**: Update requirements.txt but don't rebuild, changes not applied

**Fix**: Rebuild container after dependency updates

```markdown
# After Edit requirements.txt:
Bash: docker-compose build app
Bash: docker-compose up -d app
```

**Why**: Container image must be rebuilt to include new dependencies

---

### Pitfall 3: Not Checking Service Health Before Declaring Success

**Problem**: Service starts but crashes immediately, declare success too early

**Fix**: Check logs and status after starting

```markdown
# After docker-compose up:
Bash: docker-compose ps  # Check status
Bash: docker-compose logs app | tail -10  # Check for errors
```

**Why**: Container may start then immediately crash, logs show real state

---

### Pitfall 4: Using Relative Paths in Volume Mounts Without Verification

**Problem**: Volume mount points to wrong directory, code changes not reflected

**Fix**: Use `.` for current directory, verify mounts

```yaml
# ✅ GOOD: Current directory
volumes:
  - .:/workspace

# ❌ BAD: Relative path might be wrong
volumes:
  - ../project:/workspace
```

**Why**: `.` always refers to docker-compose.yml directory

---

### Pitfall 5: Not Adding Environment Variables to docker-compose.yml

**Problem**: API keys work on host but not in container

**Fix**: Explicitly pass environment variables

```yaml
# In docker-compose.yml:
services:
  app:
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
```

**Why**: Containers isolated from host environment

---

## Support & Resources

**SAP-017 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic chora-compose integration workflows
- [Capability Charter](capability-charter.md) - Integration problem and scope
- [Protocol Spec](protocol-spec.md) - Installation methods and patterns
- [Awareness Guide](awareness-guide.md) - Detailed workflows
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking

**chora-compose Resources**:
- [chora-compose Repository](https://github.com/liminalcommons/chora-compose)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

**Related SAPs**:
- [SAP-011 (docker-operations)](../docker-operations/) - Docker basics
- [SAP-018 (chora-compose-meta)](../chora-compose-meta/) - chora-compose internals
- [SAP-012 (development-lifecycle)](../development-lifecycle/) - Development workflows

---

## Version History

- **1.0.0** (2025-11-05): Initial CLAUDE.md for SAP-017
  - 3 workflows: Configure MCP with Write, Create docker-compose with Write, Debug with Bash/Read
  - Tool patterns: Write for configs, Bash for Docker ops, Read for verification, Edit for updates
  - 5 Claude-specific tips, 5 common pitfalls
  - YAML/JSON validation patterns with docker-compose config and jq

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic chora-compose workflows
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Check [adoption-blueprint.md](adoption-blueprint.md) for installation
4. Install: `pip install chora-compose`
5. Configure MCP: Edit claude_desktop_config.json and restart Claude Desktop
