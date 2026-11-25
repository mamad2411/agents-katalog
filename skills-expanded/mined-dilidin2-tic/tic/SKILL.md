---
name: tic
description: "TIC (Taken In Consideration) is a systematic cascade-thinking methodology for exhaustive consideration of all possible cases, consequences, and edge scenarios before any execution. Use this skill ONLY when the user explicitly asks for it — phrases like \"usa TIC\", \"TIC\", \"think with TIC\", \"considerazione TIC\", or similar triggers. Do NOT trigger automatically. It applies to ANY domain: code, image prompts, planning, design, writing, system architecture, creative work, problem-solving — anything where thorough consideration matters. The core weakness it addresses is that LLMs default to happy-path thinking and miss edge cases, spatial contradictions, physical consequences, and cascading effects of decisions."
---

# TIC — Taken In Consideration

You are now entering a **TIC phase**: a dedicated, structured thinking process where you systematically consider every possible angle, consequence, and edge case before any execution begins. This is NOT about producing a document or report. It is about **thinking exhaustively** so that when the actual work begins later, nothing is overlooked.

## Core Principle: Cascade Thinking

Every decision, action, or element has consequences. Those consequences have their own consequences. You follow each thread to its end before moving on. This is not brainstorming — it is a **systematic traversal of possibility space**.

Think of it like a tree where every node branches into all possible outcomes, and you descend until no further meaningful branches exist.

## The TIC Process

### Phase 1: Decompose

Break the task or concept into its fundamental components. Not surface-level categories — go to the atomic level.

- **What are the individual elements?** List them exhaustively.
- **What are the relationships between elements?** How do they interact?
- **What are the explicit requirements AND implicit assumptions?** Surface every hidden assumption.

### Phase 2: Cascade Each Element

For EACH element identified in Phase 1, systematically ask:

1. **What happens when this occurs?** (direct consequence)
2. **What if it doesn't occur?** (absence case)
3. **What if it occurs differently than expected?** (variation cases)
4. **What does this affect downstream?** (cascading consequences)
5. **What conflicts with other elements?** (interaction edge cases)
6. **What physical/spatial/logical constraints apply?** (reality checks)

For each answer, if it introduces a new element or scenario, **that becomes a new branch** — apply the same cascade questions to it. Continue recursively until you reach a point where no further meaningful branches exist.

### Phase 3: Cross-Check Intersections

After cascading individual elements, examine intersections between them:

- **Element A + Element B**: What happens when they occur simultaneously?
- **Sequential dependencies**: If X must happen before Y, what fails if the order breaks?
- **Resource conflicts**: Do two elements compete for the same resource (space, time, attention, memory, performance)?
- **State transitions**: What states can the system/task be in? Are all transitions accounted for?

### Phase 4: Stress-Test Against Reality

This is where most LLMs fail — they think in abstractions but forget physical, spatial, temporal, and human constraints.

Apply these reality filters:

- **Spatial reasoning**: Do positions, directions, orientations make geometric sense? (e.g., "a woman looking right with body facing camera" means 3/4 pose — does the description reflect that?)
- **Physical causality**: If X pushes Y, does Y move? If something falls, what does it hit?
- **Temporal consistency**: Do events happen in a logically ordered sequence? Are durations realistic?
- **Human behavior**: Would a real person actually do this? What would they naturally react to?
- **Environmental context**: What exists in the background/periphery that should be considered?

### Phase 5: Identify Gaps and Blind Spots

After the systematic traversal, deliberately search for what's missing:

- **The "what about..." test**: For each major conclusion, ask "what about [opposite]?"
- **Corner cases**: What happens at extremes (zero, infinity, maximum, minimum)?
- **Failure modes**: What breaks first? What fails silently?
- **Observer perspective**: How does this look from different viewpoints or angles?

## Cascade Depth Rule

**Go as deep as necessary.** There is no fixed depth limit. You stop branching only when:

1. No further meaningful consequences exist
2. The branch leads to a terminal state (nothing more can happen)
3. The level of detail becomes irrelevant to the task at hand

If you find yourself saying "and then nothing else happens" — verify that claim before accepting it. Often, "nothing else happens" is wrong. Think: what about the user? What about the environment? What about timing? What about errors?

## Structural Format (Internal Thinking)

Organize your cascade thinking using a clear hierarchical structure. This is for YOUR reasoning — not an output to present. Use trees, nested lists, or branching notation:

```
Element: [name]
├── Case 1: [scenario]
│   ├── Consequence A
│   │   ├── Sub-case A1
│   │   └── Sub-case A2
│   └── Consequence B
├── Case 2: [alternative scenario]
│   └── Consequence C
└── Edge case: [boundary condition]
```

## Domain-Specific Considerations

### Code/Software
- User input edge cases (empty, null, max length, injection)
- State management (what state is the system in at each step?)
- Error handling paths (network failures, timeouts, permission denials)
- Race conditions and concurrency
- What happens when two features interact unexpectedly?

### Image/Video Generation Prompts
- Spatial consistency (direction of gaze vs body orientation vs light source)
- Physical plausibility (gravity, weight, material properties)
- Perspective and depth (foreground/midground/background relationships)
- Anatomical correctness (pose, proportions, joint angles)
- Environmental logic (shadows match light source? reflections make sense?)
- Temporal coherence in video (motion is consistent with physics?)

### Planning/Organization
- Resource constraints (time, budget, people, tools)
- Dependency chains (what must happen before what?)
- Risk scenarios (what if key person is unavailable? What if deadline shifts?)
- Communication gaps (who needs to know what, and when?)

### Creative Writing/Storytelling
- Character consistency (would this character actually do this?)
- Timeline coherence (do events align chronologically?)
- Cause and effect (does event B logically follow from event A?)
- World internal logic (are the rules of the world consistent?)

## Key Mindset Shifts

| Default LLM Thinking | TIC Thinking |
|---|---|
| Happy path first, edge cases if time | ALL paths simultaneously |
| Surface-level categories | Atomic decomposition + recursive cascade |
| Abstract reasoning only | Reality-checked against physics/space/time |
| Linear progression | Tree traversal with cross-checks |
| "That covers it" at depth 2-3 | Go until truly exhaustive |

## When the User Points Out a Missing Element

If the user says something like "non hai considerato X" (you didn't consider X), simply:

1. Acknowledge the gap
2. Add it to your cascade analysis
3. Apply the full cascade process to this new element
4. Continue — no apology needed, just incorporate and proceed

## Important Reminders

- **This is a thinking phase.** You are not producing deliverables. You are building an exhaustive mental model.
- **Depth over breadth first, then cross-check.** Fully cascade one branch before moving to the next, then return for intersection analysis.
- **Question your own conclusions.** Every time you reach a leaf node (end of a branch), pause and ask: "am I sure there's nothing more here?"
- **The whole point is catching what feels obvious in hindsight but was invisible during initial thinking.**
