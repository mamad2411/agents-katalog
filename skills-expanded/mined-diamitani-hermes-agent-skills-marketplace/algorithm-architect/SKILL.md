---
name: algorithm-architect
description: "Use when creating algorithms, code tutorials, and structured programming solutions. Helps design and explain algorithmic approaches."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [algorithms, tutorials, programming, education, problem-solving]
---

# Algorithm Architect

## Overview

Design, explain, and implement algorithmic solutions with clarity and precision. This skill provides a structured approach to breaking down complex programming problems into well-defined algorithms, complete with step-by-step explanations, complexity analysis, and runnable code examples. Ideal for coding tutorials, interview preparation, or when a problem requires a methodical algorithmic approach.

## When to Use

- "Design an algorithm for..." — creating a new algorithm from scratch
- "Explain how [algorithm] works" — educational walkthroughs of existing algorithms
- "What's the most efficient way to..." — optimization and complexity analysis
- "Write a tutorial on..." — creating code tutorials with structured explanations
- "Help me solve this coding challenge" — competitive programming and interview problems

**Don't use for:** simple one-liner scripts, CRUD boilerplate, configuration changes, or frontend layout work.

## How It Works

The skill follows a five-phase approach: **Understand → Design → Analyze → Implement → Explain**. Each phase builds on the previous one, ensuring the final solution is correct, efficient, and well-documented.

## Steps

### 1. Problem Understanding
- Restate the problem in your own words
- Identify input constraints, edge cases, and expected output
- Ask clarifying questions if any ambiguity exists

### 2. Algorithm Design
- Brainstorm 2-3 approaches (brute force → optimized)
- Sketch the algorithm in pseudocode before writing real code
- Trace through a small example manually to validate the logic

### 3. Complexity Analysis
- Time complexity: best, average, and worst case
- Space complexity: auxiliary vs. total
- Justify why the chosen approach is optimal (or note trade-offs)

### 4. Implementation
- Write clean, well-commented code in the target language
- Include meaningful variable names and helper functions
- Add docstrings explaining parameters, returns, and side effects

### 5. Explanation & Testing
- Walk through the code with a concrete example
- Test with edge cases: empty input, single element, large input, duplicates
- Provide a summary that connects back to the original problem

## Common Pitfalls

1. **Jumping to code too fast.** Without pseudocode and manual tracing, subtle off-by-one errors or logic gaps slip through. Always sketch the approach first.

2. **Ignoring edge cases.** Empty arrays, null values, integer overflow, and boundary conditions are where most algorithms fail. Test these explicitly.

3. **Wrong complexity claims.** Nested loops don't always mean O(n²) — consider early exits, amortized analysis, and input constraints. Verify your claims against the actual code.

4. **Over-optimizing prematurely.** A correct O(n²) solution is better than a buggy O(n log n) one. Optimize only after correctness is confirmed.

5. **Unreadable code.** Algorithm code is read far more often than it's written. Use descriptive variable names (not `i`, `j`, `tmp`) and add comments for non-obvious steps.
