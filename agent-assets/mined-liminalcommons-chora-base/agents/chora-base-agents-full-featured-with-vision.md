# AGENTS.md

This file provides machine-readable instructions for AI coding agents working with Example MCP Server with Vision.

---

## Project Overview

**Example MCP Server with Vision** is a Model Context Protocol (MCP) server that provides [describe your server's capabilities].

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

## Dev Environment Tips

### Prerequisites
- **Python +** required (+ recommended)
- **Git** for version control
- **[Add project-specific prerequisites]**

### Installation

```bash
# Clone repository
git clone https://github.com//example-mcp-vision.git
cd example-mcp-vision

# One-command setup (recommended)
./scripts/setup.sh

# Manual setup alternative
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

### Environment Variables

Create a `.env` file in project root:

```env
# Application configuration
_LOG_LEVEL=INFO     # DEBUG, INFO, WARNING, ERROR, CRITICAL
_DEBUG=0             # Set to 1 for debug mode

# Add your environment variables here
```

### Client Configuration

#### Claude Desktop (macOS)

**Development Mode (Editable Install):**
```json
{
  "mcpServers": {
    "example-mcp-vision-dev": {
      "command": "/path/to/example-mcp-vision/.venv/bin/python",
      "args": ["-m", ".server"],
      "cwd": "/path/to/example-mcp-vision",
      "env": {
        "_DEBUG": "1"
      }
    }
  }
}
```

**Production Mode (Installed Package):**
```json
{
  "mcpServers": {
    "example-mcp-vision": {
      "command": "example-mcp-vision",
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

## Testing Instructions

### Run All Tests

```bash
# Direct pytest
pytest

# With coverage report
pytest --cov= --cov-report=term-missing
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
**Documentation (if applicable):**
- [ ] README.md updated (if user-facing changes)
- [ ] AGENTS.md updated (if agent workflow changes)
- [ ] API reference docs updated (if new tools/capabilities)
- [ ] CHANGELOG.md entry added (for releases)

**Testing:**
- [ ] Manual testing completed

**Review:**
- [ ] Self-review completed
- [ ] Code follows project style guide
- [ ] No debug code or commented-out code
- [ ] Error messages are clear and actionable
- [ ] Logging statements use appropriate levels

### PR Review Process

- **Required approvals:** 1+ reviewer
- **Merge strategy:** Squash and merge (clean history)
- **Timeline:** Most PRs reviewed within 24-48 hours

---

## Architecture Overview

[Describe your project's architecture here. Include diagrams, key design patterns, and architectural decisions.]

### Key Design Patterns

- **[Pattern 1]:** [Description]
- **[Pattern 2]:** [Description]
- **[Pattern 3]:** [Description]

### Configuration Management

[Describe how configuration works in your project, including environment variables, config files, etc.]

---

## Key Constraints & Design Decisions

### Target Audience



**CRITICAL:** Example MCP Server with Vision is designed for **LLM-intelligent MCP clients** (Claude Desktop, Cursor, Roo Code).

- ✅ **FOR LLM agents** - Claude Desktop, Cursor, custom MCP clients
- ✅ **FOR programmatic use** - Python API, automation workflows
- ❌ **NOT for human CLI users** - No interactive wizards or watch modes

**Implication:** All features prioritize agent ergonomics over human UX.

### [Additional Constraints]

[Document your project-specific constraints and design decisions here.]

---

## Strategic Design

### Balancing Current Priorities with Future Vision

**The Balance:**
- ✅ **Deliver:** Ship current commitments on time
- ✅ **Design for evolution:** Keep future doors open (extension points)
- ✅ **Refactor strategically:** When it serves both present and future
- ❌ **NOT:** Premature optimization, gold plating, scope creep

**Key Insight:** Build for today, design for tomorrow. Don't implement Wave 2 features in Wave 1, but don't paint yourself into corners either.

### Vision-Aware Implementation Pattern

**When implementing features, ask:**

1. **Architecture Check:** "Does this design block future capabilities in [dev-docs/vision/](dev-docs/vision/)?"
   - ✅ YES → Refactor before implementing
   - ✅ NO → Proceed

2. **Refactoring Signal:** "Should I refactor this now?"
   ```
   ┌─────────────────────────────────────────────────────┐
   │ Does it help current work (Wave 1)?                 │
   │   NO → DEFER (focus on current deliverables)       │
   │   YES → Continue ↓                                  │
   ├─────────────────────────────────────────────────────┤
   │ Does it unblock future capabilities?                │
   │   YES → LIKELY REFACTOR (strategic investment)     │
   │   NO → Continue ↓                                   │
   ├─────────────────────────────────────────────────────┤
   │ Cost vs. benefit?                                    │
   │   HIGH COST → DEFER (wait for Wave 2 commitment)   │
   │   LOW COST → REFACTOR (small prep, big payoff)     │
   └─────────────────────────────────────────────────────┘
   ```

3. **Decision Documentation:** Where to record decisions
- **Knowledge notes:** `-memory knowledge create "Decision: [topic]"`
   - **Tags:** Use `architecture`, `vision`, `wave-N` tags for discoverability
### Practical Examples

**Example: Building Tool Interface**

**Scenario:** Wave 1 needs simple tool responses. Wave 2 vision includes tool chaining.

**❌ DON'T (Premature Optimization):**
```python
# DON'T build tool chaining now
async def get_data(query: str) -> str:
    # Implements full chaining system (Wave 2 feature)
    return chain_tools([tool_a, tool_b])(query)  # Not needed yet!
```

**✅ DO (Extension Point):**
```python
# DO return structured data (enables future chaining)
async def get_data(query: str) -> dict:
    """Returns structured response (extensible for Wave 2)."""
    return {
        "result": process_query(query),
        "metadata": {"timestamp": now(), "version": "1.0"}
    }
    # Wave 2 can add: "next_tool": "tool_b", "chain_id": "..."
```

### Refactoring Decision Framework

**Use this checklist before refactoring:**

- [ ] **Current Work:** Does this help Wave 1 deliverables?
- [ ] **Future Vision:** Check [dev-docs/vision/](dev-docs/vision/) - does this prepare for next wave?
- [ ] **Cost Assessment:** Low cost (<2 hours) or high cost (>1 day)?
- [ ] **Decision:** Apply framework above → Refactor now or defer?
- [ ] **Documentation:** Record decision (knowledge note)

### Capturing Knowledge for Future Agents

**Use A-MEM (Agentic Memory) patterns:**

1. **Emit Events:** Track architectural decisions
   ```python
   from .memory import emit_event

   emit_event(
       event_type="architecture.decision",
       data={
           "decision": "Use dict returns for tool extensibility",
           "rationale": "Enables Wave 2 tool chaining",
           "wave": "wave-2-preparation"
       },
       status="success"
   )
   ```

2. **Create Knowledge Notes:**
   ```bash
   echo "Decision: Tool Response Format

   Context: Wave 1 tools return simple data, Wave 2 vision includes tool chaining.

   Decision: Return dict (not str) from all tools.

   Rationale:
   - Low cost refactor (1 hour)
   - Unblocks Wave 2 tool chaining
   - Backward compatible (wrap str in dict)

   Tags: architecture, vision, wave-2, tools
   " | -memory knowledge create "Tool Response Format"
   ```

3. **Link to Vision:**
   - Reference vision waves in knowledge notes
   - Tag notes with `wave-N` for future discoverability
   - Query past decisions: `-memory knowledge search --tag wave-2`

### Quick Reference: Strategic Design Checklist

**Before implementing any feature:**

1. ✅ **Check ROADMAP.md:** Is this in current committed work?
2. ✅ **Check vision:** Does this align with evolutionary direction?
3. ✅ **Apply framework:** Refactor now or defer? (use flowchart above)
4. ✅ **Document:** Record decision for future agents
5. ✅ **Code:** Implement with extension points, not future features

**Remember:** Deliver today, design for tomorrow. No gold plating!

---

## Common Tasks for Agents

### Adding a New MCP Tool

1. Create tool function in `src//tools/your_tool.py`
2. Register tool with `@mcp.tool()` decorator
3. Add memory integration (emit events)
4. Add unit test in `tests/unit/test_your_tool.py`
5. Add integration test with memory validation
6. Update README.md tool list
7. Run tests: `pytest`

**Example:**
```python
from .memory import emit_event, TraceContext
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Example MCP Server with Vision")

@mcp.tool()
async def your_tool(param: str) -> dict:
    """Your tool description.

    Args:
        param: Parameter description

    Returns:
        Result dictionary
    """
# Emit start event
    emit_event("tool.your_tool.started", status="pending", metadata={"param": param})

try:
        # Your tool logic here
        result = process(param)
# Emit success event
        emit_event("tool.your_tool.completed", status="success", metadata={"result_count": len(result)})
return {"success": True, "data": result}
    except Exception as e:
# Emit failure event
        emit_event("tool.your_tool.failed", status="failure", metadata={"error": str(e)})
return {"success": False, "error": str(e)}
```

### Agent Self-Service: Learning from Past Errors

**When encountering a problem you've seen before:**

1. **Query past events** to find similar failures
2. **Search knowledge** for documented solutions
3. **Review related notes** via bidirectional links
4. **Apply the solution** from past learning
5. **Record outcome** to improve knowledge base

**Example workflow:**

```bash
# Problem: Tool failing with "rate limit exceeded"

# Step 1: Query past rate limit failures
example-mcp-vision-memory query --type "tool.failed" --since 30d | grep "rate limit"

# Step 2: Search knowledge base
example-mcp-vision-memory knowledge search --tag rate-limits --tag troubleshooting

# Step 3: Show specific solution note
example-mcp-vision-memory knowledge show rate-limit-handling

# Step 4: Apply exponential backoff solution (from knowledge note)
# ... implement fix ...

# Step 5: Record successful outcome
echo "Applied exponential backoff from rate-limit-handling note.
Rate limit errors reduced from 50/day to 2/day (96% improvement).
Solution: Added retry logic with delays [1s, 2s, 4s, 8s]." | \
  example-mcp-vision-memory knowledge create "Rate Limit Fix - Exponential Backoff Success" \
    --tag rate-limits --tag performance --tag solved --confidence high

# Step 6: Link to original problem note
example-mcp-vision-memory knowledge link rate-limit-handling rate-limit-fix-success
```

### Agent Self-Service: Creating Knowledge from Debugging

**When you solve a non-obvious problem:**

```bash
# After fixing a tricky bug, create knowledge note

# 1. Create note with problem context
echo "## Problem
Tool X was failing intermittently with 'connection timeout'.

## Investigation
- Analyzed events: example-mcp-vision-memory query --type tool.x.failed --since 7d
- Found pattern: Failures only during peak hours (9am-5pm)
- Root cause: Connection pool exhaustion (max 10 connections)

## Solution
Increased connection pool size to 50 in config.
Added connection pool monitoring.

## Validation
- Ran load test: 100 concurrent requests
- Zero timeouts after fix
- Connection pool usage: avg 15/50 (healthy headroom)

## Related
- Connection pool settings: [link to config docs]
- Load testing guide: [link to testing docs]" | \
  example-mcp-vision-memory knowledge create "Tool X Connection Timeout Fix" \
    --tag connection-pool --tag timeout --tag performance --confidence high

# 2. Tag for future retrieval
example-mcp-vision-memory knowledge tag connection-timeout-fix production-issues

# 3. Link to related notes
example-mcp-vision-memory knowledge link connection-timeout-fix connection-pool-config
```

**Benefits of creating knowledge:**
- Future sessions can query this solution
- Avoid repeating the same debugging work
- Build cumulative expertise over time
- Share learnings across agent instances

### Debugging Common Issues

```bash
# Check logs
tail -f logs/.log

# Test single component
python -m .module_name

# Check environment
env | grep 

# Validate configuration
python -c "from  import config; print(config)"
```



### Design Decision: Check Against Vision

**When:** Before making architectural decisions or significant refactors

**Steps:**

1. **Check current priority:**
   ```bash
   cat ROADMAP.md | head -50
   # Current: [Your current sprint/milestone]
   ```

2. **Check long-term vision:**
   ```bash
   cat dev-docs/vision/CAPABILITY_EVOLUTION.md | head -100
   # Future waves: [Your capability themes]
   ```

3. **Apply decision framework:**
   - **Does this help current work?** (YES → continue)
   - **Does this align with vision?** (YES → good sign)
   - **Cost vs. benefit?** (LOW COST → likely proceed)

4. **Document decision:**
```bash
   # Create knowledge note
   echo "Decision: [Your decision]

   Context: [Current situation]

   Decision: [What you decided]

   Rationale:
   - Helps Wave 1 deliverables: [How]
   - Aligns with Wave 2 vision: [Which capability]
   - Low cost: [Effort estimate]

   Outcome: [Expected result]

   Tags: architecture, vision, wave-N, decision
   " | -memory knowledge create "Decision: [Topic]"
   ```
5. **Link to vision:**
   - If prepares for future waves, note it in documentation
- Add tags to knowledge notes for discoverability: `wave-2`, `architecture`, `vision`
- Update vision document if decision affects feasibility

**Example Decision:**

**Scenario:** Should we refactor tool responses from `str` to `dict`?

1. **Current work:** Wave 1 needs simple responses → `str` works
2. **Vision:** Wave 2 includes tool chaining → needs structured data (`dict`)
3. **Cost:** Low (1-2 hours to refactor)
4. **Decision:** ✅ REFACTOR NOW (serves both present and future)

---

## Project Structure

```
example-mcp-vision/
├── src//       # Main source code
│   ├── __init__.py
│   ├── server.py               # MCP server entry point
│   ├── memory/                 # Agent memory system
│   │   ├── event_log.py
│   │   ├── knowledge_graph.py
│   │   └── trace.py
│   └── [your modules]
├── scripts/                    # Automation scripts
│   ├── setup.sh                # One-command setup
│   ├── venv-create.sh          # Create virtual environment
│   └── [other scripts]
├── .chora/memory/              # Agent memory (gitignored)
│   ├── README.md               # Memory architecture docs
│   ├── events/                 # Event log (JSONL format)
│   ├── knowledge/              # Knowledge notes (YAML frontmatter)
│   │   ├── notes/*.md          # Individual notes
│   │   ├── links.json          # Bidirectional links
│   │   └── tags.json           # Tag index
│   └── profiles/               # Agent-specific profiles
├── pyproject.toml              # Python packaging & tool config
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore patterns
├── README.md                   # Human-readable project overview
├── AGENTS.md                   # This file (machine-readable instructions)
└── LICENSE                     #  license
```

### Knowledge Note Metadata Standards

Knowledge notes (`.chora/memory/knowledge/notes/*.md`) use **YAML frontmatter** following Zettelkasten best practices for machine-readable metadata.

**Required Frontmatter Fields:**
- `id`: Unique note identifier (kebab-case)
- `created`: ISO 8601 timestamp
- `updated`: ISO 8601 timestamp
- `tags`: Array of topic tags for search/organization

**Optional Frontmatter Fields:**
- `confidence`: `low` | `medium` | `high` - Solution reliability
- `source`: `agent-learning` | `human-curated` | `external` | `research`
- `linked_to`: Array of related note IDs (bidirectional linking)
- `status`: `draft` | `validated` | `deprecated`
- `author`: Agent or human creator
- `related_traces`: Array of trace IDs that led to this knowledge

**Example Knowledge Note:**

```markdown
---
id: api-timeout-solution
created: 2025-01-17T10:00:00Z
updated: 2025-01-17T12:30:00Z
tags: [troubleshooting, api, performance]
confidence: high
source: agent-learning
linked_to: [connection-pool-tuning, retry-patterns]
status: validated
author: claude-code
related_traces: [abc123, def456]
---

# API Timeout Solution

## Problem
API calls timing out after 30s during high load...

## Solution
Increase timeout to 60s and implement retry with exponential backoff...

## Evidence
- Trace abc123: Successful completion at 45s
- Trace def456: Successful completion at 52s
- Load test: 98% success rate with new settings
```

**Why YAML Frontmatter?**
- ✅ **Semantic Search**: Query by confidence, tags, or date (`grep "confidence: high"`)
- ✅ **Tool Compatibility**: Works with Obsidian, Zettlr, LogSeq, Foam
- ✅ **Knowledge Graph**: Enables bidirectional linking and visualization
- ✅ **Agent Decision-Making**: Filter by confidence level for solution reliability

**Reference:** See [.chora/memory/README.md](.chora/memory/README.md) for complete schema documentation.

---

## Documentation Philosophy

### Diátaxis Framework

Example MCP Server with Vision documentation follows the [Diátaxis framework](https://diataxis.fr/), serving **two first-class audiences**:

1. **Human Developers** - Learning, understanding, decision-making
2. **AI Agents** - Task execution, reference lookup, machine-readable instructions

**Four Quadrants:**

| Type | Purpose | Primary Audience | When to Use |
|------|---------|------------------|-------------|
| **Tutorials** | Learning-oriented | Humans (new users) | "I want to learn how Example MCP Server with Vision works" |
| **How-To Guides** | Task-oriented | Humans + Agents | "I want to accomplish a specific task" |
| **Reference** | Information-oriented | Humans + Agents | "I need to look up a fact/command/API" |
| **Explanation** | Understanding-oriented | Humans | "I want to understand why/how this works" |

### For AI Agents (Recommended Reading Order)

**When starting work on Example MCP Server with Vision:**

1. **Start here:** AGENTS.md (this file) - Machine-readable project instructions
2. **Quick reference:** How-To Guides - Executable task recipes
   - How to add new features
   - How to run tests
   - How to deploy
3. **Lookup facts:** Reference Docs - API specs, configuration options, commands
4. **Skip:** Tutorials (for human learning) and Explanations (conceptual background)

**Example: Agent workflow for "Add new feature X"**

```bash
# 1. Read AGENTS.md section: "Common Tasks for Agents" → "Adding a New MCP Tool"
# 2. Follow steps 1-7 (create file, register tool, add tests, etc.)
# 3. If unclear on testing: Consult "Testing Instructions" section in AGENTS.md
# 4. If need API reference: Read relevant module docstrings or Reference docs
# 5. Run pre-merge: `just pre-merge` (from AGENTS.md "Pre-Merge Verification")
```

### For Human Developers (Recommended Learning Path)

**New to Example MCP Server with Vision:**

1. **README.md** - Project overview, quick start (5 minutes)
2. **Tutorial** - Guided learning experience (30-60 minutes)
4. **How-To Guides** - Task-specific recipes (as needed)
5. **Reference Docs** - Lookup API details (as needed)
6. **Explanation Docs** - Understand design decisions (optional)

### Documentation Hierarchy

```
docs/
├── README.md                   # Human entry point (project overview)
├── AGENTS.md                   # Agent entry point (this file)
└── [additional docs]/
```

**Quick Reference:**

- **For agents:** AGENTS.md → How-To Guides → Reference Docs
- **For humans:** README → Tutorials → How-To Guides → Explanations

### DDD/BDD/TDD Workflow

This project follows the Chora ecosystem's integrated DDD/BDD/TDD workflow:

1. **DDD Phase** - Write API reference docs FIRST (documentation-driven design)
2. **BDD Phase** - Write scenarios SECOND (behavior-driven development)
3. **TDD Phase** - Red-Green-Refactor THIRD (test-driven development)
4. **CI Phase** - Automated quality gates
5. **Merge & Release** - Semantic versioning

**Why this order matters:**

- **Docs first** ensures clear API design before implementation
- **Scenarios second** captures expected behavior as executable specs
- **Tests third** drives implementation with fast feedback loop
- **CI validates** all quality gates pass before merge
- **Semantic versioning** communicates changes to users

**For agents:** Follow this workflow when adding new features. Write docs → scenarios → tests → implementation.

---

## Troubleshooting

### Application Won't Start

```bash
# Check Python version
python --version  # Must be +

# Check virtual environment
which python  # Should be .venv/bin/python

# Reinstall dependencies
./scripts/venv-create.sh

# Check environment variables
cat .env

# Test application directly
python -m .server
```

### Memory CLI Errors

**Problem: Memory commands not found**

```bash
# Verify CLI installation
which example-mcp-vision-memory
# Expected: .venv/bin/example-mcp-vision-memory

# If missing, reinstall package with CLI
pip install -e .

# Verify entry point in pyproject.toml
grep -A 5 "\[project.scripts\]" pyproject.toml
# Should contain: example-mcp-vision-memory = ".cli.memory:main"
```

**Problem: Query returns empty results**

```bash
# Check event log directory
ls -la .chora/memory/events/
# Expected: Monthly directories (e.g., 2025-01/)

# Check events file exists and has content
cat .chora/memory/events/$(date +%Y-%m)/events.jsonl | wc -l
# If 0, no events emitted yet

# Emit test event to verify system
python -c "from .memory import emit_event; emit_event('test.verify', status='success')"

# Query again
example-mcp-vision-memory query --type test.verify
# Should show test event
```

**Problem: JSON parsing errors from CLI**

```bash
# Validate JSONL format in event log
python -c "
import json
with open('.chora/memory/events/2025-01/events.jsonl') as f:
    for i, line in enumerate(f, 1):
        try:
            json.loads(line)
        except json.JSONDecodeError as e:
            print(f'Line {i} invalid: {e}')
"

# If corrupted, backup and recreate
mv .chora/memory/events/2025-01/events.jsonl .chora/memory/events/2025-01/events.jsonl.backup
touch .chora/memory/events/2025-01/events.jsonl
```

### Event Log Troubleshooting

**Problem: Events not appearing in queries**

```bash
# 1. Verify event emission
python -c "
from .memory import emit_event
print('Emitting test event...')
emit_event('debug.test', status='success', metadata={'test': 'value'})
print('Event emitted successfully')
"

# 2. Check event log file was written
ls -lh .chora/memory/events/$(date +%Y-%m)/events.jsonl
# Size should increase after emission

# 3. View raw event log
tail -5 .chora/memory/events/$(date +%Y-%m)/events.jsonl

# 4. Query with verbose output
example-mcp-vision-memory query --type debug.test --json | python -m json.tool
```

**Problem: Trace correlation not working**

```bash
# Verify CHORA_TRACE_ID environment variable
echo $CHORA_TRACE_ID
# Should be UUID format if set by TraceContext

# Emit event with explicit trace_id
python -c "
from .memory import emit_event, TraceContext
with TraceContext() as trace_id:
    print(f'Trace ID: {trace_id}')
    emit_event('test.trace', trace_id=trace_id, status='success')
"

# Query by trace_id
example-mcp-vision-memory trace <TRACE_ID>
# Should show all events with that trace_id
```

**Problem: Event log too large / performance issues**

```bash
# Check total event count
cat .chora/memory/events/*/events.jsonl | wc -l

# Archive old events (older than 90 days)
mkdir -p .chora/memory/archive
find .chora/memory/events -type d -name "2024-*" -exec mv {} .chora/memory/archive/ \;

# Query stats for retention analysis
example-mcp-vision-memory stats --since 90d
# Review event types, identify noise (e.g., excessive debug events)
```

### Knowledge Graph Troubleshooting

**Problem: Knowledge notes not found in search**

```bash
# 1. List all knowledge notes
ls -la .chora/memory/knowledge/notes/
# Check if note file exists

# 2. Verify note format (YAML frontmatter + markdown)
cat .chora/memory/knowledge/notes/my-note.md
# Expected format:
# ---
# id: my-note
# title: My Note
# tags: [tag1, tag2]
# confidence: medium
# created: 2025-01-17T10:00:00Z
# updated: 2025-01-17T10:00:00Z
# ---
# Content here

# 3. Rebuild tag index if corrupted
python -c "
from .memory.knowledge_graph import KnowledgeGraph
kg = KnowledgeGraph()
kg._rebuild_tag_index()  # Internal method - use with caution
print('Tag index rebuilt')
"

# 4. Search again
example-mcp-vision-memory knowledge search --tag my-tag
```

**Problem: Broken bidirectional links**

```bash
# Check links.json structure
cat .chora/memory/knowledge/links.json | python -m json.tool

# Expected format:
# {
#   "note-a": ["note-b", "note-c"],
#   "note-b": ["note-a"],
#   "note-c": ["note-a"]
# }

# Verify linked notes exist
python -c "
import json
with open('.chora/memory/knowledge/links.json') as f:
    links = json.load(f)
    for note, targets in links.items():
        print(f'{note} → {targets}')
        for target in targets:
            path = f'.chora/memory/knowledge/notes/{target}.md'
            if not __import__('os').path.exists(path):
                print(f'  WARNING: {target} does not exist')
"

# Fix broken links
example-mcp-vision-memory knowledge link note-a note-b  # Recreate link
```

**Problem: Tag corruption or duplicates**

```bash
# View tag index
cat .chora/memory/knowledge/tags.json | python -m json.tool

# Find duplicate tags (case-sensitive)
cat .chora/memory/knowledge/tags.json | python -c "
import json, sys
tags = json.load(sys.stdin)
seen = {}
for tag in tags.keys():
    lower = tag.lower()
    if lower in seen:
        print(f'Duplicate: {tag} vs {seen[lower]}')
    seen[lower] = tag
"

# Merge tags if needed
example-mcp-vision-memory knowledge search --tag old-tag
# Create notes with new standardized tag
# Manually remove old tag from tag index
```

### Trace Context Troubleshooting

**Problem: CHORA_TRACE_ID not propagating to subprocesses**

```bash
# Verify TraceContext sets environment variable
python -c "
from .memory import TraceContext
import os
with TraceContext() as trace_id:
    print(f'Inside context: {os.environ.get(\"CHORA_TRACE_ID\")}')
    # Should match trace_id
print(f'Outside context: {os.environ.get(\"CHORA_TRACE_ID\")}')
# Should be None or previous value
"

# Test subprocess propagation
python -c "
from .memory import TraceContext
import subprocess, os
with TraceContext() as trace_id:
    result = subprocess.run(
        ['python', '-c', 'import os; print(os.environ.get(\"CHORA_TRACE_ID\"))'],
        capture_output=True,
        text=True
    )
    print(f'Trace ID: {trace_id}')
    print(f'Subprocess saw: {result.stdout.strip()}')
    # Should match
"
```

**Problem: Multiple overlapping trace contexts**

```bash
# Anti-pattern: Nested TraceContext (avoid this)
# python -c "
# from .memory import TraceContext
# with TraceContext() as trace_1:  # Outer context
#     with TraceContext() as trace_2:  # Inner context overrides
#         emit_event('test')  # Uses trace_2, loses trace_1
# "

# Correct pattern: Single TraceContext per workflow
python -c "
from .memory import TraceContext, emit_event
with TraceContext() as trace_id:
    emit_event('workflow.started', trace_id=trace_id)
    # ... all workflow steps ...
    emit_event('workflow.completed', trace_id=trace_id)
# Query workflow by trace_id
"
```

---

## Agent Memory System

### Overview

Example MCP Server with Vision includes a stateful memory infrastructure for cross-session learning and knowledge persistence, implementing A-MEM (Agentic Memory) principles.

**Memory capabilities:**
- **Event Log** - Append-only operation history with trace correlation
- **Knowledge Graph** - Structured learnings with Zettelkasten-style linking
- **Trace Context** - Multi-step workflow tracking via `CHORA_TRACE_ID`
- **Cross-Session Learning** - Avoid repeating mistakes across sessions

### Memory Location

All memory data stored in `.chora/memory/`:

```
.chora/memory/
├── README.md                    # Memory architecture documentation
├── events/                      # Event log storage (monthly partitions)
│   ├── 2025-01/
│   │   ├── events.jsonl         # Daily aggregated events
│   │   └── traces/              # Per-trace details
│   └── index.json               # Event index (searchable)
├── knowledge/                   # Knowledge graph
│   ├── notes/                   # Individual knowledge notes
│   ├── links.json               # Note connections
│   └── tags.json                # Tag index
├── profiles/                    # Agent-specific profiles
└── queries/                     # Saved queries
```

**Privacy:** Memory directory is in `.gitignore` by default (contains ephemeral learning data, not source code).

### Event Log Usage

**Emit events during operations:**

```python
from .memory import emit_event, TraceContext

# Start workflow with trace context
with TraceContext() as trace_id:
    # Emit operation events
    emit_event(
        "app.operation_completed",
        trace_id=trace_id,
        status="success",
        operation_name="example",
        duration_ms=1234
    )
```

**Query recent events:**

```python
from .memory import query_events

# Find failures in last 24 hours
failures = query_events(
    event_type="app.operation_failed",
    status="failure",
    since_hours=24
)

# Analyze patterns
for failure in failures:
    error = failure["metadata"]["error"]
    print(f"Operation failed: {error}")
```

### Knowledge Graph Usage

**Create learning notes:**

```python
from .memory import KnowledgeGraph

kg = KnowledgeGraph()

# Create note from learned pattern
note_id = kg.create_note(
    title="[Learning Title]",
    content="[Detailed learning content]",
    tags=["tag1", "tag2"],
    confidence="high"
)
```

**Search knowledge:**

```python
# Find notes by tag
notes = kg.search(tags=["error", "fix"])

# Find notes by content
notes = kg.search(text="timeout")

# Get related notes
related = kg.get_related("note-id", max_distance=2)
```

### A-MEM Self-Service Workflow (Agent Learning Loop)

**The agent learning loop implements A-MEM (Agentic Memory) principles:**

```
┌─────────────────────────────────────────────────────────┐
│  1. ENCOUNTER PROBLEM                                   │
│  Agent encounters error, unexpected behavior, or        │
│  performance issue during task execution                │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  2. QUERY PAST EVENTS (Event Log)                       │
│  Search for similar failures in event history           │
│  example-mcp-vision-memory query --type problem.type --since 30d  │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  3. SEARCH KNOWLEDGE (Knowledge Graph)                  │
│  Find documented solutions in knowledge base            │
│  example-mcp-vision-memory knowledge search --tag problem_domain  │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  4. TRAVERSE LINKS (Bidirectional Navigation)           │
│  Follow related notes for deeper context                │
│  example-mcp-vision-memory knowledge show note-id        │
│  (Shows linked notes in "Related" section)              │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  5. APPLY SOLUTION                                       │
│  Implement the learned fix from knowledge base          │
│  (Code changes, config updates, etc.)                   │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  6. VALIDATE OUTCOME                                     │
│  Test that solution resolves the problem                │
│  Run tests, check metrics, verify behavior              │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  7. RECORD LEARNING (Memory Evolution)                   │
│  Create/update knowledge note with outcome              │
│  example-mcp-vision-memory knowledge create "Solution Title"     │
│  Link to original problem note                          │
│  Tag for future retrieval                               │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  8. CUMULATIVE IMPROVEMENT                               │
│  Future encounters of same problem → query knowledge    │
│  Faster resolution time (no re-debugging)               │
│  Build expertise over multiple sessions                 │
└─────────────────────────────────────────────────────────┘
```

**Example: Applying A-MEM Loop to Performance Issue**

```bash
# 1. ENCOUNTER PROBLEM
# Agent notices: API responses taking >5 seconds (slow)

# 2. QUERY PAST EVENTS
example-mcp-vision-memory query --type "api.slow_response" --since 30d
# Output: Found 15 events of slow responses in past month

# 3. SEARCH KNOWLEDGE
example-mcp-vision-memory knowledge search --tag performance --tag api
# Output: Found 3 notes: "API Caching Strategy", "Connection Pool Tuning", "Query Optimization"

# 4. TRAVERSE LINKS
example-mcp-vision-memory knowledge show api-caching-strategy
# Output shows:
# ## API Caching Strategy
# Problem: API responses slow due to repeated database queries
# Solution: Implemented Redis caching with 5-minute TTL
# Validation: Response time reduced from 5s to 200ms (96% improvement)
# Related: connection-pool-tuning, query-optimization

# 5. APPLY SOLUTION
# Implement Redis caching based on knowledge note guidance
# ... code changes ...

# 6. VALIDATE OUTCOME
# Run load test, measure response times
# Result: Response time now 180ms (97% improvement vs original 5s)

# 7. RECORD LEARNING
echo "## Context
Applied Redis caching to API endpoints based on 'API Caching Strategy' note.

## Implementation
- Added Redis client with 5-minute TTL
- Cached GET endpoints for /users, /products, /orders
- Cache invalidation on POST/PUT/DELETE

## Outcome
- Response time: 5s → 180ms (97% faster)
- Database load: -80% (queries cached)
- Redis memory usage: ~50MB (within budget)

## Refinement from Original
Original note used 5-minute TTL. Found 10-minute TTL works better for this use case.
Updated cache invalidation logic to be more granular.

## Related
- api-caching-strategy (original guide)
- connection-pool-tuning (complementary optimization)
- redis-configuration (cache config details)" | \
  example-mcp-vision-memory knowledge create "API Caching - Production Implementation" \
    --tag performance --tag api --tag caching --tag production --confidence high

# 8. CUMULATIVE IMPROVEMENT
# Link back to original note
example-mcp-vision-memory knowledge link api-caching-strategy api-caching-production

# Tag for production issues
example-mcp-vision-memory knowledge tag api-caching-production solved production-win

# Future sessions encountering slow API will:
# 1. Query events → find "api.slow_response"
# 2. Search knowledge → find "API Caching - Production Implementation"
# 3. See 97% improvement outcome → high confidence solution
# 4. Apply immediately without re-debugging
```

**A-MEM Principles in Action:**

1. **Dynamic Organization** - Agent creates notes, tags, links (not pre-defined schema)
2. **Note Construction** - Structured format with Problem/Solution/Validation
3. **Bidirectional Linking** - Notes reference each other (knowledge graph)
4. **Memory Evolution** - New notes update/refine existing knowledge
5. **Cross-Session Learning** - Future sessions benefit from past learning
6. **Confidence Tracking** - High confidence solutions applied first

See [.chora/memory/README.md](.chora/memory/README.md) for complete memory architecture documentation.

---

## Related Resources

- **Repository:** https://github.com//example-mcp-vision
- **Chora Base Template:** https://github.com/liminalcommons/chora-base
- **Chora Composer:** https://github.com/liminalcommons/chora-composer
- **Chora Platform:** https://github.com/liminalcommons/chora-platform
- **MCP Specification:** https://modelcontextprotocol.io/
---

**Version:** 
**Last Updated:** [Update date]
**Format:** AGENTS.md standard (OpenAI/Google/Sourcegraph)
🤖 Generated with [chora-base](https://github.com/liminalcommons/chora-base) template
