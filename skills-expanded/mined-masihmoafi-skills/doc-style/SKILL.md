---
name: doc-style
description: Use when writing, reviewing or auditing a README, skill, specification, project page or launch material that must stay concise and evidence-backed, including "audit docs" and "prune AI self-talk".
---

# Documentation style

Part 1 applies to every document. Parts 2 and 3 apply to public READMEs and project pages. A file with a required schema (a `SKILL.md`, a spec) keeps its schema. Agent docs (`AGENTS.md`, `ES.md`) follow `project-docs`; sentences follow `writing-style`.

## 1. Every document

- Keep the author's voice. Use facts and short, direct sentences; no marketing words.
- Claim nothing the repository cannot prove: no feature, result, benchmark, release, user count or stability level without evidence.
- Name the true state: "planned", "under acceptance" or "experimental".
- Put the evidence beside the claim it supports.
- Prefer a pointer (`file:line`, a link) to a copy; copies go stale.

## 2. Public README or project page

The first screen answers four questions: what is it, who is it for, what painful problem does it remove, what proof can the reader inspect now (a demo, screenshot, passing workflow, benchmark, release or command). Do not open with history, philosophy or a feature list.

Sections, in this order:

1. **Intro**: two or three sentences: what it is, who it serves, why it exists. A good hook is a falsifiable claim ("A coding agent should not forget why it is changing your code."), and the next sentence says how the project acts on it.
2. **Quick start**: install (one command), run (one command), expected result. Long walkthroughs go below.
3. **The problem**: the concrete failure in today's workflow, shown as "without this" against "with this".
4. **How it works**: a one-page manual of mechanics and limits; a small diagram if it helps. Deep references go to the project's docs home (GitHub Pages is one option) and are linked by topic.
5. **Current state**: four separate lists: verified, under acceptance, planned, unsupported. Link the source of truth.
6. **What sets it apart**: design choices and tradeoffs checked against the repository and real alternatives. Invent no novelty.
7. **Evidence**: what the tests, workflows and benchmarks cover, and what a passing badge does and does not prove. If there is none, say so and name the smallest useful test.
8. **Next**: near-term work backed by the task tracker only.

Before you finish, check: the opening states the real product and its maturity; Quick start comes before deep detail; every major claim can be verified; the reader knows what to do next; one sentence could serve as the public description.

## 3. Distribution

Derive every channel from the README; change the opening, never the facts.

- GitHub description: one factual sentence.
- Launch post: problem, result, proof, link.
- Technical post: one design decision, its tradeoff, its evidence.
- Community post: ask for feedback on one open problem; no bare link.
- Demo script: the failure, the project in use, the visible improvement.

## 4. Audit

To audit docs or prune AI self-talk, search the `*.md` and `*.html` files for `TODO`, `not done`, `AI note` and `no cost`, and group findings by file.

Remove:

- notes the agent left for itself, including notes on abandoned attempts;
- progress logs, `TODO`s and status tables for work that is finished, dropped or refactored;
- run IDs, hashes and verification prose outside `reports/` or commit messages;
- price or free-tier claims without a source and a date.

Keep current limitations, skipped checks, known risks and useful handoffs. A review request produces findings; a cleanup request produces the edits, with no second ask. When a plain diff cannot show a visual change, write a side-by-side HTML diff to `/tmp`.
