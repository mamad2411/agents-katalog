# Orchestrator Token Protocol

## Summary

**One-sentence:** A dispatch protocol for an orchestrator that fans work out to
subagents over a content CLI — search once and share identifiers, hydrate
through a sink, mark every child process as a subagent, and read the meter
around the fan-out so the retrieval bill is attributed instead of invisible.

**One-paragraph:** Retrieval looks free to an orchestrator because it does not
appear in its own context. A subagent that runs its own search spends nothing
the parent can see: the candidate set is assembled inside a fresh child
process, sent to a provider, and discarded. Repeat that per subagent and the
pipeline pays for the same corpus scan N times, in a cost line nobody is
reading. The protocol closes the leak with four moves that cost nothing to
adopt. The orchestrator performs the one search the fan-out needs and passes
**hash-IDs**, so children resolve instead of rank. Children hydrate with
`get-content --sink`, which writes bodies to disk and returns a short receipt,
so a body never transits a prompt. Every spawned process sets
`FAION_SUBAGENT=1`, which drops the transcript block and lands the child in the
shared no-transcript cache bucket where repeats are free. And the meter is read
before and after the fan-out, because a saving nobody measured is the failure
this methodology exists to prevent.

## Applies If (ALL must hold)

- An orchestrator spawns two or more subagents, each in its own OS process,
  and any of them may need corpus content.
- Retrieval is ranked by a model — so a search call carries a candidate set
  into a provider prompt and is billed per invocation.
- A meter or equivalent cost ledger exists. Without it the protocol is
  adopted on faith and the regression that motivated it cannot be seen.

## Skip If (ANY kills it)

- A single agent, no fan-out. There is no duplicate to eliminate; the shared
  cache already covers the repeat case.
- Retrieval is a local deterministic lookup with no model in the path — an
  exact-key or filesystem read costs nothing to repeat, so identifier passing
  buys only complexity.
- Subagents genuinely explore disjoint parts of the corpus and cannot know
  their targets in advance. Force one shortlist onto them and the orchestrator
  becomes the recall bottleneck; keep the searches, apply rules 2-4.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Six testable rules. R1 removes the duplicate scans; R4 is the one that keeps the others honest. |
| `content/03-failure-modes.xml` | Five ways a fan-out silently pays for retrieval more than once. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- `hierarchical-index-compression` — bounds what one index read costs. This
  methodology bounds how many times that read is paid; both are needed, and
  neither substitutes for the other.
- `retrieval-cost-per-answer-audit` — the measurement this protocol assumes.
  Run it to get the per-answer number the meter checkpoints compare against.
- `auto-evict-tool-results` — the same principle applied inside one context:
  keep the receipt, drop the body.
- `headless-cli-four-guards` — the invocation-level guards for the same
  spawned processes; `FAION_SUBAGENT=1` belongs to that env block.
