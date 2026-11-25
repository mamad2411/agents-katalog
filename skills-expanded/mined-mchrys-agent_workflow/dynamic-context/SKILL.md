---
name: dynamic-context
description: System for building, manipulating, and sharing structured context between agents via XML injection. Enables typed variables, context blocks with inline XML, external prompt references, and result passing between runs.
version: 1.0.0
---

# Dynamic Context System

## Overview

The Dynamic Context System enables agents to:
- **Build structured context** with typed variables and nested objects
- **Pass data between agents** via context blocks with inline XML variables
- **Reference external prompts** with variable substitution
- **Share results from previous runs** in a structured format
- **Chain agents** by propagating context through the workflow

---

## Quick Start

```python
from agents import QueryContext, ContextBlock, PromptReference

# Create context with all features
ctx = QueryContext.create("You are an expert code reviewer.") \
    .add_content(code, "main.py") \
    .add_prompt("/prompts/security-review.md", language="python") \
    .add_previous_run_results({"issues_found": 3, "severity": "high"}) \
    .add_var("config", {"strict": True, "max_issues": 10})

# Use in query
result = await run_query("Review this code", context=ctx)
```

---

## Core Concepts

### 1. QueryContext
The central object holding all context elements. Chain builder methods to construct.

### 2. Context Types

| Type | Purpose | When to Use |
|------|---------|-------------|
| `DataSource` | Files/content to analyze | Input data for the agent |
| `SkillReference` | Instructions to follow | Behavioral guidelines |
| `PromptReference` | External prompt files | Reusable prompt templates |
| `ContextBlock` | Rich text + inline vars | Previous run results, dynamic context |
| `TypedVariable` | Standalone typed values | Configuration, parameters |
| `FunctionReference` | Available tools | Tool definitions |
| `MessageHistoryItem` | Conversation history | Context from prior messages |

---

## 📚 Reference Documentation

Load these files for detailed information:

### Class References
- [📋 Classes & Methods](./reference/classes.md) - Complete API for all context types
- [📐 XML Schema](./reference/xml-schema.md) - Generated XML structure and examples
- [🔗 Agent Integration](./reference/integration.md) - How to integrate with agents

### Usage Patterns
- [🔄 Agent Chaining](./patterns/agent-chain.md) - Pass context between agents
- [📤 Context Propagation](./patterns/context-propagation.md) - Share context across queries
- [📊 Result Passing](./patterns/result-passing.md) - Pass results from previous runs

### Examples
- [examples/basic_context.py](./examples/basic_context.py) - Basic context building
- [examples/agent_handoff.py](./examples/agent_handoff.py) - Agent-to-agent handoff
- [examples/previous_run.py](./examples/previous_run.py) - Using previous run results
- [examples/multi_agent_chain.py](./examples/multi_agent_chain.py) - Multi-agent workflow

### Scripts
- [scripts/validate_context.py](./scripts/validate_context.py) - Validate context structure

---

## Building Context

### Adding Data Sources

```python
ctx.add_source("src/main.py")                    # File path
ctx.add_sources(["a.py", "b.py", "c.py"])        # Multiple files
ctx.add_content("print('hello')", name="script") # Raw content
```

### Adding Skills

```python
ctx.add_skill("/skills/review.md", priority=5)
ctx.add_inline_skill("focus", "Check for SQL injection", priority=10)
```

### Adding Prompts

```python
# From file with variable substitution
ctx.add_prompt("/prompts/review.md", language="python", focus="security")

# Inline prompt
ctx.add_inline_prompt(
    "Review {language} code for {focus} issues",
    language="python", 
    focus="memory leaks"
)
```

### Adding Context Blocks (Rich Text with Inline Variables)

This is the key feature for passing data between runs/agents:

```python
# Template with inline variables
ctx.add_context(
    "Previous analysis found {count} issues with severity {severity}",
    name="previous_analysis",
    inline_vars={"count": 5, "severity": "high"}
)

# From previous run results
ctx.add_previous_run_results({
    "total_files": 150,
    "issues": ["XSS", "CSRF"],
    "metrics": {"coverage": 0.95}
})

# Manual block building
block = ContextBlock.create("analysis") \
    .add_text("Found ") \
    .add_inline_var("count", 42) \
    .add_text(" vulnerabilities")
ctx.add_context_block(block)
```

### Adding Typed Variables

```python
ctx.add_var("count", 42)                         # Auto-detect type
ctx.add_var("config", {"nested": {"value": 1}})  # Nested objects
ctx.add_vars(a=1, b=2, c=3)                      # Multiple at once
```

---

## Agent Integration

### Attaching Context to a Query

```python
from agents import run_query, QueryContext

ctx = QueryContext.create("You are helpful.") \
    .add_var("user_preference", "concise")

result = await run_query("Explain quantum computing", context=ctx)
```

### Passing Context Between Agents

```python
# Agent 1: Analyze
analysis_ctx = QueryContext.create("Analyze this code") \
    .add_content(code, "main.py")

result1 = await run_query("Find all issues", context=analysis_ctx)

# Agent 2: Fix (receives results from Agent 1)
fix_ctx = QueryContext.create("Fix the issues found") \
    .add_content(code, "main.py") \
    .add_previous_run_results({
        "issues": result1.parsed_issues,
        "severity": result1.max_severity
    })

result2 = await run_query("Fix these issues", context=fix_ctx)
```

### Using QueryTaskManager for Parallel Agents

```python
from agents import QueryTaskManager

manager = QueryTaskManager(base_context=shared_ctx)

manager.add_task("Review for security", sources=["auth.py"])
manager.add_task("Review for performance", sources=["db.py"])
manager.add_task("Review for style", sources=["utils.py"])

results = await manager.execute_all(max_concurrency=3)
```

---

## XML Output Structure

The context is injected into the system prompt as structured XML:

```xml
<injected_context>
  <data_sources>
    <source name="main.py" type="file">...</source>
  </data_sources>
  
  <skills>
    <skill name="security" priority="10">Check for vulnerabilities</skill>
  </skills>
  
  <prompts>
    <prompt path="/prompts/review.md" name="review">
      [content with variables substituted]
    </prompt>
  </prompts>
  
  <context name="previous_run">
    Found <var type="int" name="count">5</var> issues
  </context>
  
  <variables>
    <var name="config" type="object">
      <property name="strict" type="bool">true</property>
    </var>
  </variables>
</injected_context>
```

---

## Best Practices

1. **Use context blocks for previous run results** - Inline variables preserve type information
2. **Set skill priorities** - Higher priority skills are listed first
3. **Use prompts for reusable templates** - Variable substitution keeps prompts DRY
4. **Chain contexts for multi-agent workflows** - Each agent can add to/modify context
5. **Keep context focused** - Only include relevant information for the task

---

## See Also

- [📋 Full Class Reference](./reference/classes.md)
- [📐 XML Schema Details](./reference/xml-schema.md)
- [🔗 Agent Integration Guide](./reference/integration.md)
