---
name: autonomous-agent-harness
description: Building autonomous AI agent workflows with bounded autonomy, guardrails, tool calling, self-correction, escalation patterns, safety constraints, output validation, and sandboxing.
origin: AI Dev Kit
disable-model-invocation: false
---

# Autonomous Agent Harness

Patterns for building autonomous AI agent systems: bounded autonomy loops, tool-use orchestration, self-correction, escalation to human-in-the-loop, safety guardrails, output validation, and sandboxing. This skill covers architecture, execution loops, and production hardening.

## When to Use

- Designing multi-step autonomous agent workflows
- Building tool-calling agent architectures (function calling, ReAct, Plan-and-Execute)
- Implementing bounded autonomy with safety guardrails
- Creating self-correcting agent loops with quality gates
- Setting up escalation patterns (agent → human handoff)
- Sandboxing agent actions before production execution
- Validating agent outputs against schemas and constraints

## Core Concepts

### 1. Bounded Autonomy Architecture

Autonomous agents operate within constrained boundaries. The architecture separates **planning**, **execution**, and **validation** into distinct phases with explicit guardrails.

```
┌─────────────────────────────────────────────────────┐
│                  ORCHESTRATOR                        │
│  ┌──────────┐    ┌──────────┐    ┌───────────────┐  │
│  │ PLANNER  │───▶│ EXECUTOR │───▶│  VALIDATOR    │  │
│  │          │    │          │    │               │  │
│  │ - Decompose│  │ - Tool   │    │ - Schema      │  │
│  │   task     │  │   calls  │    │   check       │  │
│  │ - Set      │  │ - Sub-   │    │ - Constraint  │  │
│  │   bounds   │  │   tasks  │    │   validation  │  │
│  │ - Budget   │  │ - Retry  │    │ - Quality     │  │
│  │   tokens   │  │   logic  │    │   gate        │  │
│  └──────────┘    └──────────┘    └───────┬───────┘  │
│                                          │          │
│                                    ┌─────▼───────┐  │
│                                    │ ESCALATION  │  │
│                                    │ - Human     │  │
│                                    │   handoff   │  │
│                                    │ - Fallback  │  │
│                                    │   policy    │  │
│                                    └─────────────┘  │
└─────────────────────────────────────────────────────┘
         │
         ▼
  ┌──────────────┐     ┌──────────────┐
  │  TOOL SANDBOX │     │ STATE STORE  │
  │ - Read-only   │     │ - Step log   │
  │   by default  │     │ - Token      │
  │ - Allow-list  │     │   budget     │
  │   mutations   │     │ - Results    │
  └──────────────┘     └──────────────┘
```

### 2. Agent Execution Loop

The core loop: plan → execute → validate → (retry or complete). Each iteration is bounded by token budgets, step limits, and safety constraints.

**Python — Agent Loop with Guardrails:**

```python
from dataclasses import dataclass, field
from typing import Any, Callable
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


class AgentState(Enum):
    PLANNING = "planning"
    EXECUTING = "executing"
    VALIDATING = "validating"
    COMPLETE = "complete"
    ESCALATED = "escalated"
    FAILED = "failed"


@dataclass
class AgentContext:
    """Mutable state carried through the agent loop."""
    task: str
    plan: list[str] = field(default_factory=list)
    results: list[dict] = field(default_factory=list)
    step_count: int = 0
    token_budget: int = 8000  # Max tokens per loop
    max_steps: int = 10       # Hard step limit
    state: AgentState = AgentState.PLANNING
    error: str | None = None


@dataclass
class Guardrail:
    """A constraint checked after each step."""
    name: str
    check: Callable[[AgentContext], bool]
    action_on_violation: str  # "halt", "retry", "escalate"


def create_file_write_guardrail() -> Guardrail:
    """Prevents agent from writing to sensitive paths."""
    def check(ctx: AgentContext) -> bool:
        for result in ctx.results:
            if result.get("action") == "write_file":
                path = result.get("path", "")
                # Block writes to config, secrets, or system files
                blocked_prefixes = ("/etc/", ".env", "secrets/", "config/production")
                if any(path.startswith(p) for p in blocked_prefixes):
                    return False
        return True
    return Guardrail(
        name="no-sensitive-file-writes",
        check=check,
        action_on_violation="halt"
    )


def agent_loop(
    context: AgentContext,
    tools: dict[str, Callable],
    guardrails: list[Guardrail],
    planner_fn: Callable,
    executor_fn: Callable,
    validator_fn: Callable,
) -> AgentContext:
    """Main autonomous agent loop with bounded execution."""

    context.state = AgentState.PLANNING
    context.plan = planner_fn(context.task)
    logger.info("Plan: %s", context.plan)

    while context.state not in (AgentState.COMPLETE, AgentState.FAILED, AgentState.ESCALATED):
        # Token budget check
        estimated_tokens = estimate_tokens(context)
        if estimated_tokens > context.token_budget:
            logger.warning("Token budget exceeded (%d > %d), escalating", 
                          estimated_tokens, context.token_budget)
            context.state = AgentState.ESCALATED
            context.error = f"Token budget exceeded: {estimated_tokens}"
            break

        # Step limit check
        if context.step_count >= context.max_steps:
            logger.warning("Max steps reached (%d), escalating", context.step_count)
            context.state = AgentState.ESCALATED
            context.error = f"Max steps reached: {context.step_count}"
            break

        # Execute next step
        context.state = AgentState.EXECUTING
        try:
            step_result = executor_fn(context.plan[context.step_count], tools, context)
            context.results.append(step_result)
            context.step_count += 1
        except Exception as e:
            logger.error("Step %d failed: %s", context.step_count, e)
            context.error = str(e)
            context.state = AgentState.FAILED
            break

        # Validate results
        context.state = AgentState.VALIDATING
        validation = validator_fn(step_result)
        if not validation["valid"]:
            if validation.get("action") == "retry" and context.step_count < context.max_steps:
                logger.info("Retrying step %d: %s", context.step_count, validation["reason"])
                continue  # Re-execute current step
            elif validation.get("action") == "escalate":
                context.state = AgentState.ESCALATED
                context.error = f"Validation failed: {validation['reason']}"
                break
            else:
                context.state = AgentState.FAILED
                context.error = f"Validation failed: {validation['reason']}"
                break

        # Check guardrails
        for guardrail in guardrails:
            if not guardrail.check(context):
                logger.critical("Guardrail violated: %s", guardrail.name)
                if guardrail.action_on_violation == "halt":
                    context.state = AgentState.FAILED
                    context.error = f"Guardrail violation: {guardrail.name}"
                    break
                elif guardrail.action_on_violation == "escalate":
                    context.state = AgentState.ESCALATED
                    context.error = f"Guardrail escalation: {guardrail.name}"
                    break

    if context.state == AgentState.COMPLETE:
        logger.info("Agent completed in %d steps", context.step_count)

    return context


def estimate_tokens(context: AgentContext) -> int:
    """Rough token estimation (4 chars ≈ 1 token for English text)."""
    total = len(json.dumps(context.results)) + len(context.task)
    for step in context.plan:
        total += len(step)
    return total // 4
```

### 3. Tool-Calling Pattern

Agents interact with the world through an allow-list of tools. Each tool has explicit permissions, input schemas, and output validation.

**TypeScript — Tool Registry with Schema Validation:**

```typescript
import { z } from "zod";

interface Tool<TInput, TOutput> {
  name: string;
  description: string;
  inputSchema: z.ZodType<TInput>;
  outputSchema: z.ZodType<TOutput>;
  execute: (input: TInput) => Promise<TOutput>;
  permissions: string[];  // e.g., ["file:read", "api:github"]
}

class ToolRegistry {
  private tools: Map<string, Tool<any, any>> = new Map();

  register<TIn, TOut>(tool: Tool<TIn, TOut>): void {
    this.tools.set(tool.name, tool);
  }

  async invoke(toolName: string, rawInput: unknown): Promise<unknown> {
    const tool = this.tools.get(toolName);
    if (!tool) {
      throw new Error(`Unknown tool: ${toolName}`);
    }

    // Validate input against schema
    const input = tool.inputSchema.parse(rawInput);

    // Execute with timeout
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30_000);

    try {
      const result = await tool.execute(input);
      // Validate output against schema
      return tool.outputSchema.parse(result);
    } finally {
      clearTimeout(timeout);
    }
  }

  getAllowList(): string[] {
    return Array.from(this.tools.keys());
  }
}

// Example: Safe file read tool
const fileReadTool: Tool<{ path: string; maxLines?: number }, { content: string; lines: number }> = {
  name: "file_read",
  description: "Read contents of a file (read-only, no mutations)",
  inputSchema: z.object({
    path: z.string().min(1).max(500),
    maxLines: z.number().int().positive().default(1000),
  }),
  outputSchema: z.object({
    content: z.string(),
    lines: z.number().int(),
  }),
  permissions: ["file:read"],
  execute: async ({ path, maxLines }) => {
    // Block sensitive paths
    const blockedPatterns = [".env", "secrets/", "/etc/", "id_rsa", ".pem"];
    if (blockedPatterns.some(p => path.includes(p))) {
      throw new Error(`Access denied: cannot read ${path}`);
    }

    const content = await fs.readFile(path, "utf-8");
    const lines = content.split("\n").slice(0, maxLines);
    return { content: lines.join("\n"), lines: lines.length };
  },
};

// Example: Safe search tool
const grepTool: Tool<{ pattern: string; path: string }, { matches: Array<{ file: string; line: number; content: string }> }> = {
  name: "grep_search",
  description: "Search for patterns in files",
  inputSchema: z.object({
    pattern: z.string().min(1).max(200),
    path: z.string().min(1).max(500),
  }),
  outputSchema: z.object({
    matches: z.array(z.object({
      file: z.string(),
      line: z.number(),
      content: z.string(),
    })),
  }),
  permissions: ["file:read", "search"],
  execute: async ({ pattern, path }) => {
    // Use safe grep (no shell injection)
    const matches: Array<{ file: string; line: number; content: string }> = [];
    // ... grep implementation
    return { matches };
  },
};
```

### 4. Self-Correction Loop

When validation fails, the agent attempts self-correction before escalating. This requires feeding the error back to the agent with explicit retry instructions.

```python
def self_correction_loop(
    context: AgentContext,
    tools: dict,
    max_retries: int = 3,
) -> AgentContext:
    """Attempt self-correction on validation failures before escalating."""

    for attempt in range(max_retries):
        context = agent_loop(
            context=context,
            tools=tools,
            guardrails=[create_file_write_guardrail()],
            planner_fn=create_planner,
            executor_fn=create_executor(tools),
            validator_fn=create_validator(),
        )

        if context.state == AgentState.COMPLETE:
            return context

        if context.state == AgentState.FAILED and attempt < max_retries - 1:
            # Feed error back for self-correction
            logger.info("Self-correction attempt %d/%d: %s", 
                       attempt + 1, max_retries, context.error)
            context.task += f"\n\nPREVIOUS ERROR: {context.error}. Fix this and retry."
            context.error = None
            context.results.clear()
            context.step_count = 0
            context.state = AgentState.PLANNING
            continue

        # Failed after all retries — escalate
        context.state = AgentState.ESCALATED
        context.error = f"Failed after {max_retries} self-correction attempts: {context.error}"
        break

    return context
```

### 5. Escalation Patterns

When the agent exceeds bounds or cannot resolve an issue, escalate to a human or fallback policy.

```python
class EscalationPolicy:
    """Defines when and how to escalate from agent to human."""

    def __init__(
        self,
        max_token_budget: int = 16000,
        max_steps: int = 20,
        max_retries: int = 3,
        blocked_actions: list[str] | None = None,
    ):
        self.max_token_budget = max_token_budget
        self.max_steps = max_steps
        self.max_retries = max_retries
        self.blocked_actions = blocked_actions or []

    def should_escalate(self, context: AgentContext) -> bool:
        """Check all escalation conditions."""
        if estimate_tokens(context) > self.max_token_budget:
            return True
        if context.step_count >= self.max_steps:
            return True
        if context.state == AgentState.FAILED:
            return True
        # Check for blocked actions in results
        for result in context.results:
            action = result.get("action", "")
            if action in self.blocked_actions:
                return True
        return False

    def escalation_message(self, context: AgentContext) -> str:
        """Generate context-rich escalation message for human."""
        lines = [f"🚨 Agent escalation: {context.task}"]
        lines.append(f"Steps completed: {context.step_count}")
        lines.append(f"Token usage: ~{estimate_tokens(context)}")
        if context.error:
            lines.append(f"Error: {context.error}")
        lines.append(f"\nResults so far:")
        for i, result in enumerate(context.results):
            lines.append(f"  {i+1}. {result.get('action', 'unknown')}: {result.get('summary', '')}")
        return "\n".join(lines)
```

## Security Considerations

### Tool Permission Model

| Permission | Granted To | Risk Level |
|---|---|---|
| `file:read` | Search, analyze tools | Low |
| `file:write` | Code generation (sandbox only) | **High** — restrict to temp dirs |
| `exec:readonly` | Test runners, linters | Medium |
| `exec:write` | **Never grant to autonomous agents** | **Critical** |
| `api:read` | Data fetching | Low |
| `api:write` | **Require human approval** | **Critical** |
| `network:outbound` | External API calls | Medium — allow-list domains |

### Sandboxing Rules

1. **Read-only by default** — agents read, never write or execute
2. **Allow-list mutations** — specific paths in `/tmp/` or `workspace/sandbox/`
3. **No shell access** — use structured tool calls, never `eval` or `exec`
4. **Network allow-list** — only permitted API endpoints
5. **Timeout enforcement** — every tool call has a max duration (30s default)
6. **Rate limiting** — max N tool calls per loop iteration

### Output Validation

Always validate agent outputs before acting on them:

```python
from pydantic import BaseModel, field_validator

class AgentAction(BaseModel):
    action: str
    path: str
    content: str | None = None
    reason: str

    @field_validator("path")
    @classmethod
    def validate_path(cls, v: str) -> str:
        # Prevent path traversal
        if ".." in v or v.startswith("/"):
            raise ValueError(f"Invalid path: {v}")
        return v

    @field_validator("action")
    @classmethod
    def validate_action(cls, v: str) -> str:
        allowed = {"read_file", "write_file", "search", "run_test"}
        if v not in allowed:
            raise ValueError(f"Unknown action: {v}. Allowed: {allowed}")
        return v
```

## Workflow Steps

### Step 1: Define Task Boundaries

Clearly scope what the agent can and cannot do:

```python
task_bounds = {
    "objective": "Refactor auth module to use Pydantic v2",
    "scope": ["src/auth/", "tests/auth/"],
    "blocked_paths": ["src/auth/secrets.py", "config/"],
    "allowed_tools": ["file_read", "file_write", "grep_search", "run_test"],
    "max_steps": 15,
    "token_budget": 12000,
    "output_format": "pydantic.AgentAction",
}
```

### Step 2: Set Up Tool Registry

Register only the tools the agent needs, with strict schemas:

```python
registry = ToolRegistry()
registry.register(FileReadTool(scope=["src/auth/", "tests/auth/"]))
registry.register(FileWriteTool(scope=["src/auth/", "tests/auth/"]))
registry.register(GrepSearchTool(scope=["src/"]))
registry.register(RunTestCommand("pytest tests/auth/ -v"))
```

### Step 3: Configure Guardrails

```python
guardrails = [
    create_file_write_guardrail(),
    create_token_budget_guardrail(12000),
    create_step_limit_guardrail(15),
    create_no_shell_guardrail(),
    create_output_schema_guardrail(AgentAction),
]
```

### Step 4: Run with Monitoring

Execute the loop and log every step for audit:

```python
context = AgentContext(task=task_bounds["objective"])
context = agent_loop(context, registry.tools, guardrails, planner, executor, validator)

if context.state == AgentState.ESCALATED:
    print(escalation_policy.escalation_message(context))
    # Hand off to human
elif context.state == AgentState.COMPLETE:
    print(f"Completed in {context.step_count} steps")
```

### Step 5: Audit Results

Review the step log, validate outputs, and merge changes:

```python
for i, result in enumerate(context.results):
    print(f"Step {i+1}: {result['action']} — {result.get('summary', 'no summary')}")

# Run full test suite before merging
run_shell_command("pytest tests/ -v --cov=src")
```

## Anti-Patterns to Avoid

| Anti-Pattern | Risk | Mitigation |
|---|---|---|
| Unbounded loops | Token explosion, runaway costs | Hard step + token limits |
| `eval` / shell access | Arbitrary code execution | Structured tool calls only |
| No output validation | Malformed actions | Pydantic/Zod schemas |
| Write access to production paths | Data loss | Sandbox to temp dirs only |
| No escalation path | Stuck agents | Timeout + step limit + human handoff |
| Silent failures | Undetected errors | Log every step, fail loudly |

## Success Checklist

- [ ] Task boundaries defined (scope, blocked paths, allowed tools)
- [ ] Tool registry configured with allow-listed tools only
- [ ] Input/output schemas validated on every tool call
- [ ] Guardrails active (file write, token budget, step limit, no shell)
- [ ] Self-correction loop with max retry count
- [ ] Escalation policy with human handoff
- [ ] Step-by-step audit logging enabled
- [ ] Test suite runs after agent completes
- [ ] No secrets or credentials exposed to agent context
