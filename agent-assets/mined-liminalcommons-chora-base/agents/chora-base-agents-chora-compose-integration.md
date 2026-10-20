---
sap_id: SAP-017
version: 1.0.0
status: active
last_updated: 2025-11-05
type: reference
audience: agents
complexity: intermediate
estimated_reading_time: 9
progressive_loading:
  phase_1: "lines 1-200"   # Quick Reference + Core Workflows
  phase_2: "lines 201-380" # Advanced Integration
  phase_3: "full"          # Complete including troubleshooting
phase_1_token_estimate: 4000
phase_2_token_estimate: 8000
phase_3_token_estimate: 10500
---

# chora-compose Integration (SAP-017) - Agent Awareness

**SAP ID**: SAP-017
**Last Updated**: 2025-11-05
**Audience**: Generic AI Coding Agents

---

## 📖 Quick Reference

**New to SAP-017?** → Read **[README.md](README.md)** first (5-min read)

The README provides:
- 🚀 **Quick Start** - Interactive modality selector (`select-modality.py`) + 4 modality quick starts
- 📚 **4 Modalities** - pip (library), MCP (AI agents), CLI (interactive), Docker (team deployment)
- 🎯 **Decision Trees** - Choose modality by role, use case, or team size
- 📊 **Role-Based Workflows** - Developer, AI agent, team lead, DevOps paths
- 🔧 **Troubleshooting** - 3 common problems (selector not found, import errors, MCP loading)

**This AGENTS.md provides**: Agent-specific patterns for chora-compose integration, modality selection, and deployment workflows.

---

## Detailed Quick Reference

### When to Use

**Use chora-compose integration (SAP-017) when**:
- Integrating Docker Compose with chora-base projects
- Setting up containerized development environments
- Orchestrating multi-service AI agent architectures
- Managing environment configuration and secrets
- Need reproducible builds across machines
- Deploying to Docker-based production environments

**Don't use when**:
- Simple single-process Python scripts (use venv directly)
- No service dependencies (database, APIs, etc.)
- Developing chora-compose internals (see SAP-018)
- Production Kubernetes deployments (different orchestration)

### Installation Methods

| Method | When to Use | Command |
|--------|-------------|---------|
| **pip** | CLI access, scripting, CI/CD | `pip install chora-compose` |
| **MCP Server** | Claude Desktop integration | Configure `claude_desktop_config.json` |
| **Direct CLI** | One-off content generation | `uvx chora-compose` |

### Key Concepts

- **chora-compose**: Docker Compose-based orchestration for AI agents
- **MCP Server**: Model Context Protocol integration for Claude
- **Service Orchestration**: Multi-container coordination (DB, API, tools)
- **Volume Mounts**: Persistent data and code sharing
- **Environment Config**: API keys, secrets, service URLs

---

## User Signal Patterns

### Integration Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "integrate chora-compose" | install_chora_compose() | pip install chora-compose | Python package |
| "setup MCP server" | configure_mcp_server() | Edit claude_desktop_config.json | Claude Desktop |
| "configure Docker" | setup_docker_compose() | Create docker-compose.yml | Multi-service |
| "add service dependency" | add_service(name) | Update docker-compose.yml | Database, API, etc. |
| "run containerized" | start_services() | docker-compose up | Launch all services |
| "debug container" | debug_container(service) | docker-compose logs | View service logs |

### Common Variations

**Installation**:
- "integrate chora-compose" / "setup chora-compose" / "install chora-compose" → install_chora_compose()
- "configure MCP" / "setup MCP server" / "enable MCP integration" → configure_mcp_server()

**Service Management**:
- "start services" / "run containers" / "launch Docker" → start_services()
- "debug container" / "check logs" / "troubleshoot service" → debug_container()

---

## Common Workflows

### Workflow 1: Install chora-compose via pip (2-3 minutes)

**User signal**: "Integrate chora-compose", "Setup chora-compose", "Install chora-compose"

**Purpose**: Install chora-compose Python package for CLI access

**Steps**:
1. Install package:
   ```bash
   pip install chora-compose
   ```

2. Verify installation:
   ```bash
   chora-compose --version
   # Expected: chora-compose v1.0.0 or higher
   ```

3. Configure API keys:
   ```bash
   export ANTHROPIC_API_KEY="your-key"
   export OPENAI_API_KEY="your-key"
   ```

4. Test basic usage:
   ```bash
   chora-compose generate --template blog-post --output test.md
   ```

**Expected outcome**: chora-compose installed and functional

---

### Workflow 2: Configure MCP Server for Claude Desktop (5-10 minutes)

**User signal**: "Setup MCP server", "Configure MCP", "Enable MCP integration"

**Purpose**: Integrate chora-compose with Claude Desktop via MCP

**Steps**:
1. Install chora-compose:
   ```bash
   pip install chora-compose
   ```

2. Locate Claude Desktop config:
   ```bash
   # macOS
   ~/Library/Application Support/Claude/claude_desktop_config.json

   # Linux
   ~/.config/Claude/claude_desktop_config.json
   ```

3. Update config to add MCP server:
   ```json
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
   ```

4. Restart Claude Desktop

5. Verify in Claude:
   ```
   User: "List available MCP tools"
   Claude: [Shows chora-compose tools: generate_content, validate_config, etc.]
   ```

**Expected outcome**: chora-compose tools available in Claude Desktop

---

### Workflow 3: Create docker-compose.yml for Multi-Service Architecture (10-20 minutes)

**User signal**: "Configure Docker", "Setup docker-compose", "Create multi-service architecture"

**Purpose**: Orchestrate multiple services (app, database, API) with Docker Compose

**Steps**:
1. Create docker-compose.yml:
   ```yaml
   version: '3.8'

   services:
     app:
       build: .
       volumes:
         - .:/workspace
       environment:
         - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
       depends_on:
         - postgres
         - redis

     postgres:
       image: postgres:15
       environment:
         POSTGRES_DB: chora
         POSTGRES_USER: user
         POSTGRES_PASSWORD: password
       volumes:
         - postgres_data:/var/lib/postgresql/data

     redis:
       image: redis:7-alpine
       volumes:
         - redis_data:/data

   volumes:
     postgres_data:
     redis_data:
   ```

2. Create Dockerfile:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /workspace
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   CMD ["python", "main.py"]
   ```

3. Start services:
   ```bash
   docker-compose up -d
   ```

4. Verify services running:
   ```bash
   docker-compose ps
   # Expected: All services "Up"
   ```

**Expected outcome**: Multi-service architecture running in Docker

---

### Workflow 4: Add Service Dependency (5 minutes)

**User signal**: "Add service dependency", "Add database", "Add Redis"

**Purpose**: Add new service to existing docker-compose.yml

**Steps**:
1. Read current docker-compose.yml

2. Add new service:
   ```yaml
   # Example: Adding Elasticsearch
   elasticsearch:
     image: elasticsearch:8.10.0
     environment:
       - discovery.type=single-node
       - xpack.security.enabled=false
     ports:
       - "9200:9200"
     volumes:
       - es_data:/usr/share/elasticsearch/data
   ```

3. Update app service to depend on new service:
   ```yaml
   app:
     depends_on:
       - postgres
       - redis
       - elasticsearch  # Added
   ```

4. Add volume for new service:
   ```yaml
   volumes:
     postgres_data:
     redis_data:
     es_data:  # Added
   ```

5. Restart services:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

**Expected outcome**: New service integrated and running

---

### Workflow 5: Debug Container Issues (2-5 minutes)

**User signal**: "Debug container", "Check logs", "Troubleshoot service"

**Purpose**: Diagnose and fix containerized service problems

**Steps**:
1. Check service status:
   ```bash
   docker-compose ps
   # Identify failing service
   ```

2. View service logs:
   ```bash
   docker-compose logs <service-name>
   # Example: docker-compose logs app
   ```

3. Common issues and fixes:

   **Issue: Service not starting**
   ```bash
   # Check for port conflicts
   docker-compose logs <service> | grep "bind: address already in use"
   # Fix: Change port in docker-compose.yml
   ```

   **Issue: Volume mount errors**
   ```bash
   # Check volume paths
   docker-compose config | grep volumes -A 5
   # Fix: Update volume paths to absolute paths
   ```

   **Issue: Environment variables not set**
   ```bash
   # Check environment
   docker-compose exec <service> env | grep API_KEY
   # Fix: Add to docker-compose.yml env section
   ```

4. Restart service after fix:
   ```bash
   docker-compose restart <service>
   ```

**Expected outcome**: Service issue identified and resolved

---

## Best Practices

### Practice 1: Use Environment Variables for Secrets

**Pattern**:
```yaml
# ✅ GOOD: Environment variables
services:
  app:
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

# ❌ BAD: Hardcoded secrets
services:
  app:
    environment:
      - ANTHROPIC_API_KEY=sk-ant-xxxxx
```

**Why**: Prevents committing secrets to git, enables per-environment configuration

---

### Practice 2: Mount Code as Volume for Development

**Pattern**:
```yaml
# ✅ GOOD: Volume mount for development
services:
  app:
    volumes:
      - .:/workspace  # Code reloads without rebuild

# ❌ BAD: Copy code in Dockerfile only
# Requires rebuild for every code change
```

**Why**: Faster development iteration, no rebuild needed

---

### Practice 3: Use Health Checks for Service Dependencies

**Pattern**:
```yaml
services:
  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

  app:
    depends_on:
      postgres:
        condition: service_healthy  # Wait for health check
```

**Why**: Ensures services start in correct order, app doesn't crash on startup

---

### Practice 4: Use Named Volumes for Persistent Data

**Pattern**:
```yaml
services:
  postgres:
    volumes:
      - postgres_data:/var/lib/postgresql/data  # Named volume

volumes:
  postgres_data:  # Persists across container restarts
```

**Why**: Data survives container recreation, avoids data loss

---

### Practice 5: Document Service Configuration in README

**Pattern**:
```markdown
# README.md

## Services

- **app**: Main application (Python 3.11)
- **postgres**: Database (PostgreSQL 15)
- **redis**: Cache (Redis 7)

## Quick Start

\`\`\`bash
docker-compose up -d
docker-compose logs -f app
\`\`\`
```

**Why**: Team members understand architecture, easier onboarding

---

## Common Pitfalls

### Pitfall 1: Not Configuring API Keys

**Problem**: Container starts but chora-compose fails with "missing API key"

**Fix**: Add environment variables

```yaml
# In docker-compose.yml
services:
  app:
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
```

**Why**: Containers isolated from host environment, must explicitly pass vars

---

### Pitfall 2: Volume Mount Path Errors

**Problem**: Code changes not reflected in container

**Fix**: Use correct volume syntax

```yaml
# ❌ BAD: Missing leading dot
services:
  app:
    volumes:
      - /workspace  # Anonymous volume

# ✅ GOOD: Mount current directory
services:
  app:
    volumes:
      - .:/workspace  # Bind mount
```

**Why**: Anonymous volumes don't link to host filesystem

---

### Pitfall 3: Service Starts Before Dependencies Ready

**Problem**: App crashes on startup with "connection refused" to database

**Fix**: Use health checks

```yaml
services:
  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]

  app:
    depends_on:
      postgres:
        condition: service_healthy  # Wait for health check
```

**Why**: depends_on alone only waits for container start, not readiness

---

### Pitfall 4: Port Conflicts

**Problem**: "bind: address already in use"

**Fix**: Change port mapping

```yaml
# ❌ BAD: Port 5432 already used on host
services:
  postgres:
    ports:
      - "5432:5432"

# ✅ GOOD: Use different host port
services:
  postgres:
    ports:
      - "5433:5432"  # Host:Container
```

**Why**: Multiple services can't bind same host port

---

### Pitfall 5: Not Using .dockerignore

**Problem**: Docker build slow, copies unnecessary files

**Fix**: Create .dockerignore

```
# .dockerignore
.git
__pycache__
*.pyc
.env
node_modules
.venv
```

**Why**: Reduces build context size, faster builds

---

## Integration with Other SAPs

### SAP-011 (docker-operations)
- Docker Compose builds on Docker basics
- Integration: Use docker-operations for single-container, chora-compose for orchestration

### SAP-018 (chora-compose-meta)
- Meta-SAP for chora-compose internals
- Integration: Use SAP-017 for integration, SAP-018 for development

### SAP-012 (development-lifecycle)
- Docker Compose in development workflows
- Integration: Use chora-compose in DDD phase for environment setup

---

## Support & Resources

**SAP-017 Documentation**:
- [Capability Charter](capability-charter.md) - Integration problem and scope
- [Protocol Spec](protocol-spec.md) - Installation methods and patterns
- [Awareness Guide](awareness-guide.md) - Detailed workflows
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking

**chora-compose Resources**:
- [chora-compose Repository](https://github.com/liminalcommons/chora-compose)
- [MCP Protocol](https://modelcontextprotocol.io/)

**Related SAPs**:
- [SAP-011 (docker-operations)](../docker-operations/) - Docker basics
- [SAP-018 (chora-compose-meta)](../chora-compose-meta/) - chora-compose internals
- [SAP-012 (development-lifecycle)](../development-lifecycle/) - Development workflows

---

## Version History

- **1.0.0** (2025-11-05): Initial AGENTS.md for SAP-017
  - 5 workflows: Install pip, Configure MCP, Create docker-compose, Add Service, Debug Container
  - 1 user signal pattern table (Integration Operations)
  - 5 best practices, 5 common pitfalls
  - Integration with SAP-011, SAP-018, SAP-012

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code-specific patterns
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Check [adoption-blueprint.md](adoption-blueprint.md) for installation
4. Install: `pip install chora-compose`
