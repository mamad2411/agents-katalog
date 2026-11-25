---
name: debugging-strategies
description: A systematic approach to debugging complex issues.
---

# Debugging Strategies Skill

A systematic approach to debugging complex issues.

## When to Use
- Bug reports that are hard to reproduce
- Intermittent failures
- Performance issues
- Production incidents

## Strategy Selection

Based on the problem type, apply the appropriate strategy:

### 1. Binary Search Debugging
For: "It worked before, now it doesn't"
- Use `git bisect` to find the breaking commit
- `git bisect start`, `git bisect bad`, `git bisect good [commit]`

### 2. Trace-Based Debugging
For: "I don't know where the bug is"
- Add strategic console.log/print at function entry/exit points
- Follow the data flow from input to unexpected output
- Narrow down to the exact function where data transforms incorrectly

### 3. Isolation Debugging
For: "Too many things could be wrong"
- Create a minimal reproduction
- Remove components until the bug disappears
- The last removed component is likely the cause

### 4. Hypothesis-Driven Debugging
For: "I have a theory"
- State the hypothesis clearly
- Design a test that would prove/disprove it
- Execute the test
- If disproven, form a new hypothesis

### 5. Performance Debugging
For: "It's slow"
- Profile first, don't guess
- Use built-in profilers (Chrome DevTools, cProfile, pprof)
- Focus on the hottest path
- Measure before and after any change

## Process

1. **Reproduce**: Confirm you can trigger the bug reliably
2. **Isolate**: Narrow down to the smallest reproducing case
3. **Identify**: Find the root cause (not just the symptom)
4. **Fix**: Apply the minimal fix
5. **Verify**: Confirm the fix resolves the issue
6. **Prevent**: Add a test that would catch regression
