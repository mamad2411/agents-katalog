---
name: pbs-exploration-discovery
description: "Use after brainstorming synthesis is approved, when open technical questions need answers and stack decisions need evidence"
---

# Exploration Discovery

## Overview

Guide the technical investigation phase (Etapa 0-B). Research technologies, evaluate options, validate feasibility through spikes, and make informed stack decisions. The output is a discovery synthesis with DECISIONS backed by evidence.

**Core principle:** Discovery produces decisions with evidence, not opinions. "This API should work" is not a decision — "I tested this API and confirmed it returns X in Y format" is.

**Announce at start:** "I'm using the pbs-exploration-discovery skill to investigate technical options for this project."

## When to Use

- Brainstorming synthesis is approved — open questions need technical answers
- Need to evaluate and choose between technology options
- Need to validate that a critical integration or capability is feasible

## Input

Read the Brainstorming Synthesis document, specifically:
- **Section 6: Open Questions for Discovery** — these are your research agenda
- **Section 4: Key Assumptions** — pending ones need validation
- **Section 5: Risks** — those requiring technical investigation

## The Verification Rule

```
The AI can INVENT APIs, give OUTDATED prices, or suggest ABANDONED libraries.
ALWAYS verify claims with primary sources: official docs, web search, spikes.
NEVER register a technical decision based solely on AI knowledge.
```

**REQUIRED:** Use superpowers:verification-before-completion — before registering any claim about APIs, libraries, compatibility, or pricing, verify with evidence.

## The 7 Investigation Blocks

Guide the human through these blocks. Not all blocks apply to every project — skip what's irrelevant.

### Block 1: Stack and Technologies
- What language(s) fit this project best? Why?
- What framework(s)? What alternatives were considered?
- Do you need a database? What type? (relational, document, key-value, time-series)
- Do you know this stack or are you learning something new? (affects estimates)

### Block 2: Integrations and External Data
- What external APIs or data sources do you need?
- For each API: free? rate limits? auth required? SDK available?
- What format is the data? (JSON, CSV, WebSocket, etc.)
- What happens if an external API fails or is unavailable?

**CRITICAL:** Verify every API claim with web search or official docs. The AI frequently invents APIs or gives outdated information.

### Block 3: Tentative Architecture
- What are the main domain entities?
- What logical modules or components will the system have?
- How does data flow from input to output?
- Are there background processes, scheduled jobs, or real-time streams?
- What data needs persistence and what is ephemeral?

### Block 4: Design Patterns and Decisions
- What general architectural pattern? (monolith, modular, microservices, serverless)
- How will errors and retries be handled?
- Authentication/authorization needed? What type?
- Any irreversible architectural decisions to make now?

### Block 5: Non-Functional Requirements
- Acceptable latency for main operations?
- Expected concurrent users/requests?
- Does it matter if the system goes down for 5 minutes? 1 hour?
- Are there irreversible operations? (transactions, sending data, deletion)
- Are sensitive data or funds handled?
- What invariants must NEVER be broken?

### Block 6: Dev Tools and Environment
- What AI development tool will you use? (Claude Code, Cursor, etc.)
- Are there existing skills or rules for your stack worth using?
- Special environment setup needed?
- What testing framework?
- What package manager will you use? (npm/pnpm/yarn/pip/poetry/etc.)
- What naming convention will you follow? (camelCase/snake_case/PascalCase/etc.)

### Block 7: Feasibility Validation (Spikes)

A spike is a mini-experiment — NOT a prototype. It answers ONE specific question.

For each uncertain question identified during Blocks 1-6, decide:
- **No spike needed:** Answer is clear from docs/web search (just document the evidence)
- **Spike needed:** Requires real code/integration to answer → delegate to pbs-spike-planning

**If spikes are needed:**

**REQUIRED:** Use pbs-spike-planning to generate spike specs for each uncertain question. Discovery provides the questions and context; pbs-spike-planning structures them into proper specs with measurable criteria.

```
GOOD spike question: "Can the Binance WebSocket API stream trades
  for 100 pairs simultaneously without disconnecting?"
BAD spike question: "Does this library work?"
```

**After spike specs are generated:**

<HARD-GATE>
PAUSE the discovery session here. Tell the human:
"I've generated [N] spike specs at `.pbs-framework/exploration/spikes/`.
Execute them in separate sessions using pbs-spike-execution, then return here to continue."

Do NOT attempt to execute spikes within the discovery session.
Do NOT continue to the synthesis until spike results are available.
</HARD-GATE>

**After spikes are executed (human returns):**

1. Read the results from each spike spec file (the `## Results` section)
2. Incorporate findings into the discovery synthesis (Section 6: Spike Results)
3. If any spike was INCONCLUSIVE, discuss with the human: re-spike, pivot, or accept the risk
4. Continue closing the discovery

## Decision Evaluation Format

For every significant technical decision, evaluate options explicitly:

| Option | Cost | Pros | Cons | Decision |
|--------|------|------|------|----------|
| [option A] | [free/paid] | [advantages] | [disadvantages] | chosen / discarded |
| [option B] | [free/paid] | [advantages] | [disadvantages] | chosen / discarded |

Include the REASON for the final choice. "I'm familiar with it" is valid only if the alternatives offer no clear advantage.

## Readiness Signals

Discovery is ready when:
- [ ] Stack chosen with clear, documented reasons
- [ ] Critical external integrations validated (at minimum: docs reviewed; ideally: spike run)
- [ ] Architecture sketch can be explained in 2 minutes
- [ ] No blocking technical questions remain unanswered
- [ ] Key decisions documented with alternatives considered

If any signal fails → continue investigating the weak areas.

## Output

Generate `.pbs-framework/exploration/discovery-synthesis.md` with:

1. **Stack decisions** — table with chosen tech, alternatives, reasons
2. **Integrations evaluated** — table with APIs, cost, limits, auth, SDK, decision
3. **Tentative architecture** — modules, data flow, persistence
4. **Design decisions** — numbered decisions with context, alternatives, rationale
5. **Non-functional requirements** — latency, concurrency, availability, security
6. **Spike results** — table with question, result, time, conclusion
7. **Dev environment and tools** — AI tool, skills evaluated, setup needed, code conventions (package manager, naming convention)
8. **Resolved questions from brainstorming** — mapping of original questions to answers
9. **Updated technical risks** — risks from brainstorming + new ones discovered
10. **Next steps → Etapa 1** — what remains before generating definitions

<HARD-GATE>
The human MUST approve the discovery synthesis before proceeding to definitions.
If the human disagrees with a technical decision, re-evaluate with their input.
If the human identifies unverified claims, verify them before finalizing.
</HARD-GATE>

## Session Structure (Suggested)

```
Session 1: Stack + Integrations (Blocks 1-2)
  Duration: 2-3 hours (includes web search)
  Key: Do NOT trust AI alone for API data. Verify.

Session 2: Architecture + Decisions (Blocks 3-4)
  Duration: 1-2 hours
  Technique: Ask for 2-3 architecture options and compare

Session 3: NFRs + Spike Identification (Blocks 5-7)
  Duration: 1-2 hours
  Key: Generate spike specs, then PAUSE for spike execution

--- SPIKE SESSIONS (separate, using pbs-spike-execution) ---

Session 4: Resume Discovery + Synthesis (read spike results + final document)
  Duration: 1-2 hours
```

## Common Mistakes

- **Trusting AI-generated API specs** — the AI invents endpoints, parameters, and pricing. Always verify with official docs or web search.
- **Choosing stack by familiarity alone** — valid reason, but evaluate at least one alternative to confirm.
- **Skipping spikes for uncertain questions** — a 2-hour spike now prevents a 2-day rewrite later.
- **No decision table for major choices** — every significant choice needs Option | Cost | Pros | Cons | Decision format.

## Red Flags

- "This API should work" without verification → Verify with docs or a spike first.
- Choosing stack only because "I'm familiar with it" → Valid reason, but evaluate at least one alternative.
- Skipping spikes for uncertain questions → If you're not sure it's feasible, run a spike.
- Discovery taking more than 1 week → You're over-exploring. Converge and decide.
- No decision log entries → Every technology choice is a decision. Log it.
- Trusting AI-generated API specs → The AI invents endpoints, parameters, and pricing. Verify.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I already know the best stack" | Evaluate at least one alternative. You might be surprised. |
| "The API docs say it works" | Did you read the actual docs, or is the AI paraphrasing? Verify. |
| "A spike would take too long" | A 2-hour spike now prevents a 2-day rewrite later. |
| "I'll figure out NFRs during implementation" | Latency and concurrency constraints affect architecture. Decide now. |
| "This decision is reversible anyway" | Document it anyway. Future-you needs to know WHY. |

## Integration

**Called after:**
- pbs-exploration-brainstorming — synthesis approved by human

**Required skills:**
- **REQUIRED:** superpowers:verification-before-completion — verify claims before registering decisions

**Optional skills:**
- superpowers:test-driven-development — for structuring spikes as tests
- superpowers:systematic-debugging — for understanding why spikes fail

**Delegates spike spec generation to:**
- pbs-spike-planning — generates structured spike specs for uncertain questions

**Spike specs are executed by:**
- pbs-spike-execution — in separate sessions, results written back to spike spec files

**Calls next:**
- pbs-generating-definitions — after human approves the discovery synthesis

**Language:** Write all `.pbs-framework/` documents in the language defined in AGENTS.md `framework_language` field. If not set, match the language of the brainstorming synthesis.
