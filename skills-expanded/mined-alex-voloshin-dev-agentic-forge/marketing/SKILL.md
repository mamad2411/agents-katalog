---
name: marketing
description: Outward-facing marketing work with cited evidence — market and competitor analysis, go-to-market strategy and positioning, offer, pricing and packaging design, landing, social and ad copy, and GEO/SEO audits of a page for AI-search citability. Use for any of these. Not product requirements or a PRD (product), researching a feature or technical approach (research), or system design (architecture).
allowed-tools: Read, Grep, Glob, Bash, Task, Write, Edit, WebSearch, WebFetch
---

# Marketing (domain router)

The marketing domain: turn a product into market understanding, a go-to-market strategy, and
on-brand content. This is one router skill — it dispatches to the sub-procedure in `references/`
for the task at hand, gathering evidence itself (`WebSearch` / `WebFetch`) or via the built-in
`Explore` agent for a repo sweep. The product
requirements themselves are the `product` skill's job; this is everything outward-facing.
(Design: ADR 0022 and `docs/architecture/product-marketing.md` in the agentic-forge repository —
not shipped with the plugin.)

## When to use

Market or competitor research, go-to-market / positioning / channel strategy, offer / pricing /
packaging design, marketing content (landing copy, social, ad/paid), or a GEO/SEO audit of a page
for AI search readiness. **Not** for the product spec / PRD (`product`), researching the
feature or technical options (`research`), or the technical design (`architecture`).

## Evidence discipline (non-negotiable)

The failure mode of generated marketing is confident, low-signal fluff. So every output obeys:

- **Cite or mark.** Every market-size, competitor, or performance claim cites a source, or is
  explicitly labelled an assumption. Never state a bare figure as fact.
- **No fabrication.** If the evidence has no number (e.g. no reliable TAM), say so — do not invent
  one. Name *specific* competitors, never "various players".
- **No unsupported superlatives** in content — claims trace to real proof points.

## Pick the sub-area

| Task | Reference | Output |
| --- | --- | --- |
| Market sizing, segments, competitor landscape | [references/market-research.md](references/market-research.md) | `market-brief` |
| Positioning, GTM, channels, messaging | [references/strategy.md](references/strategy.md) | `marketing-strategy` |
| Offer / pricing / packaging design | [references/offer-design.md](references/offer-design.md) | offer doc |
| Landing copy, social, ad / paid content | [references/content.md](references/content.md) | content files |
| GEO / SEO audit of a page or content | [references/geo-content.md](references/geo-content.md) | audit report |

## Process

> **Deliver in isolation** — when a `<feature-slug>` is in play, write into the feature's
> shared documentation worktree rather than the checkout, and deliver the result as a pull
> request (see [doc-delivery](../../patterns/doc-delivery.md)). One worktree and one PR per
> **feature**, shared by every document phase — that is what lets the next phase read what
> this one wrote. Skip it for a one-off document outside a feature flow. A repo with no remote (or
> no `gh`) still commits — on `docs/<slug>`, reported as not pushed / no PR — never a failed phase.

1. **Identify the sub-area** from the request and read its reference for the procedure + rubric.
2. **Gather evidence.** Use provided research/notes if present; otherwise gather it **live with
   `WebSearch` / `WebFetch`** (analyst reports, competitor sites, pricing pages) — or fork the
   built-in `Explore` agent via `Task` for a repo / notes sweep, and a fresh `general-purpose`
   subagent per web track when fanning out (there is no `research` *role*; `research` is the
   feature-flow skill) — **keeping every source URL**. Then
   apply the evidence discipline above (cite or mark every claim; no fabrication).
3. **Synthesize** the sub-area's output: the handoff artifact — `market-brief` (frontmatter `type`, `feature`, `status`, `competitors`, `segments`, `sources`) or `marketing-strategy` (`type`, `feature`, `status`, `positioning`, `channels`), each written with `review_decision: revise` until the loop exits — validated by the read-back below —
   **valid YAML: quote any value containing a colon**, which a cited source URL always has, or the
   whole artifact fails to parse
   (see [handoff.md](../../patterns/handoff.md)); or the untyped deliverables per the reference —
   content files, the offer doc, or the audit report — grounded in the evidence and the upstream
   `prd.md` where relevant. **A content file is the thing that gets published**: its whole
   contents are the post or the copy, with no title heading and no editorial note (publishing
   guidance goes in your report and the calendar), and it has a size to hit:
   **X at most 280 characters; LinkedIn 1,300-1,900** (below reads thin, above loses dwell);
   short-form elsewhere under ~1,000. `wc -m` each file and state the counts in your report
   before you finish — a file outside its band is unfinished, not a draft to explain away. The
   numbers are here and not only in `references/content.md` because a rule binds only the
   sessions that read it, and a session that never opens the reference wrote 847 characters
   against LinkedIn's "~3,000-char limit", five runs out of five (ADR 0099).
   Then **read the file back** — `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" handoff-load --path <path> --type market-brief` (or `--type marketing-strategy`) —
   and fix whatever it reports: this reads the file, so it sees the YAML you typed, and a single
   malformed value (a flow sequence with prose after it, an unquoted `:`) leaves an artifact the
   next phase cannot read (ADR 0096).
4. **Adversarial claims pass (bounded).** Fork a fresh `reviewer`/skeptic (via `Task`) to attack
   the draft against the evidence discipline above — every claim **cited or marked an assumption**,
   **no invented figures**, competitors named specifically, **no unsupported superlatives** — then
   fix what it flags worst-first. This is the guard against the fluff failure mode above.
   **External reviewer lens (on by default, ADR 0057/0062):** when `external_reviewer.enabled`
   (settings), also run the external reviewer over the deliverable —
   `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/external_review.py" --target <worktree>/<the deliverable> --repo <worktree> --kind marketing`; codex attacks the same evidence discipline as an
   independent-model lens and its `findings` fold into the same worst-first revision. It **degrades
   gracefully** (absent/disabled codex is skipped, not a failure; **exit 3 is a failed lens**, not a skip — record it in the round and tell the user) and its findings are **advisory**
   (prompt-injectable) — verify before acting. **Persist each round** — one `review-<artifact>-<iteration>.md` per round under `docs/sdlc/<feature-slug>/`, aggregating **both** lenses; on `proceed` keep only the final round, on `escalate` keep them all (naming + lifecycle: [review-loop.md](../../patterns/review-loop.md)). **Exit criterion (the shared, tested rule):** each
   round, compute `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" review-decision --verdict <approve or changes> --iteration <n> --gate-green <yes if the gate below, else no>` (see [adversarial-review.md](../../patterns/adversarial-review.md), bounded by
   [review-loop.md](../../patterns/review-loop.md)) — `revise` (loop back and fix worst-first),
   `escalate` (still `changes` at N = 3 → **commit nothing; mark the feature PR a draft** (the merge gate already refuses a draft); for a typed handoff **set `review_decision` to `escalate`** (not `status`, the repo's lifecycle field), surface the unresolved claims and stop; don't ship), or
   `proceed` (**commit this phase's artifact and push — opening or updating the feature PR per [doc-delivery](../../patterns/doc-delivery.md)**; `approve` **and** the gate → the deliverable is done). **The gate depends on what this
   sub-area produced:** for a typed handoff (`market-brief` / `marketing-strategy`) it is step 3's
   read-back; for the untyped deliverables (offer doc, content files, audit report)
   there is no schema, so it is the evidence discipline itself — every claim cited or labelled, no
   bare figure stated as fact. Don't ship a deliverable whose claims aren't sourced.

## Output

**A full marketing run produces the finished deliverable for the sub-area** — a validated
`market-brief` or `marketing-strategy` handoff (see [handoff.md](../../patterns/handoff.md)), or the
untyped offer doc / content files / audit report — with every claim cited or labelled, that survived
the bounded claims loop to `proceed`. A run whose loop `escalate`s (unsourced claims still standing
at N = 3) surfaces them and stops; it does **not** ship fluff.

## Definition of done

- The claims loop exited on `proceed` (`review-decision`): `approve` **and** the sub-area's
  gate (schema validation, or the evidence discipline for an untyped deliverable) — not `escalate`.
- The right sub-area procedure was followed; the output is the expected handoff/content.
- Every market/competitor claim is cited or labelled an assumption; nothing is fabricated;
  competitors are named specifically.
- A bounded adversarial claims pass (plus the external-reviewer lens when enabled) checked the
  evidence discipline before shipping.
- Strategy ties to the market brief and the PRD; content traces to real proof points and the brand tone.
