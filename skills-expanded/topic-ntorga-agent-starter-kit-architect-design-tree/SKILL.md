---
name: architect-design-tree
description: Builds the design tree for the grill — decisions mapped as nodes with dependencies, recommendations, and impact, pruned by path.
usedBy: [architect]
version: 0.2.2
lastUpdated: 2026-09-12
---

## Purpose

The grill interviews the user over the design tree. This skill builds and extends that tree. The tree is the grill's working state: every decision the feature must settle, mapped with its dependencies, pruned to the selected path, ranked by impact. The Maestro computes the frontier from this file and works the rounds. You never talk to the user.

## Procedure

- **Initial** — no tree exists. Build the tree from the task prompt.
- **Re-tree** — the tree exists. The user's answers opened a branch the tree does not have. Extend the tree. Do not rebuild it.

1. Read the task block. Note the selected path (beginner, tinkerer, or pro) and any new user answers it carries.
2. Orient in the codebase before mapping decisions:
   - Read `.context.md` files in the affected directories.
   - Read `docs/FEATURE-MAP.md` if it exists.
   - For the beginner path, infer the default architecture from the maintenance, lightweight, and safe principles (KISS, single responsibility, safe boundaries — `rules/code/general.md`).
3. Identify the decisions the feature must settle. Map them as a tree with three branches:
   - **Business** — what the user wants. Acceptance criteria, scope, constraints, success conditions.
   - **Architecture** — how the system is structured. Directory layout, layer separation, frameworks, reference projects.
   - **Implementation** — how the work is organized. Epics, dependencies, parallelizable groups.
   Prune branches the path does not explore. Beginner: business only. Tinkerer: business and architecture. Pro: all three.
4. Apply the quality filter to every candidate decision: does this decision pivot the destination substantially? If the answer does not change the project's direction, remove the node. Prune with the filter, not the ceiling. The ceiling only bounds how large a branch grows — never pad the tree to hit it.
5. Check the ceilings. Business: 30 (beginner, tinkerer), 100 (pro). Architecture: 10 (tinkerer), 100 (pro). Implementation: 100 (pro). If a branch exceeds its ceiling, prune until it fits.
6. For each node, write:
   - The question in plain terms the user can answer alone.
   - Dependencies — the node numbers that must settle first. A node may also depend on a fact from step 7.
   - Recommendation — the answer you would choose, with the reason, in one or two sentences.
   - Impact — high, medium, or low, by how many downstream nodes the answer unblocks.
7. List the facts the tree needs from the codebase or the environment in the `## Facts` section. A fact is a question only a lookup can answer — a library capability, an existing endpoint, a config key. Number them `f1`, `f2`, and so on.
8. Write the tree to `.memory/plan/<feature-slug>/tree.md` in the format below. Create the directory if it does not exist.
9. For re-tree: read `tree.md`. Add the new nodes with their fields. Add new facts if needed. Keep every settled node and every settled fact as is. Never renumber.

## Tree Format

    # Design Tree: <Feature Name>
    Path: <beginner | tinkerer | pro>

    ## Business
    1. [settled] <question> — answer: <settled answer>
    2. [open] <question> — depends: 1 — recommendation: <answer and why> — impact: high

    ## Architecture
    1. [open] <question> — depends: B2 — recommendation: <answer and why> — impact: medium

    ## Implementation
    1. [open] <question> — depends: B1, A1, f1 — recommendation: <answer and why> — impact: low

    ## Facts
    - f1: <fact question> — open
    - f2: <fact question> — <found answer, with source>

- Number nodes per branch, starting at 1. Refer to a node in another branch by prefix: B2, A1, I1.
- A node with no dependencies is frontier from round 1.
- A node is frontier when every dependency is settled: a node marked `[settled]`, or a fact with a found answer.

## Handoff

Deliver `tree.md` with a summary:

```
## Summary
[One sentence: what was done]

## Tree
- Branches explored: [list]
- Branches pruned: [list and why]
- Facts needed: [list]
```

## Guardrails

- Never ask the user a question. You deliver the tree. The Maestro relays it.
- Never leave a decision silently assumed. If the feature must settle it, it gets a node.
- Never rebuild on re-tree. Extend. Settled nodes keep their numbers and answers.
- Never put a codebase fact inside a user question. It goes in `## Facts` as a fact dependency.
- Keep questions answerable by the user alone. If answering requires a file read, it is a fact, not a question.
- Write the tree in STE-100. Short sentences. One idea per sentence. Active voice.
