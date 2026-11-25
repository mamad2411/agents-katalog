---
name: "agent-construction"
description: "Multi-agent architecture, orchestrator patterns, tool design, agent loops, memory, error handling, handoffs"
---

# Agent Construction Skill

## When to activate
- Designing a multi-agent system with Claude (orchestrator + subagents)
- Building a Claude-powered agent that uses tools across multiple turns
- Designing memory for a long-running agent (in-context vs. external)
- Handling agent errors, retries, and stopping conditions
- Implementing agent handoffs between specialized subagents

## When NOT to use
- Single-turn Claude API calls — the Claude API skill is sufficient
- Simple chatbots without tool use or autonomous decision-making
- LangChain/LlamaIndex abstractions — address the abstraction layer directly

## Instructions

### Agent architecture patterns

**Single agent with tools** — one Claude instance, multiple tools, loops until task is done:
```
User → Agent → [Tool A] → [Tool B] → Agent → User
```

**Orchestrator + subagents** — one parent spawns specialized children:
```
User → Orchestrator → [ResearchAgent] → [WriterAgent] → Orchestrator → User
```

**Pipeline** — agents hand off results in sequence:
```
User → Agent1(classify) → Agent2(extract) → Agent3(generate) → User
```

Choose the simplest architecture that solves the problem. Single agent with tools handles most cases.

### Tool design
```python
# Tool definitions for multi-turn agent loop
tools = [
    {
        "name": "search_web",
        "description": "Search the web for current information. Use when you need facts not in your training data.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "read_file",
        "description": "Read contents of a file by path.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Absolute file path"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file. Creates the file if it doesn't exist.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["path", "content"]
        }
    }
]
```

Tool design rules:
- Description must tell Claude WHEN to use it, not just what it does
- Keep `input_schema` minimal — only required fields, no optional noise
- Return structured data (JSON), not prose, so Claude can use it reliably
- One tool per action — don't bundle read+write into one tool

### Agent loop
```python
import anthropic
import json

client = anthropic.Anthropic()

def run_agent(task: str, max_iterations: int = 20) -> str:
    messages = [{"role": "user", "content": task}]
    
    for iteration in range(max_iterations):
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=AGENT_SYSTEM_PROMPT,
            tools=tools,
            messages=messages,
        )
        
        # Append assistant's response
        messages.append({"role": "assistant", "content": response.content})
        
        if response.stop_reason == "end_turn":
            # Extract final text response
            return next(b.text for b in response.content if hasattr(b, "text"))
        
        if response.stop_reason == "tool_use":
            # Execute all tool calls in this response
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result) if not isinstance(result, str) else result
                    })
            
            messages.append({"role": "user", "content": tool_results})
        else:
            # Unexpected stop reason
            break
    
    raise RuntimeError(f"Agent exceeded {max_iterations} iterations without completing")


def execute_tool(name: str, inputs: dict) -> any:
    match name:
        case "search_web":
            return search(inputs["query"])
        case "read_file":
            return Path(inputs["path"]).read_text()
        case "write_file":
            Path(inputs["path"]).write_text(inputs["content"])
            return {"success": True, "path": inputs["path"]}
        case _:
            return {"error": f"Unknown tool: {name}"}
```

### System prompt for agents
```
AGENT_SYSTEM_PROMPT = """You are an autonomous agent completing tasks step by step.

Approach:
1. Analyze the task before acting
2. Use the minimum tools necessary
3. Check your work before declaring done
4. If a tool returns an error, diagnose and retry once — if it fails again, report the error

Stopping conditions — declare "DONE: <result>" when:
- The task is fully complete
- You've hit an unrecoverable error after retrying
- You've been asked to do something harmful or impossible

Never loop more than 3 times on the same tool call with the same inputs.
"""
```

### Memory patterns

**In-context memory** (messages array) — for single session, small state:
```python
# Summarize when context grows large
if count_tokens(messages) > 150_000:
    summary = summarize_messages(messages[:-5])  # keep last 5 turns
    messages = [
        {"role": "user", "content": f"[Previous context summary]\n{summary}"},
        {"role": "assistant", "content": "Understood. Continuing from where we left off."},
        *messages[-5:]
    ]
```

**External memory** (for multi-session agents):
```python
# Simple file-based memory
class AgentMemory:
    def __init__(self, path: str):
        self.path = Path(path)
        self.data = json.loads(self.path.read_text()) if self.path.exists() else {}

    def remember(self, key: str, value: any):
        self.data[key] = {"value": value, "timestamp": datetime.utcnow().isoformat()}
        self.path.write_text(json.dumps(self.data, indent=2))

    def recall(self, key: str) -> any:
        entry = self.data.get(key)
        return entry["value"] if entry else None

    def as_context(self) -> str:
        if not self.data:
            return ""
        lines = [f"- {k}: {v['value']}" for k, v in self.data.items()]
        return "Known context:\n" + "\n".join(lines)
```

### Orchestrator pattern
```python
def orchestrate(task: str) -> str:
    # Step 1: Planning agent decomposes the task
    plan = run_subagent(
        model="claude-sonnet-4-6",
        system="You are a planner. Decompose tasks into numbered steps.",
        task=f"Decompose this task into steps: {task}",
        tools=[]  # No tools needed for planning
    )

    # Step 2: Execute each step with specialized agents
    results = []
    for step in parse_steps(plan):
        agent_type = classify_step(step)  # "research" | "code" | "write"
        result = run_subagent(
            model=agent_model(agent_type),
            system=agent_system_prompt(agent_type),
            task=step,
            tools=agent_tools(agent_type),
            context="\n".join(results)  # Give context from previous steps
        )
        results.append(f"Step result: {result}")

    # Step 3: Synthesis agent combines results
    return run_subagent(
        model="claude-sonnet-4-6",
        system="You are a synthesizer. Combine step results into a final answer.",
        task=f"Original task: {task}\n\nStep results:\n" + "\n".join(results),
        tools=[]
    )
```

### Error handling and stopping conditions
```python
class AgentError(Exception):
    pass

class MaxIterationsError(AgentError):
    pass

class ToolFailureError(AgentError):
    pass

def execute_tool_safe(name: str, inputs: dict, consecutive_failures: dict) -> dict:
    try:
        result = execute_tool(name, inputs)
        consecutive_failures[name] = 0
        return {"success": True, "result": result}
    except Exception as e:
        consecutive_failures[name] = consecutive_failures.get(name, 0) + 1
        if consecutive_failures[name] >= 3:
            raise ToolFailureError(f"Tool {name} failed 3 consecutive times: {e}")
        return {"success": False, "error": str(e), "retry": True}
```

### Handoff pattern
```python
# Parent agent passes context explicitly — subagents have no session memory
def handoff_to_specialist(context: dict, task: str, specialist: str) -> str:
    handoff_prompt = f"""
Context from orchestrator:
{json.dumps(context, indent=2)}

Your task:
{task}
"""
    return run_subagent(
        system=SPECIALIST_PROMPTS[specialist],
        task=handoff_prompt,
        tools=SPECIALIST_TOOLS[specialist]
    )
```

## Example

**User:** Build a research agent that takes a topic, searches the web for 3 sources, reads each URL, and writes a 500-word summary with citations to a file.

**Expected output:**
- `tools` list: `search_web`, `fetch_url`, `write_file`
- System prompt: instructs agent to search → fetch 3 URLs → synthesize → write file before declaring done
- `run_agent(task)` loop with `max_iterations=15`
- Error handling: if `fetch_url` fails, try next search result
- Final output: path to the written summary file

---
