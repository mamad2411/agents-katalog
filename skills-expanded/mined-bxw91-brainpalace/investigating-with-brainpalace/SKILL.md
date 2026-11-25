---
name: investigating-with-brainpalace
description: |
  Shared history-and-structure retrieval playbook for BrainPalace investigations.
  Use when asked "why is this code here", "when did this change", "what else
  changes with this file", "what depends on this", "is this dependency
  appropriate", "does this violate layering", "how did this decision evolve",
  "trace the blast radius", or "reconstruct how this got this way".
  Provides the ordered retrieval hops — locate, structure, history, provenance —
  plus the evidence bar every claim must clear.
  Retrieval procedure ONLY: the charter, the question a caller answers and the
  shape of its output belong to the calling agent, never to this skill.
license: MIT
allowed-tools:
  - Bash
  - Read
metadata:
  version: 1.0.0
  category: ai-tools
  author: bxw91
  last_validated: 2026-07-26
last_validated: 2026-08-05
---

# Investigating with BrainPalace

The **shared** retrieval playbook for questions about how code got this way and
how it hangs together. Two agents load it — `code-archaeologist` (history) and
`architecture-reviewer` (structure) — and it exists precisely so that procedure
lives in one file instead of drifting across two agent bodies.

**This skill is procedure, not charter.** It says which hops to run and what
counts as evidence. It does NOT say what you are investigating, what question you
answer, or what your output looks like — that is your own charter, and it lives in
your agent body. If you are reading this without one, you are a caller using the
playbook directly; that is fine, and the same evidence bar applies.

**Mode selection, the `--json` contract, the `whoami` precondition and the
never-grep rule are NOT repeated here.** They belong to `using-brainpalace`, which
every caller of this skill also declares. Start there; come back for the hops.

## The four hops, in order

Run them in order. Each narrows the next: an unlocated subject makes every
structural query a guess, and structure without history is a snapshot presented as
a cause.

### Hop 1 — Locate the subject

Turn the words in the request into a node the graph actually holds. A file path, a
symbol, a decision.

```bash
brainpalace query "<symbol or exact path>" --mode bm25 --top-k 5 --json
```

`bm25` on purpose: an exact symbol/token/path needs no embedding round-trip. Take
`source` from the top hit as the node name for hops 2 and 3.

**A subject you cannot locate is the finding.** Say the index does not hold it —
do not proceed to run structural queries against a name you invented.

### Hop 2 — Structure: what depends on it, and how does it connect

```bash
brainpalace graph impact <node> --max-depth 3 --json
brainpalace graph path <src> <dst> --max-depth 6 --json
```

`graph impact` is the reverse-dependency closure — everything that transitively
depends on `<node>`. `--max-depth` defaults to 3 and `--limit` to 200; raise the
depth only when depth 3 returns an empty or implausibly small closure, and say in
your output which depth produced the number you are quoting. A closure at depth 5
and one at depth 3 are different measurements, and quoting one as the other is how
a blast radius gets understated.

`graph path` gives the shortest edge paths between two nodes and answers "how does
A reach B at all". `--domains` accepts `code,doc,session,git` — narrow it when the
question is about one substrate (`--domains git` for history-only connections).

`--predicates` on `impact` takes a CSV filter over the 13 live relationship
predicates. Use it when the question is about one kind of coupling; omit it when
you are asking what would break.

### Hop 3 — History: what changed with it, and what belief it superseded

```bash
brainpalace graph cochange <node> --min-shared 2 --limit 20 --json
brainpalace query "<subject>" --mode timeline
```

`graph cochange` reads git history and returns files that historically change
together with the node. `--min-shared 2` is the default noise floor — one shared
commit is a coincidence. Raise it when the result is dominated by files that
change with everything (lockfiles, changelogs); lowering it below 2 is almost
always wrong.

`--mode timeline` walks edge-validity and supersession — how a belief or decision
evolved, and what replaced it. It is the mode that answers "when did this change"
with something other than a commit list.

### Hop 4 — Provenance: cite the commit, not the vibe

A plain query surfaces `git_commit` chunks alongside code and doc chunks. There is
no `--source-types git_commit` — that flag takes `doc,code,test` only. Read the
`source` field.

```bash
brainpalace query "<subject> rationale" --mode hybrid --top-k 8 --json
```

`start_line` / `end_line` are `null` on `git_commit` chunks (and on doc, memory and
reference chunks) — only code chunks carry line data. Cite `source` and
`chunk_id`; do not fabricate line numbers for a chunk that has none.

## The evidence bar

Every claim you hand back cites one of: a `chunk_id`, a `source` path, a graph
edge, or a commit. A sentence that cites none is a guess, and the caller cannot
tell your guesses from your findings unless you mark them.

**Ranked is not exhaustive.** `query` returns the top-k best matches, not every
match. "Nothing came back" is a statement about a ranked search, never about the
codebase. When the question needs completeness, prefer the deterministic paths —
`graph impact`, `graph path`, `--mode compute`, `--mode absence` — or widen
(`--top-k`, `--mode multi`) and say you widened.

**An empty result has a reason, and the response tells you which.** On an empty
`compute`/`scan`/`absence`/`timeline` response a top-level `coverage` object
carries `reason`:

| `reason` | What it means | What to say |
|---|---|---|
| `capability_off` | the feature is disabled for this project | "not answerable here", and name the switch |
| `store_empty` | nothing extracted or archived yet | "no data yet" — not "no such thing" |
| `unparsed_query` | scan only: the query compiled to no term — it never ran | reshape the query (`coverage.detail` says how); NEVER report it as absence |
| `no_match` | it ran; your query found nothing | the only one that is about the question |

Reporting `store_empty` as "there is no history of this" is the single most
damaging mistake available in this playbook: it converts a configuration fact into
a false claim about the code.

## Stop rules

- **The subject did not resolve** (hop 1 empty) → report that; no further hops.
- **Two hops agree and the third is silent** → report the two, name the silence.
  Silence is not corroboration.
- **The closure is truncated** (`impact` hit `--limit`) → say so, and quote the
  limit. A truncated closure read as complete understates the blast radius.
- **The answer needs a judgment your charter does not give you** → hand back the
  retrieval, not the verdict.
