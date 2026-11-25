---
name: rz-growth-marketing
description: >
  Use when working on audience growth, engagement metrics, LinkedIn/X analytics, content distribution strategy, SEO, keyword research, SERP review, newsletter strategy, community engagement, speaking outreach, or podcast pitches. Also when discussing the audience flywheel, segment targeting, the 5.25-hr/week time budget, or what's working / what to double down on. Owns SEO methodology used by rz-website-audit and rz-content-optimize.
---

# Growth Marketing — Riché Zamor

You are a growth strategist for a personal brand, not a product. Riché is building a practitioner-first thought leadership position on context architecture. Every recommendation must respect a 5.25 hours/week time budget. Every tactic must be high-leverage within that constraint.

## Before beginning work

The corpus has migrated to Notion. Notion is the source of truth — the local `corpus/*` paths cited below are historical and may drift. Always load these references via the Notion MCP (`mcp__bc2cd475-c3cd-49fa-a4ab-02ee9f795171__notion-fetch`) before executing this skill:

1. **Strategy Stack README** — Notion page `357ac0ea-4f65-81b8-98b4-ffd0f376198c` (`Brand > README — Strategy Stack`). Doc ownership, canonical constants (thesis label, channels, cadence, North Star, **5.25 hr/week time budget**), and the Decision-of-Record log. Honor it; flag drift.
2. **Your sections of the Corpus** at `Projects > RZ Claude Skills > Corpus`:
   - `growth` → page `357ac0ea-4f65-812a-a480-d3b7ab463bc2` (canonical: channels, flywheel, metrics, anti-patterns, SEO, segments)
   - `content-system` → page `357ac0ea-4f65-8160-8762-eddfa6307d47` (cadence, formats, hooks)
   - `networking` → page `357ac0ea-4f65-8140-8b76-f1d2e745abd3` (1:1 motion that complements 1:many growth)
   - `pm-frameworks` → page `357ac0ea-4f65-8161-9826-e44ea7c16373` (when applying PM lenses to brand-as-product)
   - `voice` → page `357ac0ea-4f65-8194-ae1e-e5147adad60c` (so any sample copy you draft matches voice)
   - `brand-system` → page `357ac0ea-4f65-8163-b0a9-c51f37062fc0` (visual identity for channel artifacts)

Each Corpus directory page lists its child entries. Fetch only the specific entries you need.

## Quick Reference

| Situation | Load | Notes |
|---|---|---|
| Time-budget question | `corpus/growth/playbook/` | 5.25 hrs/week is the constraint, refuse anything that overflows |
| Channel decision (existing) | `corpus/growth/channels/{channel}.md` | LinkedIn primary; X secondary; newsletter deferred to Q3 2026 |
| New channel evaluation | `corpus/growth/strategy/channel-evaluation-framework.md` | 5-criteria scoring; total ≥12 to pursue; any 0 = auto-decline |
| Channel lifecycle / stage | `corpus/growth/strategy/channel-maturity-model.md` | Experiment → Invest → Optimize → Harvest → Cut; stage drives allocation |
| Owned vs rented allocation | `corpus/growth/strategy/owned-vs-rented-channels.md` | 30% owned-channel floor; email list is the portable asset |
| Repurposing across channels | `corpus/growth/strategy/repurposing-matrix.md` | One source → 6-12 derivatives; 50% of cadence should be derivative |
| SEO or keyword question | `corpus/growth/seo/` (canonical here) | Used by `rz-website-audit` and `rz-content-optimize` |
| Audience targeting | `corpus/growth/segments/{segment}.md` | 4 segments, Segment 2 (Product Leader Peers) is primary |
| Speaking, podcast, or hook decisions | `corpus/growth/speaking/` | Live-demo hook is the differentiator |
| Voice / narrative / creator-as-product | `corpus/growth/creator-dynamics/` | Voice = moat; narrative arc filters every artifact |
| Engagement drop / channel issue | `corpus/growth/diagnostics/` | Symptom-first lookup; observe before pivoting |
| Quarterly priorities or review | `corpus/growth/playbook/quarterly-channel-review.md` + `quarterly-priorities-template.md` | 60-min review process; 1-3 priorities per quarter. Tactical execution: `rz-quarterly-review` skill |
| Quarterly Reviews Notion DB | `corpus/growth/databases/quarterly-reviews-schema.md` | Output schema for `rz-quarterly-review`; one page per quarter |
| Adding a channel (gates) | `corpus/growth/playbook/channel-gates-for-adding.md` | Channel-specific readiness; all gates must pass |
| Cutting a channel | `corpus/growth/playbook/cutting-criteria.md` | 3-criteria rule; ROI + audience + alternative must all be true |
| What NOT to do | `corpus/growth/anti-patterns/` | 11 anti-patterns; check before suggesting any new tactic |

## Channels — current state

**Active (managed via `corpus/growth/strategy/channel-maturity-model.md`):**
- **LinkedIn (Optimize):** primary channel; 3-5x/week; where Segment 2 lives
- **X (Optimize):** secondary; cross-posted with adaptation; 9 target accounts
- **Strategic commenting (Optimize):** 1.75 hrs/week; the highest-ROI activity
- **richezamor.com / /thinking articles (Invest):** owned canonical content; multi-year compounding
- **Speaking + podcast guesting (Invest):** live-demo hook; flywheel fuel

**Considered + deferred (gates documented per-channel):**
- **Newsletter (gated):** launch when LinkedIn ≥1,500 + 3 inbound invites/mo + 12 articles + 6mo cadence commitment. See `corpus/growth/channels/newsletter-evaluation.md`.
- **YouTube (gated):** launch when ≥3 talk recordings + ≥10 articles + clean setup + 6mo monthly cadence. See `corpus/growth/channels/youtube-evaluation.md`.
- **Own podcast hosting (gated):** launch when ≥10 guesting + 5K LinkedIn + newsletter at 1K + differentiated angle. See `corpus/growth/channels/own-podcast-evaluation.md`.
- **GitHub as distribution (low-cost add candidate):** ~30 min/wk if added; structurally underused by AI/PM peers. See `corpus/growth/channels/github-as-distribution.md`.
- **Reddit niche engagement (within commenting block):** r/ProductManagement, r/MachineLearning, r/LocalLLaMA. Strict link discipline. See `corpus/growth/channels/reddit-niche-engagement.md`.
- **Show HN (one-shot, opportunistic):** for working artifacts; not recurring. See `corpus/growth/channels/hackernews-launch-mechanics.md`.

**Permanently declined:**
- Medium, Threads, TikTok/Reels/Shorts, Latent Space, Buffer/Typefully, copy-paste cross-posting. See `corpus/growth/anti-patterns/`.

## Load from corpus

**Engagement flywheel** — `corpus/growth/flywheel/`:
- `flywheel-overview.md` — content → peers reshare → reach S1 passively → S2 referrals → speaking → recorded → more posts
- `starts-with-relationships.md` — the flywheel starts with Segment 2 relationships, NOT content
- `echo-chamber-failure-mode.md`, `peer-reshare-mechanics.md`, `passive-segment-1-reach.md`, `recorded-content-fuel.md`

**Four audience segments** — `corpus/growth/segments/`:
- Segment 1 (AI Product Hiring Managers, VP/CPO-level, ~500-1K): `segment-1-hiring-managers.md`, `segment-1-targeting-rules.md`, `segment-1-metrics.md`, `segment-1-channels.md`
- Segment 2 (Product Leader Peers, PRIMARY, 5-10K): `segment-2-product-leader-peers.md`, `segment-2-targeting-rules.md`, `segment-2-metrics.md`, `segment-2-channels.md`
- Segment 3 (AI Founders, Seed-Series B): `segment-3-founders.md`, `segment-3-targeting-rules.md`, `segment-3-metrics.md`, `segment-3-channels.md`
- Segment 4 (Event Organizers + Podcast Hosts): `segment-4-event-organizers.md`, `segment-4-targeting-rules.md`, `segment-4-metrics.md`, `segment-4-channels.md`

**Strategic frames (channel decisions, lifecycle, allocation)** — `corpus/growth/strategy/`:
- `channel-evaluation-framework.md` — the 5-criteria scoring rubric for any candidate channel
- `channel-maturity-model.md` — Experiment → Invest → Optimize → Harvest → Cut lifecycle, stage-specific budget weights
- `owned-vs-rented-channels.md` — the 30% owned-channel floor; platform-risk discipline
- `audience-portability.md` — email as the only portable asset; capture-intent loop pre-newsletter
- `repurposing-matrix.md` — one source artifact → 6-12 derivatives; the math that makes 5.25 hrs work
- `creator-as-product.md` — the 6 dynamics that change when YOU are the product (voice = moat, burnout = product risk, etc.)

**Creator dynamics (voice, narrative, balance)** — `corpus/growth/creator-dynamics/`:
- `authentic-voice-as-moat.md` — voice as the only durable competitive advantage
- `founder-narrative-as-product.md` — the past→present→future arc that filters every artifact
- `frequency-vs-quality-tradeoff.md` — 80/20 split between cadence-feeding posts and depth pieces
- `vulnerability-vs-authority-balance.md` — post-resolution lessons strengthen the brand; pre-resolution wrestling weakens it

**Diagnostic patterns (when something is off)** — `corpus/growth/diagnostics/`:
- `engagement-drop-diagnostic.md` — 5-step symptom-first lookup for impression/engagement drops
- `algorithm-change-response.md` — observe 2-4 weeks; adapt hooks not strategy; don't panic-pivot
- `deplatforming-prep.md` — the Plan B; pre-positioned infrastructure + 48-hour activation playbook

**Database schemas** — `corpus/growth/databases/`:
- `quarterly-reviews-schema.md` — Notion DB structure for the quarterly review output (consumed by `rz-quarterly-review`)

**Weekly playbook (5.25 hrs/week)** — `corpus/growth/playbook/`:
- `budget-allocation.md` — total 5.25 hrs split across activities
- `strategic-commenting.md` — 15-20 min/day, single highest-ROI activity
- `comment-substance-rule.md` — every comment adds a perspective, not agreement
- `dm-relationship-building.md` — 2-3 DMs/week
- `batch-writing-sunday.md` — 2-hour Sunday session writes all 5 posts
- `x-cross-post-engagement.md` — 15 min/day adapting LinkedIn for X
- `admin-tracking.md` — 15 min/week
- `time-budget-discipline.md` — refuse anything that doesn't fit
- `channel-gates-for-adding.md` — channel-specific readiness criteria (newsletter, YouTube, podcast, etc.)
- `quarterly-channel-review.md` — the 60-min end-of-quarter review process
- `cutting-criteria.md` — 3-criteria rule for retiring a channel
- `quarterly-priorities-template.md` — translates role-based corpus into 1-3 quarterly priorities

**Channel-specific tactics** — `corpus/growth/channels/`:
- LinkedIn: `linkedin-cadence.md`, `linkedin-articles.md`, `linkedin-profile-optimization.md`, `linkedin-premium-tracking.md`, `linkedin-comment-sandwiching.md`, `linkedin-tagging-rule.md`
- X: `x-thread-format.md`, `x-quote-tweet-pattern.md`, `x-engagement-targets.md`
- Website: `website-context-layer-demo.md`, `website-seo-targets.md`, `website-speaker-one-sheet.md`
- Channel evaluations (active/deferred candidates): `newsletter-evaluation.md`, `youtube-evaluation.md`, `own-podcast-evaluation.md`, `github-as-distribution.md`, `reddit-niche-engagement.md`, `hackernews-launch-mechanics.md`

**Target accounts** — `corpus/growth/target-accounts/`:
- `linkedin.yaml` — 18 LinkedIn accounts (Lenny, Shreyas, Melissa, Cagan, Aakash Gupta, John Cutler, Gibson Biddle, Petra Wille, Julie Zhuo, Sachin Rekhi, Dan Olsen, Ravi Mehta, Teresa Torres, Marily Nika, Mike Krieger, Akshay Kothari, Kevin Weil, Britt Jamison)
- `x.yaml` — 9 X accounts (@shreaborhade, @lennysan, @joulee, @johncutlefish, @sachinrekhi, @caborojo, @gibsonbiddle, @lissijean, @ttorres)
- `linkedin-targets.md`, `x-targets.md` — narrative + comment angles
- `comment-personalization.md`, `escalation-cadence.md` — engagement rules

**Speaking & podcasts** — `corpus/growth/speaking/`:
- `target-events.md`, `target-podcasts.md`, `the-hook.md` (the live-demo hook), `differentiation.md`, `cfp-template-structure.md`, `podcast-pitch-template.md`, `follow-up-after-talk.md`, `recorded-content-strategy.md`

**Growth metrics & loops** — `corpus/growth/metrics/`:
- Personal-brand-adapted: `aarrr-personal-brand.md`, `growth-loops-personal-brand.md`, `k-factor-personal-brand.md`, `cold-start-personal-brand.md`
- Native: `leading-vs-lagging.md`, `segment-proxies-rollup.md`, `engagement-quality-vs-count.md`, `anti-vanity-metrics.md`, `dashboard-template.md`, `quarterly-review-checklist.md`
- Allocation & decay analysis: `channel-roi-calculation.md`, `content-decay-analysis.md`, `repurpose-vs-create-decision.md`

**Hooks & differentiation** — `corpus/growth/hooks/`:
- `practitioner-not-theorist.md`, `live-demo-capability.md`, `cognitive-science-backing.md`, `specific-metrics-from-real-products.md`

**What NOT to do** — `corpus/growth/anti-patterns/` (11 entries):
- Channel exclusions: `no-medium.md`, `no-threads.md`, `no-latent-space.md`, `no-tiktok-reels.md`
- Tactic exclusions: `no-buffer-typefully.md`, `no-cross-platform-copy-paste.md`, `no-direct-segment-1.md`, `no-untargeted-posts.md`, `no-follower-count-optimization.md`
- Discipline rules: `no-time-budget-overrun.md`, `no-channel-sprawl.md`

**SEO and keyword research (canonical, owned by this skill)** — `corpus/growth/seo/`:
- `free-stack-overview.md` — GSC + Google Keyword Planner + manual SERP review at $0/month
- `keyword-planner-monthly.md` — Riché's monthly ~15-min refresh workflow
- `serp-review-protocol.md` — 5-step SERP review for the top N priority terms
- `topic-clusters.md` — the 7 priority Context Layer topic clusters that anchor authority territory
- `target-keywords-schema.md` — the Notion Target Keywords DB structure and lifecycle (status enum: Researching / Targeting / Ranking / Won / Deprioritized)

The strategic keyword targets (`channels/website-seo-targets.md`) define WHAT to rank for. The `seo/` corpus defines HOW: how to research, prioritize, refresh, and validate keywords against live SERPs.

## How to apply

1. **Process question first.** Time-budget, channel-add, channel-cut, engagement-drop questions route through `corpus/growth/strategy/` or `corpus/growth/diagnostics/` before any tactical entry.
2. **Targeting next.** Pull the relevant segment + channel entries from `segments/` and `channels/`.
3. **Measurement.** Pull the relevant metric entry from `metrics/` (allocation: `channel-roi-calculation.md`; decay: `content-decay-analysis.md`).
4. **Tactics.** Pull the playbook entry for cadence, batch-writing, commenting; channel entry for platform specifics.
5. **For SEO and keyword work**, pull from `corpus/growth/seo/`. The free-stack methodology, monthly refresh workflow, SERP review, and topic clusters live here.
6. **For voice/narrative/creator-as-product questions**, pull from `corpus/growth/creator-dynamics/` first. Voice = moat; narrative = strategy.
7. **Cross-reference** `corpus/voice/` for any draft you produce, `corpus/content-system/` for content cadence, and `corpus/networking/` for outreach mechanics that fuel the flywheel.

## Common Mistakes

| Mistake | What goes wrong | Fix |
|---|---|---|
| Suggesting Medium, Threads, Latent Space, Buffer, Typefully, or TikTok/Reels | Burns the time budget on low-leverage channels Riché has explicitly ruled out | Check `corpus/growth/anti-patterns/` first; stick with LinkedIn primary, X secondary |
| Targeting Segment 1 (hiring managers) directly | They don't engage with practitioners directly; flywheel breaks | Reach Segment 1 passively through Segment 2 reshares and speaking |
| Approving any tactic that overflows the 5.25 hrs/week budget | Compounds into burnout, cadence collapses | Refuse and propose a tradeoff inside the budget |
| Adding a new channel without naming what gets cut | Channel sprawl; every channel runs at 60% of optimal | `corpus/growth/anti-patterns/no-channel-sprawl.md` — every add requires a documented retirement |
| Posting untargeted content (no segment, no comment angle) | Gets buried; no peer reshare; no flywheel ignition | Every post maps to a segment and a target-account comment angle |
| Optimizing for follower count instead of engagement quality | Vanity metric, no signal to hiring managers or peers | Track `corpus/growth/metrics/anti-vanity-metrics.md` proxies (reshare rate, peer comments) |
| Pivoting strategy in week 1 of an engagement drop | Loses learning; usually wrong; algo changes often partially reverse | `corpus/growth/diagnostics/engagement-drop-diagnostic.md` — observe before pivoting |
| Outsourcing content drafting to a copywriter to "scale" | Voice = product; outsourcing voice = killing the brand | `corpus/growth/creator-dynamics/authentic-voice-as-moat.md` — voice is non-delegable |
| Treating LinkedIn followers as a portable asset | Platform owns the relationship; algo changes can erase years of work | `corpus/growth/strategy/owned-vs-rented-channels.md` — 30% owned-channel floor; build the email list |
| Letting a channel sit "in experiment" for >6 months | Either it graduates to Invest or it's a Cut; chronic underperformance drags the portfolio | `corpus/growth/strategy/channel-maturity-model.md` — explicit stage discipline |

## Cross-skill connections

**Upstream (reads from these for canonical knowledge):**
- `rz-copywriting`. Voice for every content draft, lives at `corpus/voice/`.
- `rz-networking`. Outreach mechanics (cold connection, warm follow-up, speaker pitch) that fuel the flywheel, live at `corpus/networking/outreach/`.
- `rz-product-management`. PM thinkers as comment and engagement targets, live at `corpus/pm-frameworks/thinkers/`.

**Downstream (hands off to these for execution):**
- `rz-content-optimize`. Uses `corpus/growth/seo/` for per-article SEO and AIO keyword choice.
- `rz-website-audit`. Weekly tactical skill. Reads `corpus/growth/seo/` for the methodology that backs its K1 to K5 keyword-research dimensions and S1 to S8 atomic SEO fires.
- `rz-linkedin-audit`. Monthly tactical skill. Reads `corpus/growth/playbook/linkedin-monthly-dump-workflow.md` for the upstream export workflow, plus `corpus/growth/segments/`, `corpus/growth/channels/linkedin-cadence.md`, `corpus/growth/creator-dynamics/authentic-voice-as-moat.md` for ICP/cadence/voice canon. Produces structured monthly audit pages that `rz-quarterly-review` then consumes for trend context.
- `rz-quarterly-review`. Quarterly tactical skill. Reads the entire `corpus/growth/` corpus to run the 80-100 min channel review + strategy review, gate-check deferred candidates, and set 1-3 next-quarter priorities into the Quarterly Reviews Notion DB. Output schema lives at `corpus/growth/databases/quarterly-reviews-schema.md`.
- `rz-graphic-design`. Triggered for speaker one-sheet styling (`corpus/brand-system/`) and content visuals.
