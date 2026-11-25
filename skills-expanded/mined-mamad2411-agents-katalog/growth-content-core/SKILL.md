---
name: growth-content-core
description: "Shared reference for the growth-content cluster: the searchable-vs-shareable decision, the buyer-stage map every asset is aimed at, the one product-marketing-context source of truth all spokes read, voice-of-customer conventions, and the asset × stage routing matrix. USE WHEN planning a campaign, picking a content type, or writing any growth asset — the interlocking rules every spoke shares."
cluster: growth-content
version: 1.0.0
---

# Growth Content Core

Shared model for the `growth-content` cluster. The strategy, writing, conversion, and launch
spokes all depend on these decisions — keep them consistent here so no spoke contradicts another.

## 1. The decision this domain turns on: searchable vs. shareable

Every asset must be **searchable, shareable, or both** — and you decide *before* you write.
Prioritize in that order; search demand is the foundation that compounds, shareable demand is the
spark that spreads.

```
                 captures EXISTING demand          creates NEW demand
                 (people already looking)          (spread an idea)
   SEARCHABLE  ──────────────────────────┐   ┌────────────────────── SHAREABLE
   keyword-led · intent-matched          │   │   insight-led · emotion-driven
   comprehensive · structured            ▼   ▼   novel · contrarian · story
                        ┌──────────────────────────────┐
                        │   BOTH = the strongest asset  │
                        │  (rank AND get passed around) │
                        └──────────────────────────────┘
```

- **Searchable** → target a specific query, match intent exactly, structure for skim + LLM citation. Owned by `content-strategy` (planning) and `content-research-writer` (writing).
- **Shareable** → lead with a novel insight, original data, or a take worth repeating. Same two spokes, different mode.
- If an asset is *neither*, it has no distribution. Send it back to `content-strategy`.

**Rule:** name the call (searchable / shareable / both) at the top of every brief. It dictates the
headline, the structure, and the channel.

## 2. The buyer stage every asset is aimed at

One asset serves **one stage**. The stage sets the keyword modifiers, the CTA, and the proof.

| Stage | Modifiers / intent | Asset that fits | Primary spoke |
|---|---|---|---|
| **Awareness** | "what is," "how to," "guide to" | educational blog, checklist, quiz | `content-research-writer`, `lead-magnets` |
| **Consideration** | "best," "vs," "alternatives," "comparison" | comparison page, assessment, webinar, ad | `copywriting`, `ad-creative`, `lead-magnets` |
| **Decision** | "pricing," "demo," "trial," "templates" | pricing copy, ROI tool, sales email | `copywriting`, `free-tool-strategy`, `cold-email` |
| **Retention/Expansion** | onboarding, upsell, win-back | lifecycle email, usage nudge | `email-sequence` |

Mismatched stage is the most common failure: a decision-stage CTA on an awareness asset converts
no one. State the stage in the brief.

## 3. The one source of truth: product-marketing-context

`product-marketing-context` writes `.agents/product-marketing-context.md` — positioning, ICP,
JTBD, competitors, differentiation, objections, **voice-of-customer language**, proof points,
brand voice. **Every spoke reads it first.** It exists so the user never re-explains their product
and so all output stays consistent.

- New project → run `product-marketing-context` before any other spoke.
- It exists → spokes pull voice + proof from it and only ask for task-specific gaps.
- Missing on an older setup → check `.claude/product-marketing-context.md` and offer to move it.

## 4. Voice & evidence conventions (shared by all spokes)

- **Customer language > company language.** Mirror verbatim phrases from reviews, calls, support tickets. Exact words beat polished descriptions.
- **Specific > vague.** "Cut reporting from 4 hours to 15 minutes," not "save time." Numbers, timeframes, names.
- **Benefits > features.** Every feature gets a "which means…" bridge to an outcome.
- **One idea per unit.** One CTA per page/email, one job per asset, one argument per section.
- **Proof is sourced, never invented.** Pull stats, testimonials, and logos from the context doc or ask for them. Fabrication is a hard stop.
- **Banned filler:** "leverage," "synergy," "best-in-class," "seamless," "cutting-edge," "utilize," "robust," exclamation points, and "I hope this email finds you well."

## 5. Asset × funnel routing matrix

| Funnel stage | Plan | Write | Convert | Launch |
|---|---|---|---|---|
| **Spoke(s)** | `content-strategy`, `marketing-ideas`, `marketing-psychology` | `content-research-writer`, `copywriting`, `copy-editing` | `lead-magnets`, `free-tool-strategy`, `cold-email`, `email-sequence`, `ad-creative` | `launch-strategy` |
| **Output** | pillars, calendar, ideas, principles | articles, page copy, edited copy | gated assets, tools, outbound + lifecycle email, ads | GTM plan, Product Hunt, rollout |
| **Reads context doc** | yes | yes | yes | yes |

**Standard pipeline:** strategy → write → edit → convert → launch. Cold outbound (`cold-email`)
and lifecycle (`email-sequence`) are distinct lanes — cold = no relationship, lifecycle = existing
contact. Downloadable (`lead-magnets`) vs. interactive (`free-tool-strategy`) is the other common fork.

## 6. Shared guardrails

- **Searchable, shareable, or both** — name it before writing; no asset ships without a distribution path.
- **One asset, one stage, one job, one CTA.**
- **Customer language**, never buzzwords; read it aloud — if it sounds like marketing, rewrite it.
- **Proof is sourced, never invented** — hard stop on fabricated stats/testimonials/logos.
- **Draft, then `copy-editing`** — the seven sweeps run on a complete draft, not midstream.
- **Urgency/scarcity only when genuine.**
- **Context first** — pull voice and proof from `product-marketing-context.md`; if it's missing, that's the first task.
- Sibling clusters: `business-content` (voice-profile-led GTM writing — articles, investor materials, outbound), `social-media` (channel-native social). Reach for those when the work is brand-voice or platform-specific rather than demand-generation.
