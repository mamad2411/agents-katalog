---
name: code-smells
description: Identify code smells and suggest refactors. Use when reviewing code
  for quality signals.
metadata:
  tags: code, smells
---

# Code Smells

## Use this skill when
- Reviewing code quality
- Planning refactoring sessions
- Coaching developers on maintainability

## Do not use this skill when
- Writing new code from scratch (apply principles instead)
- Only fixing a bug

## Instructions
1. Review for duplication and extract functions/classes.
2. Flag long methods and god classes and name their responsibilities.
3. Detect feature envy and data clumps.
4. Identify switch/if chains that are polymorphism in disguise.
5. Guard against speculative generality.
6. Ground each recommendation in current pain, not theory.

## Output Format
- Smell | Location | Why it matters | Refactor

## Common Mistakes
- Listing smells generically instead of tailoring to the codebase
- Ignoring testability signals
