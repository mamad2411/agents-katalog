---
name: science
description: Hypothesis-driven investigation using the scientific method. Define goals, form hypotheses, design experiments, measure, analyze, iterate. USE WHEN scientific method, hypothesis, experiment, investigate, debug, diagnose, why is this happening, root cause analysis, test theory.
---

# Science: Hypothesis-Driven Investigation

The scientific method applied to problem-solving. Define goals, form hypotheses, design experiments, execute, measure, analyze, and iterate. The universal algorithm for making progress on any problem.

## Customization

Check for user customizations at:
`~/.augment/USER/SKILLCUSTOMIZATIONS/Science/PREFERENCES.md`

If this file exists, load and apply preferences found there. They override defaults below.

## The Universal Cycle

```
GOAL -------> What does success look like?
   |
OBSERVE ----> What is the current state?
   |
HYPOTHESIZE > What might work? (Generate MULTIPLE)
   |
EXPERIMENT -> Design and run the test
   |
MEASURE ----> What happened? (Collect data)
   |
ANALYZE ----> How does it compare to the goal?
   |
ITERATE ----> Adjust hypothesis and repeat
   |
   +---------> Back to HYPOTHESIZE
```

**The goal is CRITICAL.** Without clear success criteria, you cannot judge results.

## Two Modes

### Mode 1: Quick Diagnosis (Under 15 Minutes)

Use when stuck, when intuition fails, or when you are about to "try random stuff."

**Step 1: State your goal (30 seconds)**
One sentence. What does "fixed" look like?
```
GOAL: [What will be true when this is solved?]
```

**Step 2: Generate hypotheses (60 seconds)**
MINIMUM THREE. If you cannot think of three, you have not thought hard enough.
```
H1: [Most likely cause] - because [evidence/reasoning]
H2: [Second possibility] - because [evidence/reasoning]
H3: [Third possibility] - because [evidence/reasoning]
```
For each, ask: "What would prove this WRONG?"

**Step 3: Rank and test (60 seconds)**
Order by: (Fastest to verify) x (Most likely). Test the top one.

**Step 4: Update and iterate (30 seconds)**
- Hypothesis confirmed --> Fix it, done
- Hypothesis refuted --> Move to next hypothesis
- Inconclusive --> Need more data, design better test

**One-Liner Version:**
"I think [X] because [Y]. If I am wrong, [Z] would be true. Let me check [Z]."

**Exit Criteria:** Problem solved, or 15 minutes elapsed without resolution --> escalate to Structured Investigation.

### Mode 2: Structured Investigation (Hours to Days)

Use when Quick Diagnosis is not enough, multiple systems are involved, or stakes are high.

**Phase 1: Define the Goal** -- Specific outcome, measurable success criteria, constraints, and anti-goals (what you are NOT trying to do). Quality check: Can someone else read this and know exactly when you have succeeded?

**Phase 2: Gather Context** -- What we know (with sources), what we do not know, what has been tried, baseline measurements. Quality check: Did you look for disconfirming evidence?

**Phase 3: Generate Hypotheses** -- Minimum 3, better 5-10 for important problems. Each needs: claim, rationale, evidence for/against, falsification criteria ("WRONG if..."), cost to test, confidence level. Single-hypothesis thinking leads to confirmation bias.

**Phase 4: Design Experiments** -- Minimum Viable Experiments (smallest test that gives meaningful data). For each: method, what you are measuring, success/refutation/inconclusive criteria, duration. Prioritize by (likelihood) x (cost to test).

**Phase 5: Execute and Measure** -- Run experiments, collect data, do not peek prematurely. Record metrics as Expected vs. Actual vs. Delta.

**Phase 6: Analyze Against Goal** -- Compare results to pre-defined success criteria. Determine hypothesis status (CONFIRMED / REFUTED / INCONCLUSIVE). Capture key learnings, surprises, and new questions.

**Phase 7: Iterate** -- Goal achieved: document and done. Promising hypothesis: go deeper. All failed: generate new hypotheses. Need more data: design more experiments. Problem reframed: return to Phase 1.

## Output Format

```markdown
## Investigation Report: [Problem]

**Goal:** [What we were trying to achieve]
**Mode:** [Quick Diagnosis / Structured Investigation]

### Hypotheses Tested
| ID | Hypothesis | Verdict | Confidence |
|----|-----------|---------|------------|
| H1 | [Claim] | CONFIRMED/REFUTED | High/Med/Low |
| H2 | [Claim] | CONFIRMED/REFUTED | High/Med/Low |

### Key Finding
[One sentence: what we discovered]

### Evidence
[Data supporting the finding]

### Resolution
[What we did / what we recommend]

### Learnings
- [Generalizable insight 1]
- [Generalizable insight 2]
```

## Key Principles

1. **Goal-First** -- Define success before starting
2. **Hypothesis Plurality** -- NEVER just one idea (minimum 3)
3. **Minimum Viable Experiments** -- Smallest test that teaches
4. **Falsifiability** -- Experiments must be able to fail
5. **Measure What Matters** -- Only goal-relevant data
6. **Honest Analysis** -- Compare to goal, not expectations
7. **Rapid Iteration** -- Cycle speed matters more than perfect experiments

## Scale of Application

| Level | Cycle Time | Example |
|-------|-----------|---------|
| **Micro** | Minutes | TDD: write test, code, refactor |
| **Meso** | Hours-Days | Feature: spec, implement, validate |
| **Macro** | Weeks-Months | Product: MVP, launch, measure PMF |

## Anti-Patterns

| Bad | Good |
|-----|------|
| "Make it better" | "Reduce load time from 3s to 1s" |
| "I think X will work" | "Here are 3 approaches: X, Y, Z" |
| "Prove I'm right" | "Design test that could disprove" |
| "Pretend failure didn't happen" | "What did we learn?" |
| "Keep experimenting forever" | "Ship and learn from production" |
| Random flailing ("let me try this... nope") | Structured: 3 hypotheses, test fastest first |

## Quick Reference

1. **Goal** -- What does success look like?
2. **Observe** -- What do we know?
3. **Hypothesize** -- At least 3 ideas
4. **Experiment** -- Minimum viable tests
5. **Measure** -- Collect goal-relevant data
6. **Analyze** -- Compare to success criteria
7. **Iterate** -- Adjust and repeat

**The answer emerges from the cycle, not from guessing.**
