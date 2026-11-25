---
name: fact-request
description: Turns a fact a builder is missing into a structured request the collector can collect, instead of fetching it, guessing it, or stopping with "insufficient info". Use on a builder machine whenever the brief does not answer something a design depends on, when handoff or preflight fails, when a skill's research step would run on a builder, or when the user asks "can you look that up" on a machine that does not collect.
---

# Fact request

A builder does not collect. `research.mjs` and `decompose.mjs` refuse there (exit 2), and
a page fetched by hand, by a browser tool, or from memory is not evidence in this kit
(ADR-0010). The honest move is to name the fact precisely and hand it to the collector.

## The request file (the collector collects it automatically)

When the collector runs auto-collect (ADR-0148), write one file per fact, then commit and push it. This
is the only place under the collector's Git `research/` corpus a builder writes;
ADR-0052's local review of a received package is a separate workflow:

```
research/requests/<id>.json        id: lower-case letters, digits and dashes
{
  "fact":    "<the fact, as a question a page can answer>",
  "blocks":  "<the design decision that changes if it is guessed wrong>",
  "urls":    ["https://<the page that owns the fact>"],
  "queries": ["<a search, when no owner page is known>"],
  "prefer":  ["<owner domain>"],          optional
  "unknown": "U-NN",                      optional: an existing contract row
  "maxPages": 4,                          optional: at most the collector's cap
  "topic":   "<a whole new project>"      optional, instead of one fact in this one
}
```

The collector pulls it, checks it, adds the contract row and the plan entry, collects with
the same `research.mjs`, and pushes the corpus with its ledger, plus `<id>.result.json`
beside your request. Pull, and read the result:
- `collected`: captures were delivered. Read and judge them, then report review-only
  gaps in prose. The collector records the Findings, unknown closure, classified map
  and current authored brief in the Git corpus. Run handoff, preflight and
  `brief.mjs --state`; stop dependent building until the complete review is present
  (ADR-0150). The result alone does not authorize building.
- `partial`: credits ran out after some pages were collected. The collector pauses without
  switching transports; the result records the target, unknown, pages spent, and remaining
  allowance. The operator can top up and press Resume, after which the collector continues
  that same request without resetting its page cap.
- `refused`: its `problems` say why (a page on an internal address, too many pages, a
  missing field). Fix the request under a new id.
- `failed`: its `detail` says why. When no page could be fetched, its `next` says what to
  change - another owner page in `urls`, or a search in `queries`. Edit the request and push
  it: a changed request is processed again, on the contract row it already has.
- no result yet: the request is waiting, either for today's cap, for the operator to top up
  the credits, for the operator to approve a folder for new topics (a `topic` request), or
  for the collector to retry delivery of a previous result.

Never fetch the page yourself while you wait.

When the capture already answers the fact, ask the collector to finish its review;
do not submit another paid fetch request for classification, wording or brief currency.
ADR-0052 still permits reviewing and re-packaging a received local package without
collection; that is separate from editing the collector-owned Git corpus. In either
workflow approval remains derived from the existing corpus/review checks on any role.

## The request in prose (no auto-collect)

When the collector does not run auto-collect, write it in your report, the pull request,
or an issue - not into `research/`, which the collector owns. One request per fact:

```
Fact request - <project path>
Missing:   <the fact, as a question a page can answer>
Blocks:    <the design decision that changes if it is guessed wrong>
Map row:   <the D-n / S-n subtopic it belongs to, or "new subtopic">
Owner:     <the page that owns the fact: official docs, the repo at a tag, the pricing page>
Plan entry (for research/plan.json):
  { "url": "<owner page>", "why": "U-NN <short reason>" }
Contract row (for research/DISCOVERY.md):
  | U-NN | <question> | <why it blocks> | OPEN | |
Meanwhile: <what is being built that does not depend on it, or "stopped">
```

## Rules

- **Name one fact, not a topic.** "What is the burst limit of endpoint X on the free
  tier?" - not "research the API".
- **Name the owner page**, the one that owns the fact, never a write-up about it.
- **Never write the answer you expect into the request as if it were known.** If you
  have a prior, label it as one.
- **Stop the dependent work.** Building on a guessed value and "fixing it later" is the
  failure this kit exists to prevent.
- When handoff or preflight is what failed, the request says which check and quotes its
  output; that is the fact the collector needs.
