# CLAUDE.md - Claude-Specific Development Guide

**For SAP Verification Test Server**

This file provides **Claude-specific** optimizations and patterns for working with SAP Verification Test Server.

**Read first:** [AGENTS.md](AGENTS.md) contains generic AI agent guidance (project structure, conventions, workflows). This file builds on that foundation with Claude-specific optimizations.

---

## Quick Start for Claude

### Reading Order

1. **[AGENTS.md](AGENTS.md)** - Project overview, architecture, development workflows
2. **CLAUDE.md** (this file) - Claude-specific optimizations
3. **[/claude/](../../claude/)** - Advanced pattern library (in chora-base repository)

### What Makes This Claude-Specific?

Unlike generic AI agents, Claude has unique capabilities this guide optimizes for:

- **200k token context window** - Sophisticated state management across long sessions
- **Artifact generation** - Native support for structured code/document output
- **Multi-tool orchestration** - Web search, file operations, computational tools
- **Safety-conscious** - Built-in guardrails for secure development
- **Conversational autonomy** - Intent interpretation and adaptive execution

---

## Claude Capabilities Matrix

| Capability | Claude Strength | Implementation Strategy |
|------------|-----------------|------------------------|
| **Code Generation** | Excellent (50+ languages) | Provide clear specs with example patterns |
| **Architecture Design** | Strong systems thinking | Request architectural diagrams alongside code |
| **Debugging** | Exceptional error analysis | Share full error traces and context |
| **Documentation** | Native markdown expertise | Request inline docs with code generation |
| **Testing** | Comprehensive coverage | Ask for tests in same request as implementation |
| **Refactoring** | Pattern recognition excellence | Provide before/after examples for style matching |

---

## Context Window Management (200k Tokens)

Claude's 200k token context enables sophisticated state management. Use **progressive context loading**:

### Progressive Context Loading Strategy

#### Phase 1: Essential Context (0-10k tokens)
**Load immediately at session start:**
- Current task definition
- Relevant AGENTS.md section
- Active file contents (1-3 files you're working on)
- Recent conversation summary (if continuing session)

#### Phase 2: Extended Context (10-50k tokens)
**Load as needed for implementation:**
- Related module code
- Test suites for affected components
- Recent git history (`git log --oneline -20`)
- Related documentation files

#### Phase 3: Full Context (50-200k tokens)
**Load for complex refactoring or architectural work:**
- Complete codebase structure
- Full test suite
- All documentation
- Historical decisions from knowledge graph

### Context Preservation

**After every 5-10 interactions, create a checkpoint:**

```markdown
## Claude Session Checkpoint

**Date:** YYYY-MM-DD
**Task:** [Current task description]

### Completed
- ✅ Task 1
- ✅ Task 2

### In Progress
- 🔄 Task 3 (50% complete)

### Key Decisions
- Decision 1: Rationale
- Decision 2: Rationale

### Next Steps
1. Step 1
2. Step 2
```

**Save checkpoints to:** `.chora/memory/claude-checkpoints/YYYY-MM-DD-session.md`

For detailed checkpoint patterns, see: [/claude/CHECKPOINT_PATTERNS.md](../../claude/CHECKPOINT_PATTERNS.md) (in chora-base repo)

---

## Development Workflows (DDD → BDD → TDD)

SAP Verification Test Server follows the **chora-base evidence-based development lifecycle**.

### Integration with Claude's Strengths

**Claude excels at this workflow because:**
- Conversational nature aligns with iterative refinement (DDD → BDD → TDD)
- Can generate docs, tests, and code in single cohesive session
- Strong pattern recognition helps maintain consistency
- Context window holds entire feature context (design → implementation → tests)

### Quick Reference

**Phase 1: Documentation-Driven Design (DDD)**
- See [dev-docs/workflows/DDD_WORKFLOW.md](dev-docs/workflows/DDD_WORKFLOW.md)
- **Claude advantage:** Native markdown expertise, can draft comprehensive specs
- **Pattern:** "Document the [feature] API/behavior before implementation"
- **Time saved:** 8-15 hours per feature (prevents rework)

**Phase 2: Behavior-Driven Development (BDD)**
- See [dev-docs/workflows/BDD_WORKFLOW.md](dev-docs/workflows/BDD_WORKFLOW.md)
- **Claude advantage:** Excellent at Gherkin scenario generation
- **Pattern:** "Generate acceptance tests for [feature] covering happy path and 5 edge cases"
- **Issues prevented:** 2-5 acceptance issues per feature

**Phase 3: Test-Driven Development (TDD)**
- See [dev-docs/workflows/TDD_WORKFLOW.md](dev-docs/workflows/TDD_WORKFLOW.md)
- **Claude advantage:** Can write test + implementation together, ensuring alignment
- **Pattern:** "Write failing test for [function], then implement to pass"
- **Defect reduction:** 40-80% (Microsoft Research)

**Complete Example:**
- [dev-docs/examples/FEATURE_WALKTHROUGH.md](dev-docs/examples/FEATURE_WALKTHROUGH.md)
- Real OAuth2 feature: 14 days, 56 hours, 27% efficiency gain

---

## Artifact-First Development

Claude's artifact generation is ideal for SAP Verification Test Server development.

### When to Use Artifacts

**✅ Use artifacts for:**
- Complete Python modules (< 500 lines)
- Configuration files (pyproject.toml, docker-compose.yml)
- Documentation files (README sections, API docs)
- Test suites
- Code that will be directly copied to files

**❌ Don't use artifacts for:**
- Small code snippets (< 20 lines) - inline markdown is clearer
- Exploratory explanations - conversational format better
- Multi-file changes spanning many files - describe changes instead

### Artifact Best Practices

```markdown
# Good Artifact Request
"Create a new FastMCP tool for listing servers. Include:
- Type hints and docstrings
- Error handling for missing servers
- Unit tests (pytest)
- Follow existing patterns in src/sap_verification_test_server/mcp/tools.py"

# Less Effective
"Make a server list function"
```

---

## Multi-Tool Orchestration

Claude can use web search, file operations, and computational tools. Optimize for SAP Verification Test Server:

### Web Search Integration

**Automatic triggers for Claude:**
- Latest framework documentation (FastMCP, specific to version)
- Current best practices (security patterns, Python 3.11+ features)
- Recent package compatibility (dependency version conflicts)
- Error message solutions (stack trace + framework + year)

**Search templates:**
- `"FastMCP [feature] documentation 2024"`
- `"Python 3.11 [specific feature] best practices"`
- `"[Error message text] solution 2024"`

### File Operations Protocol

**Best practices for Claude:**

1. **Always read before modifying**
   ```python
   # Read current state
   with open('path/file.py') as f:
       content = f.read()

   # Modify
   # Write atomically
   ```

2. **Use project utilities**
   ```python
   from sap_verification_test_server.utils.persistence import StatefulObject
   # Atomic writes built-in
   ```

3. **Validate before writing**
   - Check syntax (Python: `ast.parse()`)
   - Run linter (`ruff check`)
   - Verify imports

---

## Testing with Claude

### Test Generation Pattern

When implementing features, use this request structure:

```markdown
"Implement [feature] with comprehensive tests:

1. **Implementation**: [requirements]
2. **Tests**: Generate using this pattern:
   - ✅ Happy path test
   - ✅ Edge cases (minimum 3)
   - ✅ Error conditions (all exceptions)
   - ✅ Boundary value tests
   - ✅ Integration test (if applicable)

3. **Fixtures**: Use pytest fixtures for common setup
4. **Documentation**: Docstrings explaining test purpose
5. **Organization**: @pytest.mark categories

Target coverage: 85%"
```

See [tests/CLAUDE.md](tests/CLAUDE.md) for Claude-specific test patterns.

---

## Code Review with Claude

### Review Request Template

```markdown
# Code Review Request

Claude, please review this code for:

## Functionality
- [ ] Correct implementation of requirements
- [ ] Edge case handling
- [ ] Error handling completeness

## Performance
- [ ] Time complexity analysis
- [ ] Space complexity concerns
- [ ] Database query optimization (if applicable)

## Security
- [ ] Input validation
- [ ] Injection prevention (SQL, command, etc.)
- [ ] Authentication/authorization checks
- [ ] Sensitive data handling

## Maintainability
- [ ] Code readability
- [ ] Documentation completeness
- [ ] Test coverage (target: 85%)
- [ ] SOLID principles adherence

## Project-Specific
- [ ] Follows patterns in [relevant module]
- [ ] Consistent with [architecture decision]
```

---

## Memory System Integration

SAP Verification Test Server includes A-MEM (Agentic Memory) for cross-session learning.

### Claude-Specific Memory Patterns

**Tier 1: Ephemeral (Your Context Window)**
- Current conversation
- Working memory
- Temporary state

**Tier 2: Event Log (.chora/memory/events/)**
- Query for recent failures: `sap-verification-test-server-memory query --type app.failed --since 24h`
- Track multi-step workflows with trace IDs
- Analyze patterns across sessions

**Tier 3: Knowledge Graph (.chora/memory/knowledge/)**
- Search for proven solutions: `sap-verification-test-server-memory knowledge search --tag [topic]`
- Create notes for future reference
- Link related concepts (Zettelkasten-style)

**Best practice for Claude:**
After solving a non-trivial problem, create a knowledge note:

```bash
echo "Solution to [problem]: [approach]. Works because [reason]." | \
  sap-verification-test-server-memory knowledge create "[Problem Title]" \
  --tag problem-type --tag solution-pattern
```

See [.chora/memory/CLAUDE.md](.chora/memory/CLAUDE.md) for detailed patterns.

---

## Response Time Optimization

### Request Structuring for Speed

**Fast Responses (< 10 seconds):**
- Single file modifications
- Simple function implementations
- Documentation updates
- Configuration changes

**Medium Responses (10-30 seconds):**
- Multi-file refactoring
- Complex algorithm implementation
- Architecture design discussions
- Comprehensive test generation

**Long Responses (30+ seconds):**
- Full feature implementation (DDD → BDD → TDD)
- Large-scale refactoring
- Complete module generation

**Pro tip:** Break complex tasks into phases for faster iteration:
```markdown
"Let's implement [feature] in phases:
1. First, design the API interface
2. Then, implement core logic
3. Finally, add error handling and tests"
```

---

## Iteration Efficiency Patterns

### Single-Shot Success Pattern

**Maximize first-pass success:**

```markdown
"Implement [feature]:

**Specifications:**
- Input: [type, format, constraints]
- Output: [type, format]
- Behavior: [detailed description]

**Example:**
```python
# Input
input_data = {"key": "value"}

# Expected output
expected = {"result": "processed_value"}
```

**Edge cases:**
- Empty input: [expected behavior]
- Invalid input: [expected behavior]
- Null values: [expected behavior]

**Style reference:**
Follow patterns in [src/sap_verification_test_server/existing_module.py]
```

### Progressive Enhancement Pattern

**For iterative development:**

1. **Get working prototype** - Basic functionality
2. **Add error handling** - Graceful failure modes
3. **Optimize performance** - Profiling and improvements
4. **Add comprehensive tests** - Coverage target
5. **Polish documentation** - Inline docs and examples

---

## Advanced Patterns

### Socratic Development Pattern

For complex architectural decisions, engage Claude in exploratory dialogue:

```markdown
"I need to implement [complex feature]. Before we code, help me think through:
1. What are the key architectural decisions?
2. What trade-offs should I consider?
3. What edge cases might I overlook?
4. Are there existing patterns in this codebase I should follow?"
```

**Claude will provide:**
- Analytical questions to consider
- Architecture alternatives
- Pattern recommendations
- Risk identification

### Checkpoint Recovery Pattern

If Claude loses context mid-task:

```markdown
"Continuing from checkpoint:
- Completed: [list]
- Current file: [path]
- Working on: [specific task]
- Key decisions: [list]
- Next: [specific next step]"
```

---

## Metrics & ROI Tracking

SAP Verification Test Server includes `claude_metrics.py` for tracking Claude's effectiveness.

### Using the ROI Calculator

```python
from sap_verification_test_server.utils.claude_metrics import ClaudeMetric, ClaudeROICalculator

# Initialize calculator
calculator = ClaudeROICalculator(developer_hourly_rate=100)

# Log a session
metric = ClaudeMetric(
    session_id="session-001",
    timestamp=datetime.now(),
    task_type="feature_implementation",
    lines_generated=250,
    time_saved_minutes=120,  # 2 hours saved vs manual
    iterations_required=2,
    bugs_introduced=0,
    bugs_fixed=3,
    documentation_quality_score=8.5,
    test_coverage=0.92
)
calculator.add_metric(metric)

# Generate report
print(calculator.generate_report())
```

**See:** [/claude/METRICS_TRACKING.md](../../claude/METRICS_TRACKING.md) for detailed tracking patterns.

---

## Domain-Specific Guidance

**SAP Verification Test Server specifics:**

### MCP Server Development

- Use FastMCP framework for tool/resource/prompt definitions
- Follow MCP protocol specification
- Test with MCP Inspector: `npx @modelcontextprotocol/inspector sap_verification_test_server`

### Python Best Practices

- Python version: 3.11+
- Type hints required (enforced by mypy)
- Docstrings for all public APIs
- Follow PEP 8 (enforced by ruff)

### Project Structure

```
src/sap_verification_test_server/
├── mcp/              # MCP server implementation
│   ├── server.py     # FastMCP server
│   └── tools.py      # MCP tools
├── utils/            # Reusable utilities
└── memory/           # A-MEM implementation (optional)
```

---

## Nested CLAUDE.md Files

For specialized topics, see domain-specific CLAUDE.md files:

- **[tests/CLAUDE.md](tests/CLAUDE.md)** - Claude test generation patterns
- **[.chora/memory/CLAUDE.md](.chora/memory/CLAUDE.md)** - Claude memory integration
- **[docker/CLAUDE.md](docker/CLAUDE.md)** - Claude Docker assistance
- **[scripts/CLAUDE.md](scripts/CLAUDE.md)** - Claude automation patterns

---

## Pattern Library Reference

**Advanced patterns (in chora-base repository):**

- **[/claude/README.md](../../claude/README.md)** - Pattern library overview
- **[/claude/CONTEXT_MANAGEMENT.md](../../claude/CONTEXT_MANAGEMENT.md)** - 200k context optimization
- **[/claude/CHECKPOINT_PATTERNS.md](../../claude/CHECKPOINT_PATTERNS.md)** - State preservation
- **[/claude/METRICS_TRACKING.md](../../claude/METRICS_TRACKING.md)** - ROI calculation
- **[/claude/FRAMEWORK_TEMPLATES.md](../../claude/FRAMEWORK_TEMPLATES.md)** - Task templates

---

## Quick Reference Card

### Essential Commands for Claude

| Task | Prompt Template |
|------|----------------|
| **Generate Code** | "Implement [feature] following patterns in [file]" |
| **Debug** | "Debug this error: [error]. Context: [context]" |
| **Refactor** | "Refactor [code] to improve [metric]" |
| **Document** | "Document [code] with examples and edge cases" |
| **Test** | "Write comprehensive tests for [code] (85% coverage)" |
| **Review** | "Review [code] for security, performance, and style" |

### Do's and Don'ts

**✅ DO:**
- Provide clear success criteria
- Include example patterns from codebase
- Specify constraints upfront
- Request tests with implementation
- Ask for inline documentation
- Use progressive context loading

**❌ DON'T:**
- Dump entire codebase without context
- Use vague requirements
- Skip error handling requirements
- Forget to specify Python version (3.11)
- Ignore clarifying questions

---

## Getting Help

**For Claude-specific questions:**
1. Check [/claude/](../../claude/) pattern library
2. Review [CLAUDE_SETUP_GUIDE.md](../../docs/CLAUDE_SETUP_GUIDE.md)
3. See examples in [dev-docs/examples/](dev-docs/examples/)

**For project-specific questions:**
1. Read [AGENTS.md](AGENTS.md) first
2. Check nested AGENTS.md/CLAUDE.md for topic
3. Search knowledge graph: `sap-verification-test-server-memory knowledge search`

---

**Version:** 3.3.0
**Last Updated:** 2025-10-26
**Maintained by:** chora-base project
**License:** MIT