---
name: deep-research-with-codebase
version: 2
description: >-
  Resumable codebase research that answers "how does this codebase do X" via BFS traversal of a research-question tree, with `file:line` citations and state at `.plans/research/<topic>/`. Investigates autonomously — asks only when the code can't answer. Triggers: "deep research X", "deep dive into the codebase", "investigate the codebase", "how does this codebase do X", "explain how X works in this repo", "trace how X flows". Answers come from reading code — for questions that need the user's own design answers rather than what the codebase does, don't fire. Read-only, codebase-only (no Context7/Exa/web).
---

# Deep Research with Codebase

A relentless, resumable research skill that answers "how does this codebase do X" by walking an explicit tree of sub-questions and grounding every finding in `file:line` evidence. Codebase-only — never asks the user when the code can answer, never reaches outside the repo for sources, never modifies code.

## Core rules

1. **Tree-first.** Every research sub-question lives at a specific position in a branch tree. The tree is maintained explicitly in `STATE.md` so no thread is forgotten.
2. **Breadth-first traversal.** Resolve all sibling branches at the current depth before descending. Depth-first tunnels into one rabbit hole and forgets the siblings.
3. **Codebase-first.** Investigate with Grep/Read/Glob/Bash in the main thread. Spawn `Agent` with `subagent_type: Explore` only for breadth-heavy lookups (multi-directory scans, "find all callers", cross-cutting patterns). Never use Context7, Exa, or web tools — this skill is codebase-only.
4. **Ask only when the codebase is silent.** Use `AskUserQuestion` only when (a) the question can't be answered from code, (b) two plausible interpretations split the research, or (c) scope is genuinely ambiguous. Default to autonomous investigation.
5. **Persist before asking.** Update `STATE.md` and `FINDINGS.md` before any `AskUserQuestion` call. A session that dies mid-turn must be resumable.
6. **Cite evidence.** Every finding in `FINDINGS.md` and `REPORT.md` carries `path/to/file.ext:lineno` references. Conclusions without citations are not acceptable.
7. **Never modify code.** Pure read-only audit. Only writes inside `.plans/research/<topic>/`.

## State files

```
<repo or cwd>/
└── .plans/research/
    └── <topic>/
        ├── STATE.md       # research tree + cursor + BFS queue + decisions log
        ├── FINDINGS.md    # append-only evidence log with file:line citations
        └── REPORT.md      # final synthesis (only after user confirms)
```

Read [RESUMING.md](RESUMING.md) for the resume protocol and full schemas. Read [EXAMPLE.md](EXAMPLE.md) for a turn-by-turn walkthrough.

`.plans/research/` is **not** gitignored by default. When first creating the directory, tell the user. If they want it ignored, append `.plans/research/` to the project's `.gitignore` (create the file if absent) and confirm.

## Workflow

### 1. Init / resume

- **Always read `.plans/research/` first.** If any topic folder exists, list topics with status, cursor, and pending count, then ask which to resume — only start fresh when the user picks a new topic or the directory is absent. See [RESUMING.md](RESUMING.md).
- For a new topic: ask for a kebab-case slug (e.g. `auth-flow`, `payment-webhooks`). Create `.plans/research/<topic>/` with skeleton `STATE.md` and empty `FINDINGS.md`.

### 2. Discovery (silent)

Before seeding the tree, scan the repo so subsequent branches reflect actual structure. Record briefly under a "Project context" section in `STATE.md`:

- Language(s), package manager, build/test config (read `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc. as present).
- Top-level directories and likely entry points.
- Frameworks in use (inferred from manifests and imports).

No user questions in this phase.

### 3. Seed the tree

From the user's brief plus the discovery scan, propose **top-level research branches** — the major sub-questions whose union answers the user's prompt. Write them as level-1 `[ ]` entries in `STATE.md`. Show the tree and ask: _"Did I capture the right top-level branches, or should I add/remove any?"_

### 4. Traverse (BFS)

Loop:

1. Pick the next pending **leaf** branch in BFS order: shallowest depth first; among same-depth nodes, order by parent then child index.
2. **Investigate.** Default to main-thread Grep/Read/Glob/Bash. If the branch is breadth-heavy, spawn `Agent` with `subagent_type: Explore` and a self-contained prompt that names the question and the search hints; capture the returned summary verbatim in `FINDINGS.md` (entry format: see [RESUMING.md](RESUMING.md)) with citations.
3. Record evidence + finding in `FINDINGS.md` (entry format: see [RESUMING.md](RESUMING.md)) with `file:line` citations. In `STATE.md`: mark the branch `[x]`, update the **Cursor** section (active branch, next pending, depth), update the **BFS queue** section (remove the resolved branch; reorder if new children were added below), and log the conclusion under **Decisions log**.
4. If the answer **opens new sub-questions**, append them as children — but do **not** descend until all current-depth siblings are resolved.
5. If the codebase truly cannot answer (or two interpretations split the work), persist `STATE.md` + `FINDINGS.md` first, then call `AskUserQuestion` with one question, a recommended interpretation as the first option, and one-sentence reasoning.
6. If the user defers a branch, mark it `[~] — <reason>` and continue.
7. Loop until the queue is empty.

### 5. Finalize

When no `[ ]` branches remain:

- Show the resolved tree and a one-paragraph summary of key findings.
- Ask: _"All branches resolved. Anything else to investigate, or should I write `REPORT.md`?"_
- If `REPORT.md` already exists, ask before overwriting — never silently clobber a prior run.
- Only on explicit confirmation: write `REPORT.md` (schema in [RESUMING.md](RESUMING.md)) and set `STATE.md` status to `finalized`. The report contains summary + per-branch findings with citations + open questions + deferred branches. **No** Recommendations or Next Steps — this skill produces findings, not advice.

## Anti-tunnelling reminder

Before each new investigation, re-read the BFS queue. If you're about to investigate at depth N+1 while any depth-N sibling is still `[ ]`, **stop and reorder**. Tunnelling is the failure mode this skill exists to prevent.

## What NOT to do

- Don't modify code; this skill is read-only.
- Don't use Context7, Exa, web search, or any external research tool — codebase-only.
- Don't tunnel: never descend while siblings are pending.
- Don't auto-finalize: the user must confirm before `REPORT.md` is written.
- Don't record conclusions without `file:line` citations.
- Don't include "Recommendations" or "Next Steps" in `REPORT.md`.

## Companion files

Each covers a distinct domain (per the split-by-domain threshold).

- [RESUMING.md](RESUMING.md) — resume protocol and full schemas for `STATE.md`, `FINDINGS.md`, `REPORT.md`.
- [EXAMPLE.md](EXAMPLE.md) — turn-by-turn walkthrough including a mid-investigation interruption and resume.
