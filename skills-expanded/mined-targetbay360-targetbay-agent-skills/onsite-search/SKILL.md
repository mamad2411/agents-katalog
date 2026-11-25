---
name: onsite-search
description: Use when search on the store's site is underperforming — searches coming back with no results, high-volume queries that do not convert, synonyms and redirects that need setting, or search results that do not reflect what the store actually wants to sell. Answers "our searches return no results" and "why does site search find nothing?". Also use to mine search queries for catalogue and merchandising gaps. Use personalization-audit when search is only one suspect among several and nobody has named the problem.
license: MIT
metadata:
  targetbay.display_name: Onsite Search
  targetbay.version: "2.0.0"
  targetbay.category: discovery
  targetbay.requires: onboarding.store_context, onboarding.onsite_search, onboarding.product_intelligence, onboarding.experience_analytics, onboarding.visitor_intelligence
  targetbay.composes: surface-inventory
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Onsite Search

## Purpose

Turn what visitors type into decisions about synonyms, ranking, redirects, catalogue and merchandising.

Search is the highest-intent surface a store has and usually the least examined. A visitor who types a
query has stated exactly what they want, and the queries that fail are the clearest signal available about
what the catalogue or its vocabulary is missing
([../../knowledge/personalization-principles.md](../../knowledge/personalization-principles.md)).

## When to Use

- Queries are returning no results
- High-volume queries convert poorly
- Setting synonyms, redirects or ranking rules
- Mining queries for catalogue gaps
- Search converts worse than navigation and nobody knows why
- Deciding whether a query deserves a curated landing rather than a result set

## When Not to Use

- The question is what to recommend alongside results. Use
  [recommendation-strategy](../recommendation-strategy/SKILL.md).
- The question is an offer on the search page. Use
  [offer-targeting](../offer-targeting/SKILL.md).
- The inventory of onsite elements is unknown. Use
  [surface-inventory](../surface-inventory/SKILL.md) — this skill composes it.
- A ranking change needs proving rather than deciding. Use
  [experience-experimentation](../experience-experimentation/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Query log with volume and result counts | The finding itself | Blocked |
| Per-query click-through and conversion | Separates "no results" from "wrong results" | Blocked |
| Current synonym, redirect and ranking configuration | What already runs | Blocked |
| Catalogue attributes and vocabulary | Whether a failing query is a gap or a mismatch | Blocked |
| Stock and margin posture | Whether ranking should favour anything | Partial |
| Search-to-purchase funnel | Where the drop actually happens | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `onboarding.store_context` | Catalogue size, vertical, traffic volume |
| `onboarding.onsite_search` | Query log, result counts, conversion; synonym, redirect and ranking configuration |
| `onboarding.product_intelligence` | Catalogue vocabulary, attributes, stock, margin |
| `onboarding.experience_analytics` | Search-to-purchase funnel against navigation |
| `onboarding.visitor_intelligence` | Session context around the query |

## Decision Process

```
1. Rank queries by volume × failure            ← a rare failing query costs nothing
2. Classify each failure                       ← catalogue gap / vocabulary mismatch / ranking / presentation
3. Route catalogue gaps out of search entirely
4. Fix vocabulary with synonyms, not with redirects
5. Decide which queries deserve a curated landing
6. Decide ranking adjustments, and what they cost
7. Compare search conversion against navigation
8. Define the measurement before changing anything
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/measurement-rules.md](../../rules/measurement-rules.md),
[../../rules/surface-rules.md](../../rules/surface-rules.md).

- Rank by volume times failure, not by failure alone. A query nobody types is not a problem (G17).
- Classify before fixing. A zero-result query caused by a catalogue gap is a merchandising finding and is
  routed out of search; fixing it with a synonym points visitors at something that is not there.
- Prefer synonyms over redirects for vocabulary mismatches. A redirect hides the mismatch and breaks when
  the catalogue changes; a synonym fixes the vocabulary.
- Reserve curated landings for queries whose volume justifies the maintenance. Each one is a page somebody
  has to keep current (G22).
- State what a ranking change costs as well as what it gains (M7). Promoting margin or stock demotes
  relevance, and that trade is stated rather than assumed.
- Never rank on a signal the visitor would find surprising if explained. Search results that favour the
  store over the query are a short-term trade against the surface's credibility.
- Compare search conversion against navigation conversion before concluding search is broken — a gap in
  either direction is informative.
- Define the metric, comparison and horizon before any change (M1, G24).
- Where traffic supports it, prove a ranking change rather than asserting it (M5), handing off to
  [experience-experimentation](../experience-experimentation/SKILL.md).
- Publishing a search configuration change is `high_impact` — it changes what every searching visitor sees
  ([#S5](../../rules/safety-rules.md)).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read query log, configuration, catalogue, funnel | `read_only` |
| ANALYZE | Rank by volume × failure; classify each failure | `analysis` |
| PLAN | Synonyms, redirects, landings, ranking; route catalogue gaps out | `recommendation` |
| PREVIEW | State each change, the query volume it affects, and its trade-offs | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves; ranking changes approved separately from vocabulary | — |
| EXECUTE | Stage configuration | `mutation` |
| EXECUTE | Publish to live search | `high_impact` |
| VERIFY | Confirm live configuration matches what was approved | `read_only` |
| MEASURE | Zero-result share and search conversion over the declared horizon | `read_only` |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: queries ranked by volume times
failure, each classified, with the fix and its owner — synonym, redirect, curated landing, ranking rule, or
routed out as a catalogue or merchandising finding.

Ranking changes state what they demote as well as what they promote. Recommendations conform to
[../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json).

Plus: search conversion against navigation conversion, current configuration as read, and what was
deliberately left alone.

## Validation

- [ ] Queries ranked by volume times failure, not by failure count (G17)
- [ ] Every failing query classified before a fix is proposed
- [ ] Catalogue gaps routed out of search rather than papered over
- [ ] Synonyms preferred over redirects for vocabulary mismatches
- [ ] Curated landings justified by volume against maintenance cost (G22)
- [ ] Ranking changes state what they demote (M7)
- [ ] Search conversion compared against navigation
- [ ] Measurement defined before the change, with metric, comparison and horizon (M1, G24)
- [ ] Ranking changes tested where traffic supports it, or the decision stated as reasoning-based (M5)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Recommend | `recommendation` | None |
| Stage configuration | `mutation` | Preview, then confirm |
| Publish to live search | `high_impact` | Explicit, with affected query volume shown |
| Remove an existing rule or redirect | `destructive` | Explicit, after reporting what it currently does (S19) |

## Examples

**"Our search returns nothing for loads of queries."**
Ranks zero-result queries by volume and finds two thirds of the volume sits in a handful of terms. Of
those, most are vocabulary — the store's catalogue says one word and customers type another — fixed with
synonyms. The remainder are genuine catalogue gaps: products visitors expect the store to carry and it
does not. Routes those out as a merchandising finding rather than hiding them behind a redirect to
something unrelated.

**"Can we push our own-brand products up the search results?"**
States the trade explicitly: what own-brand promotion gains in margin and what it demotes in relevance for
the queries affected, with the query volume attached. Recommends limiting the adjustment to queries where
own-brand products are genuinely relevant results rather than applying it globally, and — since traffic
supports it — handing the change to
[experience-experimentation](../experience-experimentation/SKILL.md) rather than shipping it on the
assumption it helps.

## Failure Handling

| Situation | Response |
|---|---|
| `onboarding.onsite_search` unavailable | **Blocked.** There is no analysis without the query log |
| Per-query conversion unavailable | **Partial.** Zero-result queries can still be ranked; "wrong results" queries cannot be separated from good ones |
| Catalogue vocabulary unavailable | **Blocked.** Gap and mismatch cannot be distinguished, and the fixes are opposite |
| Funnel data unavailable | **Partial.** Report query-level findings; state that search-versus-navigation comparison was not possible |
| Query volume too low to rank | Report it; the finding is that search is not a significant surface here |
| Margin or stock unavailable | **Partial.** Withhold ranking recommendations that trade relevance for commercial outcome |
| Asked to rank on a signal visitors would find surprising | State the credibility cost explicitly and require it as its own decision |

Degraded outcomes set `status` and populate `unmet_requirements`.
