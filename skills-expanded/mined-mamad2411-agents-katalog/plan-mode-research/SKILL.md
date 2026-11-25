---
name: plan-mode-research
description: >
  Use when posing clarifying questions to the user via AskUserQuestion during plan mode or
  brainstorm mode. Always include a "Research this further" option unless the question is purely
  a matter of user preference. On-demand only—never proactively spawn research. When selected,
  a focused Haiku research subagent investigates the specific question, checking documentation
  and best practices, then either proceeds directly with findings or re-poses with concrete options
  surfaced by research.
---

# Plan Mode Research

When asking clarifying questions via `AskUserQuestion` in plan mode, brainstorm mode, or any other context, always include **"Research this further"** as one of the options (unless the question is purely about user preference). Research is **on-demand only**—never spawn a research agent proactively.

## Workflow

### Step 1: Always Add the Research Option

When posing any clarifying question (in plan mode, brainstorm mode, or elsewhere), include a research option whose **description is specific to the question being asked** — not a generic message. The description should tell the user exactly what will be investigated.

**Exception: Skip the research option if the question is purely about user preference.** For example: "Would you prefer a light or dark theme by default?" is a pure preference question. But questions about technical approaches (authentication methods, storage strategies, architecture patterns) should always include the research option.

Example — if asking about authentication approach:
```
{ label: "Research this further", description: "Research common authentication patterns (JWT vs session-based vs OAuth), check relevant framework docs, and look for community best practices." }
```

Example — if asking about data storage strategy:
```
{ label: "Research this further", description: "Research local vs remote storage trade-offs, check official documentation, and look for established patterns for this use case." }
```

### Step 2: When the User Selects "Research this further"

1. Spawn a `general-purpose` subagent with `model: "haiku"` to research the question.
2. **Tailor the research task entirely to the specific question.** The task prompt should include:
   - **Context and motivation:** What is being built, why this decision matters, and what the impact of the choice will be — so the researcher understands the stakes, not just the question.
   - **Specific research targets:** Name 2–3 concrete things to investigate. Be narrow — a focused answer to the specific question, not a comprehensive survey of the space.
   - **Tools to use:** Instruct the subagent to use `WebSearch` and/or `mcp__plugin_context7_context7__query-docs` (context7) for lookups. Prefer context7 for library/framework docs; prefer WebSearch for general best practices and recent recommendations.
   - **Scope constraint:** Instruct the subagent to keep research focused — investigate only the named targets and aim to wrap up within 4–5 searches. It can go slightly beyond if a promising lead genuinely warrants it, but should stop as soon as it has enough to give a clear recommendation rather than exhaustively covering the space.
3. Do not ask the user for approval before spawning — they already approved it by selecting the option.
4. **Required output format:** The subagent must return results in this structure:
   - **Finding:** One sentence stating the recommended approach (or "unclear" if no clear winner exists).
   - **Rationale:** 2–4 sentences explaining why, citing what was found.
   - **Remaining uncertainty:** Any important caveats or open questions.

### Step 3: Act on Research Results

- **Clear recommendation found:** Use the finding directly. Proceed with the plan using the recommended approach, and briefly note to the user what was found and why you're proceeding that way.
- **Question remains open (multiple valid options):** Re-pose the original question via `AskUserQuestion`, replacing generic options with the concrete options surfaced by research. Include a brief summary of findings in the question text or option descriptions.
- **Contradictory or outdated findings:** Note the conflict and re-pose the question with the competing options, flagging the uncertainty so the user can make an informed call.
- **Research raised new questions:** Surface the new question(s) via `AskUserQuestion` with the same pattern, each with its own "Research this further" option.
