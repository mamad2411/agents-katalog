---
name: openclawn-agent-framework
description: Use OpenCLAWN, a self-improving multi-agent framework with routing audit, skill decay, confidence-gated learning, and 26 sandboxed tools for code, data, docs, git, and web.
triggers:
  - set up openclawn agent framework
  - create self-improving ai agent with openclawn
  - configure openclawn multi-agent conversation
  - use openclawn skill crystallization
  - implement openclawn autopilot with approval gate
  - debug openclawn routing decisions
  - export import openclawn skill packs
  - add custom tool to openclawn agent
---

# OpenCLAWN Agent Framework

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

OpenCLAWN is a lightweight, self-improving multi-agent framework built around **4 core innovations**: routing audit + self-calibration, skill decay, confidence-gated crystallization, and role output contracts. It features hybrid local (Ollama) + cloud (Gemini/Claude) LLM routing, 26 sandboxed tools, and a compounding skill library that tidies and improves itself as it's used.

**Key capabilities:**
- Multi-agent conversations (pipeline, debate, orchestrator strategies)
- Self-calibrating smart router with multilingual complexity detection
- Skill compounding: promote, refine, merge, decay — all versioned & revertible
- Autopilots with approval-gated proposals (no silent execution)
- Activity timeline tracking every agent action
- Skill pack export/import with SSRF + injection guards

---

## Installation

### Prerequisites

- Python 3.12+
- Docker (for sandboxed tool execution)
- Ollama installed and running (for local models)
- API keys for Gemini and/or Claude (optional, for heavy tiers)

### Quick Setup

```bash
# Clone repository
git clone https://github.com/MuhammadHasbiAshshiddieqy/OpenClawn.git
cd OpenClawn

# Install with uv (recommended for reproducibility)
uv sync --frozen --extra dev

# Or with pip
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# Configure environment
cp .env.example .env
# Edit .env and add:
# GEMINI_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here
# OPENCLAWN_PREFER_LOCAL=true  # Optional: stay local longer
# OPENCLAWN_WORKSPACE_PATH=./workspace  # Agent workspace root

# Initialize database
mkdir -p data
sqlite3 data/openclawn.db < migrations/001_initial.sql

# Pull Ollama models (one per local tier)
ollama pull gemma4:e2b    # Light tier
ollama pull gemma4:e4b    # Moderate tier
ollama pull gemma4:12b    # Complex tier

# Build sandbox Docker image
docker build -t openclawn-sandbox:latest -f Dockerfile.sandbox .

# Start the web interface
uvicorn web.main:app --reload --port 8000
```

Access the UI at `http://localhost:8000`.

---

## Architecture Overview

### Core Components

1. **SmartRouter** — Innovation #1: Routing audit + self-calibration
   - Scores queries on 10 dimensions (code, math, reasoning, etc.)
   - Labels complexity: TRIVIAL → SIMPLE → MODERATE → COMPLEX → CRITICAL
   - Logs every decision for later calibration
   - Multilingual support with optional script-aware tier bumps

2. **SkillDecay** — Innovation #2: Skill lifecycle management
   - Skills scored 0–1 based on age, usage, success rate
   - Decay passes run hourly (throttled)
   - Skills below 0.3 score excluded from context

3. **Crystallizer** — Innovation #3: Confidence-gated skill storage
   - Captures multi-tool solutions as reusable skills
   - Self-evaluates with confidence score (1–5)
   - Only stores skills with confidence ≥4
   - Uses evaluator tier ≥ generator tier

4. **RoleNegotiator** — Innovation #4: Typed multi-agent contracts
   - Validates handoffs between roles (PM → Dev → QA)
   - Ensures output contracts are met before handoff
   - Prevents fragile multi-agent communication

5. **SkillCurator** — Compounding layer (I1)
   - Merges duplicate skills
   - Deduplicates based on semantic similarity
   - Requires judge tier ≥4, revertible

6. **SkillFeedback** — Compounding layer (I2/I3)
   - Promotes draft skills on success
   - Refines skills on correction
   - Revives decayed skills on proven re-use

---

## Basic Usage

### Single Agent Chat

```python
from agent.agent import Agent
from core.llm_client import LLMClient
from core.memory_manager import MemoryManager
from core.smart_router import SmartRouter
from core.routing_auditor import RoutingAuditor

# Initialize components
llm_client = LLMClient()
memory_manager = MemoryManager(agent_id="agent_1")
router = SmartRouter()
auditor = RoutingAuditor()

# Create agent
agent = Agent(
    llm_client=llm_client,
    memory_manager=memory_manager,
    router=router,
    auditor=auditor,
    agent_id="agent_1"
)

# Stream response
async for chunk in agent.process_query(
    query="Write a Python script to parse CSV and export to JSON",
    stream=True
):
    print(chunk, end="", flush=True)
```

### Multi-Agent Conversation (Pipeline)

```python
from conversation.orchestrator import ConversationOrchestrator
from conversation.strategies import PipelineStrategy

# Define roles with output contracts
roles = [
    {
        "name": "product_manager",
        "system_prompt": "You are a product manager. Define requirements.",
        "output_contract": {
            "required_fields": ["requirements", "acceptance_criteria"],
            "format": "markdown"
        }
    },
    {
        "name": "developer",
        "system_prompt": "You are a developer. Implement the solution.",
        "output_contract": {
            "required_fields": ["implementation", "tests"],
            "format": "code"
        }
    },
    {
        "name": "qa_engineer",
        "system_prompt": "You are a QA engineer. Test the solution.",
        "output_contract": {
            "required_fields": ["test_results", "bugs_found"],
            "format": "markdown"
        }
    }
]

# Create pipeline orchestrator
orchestrator = ConversationOrchestrator(
    strategy=PipelineStrategy(),
    roles=roles
)

# Run conversation
result = await orchestrator.run_conversation(
    initial_prompt="Build a user authentication system"
)
```

### Autopilot with Approval Gates

```python
from autopilots.scheduler import AutopilotScheduler
from autopilots.autopilot import Autopilot

# Create autopilot
autopilot = Autopilot(
    name="daily_security_scan",
    schedule="0 9 * * *",  # Daily at 9 AM
    prompt="Scan the codebase for security vulnerabilities and report findings",
    agent_id="security_agent",
    require_approval=True  # Actions become proposals
)

# Start scheduler
scheduler = AutopilotScheduler()
await scheduler.add_autopilot(autopilot)
await scheduler.start()

# Check proposals (via web UI or API)
# GET /autopilots/{autopilot_id}/proposals
# POST /autopilots/proposals/{proposal_id}/approve
```

---

## Configuration

### Router Tier Mapping (`/router` endpoint or config file)

```yaml
# config/router_tiers.yaml
tiers:
  trivial:
    local: "gemma4:e2b"
    fallback: ["gemini-2.5-flash"]
  
  simple:
    local: "gemma4:e4b"
    fallback: ["gemini-2.5-flash"]
  
  moderate:
    local: "gemma4:12b"
    fallback: ["gemini-2.5-pro"]
  
  complex:
    cloud: "gemini-2.5-pro"
    fallback: ["claude-3-7-sonnet"]
  
  critical:
    cloud: "claude-3-7-sonnet"
    fallback: ["gemini-2.5-pro-exp-03"]
```

### Soul Configuration (`soul.toml`)

```toml
# soul.toml — agent personality and routing hints
[identity]
name = "DevBot"
role = "Senior Full-Stack Developer"
tone = "professional, helpful"

[routing_hints]
# Keywords that upgrade complexity tier (+3 to score)
upgrade_keywords = [
    "production",
    "critical bug",
    "security",
    "performance optimization",
    "database migration"
]

# Prefer local models (adds +1 to threshold, stays local longer)
prefer_local = true

[memory]
# L4 archival threshold (messages before archiving to FTS5)
archive_threshold = 50
```

### Environment Variables

```bash
# .env
GEMINI_API_KEY=your_gemini_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Workspace root (all file operations bounded to this)
OPENCLAWN_WORKSPACE_PATH=./workspace

# Database path
OPENCLAWN_DB_PATH=./data/openclawn.db

# Ollama endpoint
OLLAMA_BASE_URL=http://localhost:11434

# Routing preferences
OPENCLAWN_PREFER_LOCAL=true
OPENCLAWN_LANGUAGE_AWARE_ROUTING=true  # Bump tier for non-local scripts

# Skill system
OPENCLAWN_SKILL_DECAY_ENABLED=true
OPENCLAWN_CRYSTALLIZATION_MIN_CONFIDENCE=4

# Autopilot behavior
OPENCLAWN_AUTOPILOT_APPROVAL_TIMEOUT=3600  # 1 hour

# Calibration (opt-in auto-apply)
OPENCLAWN_AUTO_CALIBRATION=false
```

---

## Tools

OpenCLAWN includes 26 sandboxed tools, all workspace-bounded:

### Filesystem Tools

```python
# Read file
await agent.process_query("Read the contents of src/main.py")

# Write file
await agent.process_query("Write 'Hello, World!' to output.txt")

# Edit file (line-based replacement)
await agent.process_query(
    "In config.yaml, replace line 5 with 'debug: true'"
)

# Patch file (unified diff)
await agent.process_query("""
Apply this patch to api.py:
--- a/api.py
+++ b/api.py
@@ -10,7 +10,7 @@
-DEBUG = False
+DEBUG = True
""")

# Glob search
await agent.process_query("Find all Python files in the tests directory")

# Grep search
await agent.process_query("Search for 'TODO' in all JavaScript files")

# Read many files (batch read, single tool call)
await agent.process_query("Read all config files: .env, config.yaml, settings.json")
```

### Execution Tools (Sandboxed)

```python
# Run Python code in sandbox
await agent.process_query("""
Run this Python code:
import json
data = {"name": "test", "value": 42}
print(json.dumps(data, indent=2))
""")

# Run shell command in sandbox
await agent.process_query("Run: ls -lah /workspace")
```

**Sandbox specs:**
- Docker container with `network=none`
- Read-only workspace mount
- Non-root user
- 30-second timeout
- Stdout/stderr captured

### Network Tools (SSRF-guarded)

```python
# Fetch web page
await agent.process_query("Fetch the content of https://example.com")

# Web search (requires API key)
await agent.process_query("Search the web for 'Python async best practices'")

# HTTP request (arbitrary method/headers)
await agent.process_query("""
Make a POST request to https://api.example.com/data
Headers: {"Authorization": "Bearer ${API_TOKEN}"}
Body: {"query": "test"}
""")
```

SSRF protections:
- Blocks private IPs (127.0.0.0/8, 192.168.0.0/16, etc.)
- Blocks cloud metadata endpoints
- DNS rebinding protection

### Data & Document Tools

```python
# Query SQLite database
await agent.process_query("Query the users table: SELECT * FROM users LIMIT 10")

# JSON query (JMESPath)
await agent.process_query("""
Query data.json with: users[?age > `25`].{name: name, email: email}
""")

# PDF read
await agent.process_query("Extract text from report.pdf")

# Document write (Markdown/HTML/plain text)
await agent.process_query("Write a report to docs/summary.md with this content: ...")

# PDF write (from Markdown)
await agent.process_query("Convert docs/summary.md to PDF at reports/summary.pdf")
```

### Development Tools

```python
# Git status
await agent.process_query("Show git status")

# Git diff
await agent.process_query("Show diff for src/main.py")

# Git log
await agent.process_query("Show last 5 commits")

# Write TODO
await agent.process_query("Add TODO: Refactor auth module")

# Report blocker
await agent.process_query("""
Report blocker: Database migration failed
Context: PostgreSQL version mismatch
Needs: Manual intervention
""")
```

---

## Skill Management

### Viewing Skills

```python
# Via web UI: http://localhost:8000/skills

# Via API
import httpx

async with httpx.AsyncClient() as client:
    resp = await client.get("http://localhost:8000/api/skills")
    skills = resp.json()
    
    for skill in skills:
        print(f"{skill['name']} (score: {skill['decay_score']:.2f})")
```

### Exporting Skill Pack

```python
# Export all active skills (score > 0.5)
# POST /api/skills/export
{
    "min_score": 0.5,
    "include_drafts": false
}

# Returns Markdown file with YAML frontmatter:
# ---
# pack_name: my-skills
# exported_at: 2026-06-20T10:00:00Z
# skill_count: 12
# checksum: sha256:abc123...
# ---
# ## Skill: error-handling-pattern
# ...
```

### Importing Skill Pack

```python
# Import skill pack from Markdown
# POST /api/skills/import
# Content-Type: multipart/form-data
# File: skills.md

# All imported skills start as "draft" status
# They won't be auto-injected into context
# Manually promote after review:
# POST /api/skills/{skill_id}/promote
```

**Security checks on import:**
- NFKD normalization scan for homograph attacks
- Injection pattern detection
- SSRF guard for any embedded URLs
- Checksum verification

---

## Routing Calibration

### View Calibration Dashboard

Navigate to `http://localhost:8000/metrics` to see:
- Decision distribution (pie chart)
- Accuracy trends (over time)
- Per-tier precision/recall
- Suggested offsets for each complexity label

### Manual Calibration

```python
# After reviewing routing decisions, apply offset
# POST /api/router/calibrate
{
    "label": "moderate",
    "offset": -0.5  # Make "moderate" less likely (higher threshold)
}

# Revert calibration
# POST /api/router/calibration/revert
{
    "label": "moderate"
}
```

### Auto-Calibration (Opt-In)

```bash
# Enable in .env
OPENCLAWN_AUTO_CALIBRATION=true

# Runs weekly, clamps offsets to ±1.0, always revertible
```

**How it works:**
1. Auditor logs every routing decision with 10 dimension scores
2. User feedback (implicit: correction, explicit: rating) marks decisions
3. Calibration service analyzes misrouted queries
4. Suggests offset adjustments to improve accuracy
5. Auto-apply (if enabled) or manual review

---

## User Modeling (Opt-In, Innovation #5)

```bash
# Enable in .env
OPENCLAWN_USER_MODELING=true
```

Tracks dialectic patterns:
- Preferred reasoning style (Socratic, direct, exploratory)
- Common correction patterns
- Domain expertise signals
- Interaction rhythm

**Privacy:**
- Opt-in only
- Versioned (revertible)
- Stored locally in SQLite
- Never sent to LLM providers
- Used only for context shaping

```python
# View user profile
# GET /api/user/profile
{
    "reasoning_preference": "socratic",
    "expertise_domains": ["python", "async", "databases"],
    "interaction_rhythm": "detailed",
    "correction_patterns": [
        "prefers_explicit_types",
        "values_error_handling"
    ]
}
```

---

## Common Patterns

### Pattern: Multi-Step Workflow with Skill Crystallization

```python
# Agent will automatically crystallize this into a reusable skill
# if confidence ≥ 4 and no critical gaps

query = """
1. Read requirements.txt
2. Check for outdated dependencies using pip list --outdated
3. Update requirements.txt with new versions
4. Run tests to verify compatibility
5. Commit changes if tests pass
"""

async for chunk in agent.process_query(query, stream=True):
    print(chunk, end="", flush=True)

# After successful execution, check /skills for new skill
# Will be named something like "dependency-update-workflow"
```

### Pattern: Approval-Gated Autopilot

```python
# Create autopilot that requires approval for destructive actions
autopilot = Autopilot(
    name="weekly_cleanup",
    schedule="0 0 * * 0",  # Weekly on Sunday
    prompt="""
    1. Find all .log files older than 30 days
    2. Create archive of old logs
    3. Delete archived logs (REQUIRES APPROVAL)
    4. Report disk space saved
    """,
    agent_id="maintenance_agent",
    require_approval=True
)

# When delete action is proposed:
# - Execution pauses
# - Proposal created in /autopilots/proposals
# - Notification sent
# - Waits for user approval/rejection
# - Timeout after 1 hour (configurable)
```

### Pattern: Multi-Agent Debate

```python
from conversation.strategies import DebateStrategy

roles = [
    {
        "name": "architect",
        "system_prompt": "You advocate for clean architecture and SOLID principles."
    },
    {
        "name": "pragmatist",
        "system_prompt": "You advocate for shipping fast and iterating."
    },
    {
        "name": "security_expert",
        "system_prompt": "You advocate for security-first design."
    }
]

orchestrator = ConversationOrchestrator(
    strategy=DebateStrategy(rounds=3),
    roles=roles
)

result = await orchestrator.run_conversation(
    initial_prompt="Design a user authentication system for a new SaaS product"
)

# Debate strategy:
# - Round-robin turn order
# - Each role responds to previous arguments
# - Synthesizes final consensus after N rounds
```

### Pattern: Context-Aware Skill Refinement

```python
# If agent makes a mistake and user corrects it:
# "Actually, use asyncio.create_task instead of asyncio.ensure_future"

# On next turn, agent:
# 1. Detects correction (had_correction=1)
# 2. Calls SkillFeedback.resolve_previous()
# 3. If skill was used last turn:
#    - Resets decay score
#    - Creates refined version with correction
#    - Stores as new draft
# 4. Original skill still exists (versioned)

# View skill versions:
# GET /api/skills/{skill_id}/versions
```

---

## Troubleshooting

### Routing Always Uses Same Model

**Problem:** Router ignores complexity and always routes to one model.

**Solution:**
1. Check `/settings` for active override — disable it
2. Review `soul.toml` — if `prefer_local=true` and all queries score low, will stay local
3. Check calibration offsets in `/metrics` — large negative offsets raise thresholds
4. Verify Ollama is running: `curl http://localhost:11434/api/tags`

### Skills Not Being Crystallized

**Problem:** Agent completes multi-tool tasks but no skills are created.

**Checklist:**
- Minimum 3 tool calls required
- Confidence must be ≥4 (self-evaluation)
- Evaluator tier must be ≥ generator tier
- Check logs for "critical gaps" in solution
- Verify `OPENCLAWN_CRYSTALLIZATION_MIN_CONFIDENCE` in `.env`

### Sandbox Tools Failing

**Problem:** `code_run` or `shell_run` returns errors.

**Solutions:**
```bash
# Verify Docker is running
docker ps

# Rebuild sandbox image
docker build -t openclawn-sandbox:latest -f Dockerfile.sandbox .

# Check Docker logs
docker logs <container_id>

# Test sandbox manually
docker run --rm \
  --network none \
  -v $(pwd)/workspace:/workspace:ro \
  openclawn-sandbox:latest \
  python3 -c "print('Hello')"
```

### Memory Context Too Large

**Problem:** Queries fail with token limit errors.

**Solutions:**
1. Reduce `archive_threshold` in `soul.toml` (archives older messages to FTS5)
2. Manually archive old messages: `POST /api/memory/archive`
3. Increase model's context window in router config
4. Enable `ContextCompactor` budget limits in agent config:

```python
agent = Agent(
    ...,
    context_budget=8000  # Max tokens for context
)
```

### Autopilot Proposals Not Appearing

**Problem:** Autopilot runs but no proposals in UI.

**Check:**
1. Verify `require_approval=True` on autopilot
2. Check autopilot logs: `GET /api/autopilots/{id}/logs`
3. Ensure action tools are marked `requires_approval=True`:

```python
# In tools/registry.py
TOOL_REGISTRY = {
    "file_write": {
        "requires_approval": True,  # ← Must be set
        ...
    }
}
```

### Skill Decay Too Aggressive

**Problem:** Useful skills dropping below 0.3 threshold too quickly.

**Solutions:**
1. Adjust decay rate in config:

```python
# config/skill_decay.yaml
decay:
  age_weight: 0.2      # Default: 0.3
  usage_weight: 0.4    # Default: 0.3
  success_weight: 0.4  # Default: 0.4
  base_rate: 0.05      # Default: 0.1 (lower = slower decay)
```

2. Manually boost skill score: `POST /api/skills/{id}/boost`
3. Mark skill as "pinned" (never decays): `POST /api/skills/{id}/pin`

### Web UI Not Loading

**Problem:** Blank page or 404 errors.

**Solutions:**
```bash
# Check FastAPI is running
curl http://localhost:8000/health

# Check static files are built
ls web/static/

# Rebuild frontend (if using build step)
cd web && npm run build

# Check logs
uvicorn web.main:app --reload --log-level debug
```

---

## API Reference (Key Endpoints)

```http
### Chat
POST /api/chat/stream
Content-Type: application/json
{
  "message": "Write a function to parse JSON",
  "agent_id": "default",
  "stream": true
}

### Multi-Agent Conversation
POST /api/converse/stream
{
  "prompt": "Build user auth system",
  "strategy": "pipeline",  # or "debate" or "orchestrator"
  "roles": [...]
}

### Skills
GET /api/skills?min_score=0.5&status=active
POST /api/skills/export
POST /api/skills/import
POST /api/skills/{id}/promote
POST /api/skills/{id}/pin
DELETE /api/skills/{id}  # Soft delete (revertible)

### Autopilots
GET /api/autopilots
POST /api/autopilots
GET /api/autopilots/{id}/proposals
POST /api/autopilots/proposals/{id}/approve
POST /api/autopilots/proposals/{id}/reject

### Routing
GET /api/router/tiers
POST /api/router/calibrate
POST /api/router/calibration/revert
GET /api/router/decisions?limit=100

### Memory
POST /api/memory/archive
GET /api/memory/search?q=authentication
DELETE /api/memory/clear  # Requires confirmation

### Activity
GET /api/activity?limit=50&type=tool_call
GET /api/activity/blockers
```

---

## Testing

```bash
# Run full test suite (420 tests)
pytest

# Run specific test modules
pytest tests/test_router.py
pytest tests/test_crystallizer.py

# Run with coverage
pytest --cov=agent --cov=core --cov-report=html

# Run integration tests (requires Docker + Ollama)
pytest tests/integration/

# Test sandbox specifically
pytest tests/test_sandbox.py -v
```

---

## Advanced: Custom Tool Development

```python
# tools/my_custom_tool.py
from pydantic import BaseModel, Field
from typing import Optional

class MyCustomToolInput(BaseModel):
    """Input schema for my custom tool."""
    target: str = Field(..., description="Target identifier")
    options: Optional[dict] = Field(default=None, description="Optional parameters")

async def my_custom_tool(
    target: str,
    options: Optional[dict] = None,
    workspace_path: str = "./workspace"
) -> dict:
    """
    Custom tool that does something useful.
    
    Args:
        target: Target identifier
        options: Optional parameters
        workspace_path: Workspace root (auto-injected)
    
    Returns:
        Result dict with 'success', 'output', 'error'
    """
    try:
        # Your tool logic here
        result = f"Processed {target}"
        
        return {
            "success": True,
            "output": result,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "output": None,
            "error": str(e)
        }

# Register in tools/registry.py
TOOL_REGISTRY["my_custom_tool"] = {
    "function": my_custom_tool,
    "input_schema": MyCustomToolInput,
    "description": "Does something useful with a target",
    "requires_approval": False,
    "allowed_roles": ["developer", "admin"]  # Optional role restriction
}
```

---

## Resources

- **GitHub**: https://github.com/MuhammadHasbiAshshiddieqy/OpenClawn
- **Documentation**: See `docs/` directory in repo
- **Issues**: https://github.com/MuhammadHasbiAshshiddieqy/OpenClawn/issues
- **License**: MIT

---

**Quick command reference:**

```bash
# Start server
uvicorn web.main:app --reload --port 8000

# Pull Ollama model
ollama pull gemma4:e4b

# Run tests
pytest

# Export skills
curl -X POST http://localhost:8000/api/skills/export

# View routing metrics
open http://localhost:8000/metrics

# Check autopilot proposals
open http://localhost:8000/autopilots
```
