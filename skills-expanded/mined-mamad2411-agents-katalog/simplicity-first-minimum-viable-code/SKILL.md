---
name: simplicity-first-minimum-viable-code
description: Write the minimum code that solves the stated problem. No speculative features, no abstractions for single-use code, no error handling for impossible scenarios. Use for any implementation task.
category: engineering
version: 1.0.0
version_origin: extracted
tags: [simplicity, yagni, anti-overengineering, code-review]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/forrestchang/andrej-karpathy-skills.git
source_ref: main
source_commit: c9a44ae835fa2f5765a697216692705761a53f40
source_project: andrej-karpathy-skills
source_path: skills/karpathy-guidelines/SKILL.md
imported_at: 2026-04-18T08:26:22Z
---

# Simplicity First — Minimum Viable Code

**Minimum code that solves the problem. Nothing speculative.**

LLMs tend to "overcomplicate code and APIs, bloat abstractions" — implementing 1000 lines where 100 would do. Bias hard toward simplicity.

## Rules
- No features beyond what was asked.
- No abstractions for single-use code (no Strategy pattern for one discount type).
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for scenarios that cannot happen.
- If 200 lines could be 50, rewrite it.

## Self-test
> "Would a senior engineer say this is overcomplicated?"
If yes, simplify before shipping.

## Decision rubric — when to add complexity
| Signal | Add abstraction? |
|--------|------------------|
| "Might need later" | No |
| Exactly one call site today | No |
| Multiple concrete variants exist right now | Maybe |
| Already three copy-pasted variants in the codebase | Yes |

## Anti-patterns from the source corpus
- `DiscountStrategy` ABC + `PercentageDiscount`, `FixedDiscount`, `DiscountConfig`, `DiscountCalculator` for a single percentage calculation → replace with `def calculate_discount(amount, percent): return amount * (percent / 100)`.
- `PreferenceManager` with cache, validator, notify, merge params when "save preferences" was requested.

## Fallback
When in doubt, write the boring version first. Refactor *when* the second concrete need appears, not before.
