---
name: lyra-council
description: "Five-advisor deliberation engine. Spawns five subagents in parallel, each with a fixed persona (Contrarian, First Principles, Expansionist, Outsider, Executor). They peer-review each other anonymously. A chairman synthesizes a verdict: where the council agrees, where it clashes, blind spots caught, the recommendation, and the one thing to do first. Every session is saved to .lyra/council/ so future councils can read what past councils concluded."
compatibility: "Task tool for parallel subagent spawning. Reads CLAUDE.md and memory/ for context. Writes to .lyra/council/."
---

# lyra-council

## What it does

Runs a decision through five advisors who think from different angles, then synthesizes their independent analysis into a verdict a single pass could not produce. Each advisor is a separate subagent spawned in parallel, not one model roleplaying five experts. They peer-review each other's outputs anonymously. A chairman resolves the round into a recommendation.

The council is for decisions where being wrong is expensive: a launch, a pivot, a hire, a refactor strategy. It is wasted on questions with one right answer, on creation tasks, or on casual validation seeking.

Every session is saved to `.lyra/council/sessions/` as Markdown — flat frontmatter for the queryable fields, verbatim prose for the deliberation — with a permanent append-only digest ledger at `.lyra/council/ledger.md` that doubles as the index. The store is local runtime state: the skill keeps it git-ignored and refuses to write where `.lyra/` is tracked. Before convening, the skill greps the ledger for past sessions whose tags or topic overlap and feeds their verdicts to the advisors. The second council on pricing knows what the first concluded.

## When to convene

Convene when the user faces a genuine decision with stakes, multiple options, and uncertainty. Trigger phrases include "council this", "run the council", "pressure-test this", and "should I X or Y" when a real tradeoff is present. Do not convene for factual lookups, creation tasks, or a casual "should I" with nothing on the line.

## The workflow

1. Frame the question. Read the user's raw question. Scan the workspace for context — `CLAUDE.md`, `memory/`, files the user referenced. Reframe as a neutral prompt all five advisors receive. Include the core decision, the key context, and what is at stake. No opinion from you.
2. Query memory. Grep `.lyra/council/ledger.md` for sessions with overlapping tags or topic. Pull their recommendations and first actions into the framed question as prior-session notes. If the store still holds the JSON-era schema (an `index.jsonl` exists), run the one-time migration in `references/memory-schema.md` first.
3. Spawn five advisors in parallel. Use the Task tool, one subagent per advisor. Each gets its persona, the framed question, prior-session notes, and the instruction to lean fully into its angle without hedging. Personas live in `references/advisor-personas.md`. The spawn template is below.
4. Collect responses. Wait for all five. If one times out, note it and proceed with four. Never synthesize with fewer than four.
5. Peer review. Anonymize responses as A through E with a randomized mapping. Spawn five reviewer subagents in parallel. Each sees all five anonymized responses and answers three questions: which is strongest and why, which has the biggest blind spot, what did all five miss. The protocol is in `references/peer-review-protocol.md`.
6. Chairman synthesis. One agent gets the framed question, all five de-anonymized responses, and all five peer reviews. It produces the verdict using the format below. The chairman may side with a minority if the reasoning supports it.
7. Save the session. Run the git guard first (`references/memory-schema.md`): ensure `.lyra/` is ignored, and stop — reporting the untrack commands, never running them — if `.lyra/` is tracked. Then write the full record to `.lyra/council/sessions/{id}.md` and append the session's digest block to `.lyra/council/ledger.md`. Both writes must succeed before the verdict is presented as final.
8. Present the verdict in chat.

A caller may explicitly request a condensed round — five advisors and chairman synthesis, no peer-review round — for plan gates and other low-stakes checkpoints. The session declares the deviation in its Peer review section, and a condensed verdict carries less weight than a full-protocol one; decisions with real stakes get the full protocol.

## The advisor spawn

Each advisor is spawned as a Task subagent with this prompt, persona inserted per advisor:

```
You are {advisor_name} on a five-advisor LLM council.

Your thinking style: {persona}

The question brought to the council:
---
{framed_question}
---

Prior council sessions on related topics (build on or contradict; do not ignore):
{prior_session_notes or "none"}

Respond from your perspective only. Lean fully into your angle. Do not hedge and do not try to be balanced — the other advisors cover the angles you do not. If you see a fatal flaw, name it. If you see massive upside, name it.

150 to 300 words. No preamble. Start with the analysis.
```

The five default personas — Contrarian, First Principles, Expansionist, Outsider, Executor — are in `references/advisor-personas.md`. A caller may substitute its own five; lyra-docs passes accuracy, citations, slop, repetition, and completeness for its per-file gate. The orchestration is unchanged.

## The chairman synthesis

The chairman receives the framed question, the five de-anonymized advisor responses, and the five anonymized peer reviews. It produces the verdict in this shape:

```
## Council Verdict: {short topic}

### Where the council agrees
[Points multiple advisors converged on independently. High-confidence signals.]

### Where the council clashes
[Genuine disagreements. Present both sides. Explain why reasonable advisors disagree.]

### Blind spots the council caught
[Things that emerged only through peer review.]

### The recommendation
[A real answer with reasoning. Not "it depends". The chairman may side with a minority.]

### The one thing to do first
[A single concrete next step. Not a list. One thing.]
```

## Memory

Sessions live under `.lyra/council/` — local runtime state, never committed:

```
.lyra/council/
├── sessions/
│   └── council-{YYYY-MM-DD-HHMM}-{shortid}.md
└── ledger.md
```

Each session file is the full record in Markdown: flat single-line frontmatter for the queryable fields (id, date, topic, tags, refs, advisor set), then verbatim prose under fixed headings — question, the five advisor responses de-anonymized, the peer reviews with their `Mapping:` line, the verdict. `ledger.md` is the permanent tier and the only index: an append-only digest block per session (topic, tags, recommendation, first action, one clause per advisor) plus lifecycle events. An LLM reads and writes both directly — no parsing, no escaping — and a human opens them and reads a document. The full schema, the git guard, query patterns, and the JSON-era migration are in `references/memory-schema.md`.

Write-once governs content: session files and ledger blocks are never edited. It does not promise a body lives forever — once the global task that convened a council is settled, the owner may prune full session bodies; each pruned file leaves a `pruned` event in the ledger, and its digest, permanent since save time, remains the record. Pruning never runs on an inferred "task finished" signal: the skill proposes, the owner confirms. If a decision is revisited, a new session references the prior one in `refs:`. The ledger chain is the audit trail.

## Composes with

- `lyra-docs` — invokes lyra-council for its per-file review gate. lyra-docs passes its own five advisors and the draft file as the question. The orchestration is unchanged.
- `lyra` — when prompt optimization surfaces a real decision (which platform, which structure), convene a council before shipping.
- `lyra-code-review` — for pre-merge calls with genuine tradeoffs (architectural direction, breaking change), a council pressure-tests the decision.
- `lyra-clean-architecture` — when the pattern choice is contested for a specific service, the council debates it.

The external `llm-council` skill covers similar ground without memory or composition. Inside the Collection, lyra-council is preferred because it persists and composes.

---

_Part of the [skill collection](../README.md)._