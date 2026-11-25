---
name: short-form-brief
description: "Produces production-ready briefs for short-form video — hook, shot list, on-screen text, audio plan, caption, CTA, aspect, length — covering live-action and motion-graphic production modes. Native cross-platform tailoring (1 hero + max 2 variants per invocation). Reads short-form-research.md catalog. Not for static visual (use design-brief), long-form video (parked), or paid ad creative (parked). For brand voice, see brand-system; for audience, see icp-research."
argument-hint: "[angle or topic] [--platforms tiktok,reels,...] [--brand-mode founder|company]"
allowed-tools: Read Edit Write Grep Glob Bash WebSearch WebFetch
license: MIT
metadata:
  author: hungv47
  version: "1.0.0"
  budget: deep
  estimated-cost: "$2-4 (single platform) / $4-8 (1 hero + 2 variants)"
promptSignals:
  phrases:
    - "short-form brief"
    - "tiktok brief"
    - "reels brief"
    - "shorts brief"
    - "video brief"
    - "shoot brief"
    - "storyboard"
  allOf:
    - [short-form, brief]
    - [tiktok, plan]
    - [reels, brief]
  anyOf:
    - "shot list"
    - "hook variations"
    - "video script"
    - "production brief"
  noneOf:
    - "blog post"
    - "newsletter"
    - "long-form"
    - "podcast"
  minScore: 6
routing:
  intent-tags:
    - short-form-brief
    - video-brief
    - production-brief
  position: pipeline
  produces:
    - mkt/short-form-brief/[slug]/brief.md
    - mkt/short-form-brief/[slug]/variants/[platform].md
  consumes:
    - mkt/short-form-research.md
    - research/icp-research.md
    - research/product-context.md
    - brand/BRAND.md
    - mkt/campaign-plan.md
  requires: []
  defers-to:
    - skill: short-form-research
      when: "no research artifact OR trend signals >30d stale OR mechanics >180d stale"
    - skill: brand-system
      when: "no BRAND.md and brand_mode cannot be inferred"
    - skill: icp-research
      when: "no audience context and no audience hint provided"
  parallel-with: []
  interactive: false
  estimated-complexity: heavy
---

# Short-Form Brief — Orchestrator

*Production-grade brief for one short-form asset. Reads the per-platform research catalog and turns an angle into a hero brief plus optional per-platform variants — each producible without follow-up questions.*

**Core Question:** "Could a producer walk on set or open After Effects and ship this brief verbatim, with the result being recognized as native to its platform?"

---

## Critical Gates — Read First

Non-negotiable constraints before dispatching any agent:

1. **Soft-required: `short-form-research` artifact.** Missing → warn but proceed (briefs lack current trend signals; flag in artifact frontmatter). Stale beyond 30d trends or 180d mechanics → recommend re-run; user can override.
2. **Hard cap: 1 hero + max 2 variants per invocation.** More platforms → re-invoke. Cost discipline.
3. **Hard cap: brand_mode is `founder` OR `company` — no `hybrid`.** User picks per-brief.
4. **No fabricated VoC.** Every quote in the brief traces to `research/icp-research.md`. Cold-start audience hint accepted but flagged in artifact.
5. **Generic content fails.** Critic gate enforces specificity at four axes (hook, production, algorithm-fit, brand-fit). Two cycles max, then ship `done_with_concerns` with concerns pinned.
6. **Variants are TRUE RECUTS, not caption-resizes.** `platform-tailor-agent` rebuilds hook + audio + caption + CTA per platform; orchestrator rejects caption-only resizing.

---

## Philosophy

The brief is the contract between research and production. Specificity is the unit of value: "hand pulls latch on case, latch click audible at 0:03–0:05" beats "show product." A producer should never need to ask follow-up questions to execute.

Per-platform variants are craft, not parameter-tweaking. A LinkedIn cut isn't a TikTok with longer captions — it's a re-thought hook archetype, audio rule, caption norm, and CTA placement, all from the research catalog.

Brand mode and market drive the voice and polish chain; they're not cosmetic. Founder content sounds nothing like company content; making one prompt handle both produces blandness.

## Inputs / Output

**Inputs:** Angle (required); target platforms (1-3, hard cap 1+2); brand mode (founder | company, auto-detect or ask); production mode (live-action | motion-graphic | mixed, default per brand mode); market (inherited from research); optional campaign tie-in.

**Output:** `.agents/mkt/short-form-brief/[slug]/brief.md` (hero) + `[slug]/variants/[platform].md` per variant.

## Quality Gate

Critic agent verifies before delivery (all four PASS required, max 2 rewrite cycles):

- [ ] Hook clears platform's hook window from research; visual + verbal + text triad simultaneous; 3Q test passes; archetype tagged
- [ ] Every shot/scene has timing (seconds), framing, action, on-screen text, audio sync; audio names a track or VO direction; production notes filled
- [ ] Brief aligns with target platform's algorithmic preferences from research catalog (completion thresholds, hold rates, audio rules, captions, watermarks)
- [ ] Caption + verbal lines use VoC phrases from ICP; voice matches BRAND.md archetype; no generic founder/company tropes

## Chain Position

Previous: `short-form-research` (warm-start, soft-required) | Next: human producer / video editor / motion designer (no further skill chain).

**Re-run triggers:** angle change, platform mix change, market pivot, campaign re-positioning.

### Skill Deference
- No research artifact → `short-form-research` first (soft — proceeds without it but flags `trend_signals_stale`)
- No BRAND.md + brand_mode unresolvable → `brand-system` first
- No ICP + no audience hint → `icp-research` first
- Static visual brief (carousel, infographic) → `design-brief`

---

## Agent Manifest

| Agent | Layer | File | Focus |
|-------|-------|------|-------|
| Format Agent | 1 (parallel) | `agents/format-agent.md` | Locks aspect / length / safe zones / file specs per platform from research catalog |
| VoC Extraction Agent | 1 (parallel) | `agents/voc-extraction-agent.md` | Pulls 3-5 buyer phrases + register + sensitivity flags from ICP |
| Production Mode Agent | 1 (parallel) | `agents/production-mode-agent.md` | Resolves live-action vs. motion-graphic; outputs production-notes template |
| Hook Agent | 1.5 (parallel) | `agents/hook-agent.md` | Visual + verbal + text triad in 0–3s; 3 variations; 3Q test; archetype menu from research catalog |
| Storyboard Agent | 1.5 (parallel) | `agents/storyboard-agent.md` | Shot list (live-action) or scene list (motion-graphic) with timing, framing, action — includes on-screen text choreography |
| Audio Agent | 1.5 (parallel) | `agents/audio-agent.md` | Track choice (named, from research's audio-trend) OR VO direction with sync points |
| Copy Pack Agent | 1.5 (parallel) | `agents/copy-pack-agent.md` | Caption + hashtags + CTA per platform native conventions |
| Platform Tailor Agent | 2 (sequential, conditional) | `agents/platform-tailor-agent.md` | TRUE RECUT for variants — rebuilds hook + audio + caption + CTA per platform |
| Critic Agent | 2 (final) | `agents/critic-agent.md` | Four sub-critics (hook / production / algorithm-fit / brand-fit); routes failures back; max 2 cycles |

---

## Routing Logic

Single route — the skill always runs Layer 1 + Layer 1.5 + Layer 2. Multi-platform invocations add `platform-tailor-agent` in Layer 2.

```
1. Pre-dispatch (warm-start scan + cold-start if needed)
2. LAYER 1 IN PARALLEL: format-agent, voc-extraction-agent, production-mode-agent
3. LAYER 1.5 IN PARALLEL (after Layer 1): hook-agent, storyboard-agent, audio-agent, copy-pack-agent
4. LAYER 2 SEQUENTIAL:
   - platform-tailor-agent (only if multi-platform — produces variants)
   - critic-agent (4-sub-critic gate; FAIL → re-dispatch named source agent)
5. Critic FAIL → re-dispatch (max 2 cycles); after cycle 2, ship done_with_concerns
6. Apply polish chain (vn-tone | humanize | none) per market + brand_mode on spoken-line section
7. Deliver hero + variants
```

---

## Pre-Dispatch

Run the canonical Pre-Dispatch protocol (`meta-skills/references/pre-dispatch-protocol.md`).

**Needed dimensions:** angle, platforms (1-3), brand_mode (founder | company), production_mode (auto | live-action | motion-graphic | mixed), market, optional campaign tie-in.

**Read order:**
1. `.agents/mkt/short-form-research.md` — **primary dependency.**
   - Missing → "No short-form-research artifact for this market. Run `short-form-research` first, or proceed with platform references only (briefs will lack current trend signals). [Run upstream / Proceed without]"
   - Trend signals stale (>30d) → "Trend signals are X days old. Re-run research, or proceed with stale trends? Briefs may bet on decayed patterns."
   - Mechanics stale (>180d) → strongly recommend re-run; user can override with concerns flag.
2. `brand/BRAND.md` + `.agents/experience/business.md` → infer `brand_mode`. Solo founder / personal brand → `founder`. Faceless product / company → `company`. Ambiguous → ask.
3. `research/icp-research.md` + `.agents/experience/audience.md` → audience VoC, register, market.
4. `.agents/experience/content.md` → recent content decisions, market lock-in.
5. `.agents/mkt/campaign-plan.md` → if `[slug]` matches a campaign asset, inherit theme/dates/CTAs.

**Warm Start** (research artifact found, brand_mode inferred):

```
Found context for short-form-brief:
- research artifact: .agents/mkt/short-form-research.md (trends 8d ago, mechanics 22d ago — fresh)
- brand_mode: founder (from BRAND.md archetype)
- market: VN (from research artifact)
- production_mode default: live-action (founder)
- platforms in research: TikTok, Reels, Shorts

Missing: angle, target platforms for this brief. What's the angle?
```

**Cold Start** (multi-question bundle):

```
Short-form brief — quick decisions (one round-trip).

1. Angle / topic for this piece:
   [free text]

2. Target platform(s) (1-3 max — hard cap 1 hero + 2 variants):
   (a) TikTok only
   (b) Reels only
   (c) Shorts only
   (d) TikTok + Reels (default for founder content)
   (e) Reels + Shorts (default for company content)
   (f) All three (highest cost — review whether each is worth it)
   (g) Other: ___

3. Brand mode (skip if BRAND.md was found):
   (a) Founder — face-led, voice-driven, parasocial
   (b) Company — faceless, product-led, motion-graphic-friendly

4. Production mode (skip if you want default per brand mode):
   (a) Live-action (default for founder)
   (b) Motion-graphic / animated (default for company)
   (c) Mixed
   (d) Use brand-mode default — auto

5. Campaign tie-in (skip if no campaign-plan applies):
   [free text — campaign slug or theme to inherit, or 'none']

Answer 1-5 (skip resolved) in one response. I'll confirm what I heard, then dispatch.
```

**Write-back to `.agents/experience/content.md`:**

| Q | Key |
|---|---|
| 3. Brand mode | `Content — brand mode` |
| 4. Production mode | `Content — production mode default` |

---

## Dispatch Protocol

For each agent dispatched, use the **Agent tool** with a prompt built as follows:

1. **Read** the agent instruction file — include FULL content in the Agent prompt
2. **Append** brief, context, and Layer 1/1.5 outputs (for Layer 2 agents)
3. **Resolve paths to absolute** for reference files
4. **Pass research artifact context by excerpt** — orchestrator extracts the relevant per-platform section from `short-form-research.md` and passes excerpts; sub-agents do not re-read the artifact
5. If **feedback** exists (critic FAIL cycle), append at end with header "## Critic Feedback — Address Every Point"

**Single-agent fallback:** if multi-agent dispatch unavailable, execute each agent's instructions sequentially in-context. Output quality equivalent.

---

## Layer 1: Foundation (Parallel)

Spawn **IN PARALLEL** (multiple Agent tool calls in one message).

| Agent | Instruction File | Inputs | Reference Files |
|-------|-----------------|--------|-----------------|
| Format Agent | `agents/format-agent.md` | `{ platforms, research_artifact_excerpt }` | None — research artifact is the source |
| VoC Extraction Agent | `agents/voc-extraction-agent.md` | `{ icp_excerpt, product_context_excerpt, audience_hint }` | None |
| Production Mode Agent | `agents/production-mode-agent.md` | `{ brand_mode, production_mode, angle }` | `references/production-modes.md` |

---

## Layer 1.5: Craft (Parallel, after Layer 1)

Spawn **IN PARALLEL** after Layer 1 completes.

| Agent | Instruction File | Inputs | Reference Files |
|-------|-----------------|--------|-----------------|
| Hook Agent | `agents/hook-agent.md` | All Layer 1 + research's hook archetypes | `references/hook-archetypes.md`, `references/anti-patterns.md` |
| Storyboard Agent | `agents/storyboard-agent.md` | Format spec + production mode + recommended hook | `references/storyboard-grammar.md`, `references/anti-patterns.md` |
| Audio Agent | `agents/audio-agent.md` | Storyboard + research's audio-trend output if applicable | None — research artifact is the source |
| Copy Pack Agent | `agents/copy-pack-agent.md` | Format spec + VoC + research's caption/CTA findings | `references/caption-cta-rules.md` |

---

## Layer 2: Finalize (Sequential)

| Agent | Instruction File | Inputs | Reference Files |
|-------|-----------------|--------|-----------------|
| Platform Tailor Agent | `agents/platform-tailor-agent.md` | Hero brief + research catalog per variant platform | `references/hook-archetypes.md`, `references/caption-cta-rules.md` |
| Critic Agent | `agents/critic-agent.md` | Hero + variants | `references/anti-patterns.md`, `references/success-criteria-templates.md` |

**Conditional dispatch:** `platform-tailor-agent` runs only when `len(platforms) >= 2`. Otherwise Layer 2 starts at critic.

---

## Critic Routing

Critic returns one of:

- **PASS** → apply polish chain (per market + brand_mode), deliver as `done`
- **FAIL with named sub-critic** → re-dispatch source agent with feedback:
  - Hook FAIL → `hook-agent` (rewrite to clear hook window, fix triad, pass 3Q)
  - Production FAIL → `storyboard-agent` / `audio-agent` / `production-mode-agent` (specific failures)
  - Algorithm-fit FAIL → `format-agent` / `storyboard-agent` / `audio-agent` (length/captions/audio rule mismatch)
  - Brand-fit FAIL → `voc-extraction-agent` / `hook-agent` / `copy-pack-agent` (re-pull VoC, kill generic tropes)

**Loop cap:** 2 cycles. After cycle 2 with any FAIL remaining, ship `done_with_concerns` with concerns pinned at top of brief.

---

## Polish Chain (Layer 2 post-critic)

After PASS, apply language polish to the spoken-line section (Hook verbal + VO direction + on-screen text where it's spoken text):

| (Market, Brand mode) | Polish chain |
|---|---|
| VN, founder | `vn-tone` Layer 2 on spoken-line section + full body |
| VN, company | `vn-tone` Layer 2 on full body |
| EN, founder | `humanize` Layer 2 on spoken-line section |
| EN, company | none |
| Other | flag `polish-chain-extension-needed` |

The polish chain runs as a final pass over the relevant sections — not a re-dispatch of craft agents. See `references/polish-chain.md`.

---

## Output Artifact Structure

`.agents/mkt/short-form-brief/[slug]/brief.md` (hero) — full template lives in `.agents/meta/short-form-brief-spec.md` §5.1. Frontmatter:

```yaml
---
type: short-form-brief
role: hero
status: done | done_with_concerns | blocked | needs_context
date: [YYYY-MM-DD]
slug: [slug]
angle: [free text]
brand_mode: founder | company
production_mode: live-action | motion-graphic | mixed
market: [region]
hero_platform: tiktok | reels | shorts | x | linkedin
variants: [list]
research_artifact: .agents/mkt/short-form-research.md
research_trend_signals_date: [YYYY-MM-DD]
research_mechanics_date: [YYYY-MM-DD]
campaign_tie_in: [slug or null]
critic_passes: [hook, production, algorithm-fit, brand-fit]
critic_loop_count: [1 | 2]
polish_chain_applied: vn-tone | humanize | none
---
```

**Body sections (in order):**
1. TL;DR for the Producer
2. What This Brief Bets On (traces to research)
3. Audience & Voice (VoC phrases, register, polish chain applied)
4. Format Specification
5. Hook (recommended + 2 alternatives, all with 3Q test)
6. Storyboard (shot/scene table)
7. On-Screen Text Choreography
8. Audio Plan
9. Caption (per platform)
10. CTA
11. Production Notes (live-action OR motion-graphic OR both)
12. What NOT To Do (per-platform failure modes from research)
13. Success Criteria (retention/completion/engagement targets)
14. Variant Roadmap (links to variants/[platform].md)

`variants/[platform].md` template starts with "What Changed From Hero" — guards against caption-only resizing.

---

## Completion Status

- **DONE** — all 4 critics PASS within ≤2 cycles. Hero + all requested variants produced.
- **DONE_WITH_CONCERNS** — loop cap reached; remaining FAILs surfaceable as warnings. Concerns pinned at top of artifact.
- **BLOCKED** — research stale beyond windows AND user declined re-run; ICP read fails; WebSearch/WebFetch blocked when verifying audio.
- **NEEDS_CONTEXT** — required inputs missing (no research AND user declined to proceed; no BRAND.md AND brand_mode unresolvable). State which upstream skill provides what's missing.

---

## Format Conventions

- All dates ISO 8601 (`YYYY-MM-DD`).
- All timings in seconds (`0:03–0:05`), not vague phrases.
- All shots specify framing per `references/storyboard-grammar.md` (ECU/CU/MCU/MS/MLS/LS/WS/EWS).
- All hooks tag archetype name from research catalog.
- All VoC phrases quoted exactly — no paraphrasing.
