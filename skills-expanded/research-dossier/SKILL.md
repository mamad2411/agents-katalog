---
name: research-dossier
description: Answer a question from primary sources and record every source checked under `research/`. Use when the user asks for a topic researched, for the evidence behind a claim, or when a decision needs facts you would otherwise guess at.
---

Two artifacts, both required: an answer someone can act on, and a trail someone can re-walk.

Done when every claim in the answer carries a footnote, and every source you opened appears in `resources/` with a verdict.

Cite what already exists. When answering requires running something new — a benchmark, a script, a test — that is a prototype: build it there, then cite its result here.

## Where it goes

Put the folder where the repo already keeps such notes, matching that convention. Absent one, use `research/`. Say where you put it.

The folder's internal shape is fixed either way:

```
{notes-root}/YYYY-MM-DD-{slug}/
├── outcome.md
└── resources/
    └── {nn}-{query-slug}.md    # one file per search query
```

Read today's date from the system. `{slug}` is three to five kebab-case words naming the question.

## Steps

1. **Split the question.** Write the sub-questions that must each be answered before the whole one is. These become your queries.
2. **Search one query at a time.** Open that query's `resources/` file before you read anything, and log each result as you judge it — mid-flight, not reconstructed at the end.
3. **Read the source that owns the claim.** Official docs, specs, first-party APIs, the paper itself — and locally, the installed source in `node_modules`, the lockfile, the repo's own code. A package's shipped source outranks its documentation. A secondary write-up is a pointer to a primary source, not a substitute for one: follow it back and cite what it points at.
4. **Write `outcome.md`.** Where sources disagree, say so in the body, name the one you trust, and say why.

## outcome.md

```md
---
date: 2026-08-22
question: <verbatim, as the user asked it>
answer: <one or two sentences; the thing they can act on>
sources:
  - <url, or pinned local reference>
---

Long-form answer in markdown, with references as footnotes.[^1]

[^1]: [Title](url), section name.
[^2]: lodash@4.17.21 · src/index.js:340
```

`sources` lists only what you cited. Everything you opened and rejected lives in `resources/`.

Cite a local source as `{package}@{version} · {path}:{line}`, or `{repo}@{sha} · {path}:{line}` for the repo's own code. A bare path rots the moment the dependency moves.

## Downstream documents cite your sources, not you

This folder is a trail, and a trail is deletable. Anything durable that comes out of it, an ADR above all, restates the finding and cites what you cited: the vendor's reference, the spec, the pinned declarations, the manual page, a commit-pinned permalink. A document that points at `research/` instead is only checkable while this folder survives. Leaving the primary source easy to lift, one link per claim, is what makes that possible.

## resources/{nn}-{query-slug}.md

```md
# {the query, verbatim as run}

- Tool: <search engine, ripgrep, npm view, gh api, …>
- Params: <flags, filters, date range, site: scoping, paths searched, pages read>

| Source | Verdict | Why | Summary |
| --- | --- | --- | --- |
| [title](url) | used | first-party spec for X | one line of what it contributes |
| zod@3.23.8 · src/types.ts:1204 | used | the shipped implementation | one line of what it contributes |
| [title](url) | discarded | 2019 blog restating the spec | — |
```

Verdict is `used` or `discarded`. Every source you opened gets a row, including the ones that wasted your time — the trail earns its keep by stopping the next run re-opening them.
