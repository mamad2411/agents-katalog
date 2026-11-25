---
name: karpathy-guidelines
description: Behavioral guidelines to reduce common LLM coding mistakes. Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface assumptions, and define verifiable success criteria.
allowed-tools: Read, Write, Edit
version: 2.0
priority: CRITICAL
---

# Karpathy Guidelines - Defensive AI Coding

> **CRITICAL SKILL** - Eliminate speculative code, prevent overcomplication, and verify every step.
> Derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.
> **Reference:** For pragmatic coding standards, SRP/DRY, and general programming conventions, refer to the [clean-code](../clean-code/SKILL.md) skill.

---

## The Four Principles

| Principle | Core Directive | Actionable Target |
|-----------|----------------|-------------------|
| **1. Think Before Coding** | Surface tradeoffs, assumptions, and confusion. | Ask clarifying questions BEFORE implementing. |
| **2. Simplicity First** | Minimal code that works. Avoid speculation. | Write 50 lines instead of 200. No abstractions. |
| **3. Surgical Changes** | Edit only what you must. No side effects. | Every changed line must trace to user request. |
| **4. Goal-Driven Execution** | Define success criteria and verification loops. | Red-green-verify loops with concrete goals. |

---

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

| Situation | Required Action |
|-----------|-----------------|
| **Uncertainty/Ambiguity** | State assumptions explicitly. Stop and ask the user. |
| **Multiple Interpretations** | Present options and tradeoffs. Do not pick silently. |
| **Simpler Alternative Exists** | Push back and propose the simpler approach. |
| **Unclear Code/Goal** | Pause. Name what is confusing. Clarify first. |

---

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

| Do ✅ | Don't ❌ |
|-------|---------|
| Focus strictly on requested features | Add speculative features or "future-proofing" |
| Keep code inline and concrete | Build abstractions for single-use code |
| Use hardcoded settings where adequate | Add unrequested config or flexibility options |
| Handle only expected scenarios | Add error handling for impossible edge cases |
| Rewrite a 200-line solution into 50 lines | Leave bloated, complex, or multi-layered code |

> **The Golden Test:** "Would a senior engineer say this is overcomplicated?" If yes, rewrite and simplify.

---

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

| Target Code | Rules & Boundaries |
|-------------|-------------------|
| **Adjacent Code** | Do NOT "improve", reformat, or modify adjacent code. |
| **Comments & Formatting** | Preserve all existing comments and style. Match exactly. |
| **Refactoring** | Do NOT refactor code that is not broken. |
| **Dead Code (Unrelated)** | Mention it to the user. Do NOT delete it silently. |
| **Orphaned Code (Your changes)**| Remove imports/variables/functions YOUR changes made unused. |

---

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform vague instructions into verifiable, precise targets:

| Imperative Task | Declarative Verifiable Goal |
|-----------------|-----------------------------|
| "Add validation" | "Write tests for invalid inputs, then make them pass." |
| "Fix the bug" | "Write a test that reproduces the bug, then make it pass." |
| "Refactor function X" | "Verify that existing tests pass before and after the change." |

### Plan-Act-Verify Loop
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

---

## Summary: Defensive Coding Guidelines

| Defensive Coding (Do) | Speculative Coding (Don't) |
|-----------------------|----------------------------|
| Surface assumptions & ask early | Pick an interpretation silently and run with it |
| Write the absolute minimum code | Add abstractions, layers, or config |
| Perform surgical, targeted edits | Touch adjacent code, reformat files, or refactor |
| Establish concrete tests & verify | Assume it works without checking or testing |

```
Guidelines are working if:
└── Fewer unnecessary changes in diffs
└── Fewer rewrites due to overcomplication
└── Clarifying questions come before implementation, not after mistakes
```
