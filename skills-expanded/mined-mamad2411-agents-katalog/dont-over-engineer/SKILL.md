---
name: dont-over-engineer
description: Avoid over-engineering — use minimal changes
argument-hint: "[scope]"
related:
  - dont-ask-me
  - dont-understand
  - review-by-all-stakeholder
  - deep-debug

---

## Goal

Always solve problems with minimal changes

## Scope

Use for every code change and implementation

## Execute

### 1. Analyze Problem

> Goal: Analyze Problem

Analyze the problem to find the root cause

1. Run `/deep-debug` to analyze the problem
2. Find the simplest solution
3. Do not create unnecessary abstractions

### 2. Apply Minimal Fix

> Goal: Apply Minimal Fix

Use minimal changes whenever possible

1. Use a `single-line change` when possible
2. Do not refactor the whole codebase to fix a small problem
3. Do not build a generic solution for a specific problem

### 3. Verify Solution

> Goal: Verify Solution

Verify that the problem is really solved

1. Test that the problem is really fixed
2. Check that there are no side effects
3. Remove any unnecessary code that was added

## Rules

### 1. Minimal Changes

Use minimal changes whenever possible

- Use a `single-line change` when possible
- Do not refactor the whole codebase to fix a small problem
- Do not create unnecessary abstractions
- Do not add complexity unnecessarily

### 2. Root Cause First

Understand the root cause before fixing

- Run `/deep-debug` to analyze the problem
- Do not fix symptoms without knowing the cause
- Do not guess solutions without analysis
- Use the simplest possible solution

### 3. Simple Solutions

Use simple, to-the-point solutions

- Do not build a generic solution for a specific problem
- Do not add unnecessary dependencies
- Do not build overly complex architecture
- Use the `YAGNI` principle (You Aren't Gonna Need It)

### 4. Verify Impact

Verify the impact of the change

- Test that the problem is really fixed
- Check that there are no side effects
- Remove any unnecessary code that was added
- Measure the impact (performance, complexity)

- Use /dont-ask-me if needed
- Use /dont-understand if needed
- Use /review-by-all-stakeholder if needed

## Expected Outcome

- Problems solved with minimal changes
- No over-engineering
- Code stays simple and easy to understand
- No unnecessary abstractions
- Solutions are to-the-point and easy to understand