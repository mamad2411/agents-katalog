---
name: agentic-ai
description: >
  Expert guidance on agentic AI systems, autonomous agents, and AI orchestration. Use for: 
  building agentic AI systems, tool orchestration, memory systems, planning and reasoning, 
  multi-step workflows, feedback loops, evaluation frameworks, ReAct patterns, and building 
  sophisticated AI pipelines.
license: MIT
compatibility: opencode
metadata:
  audience: ml-engineers, developers
  category: artificial-intelligence
  tags: [agentic-ai, autonomous-agents, ai-agents, llm-agents]
---

# Agentic AI — Implementation Guide

Covers: **Agent Architectures · Tool Use · Memory Systems · Planning · Evaluation · Multi-Agent Systems**

-----

## Understanding Agentic AI

### What Makes an AI "Agentic"?

An agentic AI system differs from traditional AI assistants in several fundamental ways. While a standard language model responds to each prompt independently, an agentic system maintains state across interactions, takes autonomous actions to achieve goals, and can plan multi-step sequences of operations.

The key characteristics that define agentic AI include: autonomy in decision-making without requiring constant human guidance, the ability to plan and execute multi-step workflows, the capacity to use external tools and APIs to interact with the world, memory systems that preserve context across interactions, and feedback mechanisms that enable learning and adaptation.

**Agentic systems can be categorized by their complexity:**

Simple reflex agents respond to stimuli based on predetermined rules. Goal-based agents work toward specific objectives using planning algorithms. Utility-based agents maximize expected utility through optimization. Learning agents improve performance through experience. Multi-agent systems involve multiple AI agents collaborating or competing.

**Common Agent Architectures:**

- **ReAct (Reason + Act)** — Combines reasoning traces with action execution
- **Reflexion** — Adds verbal reinforcement learning for self-reflection
- **Tool Use Agents** — Integrate external tools and APIs into reasoning
- **Plan-and-Execute** — Separates planning from execution phases
- **Multi-Agent** — Multiple specialized agents working together

### When to Use Agentic Systems

Agentic systems excel in scenarios requiring complex multi-step reasoning, dynamic tool orchestration, persistent context across sessions, autonomous decision-making, iterative refinement, or coordination of multiple specialized components. They are particularly valuable for building AI assistants that can take actions rather than just generating text.

Traditional completion-based AI remains superior for simple question-answering, content generation, summarization, and single-turn interactions. The complexity of agentic systems is justified when the task genuinely requires persistent state, tool use, or multi-step execution.

-----

## Agent Architecture Design

### Core Agent Loop

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from enum import Enum
from datetime import datetime

class AgentState(Enum):
    IDLE = "idle"
    REASONING = "reasoning"
    ACTING = "acting"
    OBSERVING = "observing"
    FINISHED = "finished"
    ERROR = "error"

@dataclass
class Thought:
    """A single thought in the agent's reasoning chain"""
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    action: Optional[str] = None
    observation: Optional[str] = None

@dataclass
class AgentConfig:
    """Configuration for agent behavior"""
    model: str = "claude-sonnet-4-5-20251120"
    max_iterations: int = 100
    max_tokens_per_iteration: int = 4096
    temperature: float = 0.7
    tools: List[Any] = field(default_factory=list)
    memory_system: Optional['MemorySystem'] = None
    planning_enabled: bool = True
    reflection_enabled: bool = True

class BaseAgent:
    """Core agent implementation"""
    
    def __init__(self, config: AgentConfig, llm_client):
        self.config = config
        self.llm = llm_client
        self.state = AgentState.IDLE
        self.thought_history: List[Thought] = []
        self.tools = {tool.name: tool for tool in config.tools}
    
    async def run(self, task: str) -> Dict[str, Any]:
        """Main agent loop"""
        self.task = task
        self.thought_history = []
        
        for iteration in range(self.config.max_iterations):
            # Think phase
            thought = await self.think(task)
            self.thought_history.append(thought)
            
            # Act phase
            if thought.action:
                result = await self.act(thought.action)
                thought.observation = result
                
                # Check if task is complete
                if self.is_complete(result):
                    return self.format_result()
            else:
                # No action needed, provide final response
                return {"status": "completed", "response": thought.content}
        
        return {"status": "max_iterations", "thoughts": self.thought_history}
    
    async def think(self, task: str) -> Thought:
        """Reason about the current state and determine next action"""
        self.state = AgentState.REASONING
        
        # Build context from history and memory
        context = self.build_context()
        
        # Get LLM response with action
        response = await self.llm.chat([
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": f"Task: {task}\n\n{context}"}
        ])
        
        return Thought(content=response.content, action=response.tool_use)
    
    async def act(self, action: str) -> str:
        """Execute the determined action"""
        self.state = AgentState.ACTING
        
        if action in self.tools:
            return await self.tools[action].execute()
        else:
            return action  # Plain text response
    
    def build_context(self) -> str:
        """Build context from thought history and memory"""
        history = "\n".join([
            f"- {t.content}" + (f" -> {t.observation}" if t.observation else "")
            for t in self.thought_history[-5:]
        ])
        
        memory = ""
        if self.config.memory_system:
            memory = f"\nRelevant memory:\n{self.config.memory_system.retrieve(self.task)}"
        
        return f"History:\n{history}{memory}"
    
    def is_complete(self, result: str) -> bool:
        """Determine if task is complete"""
        completion_indicators = [
            "task complete",
            "finished",
            "successfully",
            "delivered"
        ]
        return any(indicator in result.lower() for indicator in completion_indicators)
    
    def format_result(self) -> Dict[str, Any]:
        """Format the final result"""
        return {
            "status": "completed",
            "thoughts": [t.content for t in self.thought_history],
            "actions": [t.action for t in self.thought_history if t.action],
            "observations": [t.observation for t in self.thought_history if t.observation]
        }
```

### ReAct Implementation

```python
class ReActAgent(BaseAgent):
    """ReAct (Reason + Act) agent implementation"""
    
    def get_system_prompt(self) -> str:
        return """You are a ReAct agent. For each step:
1. Think about what to do
2. Act by calling a tool or responding
3. Observe the result

Format your response as:
Thought: [your reasoning]
Action: [tool_name] [arguments] OR respond [your response]
Observation: [result of action]"""
    
    async def think(self, task: str) -> Thought:
        """ReAct-style reasoning"""
        context = self.build_context()
        
        # Prompt for ReAct format
        prompt = f"""Task: {task}

{context}

Follow this format:
Thought: [your reasoning]
Action: [tool_to_use] [arguments]
Observation: [result]"""
        
        response = await self.llm.chat([
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": prompt}
        ])
        
        # Parse response
        return self.parse_response(response.content)
    
    def parse_response(self, response: str) -> Thought:
        """Parse ReAct format response"""
        lines = response.strip().split("\n")
        thought = Thought(content="")
        
        for line in lines:
            if line.startswith("Thought:"):
                thought.content = line[8:].strip()
            elif line.startswith("Action:"):
                action = line[7:].strip()
                if action.startswith("respond"):
                    thought.action = action[8:].strip()
                else:
                    # Parse tool call
                    parts = action.split(" ", 1)
                    thought.action = parts[0] if len(parts) > 1 else action
            elif line.startswith("Observation:"):
                thought.observation = line[12:].strip()
        
        return thought
```

-----

## Tool Systems

### Tool Definition and Execution

```python
from abc import ABC, abstractmethod
from typing import Any, Dict
import json

class Tool(ABC):
    """Base class for agent tools"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description for LLM"""
        pass
    
    @property
    @abstractmethod
    def input_schema(self) -> Dict:
        """JSON schema for tool input"""
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> str:
        """Execute the tool"""
        pass

class SearchTool(Tool):
    """Web search tool"""
    
    @property
    def name(self) -> str:
        return "search"
    
    @property
    def description(self) -> str:
        return "Search the web for information. Use this when you need current information or facts not in your training data."
    
    @property
    def input_schema(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "max_results": {"type": "integer", "default": 5}
            },
            "required": ["query"]
        }
    
    async def execute(self, query: str, max_results: int = 5) -> str:
        # Implementation would call search API
        results = await self.search_api.search(query, max_results)
        return json.dumps(results)

class CodeExecutionTool(Tool):
    """Code execution tool"""
    
    @property
    def name(self) -> str:
        return "execute_code"
    
    @property
    def description(self) -> str:
        return "Execute Python code in a sandboxed environment. Use this for calculations, data processing, or testing code snippets."
    
    @property
    def input_schema(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Python code to execute"},
                "timeout": {"type": "integer", "default": 30}
            },
            "required": ["code"]
        }
    
    async def execute(self, code: str, timeout: int = 30) -> str:
        # Would execute in sandbox
        result = await self.sandbox.execute(code, timeout)
        return str(result)

class FileSystemTool(Tool):
    """File system operations"""
    
    @property
    def name(self) -> str:
        return "file_operations"
    
    @property
    def description(self) -> str:
        return "Read, write, or list files in the working directory."
    
    @property
    def input_schema(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "operation": {"type": "string", "enum": ["read", "write", "list"]},
                "path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["operation", "path"]
        }
    
    async def execute(self, operation: str, path: str, content: str = None) -> str:
        if operation == "read":
            return self.read_file(path)
        elif operation == "write":
            return self.write_file(path, content)
        elif operation == "list":
            return self.list_directory(path)
```

### Tool Manager

```python
class ToolManager:
    """Manages available tools for the agent"""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.tool_descriptions: List[Dict] = []
    
    def register(self, tool: Tool):
        """Register a new tool"""
        self.tools[tool.name] = tool
        self.tool_descriptions.append({
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.input_schema
        })
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get tool by name"""
        return self.tools.get(name)
    
    def get_descriptions(self) -> str:
        """Get formatted tool descriptions for LLM"""
        desc = "Available tools:\n"
        for t in self.tool_descriptions:
            desc += f"- {t['name']}: {t['description']}\n"
            desc += f"  Input: {json.dumps(t['input_schema'])}\n"
        return desc
```

-----

## Memory Systems

### Working Memory

```python
class WorkingMemory:
    """Short-term memory for current task"""
    
    def __init__(self, max_items: int = 10):
        self.max_items = max_items
        self.items: List[Dict] = []
    
    def add(self, item: Dict):
        """Add item to working memory"""
        self.items.append({
            **item,
            "timestamp": datetime.now()
        })
        
        # Keep only recent items
        if len(self.items) > self.max_items:
            self.items = self.items[-self.max_items:]
    
    def get_recent(self, n: int = 5) -> List[Dict]:
        """Get n most recent items"""
        return self.items[-n:]
    
    def clear(self):
        """Clear working memory"""
        self.items = []
    
    def summarize(self) -> str:
        """Get text summary of working memory"""
        if not self.items:
            return "No items in working memory"
        
        summary = "Recent items:\n"
        for item in self.items[-5:]:
            summary += f"- {item.get('type', 'unknown')}: {item.get('content', '')[:100]}\n"
        return summary
```

### Semantic Memory

```python
class SemanticMemory:
    """Long-term semantic memory using embeddings"""
    
    def __init__(self, vector_store, embedding_model):
        self.vector_store = vector_store
        self.embedding_model = embedding_model
    
    async def store(self, content: str, metadata: Dict = None):
        """Store content in semantic memory"""
        embedding = await self.embedding_model.embed(content)
        
        await self.vector_store.insert({
            "id": str(uuid.uuid4()),
            "embedding": embedding,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        })
    
    async def retrieve(self, query: str, top_k: int = 5) -> str:
        """Retrieve relevant memories"""
        query_embedding = await self.embedding_model.embed(query)
        
        results = await self.vector_store.search(
            query_embedding,
            top_k=top_k
        )
        
        return "\n".join([
            f"- {r['content']}" for r in results
        ])
    
    async def retrieve_with_scores(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve with similarity scores"""
        query_embedding = await self.embedding_model.embed(query)
        
        return await self.vector_store.search(
            query_embedding,
            top_k=top_k
        )
```

### Episodic Memory

```python
class EpisodicMemory:
    """Memory of past agent experiences"""
    
    def __init__(self, storage):
        self.storage = storage
    
    async def store_episode(self, episode: Dict):
        """Store a complete episode"""
        await self.storage.insert({
            "id": str(uuid.uuid4()),
            "task": episode.get("task"),
            "actions": episode.get("actions", []),
            "outcome": episode.get("outcome"),
            "success": episode.get("success", False),
            "reflection": episode.get("reflection"),
            "timestamp": datetime.now().isoformat()
        })
    
    async def get_similar_episodes(self, task: str, top_k: int = 3) -> List[Dict]:
        """Find similar past episodes"""
        # Would use embeddings or keyword matching
        return await self.storage.query(
            f"task:{task}",
            limit=top_k
        )
    
    async def get_success_rate(self, task_type: str = None) -> float:
        """Calculate success rate"""
        # Query and calculate
        return 0.75  # Placeholder
```

-----

## Planning Systems

### Plan-and-Execute Agent

```python
class PlanExecuteAgent(BaseAgent):
    """Agent that plans before executing"""
    
    async def run(self, task: str) -> Dict:
        # Planning phase
        plan = await self.create_plan(task)
        
        # Execution phase
        results = []
        for step in plan["steps"]:
            result = await self.execute_step(step)
            results.append(result)
            
            # Check for plan deviations
            if not self.validate_step(result, step):
                # Replan if needed
                plan = await self.replan(task, plan, results)
        
        return self.format_result(results)
    
    async def create_plan(self, task: str) -> Dict:
        """Create initial plan"""
        prompt = f"""Create a step-by-step plan to accomplish this task:
Task: {task}

Format as:
Plan: [brief description]
Steps:
1. [first step]
2. [second step]
..."""

        response = await self.llm.chat([
            {"role": "system", "content": "You are a planning agent."},
            {"role": "user", "content": prompt}
        ])
        
        return self.parse_plan(response.content)
    
    async def execute_step(self, step: Dict) -> Dict:
        """Execute a single plan step"""
        # Execute using tools
        result = await self.think_and_act(step["description"])
        
        return {
            "step": step,
            "result": result,
            "success": self.evaluate_success(result, step["goal"])
        }
    
    def parse_plan(self, response: str) -> Dict:
        """Parse plan from LLM response"""
        lines = response.strip().split("\n")
        plan = {"description": "", "steps": []}
        
        for line in lines:
            if line.startswith("Plan:"):
                plan["description"] = line[5:].strip()
            elif line[0].isdigit() and ". " in line:
                step = line.split(". ", 1)[1].strip()
                plan["steps"].append({
                    "description": step,
                    "goal": step  # Simplified
                })
        
        return plan
```

### Tree of Thoughts

```python
class TreeOfThoughtsAgent:
    """Agent using Tree of Thoughts reasoning"""
    
    def __init__(self, llm, num_thoughts: int = 3, max_depth: int = 3):
        self.llm = llm
        self.num_thoughts = num_thoughts
        self.max_depth = max_depth
    
    async def solve(self, task: str) -> str:
        """Solve task using tree of thoughts"""
        root = ThoughtNode(task, None)
        
        # Generate initial thoughts
        await self.expand_node(root)
        
        # Search tree for best solution
        best = await self.search(root)
        
        return best.content
    
    async def expand_node(self, node: ThoughtNode):
        """Expand a node with multiple thoughts"""
        if node.depth >= self.max_depth:
            return
        
        # Generate multiple thoughts
        for _ in range(self.num_thoughts):
            thought = await self.generate_thought(node)
            child = ThoughtNode(thought, node)
            node.children.append(child)
            
            # Evaluate child
            child.score = await self.evaluate(child)
            
            # Expand if promising
            if child.score > 0.5:
                await self.expand_node(child)
    
    async def generate_thought(self, node: ThoughtNode) -> str:
        """Generate next thought"""
        context = node.get_path()
        
        prompt = f"""Given this reasoning chain:
{context}

Generate the next thought step:
Thought:"""
        
        response = await self.llm.chat([
            {"role": "user", "content": prompt}
        ])
        
        return response.content
    
    async def search(self, node: ThoughtNode) -> ThoughtNode:
        """Search for best solution"""
        if not node.children:
            return node
        
        # DFS with pruning
        best = node
        for child in node.children:
            candidate = await self.search(child)
            if candidate.score > best.score:
                best = candidate
        
        return best

class ThoughtNode:
    def __init__(self, content: str, parent):
        self.content = content
        self.parent = parent
        self.children: List[ThoughtNode] = []
        self.score = 0.0
        self.depth = 0 if parent is None else parent.depth + 1
    
    def get_path(self) -> str:
        """Get full reasoning path"""
        path = []
        node = self
        while node:
            path.append(node.content)
            node = node.parent
        return "\n".join(reversed(path))
```

-----

## Evaluation Frameworks

### Agent Evaluation Metrics

```python
from dataclasses import dataclass
from typing import List

@dataclass
class EvaluationResult:
    """Result of agent evaluation"""
    task: str
    success: bool
    steps_taken: int
    final_response: str
    expected_outcome: str
    metrics: Dict[str, float]

class AgentEvaluator:
    """Evaluates agent performance"""
    
    def __init__(self, metrics: List[str] = None):
        self.metrics = metrics or [
            "success_rate",
            "efficiency",
            "accuracy",
            "tool_usage",
            "error_rate"
        ]
    
    async def evaluate(
        self,
        agent: BaseAgent,
        test_cases: List[Dict]
    ) -> Dict:
        """Evaluate agent on test cases"""
        results = []
        
        for test in test_cases:
            result = await self.run_test(agent, test)
            results.append(result)
        
        # Aggregate metrics
        return self.aggregate_results(results)
    
    async def run_test(
        self,
        agent: BaseAgent,
        test: Dict
    ) -> EvaluationResult:
        """Run single test case"""
        response = await agent.run(test["task"])
        
        # Check success
        success = self.check_success(response, test.get("expected"))
        
        return EvaluationResult(
            task=test["task"],
            success=success,
            steps_taken=len(response.get("thoughts", [])),
            final_response=response.get("response", ""),
            expected_outcome=test.get("expected", ""),
            metrics=self.compute_metrics(response, test)
        )
    
    def compute_metrics(self, response: Dict, test: Dict) -> Dict:
        """Compute individual metrics"""
        return {
            "efficiency": 1.0 / (len(response.get("thoughts", [])) + 1),
            "tool_usage": len([t for t in response.get("actions", []) if t]),
        }
    
    def aggregate_results(self, results: List[EvaluationResult]) -> Dict:
        """Aggregate results into summary"""
        total = len(results)
        successes = sum(1 for r in results if r.success)
        
        return {
            "success_rate": successes / total,
            "total_tests": total,
            "avg_steps": sum(r.steps_taken for r in results) / total,
            "per_task": {r.task: r.success for r in results}
        }
```

### Benchmarking

```python
class AgentBenchmark:
    """Benchmark agent performance against baselines"""
    
    BENCHMARKS = {
        "hotpotqa": {"type": "retrieval", "metrics": ["accuracy"]},
        "math": {"type": "reasoning", "metrics": ["accuracy"]},
        "tooluse": {"type": "tool_use", "metrics": ["success_rate"]},
        "api_bank": {"type": "api_call", "metrics": ["accuracy"]}
    }
    
    async def run_benchmark(
        self,
        agent: BaseAgent,
        benchmark: str
    ) -> Dict:
        """Run specific benchmark"""
        if benchmark not in self.BENCHMARKS:
            raise ValueError(f"Unknown benchmark: {benchmark}")
        
        test_cases = self.load_benchmark(benchmark)
        evaluator = AgentEvaluator()
        
        results = await evaluator.evaluate(agent, test_cases)
        
        return {
            "benchmark": benchmark,
            **results
        }
```

-----

## Multi-Agent Systems

### Agent Collaboration

```python
class MultiAgentOrchestrator:
    """Orchestrates multiple specialized agents"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.task_queue: asyncio.Queue = asyncio.Queue()
    
    def register_agent(self, name: str, agent: BaseAgent, capabilities: List[str]):
        """Register an agent with capabilities"""
        self.agents[name] = {
            "agent": agent,
            "capabilities": capabilities,
            "busy": False
        }
    
    async def assign_task(self, task: str) -> Dict:
        """Assign task to best available agent"""
        # Analyze task requirements
        required = self.analyze_requirements(task)
        
        # Find suitable agent
        agent_info = self.select_agent(required)
        
        if not agent_info:
            return {"status": "no_agent", "task": task}
        
        # Execute task
        agent = agent_info["agent"]
        result = await agent.run(task)
        
        return {
            "status": "completed",
            "agent": agent_info["name"],
            "result": result
        }
    
    def analyze_requirements(self, task: str) -> List[str]:
        """Analyze task to determine requirements"""
        # Simplified - would use LLM
        keywords = {
            "search": ["search", "find", "look up"],
            "code": ["code", "implement", "program"],
            "write": ["write", "create", "draft"]
        }
        
        required = []
        for capability, patterns in keywords.items():
            if any(p in task.lower() for p in patterns):
                required.append(capability)
        
        return required
    
    def select_agent(self, requirements: List[str]) -> Optional[Dict]:
        """Select agent based on requirements"""
        for name, info in self.agents.items():
            caps = set(info["capabilities"])
            reqs = set(requirements)
            
            if reqs.issubset(caps) and not info["busy"]:
                info["busy"] = True
                return {"name": name, **info}
        
        return None
```

### Debate and Consensus

```python
class DebateOrchestrator:
    """Multi-agent debate system"""
    
    def __init__(self, num_agents: int = 3):
        self.agents = [BaseAgent(config) for _ in range(num_agents)]
        self.max_rounds = 3
    
    async def debate(self, topic: str) -> Dict:
        """Run debate on topic"""
        # Initial statements
        statements = []
        for agent in self.agents:
            statement = await agent.run(f"Provide your position on: {topic}")
            statements.append(statement)
        
        # Debate rounds
        for round in range(self.max_rounds):
            # Each agent responds to others
            responses = []
            for i, agent in enumerate(self.agents):
                other_statements = [s for j, s in enumerate(statements) if j != i]
                response = await agent.run(
                    f"Debate topic: {topic}\n\n"
                    f"Other positions:\n" + "\n".join(other_statements)
                )
                statements[i] = response
                responses.append(response)
        
        # Reach consensus or summarize
        consensus = await self.find_consensus(statements)
        
        return {
            "statements": statements,
            "consensus": consensus,
            "rounds": self.max_rounds
        }
```

-----

## Best Practices

1. **Start Simple** — Begin with basic agents before adding complexity.

2. **Tool Design Matters** — Design tools with clear, specific purposes and well-defined schemas.

3. **Handle Failures Gracefully** — Implement retry logic and fallback strategies.

4. **Monitor and Log** — Track agent decisions for debugging and improvement.

5. **Evaluate Continuously** — Benchmark agents on realistic test cases.

6. **Guardrails Are Essential** — Implement safety measures for autonomous actions.

7. **Memory Management** — Balance context retention with token efficiency.

8. **Plan for Scale** — Consider multi-agent architectures for complex tasks.
