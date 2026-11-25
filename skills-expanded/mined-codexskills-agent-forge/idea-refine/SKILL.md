---
name: idea-refine
description: Structured divergent and convergent thinking process to transform raw, vague ideas into sharp, actionable concepts. Integrates SCAMPER, Six Thinking Hats, and multi-cycle divergence/convergence for robust idea development.
---

# Idea Refine

## Overview

Raw ideas are fragile. They come as hunches, half-thoughts, or excited fragments — "what if we did something with AI and spreadsheets?" or "make it feel like a premium experience." Without structure, these decay into vague requirements, scope creep, or generic output.

This skill provides a systematic process for taking raw ideas through cycles of **divergence** (expand possibilities) and **convergence** (narrow to the best option). It combines proven creative methodologies — SCAMPER, Six Thinking Hats, and structured ideation — into a repeatable pipeline.

The output is a concrete, defensible concept with clear rationale, trade-offs documented, and a decision tree showing what was considered and why it was rejected.

## When to Use

| Trigger | Description |
|---------|-------------|
| Vague idea | "I want something like X but different" |
| User feels stuck | "I don't know what direction to go" |
| Too many options | Analysis paralysis, can't choose |
| Creative block | All ideas feel derivative or boring |
| Premature convergence | Team latched onto first idea without exploring |
| Reopening a solved problem | "Let's rethink this from scratch" |
| Innovation requirement | "We need something novel, not incremental" |

**Do NOT use** when: the requirement is already well-defined and specific, the user wants execution not ideation, or the problem is purely technical (known solution exists).

## Process

### Phase 1: Capture & Clarify (Divergent)

Goal: Extract the raw idea without judging or shaping it.

1. Ask the user to state the idea in one sentence, unfiltered.
2. Capture all associated thoughts, feelings, and examples.
3. Ask: "What triggered this idea? What problem were you trying to solve?"
4. Ask: "What's the simplest version of this idea?"
5. Write everything down without editing.

**Output:** Raw idea dump — 20-50 unstructured fragments.

### Phase 2: Diverge — Expand Possibilities

Goal: Generate maximum surface area around the idea.

Run **three divergent loops**, each using a different technique:

#### Loop 1: SCAMPER (7 directions)

Apply each SCAMPER catalyst to the raw idea:

| Catalyst | Questions (pick 2-3 per run) |
|----------|------------------------------|
| **S**ubstitute | What could we replace? Different audience, technology, format, channel? |
| **C**ombine | What if we merged this with another feature, product, or concept? |
| **A**dapt | What existing solution could we modify? What works in a different industry? |
| **M**agnify | What if we made it 10x bigger, faster, louder? What's the extreme version? |
| **P**ut to other use | Who else could use this? What other problem does it solve? |
| **E**liminate | What if we removed the core assumption? What's the minimum version? |
| **R**earrange | What if the order changed? What if users did our job instead? |

For each catalyst, generate 2-3 concrete variations. Minimum 14 variations total.

#### Loop 2: Six Thinking Hats (6 perspectives)

Examine the best 3-5 variations from Loop 1 through each hat:

| Hat | Lens | Questions |
|-----|------|-----------|
| 🎩 White | Facts & data | What do we know? What don't we know? What data exists? |
| ❤️ Red | Emotions & intuition | What does your gut say? How would users feel? |
| ⚫ Black | Risks & caution | What could go wrong? What's the downside? |
| 💛 Yellow | Optimism & value | What's the best case? What's the opportunity? |
| 🌿 Green | Creativity & growth | What new ideas does this spark? What's the twist? |
| 🔵 Blue | Process & control | What have we learned? What's next? |

For each variation, capture 3-5 insights across the hats that feel most relevant.

#### Loop 3: Polarity Mapping

For each surviving variation, identify tensions:

- What's the central trade-off? (e.g., power vs simplicity)
- What happens if we push too far in each direction?
- Where's the sweet spot?

**Output:** 10-20 documented idea variations, each with SCAMPER origin, hat analysis, and polarity map.

### Phase 3: Converge — Filter & Rank

Goal: Reduce to 1-3 viable candidates using structured criteria.

Apply these filters in order:

#### Filter 1: Feasibility (Must-Have)

Can we build this with available time, budget, and skills?

- **High:** Can build now
- **Medium:** Need to learn or acquire something
- **Low:** Requires major investment or unknown technology

Kill all Low feasibility ideas (unless user wants a research phase).

#### Filter 2: Impact (Should-Have)

How much does this move the needle on the user's goal?

- **High:** Directly solves the core problem
- **Medium:** Significant improvement
- **Low:** Marginal or indirect benefit

Kill Low impact ideas.

#### Filter 3: Novelty (Nice-to-Have)

How differentiated is this from existing solutions?

- **High:** Not done before in this context
- **Medium:** Known approach but with a twist
- **Low:** Standard industry pattern

Weight this lower than feasibility and impact. A novel idea that's infeasible is unusable.

#### Filter 4: Confidence Check

For surviving ideas (usually 2-4), test:

- "What would need to be true for this to work?"
- "What's the biggest risk in this direction?"
- "If we ship this and nothing else, is it useful?"

**Output:** Ranked shortlist of 1-3 ideas with filter scores and risk notes.

### Phase 4: Concept Deep-Dive (Convergent)

Goal: Fully flesh out the top candidate.

For the winning idea document:

1. **One-liner:** 15-word description anyone can understand
2. **User story:** "As [persona], I want [capability] so that [outcome]"
3. **Key features:** Bullet list of 3-7 essential capabilities
4. **Success metric:** How we know it works
5. **Key assumption:** The single thing that must be true
6. **Biggest risk:** What could kill this
7. **Minimum test:** Cheapest way to validate the key assumption

### Phase 5: Output & Handoff

Write the final output to a structured document.

## Anti-Rationalization Table

| Temptation | Why It Happens | Why It's Dangerous | What To Do Instead |
|------------|----------------|--------------------|--------------------|
| "Let's just go with the first idea" | It felt exciting in the moment | You missed better alternatives | Force at least 2 SCAMPER loops before deciding |
| "This is too similar to X" | Fear of being derivative | You discard a good, proven approach | "How is this different in implementation?" |
| "We already know what works" | Overconfidence in past experience | Market or context has changed | Run the Six Hats on your assumption |
| "Let's combine ALL the ideas" | Excitement about possibilities | Scope bloat, loss of focus | "If we pick one, which has highest impact?" |
| "The user won't like that approach" | Anticipating rejection | You self-censor before presenting | Include it as an option with trade-offs documented |
| "This needs more research" | Fear of commitment | Perpetual ideation, never ships | "What's the smallest test to validate this?" |
| "The data clearly shows X" | Cherry-picking evidence | Confirmation bias | Apply the Black Hat specifically to your favorite idea |
| "Everyone agrees on this direction" | Groupthink | No one voiced dissent | Assign someone the Black Hat for each candidate |

## Red Flags

1. All generated ideas look like existing products — no novelty
2. Every idea scores Low on feasibility — scope is too ambitious
3. The winning idea is identical to what was rejected in a previous project
4. User rejects every idea but can't articulate why
5. SCAMPER produces no useful variations — the starting idea is too rigid
6. Six Hats analysis is all Yellow (optimism) and no Black (caution)
7. Polarities are ignored — no trade-offs discussed
8. The output is longer than 2 pages — over-engineered

## Verification

- [ ] **At least 10 divergent ideas** generated (minimum 14 from SCAMPER)
- [ ] **SCAMPER** applied with all 7 catalysts, minimum 2 variations each
- [ ] **Six Hats** used on top 3-5 variations
- [ ] **Polarity map** created for each surviving idea
- [ ] **4 filters applied** — feasibility, impact, novelty, confidence
- [ ] **Winner selected** with clear rationale
- [ ] **Top candidate deep-dive** complete with all 7 sections
- [ ] **2-3 runner-ups documented** with why they weren't selected
- [ ] **One-liner** passes the "bar test" (anyone understands in 5 seconds)
- [ ] **Key assumption** is testable in < 1 week
- [ ] **Risks documented** with mitigation strategies

### Output Template

```markdown
# Idea Refinement: [Project Name]

## Raw Idea
[Original one-sentence statement]

## Divergent Exploration
### SCAMPER Variations
| Catalyst | Variation | Brief Description |
|----------|-----------|-------------------|
| Substitute | Variation 1 | ... |
| Combine | Variation 2 | ... |
| ... | ... | ... |

### Top Variations (after Six Hats)
1. **[Variation Name]** — [Key insight from hat analysis]
2. **[Variation Name]** — [Key insight from hat analysis]
3. **[Variation Name]** — [Key insight from hat analysis]

### Polarity Maps
| Variation | Tension | Sweet Spot |
|-----------|---------|------------|
| Variation 1 | Power vs Simplicity | Opinionated but learnable |

## Convergence Results
### Filter Scores
| Idea | Feasibility | Impact | Novelty | Confidence | Decision |
|------|-------------|--------|---------|------------|----------|
| A | High | High | Medium | 9/10 | **Winner** |
| B | Medium | High | High | 6/10 | Runner-up |
| C | Low | Medium | Low | 3/10 | Rejected |

## Winning Concept: [Name]

**One-liner:** [15 words]

**User story:** As [persona], I want [capability] so that [outcome]

**Key features:**
- Feature 1
- Feature 2
- Feature 3

**Success metric:** [Measurable outcome]

**Key assumption:** [What must be true]

**Biggest risk:** [What could kill this]

**Minimum test:** [Cheapest validation]

## Rejected Ideas
| Idea | Rejection Reason |
|------|------------------|
| Idea X | Low feasibility — requires unavailable technology |
| Idea Y | Low impact — doesn't solve core problem |
```

### Decision Tree (for traceability)

```
Raw Idea
  ├── SCAMPER → 14+ variations
  │   ├── Six Hats → 3-5 survive
  │   │   ├── Polarity Maps → tensions documented
  │   │   ├── Feasibility Filter → kills infeasible
  │   │   ├── Impact Filter → kills low-impact
  │   │   ├── Novelty Filter → weights remaining
  │   │   └── Confidence Check → picks winner
  │   └── Runner-ups documented
  └── Deep-dive on winner → ready for spec
```
