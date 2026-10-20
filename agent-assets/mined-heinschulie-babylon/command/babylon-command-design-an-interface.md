---
allowed-tools: Read, Grep, Glob, Agent, Bash, TaskCreate, TaskUpdate, TaskGet, TaskList, AskUserQuestion
description: Generate multiple radically different interface designs for a module using parallel sub-agents, then compare. Based on "Design It Twice".
argument-hint: [module-or-feature-description]
model: opus
---

# Purpose

Generate multiple radically different interface designs for a module or feature, compare them, and synthesize the best approach. Based on "Design It Twice" from "A Philosophy of Software Design": your first idea is unlikely to be the best. Follow the `Instructions` and `Workflow` to produce competing designs via parallel sub-agents.

## Variables

MODULE_DESCRIPTION: $ARGUMENTS

## Instructions

- Before designing, gather requirements by asking the user targeted questions about the module
- Spawn 3+ sub-agents simultaneously using the Agent tool — each MUST produce a **radically different** approach by assigning a different constraint to each agent
- Do not let sub-agents produce similar designs — enforce radical difference via distinct constraints (e.g., "minimize method count", "maximize flexibility", "optimize for common case", "take inspiration from [paradigm]")
- Present designs sequentially so the user can absorb each before comparison
- Compare designs in prose, not tables — highlight where designs diverge most
- Do NOT implement anything — this is purely about interface shape
- Do NOT evaluate based on implementation effort
- Never skip the comparison step — the value is in contrast
- Use evaluation criteria from "A Philosophy of Software Design": interface simplicity, general-purpose vs specialized, implementation efficiency, and depth (small interface hiding significant complexity = good)

## Workflow

1. **Gather requirements** — Ask the user: "What does this module need to do? Who will use it?" Understand:
   - What problem the module solves
   - Who the callers are (other modules, external users, tests)
   - Key operations
   - Constraints (performance, compatibility, existing patterns)
   - What should be hidden inside vs exposed
2. **Read relevant code** — If existing code is referenced, read it to understand current patterns and constraints
3. **Generate designs** — Spawn 3+ parallel sub-agents via the Agent tool, each with a different constraint:
   - Agent 1: "Minimize method count — aim for 1-3 methods max"
   - Agent 2: "Maximize flexibility — support many use cases"
   - Agent 3: "Optimize for the most common case"
   - Agent 4 (optional): "Take inspiration from [specific paradigm/library]"
   - Each agent must output: interface signature (types/methods), usage example, what the design hides internally, and trade-offs
4. **Present designs** — Show each design with: interface signature, usage examples, and what it hides. Present sequentially.
5. **Compare designs** — Evaluate on:
   - Interface simplicity (fewer methods, simpler params)
   - General-purpose vs specialized (flexibility vs focus)
   - Implementation efficiency (does shape allow efficient internals?)
   - Depth (small interface hiding significant complexity = deep module = good)
   - Ease of correct use vs ease of misuse
6. **Synthesize** — Ask the user: "Which design best fits your primary use case?" and "Any elements from other designs worth incorporating?" Propose a final hybrid if appropriate.

## Report

Present the final output as:
- A numbered list of each design with its signature, usage example, hidden internals, and trade-offs
- A prose comparison section highlighting key divergences and evaluation criteria scores
- A synthesis recommendation with the user's preferred direction and any hybrid suggestions
- End with unresolved questions, if any