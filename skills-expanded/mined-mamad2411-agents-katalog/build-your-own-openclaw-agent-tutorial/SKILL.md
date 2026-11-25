---
name: build-your-own-openclaw-agent-tutorial
description: Step-by-step guide to building AI agents from simple chat loops to autonomous multi-agent systems with tools, memory, and event-driven architecture
triggers:
  - how do I build an AI agent from scratch
  - teach me to create an autonomous agent
  - show me how to build an OpenClaw-style agent
  - guide me through building an agent with tools and memory
  - help me create a multi-agent system
  - how to build an event-driven AI agent
  - create an agent with scheduled tasks and persistence
  - build an agent that can use tools and skills
---

# Build Your Own OpenClaw Agent Tutorial

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

A comprehensive tutorial for building AI agents progressively, from a basic chat loop to a production-ready autonomous agent system. This project walks through 18 steps covering single-agent capabilities, event-driven architecture, multi-agent collaboration, and production features like memory and concurrency control.

## What This Tutorial Teaches

The tutorial is organized into 4 phases:

1. **Phase 1 (Steps 0-6)**: Single agent with tools, skills, persistence, and web access
2. **Phase 2 (Steps 7-10)**: Event-driven architecture with multi-platform support
3. **Phase 3 (Steps 11-15)**: Autonomous agents with routing and collaboration
4. **Phase 4 (Steps 16-17)**: Production features like concurrency and long-term memory

## Initial Setup

### Clone the Repository

```bash
git clone https://github.com/czl9707/build-your-own-openclaw.git
cd build-your-own-openclaw
```

### Configure API Keys

```bash
# Copy example config
cp default_workspace/config.example.yaml default_workspace/config.user.yaml
```

Edit `default_workspace/config.user.yaml`:

```yaml
llm:
  model: "gpt-4"  # or anthropic/claude-3-5-sonnet-20241022, etc.
  api_key: "${OPENAI_API_KEY}"  # Use environment variable
  # See https://docs.litellm.ai/docs/providers for all providers

# Optional: Add additional services
web:
  search_api_key: "${SERPER_API_KEY}"
```

### Install Dependencies (for each step)

```bash
cd 00-chat-loop  # or any step directory
pip install -r requirements.txt
```

## Phase 1: Building a Capable Single Agent

### Step 0: Basic Chat Loop

The foundation - a simple conversation loop with an LLM.

```python
# 00-chat-loop/main.py
from litellm import completion

def chat_loop():
    messages = []
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['/exit', '/quit']:
            break
            
        messages.append({"role": "user", "content": user_input})
        
        response = completion(
            model="gpt-4",
            messages=messages,
            api_key="${OPENAI_API_KEY}"
        )
        
        assistant_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_message})
        
        print(f"Assistant: {assistant_message}")

if __name__ == "__main__":
    chat_loop()
```

Run it:
```bash
cd 00-chat-loop
python main.py
```

### Step 1: Adding Tools

Give your agent function-calling capabilities.

```python
# 01-tools/tools.py
def get_current_weather(location: str) -> dict:
    """Get the current weather for a location."""
    # Tool implementation
    return {"location": location, "temperature": 72, "condition": "sunny"}

# Tool schema for LLM
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name, e.g. San Francisco"
                }
            },
            "required": ["location"]
        }
    }
}
```

Using tools in the chat loop:

```python
import json
from litellm import completion

response = completion(
    model="gpt-4",
    messages=messages,
    tools=[weather_tool],
    tool_choice="auto"
)

# Handle tool calls
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        # Execute tool
        result = get_current_weather(**arguments)
        
        # Add tool result to messages
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })
```

### Step 2: Skills with SKILL.md

Extend agent capabilities through markdown skill files.

```markdown
<!-- skills/web_search.md -->
# Web Search Skill

You can search the internet using the `search_web` tool.

## When to Use
- User asks for current information
- Need to verify facts
- Looking for recent news

## Example
User: "What's the latest news on AI?"
You: Let me search for that. [calls search_web("latest AI news")]
```

Loading skills:

```python
# 02-skills/skill_loader.py
import os

def load_skills(skills_dir="skills"):
    """Load all .md files from skills directory."""
    skills_content = []
    
    for filename in os.listdir(skills_dir):
        if filename.endswith(".md"):
            with open(os.path.join(skills_dir, filename), 'r') as f:
                skills_content.append(f.read())
    
    return "\n\n".join(skills_content)

# Add to system prompt
system_prompt = f"""You are a helpful assistant.

## Your Skills
{load_skills()}
"""
```

### Step 3: Conversation Persistence

Save conversations to resume later.

```python
# 03-persistence/session_manager.py
import json
from datetime import datetime
from pathlib import Path

class SessionManager:
    def __init__(self, sessions_dir="sessions"):
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(exist_ok=True)
    
    def save_session(self, session_id: str, messages: list):
        """Save conversation history."""
        session_file = self.sessions_dir / f"{session_id}.json"
        data = {
            "session_id": session_id,
            "updated_at": datetime.now().isoformat(),
            "messages": messages
        }
        with open(session_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_session(self, session_id: str) -> list:
        """Load conversation history."""
        session_file = self.sessions_dir / f"{session_id}.json"
        if not session_file.exists():
            return []
        
        with open(session_file, 'r') as f:
            data = json.load(f)
            return data.get("messages", [])
    
    def list_sessions(self) -> list:
        """List all available sessions."""
        return [f.stem for f in self.sessions_dir.glob("*.json")]
```

Usage:

```python
manager = SessionManager()

# Load or create session
session_id = "my-conversation"
messages = manager.load_session(session_id)

# After each exchange
manager.save_session(session_id, messages)
```

### Step 4: Slash Commands

Direct user control over agent behavior.

```python
# 04-slash-commands/commands.py
class CommandHandler:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.commands = {
            '/new': self.new_session,
            '/load': self.load_session,
            '/list': self.list_sessions,
            '/save': self.save_session,
            '/clear': self.clear_session,
            '/help': self.show_help
        }
    
    def handle(self, user_input: str, current_session: str, messages: list):
        """Handle slash commands."""
        parts = user_input.split()
        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        if command in self.commands:
            return self.commands[command](args, current_session, messages)
        
        return None  # Not a command
    
    def new_session(self, args, current_session, messages):
        new_id = args[0] if args else f"session_{int(time.time())}"
        return {"action": "new_session", "session_id": new_id}
    
    def load_session(self, args, current_session, messages):
        if not args:
            print("Usage: /load <session_id>")
            return {"action": "none"}
        
        loaded = self.session_manager.load_session(args[0])
        return {"action": "load_session", "session_id": args[0], "messages": loaded}
```

### Step 5: Context Compaction

Manage token limits by summarizing old messages.

```python
# 05-compaction/compactor.py
from litellm import completion

class MessageCompactor:
    def __init__(self, max_messages=20):
        self.max_messages = max_messages
    
    def compact_if_needed(self, messages: list) -> list:
        """Compact messages if they exceed threshold."""
        if len(messages) <= self.max_messages:
            return messages
        
        # Keep system message and recent messages
        system_msgs = [m for m in messages if m["role"] == "system"]
        recent_msgs = messages[-(self.max_messages - 2):]
        
        # Summarize older messages
        old_msgs = messages[len(system_msgs):-len(recent_msgs)]
        summary = self._summarize_messages(old_msgs)
        
        return system_msgs + [
            {"role": "system", "content": f"Previous conversation summary:\n{summary}"}
        ] + recent_msgs
    
    def _summarize_messages(self, messages: list) -> str:
        """Generate summary of message history."""
        conversation = "\n".join([
            f"{m['role']}: {m['content']}" for m in messages
        ])
        
        response = completion(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": f"Summarize this conversation concisely:\n\n{conversation}"
            }]
        )
        
        return response.choices[0].message.content
```

### Step 6: Web Tools

Give your agent internet access.

```python
# 06-web-tools/web_tools.py
import requests
import os

def search_web(query: str, num_results: int = 5) -> list:
    """Search the web using Serper API."""
    api_key = os.getenv("SERPER_API_KEY")
    
    response = requests.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": api_key},
        json={"q": query, "num": num_results}
    )
    
    results = response.json()
    return [
        {
            "title": r.get("title"),
            "link": r.get("link"),
            "snippet": r.get("snippet")
        }
        for r in results.get("organic", [])
    ]

def fetch_webpage(url: str) -> str:
    """Fetch and extract text from a webpage."""
    from bs4 import BeautifulSoup
    
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    return soup.get_text(separator="\n", strip=True)
```

## Phase 2: Event-Driven Architecture

### Step 7: Event-Driven Refactor

Decouple components with an event bus.

```python
# 07-event-driven/event_bus.py
from typing import Callable, Dict, List
from dataclasses import dataclass
from enum import Enum

class EventType(Enum):
    MESSAGE_RECEIVED = "message_received"
    MESSAGE_SENT = "message_sent"
    TOOL_CALLED = "tool_called"
    SESSION_CREATED = "session_created"

@dataclass
class Event:
    type: EventType
    data: dict
    source: str

class EventBus:
    def __init__(self):
        self.listeners: Dict[EventType, List[Callable]] = {}
    
    def subscribe(self, event_type: EventType, handler: Callable):
        """Subscribe to an event type."""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(handler)
    
    def publish(self, event: Event):
        """Publish an event to all subscribers."""
        if event.type in self.listeners:
            for handler in self.listeners[event.type]:
                handler(event)

# Usage
bus = EventBus()

def on_message(event: Event):
    print(f"Received: {event.data['content']}")

bus.subscribe(EventType.MESSAGE_RECEIVED, on_message)
bus.publish(Event(
    type=EventType.MESSAGE_RECEIVED,
    data={"content": "Hello!"},
    source="user"
))
```

### Step 9: Multi-Channel Support

Support Discord, Slack, Telegram, etc.

```python
# 09-channels/discord_channel.py
import discord
from event_bus import EventBus, Event, EventType

class DiscordChannel:
    def __init__(self, event_bus: EventBus, token: str):
        self.event_bus = event_bus
        self.client = discord.Client(intents=discord.Intents.default())
        self.token = token
        
        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return
            
            # Publish to event bus
            self.event_bus.publish(Event(
                type=EventType.MESSAGE_RECEIVED,
                data={
                    "content": message.content,
                    "channel_id": str(message.channel.id),
                    "user_id": str(message.author.id)
                },
                source="discord"
            ))
        
        # Subscribe to outgoing messages
        self.event_bus.subscribe(EventType.MESSAGE_SENT, self.send_message)
    
    async def send_message(self, event: Event):
        """Send message to Discord."""
        if event.data.get("channel") != "discord":
            return
        
        channel = self.client.get_channel(int(event.data["channel_id"]))
        await channel.send(event.data["content"])
    
    def start(self):
        self.client.run(self.token)
```

## Phase 3: Multi-Agent Systems

### Step 11: Agent Routing

Route requests to specialized agents.

```python
# 11-multi-agent-routing/router.py
from litellm import completion

class AgentRouter:
    def __init__(self, agents: dict):
        self.agents = agents  # {"code": CodeAgent(), "research": ResearchAgent()}
    
    def route(self, user_message: str) -> str:
        """Determine which agent should handle the request."""
        agent_descriptions = "\n".join([
            f"- {name}: {agent.description}"
            for name, agent in self.agents.items()
        ])
        
        response = completion(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": f"""Which agent should handle this request?

Available agents:
{agent_descriptions}

User request: {user_message}

Respond with just the agent name."""
            }]
        )
        
        agent_name = response.choices[0].message.content.strip()
        return agent_name if agent_name in self.agents else "default"
```

### Step 12: Scheduled Tasks (Cron Heartbeat)

Run agents on a schedule.

```python
# 12-cron-heartbeat/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

class AgentScheduler:
    def __init__(self, event_bus):
        self.scheduler = BackgroundScheduler()
        self.event_bus = event_bus
    
    def schedule_task(self, agent_id: str, cron: str, task: callable):
        """Schedule a recurring task."""
        self.scheduler.add_job(
            func=task,
            trigger='cron',
            **self._parse_cron(cron),
            id=f"{agent_id}_{datetime.now().timestamp()}"
        )
    
    def _parse_cron(self, cron: str) -> dict:
        """Parse cron expression to APScheduler format."""
        # "0 9 * * *" -> {"hour": 9, "minute": 0}
        parts = cron.split()
        return {
            "minute": parts[0],
            "hour": parts[1],
            "day": parts[2],
            "month": parts[3],
            "day_of_week": parts[4]
        }
    
    def start(self):
        self.scheduler.start()

# Usage
scheduler = AgentScheduler(event_bus)
scheduler.schedule_task(
    "morning_brief",
    "0 9 * * *",  # 9 AM daily
    lambda: send_daily_briefing()
)
scheduler.start()
```

### Step 15: Agent Dispatch

Agents collaborate to complete tasks.

```python
# 15-agent-dispatch/dispatcher.py
class AgentDispatcher:
    def __init__(self, agents: dict, event_bus):
        self.agents = agents
        self.event_bus = event_bus
    
    async def dispatch_task(self, task: str, requesting_agent: str):
        """Dispatch a task to another agent."""
        # Determine best agent for subtask
        target_agent = self._select_agent(task)
        
        # Execute subtask
        result = await self.agents[target_agent].execute(task)
        
        # Return result to requesting agent
        self.event_bus.publish(Event(
            type=EventType.TASK_COMPLETED,
            data={
                "task": task,
                "result": result,
                "requester": requesting_agent
            },
            source=target_agent
        ))
        
        return result
```

## Phase 4: Production Features

### Step 16: Concurrency Control

Prevent race conditions with multiple agents.

```python
# 16-concurrency-control/lock_manager.py
import asyncio
from contextlib import asynccontextmanager

class LockManager:
    def __init__(self):
        self.locks = {}
    
    @asynccontextmanager
    async def acquire(self, resource_id: str):
        """Acquire lock for a resource."""
        if resource_id not in self.locks:
            self.locks[resource_id] = asyncio.Lock()
        
        async with self.locks[resource_id]:
            yield

# Usage
lock_manager = LockManager()

async def process_session(session_id: str):
    async with lock_manager.acquire(f"session:{session_id}"):
        # Only one agent can access this session at a time
        messages = load_session(session_id)
        # ... process ...
        save_session(session_id, messages)
```

### Step 17: Long-Term Memory

Store and retrieve relevant memories.

```python
# 17-memory/memory_store.py
from chromadb import Client
from chromadb.config import Settings

class MemoryStore:
    def __init__(self, collection_name="agent_memory"):
        self.client = Client(Settings(persist_directory="./memory_db"))
        self.collection = self.client.get_or_create_collection(collection_name)
    
    def store_memory(self, content: str, metadata: dict):
        """Store a memory with embeddings."""
        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[f"mem_{metadata.get('timestamp', 0)}"]
        )
    
    def recall(self, query: str, n_results: int = 5) -> list:
        """Retrieve relevant memories."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return [
            {
                "content": doc,
                "metadata": meta
            }
            for doc, meta in zip(
                results['documents'][0],
                results['metadatas'][0]
            )
        ]

# Usage
memory = MemoryStore()

# Store memory
memory.store_memory(
    "User prefers Python over JavaScript",
    {"user_id": "user123", "timestamp": 1234567890}
)

# Recall relevant memories
relevant = memory.recall("What languages does the user like?")
```

## Common Patterns

### Full Agent Implementation

```python
# Complete agent with all features
class Agent:
    def __init__(self, config_path="config.user.yaml"):
        self.config = self.load_config(config_path)
        self.event_bus = EventBus()
        self.session_manager = SessionManager()
        self.memory = MemoryStore()
        self.tools = self.load_tools()
        self.skills = self.load_skills()
        
    async def process_message(self, message: str, session_id: str):
        # Load session with lock
        async with lock_manager.acquire(f"session:{session_id}"):
            messages = self.session_manager.load_session(session_id)
            
            # Recall relevant memories
            memories = self.memory.recall(message)
            context = self.build_context(memories)
            
            # Add user message
            messages.append({"role": "user", "content": message})
            
            # Compact if needed
            messages = self.compactor.compact_if_needed(messages)
            
            # Get response with tools
            response = await completion(
                model=self.config['llm']['model'],
                messages=[{"role": "system", "content": context}] + messages,
                tools=self.tools
            )
            
            # Handle tool calls
            while response.choices[0].message.tool_calls:
                # Execute tools and continue
                pass
            
            # Store memory of interaction
            self.memory.store_memory(
                f"User: {message}\nAssistant: {response_text}",
                {"session_id": session_id, "timestamp": time.time()}
            )
            
            # Save session
            self.session_manager.save_session(session_id, messages)
            
            return response_text
```

## Troubleshooting

### API Key Issues
```bash
# Check environment variables
echo $OPENAI_API_KEY

# Verify config.user.yaml uses correct env var syntax
# ✓ Correct: api_key: "${OPENAI_API_KEY}"
# ✗ Wrong: api_key: "$OPENAI_API_KEY" or api_key: "sk-..."
```

### LiteLLM Provider Errors
```python
# Test your LLM config
from litellm import completion

response = completion(
    model="gpt-4",  # or your model
    messages=[{"role": "user", "content": "test"}],
    api_key="${OPENAI_API_KEY}"
)
print(response.choices[0].message.content)
```

### Session Persistence Issues
```python
# Verify sessions directory exists and is writable
import os
sessions_dir = "sessions"
os.makedirs(sessions_dir, exist_ok=True)
print(f"Sessions dir: {os.path.abspath(sessions_dir)}")
```

### Memory/ChromaDB Issues
```bash
# Install ChromaDB dependencies
pip install chromadb

# Clear memory database if corrupted
rm -rf ./memory_db
```

## Next Steps

1. Start with **Step 0** and progress sequentially
2. Each step builds on previous ones
3. Reference the [example project (pickle-bot)](https://github.com/czl9707/pickle-bot) for a complete implementation
4. Customize each step for your specific use case
5. Mix and match features based on your needs

## Resources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Tutorial Homepage](https://build-your-own-openclaw.kiyo-n-zane.com/)
- [OpenClaw Project](https://github.com/openclaw/openclaw)
- Each step's README.md contains detailed explanations
