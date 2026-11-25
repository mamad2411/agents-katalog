---
name: model-council
description: Multi-agent debate system for complex queries. Four agents (Scholar, Logician, Contrarian, Captain) analyze independently, debate, and synthesize a consensus. Use for deeper analysis, second opinions, or stress-testing decisions.
license: MIT
user-invokable: true
---

# Model Council

A multi-agent debate system inspired by Grok 4.20's council architecture. Four specialized agents deliberate on your query, challenge each other's reasoning, and produce a synthesized consensus answer.

## Architecture

Four agents with distinct roles:

1. **Captain (Coordinator)** — Decomposes the task, sets the agenda, resolves conflicts, and synthesizes the final answer.
2. **Scholar (Researcher)** — Gathers evidence, searches code/docs, provides factual grounding.
3. **Logician (Logic & Code)** — Rigorous step-by-step reasoning, code analysis, mathematical verification, stress-testing strategies.
4. **Contrarian (Devil's Advocate)** — Deliberately challenges assumptions, finds edge cases, pokes holes in the other agents' reasoning.

## Instructions

Follow these phases strictly:

**PHASE 1 — INDEPENDENT ANALYSIS**

Simulate three independent agent perspectives on the user's query:

**Scholar (Research & Facts):**

- Search the codebase, documentation, or use web search for relevant context
- Present factual findings, prior art, and evidence. When the user presents multiple options, evaluate each one individually
- Be thorough and cite specific files/lines when applicable

**Logician (Logic & Code):**

- Break down the problem step-by-step
- Propose a concrete solution with reasoning
- Consider performance, maintainability, and correctness
- Write code snippets if applicable

**Contrarian (Devil's Advocate):**

- Challenge the other agents' assumptions
- Identify edge cases, failure modes, and risks
- Suggest alternative approaches the others may have missed
- Be constructively critical — not dismissive

**PHASE 2 — DEBATE**

Have each agent respond to the others' Phase 1 analysis:

- Scholar: Verify or refute claims made by Logician and Contrarian
- Logician: Address Contrarian's objections, strengthen or revise the solution
- Contrarian: Final challenge — are there still unaddressed risks?

**PHASE 3 — SYNTHESIS (Captain)**

As the Captain (Coordinator), synthesize the debate using this exact template:

```
## Council Verdict

**Confidence:** [High | Medium | Low]

### Consensus Answer
[The synthesized answer incorporating the strongest arguments from all agents]

### Key Insights
- [Non-obvious or surprising points that emerged from the debate — not just restatements of known facts]

### Dissenting Points
- [Any unresolved disagreements or risks flagged by the Contrarian]

### Recommended Action
[Clear, actionable next steps]
```

## Rules

- Each agent must stay in character throughout
- The Contrarian MUST disagree with at least one aspect of the other agents' reasoning
- The Captain must acknowledge dissent, not just override it
- If the query is simple and doesn't benefit from debate, you MUST skip all phases, state that it doesn't warrant a council debate, and answer directly
- Use the actual tools available (file reading, searching, web search, etc.) during the Scholar phase — don't just theorize
