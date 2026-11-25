---
name: deep-research-with-instructions
version: 3
description: >-
  Resumable BFS research over any user-supplied topic, citing URLs / titles / Context7 IDs, state at `.plans/research-with-instructions/<topic>/`. Exa-first, then WebSearch/WebFetch; Context7 as fallback for official package docs. Asks only when sources conflict or scope is ambiguous. Triggers: "deep research X", "research X", "investigate X", "/deep-research-with-instructions". Researches external docs and the open web — not the user's codebase; for "how does this repo do X" questions, don't fire.
---

# Deep Research (With Instructions)

Resumable research over any user-supplied topic — frameworks, products, regulations, history, science, market context, anything. Walks an explicit tree of sub-questions; every finding is grounded in cited sources (URLs, Context7 doc IDs, page titles). Only writes inside `.plans/research-with-instructions/<topic>/`.

## Core rules

1. **Tree-first.** Every sub-question lives at a specific position in a branch tree maintained explicitly in `STATE.md` so no thread is forgotten.
2. **Breadth-first traversal.** Resolve all sibling branches at the current depth before descending. Depth-first tunnels into one rabbit hole and forgets the siblings.
3. **Exa-first, then everything else.** Default to Exa (`web_search_exa`, `get_code_context_exa`, `crawling_exa`, `deep_researcher_start`/`_check`). Use Context7 only when Exa returns thin or off-target results for an official package/API question. WebSearch/WebFetch fill gaps Exa can't cover. The user's codebase is not a research source for this skill — questions answerable only by reading the repo are out of scope. A glance to clarify what's being asked (e.g. confirm a package version from `package.json`) is fine; treating files as evidence is not.
4. **Pick the right Exa tool per branch.** See [SOURCES.md](SOURCES.md) for the decision matrix and citation formats.
5. **Ask only when sources are silent or split.** Use `AskUserQuestion` only when (a) reputable sources conflict and the right interpretation changes the research, (b) scope is genuinely ambiguous, or (c) the question can't be answered without a user-side fact (their version, their region, their constraint). Default to autonomous investigation.
6. **Persist before asking.** Update `STATE.md` and `FINDINGS.md` before any `AskUserQuestion` call. A session that dies mid-turn must be resumable.
7. **Cite evidence.** Every finding in `FINDINGS.md` and `REPORT.md` carries at least one citation — a URL, a Context7 library ID + section, or a fetched page title with date accessed. Conclusions without citations are not acceptable.
8. **Never fabricate sources.** If you can't verify a fact through a real lookup, mark the branch open and either widen the search or surface the gap to the user. No invented URLs, no invented quotations, no invented version numbers.
9. **No time-stamping inside findings beyond "accessed".** Cite when *you* read the source, not "as of <year>"; the underlying source may shift.

## State files

```
<cwd>/
└── .plans/research-with-instructions/
    └── <topic>/
        ├── STATE.md       # research tree + cursor + BFS queue + decisions log
        ├── FINDINGS.md    # append-only evidence log with cited sources
        └── REPORT.md      # final synthesis (only after user confirms)
```

Read [RESUMING.md](RESUMING.md) for the resume protocol and full schemas. Read [EXAMPLE.md](EXAMPLE.md) for a turn-by-turn walkthrough.

`.plans/research-with-instructions/` is **not** gitignored by default. When first creating the directory, tell the user. If they want it ignored, append `.plans/research-with-instructions/` to the project's `.gitignore` (create the file if absent) and confirm.

## Workflow

### 1. Init / resume

- **Always read `.plans/research-with-instructions/` first.** If any topic folder exists, list topics with status, cursor, and pending count, then ask which to resume — only start fresh when the user picks a new topic or the directory is absent. See [RESUMING.md](RESUMING.md).
- For a new topic: ask for a kebab-case slug (e.g. `react-server-components`, `eu-ai-act`). Create `.plans/research-with-instructions/<topic>/` with skeleton `STATE.md` and empty `FINDINGS.md`.

### 2. Scope clarification

Before seeding the tree, lock down scope so the research doesn't sprawl. In one bundle of 2–4 `AskUserQuestion` items, confirm:

- **Audience / depth.** Quick primer, decision-grade brief, or exhaustive deep-dive?
- **Boundary.** What is explicitly **in** and **out** of scope?
- **Constraints.** Version pins, region, jurisdiction, time horizon — anything that narrows the answer.
- **Preferred sources** when relevant (official docs only vs. allow community sources / blogs).

Record the answers under "Scope" in `STATE.md`. Skip questions the user already answered in their initial prompt.

### 3. Seed the tree

From the user's brief plus scope answers, propose **top-level research branches** — the major sub-questions whose union answers the prompt. Write them as level-1 `[ ]` entries in `STATE.md`. Show the tree and ask: _"Did I capture the right top-level branches, or should I add/remove any?"_

### 4. Traverse (BFS)

Loop:

1. Pick the next pending **leaf** branch in BFS order: shallowest depth first; among same-depth nodes, order by parent then child index.
2. **Investigate.** Choose the source per [SOURCES.md](SOURCES.md). For breadth-heavy branches that need many parallel lookups, spawn `Agent` with `subagent_type: general-purpose` and a self-contained prompt naming the question, allowed tools, and required citation format; capture the returned summary verbatim in `FINDINGS.md` with citations.
3. Record evidence + finding in `FINDINGS.md` (schema in [RESUMING.md](RESUMING.md)) with citations. In `STATE.md`: mark the branch `[x]`, update the **Cursor** section (active branch, next pending, depth), update the **BFS queue** (remove resolved branch; reorder if new children were added), and log the conclusion under **Decisions log**.
4. If the answer **opens new sub-questions**, append them as children — but do **not** descend until all current-depth siblings are resolved.
5. If sources truly cannot answer (silent / conflict / user-fact required), persist `STATE.md` + `FINDINGS.md` first, then call `AskUserQuestion` with one question, a recommended interpretation as the first option, and one-sentence reasoning.
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

- Don't fabricate URLs, quotations, version numbers, or source titles.
- Don't read the user's codebase to *answer* research questions — this skill researches external sources, not the repo.
- Don't tunnel: never descend while siblings are pending.
- Don't auto-finalize, don't record conclusions without citations, don't include "Recommendations" or "Next Steps" in `REPORT.md`.

## Companion files

- [SOURCES.md](SOURCES.md) — source-selection decision matrix, per-tool guidance, citation formats.
- [RESUMING.md](RESUMING.md) — resume protocol and full schemas for `STATE.md`, `FINDINGS.md`, `REPORT.md`.
- [EXAMPLE.md](EXAMPLE.md) — turn-by-turn walkthrough including an interruption and resume.
