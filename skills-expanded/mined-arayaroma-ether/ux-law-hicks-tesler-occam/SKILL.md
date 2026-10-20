---
name: ux-law-hicks-tesler-occam
description: Use when designing any screen, menu, form, or decision point with multiple options or steps — covers Hick's Law (decision time grows with choice count/complexity), Tesler's Law (complexity is conserved, someone must absorb it), and Occam's Razor (prefer the simplest design that works). Triggers on "too many options", "simplify this flow", "reduce choices", "menu design", "onboarding steps".
allowed-tools: Read, Edit, Grep, Glob
---

# Hick's Law + Tesler's Law + Occam's Razor

Decision complexity group: fewer/clearer choices speed decisions, but complexity removed from the UI usually moves to code or config — it doesn't vanish.

## Hick's Law
Decision time increases with number and complexity of choices. Cut visible options to what the task needs now; progressive-disclose the rest (advanced settings, "show more"). Group related choices into categories rather than one flat list — categorized choices are processed faster than an equal-size flat list.

## Tesler's Law (conservation of complexity)
Every system has irreducible complexity. Ask "who absorbs this: the user, or the system?" and default to absorbing it in code (smart defaults, auto-detection, inferred values) rather than pushing a config decision onto the user for things the system can determine.

## Occam's Razor
Given two designs solving the task equally well, ship the one with fewer moving parts, fewer screens, fewer states. Simplicity is a tiebreaker, not an excuse to under-solve the task — don't strip a control the user actually needs.

## Applying together
1. List every choice/step currently shown to the user.
2. For each, ask: does the system already know the answer? -> Tesler, absorb it.
3. Of what's left, group and progressively disclose -> Hick's.
4. Between remaining valid designs, pick the simplest -> Occam.
