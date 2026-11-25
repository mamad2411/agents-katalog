---
name: prompt-context-handoff-for-agent-runtime
description: "Package prompt, identity, and runtime constraints into one explicit handoff so child agents start with the right context and no accidental leakage."
metadata:
  author: ychampion
---

# SKILL: Prompt-Context Handoff for Agent Runtime
**Domain:** multi-agent  
**Trigger:** Use when a parent agent or workflow must launch a child agent with a prompt plus selected runtime state, constraints, and capabilities.  
**Source Pattern:** Distilled from reviewed subagent orchestration, fork control, and lifecycle-bound context handoff implementations.

## Core Method
Build the child handoff as one explicit package instead of reconstructing context implicitly at the call site. Include the task prompt, the child’s identity or role, the allowed capabilities, the relevant prior state, and any lifecycle constraints the child must respect. Strip everything the child does not need, then pass the curated package through the runner that creates the child context. This keeps startup deterministic and prevents accidental leakage of parent-only state, permissions, or tool surfaces.

## Key Rules
- Decide handoff contents intentionally; do not inherit the whole parent state by default.
- Include identity, capability limits, and lifecycle expectations alongside the prompt.
- Preserve the minimum shared state needed for correctness, not convenience.
- Keep the handoff shape stable so retries and resumed child agents reconstruct the same context.
- Align the handoff package with the child’s cleanup and permission model.

## Example Application
When a main coding agent spawns a planning or execution child, create a handoff object containing the child prompt, selected tools, relevant messages, and the child’s role description. Pass that package into the child runner instead of letting the runner pull arbitrary parent globals.

## Anti-Patterns (What NOT to do)
- Don’t hand the child the entire parent session state when only a narrow slice is required.
- Don’t pass raw prompt text without the capability and lifecycle constraints that explain how the child should operate.
- Don’t let each spawn site invent a different handoff shape for the same kind of child agent.
