---
name: short-form-research
description: "Discovers what's working right now on short-form video platforms (TikTok, Instagram Reels, YouTube Shorts; X video and LinkedIn video by opt-in) for a given topic and market. Produces a per-platform best-practice catalog at .agents/skill-artifacts/research/short-form-research/[slug].md that short-form-brief consumes. Not for long-form video (parked) or static visual (use design-brief). For audience research, see icp-research; for campaign planning, see campaign-plan."
argument-hint: "[topic or angle]"
allowed-tools: Read Grep Glob Bash WebSearch WebFetch Write
license: MIT
metadata:
  author: hungv47
  version: "1.0.0"
  budget: deep
  estimated-cost: "$3-6 (default 3 platforms) / $5-10 (--all)"
promptSignals:
  phrases:
    - "what's working on tiktok"
    - "short-form trends"
    - "reels research"
    - "shorts research"
    - "tiktok patterns"
    - "viral hook research"
  allOf:
    - [short-form, research]
    - [tiktok, hook]
    - [reels, pattern]
  anyOf:
    - "trending sound"
    - "hook archetype"
    - "platform research"
    - "what's hitting"
  noneOf:
    - "long-form"
    - "youtube long"
    - "podcast"
    - "blog post"
  minScore: 6
routing:
  intent-tags:
    - short-form-research
    - platform-pattern-mining
    - hook-research
    - content-research
  position: pipeline
  lifecycle: pipeline
  produces:
    - .agents/skill-artifacts/research/short-form-research/[slug].md
  consumes:
    - product-context.md
    - icp-research.md
  requires: []
  defers-to:
    - skill: icp-research
      when: "no audience context exists yet — research without ICP underperforms"
    - skill: market-research
      when: "user wants competitive landscape, not platform pattern mining"
  parallel-with:
    - market-research
  interactive: false
  estimated-complexity: heavy
---

# Short-Form Research — Orchestrator

*Pipeline skill — produces the per-platform best-practice catalog that `short-form-brief` consumes per asset.*

**Core Question:** "What's working right now on short-form for our topic and market — and which patterns should the next 30 days of briefs bet on?"

---

## Critical Gates — Read First

Non-negotiable constraints before dispatching any agent:

1. **No fabricated data.** Every claim, number, and pattern must trace to a source URL, video ID, or cited platform doc. Orphan claims fail critic rubric #1.
2. **Single market per artifact.** Multi-market campaigns re-run research per market — never mix VN and US findings in one artifact. Cultural patterns are not averageable.
3. **Hard cap on platforms.** Default 3 (TikTok + Reels + Shorts). X video and LinkedIn video are explicit opt-in via `--all` or `--platforms`. Maximum ever is 5. Cost discipline.
4. **Sample-size honesty.** Every per-platform section declares OK (n≥8), LOW_SAMPLE (n=3-7), or INSUFFICIENT_DATA (n<3). LOW_SAMPLE flags carry through to brief skill warnings. INSUFFICIENT_DATA means no pattern claims at all — only observed examples.
5. **Two freshness windows.** Trend signals refresh every 14d, warn at 30d. Platform mechanics refresh every 90d, warn at 180d. Frontmatter records `mechanics_sources_verified[]` — the actual doc URLs and their last-updated dates, not just the run timestamp.

---

## Philosophy

Research yields a **catalog of bets**, not a survey. The brief skill consumes specific recommendations ("TikTok hook should be credential-flash archetype in 0–1.5s — 8/12 in this sample") not generic advice ("strong hooks matter"). Specificity is the contract.

Trend signals decay fast — 14-day windows are deliberate. Platform mechanics change quarterly — 90-day windows match algorithm-update cadence. The two-window split prevents the "fresh date, stale truth" failure mode where one timestamp masks the other.

## Inputs / Output

**Inputs:** Topic (required); target platforms (default 3); market (single per artifact); audience hint or `research/icp-research.md` (warm-start); optional competitor handles to seed scout.

**Output:** `.agents/skill-artifacts/research/short-form-research/[slug].md` — single artifact, single market.

## Quality Gate

Critic agent verifies before delivery (all five PASS required, max 2 rewrite cycles):

- [ ] Every numerical claim and named pattern has a source URL or video ID
- [ ] Every per-platform section declares OK / LOW_SAMPLE / INSUFFICIENT_DATA per the N≥8 / 3-7 / <3 rule
- [ ] Every recommendation is platform-specific (could not be moved to another platform's section unchanged)
- [ ] Every cited mechanic links to a source doc with a verified `last_updated` date inside the 180d warn window
- [ ] Audience Fit section either references ICP or explicitly declares "no ICP — using cold-start hint" with the hint text included

## Chain Position

Previous: `icp-research` (recommended, soft-required) | Next: `short-form-brief` (marketing-skills) — consumes this artifact per-asset.

**Re-run triggers:**
- Trend signals >30d old (warn — refresh recommended; brief skill soft-blocks downstream)
- Platform mechanics >180d old (warn — refresh recommended)
- Topic pivot, market change, or audience pivot

### Skill Deference
- No audience context yet → `icp-research` first (soft — runs without it but flags `NEEDS_CONTEXT` in Audience Fit)
- Competitive landscape (not platform patterns) → `market-research`
- Per-asset brief (not catalog) → `short-form-brief`

---

## Agent Manifest

| Agent | Layer | File | Focus |
|-------|-------|------|-------|
| Platform Scout | 1 (parallel — N×) | `agents/platform-scout-agent.md` | Per-platform: pulls top performers via WebSearch + WebFetch, captures URLs + observable metrics + opening 1-3s + audio + caption + CTA placement |
| Audience Fit Agent | 1 (parallel) | `agents/audience-fit-agent.md` | Reads ICP / product-context / cold-start hint, derives audience register, language polish routing, sensitivity flags |
| Pattern Extractor | 2 (sequential) | `agents/pattern-extractor-agent.md` | Combines scout outputs, identifies recurring hook archetypes per platform, applies sample-size flags |
| Audio Trend Agent | 2 (sequential, conditional) | `agents/audio-trend-agent.md` | Runs only if TikTok or Reels in scope; surfaces trending sounds with usage counts and decay risk |
| Synthesis Agent | 2 (sequential) | `agents/synthesis-agent.md` | Writes the artifact: TL;DR, per-platform sections, cross-platform diff, brief-handoff recommendations, risks |
| Critic Agent | 2 (final) | `agents/critic-agent.md` | Five-rubric quality gate; routes rewrites; max 2 cycles |

---

## Routing Logic

Single route. The skill always runs the full Layer 1 + Layer 2 sequence — there's no "Quick" route because per-platform analysis is the entire value proposition.

```
1. Pre-dispatch (warm-start scan + cold-start if needed)
2. LAYER 1 IN PARALLEL: platform-scout × N (one per requested platform), audience-fit-agent
3. LAYER 2 SEQUENTIAL:
   - pattern-extractor-agent (consumes all Layer 1 outputs)
   - audio-trend-agent (conditional on TikTok/Reels presence)
   - synthesis-agent (writes artifact)
   - critic-agent (5-rubric gate; FAIL → re-dispatch named agent with feedback)
4. Critic FAIL → re-dispatch named agent(s) (max 2 cycles); after cycle 2, ship done_with_concerns
5. Deliver artifact
```

---

## Pre-Dispatch

Run the canonical Pre-Dispatch protocol (`references/_shared/pre-dispatch-protocol.md`).

**Needed dimensions:** topic, market, target platforms, audience hint or ICP availability, optional competitor seeds.

**Read order:**
1. `.agents/skill-artifacts/research/short-form-research/[slug].md` if exists — check (topic, market) match and freshness windows.
2. `.agents/experience/content.md` — most recent entries for market, audience register, topics already researched.
3. `.agents/experience/audience.md` — primary persona, language, habitats.
4. `research/icp-research.md`, `research/product-context.md` — full context if present.
5. `brand/BRAND.md` — voice and archetype hints.

**Warm Start** (existing artifact for same topic+market):

```
Found existing short-form-research for "[topic]" / "[market]":
- platform_mechanics_date: [date] — [fresh / warn / stale]
- trend_signals_date: [date] — [fresh / warn / stale]
- platforms analyzed: [list]
- sample sizes: TikTok n=12 OK, Reels n=5 LOW_SAMPLE, Shorts n=9 OK

Refresh modes:
(a) Use existing (fresh enough)
(b) Refresh trends only (mechanics still fresh)
(c) Full re-run (both windows)

Which one?
```

**Cold Start** (no existing artifact, no usable experience):

```
Short-form research starts with five quick decisions (one round-trip).

1. Topic / angle to research:
   [free text — what should the catalog focus on?]

2. Target market:
   (a) Vietnam   (b) US/global English   (c) SEA   (d) Other: ___

3. Platforms to scan (default trio is plenty for most topics):
   (a) Default: TikTok + Reels + Shorts (recommended)
   (b) +X video (founder-mode + thought-leadership topics)
   (c) +LinkedIn video (B2B + professional audiences)
   (d) All 5 (research-heavy, ~$5-10 cost)

4. Audience hint (skip if you've run icp-research):
   [free text — 1-2 sentences. Who is this content for?]

5. Competitor handles to seed scout (optional, recommend 2-5):
   [free text — @handles or URLs we should analyze first]

Answer 1-5 in one response. I'll confirm what I heard, then dispatch.
```

**Write-back to `.agents/experience/content.md`:**

| Q | Key |
|---|---|
| 2. Market | `Content — primary market` |
| 3. Platforms | `Content — short-form platforms in scope` |
| 4. Audience hint | `Content — short-form audience hint` (only if no ICP) |

---

## Dispatch Protocol

### How to spawn a sub-agent

For each agent dispatched, use the **Agent tool** with a prompt built as follows:

1. **Read** the agent instruction file — include FULL content in the Agent prompt
2. **Append** brief, context, and Layer 1 outputs (for Layer 2 agents)
3. **Resolve paths to absolute**: replace relative reference paths with absolute paths rooted at this skill's directory
4. **Pass research artifact context by excerpt**: orchestrator reads `research/icp-research.md` once, includes relevant excerpts in audience-fit-agent's context — sub-agents do not re-read
5. If **feedback** exists (critic FAIL cycle), append at end with header "## Critic Feedback — Address Every Point"

### Single-agent fallback

If multi-agent dispatch unavailable, execute each agent's instructions sequentially in-context. Output quality is equivalent — multi-agent pattern optimizes parallelism, not capability.

---

## Layer 1: Parallel Scout + Audience Fit

Spawn **IN PARALLEL** (multiple Agent tool calls in one message).

| Agent | Instruction File | Pass These Inputs | Reference Files to Resolve |
|-------|-----------------|-------------------|---------------------------|
| Platform Scout × N | `agents/platform-scout-agent.md` | `{ platform, topic, market, competitor_seeds }` | `references/platforms/[platform].md`, `references/scout-protocol.md` |
| Audience Fit Agent | `agents/audience-fit-agent.md` | `{ audience_hint, icp_excerpt, product_context_excerpt, market }` | — |

**Number of platform-scout instances** = count of requested platforms (1–5, hard cap 5).

---

## Layer 2: Sequential Analysis + Synthesis

Run sequentially. Each agent receives all upstream outputs.

| Agent | Instruction File | Inputs | Reference Files |
|-------|-----------------|--------|-----------------|
| Pattern Extractor | `agents/pattern-extractor-agent.md` | All scout outputs + audience-fit | `references/scoring-rubrics.md` |
| Audio Trend Agent | `agents/audio-trend-agent.md` | Scout outputs for TikTok and Reels (only) | — |
| Synthesis Agent | `agents/synthesis-agent.md` | All Layer 1 + Layer 2 upstream | `references/platforms/_comparison.md` |
| Critic Agent | `agents/critic-agent.md` | Synthesis output | `references/scoring-rubrics.md` |

**Conditional dispatch:** `audio-trend-agent` runs only if `tiktok` or `reels` is in `platforms`. Otherwise skipped — synthesis agent omits the Trending Audio section.

---

## Critic Routing

Critic returns one of:

- **PASS** → deliver artifact as `done`
- **FAIL with named sections** → re-dispatch the source agent(s) with feedback. Common routes:
  - Citation FAIL → back to scout (capture missing URL) or synthesis (re-cite)
  - Sample-size FAIL → synthesis (apply correct flag)
  - Specificity FAIL → pattern-extractor + synthesis (rewrite recommendations per-platform)
  - Freshness FAIL → scout (re-verify source doc dates)
  - Audience FAIL → audience-fit-agent (re-pull from ICP or declare cold-start hint)

**Loop cap:** 2 cycles. After cycle 2, ship `done_with_concerns` with failed rubrics pinned at top of artifact.

---

## Output Artifact Structure

`.agents/skill-artifacts/research/short-form-research/[slug].md` (frontmatter shown; full template in §5 of `.agents/skill-artifacts/meta/specs/short-form-research-spec.md`):

```yaml
---
type: short-form-research
status: done | done_with_concerns | blocked | needs_context
date: [YYYY-MM-DD]
topic: [free text]
market: [region or 'global']
platforms_analyzed: [list]
platform_mechanics_date: [YYYY-MM-DD]
mechanics_sources_verified:
  - source: [name]
    url: [url]
    last_updated: [YYYY-MM-DD]
trend_signals_date: [YYYY-MM-DD]
sample_size_per_platform:
  tiktok: { n: [int], flag: OK | LOW_SAMPLE | INSUFFICIENT_DATA }
  reels: { ... }
  shorts: { ... }
icp_referenced: yes | no — using cold-start audience hint
---
```

**Body sections (in order):**
1. TL;DR — top 5 platform-tagged recommendations
2. Audience Fit
3. Per-Platform Findings (TikTok → Reels → Shorts → opt-in others)
4. Cross-Platform Comparison table
5. Trending Audio (TikTok + Reels only, conditional)
6. Recommendations for short-form-brief
7. Open Risks & Caveats
8. What This Research Doesn't Cover

---

## Completion Status

Skill returns one of:

- **DONE** — all 5 critic rubrics PASS within ≤2 cycles. All requested platforms returned ≥3 entries.
- **DONE_WITH_CONCERNS** — critic loop cap reached; remaining failures are surfaceable as warnings (LOW_SAMPLE on 1+ platforms, one stale source doc beyond warn window). Concerns pinned at top of artifact.
- **BLOCKED** — WebSearch / WebFetch blocked or rate-limited; ICP read failed. Requires user action — state what's needed.
- **NEEDS_CONTEXT** — cold-start abandoned; or `audience_hint` empty AND no ICP. Defer to `icp-research`.

---

## Format Conventions

- All dates ISO 8601 (`YYYY-MM-DD`).
- All URLs preserve query parameters (don't strip `?si=` or platform tracking — they're part of the canonical URL).
- All numerical claims inline-cite source: `"70% completion threshold ([TikTok Creator Portal — Algorithm Updates, last_updated 2026-04-12](url))"`.
- Sample sizes always declared with flag: `"SAMPLE: OK (n=12)"` not just `"n=12"`.
- Per-platform sections always in the same order: TikTok, Reels, Shorts, X, LinkedIn (skip absent platforms).
