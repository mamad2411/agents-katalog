---
sap_id: SAP-018
version: 1.0.0
status: active
last_updated: 2025-11-05
type: reference
audience: claude_code
complexity: advanced
estimated_reading_time: 8
progressive_loading:
  phase_1: "lines 1-180"   # Quick Start + Core Workflows
  phase_2: "lines 181-300" # Advanced Patterns
  phase_3: "full"          # Complete including tips and pitfalls
phase_1_token_estimate: 3500
phase_2_token_estimate: 7000
phase_3_token_estimate: 9500
---

# chora-compose Meta (SAP-018) - Claude-Specific Awareness

**SAP ID**: SAP-018
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-05

---

## 📖 Quick Reference

**New to SAP-018?** → Read **[README.md](README.md)** first (5-min read)

The README provides:
- 🚀 **Quick Start** - Core generation commands and MCP tool overview
- 📚 **24 MCP Tools** - Complete tool reference across 7 categories
- 🎯 **3-Tier Collections** - Content, Artifact, Collection architecture
- 🏗️ **Context Propagation** - MERGE, OVERRIDE, ISOLATE modes
- 🔧 **Troubleshooting** - Generator errors, cache issues

**This CLAUDE.md provides**: Claude Code-specific workflows using Bash (chora-compose CLI), Write (configs), Read (outputs).

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for understanding chora-compose architecture.

### First-Time Session

1. Read [AGENTS.md](AGENTS.md) for generic chora-compose meta workflows
2. Use this file for Claude Code tool integration (Read for docs, Bash for validation)
3. Focus on understanding architecture before making technology decisions

### Key Files to Read

```bash
# Architecture overview
Read docs/skilled-awareness/chora-compose-meta/protocol-spec.md
# Focus on Section 2: Architectural Principles

# Design philosophy
Read docs/skilled-awareness/chora-compose-meta/capability-charter.md
# Focus on Design Philosophy section

# MCP tools catalog
Read docs/skilled-awareness/chora-compose-meta/protocol-spec.md
# Focus on MCP Tool Catalog section
```

---

## Claude Code Meta-Documentation Workflows

### Workflow 1: Understanding Architecture with Read

```markdown
User: "Explain chora-compose architecture"

Claude (Phase 1: Read Architecture - 0-10k tokens):
1. Read architecture specification:
   Read docs/skilled-awareness/chora-compose-meta/protocol-spec.md
   # Focus on lines 50-200 (Section 2: Architectural Principles)

2. Extract key components:
   - **MCP Server Layer**: FastMCP framework with 17 tools
   - **Template Engine**: Jinja2 for content generation
   - **Provider Layer**: Anthropic/OpenAI API abstraction
   - **Config Manager**: YAML validation with Pydantic
   - **Observer**: Structured logging and metrics

Claude (Phase 2: Explain to User - 10-20k tokens):
3. Summarize architecture:
   "chora-compose architecture has 5 main components:

   **1. MCP Server Layer** (FastMCP)
      - 17 MCP tools: generate_content, validate_config, list_templates, etc.
      - 5 resource URI families: template://, config://, log://, metric://, output://
      - Standard MCP protocol compliance

   **2. Template Engine** (Jinja2)
      - Template discovery from templates/ directory
      - Variable injection with validation
      - Output formatting (markdown, JSON)

   **3. Provider Layer**
      - Anthropic Claude API integration
      - OpenAI API integration
      - Provider abstraction for future extensibility

   **4. Config Manager**
      - YAML schema validation (Pydantic)
      - Environment variable resolution
      - Config merging (global + local)

   **5. Observer**
      - Structured JSON logging
      - Request/response tracing
      - Token usage metrics"

Result: Complete architectural understanding from protocol-spec.md
```

---

### Workflow 2: Understanding Design Trade-offs with Read

```markdown
User: "Why did chora-compose choose Docker Compose over Kubernetes?"

Claude (Phase 1: Read Design Philosophy - 0-10k tokens):
1. Read capability charter:
   Read docs/skilled-awareness/chora-compose-meta/capability-charter.md
   # Focus on Design Philosophy section

2. Find trade-off documentation:
   # Search for "Trade-off" or "Docker Compose vs Kubernetes"
   Grep: pattern="Docker Compose vs Kubernetes", path="docs/skilled-awareness/chora-compose-meta/"

Claude (Phase 2: Explain Trade-off - 10-20k tokens):
3. Summarize trade-off to user:
   "chora-compose chose Docker Compose over Kubernetes:

   **Decision**: Docker Compose for development environments

   **Rationale**:
   - Simpler for local development (single docker-compose.yml vs complex K8s manifests)
   - Faster iteration (docker-compose up vs kubectl apply + wait)
   - Lower learning curve (most developers know Docker Compose)
   - DX-first approach (development experience prioritized)

   **Trade-offs Accepted**:
   - Less production-ready than Kubernetes
   - Limited scaling capabilities
   - No advanced orchestration features (service mesh, operators, etc.)

   **When to Reconsider**:
   - Large-scale production deployment needed
   - Multi-region orchestration required
   - Advanced networking/security features critical

   **Use chora-compose when**: Local development, AI agent orchestration
   **Use Kubernetes when**: Production at scale, complex deployments"

Result: Clear understanding of design decision and trade-offs
```

---

### Workflow 3: Exploring MCP Tools Catalog with Read and Bash

```markdown
User: "What MCP tools are available in chora-compose?"

Claude (Phase 1: Read MCP Tools - 0-10k tokens):
1. Read MCP tools catalog:
   Read docs/skilled-awareness/chora-compose-meta/protocol-spec.md
   # Focus on MCP Tool Catalog section (likely lines 300-500)

Claude (Phase 2: Inspect Tools Interactively - 10-30k tokens):
2. Launch MCP inspector (optional for interactive testing):
   Bash: npx @modelcontextprotocol/inspector uvx chora-compose
   # Launches inspector UI at http://localhost:5173

3. List tools from documentation:
   From protocol-spec.md reading:

   **Content Generation (6 tools)**:
   - generate_content: Generate from template
   - generate_batch: Batch generation
   - generate_with_context: Context-aware generation
   - stream_generation: Real-time streaming
   - validate_output: Output validation
   - format_content: Format markdown/JSON

   **Template Management (4 tools)**:
   - list_templates: Discover available templates
   - get_template: Retrieve template content
   - validate_template: Template syntax validation
   - create_template: New template creation

   **Configuration (3 tools)**:
   - get_config: Retrieve current config
   - validate_config: Config schema validation
   - update_config: Modify configuration

   **Observability (4 tools)**:
   - get_metrics: Token usage, generation stats
   - trace_request: Request/response tracing
   - list_logs: Query structured logs
   - health_check: System health status

Claude (response to user):
"chora-compose provides 17 MCP tools across 4 categories:

**Content Generation (6)**: generate_content, generate_batch, generate_with_context, stream_generation, validate_output, format_content

**Template Management (4)**: list_templates, get_template, validate_template, create_template

**Configuration (3)**: get_config, validate_config, update_config

**Observability (4)**: get_metrics, trace_request, list_logs, health_check

**Resource URIs**: template://, config://, log://, metric://, output://

To explore interactively, run:
npx @modelcontextprotocol/inspector uvx chora-compose"

Result: Complete catalog understanding, ready for integration
```

---

### Workflow 4: Comparing to Alternatives with Read and Grep

```markdown
User: "Compare chora-compose to Tilt and Kubernetes"

Claude (Phase 1: Read Ecosystem Positioning - 0-10k tokens):
1. Read ecosystem comparison:
   Read docs/skilled-awareness/chora-compose-meta/capability-charter.md
   # Focus on Ecosystem Positioning section

2. Search for comparison matrix:
   Grep: pattern="chora-compose.*Kubernetes.*Tilt", path="docs/skilled-awareness/chora-compose-meta/", output_mode="content", -C=10

Claude (Phase 2: Summarize Comparison - 10-20k tokens):
3. Present comparison matrix:
   "Comparison of development environment tools:

   | Tool | Use Case | Complexity | Best For |
   |------|----------|------------|----------|
   | **chora-compose** | Dev env | Low | Local dev, AI agents |
   | **Kubernetes** | Production | High | Production, scale |
   | **Tilt** | Dev + K8s | Medium | K8s-bound dev |
   | **Skaffold** | CI/CD + K8s | Medium | CI/CD pipelines |
   | **DevContainers** | VS Code | Low | VS Code users |

   **Use chora-compose when**:
   ✅ Local development environment (primary use case)
   ✅ AI agent orchestration with MCP
   ✅ Multi-service Python projects
   ✅ Docker Compose experience in team
   ✅ Simple deployment needs

   **Use Kubernetes when**:
   ⚠️ Production orchestration at scale
   ⚠️ Complex networking/security requirements
   ⚠️ Multi-region deployments
   ⚠️ Advanced rolling updates/canary

   **Use Tilt when**:
   ⚠️ Kubernetes-bound development
   ⚠️ Need hot reloading for K8s manifests
   ⚠️ Local-to-production parity critical

   **Migration Paths**:
   - chora-compose → Kubernetes: Production readiness
   - Docker Compose → chora-compose: Add MCP integration
   - Tilt → chora-compose: Simplify dev environment"

Result: Clear decision criteria for tool selection
```

---

## Claude-Specific Tips

### Tip 1: Read protocol-spec.md Before Making Technology Decisions

**Pattern**:
```markdown
# Before deciding on chora-compose:
Read docs/skilled-awareness/chora-compose-meta/protocol-spec.md
Read docs/skilled-awareness/chora-compose-meta/capability-charter.md

# Understand architecture and trade-offs
# Then read SAP-017 for integration
```

**Why**: Meta-documentation prevents misaligned technology choices

---

### Tip 2: Use Bash to Launch MCP Inspector for Interactive Exploration

**Pattern**:
```markdown
# Interactive tool discovery:
Bash: npx @modelcontextprotocol/inspector uvx chora-compose

# Opens browser UI at http://localhost:5173
# Test tools before coding integration
```

**Why**: Visual exploration faster than reading docs for tool discovery

---

### Tip 3: Use Grep to Find Specific Design Decisions

**Pattern**:
```markdown
# Search for specific trade-offs:
Grep: pattern="Trade-off.*YAML.*Code", path="docs/skilled-awareness/chora-compose-meta/", output_mode="content", -C=5

# Find architectural rationale:
Grep: pattern="MCP-Native.*rationale", path="docs/skilled-awareness/chora-compose-meta/", output_mode="content", -C=10
```

**Why**: Fast targeted search for design decision context

---

### Tip 4: Read capability-charter.md for Design Philosophy

**Pattern**:
```markdown
# Before customizing chora-compose:
Read docs/skilled-awareness/chora-compose-meta/capability-charter.md
# Focus on Design Philosophy section

# Understand core principles:
# - Composition over Configuration
# - DX-First
# - Explicit Trade-offs
# - Standards-Based
```

**Why**: Customizations aligned with philosophy avoid breaking assumptions

---

### Tip 5: Use Read to Check Current Section Headings for Navigation

**Pattern**:
```markdown
# When protocol-spec.md is large:
Read docs/skilled-awareness/chora-compose-meta/protocol-spec.md
# Scan headings (lines starting with ##)
# Note line ranges for targeted reading

# Then read specific section:
Read docs/skilled-awareness/chora-compose-meta/protocol-spec.md
# offset=300, limit=200 (if MCP Tools section at line 300)
```

**Why**: Progressive loading minimizes token usage

---

## Common Pitfalls for Claude Code

### Pitfall 1: Trying to Use chora-compose for Production Orchestration

**Problem**: Read architecture, miss trade-offs, recommend for production

**Fix**: ALWAYS read Design Philosophy section

```markdown
# ❌ BAD: Recommend without reading trade-offs
Read protocol-spec.md (architecture only)
# Recommend chora-compose for production

# ✅ GOOD: Read trade-offs before recommending
Read capability-charter.md (Design Philosophy section)
# Understand: "chora-compose optimized for dev, not production"
# Recommend Kubernetes for production
```

**Why**: Architecture looks capable, but design philosophy clarifies scope

---

### Pitfall 2: Not Reading Meta-Documentation Before Integration

**Problem**: Jump to SAP-017 (integration) without SAP-018 (meta)

**Fix**: Read SAP-018 first for architectural understanding

```markdown
# ❌ BAD: Integrate without understanding
# Directly read SAP-017 and integrate
# Miss trade-offs, wrong use case

# ✅ GOOD: Meta-documentation first
Read docs/skilled-awareness/chora-compose-meta/AGENTS.md
Read docs/skilled-awareness/chora-compose-meta/capability-charter.md
# Decide if appropriate for use case
# THEN read SAP-017 for integration
```

**Why**: Integration guide doesn't explain when NOT to use chora-compose

---

### Pitfall 3: Treating MCP Tools as REST API Endpoints

**Problem**: Assume MCP tools work like HTTP REST endpoints

**Fix**: Read MCP Protocol section in protocol-spec.md

```markdown
# MCP has different semantics:
Read docs/skilled-awareness/chora-compose-meta/protocol-spec.md
# Focus on MCP Protocol section

# Key differences from REST:
# - Server-Sent Events (SSE) for streaming
# - JSON-RPC 2.0 message format
# - Tool discovery via list_tools
# - Resource URIs (template://, config://, etc.)
```

**Why**: MCP protocol has specific request/response format, not REST

---

### Pitfall 4: Ignoring Observability Infrastructure When Debugging

**Problem**: Debug issues without checking logs/metrics

**Fix**: Use Bash to inspect structured logs

```markdown
# When debugging chora-compose issues:
Bash: cat logs/chora-compose.jsonl | jq '.level=="ERROR"'

# Trace specific request:
Bash: cat logs/chora-compose.jsonl | jq 'select(.trace_id=="abc123")'

# Check token usage:
# Use get_metrics MCP tool or read metric:// resource
```

**Why**: Observability infrastructure designed for debugging, use it

---

### Pitfall 5: Not Understanding Provider Abstraction Layer

**Problem**: Tightly couple to Anthropic API, miss abstraction

**Fix**: Read Provider Layer section in protocol-spec.md

```markdown
# Understand provider abstraction:
Read docs/skilled-awareness/chora-compose-meta/protocol-spec.md
# Focus on Provider Layer section

# Provider abstraction enables:
# - Switch between Anthropic and OpenAI
# - Add new providers (e.g., Cohere, local models)
# - Provider-agnostic templates

# Don't hardcode to specific API
```

**Why**: Provider abstraction enables flexibility, design intention

---

## Support & Resources

**SAP-018 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic chora-compose meta workflows
- [Capability Charter](capability-charter.md) - Philosophy, ecosystem positioning
- [Protocol Spec](protocol-spec.md) - Complete architecture specification
- [Awareness Guide](awareness-guide.md) - Contribution patterns, extension points
- [Adoption Blueprint](adoption-blueprint.md) - Learning path
- [Ledger](ledger.md) - Adoption tracking

**chora-compose Resources**:
- [chora-compose Repository](https://github.com/liminalcommons/chora-compose)
- [MCP Protocol Spec](https://spec.modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)

**Related SAPs**:
- [SAP-017 (chora-compose-integration)](../chora-compose-integration/) - Integration guide
- [SAP-011 (docker-operations)](../docker-operations/) - Docker basics
- [SAP-016 (mcp-server-development)](../mcp-server-development/) - MCP patterns

---

## Version History

- **1.0.0** (2025-11-05): Initial CLAUDE.md for SAP-018
  - 4 workflows: Architecture with Read, Design Trade-offs with Read, MCP Tools with Read/Bash, Comparing Alternatives with Read/Grep
  - Tool patterns: Read for documentation, Bash for MCP inspector, Grep for targeted search
  - 5 Claude-specific tips, 5 common pitfalls
  - Focus on understanding before integration

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic chora-compose meta workflows
2. Review [protocol-spec.md](protocol-spec.md) for complete architecture
3. Check [capability-charter.md](capability-charter.md) for design philosophy
4. For integration: See [SAP-017](../chora-compose-integration/)
