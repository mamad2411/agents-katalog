---
name: agent-orchestration-langgraph
description: Build multi-agent systems with LangGraph — state management, conditional edges, parallel execution, human-in-the-loop
triggers: [LangGraph, multi-agent, agent orchestration, agent workflow, LangChain, state graph, agent coordination]
---

# SKILL: Agent Orchestration with LangGraph

## What is LangGraph?

**Graph-based orchestration for multi-agent AI systems.**

Unlike linear chains, LangGraph uses a directed graph where:
- **Nodes** = Agent actions (LLM calls, tool use, logic)
- **Edges** = Control flow (which node runs next)
- **State** = Shared data passed between nodes

## Core Architecture Patterns

### Pattern 1: Supervisor-Worker (Orchestrator)
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

# Shared state
class AgentState(TypedDict):
    messages: List[str]
    next_agent: str
    final_response: str

# Supervisor decides which worker runs next
def supervisor(state: AgentState) -> AgentState:
    """Analyzes task and routes to appropriate specialist"""
    task = state["messages"][-1]
    
    # Route based on task type
    if "code" in task.lower():
        return {"next_agent": "code_agent"}
    elif "research" in task.lower():
        return {"next_agent": "research_agent"}
    else:
        return {"next_agent": "general_agent"}

# Specialist workers
def code_agent(state: AgentState) -> AgentState:
    """Handles coding tasks"""
    response = llm.invoke(f"Write code for: {state['messages'][-1]}")
    return {"final_response": response}

def research_agent(state: AgentState) -> AgentState:
    """Handles research tasks"""
    response = llm.invoke(f"Research: {state['messages'][-1]}")
    return {"final_response": response}

# Build graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("supervisor", supervisor)
workflow.add_node("code_agent", code_agent)
workflow.add_node("research_agent", research_agent)

# Add conditional routing
workflow.add_conditional_edges(
    "supervisor",
    lambda state: state["next_agent"],  # Router function
    {
        "code_agent": "code_agent",
        "research_agent": "research_agent",
    }
)

# Set entry point
workflow.set_entry_point("supervisor")

# Compile
app = workflow.compile()

# Run
result = app.invoke({"messages": ["Write Python code to sort a list"]})
```

### Pattern 2: Scatter-Gather (Parallel Execution)
```python
from langgraph.types import Send

class State(TypedDict):
    topic: str
    sections: List[str]
    completed_sections: List[str]

def plan_report(state: State) -> State:
    """Create report outline"""
    sections = ["Introduction", "Methods", "Results", "Conclusion"]
    return {"sections": sections}

def write_section(state: State) -> State:
    """Each section written in parallel"""
    section = state["section"]  # Worker state
    content = llm.invoke(f"Write {section} for {state['topic']}")
    return {"completed_sections": [content]}

def orchestrator(state: State):
    """Send each section to parallel workers"""
    return [
        Send("write_section", {"section": s, "topic": state["topic"]})
        for s in state["sections"]
    ]

# Workers run in parallel, results aggregated
workflow = StateGraph(State)
workflow.add_node("plan", plan_report)
workflow.add_node("write_section", write_section)
workflow.add_conditional_edges("plan", orchestrator)
```

### Pattern 3: Human-in-the-Loop
```python
from langgraph.checkpoint.memory import MemorySaver

def agent_action(state: AgentState) -> AgentState:
    """Agent proposes action"""
    proposed_action = llm.invoke(state["messages"])
    return {
        "proposed_action": proposed_action,
        "awaiting_approval": True
    }

def should_continue(state: AgentState) -> str:
    """Check if human approval needed"""
    if state.get("awaiting_approval"):
        return "interrupt"  # Pause for human
    return "continue"

# Workflow with interrupts
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_action)
workflow.add_conditional_edges("agent", should_continue)

# Enable persistence (required for interrupts)
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# Run until interrupt
config = {"configurable": {"thread_id": "1"}}
result = app.invoke({"messages": ["Delete all users"]}, config)

# Human reviews proposed action
print(result["proposed_action"])

# Human approves or modifies
result["awaiting_approval"] = False
result = app.invoke(result, config)  # Resume
```

### Pattern 4: Loop with Termination Criteria
```python
def research_step(state: AgentState) -> AgentState:
    """Research iteration"""
    query = generate_search_query(state)
    results = search_tool(query)
    
    # Decide if more research needed
    is_sufficient = evaluate_completeness(results)
    
    return {
        "research_results": results,
        "continue_research": not is_sufficient,
        "iteration": state["iteration"] + 1
    }

def should_continue_research(state: AgentState) -> str:
    """Termination criteria"""
    if state["iteration"] >= 5:  # Max iterations
        return "end"
    if not state.get("continue_research"):  # Sufficient info
        return "end"
    return "research"  # Continue

workflow = StateGraph(AgentState)
workflow.add_node("research", research_step)
workflow.add_conditional_edges("research", should_continue_research, {
    "research": "research",  # Loop back
    "end": END
})
```

## State Management Best Practices

```python
from typing import Annotated
import operator

class AgentState(TypedDict):
    # Overwrite (default behavior)
    current_step: str
    
    # Append to list
    messages: Annotated[List[str], operator.add]
    
    # Merge dictionaries
    metadata: Annotated[dict, operator.or_]

# Usage
state1 = {"messages": ["hello"], "current_step": "start"}
state2 = {"messages": ["world"], "current_step": "process"}

# Result:
# messages: ["hello", "world"] (appended)
# current_step: "process" (overwritten)
```

## Observability & Debugging

```python
# Enable LangSmith tracing
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"

# Every agent action logged to LangSmith
# View traces at: smith.langchain.com
```

## Quality Checks
- [ ] State schema defined (TypedDict)
- [ ] Conditional edges have termination criteria
- [ ] Parallel execution coordinated (Send API)
- [ ] Human-in-the-loop for critical actions
- [ ] Persistence enabled (MemorySaver) for long-running agents
- [ ] Maximum iteration limits (prevent infinite loops)
- [ ] Tracing enabled (LangSmith)
- [ ] Error handling in all nodes
