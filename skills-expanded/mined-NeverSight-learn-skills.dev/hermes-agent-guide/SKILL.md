---
name: hermes-agent-guide
description: Comprehensive Chinese guide for Hermes Agent framework covering installation, architecture, memory systems, skills, tools, multi-agent orchestration, and monetization strategies
triggers:
  - how do I get started with Hermes Agent
  - show me Hermes Agent documentation
  - explain Hermes Agent architecture
  - help me deploy Hermes Agent
  - what are Hermes Agent skills and tools
  - how to build AI agents with Hermes
  - Hermes Agent vs OpenClaw comparison
  - monetize with Hermes Agent
---

# Hermes Agent Guide

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

This skill provides comprehensive knowledge of the Hermes Agent framework based on the most extensive Chinese guide available. Hermes Agent is a powerful open-source AI Agent framework that inherits from OpenClaw with significant upgrades in architecture, memory systems, skill ecosystem, and automation capabilities.

## What is Hermes Agent

Hermes Agent is an advanced AI Agent framework developed by Nous Research that enables:

- **Autonomous Task Execution**: Agents can plan, execute, and learn from complex multi-step tasks
- **Three-Layer Memory System**: Session memory, persistent memory, and skill-level memory
- **Rich Skill Ecosystem**: 47+ built-in tools across 7 categories, plus Skills Hub integration
- **MCP Protocol Support**: Access to 6000+ Model Context Protocol services
- **Multi-Platform Integration**: Connect to Discord, Slack, WeChat, Feishu, and 15+ platforms
- **Multi-Agent Orchestration**: Coordinate multiple agents for complex workflows

## Installation

### Local Installation (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Required: OPENAI_API_KEY or other LLM provider keys
```

### Docker Installation (Recommended for Production)

```bash
# Pull the official image
docker pull nousresearch/hermes-agent:latest

# Create docker-compose.yml
cat > docker-compose.yml << EOF
version: '3.8'
services:
  hermes:
    image: nousresearch/hermes-agent:latest
    environment:
      - OPENAI_API_KEY=\${OPENAI_API_KEY}
      - HERMES_MEMORY_TYPE=persistent
    volumes:
      - ./data:/app/data
      - ./skills:/app/skills
    ports:
      - "8080:8080"
    restart: unless-stopped
EOF

# Start the service
docker-compose up -d
```

### VPS Deployment

```bash
# On Ubuntu/Debian
sudo apt update && sudo apt install -y python3.11 python3-pip git

# Clone and setup
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
pip3 install -r requirements.txt

# Setup systemd service
sudo tee /etc/systemd/system/hermes-agent.service << EOF
[Unit]
Description=Hermes Agent Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment="OPENAI_API_KEY=${OPENAI_API_KEY}"
ExecStart=$(which python3) main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable hermes-agent
sudo systemctl start hermes-agent
```

## Core Architecture

Hermes Agent uses a five-layer architecture:

### 1. Interface Layer
Handles user interactions across multiple platforms:

```python
from hermes.interface import DiscordInterface, SlackInterface, CLIInterface

# CLI interface
cli = CLIInterface()
cli.start()

# Discord bot
discord = DiscordInterface(
    token=os.getenv("DISCORD_BOT_TOKEN"),
    intents=["messages", "guilds"]
)
discord.run()

# Slack app
slack = SlackInterface(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)
slack.start()
```

### 2. Orchestration Layer
Manages agent lifecycle and task coordination:

```python
from hermes.orchestrator import AgentOrchestrator
from hermes.agent import HermesAgent

orchestrator = AgentOrchestrator()

# Create and register agents
research_agent = HermesAgent(
    name="research_assistant",
    model="gpt-4",
    skills=["web_search", "summarization"]
)

code_agent = HermesAgent(
    name="code_assistant", 
    model="claude-3-opus",
    skills=["code_generation", "code_review"]
)

orchestrator.register_agent(research_agent)
orchestrator.register_agent(code_agent)

# Execute coordinated task
result = await orchestrator.execute_task(
    "Research the latest AI frameworks and generate a comparison report",
    agents=["research_assistant", "code_assistant"]
)
```

### 3. Agent Core Layer
The brain of each agent:

```python
from hermes.agent import HermesAgent
from hermes.memory import MemoryConfig
from hermes.skills import SkillRegistry

agent = HermesAgent(
    name="my_assistant",
    model="gpt-4-turbo",
    temperature=0.7,
    memory_config=MemoryConfig(
        session_memory=True,
        persistent_memory=True,
        vector_store="chromadb"
    ),
    skill_registry=SkillRegistry.load_default(),
    system_prompt="""You are a helpful AI assistant with access to 
    various tools and a persistent memory system."""
)

# Agent automatically plans and executes
response = await agent.chat("Analyze my project's GitHub issues and create a priority matrix")
```

### 4. Tool Layer
47+ built-in tools organized in 7 categories:

```python
from hermes.tools import (
    WebSearchTool, FileSystemTool, GitHubTool,
    DatabaseTool, CodeExecutionTool, APIRequestTool
)

# Configure tools
tools = [
    WebSearchTool(api_key=os.getenv("SERPER_API_KEY")),
    GitHubTool(token=os.getenv("GITHUB_TOKEN")),
    FileSystemTool(allowed_paths=["/workspace"]),
    CodeExecutionTool(sandbox_mode=True),
    DatabaseTool(connection_string=os.getenv("DATABASE_URL"))
]

# Attach to agent
agent.add_tools(tools)
```

### 5. Integration Layer
Connects to external services via MCP:

```python
from hermes.mcp import MCPClient

mcp = MCPClient()

# Add MCP servers
mcp.add_server("filesystem", "npx -y @modelcontextprotocol/server-filesystem /workspace")
mcp.add_server("github", "npx -y @modelcontextprotocol/server-github")
mcp.add_server("postgres", "npx -y @modelcontextprotocol/server-postgres")

# Use in agent
agent.connect_mcp(mcp)
```

## Memory System

### Session Memory
Temporary conversation context:

```python
from hermes.memory import SessionMemory

session = SessionMemory(
    max_tokens=4096,
    summarization_threshold=3000
)

# Automatically managed during conversation
agent.memory.session = session
```

### Persistent Memory
Long-term knowledge storage:

```python
from hermes.memory import PersistentMemory

persistent = PersistentMemory(
    backend="chromadb",
    collection_name="hermes_memory",
    embedding_model="text-embedding-3-small"
)

# Store important information
await persistent.store(
    content="User prefers Python for backend development",
    metadata={"type": "preference", "category": "development"}
)

# Query relevant memories
memories = await persistent.query(
    "What are the user's coding preferences?",
    top_k=5
)
```

### Skill-Level Memory
Memory specific to each skill:

```python
from hermes.skills import Skill

class ProjectManagementSkill(Skill):
    def __init__(self):
        super().__init__(name="project_management")
        self.memory = self.get_skill_memory()
    
    async def track_project(self, project_name: str, status: str):
        await self.memory.store({
            "project": project_name,
            "status": status,
            "timestamp": datetime.now()
        })
    
    async def get_active_projects(self):
        return await self.memory.query(
            "status:active",
            filter_type="metadata"
        )
```

## Skills System

### Using Built-in Skills

```python
from hermes.skills import SkillRegistry

registry = SkillRegistry()

# Load specific skills
web_skill = registry.get("web_automation")
data_skill = registry.get("data_analysis")

# Load all skills from category
dev_skills = registry.get_category("development")

# Attach to agent
agent.add_skills([web_skill, data_skill])
```

### Creating Custom Skills

```python
from hermes.skills import Skill, skill_action

class CustomResearchSkill(Skill):
    """Advanced research skill with citation tracking"""
    
    name = "advanced_research"
    description = "Perform deep research with source tracking"
    
    def __init__(self):
        super().__init__()
        self.sources = []
    
    @skill_action(
        description="Search and summarize academic papers",
        parameters={
            "query": {"type": "string", "required": True},
            "max_results": {"type": "integer", "default": 10}
        }
    )
    async def search_papers(self, query: str, max_results: int = 10):
        # Implementation
        results = await self.tools.web_search(
            f"{query} site:arxiv.org OR site:scholar.google.com",
            max_results=max_results
        )
        
        # Track sources
        for result in results:
            self.sources.append({
                "title": result.title,
                "url": result.url,
                "timestamp": datetime.now()
            })
        
        summary = await self.summarize(results)
        return {
            "summary": summary,
            "sources": self.sources
        }
    
    @skill_action(description="Generate bibliography from tracked sources")
    async def generate_bibliography(self):
        return "\n".join([
            f"- {s['title']}: {s['url']}"
            for s in self.sources
        ])

# Register and use
registry.register(CustomResearchSkill())
```

### Skills Hub Integration

```python
from hermes.skills import SkillsHub

hub = SkillsHub(api_key=os.getenv("SKILLS_HUB_API_KEY"))

# Search for skills
results = hub.search("data visualization")

# Install skill
skill = hub.install("community/advanced-charts")

# Add to agent
agent.add_skill(skill)
```

## Tool Categories

### 1. Web & Network Tools

```python
from hermes.tools import WebSearchTool, WebScrapingTool, APIRequestTool

# Web search
search = WebSearchTool(provider="serper", api_key=os.getenv("SERPER_API_KEY"))
results = await search.search("latest AI news")

# Web scraping
scraper = WebScrapingTool(user_agent="Hermes-Agent/1.0")
content = await scraper.scrape("https://example.com")

# API requests
api = APIRequestTool()
response = await api.request(
    method="POST",
    url="https://api.example.com/data",
    headers={"Authorization": f"Bearer {os.getenv('API_TOKEN')}"},
    json={"query": "data"}
)
```

### 2. File System Tools

```python
from hermes.tools import FileSystemTool

fs = FileSystemTool(
    base_path="/workspace",
    allowed_operations=["read", "write", "list"]
)

# Read file
content = await fs.read_file("project/README.md")

# Write file
await fs.write_file("output/report.txt", "Report content")

# List directory
files = await fs.list_directory("project/src")
```

### 3. Code Execution Tools

```python
from hermes.tools import CodeExecutionTool

executor = CodeExecutionTool(
    sandbox_mode=True,
    timeout=30,
    allowed_imports=["requests", "pandas", "numpy"]
)

# Execute Python code
result = await executor.execute_python("""
import pandas as pd
data = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
print(data.describe())
""")

print(result.stdout)
print(result.return_value)
```

### 4. Database Tools

```python
from hermes.tools import DatabaseTool

db = DatabaseTool(
    connection_string=os.getenv("DATABASE_URL"),
    read_only=False
)

# Query
results = await db.query("SELECT * FROM users WHERE active = true")

# Execute with parameters
await db.execute(
    "INSERT INTO logs (message, level) VALUES ($1, $2)",
    ["Operation completed", "INFO"]
)
```

### 5. Version Control Tools

```python
from hermes.tools import GitHubTool

github = GitHubTool(token=os.getenv("GITHUB_TOKEN"))

# Create issue
issue = await github.create_issue(
    repo="owner/repo",
    title="Bug: Memory leak in agent loop",
    body="Detailed description...",
    labels=["bug", "priority-high"]
)

# Create pull request
pr = await github.create_pull_request(
    repo="owner/repo",
    title="Fix memory leak",
    head="feature-branch",
    base="main",
    body="This PR fixes the memory leak issue"
)
```

### 6. Communication Tools

```python
from hermes.tools import EmailTool, SlackTool

# Send email
email = EmailTool(
    smtp_host=os.getenv("SMTP_HOST"),
    smtp_port=587,
    username=os.getenv("SMTP_USER"),
    password=os.getenv("SMTP_PASS")
)

await email.send(
    to=["user@example.com"],
    subject="Daily Report",
    body="Here is your daily report...",
    attachments=["/reports/daily.pdf"]
)

# Slack notification
slack = SlackTool(token=os.getenv("SLACK_BOT_TOKEN"))
await slack.send_message(
    channel="#general",
    text="Task completed successfully!"
)
```

### 7. Data Processing Tools

```python
from hermes.tools import DataAnalysisTool, ImageProcessingTool

# Data analysis
analyzer = DataAnalysisTool()
stats = await analyzer.analyze_csv("/data/sales.csv")

# Image processing
image_tool = ImageProcessingTool()
await image_tool.resize("/images/photo.jpg", width=800, height=600)
await image_tool.convert("/images/photo.jpg", format="webp")
```

## Multi-Platform Integration

### Discord Bot

```python
from hermes.platforms import DiscordPlatform

discord = DiscordPlatform(
    token=os.getenv("DISCORD_BOT_TOKEN"),
    command_prefix="!hermes"
)

# Register agent
discord.register_agent(agent)

# Custom command
@discord.command(name="analyze")
async def analyze_command(ctx, *, query: str):
    result = await agent.chat(query)
    await ctx.send(result)

discord.run()
```

### Slack App

```python
from hermes.platforms import SlackPlatform

slack = SlackPlatform(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)

slack.register_agent(agent)

# Event handler
@slack.event("app_mention")
async def handle_mention(event):
    response = await agent.chat(event["text"])
    await slack.post_message(event["channel"], response)

slack.start()
```

### WeChat Integration

```python
from hermes.platforms import WeChatPlatform

wechat = WeChatPlatform(
    app_id=os.getenv("WECHAT_APP_ID"),
    app_secret=os.getenv("WECHAT_APP_SECRET")
)

wechat.register_agent(agent)

@wechat.message_handler()
async def handle_message(message):
    response = await agent.chat(message.content)
    return response

wechat.run()
```

## MCP Protocol Integration

### Connecting MCP Servers

```python
from hermes.mcp import MCPClient, MCPServer

# Initialize client
mcp = MCPClient()

# Add filesystem server
mcp.add_server(
    name="filesystem",
    command="npx -y @modelcontextprotocol/server-filesystem",
    args=["/workspace"]
)

# Add PostgreSQL server
mcp.add_server(
    name="postgres",
    command="npx -y @modelcontextprotocol/server-postgres",
    env={"DATABASE_URL": os.getenv("DATABASE_URL")}
)

# Add GitHub server
mcp.add_server(
    name="github",
    command="npx -y @modelcontextprotocol/server-github",
    env={"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")}
)

# Connect to agent
agent.connect_mcp(mcp)

# Agent can now use all MCP tools
response = await agent.chat(
    "Read my database schema and create documentation in the workspace"
)
```

### Custom MCP Server

```python
from hermes.mcp import MCPServer, mcp_tool

class CustomMCPServer(MCPServer):
    name = "custom_analytics"
    
    @mcp_tool(
        name="analyze_metrics",
        description="Analyze custom business metrics"
    )
    async def analyze_metrics(self, metric_type: str, date_range: str):
        # Your implementation
        data = await self.fetch_metrics(metric_type, date_range)
        analysis = self.perform_analysis(data)
        return analysis
    
    @mcp_tool(name="generate_report")
    async def generate_report(self, template: str):
        # Implementation
        pass

# Register and use
mcp.register_server(CustomMCPServer())
```

## Automation & Scheduling

### Cron Jobs

```python
from hermes.automation import CronScheduler

scheduler = CronScheduler(agent)

# Daily report at 9 AM
@scheduler.cron("0 9 * * *")
async def daily_report():
    report = await agent.chat(
        "Generate a summary of yesterday's activities and pending tasks"
    )
    await send_report(report)

# Hourly monitoring
@scheduler.cron("0 * * * *")
async def monitor_system():
    status = await agent.chat("Check all system metrics and alert if anomalies")
    if "ALERT" in status:
        await notify_admin(status)

scheduler.start()
```

### Event-Driven Automation

```python
from hermes.automation import EventTrigger

triggers = EventTrigger(agent)

# On file change
@triggers.on_file_change("/workspace/config.yaml")
async def config_changed(filepath):
    await agent.chat(f"Configuration file {filepath} was modified. Validate and reload.")

# On webhook
@triggers.on_webhook("/hooks/deployment")
async def deployment_hook(payload):
    await agent.chat(f"New deployment detected: {payload['version']}. Run tests and notify team.")

# On database change
@triggers.on_database_event("users", event_type="insert")
async def new_user(record):
    await agent.chat(f"New user registered: {record['email']}. Send welcome sequence.")

triggers.start()
```

## Multi-Agent Orchestration

### Sequential Workflow

```python
from hermes.orchestrator import SequentialWorkflow

workflow = SequentialWorkflow()

# Define agents
researcher = HermesAgent(name="researcher", skills=["web_search", "summarization"])
writer = HermesAgent(name="writer", skills=["content_generation"])
reviewer = HermesAgent(name="reviewer", skills=["quality_check"])

# Build workflow
workflow.add_step(researcher, "Research the topic thoroughly")
workflow.add_step(writer, "Write a comprehensive article based on research")
workflow.add_step(reviewer, "Review and improve the article")

# Execute
result = await workflow.execute("Write an article about quantum computing")
```

### Parallel Processing

```python
from hermes.orchestrator import ParallelWorkflow

workflow = ParallelWorkflow()

# Create specialized agents
agent1 = HermesAgent(name="analyzer1", skills=["data_analysis"])
agent2 = HermesAgent(name="analyzer2", skills=["data_analysis"])
agent3 = HermesAgent(name="analyzer3", skills=["data_analysis"])

# Run in parallel
workflow.add_parallel_tasks([
    (agent1, "Analyze sales data for Q1"),
    (agent2, "Analyze sales data for Q2"),
    (agent3, "Analyze sales data for Q3")
])

# Aggregate results
results = await workflow.execute_parallel()
summary = await aggregator_agent.chat(f"Summarize these quarterly analyses: {results}")
```

### Hierarchical Organization

```python
from hermes.orchestrator import HierarchicalOrchestrator

# Manager agent
manager = HermesAgent(
    name="manager",
    model="gpt-4",
    role="coordinator"
)

# Worker agents
workers = [
    HermesAgent(name="dev1", skills=["code_generation"]),
    HermesAgent(name="dev2", skills=["testing"]),
    HermesAgent(name="dev3", skills=["documentation"])
]

orchestrator = HierarchicalOrchestrator(
    manager=manager,
    workers=workers
)

# Manager delegates tasks
result = await orchestrator.execute(
    "Build a REST API for user management with tests and documentation"
)
```

## Configuration

### Environment Variables

```bash
# Core configuration
HERMES_MODEL=gpt-4-turbo
HERMES_TEMPERATURE=0.7
HERMES_MAX_TOKENS=4096

# LLM Provider keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Memory configuration
HERMES_MEMORY_TYPE=persistent
HERMES_VECTOR_STORE=chromadb
CHROMADB_PATH=./data/chromadb

# Tools & Services
SERPER_API_KEY=your_serper_key
GITHUB_TOKEN=your_github_token
DATABASE_URL=postgresql://user:pass@localhost/db

# Platform tokens
DISCORD_BOT_TOKEN=your_discord_token
SLACK_BOT_TOKEN=your_slack_token
WECHAT_APP_ID=your_wechat_id
WECHAT_APP_SECRET=your_wechat_secret

# MCP configuration
MCP_ENABLED=true
MCP_SERVERS_PATH=./mcp_servers

# Security
HERMES_SANDBOX_MODE=true
HERMES_ALLOWED_PATHS=/workspace,/data
HERMES_MAX_EXECUTION_TIME=30
```

### Configuration File

```python
# config.yaml
agent:
  name: my_hermes_agent
  model: gpt-4-turbo
  temperature: 0.7
  max_iterations: 10
  
memory:
  type: persistent
  backend: chromadb
  collection_name: hermes_memory
  embedding_model: text-embedding-3-small
  
skills:
  auto_load: true
  categories:
    - development
    - research
    - communication
  custom_path: ./custom_skills
  
tools:
  web_search:
    provider: serper
    max_results: 10
  code_execution:
    sandbox: true
    timeout: 30
  database:
    read_only: false
    
platforms:
  - type: discord
    enabled: true
  - type: slack
    enabled: true
    
mcp:
  enabled: true
  servers:
    - name: filesystem
      command: npx -y @modelcontextprotocol/server-filesystem
      args: ["/workspace"]
    - name: github
      command: npx -y @modelcontextprotocol/server-github

# Load configuration
from hermes.config import load_config

config = load_config("config.yaml")
agent = HermesAgent.from_config(config)
```

## Common Patterns

### Error Handling & Retries

```python
from hermes.utils import retry_with_backoff

@retry_with_backoff(max_retries=3, backoff_factor=2)
async def execute_task_with_retry(agent, task):
    try:
        result = await agent.chat(task)
        return result
    except Exception as e:
        agent.logger.error(f"Task failed: {e}")
        raise

# With custom error handling
async def safe_execution(agent, task):
    try:
        result = await execute_task_with_retry(agent, task)
        await agent.memory.store({"task": task, "status": "success"})
        return result
    except Exception as e:
        await agent.memory.store({"task": task, "status": "failed", "error": str(e)})
        await notify_admin(f"Task failed: {task}")
        return None
```

### Streaming Responses

```python
async def stream_agent_response(agent, query):
    async for chunk in agent.chat_stream(query):
        print(chunk, end="", flush=True)
        # Or send to UI
        await websocket.send(chunk)
```

### Context Management

```python
from hermes.context import ContextManager

async def task_with_context(agent, user_id):
    context = ContextManager(agent)
    
    # Load user context
    await context.load_user_context(user_id)
    
    # Add temporary context
    with context.temporary({
        "project": "current_project",
        "mode": "development"
    }):
        result = await agent.chat("Review the latest code changes")
    
    # Context automatically cleaned up
    return result
```

### Monitoring & Logging

```python
from hermes.monitoring import AgentMonitor

monitor = AgentMonitor(agent)

# Track metrics
monitor.track_token_usage()
monitor.track_response_time()
monitor.track_success_rate()

# Export metrics
metrics = monitor.get_metrics()
print(f"Total tokens: {metrics['total_tokens']}")
print(f"Avg response time: {metrics['avg_response_time']}s")
print(f"Success rate: {metrics['success_rate']}%")

# Log to file
monitor.export_logs("agent_metrics.json")
```

## Troubleshooting

### Common Issues

**1. Agent not responding**
```python
# Check agent status
print(agent.is_active)
print(agent.get_status())

# Reset agent state
await agent.reset()

# Check logs
agent.logger.set_level("DEBUG")
```

**2. Memory issues**
```python
# Clear session memory
await agent.memory.clear_session()

# Rebuild vector store
await agent.memory.persistent.rebuild_index()

# Check memory usage
stats = await agent.memory.get_stats()
print(f"Session tokens: {stats['session_tokens']}")
print(f"Persistent entries: {stats['persistent_entries']}")
```

**3. Tool execution failures**
```python
# Validate tool configuration
for tool in agent.tools:
    print(f"{tool.name}: {tool.is_configured()}")

# Test tool individually
tool = agent.get_tool("web_search")
result = await tool.test_connection()
print(result)

# Enable sandbox mode
agent.config.sandbox_mode = True
```

**4. MCP connection issues**
```python
# Check MCP servers
print(agent.mcp.list_servers())

# Test MCP server
server_status = await agent.mcp.test_server("filesystem")
print(server_status)

# Restart MCP client
await agent.mcp.restart()
```

**5. High token usage**
```python
# Optimize memory settings
agent.memory.session.max_tokens = 2000
agent.memory.session.enable_summarization = True

# Use cheaper model for simple tasks
agent.set_model("gpt-3.5-turbo")

# Limit context window
agent.config.max_context_tokens = 3000
```

## Migration from OpenClaw

### Key Differences

1. **Architecture**: Five layers vs. three layers
2. **Memory**: Three-tier system vs. two-tier
3. **Skills**: Skills Hub vs. basic plugin system
4. **MCP**: Native support vs. plugin-based
5. **Multi-agent**: Built-in orchestration vs. manual coordination

### Migration Steps

```python
# OpenClaw code
from openclaw import Agent

openclaw_agent = Agent(
    model="gpt-4",
    plugins=["web_search", "file_ops"]
)

# Equivalent Hermes code
from hermes import HermesAgent

hermes_agent = HermesAgent(
    model="gpt-4",
    skills=["web_search", "file_operations"]
)

# Memory migration
# OpenClaw memory export
openclaw_memory = openclaw_agent.export_memory()

# Import to Hermes
await hermes_agent.memory.import_from_openclaw(openclaw_memory)

# Plugin to Skill mapping
skill_mapping = {
    "web_search": "web_automation",
    "file_ops": "file_system",
    "code_runner": "code_execution"
}

for openclaw_plugin, hermes_skill in skill_mapping.items():
    if openclaw_plugin in openclaw_agent.plugins:
        hermes_agent.add_skill(hermes_skill)
```

## Best Practices

1. **Always use environment variables for secrets**
2. **Enable sandbox mode for code execution in production**
3. **Implement proper error handling and retries**
4. **Monitor token usage and costs**
5. **Use persistent memory for important user data**
6. **Regularly backup memory stores**
7. **Test agents in isolation before orchestration**
8. **Use appropriate models for task complexity**
9. **Implement rate limiting for external API calls**
10. **Log all agent actions for debugging**

## Resources

- **Official Repository**: https://github.com/NousResearch/hermes-agent
- **Skills Hub**: https://skills.hermes.ai
- **Documentation**: https://docs.hermes.ai
- **Community Discord**: https://discord.gg/hermes
- **This Guide**: https://github.com/jwangkun/hermes-agent-guide (16 chapters, 300,000+ words in Chinese)

## Quick Reference

```python
# Basic agent setup
from hermes import HermesAgent

agent = HermesAgent(
    model="gpt-4-turbo",
    temperature=0.7,
    skills=["web_search", "code_execution"],
    memory_type="persistent"
)

# Simple chat
response =
