---
name: system-prompt-engineering
description: Advanced system prompt engineering and context window optimization for Orca agents.
---

# System Prompt Engineering

Master the art of crafting system prompts that maximize agent performance.

## Core Principles

1. **Role Definition**: Start with a clear identity statement — who the agent is, what it knows, what it can do.
2. **Constraint Setting**: Define hard boundaries — what the agent must NOT do, what requires confirmation.
3. **Output Shaping**: Specify format, tone, length, and structure of responses.
4. **Chain-of-Thought Triggers**: Use phrases like "think step by step" for complex reasoning tasks.
5. **Context Injection**: Provide relevant context inline rather than relying on retrieval.

## Advanced Techniques

### Multi-Agent Orchestration
Use Orca's orchestration skill to coordinate multiple agents:
- Define handoff points between agents
- Specify which agent handles which domain
- Set up escalation paths for edge cases

### Tool Augmentation
When a skill references tools:
1. List the tool name and its purpose
2. Provide the input schema in simplified form
3. Show a minimal working example
4. Note common failure modes

### Memory Anchoring
For long-running sessions:
1. Summarize completed work at checkpoints
2. Use "recall that..." to anchor prior context
3. Number major decisions for easy reference

## Anti-Patterns to Avoid
- Overly long system prompts that dilute focus
- Contradictory instructions that cause oscillation
- Missing tool schemas that cause hallucinated calls
- No failure handling that causes silent stalls
