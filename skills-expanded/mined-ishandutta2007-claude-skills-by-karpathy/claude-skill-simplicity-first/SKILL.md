---
name: claude-skill-simplicity-first
description: Premium Claude Skill - Simplicity First. Bias towards the minimum code required to solve the problem. Prevents overengineering and speculative features.
license: MIT
---

# Simplicity First (Claude Skill)

**Minimum code that solves the problem. Nothing speculative.**

- **No features beyond what was asked.** Avoid "just-in-case" logic.
- **No abstractions for single-use code.** Keep it flat and readable.
- **No speculative flexibility.** Don't build for hypothetical future needs.
- **No error handling for impossible scenarios.** Avoid bloat.
- **If 200 lines could be 50, rewrite it.**

**The test:** Would a senior engineer say this is overcomplicated? If yes, simplify.
