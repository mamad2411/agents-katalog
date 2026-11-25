---
name: feature-discovery
description: >-
  Run an exhaustive, multi-agent discovery of new value-adding features for
  your product. Fans out parallel agents to map the current product from its
  repo, research competitors, ideate across product lenses, dedup and
  shortlist, spec and adversarially validate the winners, then synthesize a
  ranked roadmap. Use this whenever the user asks what to build next, wants
  feature ideas, a product or roadmap brainstorm, a gap analysis, or a
  competitor analysis - and even when they just say "find new features", "what
  are we missing", "where can we add value", or "ideate features and spec
  them", prefer this over a single agent riffing ideas. Requires the Workflow
  tool (multi-agent orchestration); invoking this skill is the user's opt-in to
  that fan-out.
---

# Feature discovery

Turns "what should we build next?" into a grounded, ranked roadmap by fanning
out many agents instead of one agent guessing.
The whole run is bundled as a deterministic Workflow script so every invocation
follows the same pipeline rather than being re-improvised.

## When this fits

Reach for it when the user wants ideas that are researched, deduped, specced,
and pressure-tested, not a quick off-the-cuff list.
It is deliberately heavyweight (roughly 35-40 agents at full depth), so for a
casual "give me three ideas" just answer directly; use this when they want the
exhaustive version.

## How it works

Five phases (see [scripts/feature-discovery.workflow.js](scripts/feature-discovery.workflow.js)):

1. **Ground** - one agent maps the current product by reading the repo (entry
   points, routes, data models, content, services, config, docs); in parallel a
   planner proposes competitor segments, then one analyst per segment researches
   it via web search. The product is always mapped, even in `internal` scope, so
   ideation never re-proposes what exists.
2. **Ideate** - one agent per product lens (discoverability, core value, UX,
   monetization, engagement, trust, IA), each grounded in the inventory +
   competitor findings, each forbidden from proposing anything that already
   exists.
3. **Shortlist** - a single curator merges duplicates, drops the trivial and the
   already-built, ranks by value-to-effort, and picks the top 8-12.
4. **Spec & validate** - a pipeline: spec each feature, then an adversarial
   skeptic scores novelty, real value, feasibility in the current architecture,
   competitor precedent, and maintenance burden.
5. **Synthesize** - one agent writes the final Markdown report: exec summary,
   gaps (internal + vs competitors), a ranked roadmap table, full specs for the
   build/maybe features, dropped ideas with reasons, and a quick-wins-vs-bigger-
   bets split.

## Running it

Invoke the **Workflow** tool pointed at the bundled script.
Do not paste the script inline; use its path so the persisted version stays the
source of truth:

```
Workflow({
  scriptPath: ".claude/skills/feature-discovery/scripts/feature-discovery.workflow.js",
  args: { product: "one-line description of your product", scope: "mixed", depth: "exhaustive" }
})
```

The workflow runs in the background and returns `{ report, meta, counts }` on
completion, where `report` is the finished Markdown.

### Parameters (`args`)

| key       | values                                | default         | effect |
|-----------|---------------------------------------|-----------------|--------|
| `product` | free text                             | (mapped from repo) | A one-line description of the product. If omitted, the mapper infers it from the code, README, and docs. |
| `scope`   | `mixed` \| `internal` \| `competitor` | `mixed`         | Where ideas come from. `internal` skips competitor research; `competitor` still maps the product but tells ideators to hunt for capabilities rivals have that it lacks. |
| `depth`   | `exhaustive` \| `quick`               | `exhaustive`    | `exhaustive` = 4 competitor tracks, 7 lenses, top 8-12. `quick` = 2 tracks, 4 lenses, top 5-6, for a faster first pass. |

If the user does not specify, ask for product, scope, and depth (or default to a
mapped product + `mixed` + `exhaustive`, the intended full run) before
launching.

## Presenting the result

- Lead with the executive summary and the ranked roadmap table in chat, then
  offer to render the full report as an Artifact for readability.
- Report the run `counts` (raw ideas / shortlisted / specced) so the user can
  see the funnel.
- Treat the report as a working artifact, not a committed file, unless the user
  asks to save it.
- If `error` is returned (`product-mapping-failed` or `empty-shortlist`), say so
  plainly and offer to rerun rather than presenting a half-report.

## Extending

The lens list (`ALL_LENSES`) lives at the top of the script; add or reword
entries to change ideation coverage.
Competitor segments are planned dynamically from the product, so no market list
is hardcoded.
The phase wiring and schemas do not need to change.
