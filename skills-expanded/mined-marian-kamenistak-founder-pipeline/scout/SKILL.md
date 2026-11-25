---
name: scout
description: "Use when the user needs a market or landscape mapped: investors, partners, companies, competitors, media, or any structured market intelligence. Asks segmentation questions first, then researches systematically with sources."
user-invocable: true
allowed-tools: Read, Glob, Grep, WebFetch, WebSearch, Agent, Bash
argument-hint: "[topic, e.g. \"seed VCs investing in my home market\", \"media partners for tech events\"]"
---

# Research

Systematic market research that produces structured, actionable intelligence. Not a brain dump — a focused scan of a well-defined segment.

## Core principle: SEGMENT BEFORE SEARCHING

Never start researching immediately. A broad question produces broad, useless results. A narrow question produces a hitlist.

## Phase 1: Define the segment (mandatory)

Ask ONE question at a time. Wait for the answer. Max 5 questions, stop when the segment is sharp enough.

**Question flow:**

1. **What are you looking for?**
   - Type of entity: VCs, companies, partners, sponsors, media, people, tools?
   - "VCs" is too broad. "Seed-stage VCs with a mandate for my region and fresh capital" is a segment.

2. **What geography?**
   - Headquartered where vs. investing/operating where?
   - "Active in [region]" vs. "headquartered in [region]" — big difference.
   - Default to the two markets the stream declared: the home market and the primary export market.

3. **What stage/size/profile?**
   - For VCs: fund size, stage (pre-seed/seed/A/B/growth), sector focus
   - For companies: revenue, headcount, industry, maturity
   - For partners: type of partnership (sponsorship, co-marketing, distribution)

4. **What's the use case?**
   - Outreach for partnership? Competitive analysis? Target list for sales?
   - This determines what data fields to collect.

5. **What do you already have?**
   - Existing lists, databases, trackers — so we don't duplicate.
   - "Check vc-landscape.md first" vs. starting from scratch.

**Stop asking when you can fill this template:**

```
Segment: [entity type] + [geography] + [profile filter]
Use case: [what the owner will do with the results]
Exclude: [existing data to skip]
Output: [where results should go]
```

Worked example (a VC-mapping run — substitute your own entity type and region):
```
Segment: VCs with an explicit mandate for the home market, fund size >{currency}20M, raised a new fund in the last 24 months
Use case: partnership outreach for the stream — add to outreach.yaml
Exclude: All VCs already in vc-landscape.md and outreach.yaml
Output: Append to vc-landscape.md Part 2/3 + add to outreach.yaml
```

## Phase 2: Research systematically

### Search strategy

Don't do one search and call it done. Use multiple angles:

1. **Direct search** — `"[segment] [current year]"`, `"[segment] fund raise"`, `"[region] [entity type] report"`
2. **Aggregator sites** — the directories, databases and trade-press lists that cover your region and entity type (Dealroom, Crunchbase and the regional startup-media lists are the usual starting points)
3. **Inverse search** — find companies in the region that recently did the thing you care about → trace back to whoever backed, supplied or sponsored them
4. **Report search** — `"[region] [entity type] landscape report [year]"`, `"state of [sector] [year]"`
5. **Conference/event lists** — sponsors and speakers at regional events in the sector often reveal who is active

**Record every query you run, verbatim.** The query log is evidence, not housekeeping — a later step may
need to show that a claim was actually checked and not just asserted.

### For each entity found, collect:

| Field | Required | Notes |
|-------|----------|-------|
| Name | Yes | Exact legal/brand name |
| HQ | Yes | City + country |
| Website | Yes | Verified, working URL |
| Fund size | If available | Latest fund, in the stream's declared currency |
| Stage focus | Yes | Pre-seed / Seed / A / B / Growth |
| Sector focus | Yes | Fintech, deeptech, SaaS, etc. |
| Region signal | Yes | What connects them to the target region — investments, mandate, team |
| Key contact | If findable | Name + role (partner-level for VCs) |
| Why relevant | Yes | 1 sentence: why this matters for the owner's use case |
| Source URL | Yes | Where the claim was read, plus the date it was accessed |

### Cross-reference against existing data

Before adding any entity to results:
1. Check if it's already in the exclude list
2. Check if it's already tracked in any existing file (grep the name)
3. If found, skip it — don't waste the owner's time with duplicates

## Phase 3: Structure the output

### Tier the results

Don't dump a flat list. Rank by relevance:

- **Tier 1** — High priority. Strong region signal, right profile, actionable now.
- **Tier 2** — Medium priority. Relevant but needs more research or has weaker signal.
- **Tier 3** — Watch list. Interesting but not actionable yet.

### Format

Output as a markdown table per tier:

```markdown
## Tier 1 — [description]

| # | Name | HQ | Fund Size | Stage | Region Signal | Key Contact | Why Relevant | Source |
|---|------|-----|-----------|-------|---------------|-------------|--------------|--------|
| 1 | ... | ... | ... | ... | ... | ... | ... | ... |
```

### Save to file

Ask the owner where to save:
- Append to an existing file? (e.g., `vc-landscape.md`)
- Create a new file? (e.g., `research/[topic]-[date].md`)
- Add to a tracker? (e.g., `outreach.yaml`)

## Anti-claim mode (verifying a uniqueness claim)

A second, narrower job: proving that **nobody else in the territory already claims the sentence you
are about to claim**. This is what the offer step calls scout for, and the output is evidence, not a
list.

The deliverable is three things, and it fails without any one of them:

1. **The queries run** — verbatim, every one, including the ones that returned nothing. Vary the
   phrasing deliberately: the claim as written, its obvious synonyms, the claim in the languages of
   both declared markets, and the claim as a buyer would type it rather than as you would write it.
2. **The 3 closest competing claims found** — each with the **URL** it was read on and the date it
   was accessed, quoting the competitor's own sentence rather than paraphrasing it.
3. **Why each one does not match** — one line per claim, naming the specific dimension that differs
   (audience, scope, delivery model, proof, price band). "It's different" is not an answer.

If the closest claim is *not* clearly distinguishable, say so plainly. A scout run that reports
"someone already says this" has done its job; a scout run that quietly returns nothing found because
it ran two lazy queries has not.

## Phase 4: Summarize

After research is complete, give the owner:

1. **Count** — "Found X new [entities] not on your existing list"
2. **Top 3-5 picks** — the ones worth acting on first, with 1-line reasoning
3. **Key trend** — one insight from the research (e.g., "defence-tech investors are flooding the region")
4. **Next step** — offer the obvious follow-on: enrich the top picks into full profiles (pull each
   one's own site and public profiles, and record who the buyer is, the warm path, recent signals and
   a personalization hook, each with a source URL), or add them to the outreach tracker.

## Rules

- Never start searching before the segment is defined
- Always cross-reference against existing data
- Tier results by relevance — don't dump everything flat
- Log every query verbatim and attach a source URL + access date to every finding — a claim without
  a source is an assumption and must be labelled as one
- Ask where to save before writing files
- If the segment is still too broad after 5 questions, say so and suggest how to narrow it
