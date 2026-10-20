---
name: "agent-supervisor"
description: "Build orchestrator agents that manage multi-agent workflows, enforce SLAs, handle escalations, and maintain overall task completion"
---

# Agent Supervisor Skill

## When to activate

- Building an orchestrator agent that spawns and manages multiple subagents
- Implementing timeout/retry/escalation logic for multi-agent workflows
- Enforcing resource limits (tokens, latency, cost) across a team of agents
- Handling task decomposition and work allocation among agents
- Implementing quality gates and validation between agent handoffs

## When NOT to use

- Single-agent workflows (no orchestration needed)
- Event-driven systems without centralized coordination
- Systems where agents are fully autonomous (no supervisor)

## Instructions

### Supervisor Responsibilities

The supervisor agent owns:

1. **Task planning:** Decompose user request into subtasks
2. **Agent delegation:** Assign subtasks to specific agents
3. **State management:** Maintain workflow state and progress
4. **Quality gates:** Validate agent outputs before proceeding
5. **Error handling:** Retry failed agents, escalate unsolvable problems
6. **Resource enforcement:** Track and enforce budgets (tokens, latency, cost)
7. **Result assembly:** Collect agent outputs and produce final result

### System Prompt Template

```
You are a supervisor agent. Your job is to manage a team of specialized agents
and ensure they complete a complex task.

Your team consists of:
- researcher: Gathers information from sources
- analyst: Synthesizes findings
- writer: Generates final report

Your workflow:
1. Break the user's request into subtasks
2. Delegate subtasks to agents in sequence
3. Validate each agent's output
4. If output is invalid, retry the agent or escalate
5. Combine outputs into final result

Rules:
- You do NOT do domain work yourself (research, analysis, writing)
- You ONLY delegate and coordinate
- You must provide agents with exactly what they need (no more, no less)
- You must validate agent outputs before proceeding
- You must track latency and tokens (budget: 5000 tokens, 30 minutes)
- If an agent fails 3 times, escalate to human

Task: {{user_request}}

Begin by decomposing the task into subtasks.
```

### Task Decomposition

```python
def decompose_task(user_request: str) -> list:
    """
    Use the supervisor agent to break a task into subtasks.
    Returns a list of subtasks with agent assignments.
    """
    import anthropic
    
    client = anthropic.Anthropic()
    
    response = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=2048,
        system=SUPERVISOR_SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Decompose this task:\n\n{user_request}"
        }]
    )
    
    # Parse response to extract subtasks
    # Response should be JSON like:
    # [
    #   {"subtask_id": "st_1", "description": "...", "agent": "researcher", "input": {...}},
    #   {"subtask_id": "st_2", "description": "...", "agent": "analyst", "input": {...}}
    # ]
    
    import json
    subtasks = json.loads(response.content[0].text)
    return subtasks
```

### Agent Delegation

```python
def delegate_to_agent(subtask: dict, agent_name: str) -> dict:
    """
    Delegate a subtask to a specific agent.
    Returns the agent's output.
    """
    # In Claude Code, spawn a subagent
    subagent_result = spawn_agent(
        agent=agent_name,
        input=subtask['input'],
        timeout_ms=subtask.get('timeout_ms', 300000)
    )
    
    return {
        'subtask_id': subtask['subtask_id'],
        'agent': agent_name,
        'status': subagent_result['status'],
        'output': subagent_result['output'],
        'tokens_used': subagent_result['tokens_used'],
        'latency_ms': subagent_result['latency_ms']
    }
```

### Quality Gate Validation

```python
def validate_agent_output(output: dict, expected_schema: dict) -> bool:
    """
    Validate that agent output matches expected schema.
    Returns True if valid, False otherwise.
    """
    import jsonschema
    
    try:
        jsonschema.validate(
            instance=output,
            schema=expected_schema
        )
        return True
    except jsonschema.ValidationError as e:
        print(f"Validation error: {e.message}")
        return False

def quality_gate_checkpoint(agent_output, expected_schema, subtask_id):
    """
    Checkpoint for validating agent output before proceeding.
    """
    if validate_agent_output(agent_output, expected_schema):
        print(f"✓ Subtask {subtask_id} passed quality gate")
        return True
    else:
        print(f"✗ Subtask {subtask_id} failed validation")
        return False
```

### Retry with Exponential Backoff

```python
import asyncio

async def delegate_with_retry(subtask, agent_name, max_retries=3):
    """
    Delegate with automatic retry on failure.
    Uses exponential backoff: 1s, 2s, 4s
    """
    for attempt in range(max_retries):
        try:
            result = delegate_to_agent(subtask, agent_name)
            
            if result['status'] == 'success':
                return result
            else:
                # Agent returned error
                print(f"Agent {agent_name} failed: {result.get('error')}")
                
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # exponential backoff
                    print(f"Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
        
        except Exception as e:
            print(f"Exception on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                raise
    
    # All retries exhausted
    raise RuntimeError(f"Agent {agent_name} failed after {max_retries} attempts")
```

### Resource Enforcement

```python
class ResourceBudget:
    def __init__(self, max_tokens=5000, max_latency_ms=300000, max_cost_cents=150):
        self.max_tokens = max_tokens
        self.max_latency_ms = max_latency_ms
        self.max_cost_cents = max_cost_cents
        
        self.tokens_used = 0
        self.latency_ms = 0
        self.cost_cents = 0
    
    def record_agent_call(self, agent_result):
        self.tokens_used += agent_result['tokens_used']['input'] + agent_result['tokens_used']['output']
        self.latency_ms += agent_result['latency_ms']
        self.cost_cents += agent_result.get('cost_cents', 0)
    
    def check_budget(self):
        if self.tokens_used > self.max_tokens:
            raise RuntimeError(f"Token budget exceeded: {self.tokens_used} / {self.max_tokens}")
        if self.latency_ms > self.max_latency_ms:
            raise RuntimeError(f"Latency budget exceeded: {self.latency_ms}ms / {self.max_latency_ms}ms")
        if self.cost_cents > self.max_cost_cents:
            raise RuntimeError(f"Cost budget exceeded: ${self.cost_cents / 100} / ${self.max_cost_cents / 100}")
    
    def get_budget_report(self):
        return {
            'tokens': f"{self.tokens_used} / {self.max_tokens}",
            'latency_ms': f"{self.latency_ms} / {self.max_latency_ms}",
            'cost_cents': f"{self.cost_cents} / {self.max_cost_cents}"
        }
```

### Orchestration Loop

```python
async def supervise_workflow(user_request: str):
    """
    Main orchestration loop for supervisor agent.
    """
    budget = ResourceBudget()
    
    # Step 1: Decompose task
    subtasks = decompose_task(user_request)
    print(f"Decomposed into {len(subtasks)} subtasks")
    
    results = {}
    
    # Step 2: Execute subtasks
    for subtask in subtasks:
        try:
            # Delegate with retry
            result = await delegate_with_retry(
                subtask,
                agent_name=subtask['agent'],
                max_retries=3
            )
            
            # Validate output
            if not quality_gate_checkpoint(result['output'], subtask.get('expected_schema'), subtask['subtask_id']):
                # Validation failed; retry the agent
                print(f"Retrying {subtask['subtask_id']} due to validation failure")
                result = await delegate_with_retry(subtask, subtask['agent'], max_retries=2)
            
            # Track resources
            budget.record_agent_call(result)
            budget.check_budget()
            
            results[subtask['subtask_id']] = result
            
        except Exception as e:
            # Escalate to human
            print(f"Escalating {subtask['subtask_id']}: {e}")
            results[subtask['subtask_id']] = {
                'status': 'escalated',
                'error': str(e)
            }
    
    # Step 3: Assemble final result
    final_result = assemble_results(results)
    
    print(f"Workflow completed. Budget report: {budget.get_budget_report()}")
    return final_result
```

## Example

```python
# Supervisor breaks down the request
user_request = "Write a report on Quantum Computing in 2026"

# Subtasks generated:
subtasks = [
    {
        "subtask_id": "st_1",
        "description": "Research quantum computing developments",
        "agent": "researcher",
        "input": {"topic": "Quantum Computing", "max_sources": 15},
        "timeout_ms": 120000,
        "expected_schema": {
            "type": "object",
            "properties": {
                "sources": {"type": "array"},
                "summary": {"type": "string"}
            },
            "required": ["sources", "summary"]
        }
    },
    {
        "subtask_id": "st_2",
        "description": "Analyze research findings",
        "agent": "analyst",
        "input": {"sources": "{{st_1.output.sources}}"},
        "timeout_ms": 120000
    },
    {
        "subtask_id": "st_3",
        "description": "Write report",
        "agent": "writer",
        "input": {"sources": "{{st_1.output.sources}}", "analysis": "{{st_2.output}}"},
        "timeout_ms": 60000
    }
]

# Supervisor delegates and validates
# If any subtask fails > 3 times, escalates
# If any subtask exceeds budget, halts workflow
# Returns final report
```

---
