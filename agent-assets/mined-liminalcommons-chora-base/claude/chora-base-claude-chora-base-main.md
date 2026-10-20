# Chora-Base: Claude Agent Awareness (Root)

**Project**: chora-base
**Version**: 5.1.0
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-13

---

## ⚠️ CRITICAL: Read This First!

**chora-base is a TEMPLATE SOURCE, not a project to set up.**

### Quick Decision for Claude

**Are you trying to CREATE A NEW PROJECT using chora-base?**

**✅ YES** → Use the fast-setup script (recommended):

```bash
python scripts/create-capability-server.py \
    --name "Your Capability Name" \
    --namespace yournamespace \
    --enable-mcp \
    --output ~/projects/your-project
```

**What happens**: 5 minutes of automated setup creating a production-ready capability server with multi-interface support (CLI, REST, optional MCP) and all chora-base infrastructure (testing, CI/CD, quality gates, beads, inbox, A-MEM, documentation).

**See**: [README.md](README.md#-start-here-ai-agent-quick-decision-tree) | [SAP-047 (Capability Server Template)](docs/skilled-awareness/capability-server-template/)

**⚠️ SAP-014 Deprecation**: If you see references to SAP-014 (mcp-server-development) or `create-model-mcp-server.py` in older documentation, these have been **deprecated**. Use SAP-047 (capability-server-template) and `create-capability-server.py --enable-mcp` instead. SAP-047 provides multi-interface capability servers (CLI, REST, optional MCP) vs MCP-only.

---

**Are you DEVELOPING chora-base itself?**

**✅ YES** → Continue reading this file for Claude-specific navigation patterns

---

## Quick Start for Claude

This file provides Claude-specific navigation and context loading strategies for working with the chora-base template repository.

### First-Time Navigation

**New to chora-base?**
1. You're reading the right file (root `CLAUDE.md`)
2. Determine your task domain (see Navigation Tree below)
3. Navigate to the appropriate domain's `AGENTS.md` file
4. Read the domain-specific `CLAUDE.md` for Claude patterns
5. Dive into specific SAP documentation as needed

**Returning to chora-base?**
1. Check your task domain
2. Navigate directly to relevant SAP or documentation
3. Use progressive context loading (see below)

---

## What is Chora-Base?

**Chora-base** is a comprehensive template and framework for AI-assisted software development, built around the **SAP (Skilled Awareness Package) framework**. It provides:

- 📦 **30+ Skilled Awareness Packages (SAPs)**: Modular capabilities for development workflows
- 🤖 **Agent-First Design**: Built for Claude Code, Claude Desktop, and other AI agents
- 📋 **Nested Awareness Pattern**: Progressive context loading via AGENTS.md/CLAUDE.md hierarchy
- 🎯 **Production-Ready Templates**: Bootstrap projects with battle-tested patterns
- 🔄 **Coordination Infrastructure**: Cross-repo inbox, event memory (A-MEM), task tracking (beads)

---

## Architecture Overview

### SAP Framework (SAP-000)

The foundation of chora-base is the **SAP framework**, which packages capabilities into five standardized artifacts:

1. **Capability Charter**: Problem statement, solution design, success criteria
2. **Protocol Spec**: Complete technical specification, commands, workflows
3. **Awareness Guide**: Operating patterns for agents (AGENTS.md or awareness-guide.md)
4. **Adoption Blueprint**: Step-by-step installation guide
5. **Ledger**: Adoption tracking, metrics, feedback, version history

Every SAP follows this pattern, making it easy to learn and adopt new capabilities.

### Nested Awareness Pattern (SAP-009)

Chora-base uses a **5-level nested awareness hierarchy**:

```
/CLAUDE.md                                    ← You are here (Root)
│
├─ docs/skilled-awareness/                    ← Domain: SAP Capabilities
│  ├─ AGENTS.md                               ← Generic agent patterns
│  ├─ CLAUDE.md                               ← Claude-specific patterns
│  │
│  ├─ sap-framework/                          ← SAP-000 (Capability Level)
│  │  ├─ AGENTS.md                            ← SAP-000 patterns
│  │  ├─ capability-charter.md
│  │  ├─ protocol-spec.md
│  │  ├─ awareness-guide.md
│  │  └─ ledger.md
│  │
│  ├─ inbox/                                  ← SAP-001 (Capability Level)
│  │  ├─ AGENTS.md
│  │  ├─ CLAUDE.md
│  │  └─ ... (5 artifacts)
│  │
│  └─ ... (30+ SAPs)
│
├─ docs/dev-docs/                             ← Domain: Developer Documentation
│  ├─ AGENTS.md
│  ├─ CLAUDE.md
│  └─ ... (architecture, contributing, etc.)
│
├─ docs/user-docs/                            ← Domain: User Documentation
│  ├─ AGENTS.md
│  ├─ CLAUDE.md
│  └─ ... (getting started, tutorials, reference)
│
└─ docs/project-docs/                         ← Domain: Project Management
   ├─ AGENTS.md
   ├─ CLAUDE.md
   └─ ... (plans, decisions, retrospectives)
```

**Principle**: "Nearest file wins" - navigate from root → domain → capability → feature → component, progressively loading context as needed.

---

## Progressive Context Loading Strategy

Claude should load context progressively to optimize token usage:

### Phase 1: Orientation (0-10k tokens)

**Goal**: Understand task domain and high-level approach

**Read**:
1. This file (`/CLAUDE.md`) for project overview
2. Target domain's `AGENTS.md` (e.g., `docs/skilled-awareness/AGENTS.md`)
3. Target domain's `CLAUDE.md` for Claude-specific patterns

**Output**: Clear understanding of where to find detailed information

---

### Phase 2: Specification (10-50k tokens)

**Goal**: Load detailed technical specifications for the task

**Read**:
1. Target SAP's `protocol-spec.md` for complete technical details
2. Target SAP's `awareness-guide.md` (or `AGENTS.md`) for operating patterns
3. Related SAPs' `AGENTS.md` files if integration needed

**Output**: Complete technical understanding of commands, workflows, APIs

---

### Phase 3: Deep Dive (50-200k tokens)

**Goal**: Understand design rationale and adoption history

**Read**:
1. Target SAP's `capability-charter.md` for problem/solution design
2. Target SAP's `ledger.md` for adoption metrics and feedback
3. Target SAP's `adoption-blueprint.md` if implementing from scratch
4. Source code files as needed

**Output**: Comprehensive understanding for complex implementations

---

## Navigation Tree: Where Should Claude Go?

### Domain 1: User-Facing Documentation

**Path**: [docs/user-docs/AGENTS.md](docs/user-docs/AGENTS.md)

**Use when**:
- User asks "how do I use chora-base?"
- User needs tutorials or getting started guides
- User wants reference documentation
- User is new to chora-base ecosystem

**Contents**:
- Getting started guides
- Tutorials and examples
- Reference documentation
- FAQ and troubleshooting

---

### Domain 2: Developer Documentation

**Path**: [docs/dev-docs/AGENTS.md](docs/dev-docs/AGENTS.md)

**Use when**:
- Contributing to chora-base
- Understanding chora-base architecture
- Setting up development environment
- Debugging chora-base internals

**Contents**:
- Developer setup
- Architecture documentation
- Contributing guidelines
- Testing and debugging

---

### Domain 3: Project Management Documentation

**Path**: [docs/project-docs/AGENTS.md](docs/project-docs/AGENTS.md)

**Use when**:
- User asks about project plans or roadmap
- User wants to understand governance or decisions
- Coordinating work across the project
- Reviewing retrospectives or lessons learned

**Contents**:
- Project plans (like PLAN-2025-11-04-SAP-009-FULL)
- Decision records (ADRs)
- Retrospectives
- Coordination requests

---

### Domain 4: Skilled Awareness (SAP Capabilities)

**Path**: [docs/skilled-awareness/AGENTS.md](docs/skilled-awareness/AGENTS.md)

**Use when**:
- User wants to adopt a specific SAP
- Understanding SAP framework
- Implementing or extending capabilities
- Exploring available SAPs (30+ capabilities)

**Contents**:
- SAP Framework (SAP-000)
- 30+ SAP capabilities
- SAP catalog and index
- Integration patterns

**Key SAPs to Know**:
- **SAP-000** (sap-framework): Foundation for all SAPs
- **SAP-001** (inbox): Cross-repo coordination
- **SAP-009** (agent-awareness): This nested awareness pattern
- **SAP-010** (A-MEM): Agent memory and event tracking
- **SAP-015** (task-tracking): Persistent task management with beads
- **SAP-027** (dogfooding-patterns): How to validate SAPs
- **SAP-029** (sap-generation): Generate new SAPs

---

## Common Claude Code Workflows

### Workflow 1: Adopting a SAP

```markdown
User: "I want to add task tracking to my project"

Claude:
1. Navigate to docs/skilled-awareness/AGENTS.md
2. Find SAP-015 (task-tracking) in the SAP catalog
3. Read docs/skilled-awareness/task-tracking/adoption-blueprint.md
4. Follow step-by-step installation guide
5. Update project AGENTS.md with SAP-015 patterns
```

**Progressive Loading**:
- Phase 1: Read `docs/skilled-awareness/AGENTS.md` + `docs/skilled-awareness/task-tracking/AGENTS.md`
- Phase 2: Read `docs/skilled-awareness/task-tracking/protocol-spec.md` + `adoption-blueprint.md`
- Phase 3 (if needed): Read `capability-charter.md` + `ledger.md` for design rationale

---

### Workflow 2: Understanding Chora-Base Architecture

```markdown
User: "How does chora-base work?"

Claude:
1. Read this file (CLAUDE.md) for overview
2. Navigate to docs/dev-docs/CLAUDE.md for developer perspective
3. Read docs/skilled-awareness/sap-framework/protocol-spec.md
4. Review sap-catalog.json for capability inventory
```

**Progressive Loading**:
- Phase 1: Read `/CLAUDE.md` + `docs/dev-docs/AGENTS.md`
- Phase 2: Read `docs/skilled-awareness/sap-framework/protocol-spec.md`
- Phase 3 (if deep dive): Read architecture documentation, source code

---

### Workflow 3: Contributing to Chora-Base

```markdown
User: "I want to contribute a new SAP"

Claude:
1. Read docs/dev-docs/AGENTS.md for contributing guidelines
2. Navigate to docs/skilled-awareness/sap-generation/
3. Read SAP-029 adoption-blueprint.md for generation workflow
4. Use SAP templates to scaffold new capability
5. Follow SAP-000 protocol-spec.md for artifact requirements
```

**Progressive Loading**:
- Phase 1: Read `docs/dev-docs/AGENTS.md` + `docs/skilled-awareness/CLAUDE.md`
- Phase 2: Read `docs/skilled-awareness/sap-generation/protocol-spec.md` + `sap-framework/protocol-spec.md`
- Phase 3: Review existing SAPs for examples (e.g., SAP-015)

---

### Workflow 4: Multi-Session Task Tracking

```markdown
User: "Continue working on the feature from yesterday"

Claude:
1. Check if SAP-015 (beads) is adopted: ls .beads/
2. If yes: bd ready --json to find unblocked work
3. Read task details: bd show {id} --json
4. Resume work with full context from task description
```

**Why This Matters**: Beads (SAP-015) provides persistent memory across sessions, eliminating context re-establishment overhead.

---

## Claude-Specific Tips

### Tip 1: Use Domain-Level CLAUDE.md Files

Each domain has a `CLAUDE.md` file with Claude-specific patterns:
- [docs/skilled-awareness/CLAUDE.md](docs/skilled-awareness/CLAUDE.md) - SAP navigation
- [docs/dev-docs/CLAUDE.md](docs/dev-docs/CLAUDE.md) - Development workflows
- [docs/user-docs/CLAUDE.md](docs/user-docs/CLAUDE.md) - User documentation tips
- [docs/project-docs/CLAUDE.md](docs/project-docs/CLAUDE.md) - Project navigation

**Always read the domain CLAUDE.md after navigating to a domain.**

---

### Tip 2: Leverage SAP Integration Patterns

Many SAPs integrate with each other:
- **SAP-001 (inbox) + SAP-015 (beads)**: Decompose coordination requests into tasks
- **SAP-010 (A-MEM) + SAP-015 (beads)**: Correlate tasks with event traces
- **SAP-009 (awareness) + all SAPs**: Every SAP uses nested awareness pattern

Look for "Integration with Other SAPs" sections in AGENTS.md files.

---

### Tip 3: Use JSON Output for Programmatic Workflows

Many SAP CLIs provide `--json` flags for Claude Code:
- `bd ready --json` (beads task tracking)
- `bd show {id} --json` (task details)
- `bd list --status open --json` (backlog)

Parse JSON in Claude Code sessions for structured data.

---

### Tip 4: Respect Progressive Loading

**Don't over-read**:
- If user asks "what is SAP-015?", read `docs/skilled-awareness/task-tracking/AGENTS.md` (5min), NOT all 5 artifacts (30min)
- Only read `protocol-spec.md` when implementing
- Only read `capability-charter.md` when understanding design rationale

**Do progressive loading**:
- Phase 1: Quick reference (AGENTS.md)
- Phase 2: Implementation (protocol-spec.md, adoption-blueprint.md)
- Phase 3: Deep understanding (capability-charter.md, ledger.md)

---

### Tip 5: Check Adoption Status Before Recommending SAPs

Always check SAP status in `sap-catalog.json` before recommending:
- **production**: Battle-tested, recommend freely
- **pilot**: Dogfooding phase, use with caution
- **draft**: Experimental, only recommend if explicitly requested
- **deprecated**: Don't recommend, suggest alternatives

Example:
```json
{
  "id": "SAP-015",
  "name": "task-tracking",
  "status": "pilot",  ← Pilot phase, validate before broad recommendation
  "version": "1.0.0"
}
```

---

## Key Files for Claude

### High-Frequency Files (Read Often)

- `/CLAUDE.md` (this file) - Root navigation
- `sap-catalog.json` - Machine-readable SAP registry
- `AGENTS.md` (project root) - Quick reference for all agents
- `docs/skilled-awareness/INDEX.md` - SAP capability index

### Configuration Files

- `.chora/config.yaml` - Chora configuration
- `.beads/config.yaml` - Beads task tracking (if SAP-015 adopted)
- `package.json` - npm dependencies
- `pyproject.toml` - Python dependencies

### Coordination Files (If SAP-001 Adopted)

- `inbox/coordination/active.jsonl` - Active coordination requests
- `inbox/coordination/archived.jsonl` - Historical requests
- `inbox/coordination/events.jsonl` - Coordination event log

### Memory Files (If SAP-010 Adopted)

- `.chora/memory/events/*.jsonl` - Event-sourced history
- `.chora/memory/events/development.jsonl` - Development events
- `.chora/memory/events/inbox.jsonl` - Coordination events

### Task Files (If SAP-015 Adopted)

- `.beads/issues.jsonl` - Task source of truth (git-committed)
- `.beads/beads.db` - SQLite cache (gitignored, auto-generated)

---

## Integration with Claude Code vs Claude Desktop

### Claude Code (VSCode Extension)

**Strengths**:
- Direct file system access (Read, Write, Edit tools)
- Shell command execution (Bash tool)
- Git integration
- Multi-file editing workflows

**Recommended SAPs**:
- SAP-015 (task-tracking): Persistent memory across sessions
- SAP-005 (ci-cd-workflows): GitHub Actions integration
- SAP-011 (docker-operations): Container management
- SAP-003 (project-bootstrap): Scaffold new projects

**Patterns**:
- Use beads CLI directly via Bash tool
- Edit AGENTS.md files as you work
- Commit task progress regularly

---

### Claude Desktop (Chat Interface)

**Strengths**:
- Interactive guidance
- Exploratory conversations
- Documentation generation
- Planning and architecture

**Recommended SAPs**:
- SAP-009 (agent-awareness): Navigate documentation
- SAP-027 (dogfooding-patterns): Validate adoption
- SAP-029 (sap-generation): Generate new capabilities
- SAP-001 (inbox): Coordinate across contexts

**Patterns**:
- Use progressive context loading heavily
- Generate plans and documentation
- Provide architectural guidance
- Coordinate multi-session work via inbox

---

## Common Pitfalls for Claude

### Pitfall 1: Over-Reading Documentation

**Problem**: Reading all 5 SAP artifacts when only AGENTS.md is needed

**Fix**: Use progressive loading:
- Quick question? Read AGENTS.md only
- Implementation? Read protocol-spec.md + adoption-blueprint.md
- Design rationale? Then read capability-charter.md

---

### Pitfall 2: Ignoring SAP Status

**Problem**: Recommending `draft` SAPs as production-ready

**Fix**: Always check `status` in sap-catalog.json:
```bash
grep -A 5 '"id": "SAP-015"' sap-catalog.json | grep status
```

---

### Pitfall 3: Not Using Task Tracking

**Problem**: Losing context between sessions, forgetting subtasks

**Fix**: If SAP-015 adopted, ALWAYS use beads:
```bash
bd ready --json                                    # Find work
bd update {id} --status in_progress --assignee me  # Claim
bd close {id} --reason "Completed X"              # Finish
```

---

### Pitfall 4: Not Updating AGENTS.md

**Problem**: Implementing features without updating agent awareness

**Fix**: After implementing a feature, update relevant AGENTS.md:
- Root AGENTS.md for project-wide patterns
- Domain AGENTS.md for domain-specific patterns
- SAP AGENTS.md for capability-specific patterns

---

### Pitfall 5: Broken Link Networks

**Problem**: Creating AGENTS.md/CLAUDE.md files with broken links

**Fix**: After creating awareness files, validate links:
```bash
bash scripts/validate-awareness-links.sh
```

---

## Quick Reference: SAP Catalog

**Organization**: 45 SAPs across 6 domains for progressive adoption

**Domain Distribution**: Infrastructure (3) • Developer Experience (14) • Foundation (6) • User-Facing (4) • Advanced (8) • Specialized (10)

---

### Infrastructure Domain (Core Foundation - 3 SAPs)

**Purpose**: Universal framework and coordination for any project

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| SAP-000 | sap-framework | active | Core SAP framework and protocols |
| SAP-001 | inbox | active | Cross-repo coordination protocol (90% effort reduction) |
| SAP-002 | chora-base | active | Chora-base meta-package (dogfooding) |

---

### Developer Experience Domain (Development Tools - 14 SAPs)

**Purpose**: Accelerate development with testing, CI/CD, quality gates, tooling, and capability server architecture

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| SAP-003 | project-bootstrap | active | Copier-based project scaffolding |
| SAP-004 | testing-framework | active | pytest + 85% coverage patterns |
| SAP-005 | ci-cd-workflows | active | GitHub Actions automation |
| SAP-006 | quality-gates | active | Pre-commit + ruff + mypy (200x faster) |
| SAP-007 | documentation-framework | active | Diátaxis 4-domain architecture |
| SAP-008 | automation-scripts | active | 25 scripts + justfile (30+ commands) |
| SAP-011 | docker-operations | active | Multi-stage Dockerfiles (150-250MB) |
| SAP-014 | mcp-server-development | deprecated | FastMCP patterns (use SAP-047) |
| SAP-042 | interface-design | pilot | Core/interface separation (80% coupling reduction) |
| SAP-043 | multi-interface | pilot | CLI/REST/MCP patterns (75% time savings) |
| SAP-044 | registry | pilot | Service mesh with capability discovery |
| SAP-045 | bootstrap | pilot | Dependency-ordered startup (90% failure reduction) |
| SAP-046 | composition | pilot | Saga orchestration + circuit breakers + event bus (1,141% ROI) |
| SAP-047 | capability-server-template | pilot | Cookiecutter template (5-min setup, 2,271% ROI) |

---

### Foundation Domain (Technology Stacks - 6 SAPs)

**Purpose**: Next.js 15 + TypeScript + Vitest foundation for React projects with authentication, database, and form validation

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| SAP-020 | react-foundation | active | Next.js 15 + TypeScript (8-12h → 45min) |
| SAP-021 | react-testing | active | Vitest v4 + RTL + MSW (80-90% coverage) |
| SAP-022 | react-linting | active | ESLint 9 + Prettier 3 (182x faster) |
| SAP-033 | react-authentication | pilot | NextAuth v5/Clerk/Supabase/Auth0 (3-4h → 15min, 93.75% savings) |
| SAP-034 | react-database-integration | pilot | Prisma/Drizzle + PostgreSQL (3-4h → 25min, 89.6% savings) |
| SAP-041 | react-form-validation | pilot | React Hook Form + Zod (2-3h → 20min, 88.9% savings) |

---

### User-Facing Domain (User Interactions - 4 SAPs)

**Purpose**: State management, styling, file uploads, and error handling for user interfaces

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| SAP-023 | react-state-management | active | TanStack Query v5 + Zustand v4 + RHF v7 + Zod |
| SAP-024 | react-styling | active | Tailwind CSS v4 + shadcn/ui |
| SAP-035 | react-file-upload | pilot | UploadThing/Vercel Blob/Supabase/S3 (6h → 30min, 91.7% savings) |
| SAP-036 | react-error-handling | pilot | Error boundaries + Sentry (3-4h → 30min, 87.5% savings) |

---

### Advanced Domain (Optimizations & Integrations - 8 SAPs)

**Purpose**: Performance, accessibility, real-time, i18n, testing, monorepos, and advanced tool integrations

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| SAP-017 | chora-compose-integration | active | Content generation (pip, MCP, CLI) |
| SAP-018 | chora-compose-meta | active | 24 MCP tools + Collections architecture |
| SAP-025 | react-performance | active | Core Web Vitals optimization |
| SAP-026 | react-accessibility | active | WCAG 2.2 Level AA compliance |
| SAP-037 | react-realtime-synchronization | pilot | Socket.IO/Pusher/Ably/Supabase (7h → 30min, 92.9% savings) |
| SAP-038 | react-internationalization | pilot | next-intl 20+ languages (5h → 30min, 90% savings) |
| SAP-039 | react-e2e-testing | pilot | Playwright cross-browser (3.5h → 30min, 85.7% savings) |
| SAP-040 | react-monorepo-architecture | pilot | Turborepo + pnpm (7.5h → 30min, 93.3% savings) |

---

### Specialized Domain (Meta-Capabilities - 10 SAPs)

**Purpose**: Process patterns, memory, task tracking, and SAP ecosystem tools

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| SAP-009 | agent-awareness | active | AGENTS.md + CLAUDE.md nested pattern |
| SAP-010 | memory-system | active | A-MEM event-sourced memory (4 types) |
| SAP-012 | development-lifecycle | active | 8-phase lifecycle (DDD→BDD→TDD) |
| SAP-013 | metrics-tracking | active | ROI calculator ($109k/year savings) ⚠️ incomplete |
| SAP-015 | task-tracking | pilot | Beads git-backed task memory |
| SAP-016 | link-validation | active | Markdown link validation (internal + external) |
| SAP-019 | sap-self-evaluation | active | SAP adoption assessment framework |
| SAP-027 | dogfooding-patterns | active | 5-week pilot methodology |
| SAP-028 | publishing-automation | pilot | PyPI OIDC trusted publishing |
| SAP-029 | sap-generation | pilot | Template-based SAP generation (80% savings) |

---

### Domain Navigation Shortcuts

**Building a capability server?**
→ Use SAP-047 (capability-server-template) - 5-minute setup with `scripts/create-capability-server.py`
→ Infrastructure + Developer Experience (SAP-042-047: multi-interface, registry, bootstrap, composition)

**Building a React app?**
→ Infrastructure + Developer Experience + Foundation (SAP-020-022) + User-Facing (SAP-023-024)

**Coordinating across repos?**
→ Infrastructure (SAP-001 Inbox) + Specialized (SAP-015 Beads)

**Improving process maturity?**
→ Specialized domain (SAP-009, 010, 012, 015, 027)

**Need performance optimization?**
→ Advanced domain (SAP-025, 026)

**Need content generation?**
→ Advanced domain (SAP-017, 018 chora-compose)

---

**Full Catalog**: See [sap-catalog.json](sap-catalog.json) or [docs/skilled-awareness/INDEX.md](docs/skilled-awareness/INDEX.md)

---

## Example Claude Code Session

```markdown
User: "Help me set up task tracking for this project"

Claude (Phase 1: Orientation):
- Read /CLAUDE.md (this file) for project overview
- Navigate to docs/skilled-awareness/AGENTS.md
- Find SAP-015 (task-tracking) in catalog
- Read docs/skilled-awareness/task-tracking/AGENTS.md for quick overview

Claude (Phase 2: Implementation):
- Read docs/skilled-awareness/task-tracking/adoption-blueprint.md
- Follow step-by-step installation:
  1. Install beads CLI: npm install -g @beads/bd
  2. Initialize: bd init
  3. Create first tasks
  4. Update AGENTS.md with beads patterns

Claude (Phase 3: If Needed):
- Read protocol-spec.md for complete CLI reference
- Read capability-charter.md for design rationale
- Review integration patterns with SAP-001 and SAP-010

Result: SAP-015 successfully adopted, task tracking operational
```

---

## Support & Resources

### Documentation

- **SAP Framework**: [docs/skilled-awareness/sap-framework/](docs/skilled-awareness/sap-framework/)
- **Agent Awareness**: [docs/skilled-awareness/agent-awareness/](docs/skilled-awareness/agent-awareness/)
- **SAP Catalog**: [sap-catalog.json](sap-catalog.json)
- **SAP Index**: [docs/skilled-awareness/INDEX.md](docs/skilled-awareness/INDEX.md)

### Key Commands

```bash
# SAP discovery
cat sap-catalog.json | grep -A 10 '"id": "SAP-'

# Task tracking (if SAP-015 adopted)
bd ready --json
bd list --status open --json

# Coordination (if SAP-001 adopted)
cat inbox/coordination/active.jsonl

# Event history (if SAP-010 adopted)
tail -n 20 .chora/memory/events/development.jsonl
```

### Navigation

- **Need SAP documentation?** → [docs/skilled-awareness/AGENTS.md](docs/skilled-awareness/AGENTS.md)
- **Need developer setup?** → [docs/dev-docs/AGENTS.md](docs/dev-docs/AGENTS.md)
- **Need user guides?** → [docs/user-docs/AGENTS.md](docs/user-docs/AGENTS.md)
- **Need project plans?** → [docs/project-docs/AGENTS.md](docs/project-docs/AGENTS.md)

---

## Version History

- **1.0.0** (2025-11-04): Initial root CLAUDE.md for chora-base
  - Complete navigation tree to 4 domains
  - Progressive context loading strategy
  - Claude Code vs Claude Desktop patterns
  - Common workflows and pitfalls
  - SAP catalog quick reference

---

**Next Steps**:
1. Determine your task domain (user docs, dev docs, project docs, SAPs)
2. Navigate to appropriate domain AGENTS.md
3. Read domain CLAUDE.md for Claude-specific patterns
4. Dive into specific SAP or documentation as needed

**Remember**: "Nearest file wins" - progressively load context from root → domain → capability → feature → component.

Happy navigating! 🚀
