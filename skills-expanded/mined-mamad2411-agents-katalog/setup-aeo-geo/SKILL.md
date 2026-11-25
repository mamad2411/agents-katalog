---
name: setup-aeo-geo
description: Build a brand's AEO/GEO (Answer Engine Optimization / Generative Engine Optimization) strategy step by step over a 3-phase roadmap. Generates measurement spreadsheets, a share calculator that emits dated markdown reports, runs an interview to build a canonical entity definition, scaffolds JSON-LD Organization schema with stack-specific injection guides, and tracks monthly trend in a single accumulating CSV. Use when user wants to set up AEO/GEO, optimize brand mentions in ChatGPT/Claude/Gemini answers, measure AI answer share, build entity definition or schema markup for AI visibility, or asks "how do I get AI to recommend my brand", "AEO 셋업", "GEO 전략 만들어줘", "AI 답변 점유율 측정".
---

# AEO/GEO Strategy Setup

3-phase roadmap. Each phase delivers value standalone — stop after any phase. See [REFERENCE.md](REFERENCE.md) for theory (4-stage funnel, 7-step framework, channel guide, schema injection per stack).

## Phase 1 — Measure (Week 1)

Goal: know where the brand stands in AI answers today.

1. Interview user for 5 candidate questions a customer would ask AI **without naming the brand**. Examples:
   - "Best <category> for <use case>?"
   - "<competitor A> vs <competitor B> — which is better?"
   - "Is <category> safe / legal / reliable?"
2. **Warn user about workload**: "5 questions × 3 AIs × 3 runs = 45 incognito queries. Roughly 1–2 hours. Three runs are required for statistical significance — AI answers are probabilistic."
3. Generate [templates/share-tracker.csv](templates/share-tracker.csv) with the 5 questions filled in.
4. After user fills CSV, run [scripts/calculate-share.py](scripts/calculate-share.py) — outputs share %, ranking, stage (risk / growth / compete / dominate), sentiment breakdown, and writes a dated markdown report to `reports/YYYY-MM-DD.md`.

Stage thresholds: 0–10% risk · 10–30% growth · 30–50% compete · 50%+ dominate.

## Phase 2 — Define (Weeks 2–4)

Goal: a single canonical sentence used everywhere.

1. Interview 5 slots one at a time:
   - **Company name**: legal + alternate name
   - **Target customer**: who specifically
   - **Concrete metric/outcome**: numbers, not adjectives ("3만 명 작가" not "many artists")
   - **Core value**: what they get
   - **Category**: noun phrase that names the market
2. Assemble: `[Company] is a [category] for [target customer], delivering [core value] backed by [metric/outcome].`
3. Save to `entity-definition.md` at project root. Tell user: "Use this verbatim on website, press releases, LinkedIn. Inconsistency = AI sees multiple companies."
4. Distribution checklist (short term — open web, low entry barrier):
   - Namu Wiki entry (Korean brands)
   - Medium / Brunch posts (10+)
   - LinkedIn company page + founder profile
   - Crunchbase company entry
   - Press releases via wire services
   - YouTube videos with subtitles + descriptions
5. Long-term goals (12+ months, see [REFERENCE.md](REFERENCE.md)):
   - Wikipedia entry (only after meeting notability — 5+ independent reliable sources)

## Phase 3 — Systematize (Weeks 5–8)

Goal: schema markup + ongoing monitoring loop.

1. **JSON-LD Organization schema**: scaffold [templates/organization-schema.json](templates/organization-schema.json).
   - Required: `name`, `url`, `description` (reuse Phase 2 sentence verbatim), `sameAs` (social/wiki URLs)
   - Optional: `logo`, `foundingDate`, `founder`, `numberOfEmployees`, `areaServed`, `knowsAbout`
   - **Detect site stack** from `package.json` / `composer.json` / `wp-config.php`. Show injection guide from [REFERENCE.md](REFERENCE.md) for that stack (Next.js, WordPress, static HTML).
2. **Monthly monitor**: append rows to single accumulating [templates/monitoring.csv](templates/monitoring.csv) — same 5 questions plus brand-name probes. Each month adds 24 rows with `month=YYYY-MM`.
3. After 2+ months, run [scripts/track-trend.py](scripts/track-trend.py) — share % delta per AI, sentiment shift, action triggers, dated markdown report.

## Operating Rules

- **No brand-name in Phase 1 questions**: customers don't search by your brand. Strip any candidate that includes it.
- **Numbers beat adjectives**: refuse vague metric slots in Phase 2. "fast delivery" → "within 1 hour citywide".
- **Open web only**: never recommend login-walled platforms (private Slack, app-only content). AI cannot read them.
- **Reuse Phase 2 sentence**: `description` field in schema and bios must match it character-for-character.
- **Single accumulating CSV**: `monitoring.csv` grows over time. Never split per month.

## Quick Start

User says "set up GEO for our brand":

1. Phase 1 → measure first. Confirm CSV results before moving on.
2. Ask: "Continue to Phase 2 (entity definition)?"
3. Continue phase by phase until user stops.

## Reference

- Theory + channel guide + schema injection per stack: [REFERENCE.md](REFERENCE.md)
- Share tracker: [templates/share-tracker.csv](templates/share-tracker.csv)
- Schema scaffold: [templates/organization-schema.json](templates/organization-schema.json)
- Accumulating monitor: [templates/monitoring.csv](templates/monitoring.csv)
- Share calculator (writes reports/): [scripts/calculate-share.py](scripts/calculate-share.py)
- Trend tracker (writes reports/): [scripts/track-trend.py](scripts/track-trend.py)
