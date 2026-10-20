---
name: ai-interaction-type-selection-rule
description: Provides a rule-of-thumb for selecting the optimal GenAI interaction type (in-code suggestions vs chat vs combined) based on task characteristics to maximize efficiency and minimize cognitive overhead. Use when designing developer-GenAI interaction guidelines, building IDE AI features, training developers on Copilot/Cursor usage, or diagnosing why a team's AI adoption isn't delivering expected productivity. NOT for evaluating model quality benchmarks or non-coding GenAI use cases.
---

# AI Interaction Type Selection Rule

## Overview

Empirical research with 22 professional developers at SAP reveals that the choice of GenAI interaction type — in-code suggestions, chat-based prompting, or combined — significantly impacts efficiency, accuracy, and perceived workload. Using a single interaction type per task improves efficiency and reduces workload; combining both interaction types within a single task eliminates the benefits and produces results comparable to not using GenAI at all. A simple rule-of-thumb guides optimal selection based on task characteristics.

## When to Use

- Designing developer-GenAI interaction guidelines or best practices
- Building IDE AI features that adapt interaction mode to task context
- Training developers on effective Copilot/Cursor/Claude Code usage
- Diagnosing why a team's AI adoption isn't delivering expected productivity
- Researching developer-GenAI interaction patterns in natural work environments

NOT for:
- Evaluating model quality benchmarks (HumanEval, SWE-bench)
- Non-coding GenAI use cases (writing, analysis, creative tasks)
- Pure prompt engineering optimization (focus is interaction TYPE, not prompt content)

## Core Process / Workflow

### 1. Identify the Three Interaction Types

| Interaction Type | Where Output Appears | Context Scope | Latency | Best For |
|---|---|---|---|---|
| **In-code suggestions** | At cursor position | Local code context (surrounding lines) | Low | Fluid, autocompletion-like workflows |
| **In-line chat** | Within source file | Limited surrounding lines | Medium | Localized questions/modifications |
| **Chat** | Separate window | Broader (entire file, multiple files) | Higher | Creativity, explanation, dialogue |

### 2. Apply the Selection Rule of Thumb

```
DECISION GUIDE:

Is the task primarily coding or non-coding related?
│
├─ CODING-RELATED
│  │
│  ├─ How much codebase context does the model need?
│  │  │
│  │  ├─ LITTLE (local changes, boilerplate, docs, tests)
│  │  │  └─ Are explanations beyond inline comments needed?
│  │  │     │
│  │  │     ├─ NO → USE IN-CODE SUGGESTIONS ✓
│  │  │     └─ YES → USE CHAT (but plan upfront, don't switch mid-task)
│  │  │
│  └─ LARGE (multiple files, architecture, deep context)
│     └─ USE CHAT ✓
│
└─ NON-CODING (brainstorming, summaries, debugging explanations)
   └─ USE CHAT ✓
```

**Summary rule**: Coding tasks with little context and no need for explanations → in-code. Everything else → chat. Never combine within a single task.

### 3. Understand the Combined-Use Penalty

```
THE COMBINED-USE PENALTY:
  Either in-code OR chat alone:
    → Significantly shorter task duration vs no Copilot
    → Significantly lower perceived workload vs no Copilot
  
  BOTH interaction types combined in one task:
    → Task duration ≈ no Copilot condition
    → Perceived workload ≈ no Copilot condition
    → Significantly higher workload than in-code alone
  
  CAUSE: Switching between interaction modes introduces cognitive overhead
  → The switching + consideration of "how to best solve given available options"
     produces overhead that negates the GenAI benefit
```

### 4. Match Interaction Type to Task Categories

```
TASK-SPECIFIC GUIDANCE:

IN-CODE SUGGESTIONS (preferred for):
  ✓ Boilerplate code generation
  ✓ Writing documentation
  ✓ Writing unit tests
  ✓ Small/simple code changes
  ✓ Repetitive/structured tasks

CHAT-BASED (preferred for):
  ✓ Debugging (requires broader context)
  ✓ Brainstorming and conceptualization
  ✓ Writing summaries
  ✓ Non-coding tasks
  ✓ Tasks requiring explanations
  ✓ Retrieving information from codebase
  ✓ Higher-level, creative, or complex tasks
```

### 5. Monitor Cognitive Load and Productivity Signals

```
DEVELOPMENT-HEAVY TASK ANALYSIS:

AI use during development-heavy tasks:
  → Associated with HIGHER perceived cognitive load (+0.58, p=0.008, d=0.34)
  → NO significant change in perceived productivity
  
When AI is perceived as HELPFUL:
  → Comparable cognitive load
  → HIGHER perceived productivity (+0.73, p=0.043, d=0.83, large effect)

INTERPRETATION:
  In dev-heavy tasks, cognitive load arises from AI INTERACTION itself
  Perceived productivity depends on AI OUTPUT QUALITY
  → Interaction type selection is the critical variable
```

### 6. Account for Interaction Intensity

```
INTENSITY MODERATION:
  Moderate use of either interaction type:
    → Improves efficiency
  
  Excessive interactions (especially frequent chat or combined):
    → Introduces overhead that diminishes or REVERSES time savings

  Excessive in-code suggestions (trial-and-error pattern):
    → Sense of achievement but also significant code discard
    → May inflate perceived productivity without real gains
```

### 7. Design for Awareness and Intentional Use

```
STUDY IMPACT FINDING:
  73% of developers said they would adjust GenAI use after structured study
  Developers with LOWER prior proficiency were MORE likely to change behavior
  
IMPLICATION FOR TEAMS:
  Structured reflection on AI use → more intentional, differentiated usage
  Workshop/hackathon-style formats in real work settings → effective training
  Don't assume frequent users have optimized strategies — they may have 
  stabilized suboptimal patterns
```

## References

- See [references/ai-interaction-type-evidence-base.md](references/ai-interaction-type-evidence-base.md) for full study design, statistical results, task categories, and qualitative findings.