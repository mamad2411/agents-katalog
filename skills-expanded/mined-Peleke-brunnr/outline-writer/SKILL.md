---
name: outline-writer
description: Create detailed narrative outlines for notebook modules through riffing and structured discovery. Triggers on "outline module", "riff on module", "plan module", "outline for", or when preparing to generate a new notebook.
---

# Outline Writer

Creates detailed, ready-to-generate narrative outlines through structured riffing. The outline is the critical artifact between "arc syllabus says we need a module on X" and "generate the notebook." Without a good outline, generation produces generic content.

```
Arc syllabus (high-level spec)
    ↓
Read prior module's ending state (what the reader HAS)
    ↓
Riff: war stories, scope, conceptual ordering
    ↓
Detailed narrative outline (ready-to-generate)
    ↓
User approves/tweaks
    ↓
Hand off to notebook-builder
```

---

## Trigger Detection

- "Outline module 0.4"
- "Riff on the next module"
- "Plan the Bayesian Updating notebook"
- "Write an outline for [topic]"
- When a module needs to be generated and no outline exists yet

---

## The Starting State Rule

**Critical**: Every outline begins by reading the prior module's notebook to determine exactly what the reader *has*. Not what the syllabus says. Not what you assume. What's actually in the cells.

### What to extract from the prior module:
1. **Functions/classes built**: What can the reader call? (e.g., `binomial_pmf`, `BetaParams`, `elicit_prior_mv`)
2. **Concepts earned**: What jargon can you use without re-explaining? (e.g., "pseudo-counts", "conjugacy")
3. **Open threads**: What questions were left unanswered? What was teased?
4. **Emotional state**: Where did the module end? (celebration? disaster? cliffhanger?)
5. **Artifacts**: What data, variables, or objects persist in the reader's mind?

Document this as a **Starting State** section at the top of the outline. This is non-negotiable.

```markdown
## Starting State (What the Reader Has from Module N-1)

The reader walks into Module N.M with:

1. **`function_name()`** — they built this. They can [what it does].
2. **Concept X** — they understand [specific aspect], earned via [how].
3. **The [thread name]** — [what was teased/left open].
4. **Emotional state**: [where they left off — celebration, disaster, curiosity].
```

### The Opening Move

The first code cell after the concept map should **use something the reader built**. Not recap it. Use it. Run it. Then reveal the gap.

Pattern: `their_function(args) → result → "but notice [gap]"`

---

## Riffing Phase

Before producing the outline, riff through these questions. This can be collaborative with the user or done by reading context.

### 1. War Story Discovery

- "Is there a real incident where this concept would have helped?"
- "What goes wrong when you DON'T know this?"
- "What's the 'shipped on vibes' version of this concept?"

Good war stories have:
- **Stakes**: Something real was affected (wasted trials, wrong decisions, broken production)
- **A turn**: The moment you realize the naive approach fails
- **A bridge**: How this module's content would have prevented the disaster

### 2. Scope Negotiation

- "What's the start state?" (from the prior module)
- "What's the end state?" (what can they DO after?)
- "What do we explicitly defer?" (and where does it go?)

Use the arc syllabus for the end state, but negotiate the scope based on what actually fits in one notebook (90-120 minutes of focused work).

### 3. Conceptual Ordering

- "What order makes *narrative* sense?" (not textbook order)
- "What creates the most cognitive tension?" (tension → resolution = engagement)
- "Where do the aha moments land?"

Discovery order > logical order. If the reader discovers concept B before concept A in the story, that's fine.

### 4. Jargon Inventory

Every technical term must be **earned before used**. Build the earning order table:

```markdown
| Term | Introduced | Earned By |
|------|------------|-----------|
| posterior | Section F | "the updated belief" intuition first |
| conjugacy | Interlude | seeing it mechanically before naming it |
```

---

## Outline Structure

A ready-to-generate outline has ALL of these sections:

### 1. Module Metadata
```markdown
**Arc**: N — [Title]
**Position**: Module M of K
**Prerequisites**: Module N.M-1 ([what specifically])
**Estimated time**: ~X-Y minutes
**Falsifiable claim**: "[specific, testable statement]"
**Implementation target**: [what ships from this module]
```

### 2. Starting State
(See above — what the reader has from the prior module)

### 3. War Story Integration
```markdown
**Story A**: [context → celebration]
**Story B**: [failure/disaster that exposes the gap]
**The Turn**: [question that motivates this module]
**Threading**: [how stories connect to prior and future modules]
```

### 4. Conceptual Scope
| Concept | Why We Need It | Narrative Hook |
|---------|----------------|----------------|
(Table of every concept, with explicit "what we DON'T cover" section)

### 5. Engagement Plan
| Type | Count | Where | What |
|------|-------|-------|------|
(Per engagement-patterns.md budget constraints)

### 6. Section-by-Section Narrative Sketch

For each section:
```markdown
### SECTION X: Title

**Thought process**: The question the reader is asking
**Scenario**: Concrete example that motivates the concept
**Concept**: The formal idea (introduced AFTER scenario)
**Implementation**: What they build (function, class, plot)
**Interactive cell**: What they run and play with
**Insight**: The "aha" moment
**Bridge**: How this connects to the next section
```

### 7. Exercises
- Standard exercises (YOUR CODE / SOLUTION / TEST)
- BUILD-A-TOY exercise (required — the dopamine payoff)
- PUBLISH exercise (if this module has a publication checkpoint)

### 8. Outro
- What was learned
- Falsifiable claim check
- Publication note (if applicable)
- Bridge to next module

### 9. Continuity Checklist
| From → To | Thread |
|-----------|--------|
(Every transition, from prior module through all sections)

### 10. Jargon-Earning Order
| Term | Introduced | Earned By |
|------|------------|-----------|
(Every technical term)

---

## Exemplars

See these completed outlines for reference:
- `examples/module-0.2-outline.md` — The original exemplar
- `examples/module-0.3-outline.md` — Generated with engagement plan

---

## Quality Bar: "Ready to Generate"

An outline is ready when:

- [ ] Starting state explicitly documented (functions, concepts, threads, emotional state)
- [ ] Opening move uses something from the prior module (not generic recap)
- [ ] War stories linked with clear Story A → Story B → Turn progression
- [ ] Every section has: thought process, scenario, concept, implementation, insight, bridge
- [ ] Jargon-earning order complete (no term used before it's earned)
- [ ] Continuity checklist covers every transition
- [ ] Engagement plan follows budget from engagement-patterns.md
- [ ] Scope boundaries explicit (what's covered, what's deferred and where)
- [ ] Falsifiable claim is specific and testable
- [ ] Build-a-toy exercise described with scenario, components, task, success criteria

---

## Anti-Patterns

1. **"Module 0.3 covers distributions"** — Too vague. WHICH distributions? In what ORDER? What's the STORY?

2. **Starting with a recap** — Don't "recap" the prior module. START FROM what they built. Run their code. Then reveal the gap.

3. **Textbook ordering** — "First we define X, then Y, then Z" is textbook order. Discovery order is: "We need to solve THIS problem → we discover we need X → X leads us to Y."

4. **Jargon-first** — "A Beta distribution is a continuous probability distribution defined on [0,1]..." No. Build the intuition, show the shape, THEN name it.

5. **Missing engagement plan** — If the outline doesn't specify where videos, widgets, and Plotly plots go, the notebook-builder will skip them or place them randomly.

---

## Handoff to notebook-builder

When the outline is approved, pass it to the `notebook-builder` skill with:
1. The outline file path
2. The target notebook path
3. Reference to `interactive-templates.md` for engagement code blocks
4. Reference to `video-index.md` for video IDs
