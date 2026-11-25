---
name: problem-solving
description: Use this skill when approaching complex or ambiguous problems, breaking down large challenges, applying first principles thinking, or structuring your approach to a new problem. Trigger on keywords: how do I approach, I don't know where to start, complex problem, break this down, first principles, problem decomposition, stuck on, overwhelmed by.
---

# Problem Solving

## Core Mindset

**Don't solve the problem you think you have. Solve the problem you actually have.**

Most wasted effort in software comes from solving the wrong problem confidently. The first step is always to verify the problem definition.

---

## The Problem-Solving Framework

```
1. DEFINE    — What is the actual problem? (not the symptom)
2. CONSTRAIN — What are the boundaries? (must-haves, non-negotiables)
3. DECOMPOSE — Break into smaller sub-problems
4. EXPLORE   — Generate multiple approaches before committing
5. DECIDE    — Choose based on explicit criteria
6. EXECUTE   — Implement the chosen approach
7. REVIEW    — Did it solve the right problem?
```

---

## First Principles Thinking

Instead of reasoning by analogy ("how do others do this?"), break the problem down to fundamental truths:

```
1. What do we know for certain is true about this problem?
2. What assumptions am I making that might be wrong?
3. If I had to rebuild this from scratch knowing only those truths, 
   what would I build?
```

Use when: existing solutions feel wrong, you're stuck in conventional thinking, or you need a breakthrough.

---

## Decomposition Techniques

### Top-Down
Start with the goal, break into sub-goals:
```
Goal: Build a user auth system
└── Registration flow
    ├── Form validation
    ├── Password hashing
    └── Email verification
└── Login flow
    ├── Credential verification
    ├── Session/token creation
    └── Remember me
└── Security hardening
    ├── Rate limiting
    ├── Brute force protection
    └── Audit logging
```

### MECE (Mutually Exclusive, Collectively Exhaustive)
Ensure sub-problems don't overlap and together cover the whole problem.

---

## When You're Stuck

1. **Restate the problem** in different words
2. **Ask "what would need to be true"** for each possible solution to work
3. **Invert** — what would make this definitely fail? Design away from that.
4. **Simplify** — solve a simpler version first, then generalize
5. **Time-box exploration** — 30 min max before asking for help

---

## Trade-Off Analysis

For every major decision, document:
```
Option A: [description]
  Pros: [benefits]
  Cons: [costs/risks]
  Best when: [conditions]

Option B: [description]
  Pros: [benefits]
  Cons: [costs/risks]
  Best when: [conditions]

Decision: [chosen option]
Reason: [why this fits the current constraints]
Revisit if: [conditions that would change the decision]
```
