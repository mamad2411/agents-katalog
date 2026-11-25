---
name: retrieve-context
description: Use before answering any question about code, conventions, ownership or past decisions that is not already on disk in front of you — routes the question to the right retrieval backend, on a token budget, and decides where what you learn gets written back
---

# Retrieving Context

## Overview

**Core principle: search before you answer, read what is on disk instead of
retrieving it, and spend a budget you chose rather than a default you inherited.**

You have up to two retrieval backends and they do not overlap. Which are
present is not configuration — it is whether their tools are in your tool
surface. Route by question, degrade quietly when a backend is missing, and never
stall waiting for an optional one.

| Backend | Tools | Corpus | Optional? |
|---|---|---|---|
| **moedex** | `mcp__moedex__*` | the code corpus the *asking user* can see in GitLab | optional — degrade to {read}/{search} when absent |
| **moe-memory** | `mcp__plugin_moe-memory_moe-memory__*` | this machine: conversation turns and journal entries | default memory store |

## The rule that fires first

**A file in the working tree is read, never retrieved.** {read} and {search}, every
time. This holds whether or not the repo is in the retrieval corpus, and it is
not a preference about cost: retrieval returns the corpus's *snapshot* of a
file, and your uncommitted edit is not in it. Reading is both cheaper and more
current, which is the whole argument.

**A corollary that expires: a repo absent from the corpus still answers.**
moedex returns its best match for every query, and its best match for a
question about code it has never seen is a plausible answer about different
code, with a real file path attached. Verified 2026-09-01 against the live
daemon: a query naming Moe's own symbols (`moe-mint`, `moe-doctor`, `probes`,
the `hard`/`soft` probe fields) returned a design document from an unrelated
repo at score 0.029. Moe is deliberately not indexed yet — that will change,
and when it does this paragraph is a dated observation rather than a rule. The
rule above it does not change: the corpus will still lag your working tree by
at least a sync.

**Gate on score, not on rank.** moedex always returns its best match, and its
best match for a question it cannot answer is noise at the top of the list.
moedex reports a `score` per block; a top hit around 0.03 is a miss, not an
answer. Say you did not find it rather than reporting rank 1.

## Routing

Route each question to its baseline: moedex for code-structure questions,
moe-memory for anything about prior work, and {read}/{search} for anything
already in the working tree.

| Question | Baseline |
|---|---|
| A file in the working tree | {read} / {search} — the corpus lags your edits |
| "Where is this symbol in a repo you are not editing?" | `search_context` with `graph_depth: 1` — one budgeted, graph-annotated call |
| "Blast radius of this change across repos?" | `impact_analysis` |
| A prior decision, ownership, a convention, or anything discussed before | `search_journal` + `search_conversations` — search this before answering from code or from first principles |
| "What did we say, have I done this before?" | `search_conversations` |
| "What did *I* note about this repo?" | `search_journal` |

## Budgets

Defaults are generous and you inherit them by saying nothing.

- **`search_context`** takes `token_budget` and honours it: asking 1200 returned
  `token_estimate: 732` with `truncated: true`. Its own default is 8000. Pass a
  budget; read `truncated` and `clipped` in the reply and say so if you were cut
  off rather than presenting a partial answer as whole.
- **`graph_depth: 0`** when you only want text. Depth 1 populates a `neighbors`
  field per block, but it comes back empty for prose blobs — you pay the
  traversal and get `bucket_totals` of zero. Depth earns its keep on code
  symbols only.
- **`read_conversation`** has no ceiling. Bound it by asking a narrower
  question, not by truncating the answer afterwards.

**Delegate the retrieval, not the conclusion.** The cheapest budget is a
subagent's context instead of yours: dispatch `search-moedex` (`model:` {model-fast},
a narrow tool allowlist, a hard word cap) and the raw blocks never enter this
window. `remembering-conversations` (in the memory plugin, when installed)
does the same for transcripts, and its skill text measures the saving at
50-100x.

## Reproducibility, and what may be cited

**A moedex answer is scoped to the asking user's GitLab access.** Two engineers
running the same query can get different results, so a moedex finding is not
reproducible for a reader who is not you.

Anything destined for a shared artifact — an MR description, a plan, a written
decision, a comment someone else will read — needs a citation your reader can
re-run. Ground it in the working tree: a re-fetchable path in a public repo,
not the corpus.

## Write-back

Nothing you learn survives the session unless you decide where it goes. Route by
record type, because the shape of the record forces it:

| What you learned | Where it goes | Why there is no choice |
|---|---|---|
| A conversation turn | local, harvested automatically | — |
| A durable fact: decision, ownership, convention, resolved question, or one that supersedes an earlier note | `process_thoughts` to the journal, when moe-memory is connected | it is the only durable store; note the supersession in the text — moe-memory has no claim graph to link it structurally |
| The same fact, moe-memory absent | say it in the answer and move on | a fact written nowhere is better than a call that errors |
| A note only useful to you | `process_thoughts`, local | — |

Write at the **end** of the work, in one batch, once the fact has stopped
changing — not at the moment you first believe it.

## When a backend is missing or slow

- **moedex absent, or up but not answering.** It is a single local daemon with
  a large mmap to warm; a slow start is routine, not an incident. Do not retry
  in a loop and do not tell the user the work is blocked. Answer
  code-structure questions from {read}/{search} where the repo is in the working
  tree, and say plainly when a repo outside it is not checkable.
- **Only the working tree.** {read} and {search} answer more than you expect. Say
  what you could not check rather than guessing at it.

## Red flags

- Answering a question about a file that is open in front of you from a
  retrieval call.
- Reporting a top hit without looking at its score.
- Passing no `token_budget`, then pasting the result wholesale.
- Citing a moedex `abs_path` in an MR description.
- Journaling something that will be false next week as if it were a durable
  fact.
- Telling the user retrieval is unavailable when only the optional backend is.
