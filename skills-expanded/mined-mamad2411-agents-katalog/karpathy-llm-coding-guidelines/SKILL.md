---
name: karpathy-llm-coding-guidelines
description: Umbrella behavioral guideline that bundles the four Karpathy principles — Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution — to reduce common LLM coding mistakes. Use when you want all four applied at once.
category: engineering
version: 1.0.0
version_origin: extracted
tags: [llm-behavior, umbrella, karpathy, coding-guidelines]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/forrestchang/andrej-karpathy-skills.git
source_ref: main
source_commit: c9a44ae835fa2f5765a697216692705761a53f40
source_project: andrej-karpathy-skills
source_path: skills/karpathy-guidelines/SKILL.md
imported_at: 2026-04-18T08:26:22Z
---

# Karpathy LLM Coding Guidelines (Umbrella)

Four principles addressing the most common LLM coding pitfalls, derived from Andrej Karpathy's X post on LLM coding behavior.

**Tradeoff:** biases toward caution over speed. For trivial fixes, use judgment.

| Principle | Addresses |
|-----------|-----------|
| Think Before Coding | Wrong assumptions, hidden confusion, missing tradeoffs |
| Simplicity First | Overcomplication, bloated abstractions |
| Surgical Changes | Orthogonal edits, drive-by refactors |
| Goal-Driven Execution | Vague "make it work" loops, missing verification |

See dedicated skills:
- `think-before-coding-surface-assumptions`
- `simplicity-first-minimum-viable-code`
- `surgical-changes-only-touch-requested`
- `goal-driven-verifiable-success-criteria`

## Success signals
- Fewer unnecessary changes in diffs.
- Fewer rewrites due to overcomplication.
- Clarifying questions come **before** implementation, not after.
- Clean, minimal PRs — no drive-by refactoring.

## Source
Karpathy's observations paraphrased: LLMs "make wrong assumptions and run along"; "like to overcomplicate code and APIs, bloat abstractions"; "sometimes change/remove comments and code they don't sufficiently understand"; and conversely, "are exceptionally good at looping until they meet specific goals."
