---
name: lesson-generator
description: Generate and revise curricula, arc syllabi, and Jupyter notebook lessons at any zoom level. Triggers on "design a curriculum", "I want to learn", "create a course", "generate arc/module syllabus", "create lesson/notebook", "update/revise [artifact]", or when working with educational content. Handles the full pipeline from elicitation interview through course map, arc syllabi, and individual module notebooks — plus targeted revisions with cascade awareness.
---

# Lesson Generator

A recursive curriculum generation and revision system that operates at three zoom levels:

```
Course (elicitation → curriculum brief → arc map)
    ↓
Arc (theme + context → module breakdown → publication checkpoints)
    ↓
Module Lesson (spec → belt system → executable notebook)

+ Revision Mode (update any artifact with cascade awareness)
```

---

## Fractal Concept Loop (Core Structural Principle)

**Every concept, at every zoom level, runs the same four-stage loop: DO → NOTICE → CODE → NAME.**

This is not a narrative suggestion — it's a structural requirement. The loop applies recursively: courses are made of arcs, arcs of modules, modules of sections, sections of **concept primitives** — and every concept primitive gets the full cycle.

### The Loop

| Stage | What Happens | Modality |
|-------|-------------|----------|
| **DO** | Experience it. Hear it, see it, interact with it. No labels yet. See `scaffold-pass` for the **designed failure variant**. | All available senses |
| **NOTICE** | Guided observation. "What did you notice?" Pattern recognition prompts. | Reflective |
| **CODE** | Build/modify/express. Change parameters, break it, make something with it. | Tactile/code |
| **NAME** | Now formalize. Give it its proper name, connect to theory, define it. | Symbolic |

### Concept Primitives

A **concept primitive** is the smallest unit of understanding where confusion is possible. Not "what has a name" but "what could go wrong in someone's head."

**Decomposition heuristic**: Keep asking "could someone be confused about a piece of this?" until the answer is no. That's your base case.

**Examples:**
- "A whole step skips one key" — primitive (you could think it means skip two)
- "E→F has no black key between them" — primitive (you could assume all white keys are equally spaced)
- "The W-W-H-W-W-W-H pattern defines major" — NOT primitive. Decompose into: what W means, what H means, why that specific sequence, what happens if you change one
- "Multiplying by a weight makes something count more" — primitive
- "Weights should sum to 1" — primitive (you could think any weights work)
- "A weighted average" — compound, built from the two primitives above

### Decomposition in Outlines

Before planning the loop for a section, **decompose** it into confusion-primitives:

```
Section: Major Scales
  Decomposition:
    - "notes have distances between them" (foundational, may already be earned)
    - "some distances are bigger than others" (half vs whole)
    - "a specific distance pattern makes it sound 'major'" (the sequence)
    - "the same pattern starting on any note gives you a new major scale" (transposition)

  Each primitive → DO → NOTICE → CODE → NAME
  Each primitive → sensory projection (which modalities?)
  Primitives chain: each one builds on the previous
```

**Skip mechanism**: If a primitive is already earned from a prior module, reference it and move on. No redundant loops. Track earned primitives across modules the same way jargon-earning is tracked.

### Sensory Projection Matrix

Every concept primitive must be projected into **at least 2 available modalities**. Plan this explicitly in the outline:

| Modality | Music Implementation | Math/ML Implementation |
|----------|---------------------|----------------------|
| **Visual** | SVG diagrams, p5.js waveforms, circle/keyboard viz, animations | Plots, geometric diagrams, FuncAnimation, Plotly 3D |
| **Auditory** | Tone.js synthesis, TidalCycles patterns, Strudel embeds, audio playback | Data sonification, audio feedback on convergence, "sound of a distribution" |
| **Tactile/Code** | Live coding, keyboard interaction, sliders, parameter knobs | ipywidgets, parameter tuning, "build a toy" exercises, code cells |

**Per-primitive planning format:**

```
Primitive: "some distances are bigger than others"
  DO:    hear C→D then hear E→F (auditory). see gaps on keyboard SVG (visual)
  NOTICE: "one jump skips a key, the other doesn't. what's different?"
  CODE:  slider for step size in semitones, hear + see the result (tactile + auditory + visual)
  NAME:  "whole step = 2 semitones. half step = 1 semitone."
  Modalities: auditory ✓ visual ✓ tactile ✓
```

### Fractal Recursion Across Zoom Levels

The loop applies at every level of the curriculum:

| Level | Unit | Loop Application |
|-------|------|-----------------|
| **Course** | Arc | Each arc has a DO (taste demo), NOTICE (patterns), CODE (build), NAME (formalize) |
| **Arc** | Module | Each module motivates → implements → verifies → names |
| **Module** | Section | Each section opens with experience, ends with formalization |
| **Section** | Concept primitive | Each primitive gets the full DO → NOTICE → CODE → NAME cycle |

The section level is where the loop is **mandatory and explicit**. Higher levels emerge naturally from well-structured sections.

---

## Outline-First Workflow (Module Generation)

**Critical**: Don't generate notebooks directly from arc syllabi. The arc syllabus is too high-level. Instead, use an **outline-first workflow**:

```
Arc syllabus (high-level spec)
    ↓
Riff with user (war stories, scope, conceptual ordering)
    ↓
Detailed narrative outline (ready-to-generate artifact)
    ↓
User approves/tweaks outline
    ↓
Generate notebook from outline
```

### What Makes an Outline "Ready to Generate"

A ready outline has:

1. **War stories linked**: Origin story → Story A → Story B → The Turn. Each story builds on the last.

2. **Jargon-earning order**: Every technical term is earned before it's used. Track this explicitly:
   | Term | Introduced | Earned By |
   |------|------------|-----------|
   | treatment/control | Section X | "Group A/B" intuition first |

3. **Section-by-section thought process**: Each section has:
   - **Thought process**: The question the reader is asking
   - **Decomposition**: Concept primitives in this section (smallest units where confusion is possible)
   - **Per-primitive loop plan**: For each primitive — DO (experience), NOTICE (observe), CODE (build/modify), NAME (formalize)
   - **Sensory projection**: Which modalities each primitive uses (visual, auditory, tactile/code — minimum 2)
   - **Scenario**: Concrete example that motivates the concept
   - **Concept**: The formal idea (introduced AFTER scenario)
   - **Implementation**: What they build
   - **Interactive cell**: What they run and play with
   - **Insight**: The "aha" moment
   - **Bridge**: How this connects to the next section
   - **Earned primitives**: Which primitives the reader now owns (tracked for skip mechanism in later sections)

4. **Continuity threads explicit**: A table showing From → To → Thread for every transition.

5. **Scope boundaries**: What we cover, what we explicitly DON'T cover (and where it goes).

### Exemplar

See `examples/module-0.2-outline.md` for a complete example of a ready-to-generate outline.

### The Riffing Phase

Before producing the outline, riff with the user:

1. **War story discovery**: "Do you have a real incident where this concept would have helped?"
2. **Scope negotiation**: "What's the start state? End state? What do we defer?"
3. **Conceptual ordering**: "What order makes narrative sense vs textbook sense?"
4. **Jargon inventory**: "What terms need to be earned? What can we assume?"

This is collaborative. The outline emerges from conversation, not from the arc syllabus alone.

---

## Pipeline Integration

This skill defines core pedagogy. Downstream skills handle specialized concerns:

```
lesson-generator (this skill: pedagogy, voice, zoom levels, belt system)
    → outline-writer (narrative outlines, starting state, war stories)
    → notebook-builder (mechanical .ipynb generation)
    → scaffold-pass (designed failures, skeleton-first, accumulation artifacts, reading strategy, troubleshooting)
    → visual-pass (static diagrams, animations, Manim, expected output, before/after)
    → engagement-pass (Plotly, ipywidgets, concept maps, video embeds, build-a-toy)
    → assessment-generator (6-tier evaluation, Socratic follow-ups, misconception log)
```

All skills share conventions from `_educational-suite-conventions.md`.

---

## Mode Detection

Detect the appropriate mode from user input:

**Revision mode** — triggered by update language:
- "Update [artifact] to..."
- "Add [content] to [artifact]"
- "Remove [content] from [artifact]"
- "Fix [issue] in [artifact]"
- "The [artifact] needs..."

→ See [Revision Mode](#revision-mode) section

**Generation mode** — triggered by creation language (see below)

## Zoom Level Detection (Generation Mode)

Detect the appropriate level from user input:

**Course level** — triggers elicitation:
- "Design a curriculum for..."
- "I want to learn..."
- "Create a course on..."
- "Help me build a learning path for..."

**Arc level** — reads course context:
- "Generate arc 2 syllabus"
- "Break down the Bayesian inference arc"
- "Create the syllabus for [topic]"

**Module level** — reads arc context:
- "Generate the module 0.1 notebook"
- "Create a lesson on [topic]"
- "Turn this outline into a notebook"
- "Generate arc 0, module 1 lesson"

---

# ZOOM LEVEL 1: Course Design

## Elicitation Protocol

Course design begins with structured discovery. Run through these five dimensions:

### Dimension 1: IDENTITY — Who is this person?

Map their cognitive profile, not demographics:

**Questions to ask:**
- What do you already know well? (anchors for new concepts)
- What have you tried to learn before that didn't stick? Why?
- When you learn something new, what makes it "click"?
  - Seeing it visually
  - Building something with it
  - Understanding the math/theory
  - Connecting to something familiar
  - Teaching it to someone else
- How do you know when you've really learned something vs just recognized it?

**Extract:**
- Learning style (visual/kinesthetic/formal)
- Prior knowledge anchors (what to connect new concepts to)
- Failure modes (what causes them to disengage)

### Dimension 2: DESTINATION — What can they DO after?

Not "understand X" — concrete capabilities:

**Questions to ask:**
- Describe a project you want to be able to build after this.
- If someone challenged you in 3 months, what would you want to demonstrate?
- What would make you say "I'm now the kind of person who can ___"?
- Is there a specific artifact you want to ship? (paper, library, app, job)

**Extract:**
- Capability checklist (specific skills)
- Capstone vision (concrete project)
- Identity shift (who they become)

### Dimension 3: TERRAIN — What's the landscape?

Discover what they don't know they don't know:

**Questions to ask:**
- What topics do you think you need to learn? (their mental model)
- What feels scary or intimidating about this domain?
- Are there specific tools/frameworks you need to use?
- What adjacent domains do you already know? (for transfer)

**Extract:**
- Perceived vs actual prerequisites
- Emotional blockers
- Transfer opportunities from adjacent knowledge

### Dimension 4: CONSTRAINTS — What's the box?

**Questions to ask:**
- Time: How many hours/week? Any hard deadlines?
- Energy: When are you sharpest? Long blocks or short bursts?
- Environment: What tools do you have? (GPU, specific stack)
- Accountability: Self-paced? Mentor? Cohort? Deadline?
- Non-negotiables: Must include? Must avoid?

**Extract:**
- Time budget (hours/week, session length)
- Energy pattern
- Hard constraints

### Dimension 5: ARC — What shape should the journey take?

**Questions to ask:**
- Build toward one big capstone, or many small wins along the way?
- Linear progression or spiral (revisit topics with more depth)?
- How much "why" vs "how"? (theory vs practical ratio)
- When stuck, push through or skip and return later?
- How do you feel about optional "rabbit hole" sections?
- What do you want to publish along the way? (forces articulation)

**Extract:**
- Curriculum shape (linear/spiral/modular)
- Depth preference
- Escape hatch strategy
- Publication goals

## Elicitation Style

- Ask 2-3 questions at a time, not all at once
- Reflect back what you heard before moving to next dimension
- It's OK if answers are vague — probe deeper on what matters
- Watch for implicit constraints (e.g., mentions of ADHD → add escape hatches)
- Total elicitation: 5-10 exchanges, not an interrogation

## Output: Curriculum Brief

After elicitation, produce this structured artifact:

```yaml
# Curriculum Brief: [Title]
generated: [date]

learner_profile:
  identity:
    anchors: [list of prior knowledge to connect to]
    learning_style: [visual-first | kinesthetic | formal | mixed]
    failure_modes: [what causes disengagement]
    strengths: [what they're good at that we can leverage]
    neurodivergence:
      type: [if disclosed]
      implications: [accommodations]

destination:
  outcomes:
    - "Can [specific capability 1]"
    - "Can [specific capability 2]"
    - "Can [specific capability 3]"
  capstone: "[concrete project/artifact description]"
  identity_shift: "I am someone who can [new identity]"
  publication:
    - "[what they want to publish, for whom]"

terrain:
  perceived_gaps: [what they think they need to learn]
  actual_gaps: [what they actually need, based on destination]
  transfer_from: [adjacent knowledge to leverage]
  emotional_blockers: [fears, intimidation points]

constraints:
  time:
    hours_per_week: [number]
    session_length: [preferred session duration]
    best_time: [morning/evening/variable]
  environment:
    hardware: [GPU, RAM, etc.]
    stack: [languages, frameworks, tools]
  accountability: [self-paced | mentor | cohort | deadline]
  non_negotiables:
    must_include: [list]
    must_avoid: [list]

arc:
  shape: [linear | spiral | modular]
  theory_practice_ratio: [e.g., 20/80]
  capstone_driven: [true | false]
  escape_hatches: [true | false]
  optional_depth: [true | false]
  dopamine_strategy: [how to maintain engagement]

structure: arcs
```

## From Brief to Course Map

Analyze the brief to produce the course structure:

1. **Gap Analysis**: Compare current state (anchors) to destination (outcomes)
2. **Dependency Mapping**: What must come before what? (arcs can run concurrently if independent)
3. **Scope Fitting**: Given constraints, what's the right number of arcs?
4. **Arc Application**: Apply the chosen shape — arcs are completion-gated, not time-gated
5. **Publication Placement**: Where are the publishable artifacts?
6. **Implementation Targets**: What real code ships from each arc?

### Course Map Format (README.md for syllabus/)

```markdown
# [Course Title]

> [Design principles, AuDHD optimizations if applicable]

## The Map

[Mermaid flowchart showing arc dependencies — arcs can be concurrent]

## Arc Overview

| Arc | Title | Prerequisites | Key Deliverables |
|-----|-------|--------------|-----------------|
| 0 | [Title] | None | [deliverables] |
| 1 | [Title] | None | [deliverables] |
| 2 | [Title] | 0, 1 | [deliverables] |
| ... | ... | ... | ... |

## Publication Cadence

[Types of publications, audiences, cadence]

## Lineage

[What prior curriculum versions this absorbs, if any]
```

---

# ZOOM LEVEL 2: Arc Syllabus

## Input Context

Read the course-level context:
- Curriculum brief (learner profile, constraints, arc)
- Course map (where this arc fits, dependencies)
- Adjacent arcs (what comes before/after, what can run concurrently)

## Arc Syllabus Structure

Each arc file follows this template:

```markdown
# Arc N: Title

**Destination**: [what you can do when this arc is complete]
**Prerequisites**: [which arcs must be complete]
**Estimated sessions**: [range, not calendar time]

## The Map (mermaid flowchart of modules within arc)

## Modules
### Module N.1: Title

> *[Absorbed from ... if consolidating prior content]*

- **Motivation** (visual/scenario/analogy — fires the start engine)
- **Implementation** (build it in code — what specifically)
- **Theory backfill** (read the math that explains what you built)
- **Exercises** (at least 1 designed to produce a publishable artifact, marked [PUBLISH])
- **[OPTIONAL DEPTH]** rabbit holes (for hyperfocus sessions)

### Module N.2: Title
[repeat pattern]

## Publication Checkpoints

| # | Artifact | Type | Audience | Template |
|---|----------|------|----------|----------|
| 1 | [title] | [tweet/tutorial/code/HN post/research] | [who] | [which exercise → edit → publish] |

## Implementation Targets
- **buildlog**: [specific files/features]
- **other**: [if applicable]

## Resources (books, videos, links — specific chapters/sections per module)
```

## Arc Design Principles

- **Completion-gated**: An arc is done when you can do the thing, not when time runs out
- **Modules are sequential within an arc**: Module N.2 depends on N.1
- **Build first, theory second**: Every module starts with implementation
- **Publication as forcing function**: At least 2 publication checkpoints per arc
- **Implementation targets are real**: Exercises produce code that ships
- **Motivation hooks**: Each module starts with something that fires the start engine
- **Concurrency**: Independent arcs (e.g., Arc 0 and Arc 1) can run in parallel

---

# ZOOM LEVEL 3: Module Lesson (Notebook Generation)

## The Belt System

Notebooks are organized into **belts** that represent depth levels. Each belt is additive — higher belts include everything from lower belts.

| Belt | Layers | Content | Self-Contained? |
|------|--------|---------|-----------------|
| **Core** | L0 + L1 + L2 | Problem + Intuition + Code | Yes |
| **Depth** | L3 + L4 | CS Speak + Math Formalism | Requires Core |

**File structure**:
```
notebooks/
  arc-0-probabilistic-foundations/
    module-0.1-taste-demo/
      0.1-taste-demo-core.ipynb       # L0 + L1 + L2 (main path)
      0.1-taste-demo-depth.ipynb      # L3 + L4 (extension)
      hero-intro.png
    module-0.2-probability-counting/
      0.2-probability-counting-core.ipynb
      0.2-probability-counting-depth.ipynb
  supplements/                         # Generated on-demand
    prereq-bayes-theorem.ipynb
    prereq-big-o-notation.ipynb
```

### Layer Definitions

| Layer | Name | Content | Voice |
|-------|------|---------|-------|
| **L0** | Problem/Motivation | Real scenario, why this matters | Narrative, engaging |
| **L1** | Intuition | Analogies, anchors, visual metaphors | Peer ("Let's...") |
| **L2** | Code + Viz | Runnable demos, plots, exercises | Peer ("Let's...") |
| **L3** | CS Speak | Terminology, complexity, patterns | Internal monologue |
| **L4** | Math Formalism | Definitions, theorems, proofs | Internal monologue |

## Input Context

Read the arc-level context:
- Arc syllabus (module spec, objectives, exercises, implementation targets)
- Learner profile (from curriculum brief)
- Position in arc (early modules = more scaffolding, late = more independence)
- Publication checkpoints (is this module's exercise a publication draft?)

## Cumulative Problem Thread

**Critical**: Problems should build on each other. Each problem uses output from the previous problem.

**Good**:
```
Problem 1: Load the data → creates `data` variable
Problem 2: Extract hotel info → uses `data`, creates `hotels`
Problem 3: Filter by amenity → uses `hotels`, creates `filtered`
Problem 4: Export to CSV → uses `filtered`
```

**Bad**:
```
Problem 1: Unrelated tensor exercise
Problem 2: Different unrelated exercise
Problem 3: Another standalone exercise
```

When designing notebooks, spend time crafting a compelling problem thread that:
1. Has a real, relatable scenario
2. Builds cumulatively
3. Ends with a tangible artifact
4. Connects to the arc's implementation targets where possible

## Voice & Tone

### Core Notebooks (L0-L2): Peer Voice
```markdown
Let's figure out how to track belief about each rule. We need something that
can represent "I'm 80% confident this rule helps" and update as we get feedback.

Here's the situation: you have 20 rules, and users keep reinforcing or
contradicting them. How do we keep score?
```

### Depth Notebooks (L3-L4): Internal Monologue Voice
```markdown
I need a distribution that updates cleanly with binary feedback. The Beta
distribution is conjugate to Bernoulli, so the posterior stays in the same
family. This means updates are O(1) — just increment α or β.
```

## Narrative Voice

The target voice blends three registers:

### Professorial clarity (Bialik/Susskind register)
Open with vivid, concrete scenarios that create genuine curiosity. Weave history and real incidents into explanations. Use "please read carefully, it will pay off" energy — the professor who respects your time but insists on rigor. Numbered steps for multi-part reasoning. "Putting It All Together" recaps after complex sections.

### Extreme handholding (Downey register)
Compute first, name second. Never assume the reader remembers what happened three problems ago — recap aggressively. Every new concept gets: what it is, why we need it, what it connects to. Pose questions, then answer them. "Why real numbers? Why [0,1]?" — always explain the WHY, not just the what.

### Personality (learner's own register)
Irreverent, direct, occasionally profane (calibrated — not gratuitous). "The fuck is salience, even?" energy. Custom nomenclature gets flagged as custom: "We made this name up. It's not jargon. We just want to feel smart." Concepts before formulas, always: "We have three numbers. We need one number. These aren't equally important. So multiply each by how important it is and add them up."

### Voice rules
- **Recap between problems**: Students do not remember what happened 3 problems ago. Every problem starts with a 2-3 sentence recap of where we are, what we have, and what we're about to do.
- **Explain the WHY for every design choice**: Why float? Why [0,1]? Why not integers? Why a class? Never let a design decision go unexplained.
- **Custom nomenclature flagging**: When we invent a name (like "salience scorer"), explicitly say it's made up. "This is our name for it. You won't find this in a textbook."
- **Concept-first formula introduction**: Before any formula, build the concept in plain English with a concrete example. The formula should feel like shorthand for what you already understand.
- **Theory backfill is substantial**: Not a paragraph — a full section. Explain concepts (linearity, independence) from scratch with intuition, examples, and visuals. Show how assumptions break down. THEN say "Module N.M builds this out."

## Narrative Flow Principles

These principles govern how concepts are introduced in every notebook. The goal is cognitive tension before framework, code before formula, recognition before naming.

### 1. Story-first opening

Every notebook opens with a concrete problem or incident, not abstract theory. The reader should feel cognitive tension ("this is wrong" or "how would I fix this?") before any framework is introduced. The opening should be a specific, real scenario — not a hypothetical.

**Pattern**: Describe an incident → show the broken output → let the reader feel the wrongness → THEN begin building the fix.

### 2. Code-before-formula rule

Mathematical notation appears ONLY AFTER working code demonstrates the concept. The sequence is always:

```
compute it → verify it → name it
```

Never: "Here's the formula. Now let's implement it." Always: "Here's what we just computed. That has a name: [formula]."

### 3. Single-example-first

Introduce concepts with ONE concrete example before building the full dataset. The reader should understand the problem on one case before seeing ten. This prevents "wall of data" paralysis and lets the reader build intuition incrementally.

**Pattern**: Show one failing case → build the fix for that one case → THEN expand to the full dataset.

### 4. Discovery order over logical order

Problems can appear in the order the reader discovers concepts, not the order they'd appear in a textbook. For example, vocabulary matching before building the test suite — because you need to feel the problem before constructing systematic tests.

The reader's curiosity drives the sequence, not taxonomic completeness.

### 5. Formula emergence

Weighted combinations, probability rules, Bayes' theorem, etc. should feel *recognized*, not *introduced*. The reader has already been computing the thing; the formula just names what they built.

**Pattern**: Build all components → combine them informally ("weighted average — you've done this since GPA") → THEN show the formula → reader thinks "oh, that's just what I already did."

### 6. Companion text callouts

Reference companion texts (ThinkBayes2, ThinkStats, Blitzstein, etc.) AFTER the reader has built something, as "go deeper" pointers. Never as prerequisites. Place them in callout blocks after verification cells.

```markdown
> **Go deeper**: You just built a weighted linear combination. For the probability
> foundations underneath this: ThinkStats Ch 1-2 (exploratory data analysis),
> ThinkBayes Ch 1 (computational Bayesian thinking), Blitzstein Ch 1-2 (formal
> probability framework).
```

### 7. Transition pattern

Use RECAP → PROBLEM RESTATEMENT → NEW APPROACH between sections. Never jump to a new concept without bridging from the previous one.

**Pattern**:
```markdown
[What we just showed] works, but [specific failure case]. Entry N [describes the
failure]. We need to check [new dimension].
```

### 8. Interludes as engagement hooks

**Interludes** are mid-notebook deep-dives that break up the main flow. They're used when a concept deserves more than a paragraph but isn't part of the main problem thread. Format: `### Interlude: [Topic Question]`

**When to use interludes:**
- Explaining a prerequisite concept (Spearman correlation, why floats, what's a falsifiable claim)
- Giving historical/motivational context
- Building intuition for something abstract
- Teasing future content without derailing the current thread

**Interlude structure:**
1. **Hook question**: "How do you measure agreement?" not "Spearman Correlation"
2. **Build from scratch**: Don't assume they know the prerequisite — explain Pearson before Spearman
3. **Concrete examples**: Use numbers, show the computation
4. **Visual payoff**: End with a plot they can run and inspect
5. **Bridge back**: Connect to the main thread ("Now that we can measure agreement, let's test our scorer")

Interludes are high-engagement sections. They should be *fun* — the reader chose to read them, so reward that choice with clarity, personality, and interactive content.

### 9. Interactive visualization cells

Include "run this, play with the plot" cells throughout. These are code cells that:
- Produce a visualization the reader can interact with
- Have tunable parameters (sliders, different inputs to try)
- Show something surprising or instructive
- Require NO work from the reader — they just run it and look

**Pattern:**
```python
# Play with this: try changing `n_samples` or `noise_level`
n_samples = 100
noise_level = 0.1

# [visualization code]
plt.show()

# What do you notice when noise_level > 0.5?
```

These cells are engagement anchors. Place them:
- After building up to a concept (payoff)
- Before asking the reader to implement something (motivation)
- In interludes (always)

### 10. Module threading

Modules aren't standalone — they form a **running example** that evolves across the arc. The artifact from Module N becomes the context for Module N+1.

**Threading rules:**
1. **End with an open question**: Module 0.1 ends with "the weights are vibes" — that's the hook for 0.2
2. **Open with the previous artifact**: Module 0.2 opens with the SalienceScorer from 0.1
3. **Extend, don't replace**: Each module adds to the running example, doesn't start fresh
4. **Make the connection explicit**: "Remember the SalienceScorer? We claimed ρ > 0.8. But 10 examples. Is that real?"

**Threading in war stories:**
When a module has multiple war stories, link them:
- Story A introduces the context (we built X)
- Story B shows what went wrong when we used X naively
- The bridge explains how B exposes gaps in our understanding from A

Example threading for Module 0.2:
- Story A: "We have the SalienceScorer from 0.1. We ran an A/B test on updated scoring rules."
- Story B: "The test 'worked' — 3 out of 5 passed. We shipped. A month later, metrics tanked."
- Bridge: "How surprised should we have been by 3/5? We need probability foundations."

### 11. Falsifiable claims pattern

Every scorer/model/approach needs a **falsifiable claim** — a statement specific enough to be wrong.

**Pattern for introducing falsifiable claims:**
1. Build the thing first (don't front-load the claim)
2. Ask: "How do we know this is good?"
3. Acknowledge: "Right now, vibes. That's not enough."
4. Introduce the claim: "Here's what would make us wrong: [specific threshold]"
5. Tease the future: "Later (Module N.M) we'll learn to test this rigorously"

**Falsifiable claim format:**
```markdown
**Falsifiable claim**: [Metric] > [threshold] on [dataset].

If we fail this, we recalibrate.
```

**The promise**: Tell the reader they're going to learn to defend their decisions with math. Hypothesis testing, confidence intervals, the works. But gently — don't scare them off. The energy is "you'll have the tools to prove you're right" not "there's a lot of scary math ahead."

### 12. Visual hooks for AuDHD engagement

**Critical**: Every 2-3 markdown cells MUST be followed by a visual hook — either a plot, a mermaid diagram, or an interactive cell. Text-heavy sections without visual breaks cause attention collapse.

**Types of visual hooks (in order of preference):**

1. **Matplotlib/Seaborn plots**: Bar charts, line plots, scatter plots. Use color intentionally (`#27ae60` for good, `#e74c3c` for bad, `#3498db` for neutral). Always include annotations that explain the key insight.

2. **Interactive tinkering cells**: Code that produces output the reader can modify. Include comments like `# Try changing this value` or `# What happens when n > 100?`

3. **Mermaid flowcharts**: For processes, loops, decision trees. Keep them simple — 5-7 nodes max.

4. **Tables with visual patterns**: When showing data, highlight the pattern with formatting or follow with a plot.

5. **ASCII diagrams**: Last resort, but better than no visual.

**Placement rules:**
- After every story section (war story, setup, etc.) — plot showing the problem
- After every concept introduction — plot showing the concept in action
- Before asking the reader to implement — plot showing what they're building toward
- After every "celebration" moment — plot showing the success

**Plot minimum per section:**
- Setup/origin story: 1 plot showing the chaos/problem
- Each major concept: 1 plot showing the concept working
- Celebration moments: 1 plot showing dynamics/improvement
- The Turn: 1 plot showing why the naive approach failed

**Never go more than 3 cells without something visual.** If you're writing 4 markdown cells in a row, you've failed. Add a plot, add a diagram, add an interactive cell.

### 13. Video Embed Placement

Embed curated YouTube videos as post-concept reinforcement. Videos *complement* code — they never replace it.

**Sequence**: Build → Verify → Video → Name. The reader earns the concept in code first, then sees it from a different angle.

**Rules**:
- Max 1 video per major section; 2-4 per core notebook total
- Place in its own markdown cell with a 1-2 sentence contextual intro
- Reference `video-index.md` for Arc 0 mappings (specific video IDs per module/section)
- Use `embed_video()` helper from `interactive-templates.md`
- Never use a video as the *introduction* to a concept
- Include `start` timestamp if the relevant part begins after the first minute

**Anti-pattern**: "Watch this video to learn about X" then repeating what the video said. The video should add a *different angle*.

### 14. Interactive Plot Requirements

Use Plotly for plots where hovering, rotating, or filtering adds value. Stay matplotlib for simple 2D comparisons.

**MUST be Plotly**:
- Scatter plots where individual points carry context (entry index, description, computed values)
- 3D surfaces (parameter spaces, loss landscapes, scoring surfaces)
- Animated parameter sweeps (distribution shape changes, convergence)
- Distribution galleries where the reader switches between distributions

**Stay matplotlib**:
- Simple 2D line/bar comparisons
- FuncAnimation internals (matplotlib only)
- Hero-adjacent simple plots
- Plots primarily for screenshot/export

**Conversion heuristic**: "If the reader would benefit from hovering, rotating, or filtering → Plotly"

**Style**: Use consistent color palette (`#2196F3`, `#FF9800`, `#4CAF50`, `#E91E63`, `#9C27B0`). Always include `fig.update_layout(template='plotly_white')`. Hover text must be *useful* — not just coordinates.

See `interactive-templates.md` for Plotly scatter, bar, 3D surface, and animated sweep templates.

### 15. Concept Maps

Every core notebook opens with an arc progress map after imports (Cell 3).

**Arc progress map** (required):
- Shows all modules in the current arc as a horizontal chain
- Highlights the current module (blue, larger), completed modules (green), future (gray)
- Hover shows module description
- Uses networkx → plotly for interactivity
- Template: `arc_progress_map()` from `interactive-templates.md`

**Concept dependency DAG** (optional):
- For modules with complex prerequisites (0.4+)
- Shows which concepts from prior modules feed into this one
- Keep under 12 nodes

**Arc 0 module titles for the map**:
```python
ARC_0_MODULES = [
    "Taste Demo", "Probability & Counting", "Distributions & Beta Priors",
    "Bayesian Updating", "Hypothesis Testing", "Bootstrap CIs",
    "Thompson Sampling", "Ship It"
]
```

### 16. "Build a Toy" Exercise Pattern

At least 1 per core notebook, in addition to standard exercises. These are the dopamine payoff — the reader constructs something *interactive*, not just fills in a function.

**Structure**:
1. **Scenario**: A concrete problem that motivates building the toy
2. **Components given**: Starter code, helpers, data — everything except assembly
3. **Task**: Wire components into something interactive (widget + plot, simulator, explorer)
4. **Success criteria**: Specific, verifiable outcomes
5. **Extensions**: Optional enhancements for hyperfocus sessions

**Examples by module**:
- **0.1**: Weight explorer — 3 sliders (w_l, w_s, w_o), live Spearman ρ display
- **0.2**: A/B test simulator — sliders for n_trials, p_treatment, p_control + "Run" button
- **0.3**: Prior elicitation tool — "I think X works Y%, ±Z%" → Beta params + plot
- **0.4**: Bayesian updating dashboard — feed observations, watch posterior evolve
- **0.5**: Hypothesis testing calculator — input data, see p-value + effect + power
- **0.6**: Bootstrap CI explorer — method picker (percentile, BCa), see CIs change
- **0.7**: Bandit playground — multi-arm Thompson vs UCB vs ε-greedy with regret tracking

**Quality bar**: The toy must be genuinely useful, interactive (widgets), and require understanding the module's concepts to assemble. "Call these three functions in order" is not a build-a-toy exercise.

See `engagement-patterns.md` for full pattern details.

### 17. Animation Patterns

Use `FuncAnimation` → `HTML(anim.to_jshtml())` for concepts involving evolution over time.

**Use for**:
- Bayesian posterior updating (prior → data → posterior step by step)
- Convergence (sample mean → true value as n grows)
- Monte Carlo buildup (points accumulating, estimate converging)
- Distribution shape evolution (Beta morphing as α, β change)

**Placement**:
- Always show the static/final version first ("Here's where we end up")
- Then the animation ("Now let's watch how we get there")
- Max 1-2 per notebook (expensive to render)

**Template**: See `interactive-templates.md` for `animate_beta_evolution()` and `animate_convergence()`.

**Anti-pattern**: Animating something that doesn't change meaningfully over time. A scatter that adds points one at a time with no pattern emerging is not useful.

### 18. Manim Integration (Future-Ready)

**Status**: Infrastructure available via MCP server. Not yet in generation pipeline.

**Current pattern**: Place `# TODO: Manim animation — [description]` comments where Manim would add value. Include what the animation would show and why.

**Future use cases**:
- Complex geometric derivations (probability spaces, Bayes rectangle)
- Transformation visualizations (matrix operations on distributions)
- Cinematic-quality animations for key concepts (3B1B style)

**Rule**: Use Manim only for what FuncAnimation can't handle. FuncAnimation for data evolution; Manim for geometric/mathematical storytelling.

See `engagement-patterns.md` for full Manim integration details.

## Problem Framing Progression

| Stage | Framing Style | Example |
|-------|---------------|---------|
| Early modules | Explicit step-by-step | "Your task is to: 1. Create X, 2. Call Y, 3. Return Z" |
| Mid modules | Goal + hints | "Extract the hotel info. Hint: each entry has a `hotel` key" |
| Late modules | Goal only | "Create `pruned_data` with only the relevant fields" |

## Visual Markers (No Emoji)

### Section Headers
```python
# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 0: THE PROBLEM
# ═══════════════════════════════════════════════════════════════════════════════
```

### Problem Headers

Problem headers should be narrative and tell a story. Use markdown headers in their own cells, not code-style decorators. The reader should understand the narrative arc from headings alone.

```markdown
## From One Example to a Test Suite
```

### Cell Splitting Rule

**CRITICAL**: Every heading gets its own cell. No cell should contain two headings. If a section has a heading followed by content followed by a subheading, that's THREE cells minimum:

1. Cell: `## Main Heading` + intro paragraph
2. Cell: Content (text, code, whatever)
3. Cell: `### Subheading` + its content

This makes it easy to:
- Reorder sections by dragging cells
- Insert content between sections
- Collapse sections in Jupyter
- Add hero images right after headings

**Bad** (two headings in one cell):
```markdown
## Theory Backfill

Some intro text...

### Linearity

Linearity explanation...

### Independence

Independence explanation...
```

**Good** (each heading in its own cell):
```markdown
[Cell 1]
## Theory Backfill

Some intro text setting up what we'll cover.
```
```markdown
[Cell 2]
### Linearity

Linearity explanation...
```
```markdown
[Cell 3]
### Independence

Independence explanation...
```

### Code Cells
```python
# --- YOUR CODE BELOW ---

# >>> SOLUTION (collapsed by default)
```

### Progress Markers (Minimal)
```python
# Tests pass. Moving on.
```

## Narrative Bookends

### Intro Section

Every notebook starts with a **narrative intro** that is:
- Fun and engaging
- Accurate and insightful
- Humorous with personality
- Sets up the problem scenario
- **Story-first**: Opens with a concrete incident, not abstract framing

Two patterns, depending on whether the module has a real incident to anchor on:

#### Pattern A: War Story (preferred when a real incident exists)

The war story pattern has three beats:

1. **Context**: What were you building? Why? What's the domain? Give enough detail that the reader understands the stakes. (2-3 paragraphs)
2. **The turn**: A dramatic reversal or failure. Something went wrong despite doing everything "right." Create cognitive tension. Use a trope if it fits — the tragedy, the irony, the "surely this will work" followed by "it does not."
3. **The bridge**: What are we going to build to fix it? Define any domain-specific terms (what IS salience? what IS a scorer?). Preview the notebook's deliverable.

The reader should understand: (a) what we're building, (b) why it matters, (c) what went wrong, and (d) what "salience" (or whatever the domain concept is) even means — all before touching code.

#### Pattern B: Scenario (when no war story is available)

```markdown
# ═══════════════════════════════════════════════════════════════════════════════
# INTRO
# ═══════════════════════════════════════════════════════════════════════════════

[HERO IMAGE: Generate with ComfyUI - something visually striking related to topic]

## The Setup

You're the lead data scientist at a hotel booking startup. Your CEO bursts in:
"We need to find family-friendly hotels. Yesterday."

You have a JSON dump from the Amadeus API. 200 hotels. Nested data. Your mission:
extract the ones with pools, babysitting, or kids' clubs, and get them into a
clean CSV before the 4pm investor demo.

No pressure.

**By the end of this notebook**, you'll have a working data pipeline that:
- Loads messy JSON
- Extracts relevant fields
- Filters by criteria
- Exports clean CSV

Let's go.
```

In both patterns, the intro ends with a concrete preview of what the reader will build and a forward-leaning transition ("Let's go." / "Let's see exactly what happened.").

### Outro Section

Every notebook ends with a **narrative outro** that:
- Summarizes what was learned
- Celebrates the achievement (without being corny)
- Bridges to the next module
- Flags if this module's output is a publication draft

```markdown
# ═══════════════════════════════════════════════════════════════════════════════
# OUTRO
# ═══════════════════════════════════════════════════════════════════════════════

## What Just Happened

You took a gnarly JSON blob and turned it into a clean CSV. Along the way, you:
- Navigated nested dictionaries without losing your mind
- Used list comprehensions like a civilized person
- Applied boolean filtering to extract exactly what you needed

## Publication Note

Exercise 3 from this module is a draft for the "contains check takedown" post.
Run an edit pass and it's ready to publish.

## What's Next

In Module 0.2, we build the probability foundations that make this scoring
rigorous instead of hand-wavy.

→ [Module 0.2: Probability & Counting](../module-0.2-probability-counting/0.2-probability-counting-core.ipynb)
```

### Hero Images

Use ComfyUI to generate hero images for intro/outro sections:

```python
# Example prompt for ComfyUI
mcp__comfyui__imagine(
    description="A determined data scientist surrounded by floating JSON brackets and hotel icons, dramatic lighting, digital art style",
    output_path="/path/to/notebooks/arc-0/module-0.1/hero-intro.png",
    style="digital_art",
    quality="standard"
)
```

## Core Notebook Structure

```python
# Cell 1: Metadata (markdown)
"""
# Module 0.1: [Title] — Core

**Arc 0: Probabilistic Foundations** | Module 1 of 8

**Prerequisites**: [Prior modules or "None"]

**Time**: ~[X] minutes

**Implementation target**: [what this builds toward in real code, if applicable]

---

## Learning Objectives

By the end of this notebook, you will be able to:

- [ ] [Objective 1]
- [ ] [Objective 2]
- [ ] [Objective 3]
"""

# Cell 2: Imports (code)
"""
# Provided Code - Do NOT Edit
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from IPython.display import YouTubeVideo, HTML, display, Markdown
from ipywidgets import interact, FloatSlider, IntSlider
import ipywidgets as widgets

plt.style.use('seaborn-v0_8-whitegrid')
%matplotlib inline
"""

# Cell 3+: Intro section (markdown + optional hero image)

# Cell N: Layer 0 - Problem/Motivation (markdown)

# Cell N+1: Layer 1 - Intuition (markdown)

# Cell N+2: Layer 2 - Code + Viz (code cells with problems)
# Each problem:
#   - Problem header (markdown)
#   - Provided code cell (if needed)
#   - Student code cell with TODO
#   - Solution cell (collapsed)
#   - Expected output / assertions

# Cell M: Exercises section
# Mark publication-track exercises with [PUBLISH]

# Cell M+1: Outro section (markdown)

# Cell M+2: Resources (markdown — from arc's Resources section)

# Cell M+3: Next Up (markdown — link to next module)
```

## Depth Notebook Structure

Depth notebooks assume the student has completed the Core notebook.

```python
# Cell 1: Metadata (markdown)
"""
# Module 0.1: [Title] — Depth

**Extends**: [0.1-topic-core.ipynb](0.1-topic-core.ipynb)

**Belt**: Depth (CS Speak + Math Formalism)

---

## Prerequisites

This notebook assumes familiarity with:

### For CS Speak (L3):
- [ ] Big-O notation (O(1), O(n), O(log n))
- [ ] Basic data structure tradeoffs

### For Math Formalism (L4):
- [ ] [Specific prereq 1]
- [ ] [Specific prereq 2]

**Gap detected?** Ask:
> "Generate prereq supplement: [topic]"

I'll create a focused notebook that fills just that gap.
"""

# Cell 2: Layer 3 - CS Speak
# Terminology, complexity, engineering considerations
# Internal monologue voice

# Cell 3: Layer 4 - Math Formalism
# Definitions, theorems, proofs
# Confident "let's fix that" energy for proofs

# Inline prereq callouts where needed:
"""
> **PREREQ CHECK: Bayes' Theorem**
> This section assumes you can apply: posterior ∝ prior × likelihood
> If shaky, ask: "Generate prereq supplement: Bayes' theorem"
"""
```

## Exercise Cell Pattern

Problems use SEPARATE cells for the exercise, solution, and test. This makes it easy to collapse or skip solutions in Jupyter.

**Cell 1: Problem description (markdown)**

````markdown
## From One Example to a Test Suite

[Description of what to do - explicit for early modules, goal-only for late]

Your task:
- [Step 1]
- [Step 2]
- [Step 3]

Hint: [Optional hint for early modules]
````

**Cell 2: Provided code (code)**

```python
# Provided Code - Do NOT Edit
provided_variable = [1, 2, 3, 4, 5]
```

**Cell 3: Student code (code)**

```python
# --- YOUR CODE BELOW ---
def solve_problem_n():
    """
    [Clear docstring with spec]
    """
    # TODO: Implement
    pass
```

**Cell 4: Solution (code — separate cell)**

```python
# --- SOLUTION ---
def solve_problem_n():
    """Solution implementation"""
    return [x * 2 for x in provided_variable]
```

**Cell 5: Test (code — separate cell)**

```python
# Test
result = solve_problem_n()
expected = [2, 4, 6, 8, 10]
assert result == expected, f"Expected {expected}, got {result}"
# Tests pass. Moving on.
```

## Prereq Supplement Generation

When a student requests a prereq supplement:

1. **Elicit current level**: "What do you know about X? Have you seen Y notation?"

2. **Generate focused supplement** at appropriate belt:
   - Core-level (code-focused) for practical understanding
   - Depth-level (math-focused) for rigorous understanding

3. **Link back**: End with "Now return to [notebook], you're ready for [section]"

Supplement structure:
```markdown
# SUPPLEMENT: [Topic] ([Belt] Belt)

**Generated for**: [Source notebook] → [Section] prereq
**Time**: ~[X] minutes

## Why You're Here

You hit a prereq gap. This supplement teaches [topic] at the [belt] level.

## [Content organized by layers appropriate to belt]

## You're Ready

You now understand:
- [Key point 1]
- [Key point 2]

→ Return to [source notebook]
```

## Code Cell Guidelines

- All cells must run in sequence without errors
- Print shapes of tensors, intermediate results
- Prefer explicit over implicit
- Use type hints in function signatures
- Include docstrings for exercise functions
- Solutions in collapsed format (visual box)

## Adaptation Based on Learner Profile

From the curriculum brief, adjust:

- **Visual learner**: More plots, diagrams, animations
- **Kinesthetic learner**: More interactive exercises, building things
- **Formal learner**: Emphasize Depth notebooks, include more proofs
- **AuDHD considerations** (validated patterns from Module 0.1):
  - **Time estimates**: Add to header ("~60-90 minutes")
  - **Clear stopping points**: End each major section with a verification cell that passes
  - **Frequent wins**: Every 2-3 cells should have a "tests pass" moment
  - **Engaging narrative hooks**: War stories that create cognitive tension ("this is wrong!")
  - **Short motivation hooks**: Fire the start engine with "here's why you care" before every section
  - **Mermaid maps**: Arc-level and module-level maps so you always know where you are
  - **Optional depth rabbit holes**: `[OPTIONAL DEPTH]` sections for hyperfocus sessions
  - **Interludes**: Mid-notebook deep-dives that break up the main flow — these are engagement gold
  - **Interactive plots**: "Run this, play with it" cells are dopamine hits
  - **Novelty through personality**: Profanity (calibrated), custom nomenclature, irreverent voice
  - **Visual payoffs**: Every concept builds toward a plot or verification
  - **Recap aggressively**: Assume they forgot what happened 3 cells ago (they did)
- **Math anxiety**:
  - Longer L0-L2 in Core
  - Gentler ramp in Depth
  - "Let's fix that" confidence for proofs

---

# Project Context

## Environment

Typical setup (adjust based on curriculum brief):
- `uv` package manager
- JupyterLab
- Core: numpy, scipy, torch
- Viz: matplotlib, seaborn, plotly, ipywidgets
- ML: sentence-transformers, transformers, hdbscan, umap-learn
- Stats: pymc, numpyro, arviz (Arc 2+)

## Directory Structure

```
aegir/
├── notebooks/
│   ├── arc-0-probabilistic-foundations/
│   │   ├── module-0.1-[topic]/
│   │   │   ├── 0.1-[topic]-core.ipynb
│   │   │   ├── 0.1-[topic]-depth.ipynb
│   │   │   └── hero-intro.png
│   │   ├── module-0.2-[topic]/
│   │   │   └── ...
│   │   └── ...
│   ├── arc-1-linear-algebra-calculus/
│   │   └── ...
│   └── supplements/
│       ├── prereq-[topic].ipynb
│       └── ...
├── syllabus/
│   ├── README.md              ← Course map (arc overview)
│   ├── curriculum-brief.yaml  ← Elicitation output
│   └── arcs/
│       ├── README.md          ← Arc overview + design principles
│       ├── curriculum-brief.yaml
│       ├── arc-0-probabilistic-foundations.md
│       ├── arc-1-linear-algebra-calculus.md
│       └── ...
├── sources/
│   ├── books.md
│   ├── videos.md
│   └── ...
├── wiki/
│   └── ...
├── archive/
│   └── v1-week-based/        ← Preserved original content
└── pyproject.toml
```

## Output Paths

- **Course map**: `syllabus/README.md`
- **Curriculum brief**: `syllabus/curriculum-brief.yaml`
- **Arc overview**: `syllabus/arcs/README.md`
- **Arc syllabi**: `syllabus/arcs/arc-N-[theme].md`
- **Core notebooks**: `notebooks/arc-N-[theme]/module-N.M-[topic]/N.M-[topic]-core.ipynb`
- **Depth notebooks**: `notebooks/arc-N-[theme]/module-N.M-[topic]/N.M-[topic]-depth.ipynb`
- **Supplements**: `notebooks/supplements/prereq-[topic].ipynb`

Support explicit path override: "generate to [path]"

---

# Quality Checklist

## Course Level
- [ ] All five elicitation dimensions covered
- [ ] Curriculum brief is complete and specific
- [ ] Arc sequence has clear dependencies (and concurrency where possible)
- [ ] Each arc has a concrete destination (what you can DO)
- [ ] Publication checkpoints defined per arc

## Arc Level
- [ ] Destination ties to course outcomes
- [ ] Module breakdown is sequential within the arc
- [ ] Each module has motivation → implementation → theory backfill → exercises
- [ ] At least 2 publication checkpoints with type/audience/template
- [ ] Implementation targets are specific (real files, real features)
- [ ] Resources reference specific chapters/sections, not whole books
- [ ] Estimated sessions range is realistic

## Module Lesson (Notebook) Level
- [ ] Compelling problem thread (cumulative, real scenario)
- [ ] All code cells run in sequence
- [ ] Core notebook is self-contained (L0+L1+L2)
- [ ] Depth notebook declares prereqs
- [ ] Narrative intro is engaging and fun
- [ ] Narrative outro celebrates and bridges to next module
- [ ] Publication-track exercises marked with [PUBLISH]
- [ ] Exercises have clear success criteria
- [ ] Solutions provided in collapsed format
- [ ] Visual markers follow style guide (no emoji)
- [ ] Voice matches belt level (peer vs internal monologue)
- [ ] Links to arc's implementation targets where applicable

## Fractal Concept Loop Level
- [ ] Every section has a concept decomposition (confusion-primitives identified)
- [ ] Every concept primitive runs the full DO → NOTICE → CODE → NAME cycle
- [ ] Every concept primitive projects into at least 2 sensory modalities
- [ ] Primitives chain correctly (each builds on previously earned primitives)
- [ ] Earned primitives tracked — no redundant loops for already-earned concepts
- [ ] Skip mechanism used for primitives earned in prior modules (reference, don't re-teach)
- [ ] Sensory projection matrix filled out per section in outline
- [ ] No primitive is "just defined" — every one is experienced before named

---

# REVISION MODE

Revision mode handles updates to existing artifacts without full regeneration.

## Revision Trigger Detection

Detect revision intent from user input:

**Course-level revision:**
- "Update the curriculum to include..."
- "Add an arc on [topic]"
- "Remove the [topic] arc"
- "Reorder arcs to put [X] before [Y]"
- "The learner profile has changed — they now..."

**Arc-level revision:**
- "Update arc N to add a module on [topic]"
- "Split module N.3 into two modules"
- "Move [module] to arc N+1"
- "Change the publication checkpoint to [new target]"
- "Add an exercise on [topic]"

**Notebook-level revision:**
- "Add a section on [concept]"
- "The explanation of [X] needs more intuition"
- "Add an exercise for [skill]"
- "Update the code to use [library/pattern]"
- "Fix the [broken thing]"

## Revision Workflow

### Step 1: Read Current State

Read the artifact being revised and its context:

```
Course revision  → Read: curriculum-brief.yaml, syllabus/README.md, syllabus/arcs/README.md
Arc revision     → Read: arc syllabus, adjacent arcs, course map
Notebook revision → Read: notebook, arc syllabus, learner profile
```

### Step 2: Identify the Delta

Categorize the change:

| Change Type | Description | Cascade Risk |
|-------------|-------------|--------------|
| **Additive** | New content, no existing content affected | Low |
| **Modificative** | Existing content updated in place | Medium |
| **Structural** | Reordering, splitting, merging | High |
| **Subtractive** | Removing content | High |

### Step 3: Plan the Edit

For each change type:

**Additive changes:**
- Identify insertion point
- Check for dependency conflicts (does new content require prerequisites?)
- Draft new content following existing patterns

**Modificative changes:**
- Identify exact scope of change
- Preserve surrounding context
- Maintain consistent voice/style

**Structural changes:**
- Map all affected sections
- Update cross-references
- Recalculate module numbering if applicable

**Subtractive changes:**
- Check for downstream dependencies
- Identify orphaned references
- Confirm removal scope with user if ambiguous

### Step 4: Execute Edit

Apply the minimal change needed. Preserve:
- Existing structure where unchanged
- Cross-references that still apply
- Formatting conventions
- Voice and tone

### Step 5: Flag Cascade Impacts

After editing, report downstream impacts:

```markdown
## Revision Complete

**Changed**: [what was modified]

**Downstream impacts to review**:
- [ ] Arc N+1 references removed content
- [ ] Module 0.3 depends on removed exercise
- [ ] Publication checkpoint no longer aligns

**No action needed**:
- Arc N-1 (independent)
- Modules 0.1-0.2 (no dependencies on changed content)
```

## Cascade Rules by Level

### Course-Level Changes

| Change | Cascades To |
|--------|-------------|
| Add arc | Course map, arc numbering, dependency graph |
| Remove arc | Course map, downstream arc prerequisites |
| Reorder arcs | All arc files (numbering), prerequisite chains |
| Update learner profile | Potentially all notebooks (adaptation) |
| Change publication goals | Publication checkpoints across arcs |

### Arc-Level Changes

| Change | Cascades To |
|--------|-------------|
| Add module | Arc module list, module numbering |
| Remove module | Arc module list, downstream module references |
| Reorder modules | Module numbering, cross-references |
| Change publication checkpoint | Arc publication table, notebook [PUBLISH] markers |
| Update implementation target | Module exercises, notebook code |

### Notebook-Level Changes

| Change | Cascades To |
|--------|-------------|
| Add section | Table of contents (if present), flow |
| Remove section | Cross-references within notebook |
| Update exercise | Test code, success criteria |
| Change imports | All code cells using those imports |
| Fix code bug | Downstream cells depending on output |

## Revision Principles

1. **Minimal diff**: Change only what's necessary
2. **Preserve voice**: Match existing style and tone
3. **Maintain integrity**: Don't break working code or valid references
4. **Flag, don't fix silently**: Report cascade impacts explicitly
5. **Confirm destructive changes**: Ask before removing significant content

## Revision Quality Checklist

- [ ] Read existing artifact before editing
- [ ] Identified change type (additive/modificative/structural/subtractive)
- [ ] Preserved unchanged content
- [ ] Updated cross-references
- [ ] Flagged downstream impacts
- [ ] Tested code still runs (for notebooks)
