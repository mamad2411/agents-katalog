---
name: "ptc"
description: "Implement prompt-to-code workflows for rapid prototyping and code generation"
---

# Programmatic Tool Calling (PTC)

## When to activate
User wants to reduce API token usage for tool-heavy workflows, mentions programmatic tool calling, or has a pattern where the same tool is called more than 3 times in a single inference pass.

## When NOT to use
- Tools with side effects that need human review between calls (write, delete, deploy)
- Tools requiring re-authentication per call or with per-call authorization prompts
- Single tool calls — PTC overhead is not worth it below ~3 calls
- Non-Python execution environments — PTC sandbox is Python only

## Instructions

### What PTC Does
Standard tool use: Claude calls one tool → result returned → Claude calls the next tool. Each round trip is one API inference pass.

With PTC: Claude writes Python orchestration code that calls multiple tools in a loop, executes in a sandbox, and only the final stdout enters the context. Three tools = 1 inference pass instead of 3.

**Measured token reduction: ~37% fewer tokens for multi-tool workflows.**

### Enabling PTC
Add `code_execution_20250825` as an allowed caller in your tool definition:
```python
tools = [
    {
        "name": "read_file",
        "description": "Read a file from the filesystem",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path to read"},
            },
            "required": ["path"],
        },
        "allowed_callers": ["code_execution_20250825"],  # Enable PTC for this tool
    }
]
```

When PTC is enabled, Claude can choose to write orchestration code instead of calling the tool directly.

### Execution Sandbox
- Python only
- No filesystem access by default (unless the tool itself provides it)
- Limited standard library — no network calls from sandbox code
- Tool results are returned as Python objects to the sandbox code
- Only stdout from the sandbox enters the conversation context

### When Claude Uses PTC Automatically
Claude selects PTC when it detects a pattern that benefits from batching:
- Reading N files and extracting a field from each
- Running the same transformation on a list of inputs
- Aggregating results from multiple tool calls before responding
- Any loop where a tool is called with different parameters each iteration

### When to Force PTC (Prompt Engineering)
If Claude is not using PTC for a pattern that clearly benefits from it, add to the system prompt:
```
When you need to call the same tool multiple times with different inputs, write Python orchestration code using code_execution_20250825 to batch the calls rather than calling the tool individually each time.
```

### Tool Design for PTC Compatibility
Tools used with PTC should:
- Accept simple, serializable inputs (strings, numbers, lists)
- Return clean, parseable output (prefer JSON over freeform text)
- Be idempotent (reads, lookups) rather than stateful (writes, mutations)
- Not require interactive confirmation

### Combining PTC with Prompt Caching
For maximum token efficiency: cache the tool definitions (which may be large) with `cache_control`, and enable PTC to reduce the number of round trips:
```python
tools = [
    # ... your tools ...
    {
        "name": "last_tool",
        "description": "...",
        "input_schema": {...},
        "allowed_callers": ["code_execution_20250825"],
        "cache_control": {"type": "ephemeral"},  # Cache all tools up to here
    }
]
```

### Limitations
- PTC cannot call tools that require human-in-the-loop approval mid-execution
- The sandbox has a timeout — very long-running loops may be cut off
- Tools that return binary data (images, files) are not suitable for PTC orchestration
- Debugging is harder — the code and intermediate results are not visible in the main context

## Example

Extracting function signatures from 20 source files without PTC: 20 `read_file` tool calls, 20 round trips, ~40,000 tokens of tool call + result overhead.

With PTC enabled on `read_file`:

Claude writes (internally, in sandbox):
```python
files = [
    "src/api/users.ts", "src/api/orders.ts", "src/api/products.ts",
    # ... 17 more
]
signatures = []
for f in files:
    content = read_file(path=f)
    # Extract export function lines
    sigs = [line.strip() for line in content.split("\n") if line.startswith("export function")]
    signatures.extend(sigs)
print("\n".join(signatures))
```

One inference pass. Only the extracted signatures (not full file contents) enter context. Token reduction: 37% on this workflow.

---
