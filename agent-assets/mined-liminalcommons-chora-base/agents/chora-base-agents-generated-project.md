# AGENTS.md

This file provides machine-readable instructions for AI coding agents working with SAP Verification Test Server.

---

## Project Overview

**SAP Verification Test Server** is a Model Context Protocol (MCP) server that provides [describe your server's capabilities].

**Core Architecture:** [Describe your architecture pattern]
- [Key architecture point 1]
- [Key architecture point 2]
- [Key architecture point 3]

**Key Components:**
- **Main Module** (`[main_module].py`) - [Description]
- **[Component 2]** (`[module].py`) - [Description]
- **[Component 3]** (`[module].py`) - [Description]

### Strategic Context

**Current Priority:** [Describe current sprint/milestone focus]
- See [ROADMAP.md](ROADMAP.md) for committed work
- Focus: [List 2-3 key deliverables]

**Long-Term Vision:** [Describe evolutionary direction]
- See [dev-docs/vision/](dev-docs/vision/) for future capabilities
- Waves: [List 2-4 high-level capability themes]

**Design Principle:** Deliver current commitments while keeping future doors open.
- Don't build future features now
- Do design extension points and document decisions
- Do refactor when it serves both present and future

---

## Development Process

This project follows the **chora-base 8-phase evidence-based development lifecycle**.

### 8-Phase Lifecycle

1. **Vision & Strategy** → [ROADMAP.md](ROADMAP.md)
2. **Planning** → [Sprint Planning](project-docs/sprints/README.md)
3. **Requirements & Design** → [DDD Workflow](dev-docs/workflows/DDD_WORKFLOW.md) (saves 8-15 hours per feature)
4. **Development** → [BDD](dev-docs/workflows/BDD_WORKFLOW.md) + [TDD](dev-docs/workflows/TDD_WORKFLOW.md) (40-80% fewer defects)
5. **Testing & Quality** → Built into all workflows
6. **Review & Integration** → [Pull Request workflow](#pull-request-workflow)
7. **Release & Deployment** → [Release Planning](project-docs/releases/RELEASE_PLANNING_GUIDE.md)
8. **Monitoring & Feedback** → [Process Metrics](project-docs/metrics/PROCESS_METRICS.md)

### Quick Reference for AI Agents

**Decision Trees:**
- **Write docs first?** → **YES** ([DDD Workflow](dev-docs/workflows/DDD_WORKFLOW.md) saves 8-15 hours)
- **Write acceptance tests first?** → **YES** ([BDD Workflow](dev-docs/workflows/BDD_WORKFLOW.md) prevents 2-5 issues)
- **Write unit tests first?** → **YES** ([TDD Workflow](dev-docs/workflows/TDD_WORKFLOW.md) reduces defects 40-80%)
- **Sprint commitment?** → **<80% capacity** ([Sprint Planning](project-docs/sprints/README.md) for predictable velocity)

**Complete Process Guide:**
- [DEVELOPMENT_PROCESS.md](dev-docs/workflows/DEVELOPMENT_PROCESS.md) - End-to-end workflow
- [DEVELOPMENT_LIFECYCLE.md](dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md) - How phases connect
- [FEATURE_WALKTHROUGH.md](dev-docs/examples/FEATURE_WALKTHROUGH.md) - Real OAuth2 example (14 days, 27% efficiency gain)

**Evidence-Based Results:**
- 40-80% defect reduction (Microsoft Research on TDD)
- 8-15 hours saved per feature (DDD prevents rework)
- 2-5 acceptance issues prevented per feature (BDD catches misalignment)
- 80-90% sprint velocity (predictable delivery with <80% commitment)

### Claude-Specific Optimizations

**For Claude Code users:** See [CLAUDE.md](CLAUDE.md) for Claude-specific patterns including:
- 200k context window management
- Artifact-first development
- Progressive context loading
- Checkpoint patterns
- ROI metrics tracking

---

## Documentation Structure (Nearest File Wins)

**SAP Verification Test Server uses nested AGENTS.md files** for focused, topic-specific guidance.

**Discovery principle**: Agents should read the AGENTS.md file nearest to the code they're working on.

### Available Guides

**Generic AI Agent Guidance (AGENTS.md):**
- **[AGENTS.md](AGENTS.md)** (this file) - Project overview, architecture, PR workflow, common tasks
- **[tests/AGENTS.md](tests/AGENTS.md)** - Testing guide (run tests, coverage, linting, troubleshooting)
- **[.chora/memory/AGENTS.md](.chora/memory/AGENTS.md)** - Memory system (event log, knowledge graph, A-MEM workflows)
- **[docker/AGENTS.md](docker/AGENTS.md)** - Docker operations (build, deploy, troubleshooting)
- **[scripts/AGENTS.md](scripts/AGENTS.md)** - Automation scripts reference

**Claude-Specific Guidance (CLAUDE.md):**
- **[CLAUDE.md](CLAUDE.md)** - Claude-specific optimizations (200k context, artifacts, checkpoints)
- **[tests/CLAUDE.md](tests/CLAUDE.md)** - Claude test generation patterns
- **[.chora/memory/CLAUDE.md](.chora/memory/CLAUDE.md)** - Claude memory integration patterns
- **[docker/CLAUDE.md](docker/CLAUDE.md)** - Claude Docker patterns
- **[scripts/CLAUDE.md](scripts/CLAUDE.md)** - Claude automation patterns

**When to use which guide:**

| Working on... | Read... |
|---------------|---------|
| Writing/running tests | [tests/AGENTS.md](tests/AGENTS.md) + [tests/CLAUDE.md](tests/CLAUDE.md) (if using Claude) |
| Cross-session learning, memory queries | [.chora/memory/AGENTS.md](.chora/memory/AGENTS.md) + [.chora/memory/CLAUDE.md](.chora/memory/CLAUDE.md) (if using Claude) |
| Docker builds, container deployment | [docker/AGENTS.md](docker/AGENTS.md) + [docker/CLAUDE.md](docker/CLAUDE.md) (if using Claude) |
| Automation scripts, justfile tasks | [scripts/AGENTS.md](scripts/AGENTS.md) + [scripts/CLAUDE.md](scripts/CLAUDE.md) (if using Claude) |
| Architecture, PRs, project structure | [AGENTS.md](AGENTS.md) (this file) + [CLAUDE.md](CLAUDE.md) (if using Claude) |

---

## Dev Environment Tips

### Prerequisites
- **Python 3.11+** required (3.11+ recommended)
- **Git** for version control
- **just** (optional but recommended) - Task runner for common commands
- **[Add project-specific prerequisites]**

### Installation

```bash
# Clone repository
git clone https://github.com/sapverifier/sap-verification-test-server.git
cd sap-verification-test-server

# One-command setup (recommended)
./scripts/setup.sh

# Manual setup alternative
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
pre-commit install
```

### Environment Variables

Create a `.env` file in project root:

```env
# Application configuration
SAP_VERIFICATION_TEST_SERVER_LOG_LEVEL=INFO     # DEBUG, INFO, WARNING, ERROR, CRITICAL
SAP_VERIFICATION_TEST_SERVER_DEBUG=0             # Set to 1 for debug mode

# Add your environment variables here
```

### Client Configuration

#### Claude Desktop (macOS)

**Development Mode (Editable Install):**
```json
{
  "mcpServers": {
    "sap-verification-test-server-dev": {
      "command": "/path/to/sap-verification-test-server/.venv/bin/python",
      "args": ["-m", "sap_verification_test_server.server"],
      "cwd": "/path/to/sap-verification-test-server",
      "env": {
        "SAP_VERIFICATION_TEST_SERVER_DEBUG": "1"
      }
    }
  }
}
```

**Production Mode (Installed Package):**
```json
{
  "mcpServers": {
    "sap-verification-test-server": {
      "command": "sap-verification-test-server",
      "args": [],
      "env": {}
    }
  }
}
```

**Config file location:** `~/Library/Application Support/Claude/claude_desktop_config.json`

#### Cursor

See `.config/cursor-mcp.example.json` for complete examples.

**Config file location:** `~/.cursor/mcp.json`

---

## Python Utilities (Optional Ergonomics)

This project includes reusable utilities that implement proven patterns from production Python projects. These are **optional affordances** — you can use them where helpful or ignore them.

### Available Utilities

| Utility | Purpose | Example Use |
|---------|---------|-------------|
| **validation.py** | Input normalization (dict/JSON/KV) | `@normalize_input(params=InputFormat.DICT_OR_JSON)` |
| **responses.py** | Response standardization | `Response.success(action="created", data=server)` |
| **errors.py** | Error formatting with suggestions | `ErrorFormatter.not_found("server", id, available)` |
| **persistence.py** | State persistence (atomic writes) | `class MyApp(StatefulObject): ...` |

### When to Use

**✅ Use when:**
- Building user-facing APIs or CLIs
- Need consistent response/error formats
- Want to reduce boilerplate code
- Need crash-safe state persistence

**⚠️ Skip when:**
- Building simple internal functions
- Framework provides equivalent (FastAPI, Click decorators)
- Prototyping (can add later)

### Quick Examples

**Input Validation:**
```python
from sap_verification_test_server.utils.validation import normalize_input, InputFormat
from sap_verification_test_server.utils.responses import Response

@normalize_input(params=InputFormat.DICT_OR_JSON)
def create_resource(name: str, params: dict | None = None):
    # params accepts: {"key": "value"} OR '{"key": "value"}'
    # Auto-converted to dict
    return Response.success(action="created", data={"name": name})
```

**Error Formatting:**
```python
from sap_verification_test_server.utils.errors import ErrorFormatter

def get_server(server_id: str):
    if server_id not in servers:
        error_msg = ErrorFormatter.not_found(
            entity_type="server",
            entity_id=server_id,
            available=list(servers.keys()),
        )
        return Response.error(error_code="not_found", message=error_msg)
```

**State Persistence:**
```python
from sap_verification_test_server.utils.persistence import StatefulObject

class ConfigManager(StatefulObject):
    def __init__(self):
        super().__init__(state_file="~/.sap_verification_test_server/config.json")
        self.config = getattr(self, 'config', {})  # Restored or default

    def update(self, settings: dict):
        self.config.update(settings)
        self._save_state()  # Atomic write
```

### Documentation

- **Reference Guide:** [user-docs/reference/python-patterns.md](user-docs/reference/python-patterns.md)
  - Complete API reference for all utilities
  - When to use each pattern
  - Performance and security considerations

- **How-To Guides:**
  - [How-To: Use Input Validation](user-docs/how-to/use-input-validation.md)
  - [How-To: Standardize Responses](user-docs/how-to/standardize-responses.md)
  - [How-To: Improve Error Messages](user-docs/how-to/improve-error-messages.md)
  - [How-To: Persist Application State](user-docs/how-to/persist-application-state.md)

### Benefits

**Code Reduction:**
- Input parsing: ~90% less boilerplate (20 lines → 1 decorator)
- Response building: ~80-85% reduction (10-15 lines → 2-3 lines)
- State persistence: ~70-75% reduction (25-30 lines → 7-8 lines)
- Bonus: Atomic writes prevent corruption (would add ~15 lines manually)

**Quality:**
- Consistent API responses across all endpoints
- Helpful error messages with fuzzy matching suggestions
- Crash-safe persistence (atomic writes with fsync)

### Implementation Notes

**All utilities:**
- Use Python stdlib only (no external dependencies)
- Work with both sync and async functions
- Include comprehensive test suites (90%+ coverage)
- Follow type hints for IDE support

**Performance:**
- Input validation: <1ms overhead (JSON parsing main cost)
- Response building: Negligible (dict construction)
- Error formatting: <1ms for fuzzy matching (<1000 items)

**Persistence:**
- Atomic writes add ~5-10ms latency (ensures durability)
- Keep state files <1MB for best performance
- JSON-only (use encryption for sensitive data)

---

## Testing Instructions

### Test Tiers

**Tier 1: Smoke Tests** (~10 sec)
```bash
just smoke        # or ./scripts/smoke-test.sh
```
- Purpose: Quick validation (imports, basic functionality)
- When: Before every commit
- Coverage: Core critical paths only

**Tier 2: Unit Tests** (~30-60 sec)
```bash
just test         # or pytest
```
- Purpose: Comprehensive unit testing
- When: Before creating PR, after significant changes
- Coverage: ≥85% required

**Tier 3: Integration Tests** (~2-5 min)
```bash
just test-integration   # or pytest tests/integration/
```
- Purpose: End-to-end validation
- When: Before merging to main, before releases
- Coverage: Critical user workflows

### Running Tests

**Basic commands:**
```bash
# All tests
pytest

# With coverage
pytest --cov=sap_verification_test_server --cov-report=html --cov-report=term

# Specific test file
pytest tests/test_server.py

# Specific test function
pytest tests/test_server.py::test_example_tool

# Watch mode (re-run on file changes)
pytest-watch

# Parallel execution (faster)
pytest -n auto
```

**Using justfile (recommended):**
```bash
just test              # Full test suite with coverage
just smoke             # Quick smoke tests
just test-coverage     # Tests with HTML coverage report
just test-watch        # Watch mode
```

### Coverage Requirements

**Target:** ≥85% overall coverage

**Check coverage:**
```bash
pytest --cov=sap_verification_test_server --cov-report=term-missing

# View HTML report
pytest --cov=sap_verification_test_server --cov-report=html
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

**Exclusions (acceptable):**
- `if __name__ == "__main__":` blocks
- Type checking code (`if TYPE_CHECKING:`)
- Defensive assertions (`assert`, debug code)
- Abstract base classes

### Linting & Type Checking

**Code quality checks:**
```bash
# Linting
ruff check src/sap_verification_test_server tests
ruff check --fix src/sap_verification_test_server tests  # Auto-fix

# Formatting
black src/sap_verification_test_server tests
black --check src/sap_verification_test_server tests  # Check only

# Type checking
mypy src/sap_verification_test_server
```

**Using justfile:**
```bash
just lint          # Check all (ruff + black + mypy)
just lint-fix      # Auto-fix issues
just format        # Format code
just typecheck     # Type checking only
```

### Pre-commit Hooks

**Installed automatically by `./scripts/setup.sh`**

**Manual installation:**
```bash
pre-commit install
```

**Run hooks manually:**
```bash
pre-commit run --all-files
```

**Hooks configured:**
- ruff (linting)
- black (formatting)
- mypy (type checking)
- trailing whitespace removal
- YAML/JSON validation
- Large file prevention

### Troubleshooting Tests

**Issue: Import errors**
```bash
# Solution: Install in editable mode
pip install -e ".[dev]"
```

**Issue: Tests fail in CI but pass locally**
```bash
# Common causes:
# 1. Environment differences (check Python version)
# 2. Missing dependencies (check pyproject.toml)
# 3. Test order dependency (use --random-order to catch)
pytest --random-order
```

**Issue: Coverage below threshold**
```bash
# View uncovered lines
pytest --cov=sap_verification_test_server --cov-report=term-missing

# Focus on specific file
pytest --cov=sap_verification_test_server.module --cov-report=term-missing tests/test_module.py
```

---

## PR Instructions

### Branch Naming

```
feature/descriptive-name     # New features
fix/issue-description        # Bug fixes
hotfix/critical-fix          # Production hotfixes
docs/documentation-update    # Documentation only
refactor/code-improvement    # Refactoring
```

### Commit Message Format

Follow **Conventional Commits** style:

```
type(scope): brief description

Detailed explanation of changes (if needed)

Closes #issue-number
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`

**Scopes:** [List your project-specific scopes]

**Examples:**
```
feat(core): add new feature X

Implement feature X with comprehensive error handling
and unit tests.

Closes #23

---

fix(server): handle edge case gracefully

When [condition], system now [behavior] instead of
crashing.

Fixes #45
```

### PR Checklist

**Before opening PR:**
- [ ] Branch is up to date with `main`
- [ ] All tests pass locally (`just test` or `pytest`)
- [ ] Coverage maintained or improved (≥85%)
- [ ] Linting passes (`just lint` or `ruff check`)
- [ ] Type checking passes (`just typecheck` or `mypy src/`)
- [ ] Pre-commit hooks pass (`just pre-commit` or `pre-commit run --all-files`)
- [ ] Code formatted (`just format` or `black src/ tests/`)

**Documentation (if applicable):**
- [ ] README.md updated (if user-facing changes)
- [ ] AGENTS.md updated (if agent workflow changes)
- [ ] API reference docs updated (if new tools/capabilities)
- [ ] CHANGELOG.md entry added (for releases)

**Testing:**
- [ ] Unit tests added/updated
- [ ] Integration tests added (if applicable)
- [ ] Smoke tests pass (`just smoke`)
- [ ] Manual testing completed

**Review:**
- [ ] Self-review completed
- [ ] Code follows project style guide
- [ ] No debug code or commented-out code
- [ ] Error messages are clear and actionable
- [ ] Logging statements use appropriate levels

### Quality Gates (must pass)

1. **Lint:** `ruff check` → No errors
2. **Format:** `black --check` → Formatted
3. **Types:** `mypy` → Type safe
4. **Tests:** All tests pass
5. **Coverage:** ≥85%
6. **Pre-commit:** All hooks pass

### PR Review Process

- **Required approvals:** 1+ reviewer
- **Merge strategy:** Squash and merge (clean history)
- **CI/CD:** All quality gates must pass
- **Timeline:** Most PRs reviewed within 24-48 hours

### CI/CD Expectations

**GitHub Actions workflows:**

1. **test.yml** - Full test suite on every push/PR
   - Runs: `pytest` with coverage
   - Required: ≥85% coverage
   - Triggers: Push to all branches, pull requests

2. **lint.yml** - Code quality checks
   - Runs: `ruff check`, `black --check`, `mypy`
   - Required: No linting errors, formatted code, type-safe
   - Triggers: Push to all branches, pull requests

3. **smoke.yml** - Quick smoke tests
   - Runs: Fast validation tests (<30s)
   - Required: Basic functionality works
   - Triggers: Every push (fast feedback)

4. **docker.yml** - Container builds
   - Runs: `docker build`, `docker-compose up`, health checks
   - Required: Image builds successfully, services start healthy
   - Triggers: Push to main, pull requests touching Docker files

5. **release.yml** - Automated releases
   - Runs: Version bump, changelog, PyPI publish
   - Required: Tests pass, version valid, PyPI credentials configured
   - Triggers: Manual workflow dispatch, tags

6. **codeql.yml** - Security scanning
   - Runs: CodeQL analysis for vulnerabilities
   - Required: No critical security issues
   - Triggers: Weekly schedule, pull requests

7. **dependency-review.yml** - Dependency vulnerabilities
   - Runs: Dependency vulnerability scanning
   - Required: No high/critical vulnerabilities in new dependencies
   - Triggers: Pull requests

**What CI will check before merge:**

```bash
# Locally verify CI will pass
just pre-merge

# This runs the same checks as CI:
# 1. Linting: ruff check → No errors
# 2. Formatting: black --check → Code formatted
# 3. Type checking: mypy → Type-safe
# 4. Tests: pytest → All tests pass
# 5. Coverage: pytest --cov → ≥85%
# 6. Docker: docker build → Image builds successfully
```

**For agents:** Run `just pre-merge` before creating PRs to avoid CI failures.

**CI failure recovery:**
1. Check workflow logs in GitHub Actions tab
2. Run failing command locally to reproduce
3. Fix issue and push new commit (CI will re-run)
4. If tests pass locally but fail in CI, check for environment differences

---

## Architecture Overview

[Describe your project's architecture here. Include diagrams, key design patterns, and architectural decisions.]

### Key Design Patterns

- **[Pattern 1]:** [Description]
- **[Pattern 2]:** [Description]
- **[Pattern 3]:** [Description]

### Configuration Management

- **Environment Variables:** `.env` file (not committed)
- **Defaults:** Sensible defaults in code
- **Validation:** On startup, fail fast if misconfigured

---

## Key Constraints & Design Decisions

### Target Audience

**Primary:** AI Coding Agents
- Machine-readable instructions (this file)
- Stateful memory for cross-session learning
- Clear error messages with remediation steps

**Secondary:** Human Developers
- Comprehensive documentation (README, dev-docs/)
- Quick-start scripts (./scripts/setup.sh)
- Standard Python tooling (pytest, ruff, black)

**Design Implications:**
- AGENTS.md is authoritative (maintain carefully)
- Error messages include "what to do next"
- Documentation follows Diátaxis framework

### [Additional Constraints]

[Document your project-specific constraints here]
- Performance requirements
- Security considerations
- Compatibility requirements

---

## Strategic Design

### Balancing Current Priorities with Future Vision

**Current Focus:** v0.1.0 - [Describe current milestone]
- See [ROADMAP.md](ROADMAP.md) for committed features
- Priority: Deliver current sprint goals

**Future Vision:** Post-v0.1.0 capabilities
- See [dev-docs/vision/](dev-docs/vision/) for exploratory ideas
- Status: Not committed (evaluate after current milestone)

**Key Principle:** Build for today, design for tomorrow.

### Vision-Aware Implementation Pattern

When implementing features, consider future extensibility:

**1. Identify Extension Points**
```python
# Example: Plugin system hook point
class ToolRegistry:
    def __init__(self):
        self._tools = {}
        # Future: Load from external plugins
        self._load_builtin_tools()
    
    def _load_builtin_tools(self):
        # Current: Builtin tools only
        pass
    
    # Extension point for future plugin system
    def register_tool(self, tool):
        self._tools[tool.name] = tool
```

**2. Document Design Decisions**
```python
# Decision: Use dict for tool storage
# Rationale: Fast lookup (O(1)), simple to implement
# Future consideration: If tools exceed 1000, consider indexed storage
# See: dev-docs/decisions/ADR-001-tool-registry.md
```

**3. Keep Future Doors Open**
- Avoid hardcoding limits unnecessarily
- Use interfaces/protocols for extensibility
- Document "why" not just "what"

### Practical Examples

**Example 1: Adding a New Tool (Current Priority)**
```python
# Implementation: Focus on current needs
@mcp.tool()
async def example_tool(param: str) -> dict:
    """Example tool for current milestone."""
    # Implement core functionality
    result = process_param(param)
    return {"result": result}

# Vision-aware: Document extension point
# Future: Could support tool chaining (see dev-docs/vision/CAPABILITY_EVOLUTION.md Wave 2)
# Design decision: Return dict (not string) to allow future enrichment
```

**Example 2: Defer Feature to Future Wave**
```python
# DO NOT implement now (deferred to Wave 2):
# - Tool chaining
# - External API integrations
# - Complex workflow orchestration

# DO document in vision:
# See dev-docs/vision/CAPABILITY_EVOLUTION.md:
# - Wave 2: Tool Chaining (post-v0.1.0)
# - Decision criteria: User demand + architecture validation
```

### Refactoring Decision Framework

**When to refactor now:**
- ✅ Serves current milestone (improves current features)
- ✅ Enables future extension (keeps doors open)
- ✅ Reduces technical debt (improves maintainability)

**When to defer:**
- ⏸️ Speculative (no clear current need)
- ⏸️ Adds complexity without immediate value
- ⏸️ Better done with more information later

### Capturing Knowledge for Future Agents

**Document in Vision Files:**
```markdown
# dev-docs/vision/CAPABILITY_EVOLUTION.md

## Wave 2: Tool Chaining (Exploratory)

**Trigger:** After v0.1.0 stabilizes + user demand signals

**Design Sketch:**
- Tool output becomes input to next tool
- DAG-based execution order
- Error handling: Rollback on failure

**Considerations:**
- Current architecture: Tools are independent (OK for Wave 1)
- Refactor needed: Tool registry + execution engine
- Estimated effort: 2-3 weeks
```

**Update Decision Records:**
```markdown
# dev-docs/decisions/ADR-002-tool-registry.md

## Context
We chose simple dict-based tool registry for v0.1.0.

## Decision
Use `Dict[str, Tool]` for tool storage.

## Consequences
**Positive:**
- Simple implementation (current need)
- Fast lookup O(1)

**Negative:**
- No ordering guarantees
- No dependency resolution

**Future:**
- If we add tool chaining (Wave 2), may need DAG-based registry
- Current design allows this refactor (tools are self-contained)
```

### Quick Reference: Strategic Design Checklist

When implementing features:
- [ ] Does this serve current milestone? (If no, defer)
- [ ] Does this keep future doors open? (Interfaces > implementations)
- [ ] Did I document the "why"? (Comments + decision records)
- [ ] Did I avoid building future features now? (Stay focused)
- [ ] Did I capture insights for future agents? (Vision docs)

---

## Common Tasks for Agents

### Task Discovery (START HERE)

**If you're an AI agent starting work on SAP Verification Test Server, start here:**

1. **Read project context:**
   - [README.md](README.md) - Project overview and features
   - [ROADMAP.md](ROADMAP.md) - Current priorities and vision
   - [dev-docs/DEVELOPMENT.md](dev-docs/DEVELOPMENT.md) - Architecture deep dive

2. **Check current status:**
   - [CHANGELOG.md](CHANGELOG.md) - Recent changes
   - [GitHub Issues](https://github.com/sapverifier/sap-verification-test-server/issues) - Known bugs and feature requests

3. **Find task-specific guidance:**
   - Testing → [tests/AGENTS.md](tests/AGENTS.md)
   - Memory system → [.chora/memory/AGENTS.md](.chora/memory/AGENTS.md)
   - Docker → [docker/AGENTS.md](docker/AGENTS.md)
   - Scripts → [scripts/AGENTS.md](scripts/AGENTS.md)

4. **Set up development environment:**
   ```bash
   ./scripts/setup.sh
   ```

5. **Run smoke test to verify setup:**
   ```bash
   just smoke
   ```

### Common Workflows

**Add a New MCP Tool:**
1. Create tool function in `src/sap_verification_test_server/mcp/server.py`
2. Add `@mcp.tool()` decorator
3. Write docstring (becomes tool description)
4. Add unit tests in `tests/test_server.py`
5. Update AGENTS.md with tool documentation
6. Run `just test` to verify
7. Create PR

**Fix a Bug:**
1. Reproduce bug locally
2. Write failing test that captures bug
3. Fix bug in source code
4. Verify test now passes
5. Run `just pre-merge` to ensure quality gates pass
6. Create PR with "fix:" commit message

**Add Documentation:**
1. Identify documentation type (tutorial/how-to/reference/explanation)
2. Create file in appropriate directory (user-docs/, dev-docs/, project-docs/)
3. Follow [DOCUMENTATION_STANDARD.md](DOCUMENTATION_STANDARD.md)
4. Add to relevant navigation/index
5. Create PR with "docs:" commit message

**Update Dependencies:**
1. Update version in `pyproject.toml`
2. Run `pip install -e ".[dev]"` to update lock file
3. Run full test suite (`just test`)
4. Check for deprecation warnings
5. Update code if needed
6. Create PR

---

## Memory System (Agent Learning)

This project includes a cross-session memory system for AI agents.

### Event Log

**Purpose:** Record significant events across sessions

**Location:** `.chora/memory/events/`

**Usage:**
```python
from sap_verification_test_server.memory.event_log import EventLog

# Log events
event_log = EventLog()
event_log.log_event(
    event_type="tool_execution",
    status="success",
    details={"tool": "example_tool", "duration_ms": 45},
    trace_id=trace_context.get_trace_id()
)

# Query events
events = event_log.query_events(
    event_type="tool_execution",
    since="24h"
)
```

**CLI:**
```bash
sap-verification-test-server-memory query --type "tool_execution" --since "24h"
sap-verification-test-server-memory trace abc-123-def
```

### Knowledge Graph

**Purpose:** Store learned insights and relationships

**Location:** `.chora/memory/knowledge/`

**Usage:**
```python
from sap_verification_test_server.memory.knowledge_graph import KnowledgeGraph

# Add knowledge note
kg = KnowledgeGraph()
kg.add_note(
    title="Tool Error Pattern",
    content="Tool X fails when parameter Y is null. Add validation.",
    tags=["bug", "tool-x"],
    confidence="high",
    links=["error-handling-best-practices"]
)

# Search knowledge
notes = kg.search(tag="bug", confidence="high")
```

**CLI:**
```bash
sap-verification-test-server-memory knowledge search --tag "bug"
sap-verification-test-server-memory knowledge create --title "..." --content "..."
```

### Trace Context

**Purpose:** Correlate events across tool calls

**Usage:**
```python
from sap_verification_test_server.memory.trace import TraceContext, get_trace_id

# In tool code
trace_id = get_trace_id()  # From CHORA_TRACE_ID env var

# Log with trace correlation
event_log.log_event(
    event_type="tool_execution",
    trace_id=trace_id  # Links events in same trace
)
```

### A-MEM Workflow (Agent Memory)

**Pattern:** Learn from errors and improve over time

1. **Execute task** → Log event (success/failure)
2. **On failure** → Create knowledge note with fix
3. **Next session** → Query knowledge before similar task
4. **Apply learnings** → Avoid previous errors

**Example:**
```python
# Session 1: Encounter error
try:
    result = risky_operation()
except ValidationError as e:
    # Log failure
    event_log.log_event("operation_failed", status="error", details={"error": str(e)})
    
    # Capture knowledge
    kg.add_note(
        title="risky_operation requires validation",
        content="Always validate input X before calling risky_operation",
        tags=["error", "validation"],
        confidence="high"
    )

# Session 2: Apply learning
# Query knowledge first
learnings = kg.search(tag="validation")
# Apply validation based on previous learning
if learnings:
    validate_input(x)
result = risky_operation()  # Succeeds this time
```

---

## Project Structure

```
sap-verification-test-server/
├── .chora/
│   └── memory/               # Agent memory system
│       ├── events/           # Event log (gitignored)
│       ├── knowledge/        # Knowledge notes (gitignored)
│       └── profiles/         # Agent profiles (gitignored)
├── .github/
│   └── workflows/            # CI/CD workflows
├── dev-docs/                 # Developer documentation
│   ├── CONTRIBUTING.md
│   ├── DEVELOPMENT.md
│   ├── TROUBLESHOOTING.md
│   └── vision/               # Strategic design docs
├── project-docs/
│   ├── ROADMAP.md            # Committed features
│   └── releases/             # Release notes
├── user-docs/                # User documentation
│   ├── tutorials/
│   ├── how-to/
│   ├── reference/
│   └── explanation/
├── scripts/                  # Automation scripts
│   ├── setup.sh
│   ├── smoke-test.sh
│   └── pre-merge.sh
├── src/sap_verification_test_server/   # Source code
│   ├── __init__.py
│   ├── mcp/
│   │   ├── __init__.py
│   │   └── server.py         # MCP server implementation
│   ├── memory/               # Memory system
│   │   ├── event_log.py
│   │   ├── knowledge_graph.py
│   │   └── trace.py
│   └── utils/                # Utilities
│       ├── validation.py
│       ├── responses.py
│       ├── errors.py
│       └── persistence.py
├── tests/                    # Test suite
│   ├── test_server.py
│   ├── test_memory.py
│   └── integration/
├── .env.example              # Example environment variables
├── .gitignore
├── .pre-commit-config.yaml
├── AGENTS.md                 # This file
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml            # Project configuration
├── README.md
└── justfile                  # Task automation
```

---

## Troubleshooting

### Common Issues

**Import errors:**
```bash
# Solution: Reinstall in editable mode
pip install -e ".[dev]"
```

**Tests failing:**
```bash
# Check test output
pytest -v

# Run specific test
pytest tests/test_server.py::test_specific -v
```

**Coverage below threshold:**
```bash
# View uncovered lines
pytest --cov=sap_verification_test_server --cov-report=term-missing
```

**Pre-commit hooks failing:**
```bash
# Run hooks manually
pre-commit run --all-files

# Auto-fix what's possible
ruff check --fix src/ tests/
black src/ tests/
```

### Getting Help

- **Issues:** [GitHub Issues](https://github.com/sapverifier/sap-verification-test-server/issues)
- **Discussions:** [GitHub Discussions](https://github.com/sapverifier/sap-verification-test-server/discussions)
- **Documentation:** [dev-docs/TROUBLESHOOTING.md](dev-docs/TROUBLESHOOTING.md)

---

**Last Updated:** 0.1.0
**Maintained By:** AI Coding Agents + Human Developers
