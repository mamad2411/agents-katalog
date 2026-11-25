# LangGraph Tools Development Rules for Python

## Project Overview
This project focuses on building LangGraph tools for Python. LangGraph is a framework for creating stateful, multi-actor applications with Large Language Models (LLMs) using graph-based workflows.

## Core Principles

### 1. State Management
- Always use TypedDict for state definitions to ensure type safety
- Include proper type annotations with Annotated types for complex fields
- Use `add_messages` from langgraph.graph.message for message handling
- State must be serializable and immutable where possible
- Initialize all state fields properly to avoid KeyError exceptions

```python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class MyState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    pending_tools: list[dict[str, Any]]
    results: dict[str, Any]
    errors: dict[str, str]
```

### 2. Tool Implementation
- Use the @tool decorator from langchain_core.tools
- Always include proper docstrings with Args and Returns sections
- Implement comprehensive error handling with try-catch blocks
- Return consistent types (prefer strings for tool outputs)
- Use async/await for tools that involve I/O operations

```python
from langchain_core.tools import tool

@tool
async def my_tool(query: str) -> str:
    """Tool description.
    
    Args:
        query: Input query string
        
    Returns:
        str: Formatted result string
        
    Raises:
        ValueError: If query is invalid
    """
    try:
        # Tool logic here
        result = process_query(query)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e!s}"
```

### 3. Graph Construction
- Use StateGraph from langgraph.graph for graph construction
- Define clear entry and exit points
- Use conditional edges for branching logic
- Always compile graphs with appropriate checkpointers for persistence
- Set proper interrupt points for human-in-the-loop scenarios

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

workflow = StateGraph(MyState)
workflow.add_node("node_name", node_function)
workflow.add_edge(START, "node_name")
workflow.add_edge("node_name", END)

# Compile with checkpointer
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
```

### 4. Node Functions
- Node functions must accept state as first parameter
- Return dictionaries that will be merged into state
- Include proper error handling and logging
- Keep nodes focused on single responsibilities
- Use descriptive function and parameter names

```python
def process_node(state: MyState) -> dict:
    """Process node implementation.
    
    Args:
        state: Current graph state
        
    Returns:
        dict: Updates to merge into state
    """
    try:
        # Node logic
        result = perform_processing(state)
        return {"results": result}
    except Exception as e:
        return {"errors": {"process_node": str(e)}}
```

## Best Practices

### Error Handling
- Implement graceful error handling at every level
- Use specific exception types where appropriate
- Return error messages in consistent format
- Log errors for debugging purposes
- Never let unhandled exceptions crash the graph

### Performance Optimization
- Use async/await for I/O bound operations
- Implement parallel tool execution using asyncio.gather
- Consider message pruning for long conversations
- Use lazy loading for expensive resources
- Monitor execution time and memory usage

### Testing
- Create mock tools for testing
- Implement state validation functions
- Test different scenarios (success, error, edge cases)
- Use pytest-asyncio for async testing
- Validate state transitions and graph flow

### Message Management
- Use proper message types (HumanMessage, AIMessage, ToolMessage)
- Implement message filtering and pruning strategies
- Handle message timestamps for time-based operations
- Consider conversation summarization for long contexts

### Configuration Management
- Use environment variables for API keys and configuration
- Implement configuration validation
- Support different environments (dev, staging, prod)
- Use Pydantic for configuration models where appropriate

## Code Structure

### File Organization
```
project/
├── tools/
│   ├── __init__.py
│   ├── search_tools.py
│   ├── analysis_tools.py
│   └── utility_tools.py
├── graphs/
│   ├── __init__.py
│   ├── main_graph.py
│   └── subgraphs/
├── state/
│   ├── __init__.py
│   └── definitions.py
├── nodes/
│   ├── __init__.py
│   ├── processing_nodes.py
│   └── utility_nodes.py
├── tests/
└── config/
```

### Import Conventions
```python
# Standard library
import asyncio
import uuid
from datetime import datetime
from typing import Annotated, Any, Dict, List, TypedDict

# Third-party
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
```

## Security Considerations
- Sanitize all user inputs
- Validate tool parameters before execution
- Use secure credential management
- Implement rate limiting for API calls
- Avoid exposing sensitive information in logs

## Debugging and Monitoring
- Add comprehensive logging with appropriate levels
- Include execution timing information
- Track state changes throughout graph execution
- Implement health checks for external dependencies
- Use structured logging for better analysis

## Documentation Requirements
- Document all public functions and classes
- Include usage examples in docstrings
- Maintain README with setup and usage instructions
- Document graph flow and decision points
- Keep API documentation up to date

## Common Patterns

### ToolNode Usage
```python
from langgraph.prebuilt import ToolNode
from uuid import uuid4

# Proper ToolNode message structure
tool_message = AIMessage(
    content="",  # Must be empty string
    tool_calls=[{
        "name": tool_name,
        "args": {"query": message},
        "id": str(uuid4()),
        "type": "tool_call",
    }]
)

tool_node = ToolNode(tools)
result = tool_node.invoke({"messages": [tool_message]})
```

### Parallel Execution
```python
async def parallel_executor(state: MyState) -> MyState:
    if not state["pending_tools"]:
        return state
    
    tasks = [execute_tool(tool_call) for tool_call in state["pending_tools"]]
    results = await asyncio.gather(*tasks)
    
    # Process results
    return updated_state
```

### Human-in-the-Loop
```python
# Compile with interrupt points
app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["human_review"]
)

# Handle interrupts
config = {"configurable": {"thread_id": "session_1"}}
result = app.invoke(input_data, config=config)

# Resume after human input
app.invoke({"human_feedback": "approved"}, config=config)
```

## Dependencies
- langgraph
- langchain-core
- langchain-community (if using community tools)
- pydantic (for configuration)
- pytest-asyncio (for testing)
- python-dotenv (for environment variables)

## Version Compatibility
- Python 3.9+
- LangGraph 0.2.0+
- LangChain 0.3.0+

Follow these rules consistently to ensure robust, maintainable, and scalable LangGraph applications.