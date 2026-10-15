---
name: lets-heavy-discussion
version: 2
description: >-
  Resumable, branch-tracking design interview that tracks every open branch in an explicit tree (so no branch is forgotten), persists state to `.plans/discussion/<topic>/` after every turn, traverses breadth-first to avoid tunnelling, and resumes exactly where the last session left off. Use when the user says "let's discuss", "let's talk through", "help me think through", "walk me through the tradeoffs", "I need to decide", "stress-test my design", or "let's continue our discussion" — especially for architecture, product, or design decisions with multiple branches, or to resume a discussion started in a previous session. Audit + interview only — never modifies code. Always recommends an answer; explores the codebase silently when the answer is in the code.
---

# Let's Heavy Discuss

A relentless, resumable design interview where every branch of the decision tree is tracked explicitly — depth-first tunnelling is forbidden, and a session reset never loses context.

## Core rules

1. **Tree-first.** Every question lives at a specific position in a branch tree. The tree is maintained explicitly in `STATE.md` so no branch is forgotten.
2. **Breadth-first traversal.** Resolve all sibling branches at the current depth before descending. Depth-first interviews tend to tunnel down one branch and forget the siblings — BFS prevents that.
3. **One question per turn.** Use the AskUserQuestion tool. Always include your recommended answer plus one-sentence reasoning.
4. **Explore code instead of asking when possible.** If an answer can be found by reading files or grepping, do that silently and record the finding in `TRANSCRIPT.md` rather than asking the user.
5. **Persist before asking.** Update `STATE.md` and `TRANSCRIPT.md` before every AskUserQuestion call. A session that dies mid-turn must be resumable.
6. **Never modify code.** Pure interview. Only writes inside `.plans/discussion/<topic>/`.

## State files

```
<repo or cwd>/
└── .plans/discussion/
    └── <topic>/
        ├── STATE.md       # branch tree + cursor + decisions log
        ├── TRANSCRIPT.md  # chronological Q&A (verbatim)
        └── FINAL.md       # design summary (only after user confirms completion)
```

**Read `RESUMING.md`** for the resume protocol and full schemas (STATE.md, TRANSCRIPT.md, FINAL.md). **Read `EXAMPLE.md`** for a turn-by-turn worked walkthrough.

`.plans/discussion/` is **not** gitignored by default — these are discussion artefacts, not local scratch. When first creating the directory, tell the user. If they ask for it to be ignored, append `.plans/discussion/` to the project's `.gitignore` (create the file if absent) and confirm.

## Workflow

### 1. Init / resume

- **Always read `.plans/discussion/` first.** If any topic folder exists, list topics with status (in-progress / finalized) and ask the user which to resume — only start fresh when the user picks a new topic or the directory is absent. See [RESUMING.md](RESUMING.md).
- For a new topic: ask the user to name it (slug form, e.g. `auth-system`, `payment-flow`). Create `.plans/discussion/<topic>/` with skeleton STATE.md and empty TRANSCRIPT.md.

### 2. Seed the tree

From the user's initial brief, extract the **top-level branches** — the major decisions the design needs to resolve. Write them as level-1 entries in STATE.md, all `[ ]` pending. Show the tree to the user and ask: _"Did I capture the right top-level branches, or should I add/remove any?"_

### 3. Traverse breadth-first

Loop:

1. Pick the next pending branch in BFS order: **shallowest depth first**; among same-depth nodes, order by parent index then child index (e.g. `[1.1, 1.2, 2.1, 2.2]`, never interleaved across parents). Container nodes that only group children (no question of their own) do not need their own decision — they're auto-resolved when all children resolve.
2. If the answer is in the codebase, explore (Read/Grep/Glob), record the finding in TRANSCRIPT.md, mark the branch `[x]` with the decision, log it under "Decisions". Continue.
3. Otherwise, formulate **one** question with a recommendation. Update STATE.md cursor → write TRANSCRIPT.md draft entry → call AskUserQuestion.
4. On answer: complete the TRANSCRIPT.md entry, mark the branch `[x]`, log the decision. If the answer **opens new sub-branches**, append them as children — but do **not** descend until all current-depth siblings are resolved.
5. If the user defers a branch, mark it `[~] — <reason>` and continue.
6. Loop until the queue is empty.

### 4. Finalize

When no `[ ]` branches remain:

- Show the resolved tree and decisions log.
- Ask: _"All branches resolved. Anything else to explore, or should I write FINAL.md?"_
- Only on explicit confirmation: write `FINAL.md` summarising the design and decisions, set STATE.md status to `finalized`.

## Recommendation format

Every AskUserQuestion call must include:

- The branch path in the question text (`[1.2 — auth strategy] …`).
- Claude's recommended answer as the **first** option, with `(Recommended)` suffix, per the AskUserQuestion convention.
- 2–4 alternative options.
- One-sentence reasoning in the question body.

## Checkpoint discipline

A **checkpoint** is one question + one answer + tree update. Update STATE.md (cursor + checkboxes + decisions) and TRANSCRIPT.md **before** each AskUserQuestion call so a mid-turn crash leaves a recoverable state. Never overwrite STATE.md without first reading it.

## What NOT to do

- Don't tunnel: never descend into a sub-branch while siblings at the current depth are still pending.
- Don't batch: one question per turn, even if siblings look independent.
- Don't auto-finalize: the user must confirm before FINAL.md is written.
- Don't modify code: this skill is interview-only.
