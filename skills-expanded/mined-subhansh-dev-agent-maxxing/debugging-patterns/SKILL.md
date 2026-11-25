---
name: debugging-patterns
description: Systematic debugging methodology — read errors completely, reproduce first, bisect, add logging, trace flow.
---

# Debugging Patterns — How to Fix Things

## The Debugging Chain

When you hit a bug:

1. **Read the error message completely.** All of it. Don't skim.
2. **Reproduce it.** Run the code. Hit the error. See it yourself.
3. **Bisect.** Comment out half the code. Does it still happen? Binary search.
4. **Add logging.** Print the state at each step. Don't guess — measure.
5. **Trace the flow.** Follow the data from input to output. Where does it go wrong?
6. **Check the obvious.** Typos, wrong variable names, missing imports, stale caches.
7. **Search for it.** Someone else probably hit this. Stack Overflow, GitHub issues, docs.
8. **Try the simplest fix first.** Don't refactor the whole system for a typo.
9. **If you're going in circles, stop.** Explain what you've tried and why each attempt failed.

## Common Bug Categories

### Null/Undefined
- Check if the value is actually defined before using it
- Trace where it comes from — is it async? Is it cached?
- Add a guard: `if (!value) return` or `value ?? fallback`

### Async/Timing
- Is something racing? Add `await` or locks
- Is the order wrong? Log timestamps
- Is the callback firing twice? Check event listener cleanup

### State
- Is the state stale? Log it before and after
- Is it shared between instances? Check for singleton issues
- Is it being mutated unexpectedly? Use immutable patterns

### Environment
- Is it a different Node/Python version?
- Is it a different OS? (path separators, line endings)
- Is it a different environment variable?
- Is it a cached build? Clean and rebuild.

## The "Rubber Duck" Technique

Explain the problem out loud (or in a comment). The act of articulating it often reveals the solution. If you can't explain it simply, you don't understand it yet.

## When to Ask for Help

After you've:
1. Read the error completely
2. Reproduced it
3. Tried the obvious fixes
4. Added logging
5. Searched for similar issues
6. Still stuck

Then ask. Include: what you tried, what happened, what you expected.
