---
name: hermes-agent-architecture
description: Deep expertise in Hermes Agent architecture, implementation patterns, and extension development
triggers:
  - "how does hermes agent work internally"
  - "explain hermes agent architecture"
  - "how to extend hermes agent with custom tools"
  - "implement a hermes plugin"
  - "how does hermes memory system work"
  - "create custom toolset for hermes"
  - "integrate hermes with messaging platform"
  - "optimize hermes agent performance"
---

# Hermes Agent Architecture

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

Hermes Agent is a production-grade LLM agent framework by Nous Research featuring advanced memory management, multi-agent orchestration, 18+ messaging platform integrations, and a sophisticated tool execution system. This skill covers internal architecture, extension patterns, and implementation strategies verified against source code.

## Installation

```bash
# Clone the repository
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent

# Install dependencies
pip install -e .

# Or with Poetry
poetry install

# Basic configuration
cp config.example.yaml config.yaml
# Edit config.yaml with your API keys and preferences
```

## Core Architecture Components

### Agent Loop and Execution

The main agent loop is in `hermes/agent.py`:

```python
from hermes.agent import Agent
from hermes.config import Config

# Initialize agent
config = Config.load("config.yaml")
agent = Agent(config)

# Run interactive session
await agent.run()

# Programmatic execution
response = await agent.process_message(
    "Analyze the repository structure",
    context={"cwd": "/path/to/repo"}
)
```

**Key execution flow:**
1. `process_message()` → Prompt assembly
2. Model inference → Tool calls extraction
3. Tool dispatch via `ToolRegistry`
4. Result aggregation → Memory storage
5. Response generation

### Tool System Architecture

Tools are registered centrally via decorators:

```python
from hermes.tools.registry import tool_registry
from hermes.tools.base import ToolResult

@tool_registry.register(
    name="custom_analyzer",
    description="Analyze code patterns",
    category="analysis",
    parameters={
        "file_path": {
            "type": "string",
            "description": "Path to file to analyze"
        },
        "pattern": {
            "type": "string", 
            "description": "Pattern to search for"
        }
    }
)
async def custom_analyzer(file_path: str, pattern: str, **kwargs) -> ToolResult:
    """Custom code analysis tool."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        matches = re.findall(pattern, content)
        
        return ToolResult(
            success=True,
            data={"matches": matches, "count": len(matches)},
            message=f"Found {len(matches)} matches"
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=str(e)
        )
```

**Toolset grouping** (from `hermes/tools/toolsets.py`):

```python
from hermes.tools.toolsets import Toolset, toolset_registry

@toolset_registry.register("code_analysis")
class CodeAnalysisToolset(Toolset):
    """Custom toolset for code analysis."""
    
    def get_tools(self):
        return [
            "custom_analyzer",
            "list_functions",
            "complexity_check"
        ]
    
    def get_description(self):
        return "Tools for analyzing code structure and patterns"
```

### Memory System

Three-layer architecture (`hermes/memory/`):

```python
from hermes.memory.manager import MemoryManager
from hermes.memory.store import MemoryStore
from hermes.memory.provider import MemoryProvider

# Initialize memory system
store = MemoryStore(db_path="~/.hermes/memory.db")
manager = MemoryManager(store)

# Store interaction
await manager.add_message(
    role="user",
    content="Remember that I prefer functional programming",
    session_id="current_session"
)

# Retrieve relevant memories
memories = await manager.search_memories(
    query="programming preferences",
    limit=5
)

# Freeze snapshot for prompt caching
snapshot = manager.freeze_snapshot()
# This protects the prefix cache boundary
```

**Session search with FTS5:**

```python
from hermes.memory.session_db import SessionDB

session_db = SessionDB(db_path="~/.hermes/sessions.db")

# Search across sessions
results = await session_db.search(
    query="docker configuration",
    limit=10
)

# Get LLM summary of related sessions
summary = await session_db.get_session_summary(
    query="docker issues",
    llm_client=auxiliary_client
)
```

### Context Compression v3

Automatic context management (`hermes/compression/compressor.py`):

```python
from hermes.compression.compressor import ContextCompressor

compressor = ContextCompressor(
    model_client=client,
    max_tokens=128000,
    preserve_recent=5  # Keep last 5 messages uncompressed
)

# Three-stage preprocessing
compressed = await compressor.compress(
    messages=conversation_history,
    strategies=[
        "md5_dedup",        # Remove duplicate tool results
        "smart_collapse",   # Collapse similar adjacent messages
        "param_truncation"  # Truncate large parameters
    ]
)

# Structured summarization
summary = await compressor.summarize_structured(
    messages=old_messages,
    format="bullet_points"  # or "narrative"
)
```

### Skills System

Progressive disclosure with conditional activation (`hermes/skills/`):

```python
from hermes.skills.manager import SkillsManager

skills_manager = SkillsManager(
    skills_dir="~/.hermes/skills",
    config=config
)

# Skills are auto-discovered from markdown files
# Triggered by keywords or explicit @skill references

# Conditional activation example in YAML frontmatter:
"""
---
name: docker-expert
triggers:
  - docker
  - container
  - dockerfile
conditions:
  - file_exists: Dockerfile
  - OR:
    - file_exists: docker-compose.yml
    - env_var: DOCKER_HOST
credentials:
  - DOCKER_API_KEY
---
"""

# Plugin namespace skills (loaded from plugins)
await skills_manager.load_plugin_skills(
    plugin_name="custom_plugin",
    skills_manifest=plugin.get_skills()
)
```

### Multi-Agent Architecture

Four runtime mechanisms:

```python
# 1. Task Delegation
from hermes.tools.delegate import delegate_task

result = await delegate_task(
    task="Research Python async patterns",
    specialist_config={
        "model": "claude-3-7-sonnet",
        "toolsets": ["web_search", "code_analysis"]
    }
)

# 2. Mixture of Agents (MoA)
from hermes.multi_agent.moa import MixtureOfAgents

moa = MixtureOfAgents(
    agents=[
        {"name": "researcher", "model": "gpt-4"},
        {"name": "critic", "model": "claude-3-opus"},
        {"name": "synthesizer", "model": "claude-3-7-sonnet"}
    ]
)

consensus = await moa.deliberate(
    question="What's the best architecture for this service?"
)

# 3. Background Review
from hermes.multi_agent.reviewer import BackgroundReviewer

reviewer = BackgroundReviewer(model="gpt-4o")
review = await reviewer.review_conversation(
    messages=conversation_history,
    focus="security concerns"
)

# 4. Direct Agent Messaging
await agent.send_message(
    to_agent="code_reviewer",
    content="Please review the changes in PR #123"
)
```

### Browser Automation

Multi-backend architecture (`hermes/tools/browser/`):

```python
from hermes.tools.browser import browser_navigate, browser_interact

# Navigate with accessibility tree extraction
result = await browser_navigate(
    url="https://github.com/trending",
    extract_content=True,
    backend="playwright"  # or "selenium", "playwright_firefox"
)

# Interact with elements
await browser_interact(
    action="click",
    selector="button[aria-label='Star']",
    wait_for="networkidle"
)

# Three-layer security:
# 1. URL allowlist/blocklist
# 2. Content filtering  
# 3. Sandboxed execution
```

### Code Execution Sandbox

Secure Python execution (`hermes/tools/code_exec/`):

```python
from hermes.tools.code_exec import execute_code

result = await execute_code(
    code="""
import numpy as np
data = np.random.rand(100)
print(f"Mean: {data.mean()}")
""",
    language="python",
    timeout=30,
    allowed_imports=["numpy", "pandas", "matplotlib"]
)

# Sandbox restrictions:
# - No os.system, subprocess, eval
# - Limited file system access
# - Network requests blocked by default
# - Resource limits enforced
```

**Communication modes:**

```python
# 1. Unix Domain Socket (default)
sandbox_config = {
    "mode": "uds",
    "socket_path": "/tmp/hermes_sandbox.sock"
}

# 2. File RPC (Windows-compatible)
sandbox_config = {
    "mode": "file_rpc", 
    "rpc_dir": "/tmp/hermes_rpc"
}
```

### Messaging Gateway Integration

Platform adapter plugin system (`hermes/gateway/`):

```python
from hermes.gateway.platform_registry import platform_registry
from hermes.gateway.base import PlatformAdapter, PlatformMessage

@platform_registry.register("custom_chat")
class CustomChatAdapter(PlatformAdapter):
    """Custom messaging platform integration."""
    
    platform_name = "custom_chat"
    
    async def initialize(self):
        """Connect to platform API."""
        self.client = CustomChatClient(
            api_key=self.config.get("api_key")
        )
        await self.client.connect()
    
    async def receive_messages(self):
        """Poll for new messages."""
        async for raw_msg in self.client.stream_messages():
            yield PlatformMessage(
                platform="custom_chat",
                channel_id=raw_msg.channel,
                user_id=raw_msg.author_id,
                username=raw_msg.author_name,
                content=raw_msg.text,
                message_id=raw_msg.id,
                timestamp=raw_msg.created_at
            )
    
    async def send_message(self, channel_id: str, content: str, **kwargs):
        """Send response to platform."""
        await self.client.send(
            channel=channel_id,
            text=content
        )
    
    def get_channel_prompt(self, channel_id: str) -> str:
        """Optional: platform-specific instructions."""
        return "Respond in a friendly, casual tone suitable for chat."

# Register and run
gateway = MessagingGateway(config)
gateway.register_platform(CustomChatAdapter(config.platforms.custom_chat))
await gateway.run()
```

**Built-in platform adapters:**
- Discord, Slack, Telegram, IRC
- WeChat, QQ, DingTalk, WeCom (企业微信)
- WhatsApp, Signal, Matrix
- BlueBubbles (iMessage), SMS
- 腾讯元宝 (Tencent Yuanbao)

### Plugin System

Dual hook architecture (`hermes/plugins/`):

```python
from hermes.plugins.base import Plugin, plugin_registry

@plugin_registry.register
class DashboardPlugin(Plugin):
    """Web dashboard for monitoring agent activity."""
    
    name = "dashboard"
    version = "1.0.0"
    
    async def initialize(self, agent):
        """Setup plugin."""
        self.agent = agent
        self.app = create_dashboard_app()
        
        # Register custom commands
        agent.register_command(
            name="/dashboard",
            handler=self.open_dashboard,
            description="Open web dashboard"
        )
        
        # Hook into tool execution
        agent.register_hook(
            "before_tool_call",
            self.log_tool_call
        )
    
    async def log_tool_call(self, tool_name, parameters):
        """Log tool executions to dashboard."""
        await self.app.broadcast_event({
            "type": "tool_call",
            "tool": tool_name,
            "params": parameters,
            "timestamp": time.time()
        })
    
    async def open_dashboard(self, args):
        """Handle /dashboard command."""
        url = await self.app.get_url()
        return f"Dashboard: {url}"

# Load plugins
await agent.load_plugins(plugins_dir="~/.hermes/plugins")
```

### MCP (Model Context Protocol) Integration

```python
from hermes.mcp.client import MCPClient

# Connect to MCP server
mcp = MCPClient(server_url="http://localhost:8000")

# MCP tools automatically registered
await mcp.connect()
mcp_tools = await mcp.list_tools()

# Tools appear in agent's tool registry
# OAuth flows handled automatically for supported MCPs
```

### Smart Model Routing

```python
from hermes.routing.smart_router import SmartRouter

router = SmartRouter(
    default_model="claude-3-7-sonnet",
    short_message_model="claude-3-5-haiku",
    short_message_threshold=100  # tokens
)

# Automatic routing based on complexity
model = router.select_model(
    messages=conversation,
    task_type="code_generation"  # or "chat", "analysis"
)

# Provider-specific features
# - AWS Bedrock with cross-region failover
# - Gemini with OAuth refresh
# - Ollama Cloud distributed routing
# - Tool Gateway for model-specific tool schemas
```

### Prompt Caching Optimization

```python
from hermes.optimization.cache import CacheStrategy

# Freeze memory snapshot to protect prefix
cache_strategy = CacheStrategy(
    enabled=True,
    min_cache_size=2000,  # tokens
    freeze_system_prompt=True
)

# Cache-aware message assembly
messages = prompt_builder.build_messages(
    system_prompt=frozen_system,  # Cached
    memory_snapshot=frozen_memory,  # Cached
    new_messages=recent_messages  # Not cached
)

# Typical savings: 75% reduction in prompt processing costs
```

### Security & Safety

```python
from hermes.security.approval import ApprovalSystem

# Configure danger command approval
approval = ApprovalSystem(
    mode="smart",  # or "manual", "off"
    dangerous_patterns=[
        r"rm -rf",
        r"DROP TABLE",
        r"chmod 777"
    ]
)

# Smart mode uses LLM to assess risk
if await approval.requires_approval(command):
    user_confirmed = await approval.request_approval(
        command=command,
        risk_level="high",
        explanation="This will delete system files"
    )
    if not user_confirmed:
        return ToolResult(success=False, error="User rejected")

# Multi-layer defense:
# 1. Prompt injection guards
# 2. Path traversal protection
# 3. Credential isolation
# 4. PII detection/redaction (in gateway mode)
```

### Error Handling & Fault Tolerance

```python
from hermes.errors import HermesError, ToolExecutionError
from hermes.errors.classifier import ErrorClassifier

classifier = ErrorClassifier()

try:
    result = await tool_function(**params)
except Exception as e:
    # Structured error classification
    error_info = classifier.classify(e)
    
    if error_info.category == "rate_limit":
        # Automatic retry with backoff
        await asyncio.sleep(error_info.retry_after)
        result = await tool_function(**params)
    
    elif error_info.category == "auth_failure":
        # Try fallback credentials
        alt_creds = credential_pool.get_next()
        result = await tool_function(**params, creds=alt_creds)
    
    elif error_info.recoverable:
        # Switch to fallback model
        fallback_model = config.get_fallback_model()
        result = await fallback_model.complete(...)
    
    else:
        # Propagate with context
        raise HermesError(
            message=f"Unrecoverable error in {tool_name}",
            original_error=e,
            context=error_info.context
        )
```

## Configuration Patterns

### Multi-Profile Setup

```yaml
# config.yaml
profiles:
  default:
    model: claude-3-7-sonnet-20250219
    provider: anthropic
    toolsets:
      - filesystem
      - web_search
      - code_execution
    memory:
      enabled: true
      compress_threshold: 50
  
  code_assistant:
    model: claude-3-7-sonnet-20250219
    toolsets:
      - filesystem
      - git
      - code_execution
      - browser
    skills:
      - python-expert
      - rust-expert
    memory:
      enabled: true
      session_isolation: true
  
  researcher:
    model: gpt-4o
    toolsets:
      - web_search
      - browser
      - pdf_tools
    auxiliary_model: gpt-4o-mini
    memory:
      compress_threshold: 30

# Load specific profile
hermes --profile code_assistant
```

### Credential Pool Management

```yaml
credentials:
  anthropic:
    pool:
      - api_key: ${ANTHROPIC_KEY_1}
        rate_limit: 1000
      - api_key: ${ANTHROPIC_KEY_2}
        rate_limit: 500
    selection_strategy: round_robin  # or least_used, weighted, failover
  
  openai:
    pool:
      - api_key: ${OPENAI_KEY_MAIN}
        organization: ${OPENAI_ORG}
      - api_key: ${OPENAI_KEY_BACKUP}
```

### Gateway Configuration

```yaml
gateway:
  enabled: true
  platforms:
    discord:
      enabled: true
      token: ${DISCORD_TOKEN}
      allowed_channels:
        - "1234567890"
      admin_users:
        - "user#1234"
      channel_prompts:
        "1234567890": "You are a helpful coding assistant."
    
    slack:
      enabled: true
      token: ${SLACK_TOKEN}
      signing_secret: ${SLACK_SIGNING_SECRET}
      socket_mode: true
    
    wechat:
      enabled: true
      auto_login: true
      contact_whitelist:
        - "friend_name"
  
  session_management:
    timeout: 3600  # seconds
    max_per_user: 5
    pii_redaction: true
```

## CLI Commands

```bash
# Interactive mode
hermes

# One-shot command
hermes "Analyze the codebase structure"

# With specific profile
hermes --profile researcher "Find recent papers on RAG"

# Dump configuration/state
hermes dump --format json --output state.json

# Skill management
hermes skills list
hermes skills reload
hermes --reload-skills  # Reload during session

# Session management
hermes sessions list
hermes sessions search "docker configuration"
hermes sessions delete <session_id>

# Gateway mode
hermes gateway --platforms discord,slack

# Generate training data
hermes trajectory --output dataset/ --runs 100
```

### Slash Commands (in interactive mode)

```
/exit or /quit          - Exit session
/reset                  - Clear conversation
/dump                   - Export state
/models                 - List available models
/switch <model>         - Switch model
/profile <name>         - Switch profile
/tools                  - List active tools
/skills                 - List loaded skills
/reload-skills          - Reload skill library
/memory search <query>  - Search memories
/help                   - Show commands
```

## Development Patterns

### Custom Provider Transport

```python
from hermes.providers.base import ProviderTransport
from hermes.providers.registry import provider_registry

@provider_registry.register("custom_llm")
class CustomLLMTransport(ProviderTransport):
    """Custom LLM provider integration."""
    
    async def create_completion(self, messages, model, **kwargs):
        """Send completion request."""
        response = await self.http_client.post(
            f"{self.base_url}/v1/chat/completions",
            json={
                "model": model,
                "messages": self._format_messages(messages),
                "tools": self._format_tools(kwargs.get("tools", []))
            },
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        
        return self._parse_response(response)
    
    async def stream_completion(self, messages, model, **kwargs):
        """Stream completion chunks."""
        async with self.http_client.stream(
            "POST",
            f"{self.base_url}/v1/chat/completions",
            json={"model": model, "messages": messages, "stream": True}
        ) as stream:
            async for line in stream.aiter_lines():
                if line.startswith("data: "):
                    yield self._parse_chunk(line)
    
    def _format_tools(self, tools):
        """Convert Hermes tool schema to provider format."""
        return [
            {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"]
            }
            for tool in tools
        ]
```

### Context Reference System

```python
from hermes.context.references import ContextReferenceParser

parser = ContextReferenceParser(
    sandbox_root="/workspace",
    max_file_size=100000  # bytes
)

# Parse @references from user input
content, references = await parser.parse(
    "@file:src/main.py @url:https://docs.python.org/3/library/asyncio.html"
)

# Automatic injection into context
context_additions = await parser.resolve_references(references)

# Supported reference types:
# @file:path/to/file
# @folder:path/to/dir
# @diff:branch1..branch2  
# @url:https://...
# @git:commit-hash
```

### Parallel Tool Execution

```python
from hermes.tools.parallel import ParallelExecutor

executor = ParallelExecutor(max_workers=5)

# Automatic safety detection
tool_calls = [
    {"name": "search_web", "params": {"query": "Python async"}},
    {"name": "search_web", "params": {"query": "Rust async"}},
    {"name": "write_file", "params": {"path": "test.txt", "content": "x"}},
]

# Intelligent batching (searches run parallel, write serialized)
results = await executor.execute_batch(
    tool_calls,
    conflict_detection=True  # Checks path overlaps
)

# Three safety categories:
# - read_only: Always safe to parallelize
# - stateless: Safe if parameters don't conflict  
# - stateful: Always serialize
```

### Voice Mode Integration

```python
from hermes.voice.stt import STTProvider
from hermes.voice.tts import TTSProvider

# Speech-to-Text (3 providers: OpenAI, Deepgram, AssemblyAI)
stt = STTProvider(
    provider="deepgram",
    api_key="${DEEPGRAM_API_KEY}",
    language="en"
)

transcript = await stt.transcribe_audio(
    audio_file="recording.wav"
)

# Text-to-Speech (5 providers)
tts = TTSProvider(
    provider="gemini",  # or openai, elevenlabs, kitten, xai
    voice="alloy"
)

audio_data = await tts.synthesize(
    text="Analysis complete. Found 3 issues.",
    output_format="mp3"
)

# Push-to-talk workflow
from hermes.voice.ptt import PushToTalkSession

async with PushToTalkSession(stt, tts, agent) as session:
    await session.run()  # Handles recording, transcription, TTS
```

## Troubleshooting

### Memory Issues

**Problem:** Context window exceeded despite compression.

```python
# Solution 1: Adjust compression threshold
config.memory.compress_threshold = 30  # More aggressive

# Solution 2: Limit memory retrieval
config.memory.max_memories_per_query = 3

# Solution 3: Use summarization
compressor.summarize_structured(
    messages=old_messages[:-10],
    format="bullet_points"
)
```

**Problem:** Memories not being recalled.

```python
# Check FTS5 index
from hermes.memory.session_db import SessionDB
db = SessionDB()
await db.rebuild_fts_index()

# Verify embedding similarity threshold
config.memory.similarity_threshold = 0.7  # Lower = more matches
```

### Tool Execution

**Problem:** Tool results too large.

```python
# Three-layer overflow protection active:
# 1. Tool-level truncation (automatic)
# 2. Single result persistence (check ~/.hermes/tool_cache/)
# 3. Round budget enforcement (configured in config.yaml)

config.tools.max_result_size = 50000  # bytes per tool
config.tools.round_token_budget = 100000  # total per round
```

**Problem:** Parallel execution conflicts.

```python
# Enable path conflict detection
from hermes.tools.parallel import PathConflictDetector

detector = PathConflictDetector()
conflicts = detector.find_conflicts([
    ("write_file", {"path": "src/main.py"}),
    ("read_file", {"path": "src/main.py"})  # Conflict!
])

# Configure safety classification
@tool_registry.register(safety_class="stateful")  # Force serialization
async def my_stateful_tool(...):
    ...
```

### Gateway Issues

**Problem:** Platform authentication failing.

```python
# Check credentials
hermes gateway --test-auth --platform discord

# For QR-code platforms (WeChat, DingTalk)
config.gateway.platforms.wechat.auto_login = true
config.gateway.platforms.dingtalk.use_qr = true

# Verify webhook delivery (Slack, Discord)
config.gateway.platforms.slack.verify_signature = true
```

**Problem:** PII leaking in logs.

```python
# Enable redaction
config.gateway.pii_redaction = true
config.gateway.redact_patterns:
  - r'\b\d{3}-\d{2}-\d{4}\b'  # SSN
  - r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # Email
```

### Performance

**Problem:** Slow response times.

```python
# Enable prompt caching
config.optimization.cache.enabled = true
config.optimization.cache.min_size = 2000

# Use smart routing for simple queries
config.routing.short_message_model = "claude-3-5-haiku"
config.routing.threshold = 100

# Parallel tool execution
config.tools.parallel_execution = true
config.tools.max_parallel_workers = 5
```

**Problem:** High API costs.

```python
# Aggressive compression
config.memory.compress_threshold = 20

# Auxiliary model for non-critical tasks
config.auxiliary_model = "gpt-4o-mini"

# Credential rotation to distribute load
config.credentials.anthropic.selection_strategy = "round_robin"
```

### Debugging

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Dump full state
hermes dump --include-memory --include-tools --output debug.json

# Trace tool execution
config.debug.trace_tools = true

# Monitor with dashboard plugin
await agent.load_plugin("dashboard")
# Access at http://localhost:7777
```

## Best Practices

1. **Memory management**: Use `freeze_snapshot()` before each model call to maximize cache hits
2. **Tool development**: Always return `ToolResult` with structured data, mark safety class correctly
3. **Multi-agent**: Prefer `delegate_task` for focused sub-tasks, MoA for complex decisions
4. **Gateway mode**: Use `channel_prompts` for platform-specific behavior, enable PII redaction
5. **Skills**: Write skills with clear triggers, use conditional activation to reduce noise
6. **Security**: Enable danger command approval in production, use sandbox for code execution
7. **Performance**: Enable prompt caching, use auxiliary models for simple tasks, parallelize read-only tools
8. **Extensions**: Register via decorators, use hook system for cross-cutting concerns, follow plugin structure for complex additions

## Resources

- Source code: https://github.com/NousResearch/hermes-agent
- Architecture wiki: https://github.com/cclank/Hermes-Wiki
- Discord community: Nous Research server
- Model: Hermes-3-Llama-3.1-405B optimized for tool use
