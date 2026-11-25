---
name: universal-ai-harness
description: "Universal AI Harness — a meta-framework that wraps any AI model to reduce token waste, ensure spec-driven thinking, maintain persistent memory, and produce calibrated, high-accuracy outputs. Combines BMAD spec-driven methodology, Deep Confidence reasoning, Monte Carlo validation, ReAct execution, and continuous learning. Use for any complex task, decision, or build. Activates on: 'think first', 'harness mode', 'spec-driven', 'BMAD', 'deep reasoning', 'plan before acting', 'structured thinking', 'truth-seeking'."
version: "1.0.0"
tags: ["harness", "meta-framework", "BMAD", "spec-driven", "reasoning", "memory", "monte-carlo", "universal"]
---

# Universal AI Harness

## The Problem This Solves

AI models waste tokens and produce inconsistent results because they:
- Start coding before understanding the problem
- Forget context between sessions
- Don't learn from past successes or failures
- Use the same reasoning approach for every task
- Produce overconfident answers without calibration
- Can't trace how they arrived at conclusions

**The Universal AI Harness** wraps any AI model in a structured framework that:

1. **Stops token waste** — by specifying before executing
2. **Maintains memory** — by persisting knowledge across sessions
3. **Ensures accuracy** — by validating before committing
4. **Learns continuously** — by tracking outcomes and updating beliefs
5. **Adapts reasoning** — by matching the thinking strategy to the task type

---

## The Seven-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    UNIVERSAL AI HARNESS                         │
├─────────────────────────────────────────────────────────────────┤
│  L1: INTAKE      │ Parse request, classify task, assess depth   │
│  L2: MEMORY      │ Query persistent knowledge, check past work  │
│  L3: SPEC        │ Write specification BEFORE any action        │
│  L4: REASON      │ Apply appropriate reasoning framework        │
│  L5: VALIDATE    │ Monte Carlo + MAD debate + confidence score  │
│  L6: EXECUTE     │ Act with full spec, reasoning, validation    │
│  L7: LEARN       │ Store outcome, update knowledge base         │
└─────────────────────────────────────────────────────────────────┘
```

Every task flows through all seven layers. No shortcuts.

---

## Layer 1: INTAKE — Parse and Classify

Before doing anything, understand exactly what you're dealing with.

### Task Classification Matrix

| Task Type | Depth Required | Reasoning Mode | Example |
|---|---|---|---|
| **Factual Query** | Minimal | Direct retrieval | "What does this function do?" |
| **Explanation** | Light | Chain-of-Thought | "Explain how OAuth works" |
| **Debugging** | Medium | ReAct (observe → hypothesize → test) | "Why is this test failing?" |
| **Implementation** | Full | Spec-first → Tree-of-Thought | "Build a user auth system" |
| **Architecture** | Full+ | BMAD multi-agent deliberation | "Design the system architecture" |
| **Decision** | Full | Monte Carlo + MAD debate | "Should we use GraphQL or REST?" |
| **Research** | Variable | Iterative ReAct with memory updates | "What's the best approach for X?" |

### INTAKE Output Format

```
INTAKE ANALYSIS
─────────────────────────────────────────────────────────
Request:     [User's request in one sentence]
Task Type:   [Classification from matrix above]
Depth:       [Minimal / Light / Medium / Full / Full+]
Reasoning:   [Which reasoning mode to use]
Memory Check: [What past knowledge might be relevant?]
Spec Needed: [Yes/No — if Yes, what kind?]
─────────────────────────────────────────────────────────
```

---

## Layer 2: MEMORY — Query Persistent Knowledge

Before reasoning, check what you already know.

### Memory Types

| Type | What It Stores | When to Query |
|---|---|---|
| **Semantic** | Facts, definitions, domain knowledge | Always — "What do I know about this?" |
| **Episodic** | Past experiences, prior conversations | When task resembles past work |
| **Procedural** | How-to knowledge, workflows, patterns | When executing a known task type |
| **Outcome** | What worked/failed in past attempts | Before repeating a similar approach |

### Memory Query Format

```
MEMORY CHECK
─────────────────────────────────────────────────────────
Semantic:    [Relevant facts/knowledge retrieved]
Episodic:    [Similar past tasks and their outcomes]
Procedural:  [Known patterns or workflows that apply]
Outcome:     [Past attempts at similar tasks — what worked/failed]

Memory Confidence: [High/Medium/Low — how reliable is this memory?]
Gaps Identified:   [What I don't know that I need to find out]
─────────────────────────────────────────────────────────
```

### Persistent Knowledge Base Structure

Maintain a structured knowledge file (JSON or Markdown) that persists:

```json
{
  "facts": {
    "domain-name": {
      "fact-id": {
        "content": "...",
        "confidence": 0.95,
        "source": "...",
        "last_validated": "2026-02-20"
      }
    }
  },
  "outcomes": [
    {
      "task_type": "implementation",
      "approach": "...",
      "result": "success|failure|partial",
      "lessons": "...",
      "timestamp": "..."
    }
  ],
  "procedures": {
    "task-type": {
      "steps": [...],
      "success_rate": 0.85,
      "last_updated": "..."
    }
  }
}
```

---

## Layer 3: SPEC — Specification Before Action

**Core principle from BMAD/SDD:** Never write code (or take action) without a specification. The spec is the source of truth.

### When Specs Are Required

| Task Type | Spec Required | Spec Format |
|---|---|---|
| Factual Query | No | — |
| Explanation | No | — |
| Debugging | Light | Hypothesis doc |
| Implementation | **Yes** | PRD → Architecture → Task breakdown |
| Architecture | **Yes** | Full architecture spec |
| Decision | **Yes** | Decision spec with options and criteria |
| Research | Light | Research questions doc |

### Spec Templates

#### Implementation Spec (BMAD-style)

```markdown
# Specification: [Feature/Task Name]

## 1. Goal
[One sentence: what does success look like?]

## 2. Context
[What exists now? What's the starting point?]

## 3. Requirements
### Functional
- [Requirement 1]
- [Requirement 2]

### Non-Functional
- [Performance, security, scalability requirements]

## 4. Constraints
- [Technical constraints]
- [Time constraints]
- [Resource constraints]

## 5. Architecture Decisions
[Key decisions that shape implementation]

## 6. Task Breakdown
1. [Task 1] — [outcome]
2. [Task 2] — [outcome]
...

## 7. Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## 8. Risks & Mitigations
| Risk | Impact | Mitigation |
|---|---|---|
| [Risk] | [H/M/L] | [Action] |
```

#### Decision Spec

```markdown
# Decision: [What are we deciding?]

## Options
1. **Option A:** [Description]
2. **Option B:** [Description]
3. **Option C:** [Description]

## Evaluation Criteria
| Criterion | Weight | Option A | Option B | Option C |
|---|---|---|---|---|
| [Criterion 1] | [1-5] | [Score] | [Score] | [Score] |
| [Criterion 2] | [1-5] | [Score] | [Score] | [Score] |

## Weighted Score
[Calculate and compare]

## Recommendation
[Which option and why]

## Reversibility
[How hard is it to change this decision later?]
```

---

## Layer 4: REASON — Apply the Right Framework

Match the reasoning approach to the task type.

### Reasoning Mode Selection

```
IF task is simple factual lookup:
    → Direct retrieval (no reasoning chain needed)

IF task requires explanation or understanding:
    → Chain-of-Thought (linear step-by-step reasoning)

IF task requires interaction with external systems:
    → ReAct (Thought → Action → Observation loop)

IF task has multiple valid approaches to explore:
    → Tree-of-Thought (branch, evaluate, backtrack)

IF task involves complex interdependencies:
    → Graph-of-Thoughts (arbitrary connections between ideas)

IF task is high-stakes architecture or strategy:
    → Multi-Agent Deliberation (BMAD Party Mode — multiple personas debate)
```

### Chain-of-Thought Format

```
REASONING (Chain-of-Thought)
─────────────────────────────────────────────────────────
Step 1: [First reasoning step]
Step 2: [Second reasoning step]
...
Conclusion: [What follows from the chain]
─────────────────────────────────────────────────────────
```

### ReAct Format

```
REASONING (ReAct)
─────────────────────────────────────────────────────────
Thought 1:  [What I'm trying to figure out]
Action 1:   [What I'll do — search, read, run, etc.]
Observation 1: [What I learned from the action]

Thought 2:  [Updated understanding]
Action 2:   [Next action]
Observation 2: [What I learned]

... [Continue until resolved]

Conclusion: [Final answer based on accumulated observations]
─────────────────────────────────────────────────────────
```

### Tree-of-Thought Format

```
REASONING (Tree-of-Thought)
─────────────────────────────────────────────────────────
Root: [The problem to solve]

Branch A: [First approach]
  └─ Evaluation: [Promising? Score 1-10]
  └─ Continue? [Yes/No]

Branch B: [Second approach]
  └─ Evaluation: [Promising? Score 1-10]
  └─ Continue? [Yes/No]

Branch C: [Third approach]
  └─ Evaluation: [Promising? Score 1-10]
  └─ Continue? [Yes/No]

Selected Branch: [Which one and why]
Deeper exploration of selected branch...
─────────────────────────────────────────────────────────
```

### Multi-Agent Deliberation (BMAD Party Mode)

```
REASONING (Multi-Agent Deliberation)
─────────────────────────────────────────────────────────
ARCHITECT says:
"[Technical perspective on the problem]"

PRODUCT MANAGER says:
"[User/business perspective]"

SECURITY ENGINEER says:
"[Security perspective]"

PRAGMATIST says:
"[What's actually achievable given constraints]"

SYNTHESIS:
[Integrated recommendation accounting for all perspectives]
─────────────────────────────────────────────────────────
```

---

## Layer 5: VALIDATE — Stress-Test Before Committing

Never commit to an answer without validation. Use Deep Confidence methods.

### ATLAS Check

```
ATLAS VALIDATION
─────────────────────────────────────────────────────────
Anchor:      [Is my answer actually solving the right problem?]
Territory:   [Did I use all available relevant knowledge?]
Limits:      [Am I respecting the real constraints?]
Assumptions: [What am I assuming? Could any be wrong?]
Scope:       [Am I staying within bounds?]
─────────────────────────────────────────────────────────
```

### MAD Debate

```
MAD VALIDATION
─────────────────────────────────────────────────────────
My Answer:   [Current recommendation]

Attack:      [Strongest argument against this answer]
             [What's the best case for a different approach?]

Defense:     [Why my answer still holds — OR — how I'm updating it]

Final:       [Confirmed or revised answer]
─────────────────────────────────────────────────────────
```

### Monte Carlo Scenarios (for decisions/implementations)

```
MONTE CARLO VALIDATION
─────────────────────────────────────────────────────────
S1 (Best, 10%):      [If everything goes right]
S2 (Optimistic, 25%): [Good execution]
S3 (Base, 35%):      [Realistic middle]
S4 (Pessimistic, 20%): [If key risks hit]
S5 (Worst, 10%):     [Cascading failures]

Expected Outcome:    [Probability-weighted]
Biggest Risk:        [What could push us to S4/S5]
Mitigation:          [How to reduce that risk]
─────────────────────────────────────────────────────────
```

### Confidence Calibration

```
CONFIDENCE SCORES
─────────────────────────────────────────────────────────
[Claim 1]        →  [X%]  →  [Basis: evidence/inference/speculation]
[Claim 2]        →  [X%]  →  [Basis]
[Claim 3]        →  [X%]  →  [Basis]

Overall:         [X%]
Key Uncertainty: [The one thing that could make this wrong]
To Validate:     [How to get real data if needed]
─────────────────────────────────────────────────────────
```

---

## Layer 6: EXECUTE — Act With Full Foundation

Only now, with spec + reasoning + validation complete, take action.

### Execution Checklist

Before executing, verify:

- [ ] INTAKE complete — I know exactly what I'm solving
- [ ] MEMORY checked — I've used relevant past knowledge
- [ ] SPEC written — I have a clear specification (if required)
- [ ] REASONING complete — I've thought through the approach
- [ ] VALIDATION passed — I've stress-tested the answer
- [ ] CONFIDENCE scored — I know what I'm sure about vs. guessing

### Execution Output

Structure final output clearly:

```markdown
# [Task/Answer Title]

## Summary
[2-3 sentence answer or outcome summary]

## Confidence: [X%]
[One line on what this confidence is based on]

## Detail
[Full answer, implementation, recommendation, etc.]

## Caveats
[What I'm less sure about — be honest]

## Next Steps
[What should happen after this — if applicable]
```

---

## Layer 7: LEARN — Update the Knowledge Base

After execution, capture what happened for future reference.

### Outcome Recording

```json
{
  "task_id": "[unique identifier]",
  "timestamp": "[ISO date]",
  "task_type": "[from INTAKE classification]",
  "summary": "[what was the task]",
  "approach": "[what approach was used]",
  "outcome": "success | partial | failure | unknown",
  "confidence_predicted": 0.75,
  "confidence_actual": 0.80,
  "lessons": "[what was learned]",
  "update_to_procedures": "[any workflow improvements]",
  "update_to_facts": "[any new knowledge to store]"
}
```

### Learning Categories

| Outcome | Action |
|---|---|
| **Success** | Store approach in procedural memory. Increase confidence in similar future tasks. |
| **Partial** | Store with lessons learned. Note what worked and what didn't. |
| **Failure** | Store failure mode. Add to "approaches to avoid" for similar tasks. |
| **Unknown** | Mark as TBD. Set reminder to validate outcome later. |

### Continuous Calibration

Track predicted vs. actual confidence over time:

```
If I said 80% confidence and was right → calibration is good
If I said 80% confidence and was wrong → I'm overconfident in this domain
If I said 40% confidence and was right → I'm underconfident in this domain
```

Use this to recalibrate future confidence scores.

---

## Quick Reference: The Full Loop

```
USER REQUEST
     │
     ▼
┌─── L1: INTAKE ──────────────────────────────────────┐
│ • Classify task type                                 │
│ • Determine depth required                           │
│ • Select reasoning mode                              │
└──────────────────────────────────────────────────────┘
     │
     ▼
┌─── L2: MEMORY ──────────────────────────────────────┐
│ • Query semantic memory (facts)                      │
│ • Query episodic memory (past experiences)           │
│ • Query procedural memory (known workflows)          │
│ • Query outcome memory (what worked/failed before)   │
└──────────────────────────────────────────────────────┘
     │
     ▼
┌─── L3: SPEC ────────────────────────────────────────┐
│ • If implementation → write PRD + architecture spec  │
│ • If decision → write decision spec with criteria    │
│ • If research → write research questions doc         │
│ • Spec becomes source of truth                       │
└──────────────────────────────────────────────────────┘
     │
     ▼
┌─── L4: REASON ──────────────────────────────────────┐
│ • Chain-of-Thought (linear reasoning)                │
│ • ReAct (thought-action-observation loop)            │
│ • Tree-of-Thought (explore branches)                 │
│ • Multi-Agent Deliberation (multiple perspectives)   │
└──────────────────────────────────────────────────────┘
     │
     ▼
┌─── L5: VALIDATE ────────────────────────────────────┐
│ • ATLAS check (problem decomposition)                │
│ • MAD debate (argue against yourself)                │
│ • Monte Carlo scenarios (simulate outcomes)          │
│ • Confidence calibration (honest scoring)            │
└──────────────────────────────────────────────────────┘
     │
     ▼
┌─── L6: EXECUTE ─────────────────────────────────────┐
│ • Verify all layers complete                         │
│ • Produce output with confidence score               │
│ • Include caveats and next steps                     │
└──────────────────────────────────────────────────────┘
     │
     ▼
┌─── L7: LEARN ───────────────────────────────────────┐
│ • Record outcome (success/partial/failure/unknown)   │
│ • Store lessons learned                              │
│ • Update knowledge base                              │
│ • Calibrate future confidence                        │
└──────────────────────────────────────────────────────┘
```

---

## Depth Modes

### Minimal (factual queries)
- L1: INTAKE (classify)
- L6: EXECUTE (answer directly)
- L7: LEARN (only if new knowledge gained)

### Light (explanations, simple debugging)
- L1: INTAKE
- L2: MEMORY (quick check)
- L4: REASON (Chain-of-Thought)
- L6: EXECUTE
- L7: LEARN

### Full (implementation, architecture, decisions)
- All 7 layers, in order, no shortcuts

### Full+ (high-stakes, irreversible, strategic)
- All 7 layers
- Extended Multi-Agent Deliberation in L4
- Full Monte Carlo (5 scenarios × 3 time horizons) in L5
- External validation step before L6

---

## Integration With Other Skills

The Universal AI Harness orchestrates these specialized skills:

| Skill | When to Invoke | Which Layer |
|---|---|---|
| `@deep-confidence` | Decision tasks, architecture | L5: VALIDATE |
| `@monte-carlo-predictor` | Project evaluation, trajectory forecasting | L5: VALIDATE |
| `@research-engineer` | Deep research tasks | L4: REASON |
| `@systematic-debugging` | Debugging tasks | L4: REASON (ReAct mode) |
| `@openclaw-henry` | Life organization tasks | L6: EXECUTE |
| `@loki-mode` | Autonomous multi-agent execution | L6: EXECUTE |

---

## The Memory File

Create and maintain this file in your project root:

**`HARNESS_MEMORY.json`**

```json
{
  "version": "1.0",
  "last_updated": "2026-02-20T12:00:00Z",

  "semantic_memory": {
    "domain_knowledge": {},
    "definitions": {},
    "facts": {}
  },

  "episodic_memory": {
    "sessions": []
  },

  "procedural_memory": {
    "workflows": {},
    "patterns": {}
  },

  "outcome_memory": {
    "successes": [],
    "failures": [],
    "pending_validation": []
  },

  "calibration": {
    "confidence_accuracy": {
      "90_plus": { "predicted": 0, "actual_correct": 0 },
      "70_89": { "predicted": 0, "actual_correct": 0 },
      "50_69": { "predicted": 0, "actual_correct": 0 },
      "below_50": { "predicted": 0, "actual_correct": 0 }
    }
  }
}
```

At the start of each session, read this file.
At the end of each session, update it.

---

## Principles

1. **Spec before action.** Never code or decide without a specification.
2. **Memory before reasoning.** Check what you already know first.
3. **Right tool for the task.** Match reasoning mode to task type.
4. **Validate before committing.** Stress-test every significant answer.
5. **Honest confidence.** Know what you know vs. what you're guessing.
6. **Learn from outcomes.** Every task teaches something — capture it.
7. **Evolve continuously.** The harness itself should improve over time.

---

## Why This Works

| Problem | How the Harness Solves It |
|---|---|
| Token waste from back-and-forth | SPEC layer front-loads understanding |
| Inconsistent reasoning | REASON layer applies structured frameworks |
| Overconfident answers | VALIDATE layer forces stress-testing |
| Forgetting past work | MEMORY layer persists knowledge |
| Repeating mistakes | LEARN layer captures and avoids past failures |
| No calibration | CONFIDENCE scoring tracks accuracy over time |
| One-size-fits-all thinking | INTAKE layer matches approach to task type |

---

## Sources & Inspirations

This harness synthesizes:

- [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) — Spec-driven, multi-agent workflows
- [Spec-Driven Development](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices) — Document-first AI development
- [ReAct Framework](https://react-lm.github.io/) — Reasoning + Acting in language models
- [Chain-of-Thought Prompting](https://www.promptingguide.ai/techniques/cot) — Step-by-step reasoning
- [Tree-of-Thought](https://arxiv.org/abs/2305.10601) — Branching exploration
- [Mem0](https://arxiv.org/pdf/2504.19413) — Persistent memory for AI agents
- [Deep Confidence / ATLAS / MAD](#) — Internal reasoning harness (this repo)
- [Monte Carlo Prediction](#) — Scenario-based forecasting (this repo)
