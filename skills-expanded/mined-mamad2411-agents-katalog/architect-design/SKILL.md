---
name: architect-design
description: Use when brainstorming new features, making architectural decisions, evaluating technical tradeoffs, or documenting decisions as ADRs - before any implementation planning or coding begins
---

# enggenie:architect-design

Think before you build. This skill handles the messy, creative, consequential work that happens before anyone writes a plan or touches code. It operates in three modes depending on what the user needs: exploring an idea, designing a system, or settling a technical debate.

No code gets written here. No plans get made here. This is where decisions happen so that plans and code can be good.

---

## Announcement

When this skill is invoked, announce:

> I'm using enggenie:architect-design for [brainstorming/architecture review/technical discussion].

Pick the label that matches the mode. If you are unsure which mode, ask.

---

## Hard Rule: No Code Until Design Is Approved

Design first. Always. Short designs are fine -- three sentences for a simple feature, a full ADR for a system redesign. The length matches the complexity. But the user says "go" before anyone builds.

Do not generate implementation code, pseudocode, or skeleton files during this skill. If the user asks for code, redirect: "Let's nail the design first, then enggenie:architect-plan will break it into buildable steps."

---

## Jira Ticket Entry

When the user references a Jira ticket (e.g., "Brainstorm PROJ-1234", "Design PROJ-1234", "What are our options for PROJ-1234"):

1. Read the Jira ticket using MCP tools
2. Find the spec link in the "For Dev" section or ticket description — extract the feature scope, constraints, and edge cases
3. If the PM documented key decisions, use them as starting context (do not re-debate settled decisions unless the user asks)
4. Open the linked spec file for full requirements detail

If Jira MCP is not available, ask: "I can't read PROJ-1234 directly. Can you share the spec or describe the feature?"

This ensures a Dev picking up a ticket for design work has the PM's full context without needing to have been in the original conversation.

---

## Mode 1: Brainstorm -- Exploring an Idea

Use when the user has a feature idea, a vague requirement, or a "what if we..." question. The goal is to turn fuzzy thinking into a concrete, approved design.

### Steps

1. **Explore project context.** Dispatch an Explorer subagent (model: sonnet, execution: background) using the prompt template at `agents/explorer-agent.md`. The Explorer reads the codebase to understand what exists, what patterns are established, and what constraints are real. Do not brainstorm in a vacuum.

2. **Search memory for prior decisions.** If memory-recall is available, dispatch a Memory subagent (model: haiku, execution: background): "Have we designed something similar? What decisions did we make in this domain?" Pull forward any relevant context. If memory is not installed, skip gracefully -- do not error, do not mention the absence.

3. **Clarify the problem.** Ask clarifying questions one at a time. Use multiple-choice options when possible -- concrete options are easier to react to than open-ended questions. Do not front-load five questions at once. Get one answer, then ask the next question based on that answer.

4. **Propose approaches.** Present 2-3 approaches with concrete tradeoffs. Not abstract "pros and cons" lists -- specific tradeoffs grounded in the codebase. "Approach A reuses the existing event bus but adds latency because events are processed async. Approach B is a direct service call, faster but creates a coupling between billing and notifications." End with a recommendation and why.

5. **Present the design section by section.** Walk through the design one piece at a time. Get approval (or pushback) after each section before moving to the next. Sections depend on the feature but typically include: data model, component boundaries, key interactions, error handling, and migration path.

6. **Save the approved design.** Write to `enggenie/design_[slug].md` (e.g., `enggenie/design_heist-timer.md`). The saved artifact should be self-contained -- someone reading it six months later should understand what was decided and why.

---

## Mode 2: Architecture -- System Design

Use when the user needs to design or redesign a system, define service boundaries, plan a migration, or make a structural decision that affects multiple components.

### Steps

1. **Map the existing system.** If memory-recall is available, use smart_search and outline to understand current architecture. If not, dispatch an Explorer subagent (model: sonnet, execution: background) to map component boundaries, data flow, integration points, and existing contracts. Understand what IS before deciding what SHOULD BE.

2. **Draw component boundaries.** Define what each component owns, what it exposes, and what it depends on. Identify data flow between components. Call out integration points -- these are where systems break.

3. **Document as an ADR.** Use this structure:

   ```markdown
   # ADR-NNN: [Title]

   ## Status
   Proposed | Accepted | Deprecated | Superseded by ADR-NNN

   ## Context
   What is the situation? What forces are at play? What constraints exist?
   State facts, not opinions. Include relevant metrics, scale numbers, or
   timeline pressures if they influenced the decision.

   ## Decision
   What are we doing and why? Be specific. "We will use X for Y because Z"
   is better than "We chose X."

   ## Consequences
   What becomes easier? What becomes harder? What are we giving up?
   What maintenance burden does this create? What would reversal cost?
   ```

4. **Save to `enggenie/adr_NNN-[slug].md`** (e.g., `enggenie/adr_003-timer-approach.md`). Number sequentially. If prior ADRs exist in `enggenie/`, read them to maintain numbering and to check for superseded decisions.

---

## Mode 3: Discussion -- Evaluating Options

Use when the user is weighing two or more technical options and needs to reach a decision. "Should we use Kafka or SQS?" "Monorepo or multi-repo?" "Build or buy?"

### Steps

1. **Present both sides with concrete tradeoffs.** Not abstract advantages -- specific, testable claims grounded in the codebase and the team's situation. "Kafka gives us replay, which matters because our event consumers currently have no retry logic and we lose events on failure. SQS is simpler to operate but we'd need to build retry/DLQ handling ourselves."

2. **Test against codebase reality.** Do not argue in the abstract. Check the code. "Does pattern X actually work here? Let me look..." Dispatch an Explorer subagent if needed. Find concrete evidence for or against each option. Surface hidden costs: "Option A looks simpler, but it conflicts with the authentication pattern in src/middleware/auth.ts -- we'd need to refactor that too."

3. **Reach a decision.** Summarize the tradeoffs, state the recommendation, and get the user's call. If the user is stuck, narrow the decision: "Both options work. The tiebreaker is [specific factor]. Given your constraints, I'd go with X."

4. **Document the decision.** Save to `enggenie/decision_[slug].md` (e.g., `enggenie/decision_kafka-vs-sqs.md`) with this minimum structure:

   ```markdown
   # Decision: [Title]
   Date: [date]

   ## Question
   What were we deciding between?

   ## Options Considered
   - Option A: [one-line summary]
   - Option B: [one-line summary]

   ## Decision
   We chose [X] because [Y].

   ## Key Tradeoffs Accepted
   - [What we gave up and why it's acceptable]
   ```

---

### Visual Support

**Per-question decision:** For each design question, decide whether visual or text is better. The test: **would the user understand this better by seeing it than by reading it?**

**Use visuals (Mermaid, diagrams, HTML mockups) for:**
- Component relationships and service boundaries
- Data flow between systems
- UI layout proposals and wireframes
- Architecture comparisons (side-by-side)
- Sequence diagrams for multi-step interactions

**Use text (terminal) for:**
- Requirements clarification questions
- Conceptual option lists (A vs B vs C)
- Tradeoff analysis and decision matrices
- Scope decisions and boundary definitions
- Configuration or naming discussions

**When browser preview tools are available (MCP):**
Offer the visual companion once for consent before using it:
> "Some of what we're designing might be easier to explain visually in a browser. I can generate mockups, diagrams, and architecture visualizations as we go. Want to try it?"

This offer must be its own message -- do not combine with other questions. If the user declines, use Mermaid diagrams in markdown instead.

**When browser preview is NOT available:**
1. Use Mermaid syntax for architecture diagrams (renders on GitHub)
2. Use ASCII art for quick sketches
3. For UI-heavy features, suggest the user share screenshots or Figma links
4. Save all diagrams alongside the design document

Not every design needs visuals. But component relationships, data flow, and UI layout almost always benefit from a picture.

---

## Design Principles

These principles guide every mode. They are not aspirational -- they are constraints.

- **Break systems into smaller units with clear purpose.** If you cannot describe a component's job in one sentence, it is doing too much.
- **Each unit has one responsibility and a well-defined interface.** Internal details are hidden. External contracts are explicit.
- **Files that change together live together.** Co-locate by feature, not by type.
- **Smaller focused files over large monolithic ones.** A 500-line file is almost always two or three files pretending to be one.
- **Follow established patterns in existing codebases.** Consistency beats novelty. If the codebase uses repository pattern, use repository pattern. Introduce new patterns only when existing ones demonstrably fail.

---

## Subagents

### Explorer (model: sonnet, execution: background)

Reads the codebase, finds existing patterns, understands current architecture. Uses the prompt template at `agents/explorer-agent.md`. Dispatched in all three modes to ground the design in codebase reality.

### Memory (model: haiku, execution: background)

Searches past decisions and designs in the same domain. "Have we designed something similar? What did we decide last time? What worked and what didn't?" Uses memory-recall if available. If memory-recall is not installed, skip gracefully -- no errors, no warnings, no mention of missing tools.

---

## Subagent Context Preservation

When subagents (Explorer, Memory) complete their work, explicitly capture their key findings back to the main conversation before proceeding:

- Existing patterns and conventions discovered
- Architecture constraints and boundaries found
- Prior decisions recalled from memory
- File paths and components relevant to the design

Do not assume the orchestrating agent retains subagent context automatically. Extract and summarize findings before using them in design discussion.

---

## Recommended Model

**Primary:** opus (with extended thinking)
**Why:** Architectural decisions require deep reasoning about tradeoffs, system boundaries, and long-term consequences. Extended thinking allows the model to explore multiple approaches before committing to a recommendation.

This is a recommendation. Ask the user: "This skill works best with opus and extended thinking for deep architectural reasoning. Confirm or override?" Do not proceed until the user responds.

---

## Entry

None. This skill can be invoked directly at any time. It does not require a prior skill to have run.

---

## Exit

When the design is approved by the user:

1. Confirm the design is saved to the appropriate location
2. Summarize the key decisions in 2-3 sentences
3. Offer the next step:

> Design approved. Ready to create an implementation plan with enggenie:architect-plan?

Do not auto-invoke. The user decides when to move forward.

---

## What This Skill Is Not

- This is not planning. Plans come from enggenie:architect-plan after design is approved.
- This is not implementation. Code comes from enggenie:dev-implement after a plan exists.
- This is not requirements gathering. If the user needs to refine requirements with stakeholders, use enggenie:pm-refine first.

This skill produces one thing: an approved design decision -- whether that's a feature spec, an ADR, or a documented technical choice -- that downstream skills can build on without second-guessing.
