---
name: subagent-arena
description: Run parallel independent subagents on the same investigation or design question, collect structured outputs, then synthesize the best elements or score approaches. Use for complex research, architecture decisions, or when multiple valid strategies exist. Trigger with "run an arena", "parallel subagents", "compare approaches", "investigate from multiple angles".
version: 1.0.0
author: Cobus Greyling
---

# Subagent Arena

Harness the parallel reasoning strength of grok-build-0.1.

## When to Use
- Ambiguous or high-stakes design questions
- Need to explore multiple implementation strategies safely
- Large investigation where one agent might miss angles
- User explicitly asks for comparison or multiple perspectives

## How to Run an Arena

1. **Define the exact question / charter** (write it down).
2. **Spawn 2–4 subagents** with deliberately different charters or constraints.
   - Example charters:
     - "Approach A: minimal diff, ship fast"
     - "Approach B: most correct long-term architecture"
     - "Approach C: best testability and observability"
     - "Approach D: security and compliance first"
3. **Give each subagent**:
   - The same core context + specific charter
   - Instructions to produce structured output (Goal, Tradeoffs, Recommended Steps, Risks, Confidence)
   - "Do not make any edits. Investigation only."
4. **Synthesize**:
   - Compare outputs side-by-side (use a table).
   - Extract the strongest ideas from each.
   - Propose a hybrid or winning path.
5. **Present synthesis + recommendation** and (usually) hand off to `plan-mode-orchestrator`.

## Structured Output Template for Subagents
```markdown
**Charter:** ...
**Findings:**
- ...
**Tradeoffs:**
- ...
**Recommended Next Steps:**
1. ...
**Risks:**
- ...
**Confidence:** High / Medium / Low
```

## Best Practices
- Make charters distinct enough to be useful.
- Keep subagents read-only unless the arena is specifically about implementation tactics.
- Always synthesize — never just paste raw subagent output.
- Track token/cost impact when relevant (especially useful in showcases).

## Integration with Other Skills
- Almost always followed by `plan-mode-orchestrator`.
- Pair with `architecture-reviewer` or `security-audit` for specialized arenas.

## Example Prompts
- "Run a subagent arena on the best way to add persistent memory to the MCP control center."
- "Use parallel subagents to investigate the three possible test strategies for the session analyzer."
