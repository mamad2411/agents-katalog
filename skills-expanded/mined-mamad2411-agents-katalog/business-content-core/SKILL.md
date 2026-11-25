---
name: business-content-core
description: "Shared reference for the business-content cluster: the source-derived Voice Profile every lane reuses, the research/evidence substrate, the per-channel message contract, and the publish/market/fund/reach lane map. USE WHEN drafting any launch-, reputation-, or fundraising-sensitive content, building a Voice Profile, or planning multi-channel outbound — the interlocking conventions every spoke shares."
cluster: business-content
version: 1.0.0
---

# Business-Content Core

Shared model for the `business-content` cluster. The publish, market, fund, and reach spokes
all depend on the same two upstream artifacts and the same channel discipline — keep them
consistent here so no spoke contradicts another or drifts into generic AI copy.

## 1. The model the cluster turns on: voice-first, evidence-backed, channel-native

Every output in this cluster is the same pipeline, regardless of lane:

```
Real sources ──derive──> VOICE PROFILE ─┐
                                        ├──shape──> Draft ──fit──> Channel-native output
Market/competitor facts ──ground──> Evidence ─┘
```

Two upstream artifacts feed everything downstream:

- **VOICE PROFILE** — a reusable style fingerprint built from *real* source material (posts, essays, launch notes, docs, site copy), not platform exemplars. It is the single source of truth for tone; downstream lanes **consume** it, they do not re-derive style per draft. → `brand-voice`
- **Evidence** — market size, competitor positioning, fund/diligence facts with source attribution. Business claims trace to this, never to invention. → `market-research`

**Rule:** if an output is voice-sensitive, the `VOICE PROFILE` is an input, not an afterthought; if it makes a business claim, that claim is sourced. Missing either is a defect, not a style choice.

## 2. The four lanes (and how they compose)

- **Publish** (own channels) → `article-writing` (long-form), `content-engine` (platform-native systems, repurposing), `seo` (search visibility).
- **Market** (the launch) → `marketing-campaign` — itself an orchestration layer that pulls `brand-voice`, `content-engine`, and `seo` into one multi-channel launch.
- **Fund** (investor-facing) → `investor-materials` (decks/memos/models, kept mutually consistent), `investor-outreach` (cold/warm/follow-up/update emails).
- **Reach** (outbound & network) → `lead-intelligence` (full find→score→path→enrich→draft pipeline), `social-graph-ranker` (the standalone bridge-ranking engine it runs internally).

Lanes share the substrate, so a single launch can cross several: `brand-voice` → `marketing-campaign` → `content-engine`/`seo`, then `lead-intelligence` for outbound — all on one `VOICE PROFILE`.

## 3. The channel contract (why "reuse the copy everywhere" is a tell)

A message is shaped for its surface; the same paragraph pasted across email, LinkedIn, and X is
an anti-pattern. Pick **one primary channel**, in warmth order:

| Channel | Use for | Shape |
|---|---|---|
| Warm intro (email) | highest-value asks with a viable bridge | one ask, one concrete reason, forwardable blurb |
| Direct email | cold high-value, investor, partnership | plain specific subject, open from something real |
| LinkedIn DM | target active there / stronger graph there | shorter than email, no fake professional warmth |
| X DM or reply | high-context operator/builder/investor | tightest; reference something real from their timeline |

Channel selection and the bridge math (which targets earn a warm intro vs. cold outreach) come
from `social-graph-ranker`; the drafting voice always comes from the `VOICE PROFILE`.

## 4. Conventions

- **Voice before draft.** Run `brand-voice` first for anything launch-, reputation-, or fundraising-sensitive; reuse the latest confirmed `VOICE PROFILE` across related tasks in the same session.
- **Source before claim.** Route business/market claims through `market-research`; attribute them.
- **Consistency across a document set.** Investor assets (deck, one-pager, memo, model) must agree on the same numbers and narrative — `investor-materials` owns that consistency.
- **Repurpose, don't re-author.** `content-engine` adapts one source asset across platforms without flattening the author's voice.
- **No fabricated metrics, logos, or traction.** If a number isn't sourced or supplied, mark it as an assumption.

## 5. Shared guardrails

- **Voice-first**: one `VOICE PROFILE` flows everywhere; never default to generic AI cadence or re-derive style per draft.
- **Evidence-backed**: every business claim traces to a real source; flag assumptions explicitly.
- **Channel-native**: one primary channel, message shaped for it; identical copy across channels is a tell.
- **Draft, don't send**: produce outreach as drafts; never auto-send without explicit user approval.
- **Ban the slop**: kill curiosity-bait hooks, "not X, just Y", "no fluff", "game-changer", "excited to share", forced lowercase, founder-journey filler, social-proof stacking, and bulk-merge field tells.
- **Which spoke**: the *engine* (`social-graph-ranker`) when the user wants the ranking/math standalone; the *pipeline* (`lead-intelligence`) when they want the full outbound workflow.
