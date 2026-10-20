---
name: mcp-advanced-tool-patterns
version: "1.0"
description: >
  For long-running operations, stream results incrementally with progress reporting.
  PROACTIVELY activate for: (1) streaming tool results, (2) tool orchestration, (3) cancellation and timeout handling.
  Triggers: "streaming", "tool orchestration", "progress reporting"
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# MCP Advanced Tool Patterns Skill

## Metadata (Tier 1)

**Keywords**: streaming, progress, cancellation, tool orchestration, async patterns

**File Patterns**: **/tools/*.py, **/handlers.py

**Modes**: backend_python

---

## Instructions (Tier 2)

### Streaming Tool Results

For long-running operations, stream results incrementally:

```python
from typing import AsyncIterator
from pydantic import BaseModel, ConfigDict

class StreamChunk(BaseModel):
    model_config = ConfigDict(strict=True)

    content: str
    progress: float  # 0.0 to 1.0
    is_final: bool

async def streaming_search_tool(query: str) -> AsyncIterator[StreamChunk]:
    """Stream search results as they're found."""
    results = []
    total_files = await count_searchable_files()

    async for file_idx, match in enumerate_matches(query):
        results.append(match)
        progress = (file_idx + 1) / total_files

        yield StreamChunk(
            content=format_match(match),
            progress=progress,
            is_final=False
        )

    # Final chunk with summary
    yield StreamChunk(
        content=f"Found {len(results)} matches",
        progress=1.0,
        is_final=True
    )

# Integration with MCP server
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "streaming_search":
        input_data = SearchInput(**arguments)

        # Collect stream chunks
        chunks = []
        async for chunk in streaming_search_tool(input_data.query):
            chunks.append(chunk.model_dump())

        return {"chunks": chunks}
```

### Progress Reporting

```python
from datetime import datetime

class ProgressUpdate(BaseModel):
    model_config = ConfigDict(strict=True)

    stage: str
    current: int
    total: int
    eta_seconds: float | None = None
    timestamp: datetime

async def long_running_tool(input_data: ToolInput):
    """Tool with progress updates."""
    stages = ["indexing", "searching", "ranking", "formatting"]
    results = []

    for stage_idx, stage in enumerate(stages):
        update = ProgressUpdate(
            stage=stage,
            current=stage_idx + 1,
            total=len(stages),
            eta_seconds=estimate_remaining_time(stage_idx, len(stages)),
            timestamp=datetime.utcnow()
        )

        # Emit progress (implementation depends on MCP version)
        await emit_progress(update)

        # Perform stage work
        stage_result = await execute_stage(stage, input_data)
        results.append(stage_result)

    return {"results": results}
```

### Tool Orchestration (Multi-Tool Workflows)

```python
from typing import AsyncIterator
import asyncio

class ToolOrchestrator:
    """Coordinate multiple tool executions."""

    def __init__(self, server):
        self.server = server

    async def execute_workflow(
        self,
        workflow: list[dict]
    ) -> list[dict]:
        """Execute tools in dependency order."""
        results = {}

        for step in workflow:
            tool_name = step["tool"]
            arguments = step["arguments"]

            # Resolve dependencies from previous results
            resolved_args = self._resolve_arguments(arguments, results)

            # Execute tool
            result = await self.server.call_tool(tool_name, resolved_args)
            results[step["id"]] = result

        return list(results.values())

    def _resolve_arguments(
        self,
        arguments: dict,
        previous_results: dict
    ) -> dict:
        """Replace placeholders with previous results."""
        resolved = {}
        for key, value in arguments.items():
            if isinstance(value, str) and value.startswith("$"):
                # Reference to previous result
                ref_id = value[1:]
                resolved[key] = previous_results.get(ref_id)
            else:
                resolved[key] = value
        return resolved

# Usage
orchestrator = ToolOrchestrator(server)

workflow = [
    {
        "id": "search_step",
        "tool": "search_code",
        "arguments": {"query": "async def"}
    },
    {
        "id": "analyze_step",
        "tool": "analyze_complexity",
        "arguments": {"files": "$search_step"}  # Reference previous result
    }
]

results = await orchestrator.execute_workflow(workflow)
```

### Concurrent Tool Execution

```python
async def execute_parallel_tools(
    tool_requests: list[tuple[str, dict]]
) -> list[dict]:
    """Execute multiple tools concurrently using TaskGroup."""

    async with asyncio.TaskGroup() as tg:
        tasks = []
        for tool_name, arguments in tool_requests:
            task = tg.create_task(
                call_tool(tool_name, arguments)
            )
            tasks.append(task)

    # Collect results
    return [task.result() for task in tasks]

# Usage
results = await execute_parallel_tools([
    ("search_code", {"query": "TODO"}),
    ("search_code", {"query": "FIXME"}),
    ("search_code", {"query": "HACK"})
])
```

### Cancellation and Timeout

```python
import asyncio

class CancellableToolExecution:
    """Tool execution with cancellation support."""

    def __init__(self, timeout_seconds: float = 30.0):
        self.timeout = timeout_seconds
        self._cancelled = False

    async def execute(
        self,
        tool_func,
        *args,
        **kwargs
    ) -> dict | None:
        """Execute tool with timeout and cancellation."""
        try:
            result = await asyncio.wait_for(
                tool_func(*args, **kwargs),
                timeout=self.timeout
            )
            return result

        except asyncio.TimeoutError:
            self._cancelled = True
            raise McpError(
                code=-32000,
                message=f"Tool execution timeout ({self.timeout}s)"
            )

        except asyncio.CancelledError:
            self._cancelled = True
            raise McpError(
                code=-32001,
                message="Tool execution cancelled"
            )

# Usage
executor = CancellableToolExecution(timeout_seconds=10.0)
result = await executor.execute(
    slow_search_tool,
    query="complex pattern"
)
```

### Stateful Tools (Session Management)

```python
from typing import Dict
import uuid

class ToolSession:
    """Maintain state across tool calls."""

    def __init__(self):
        self.sessions: Dict[str, dict] = {}

    def create_session(self) -> str:
        """Create new session and return ID."""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "created_at": datetime.utcnow(),
            "data": {}
        }
        return session_id

    def get_session(self, session_id: str) -> dict:
        """Retrieve session data."""
        if session_id not in self.sessions:
            raise ValueError(f"Invalid session: {session_id}")
        return self.sessions[session_id]["data"]

    def update_session(self, session_id: str, data: dict):
        """Update session data."""
        session = self.get_session(session_id)
        session.update(data)

# Global session manager
session_manager = ToolSession()

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "start_analysis":
        # Create session for multi-step analysis
        session_id = session_manager.create_session()
        return {"session_id": session_id}

    elif name == "continue_analysis":
        session_id = arguments["session_id"]
        session_data = session_manager.get_session(session_id)

        # Use previous state
        previous_results = session_data.get("results", [])
        new_result = await analyze_next_step(previous_results)

        # Update state
        session_manager.update_session(
            session_id,
            {"results": previous_results + [new_result]}
        )

        return {"result": new_result}
```

### Batch Processing

```python
class BatchProcessor:
    """Process items in optimized batches."""

    def __init__(self, batch_size: int = 10):
        self.batch_size = batch_size

    async def process_batch(
        self,
        items: list,
        process_func
    ) -> list:
        """Process items in parallel batches."""
        results = []

        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]

            # Process batch concurrently
            async with asyncio.TaskGroup() as tg:
                tasks = [
                    tg.create_task(process_func(item))
                    for item in batch
                ]

            batch_results = [task.result() for task in tasks]
            results.extend(batch_results)

        return results

# Usage
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "batch_analyze":
        input_data = BatchAnalyzeInput(**arguments)

        processor = BatchProcessor(batch_size=10)
        results = await processor.process_batch(
            input_data.files,
            analyze_file
        )

        return {"results": results}
```

### Retry Logic with Exponential Backoff

```python
import asyncio

async def retry_with_backoff(
    func,
    max_retries: int = 3,
    base_delay: float = 1.0
):
    """Retry function with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return await func()

        except Exception as e:
            if attempt == max_retries - 1:
                # Last attempt failed
                raise

            # Exponential backoff
            delay = base_delay * (2 ** attempt)
            await asyncio.sleep(delay)

# Usage
async def unreliable_api_call():
    """API call that might fail."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        response.raise_for_status()
        return response.json()

result = await retry_with_backoff(
    unreliable_api_call,
    max_retries=3,
    base_delay=1.0
)
```

### Anti-Patterns

❌ **Blocking in Async Tools**
```python
# WRONG
async def tool():
    result = requests.get(url)  # Blocking!
```

❌ **Using asyncio.gather() (Python 3.13)**
```python
# WRONG
results = await asyncio.gather(task1(), task2())
```

❌ **No Timeout on External Calls**
```python
# WRONG - can hang forever
async def tool():
    result = await external_api_call()  # No timeout!
```

❌ **Mutable Global State Without Locks**
```python
# WRONG - race condition
global_cache = {}  # Multiple tools modifying without lock

async def tool():
    global_cache[key] = value  # Race condition!
```

---

## Resources (Tier 3)

**Asyncio TaskGroup**: https://docs.python.org/3.13/library/asyncio-task.html#task-groups
**Asyncio Timeouts**: https://docs.python.org/3.13/library/asyncio-task.html#timeouts
**httpx Async Client**: https://www.python-httpx.org/async/
