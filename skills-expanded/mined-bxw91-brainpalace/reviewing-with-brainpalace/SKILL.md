---
name: reviewing-with-brainpalace
description: |
  Retrieval playbook for reviewing code, documentation and design with
  BrainPalace. Use when asked to "review this PR", "review this diff", "review
  this design", "check whether these docs are still true", "what else should
  change with this", "is this rename safe", "did we already decide this", or
  "what did we say about this last quarter".
  Supplies the context a reviewer cannot see in the diff — historical
  co-change, transitive dependents, superseded decisions — and the evidence bar
  every review comment must clear.
  Retrieval procedure ONLY: the judgment, the severity and the shape of the
  review belong to whoever is reviewing, never to this skill.
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

# Reviewing with BrainPalace

The retrieval playbook for the three review kinds — **code**, **documentation**
and **design**. One skill, because they differ in what they conclude and not in
what they must retrieve.

**This skill does not review anything.** It does not rank severity, does not
carry a checklist, and does not say what good code looks like. Plenty of
reviewers already do that — `/code-review`, `/security-review`, and whatever the
caller brought. What none of them can do is see the part of the truth that is not
in the diff: what this file historically changes with, what depends on the symbol
being renamed, and what was already decided about this. That is what you are here
to fetch.

**Mode selection, the `--json` contract, the `whoami` precondition and the
never-grep rule are NOT repeated here.** They belong to `using-brainpalace`.
The four investigation hops — locate, structure, history, provenance — belong to
`investigating-with-brainpalace`; when a review turns into "why is this here at
all", switch to that playbook rather than restating it.

## Start from the diff, not from the request

A review has something a general investigation does not: an exact, finite change
set. Use it. Every query below is anchored on a path or a symbol you can read out
of the diff, which is why review retrieval is cheap and precise.

```bash
git diff --name-only <base>...HEAD      # the files
git diff -U0 <base>...HEAD | grep -E '^[-+].*\b(def|class|func|function)\b'
```

**A file in the diff that the index does not hold is itself a review note** — say
so rather than reporting silence. Newly added files are the common case and are
fine; a long-lived file missing from the index means the review is partly blind.

## The three questions worth asking per changed file

### 1. What historically changes with this, and is missing here?

```bash
brainpalace graph cochange <path> --min-shared 2 --limit 20 --json
```

Files that historically change together with `<path>`, read out of git history.
`--min-shared 2` is the default noise floor — one shared commit is a coincidence.
Raise it when the answer is dominated by files that change with everything
(lockfiles, changelogs); lowering it below 2 is almost always wrong.

**The finding is the SET DIFFERENCE, not the list.** A co-change partner that is
absent from the diff is the review comment: *"`x.py` has changed with `y.py` in 7
of its last 9 commits; this diff touches only `x.py`."* Reporting the raw
co-change list back is not a review note, it is a dump.

**Historical co-change is correlation.** It is evidence that something is worth
checking, never proof that something is wrong — a partner may be absent for a
perfectly good reason, and the author knows that reason and you do not. Phrase it
as a question.

### 2. What transitively depends on what this changes?

```bash
brainpalace graph impact <symbol-or-path> --max-depth 3 --json
brainpalace graph path <changed> <suspected-dependent> --max-depth 6 --json
```

`graph impact` is the reverse-dependency closure — everything that transitively
depends on the node. `--max-depth` defaults to 3 and `--limit` to 200. Raise the
depth only when depth 3 returns an empty or implausibly small closure, and say
which depth produced the number you quote: a closure at depth 5 and one at depth 3
are different measurements, and quoting one as the other understates the blast
radius.

Run this on **every renamed, deleted or signature-changed symbol** — that is the
one review question where a ranked search is the wrong tool and the deterministic
closure is the right one. `--predicates` filters to one kind of coupling; omit it
when the question is "what would break".

`graph path` answers the follow-up a reviewer actually asks: *how* does the change
reach the thing you claim it affects. A claimed impact you cannot show a path for
is a guess.

### 3. Did we already decide this, and does the decision still hold?

```bash
brainpalace query "<subject> decision rationale" --mode hybrid --top-k 8 --json
brainpalace query "<subject>" --mode timeline
```

`--mode timeline` walks edge-validity and supersession — what a decision replaced
and what replaced it. This is the question that separates a useful design review
from a re-litigation: a change that contradicts a live decision is a finding, and
a change that contradicts a *superseded* one is correct and the reviewer is out of
date.

`--mode scan` reads the raw transcript archive, so "when did we discuss this" is
answerable even where session indexing is off. Cite the session, not your memory.

## Documentation review has one extra move

A doc review is a claim-by-claim check against code, and the useful retrieval is
per claim, not per document:

```bash
brainpalace query "<the exact symbol, flag or path the doc names>" --mode bm25 --top-k 5 --json
```

`bm25` because a doc's checkable claims are exact tokens — a flag, a key, a path,
a default. **A claim whose named token appears nowhere in the index is the
finding.** That is the one review conclusion this playbook does license you to
draw, because it is a retrieval result and not a judgment: the doc names something
that does not exist.

Do not grade prose. Check what it asserts.

## The evidence bar

Every review note you hand back cites one of: a `chunk_id`, a `source` path, a
graph edge, or a commit. A note that cites none is an opinion — and an opinion
delivered as a retrieval finding is worse than silence, because the author cannot
tell which it was.

**Ranked is not exhaustive.** `query` returns the top-k best matches, not every
match. "Nothing came back" is a statement about a ranked search, never about the
codebase — and in a review it is the single most damaging thing to say, because
"no prior decision found" reads as "there is none". When the question needs
completeness, use the deterministic paths (`graph impact`, `graph path`,
`--mode compute`, `--mode absence`) or widen (`--top-k`, `--mode multi`) and say
you widened.

**An empty result has a reason, and the response tells you which.** On an empty
`compute`/`scan`/`absence`/`timeline` response a top-level `coverage` object
carries `reason`:

| `reason` | What it means | What to say |
|---|---|---|
| `capability_off` | the feature is disabled for this project | "not answerable here", and name the switch |
| `store_empty` | nothing extracted or archived yet | "no data yet" — not "no such thing" |
| `unparsed_query` | scan only: the query compiled to no term — it never ran | reshape the query (`coverage.detail` says how); NEVER report it as absence |
| `no_match` | it ran; your query found nothing | the only one that is about the question |

Reporting `store_empty` as "we never decided this" converts a configuration fact
into a false claim about the project's history, in a review, where someone will
act on it.

## Stop rules

- **The diff is empty or unreadable** → say so; there is nothing to anchor on.
- **A changed file is not in the index** → report the blind spot, review the rest.
- **The closure is truncated** (`impact` hit `--limit`) → say so and quote the
  limit. A truncated closure read as complete understates the blast radius.
- **Co-change says nothing** (`--min-shared 2` returns empty) → that is a real
  answer for a young or isolated file. Do not lower the floor to manufacture one.
- **The finding needs a judgment call the caller owns** → hand back the
  retrieval and the question, not the verdict.
