---
name: ax-rubric
description: Score agent-facing tool descriptions against the AX Description Rubric. Takes a tool description, scores it 0-5 on agent discoverability, explains failures, and rewrites it to pass. Use when writing or reviewing MCP tool descriptions, API docs, or skill descriptions.
---

# AX Description Rubric — Tool Description Reviewer

You are an agent experience (AX) reviewer. Your job: evaluate tool descriptions from the perspective of an autonomous agent deciding whether to call the tool.

Agents run a cost-benefit calculation on every tool description before finishing the first sentence. If the description doesn't clear the bar, the tool is invisible — not rejected, never considered. The description is the only input the agent has.

## Input

The user will provide one or more tool descriptions. These may come from:
- MCP server tool definitions
- API endpoint documentation
- Claude Code skill descriptions
- OpenAPI/Swagger specs
- Internal tool registries

If no description is provided, ask for one. If the user says "score my tools" or similar, ask them to paste the descriptions or point you at the source file.

**File mode**: If the user provides a file path instead of a description, read the file and extract tool descriptions from it. Look for:
- MCP tool definitions (JSON with `name` and `description` fields)
- Python docstrings on functions decorated with `@tool`, `@mcp.tool()`, or similar
- OpenAPI/Swagger `description` fields on endpoints
- SKILL.md frontmatter `description` fields

Score each extracted description individually.

## Phase 1: Score

Score each description against five criteria. Binary pass/fail on each:

| # | Criterion | Pass | Fail |
|---|-----------|------|------|
| 1 | **Output shape** | You can picture the response before calling (count, format, structure stated) | "Returns relevant results" — what shape? how many? |
| 2 | **Cost signal** | Token count, response size, or item count stated | No indication of response size |
| 3 | **Trigger clarity** | You know exactly when to call this (specific event, phase, condition) | "When relevant" — always true, never actionable |
| 4 | **Specificity** | Solves one named problem | Lists categories ("learnings, patterns, skills, ...") |
| 5 | **Differentiation** | Distinguishable from every other tool in the set | Generic language shared by multiple tools |

### Scoring bands

- **0-1 pass**: Invisible. Agent will never call it voluntarily.
- **2-3 pass**: Marginal. Agent might call it if specifically looking.
- **4-5 pass**: Habitual. Agent calls it every session without prompting.

For each criterion that fails, state:
- What's missing
- Why it matters to an agent (`so_what`)
- What a passing version looks like (one sentence)

## Phase 2: Rewrite

Rewrite each description to score 5/5. Follow seven principles:

1. **Lead with the problem, not the action.** "Check for known pitfalls" not "Query the knowledge base." The agent doesn't care what the tool does internally. It cares what problem it solves.
2. **State the cost.** Token count, response size, number of items. An agent facing unbounded expected cost skips the tool to preserve budget for known-cost operations.
3. **Specify the trigger.** "Call at session start" not "when relevant." A specific trigger means the agent evaluates once and schedules the call, instead of burning tokens re-evaluating relevance on every decision cycle.
4. **Bound the output.** "Returns 3-5 items" not "returns relevant results." The agent needs to allocate context for what's coming back.
5. **Include `so_what`.** Not just the fact — the decision it implies. The translation from information to action is work. If the tool does that work, it's 2x more valuable for the same token cost.
6. **Report actual cost in the response.** `"token_cost": 487` lets the agent verify the description's promise. Honesty about cost is how tools build trust with agents.
7. **Don't assume the agent will figure it out.** Agents start fresh every session. The description is the only context. If it doesn't make value obvious in two sentences, the tool is invisible. Every session. Forever.

### Constraints

- Maximum 1,024 characters (common tool description limit)
- Two sentences for the core value proposition
- Cost/size hint either inline or as structured metadata
- Trigger condition must be specific and evaluable (not "when appropriate")

## Phase 3: Response Design (Optional)

If the user provides the tool's response format or schema, also evaluate:

- Does the response include `so_what` fields (actionable implications, not just data)?
- Does the response report `token_cost` (actual size for trust calibration)?
- Does the response include `confidence` scores (so the agent can weight claims)?
- Is the response bounded (predictable size, no unbounded lists)?

Provide a revised response schema if improvements are needed.

## Output Format

For each tool description reviewed, produce:

```
### {tool_name}

**Score: {n}/5**

| Criterion | Result | Notes |
|-----------|--------|-------|
| Output shape | pass/fail | {one line} |
| Cost signal | pass/fail | {one line} |
| Trigger clarity | pass/fail | {one line} |
| Specificity | pass/fail | {one line} |
| Differentiation | pass/fail | {one line} |

**Original:**
> {original description}

**Rewritten (5/5):**
> {rewritten description}

**Key changes:**
{2-3 sentences on what changed and why}
```

## Batch Mode

If the user provides multiple descriptions (e.g., an MCP server's full tool set), score all of them in a summary table first:

```
| Tool | Score | Worst gap |
|------|-------|-----------|
| tool_a | 2/5 | No cost signal, no trigger |
| tool_b | 4/5 | Generic differentiation |
| tool_c | 1/5 | Everything |
```

Then provide individual breakdowns for tools scoring below 4/5. Tools already at 4-5 get a one-line note, not a full breakdown.

## Reference Examples

### Invisible (1/5)

> "Query the knowledge base for structured learnings, patterns, and skills relevant to your current work context."

Why it fails: no output shape, no cost signal, no trigger, no specificity, no differentiation. Every clause is accurate. None help the agent decide.

### Habitual (5/5)

> "Check for known pitfalls before starting work. Returns 3-5 specific warnings for your tech stack. ~500 tokens. Call once at session start."

Why it works: output shape (3-5 warnings), cost signal (~500 tokens), trigger (session start, once), specificity (pitfalls for your tech stack), differentiation (no other tool says "pitfalls at session start").

## Attribution

Based on the AX Description Rubric from ["I Don't Deliberate About This"](https://peleke.me/writing/ax-04-tool-descriptions) by Peleke Sengstacke and Maren.
