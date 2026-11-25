---
name: zeromem
description: "Use when the user asks about something from their own past Claude Code sessions — 'what did I do about X', 'last time we…', 'which project had that bug', 'how did I fix this before', 'did I already try…', 'khi nào tôi…', 'lần trước tôi đã làm gì', 'trong project cũ tôi đã…', 'tôi từng sửa lỗi này chưa' — or wants to search, index, or refresh their local session history. Runs Zero-Mem: a zero-token memory pipeline (entity–context graph + temporal hierarchy, dual-view retrieval, deterministic calibration) over ~/.claude/projects transcripts. No LLM call and no token spend happens inside the memory pipeline; the only model reading the evidence is you."
---

# ZeroMem — structured recall over the user's own session history

Zero-token structured retrieval over this user's real Claude Code transcripts,
implementing Zero-Mem (arXiv:2607.29377v1). Every memory operation — graph
propagation, PageRank, hierarchy walk, fusion, closure, calibration — is
deterministic arithmetic. The only model in the loop is you, reading what it
returns.

## When to use it

Use it when the answer lives in the user's **past sessions**:

- "what did I do about the ENOENT bug"
- "lần trước tôi xử lý auth trong TaskBot thế nào?"
- "which project was that BM25 fix in"
- "did I already try mean-pooling here?"

**Do not** use it for:

- anything in the current session or an open file — that is already in context;
- general knowledge or library docs — this only knows what the user has done;
- reading a specific file you already have the path to — just read the file.

## How to call it

```
zeromem recall "<query>" --top-k 5
```

If `zeromem` is not on PATH, `python -m zeromem recall "<query>"` is equivalent
and works wherever the package is importable. Use one of these two forms only —
never an absolute path to the launcher script, which differs on every machine.
If neither works the package is not installed; see "When something fails".

Useful flags:

| Flag | Use |
|---|---|
| `--project <SLUG>` | Hard-restrict to one project (slugs come from `status`) |
| `--session <ID>` | Hard-restrict to one session |
| `--since` / `--until` | ISO datetime bounds, e.g. `--since 2026-07-01` |
| `--json` | Every provenance field, machine-readable |
| `--timings` | Per-stage timing breakdown |
| `--no-daemon` | Force the slow in-process path (debugging) |

Examples:

```
zeromem recall "BM25 CSC caching fix" --top-k 3
zeromem recall "lỗi auth" --project <SLUG>          # slugs come from `zeromem status`
zeromem recall "what changed in the encoder" --since 2026-07-20 --json
```

**Speed.** The first call in a session takes ~40 s because it loads a 135k-unit
index and a sentence-transformer. A background daemon makes every later call
~1.5 s:

```
zeromem serve
```

It binds loopback only, holds ~3.3 GB resident, and exits after 30 idle minutes.
**Do not start it silently** — if you expect several recalls, tell the user the
one-line tradeoff and let them decide. `recall` works either way; the slow path
prints a hint to stderr, not an error.

## First, check whether the memory actually has it

Before quoting anything, read the `support=` field on the summary line. It is
a deterministic measurement of how much of the query's distinctive vocabulary
actually appears in the returned blocks — **not** a model's opinion.

| What you see | What it means | What to do |
|---|---|---|
| `support=supported` | the query's terms are present in the evidence | answer normally, quoting blocks |
| `support=weak` + `PARTIAL EVIDENCE` | only part of the question is covered | answer the covered part, say plainly what is not covered |
| `support=unsupported` + `WEAK EVIDENCE` | the query's distinctive terms are essentially absent | **say the memory does not have this.** Do not present the blocks as an answer |
| no `support=` field | the query had no distinctive term to check | judge from the blocks as usual |

When the notice appears, it names the exact terms it could not find, and
separately any term that **never appears anywhere** in the indexed history.
Those are facts you can repeat to the user: "nothing in your indexed history
mentions `kubernetes`" is checkable and true; "you never worked on
Kubernetes" is neither — the index may simply not cover that project (see
`status`).

The retrieval still returns its best five blocks under a weak verdict — that
is deliberate, so you can see them. It is not permission to use them as the
answer. Measured behaviour: on 20 questions whose answers were genuinely
absent, 20/20 drew a hedge and 0/20 were reported as supported
(`references/abstention.md`).

### "Searched specifically for the missing terms"

On a weak verdict only, recall looks up each missing term and reports **corpus
facts, not answers**. `occurs in 0 units` is the strongest statement available —
say it directly, it is checkable. `occurs in 4 unit(s)` plus `[P]` blocks means
the word exists only there; if those are incidental mentions, say the memory has
the word but not the answer. No section means every missing term was too common
to point at anything. `[P]` blocks came from looking up **one word**, not from
the ranked retrieval — never present them as the answer.

The reverse error is likelier in Vietnamese: a Vietnamese question over English
evidence can score low even though retrieval was right (2 of 3 measured false
hedges). If the blocks plainly do answer the question, trust them and say the
match was lexically thin — do not refuse evidence you can see is relevant.

## How to use the output — the provenance rule

Every block's body is **verbatim text from the user's own history**, carrying its
uid, timestamp, project, and session.

> Quote it, or cite its uid. Do **not** paraphrase a block into a claim about
> what happened. If the evidence is thin, say the evidence is thin. Never
> present recalled text as your own recollection, and never merge two blocks
> into one narrative the user did not write.

This is the difference between a memory that is auditable and one that
confabulates. The retrieval is deterministic and provenance-preserving right up
to the moment you summarize it — that moment is where the guarantee can be lost.

Block header:

```
[E1] main · uid=<uid> · 2026-07-14 22:48 +07 · <project> · session <id> · user/text
<verbatim text>
```

`main` = retrieved directly. `bridge via <entity>` = pulled in by the
entity–context graph because it shares that entity. `neighbor via <uid>` =
an adjacent turn included for context. Bridges and neighbours are **context**,
not answers — the user asked about the main hits.

## Reading the summary line

```
route=relational (rule 3) · ρ=0.6 · support=supported (0.89) · 5 main, 2 bridges, 1 neighbors · 0 LLM calls · 0 tokens · 1013 ms
```

- **`support`** — how much of the query's distinctive vocabulary the evidence
  covers, weighted by rarity (see the table above). Omitted when the query had
  no distinctive term to check.
- **`route`** — `relational` means the query connects things across sessions
  (comparison, aggregation, multi-entity); `local` means a single anchor plus
  recency. `rule N` is which deterministic rule fired.
- **`ρ`** — how much weight the primary view got in the fusion (0.6 by default).
- **counts** — how many blocks came from retrieval vs. from closure.
- **`0 LLM calls · 0 tokens`** — literal, by construction. The pipeline contains
  no model.

Use it to tell the user *why* these results: "it routed relational, so it
connected traces across three projects" is a real explanation.

## Index maintenance

```
zeromem status                 # what is indexed, what is not, is the graph stale
zeromem update                 # incremental refresh of everything already indexed
zeromem update --quiet         # silent when nothing changed (for a scheduled run)
zeromem build --scope <SLUG> --with-graph   # add a project not yet indexed
```

**Recall only sees indexed scopes.** `status` lists the unindexed ones. If the
user asks about a project that is not indexed, say so and give the `build`
command — do not report "no memory of that", which is a different and wrong
claim.

`status` also reports whether the graph covers the current units. If it says
`STALE: covers N of M indexed units`, recall's graph view is blind to the
difference — tell the user to run `update`.

## When something fails

| Symptom | What to do |
|---|---|
| `zeromem: command not found` | The package is not installed. Tell the user: `pip install git+https://github.com/viethuynh243/ZeroMem` (or `pip install -e .` in a checkout). Try `python -m zeromem status` first — it works without the console script. |
| `no index found` | Give the user the `zeromem build --scope <SLUG> --with-graph` command. **Never** run a full build yourself — on a dense tier it is a ~45-minute encode. |
| `no entity-context graph found` | `zeromem graph --all` |
| stderr hint about no daemon | Nothing is wrong; it was just slow. Mention `zeromem serve` if you will recall repeatedly. |
| stale daemon warning | `zeromem serve --stop`, then start a fresh one. |
| recall returns nothing | Say so plainly. Check `status` for whether that project is indexed at all before concluding the memory is empty. |
| `WEAK EVIDENCE` notice | Not a failure. Report that the memory does not appear to hold this, name the missing terms, and check `status` in case the relevant project is simply unindexed. |

## More detail

- `references/usage.md` — full CLI reference, troubleshooting, scheduling
- `references/architecture.md` — the pipeline stage by stage, mapped to the paper
- Measured evidence, not claims: `references/tiers.md` (encoder throughput),
  `references/corpus.md` (what the corpus contains), `references/entities.md`
  (extractor precision), `references/routing.md` (router accuracy),
  `references/recall-quality.md` (recall@k and ablations),
  `references/abstention.md` (does it know when it does *not* know),
  `references/latency.md` (cold start, daemon, memory)
- `references/method-notes.md` — retrieval-methodology ideas measured against
  this system, including two that were rejected on the numbers
