---
name: creative-angle-lab
description: "When the user wants new paid social creative angles, hook banks, UGC briefs, TikTok or Meta ad concepts, creative testing matrices, performance creative strategy, offer angles, customer objection angles, top-spending creative analysis, Gemini image or video breakdowns, awareness-level mapping, avatar mapping, or ways to turn reviews and ad data into new tests. For finished scripts, use ugc-script-writer."
metadata:
  version: 1.0.0
---

# Creative Angle Lab

Turn context, performance data, reviews, objections, and competitor observations into testable creative angles.

## Before Ideation

1. Read `.agents/vibemarketer-context.md` if it exists.
2. Pull in performance findings from `meta-performance-analyst` if available.
3. Ask for or inspect customer reviews, comments, support tickets, top-spending ads, losing ads, landing page copy, and competitor examples when useful.
4. Separate proven facts from hypotheses.

## Reference

Load only what is needed:

- `references/angle-frameworks.md` for angle types and testing structures.
- `references/gemini-creative-analysis.md` for full image/video creative breakdowns using Gemini.

## Scripts

Use these when the user wants executable LLM creative analysis:

- `scripts/build_creative_handoff.py`: convert normalized Meta ad rows into a top-creative handoff for this skill, with optional Meta Ads CLI creative metadata and asset downloads.
- `scripts/analyze_creative_gemini.py`: send image or video assets to Gemini.
- `scripts/analyze_creative_batch_gemini.py`: analyze a top-creative handoff CSV with Gemini and synthesize the portfolio angle map.
- `scripts/analyze_static_creative_openai.py`: analyze static images with OpenAI Responses API.
- `scripts/analyze_static_creative_claude.py`: analyze static images with Claude Messages API.

Gemini remains the default for video. OpenAI and Claude are static-creative fallbacks unless the user asks otherwise.

## Workflow

1. Extract raw material
   - Customer pains
   - Desired outcomes
   - Objections
   - Proof points
   - Product mechanisms
   - Competitor gaps
   - Performance signals
   - Top-spend creative assets and transcripts

2. Build angle territories
   - Group ideas by customer motivation, not by minor wording.
   - Avoid duplicates disguised as new angles.

3. Prioritize
   - Score each angle on relevance, proof strength, novelty, production ease, and risk.
   - Favor angles that can be tested with multiple hooks and creator types.

4. Output test plan
   - Angles
   - Hooks
   - Creator brief
   - Visual concept
   - Proof asset
   - CTA
   - Success metric

## Top-Spend Creative Analysis

When creative assets are available, do not rely only on thumbnail/frame sampling. Send images or videos to Gemini for a full visual breakdown when the environment has Gemini access and user consent.

Use `meta-performance-analyst` as the upstream triage layer. It should identify top-spend creatives, high-CPMr watch items, efficient reach candidates, and campaign-level dependencies. This skill should then explain the creative patterns behind those signals and produce the next angle map. Keep media-buying allocation decisions in `meta-performance-analyst`; keep hook, avatar, awareness-level, and creative expansion decisions here.

When starting from Meta output, build the handoff first:

```bash
python3 skills/creative-angle-lab/scripts/build_creative_handoff.py \
  --ads data/live-analysis-pack-v3-conversions/meta-active-hierarchy/ads_normalized.csv \
  --output-dir outputs/creative-angle-lab/demo-brand \
  --resolve-meta-creatives \
  --download-assets
```

Then run the Gemini portfolio read:

```bash
python3 skills/creative-angle-lab/scripts/analyze_creative_batch_gemini.py \
  --handoff-csv outputs/creative-angle-lab/demo-brand/creative-handoff.csv \
  --output-dir outputs/creative-angle-lab/demo-brand/gemini-analysis
```

Default artifact structure:

- `portfolio-synthesis.md`: standalone executive read for fast sharing.
- `creative-angle-lab-report.md`: per-creative report only; it should not duplicate the full portfolio synthesis.
- `per-creative/*.md`: individual Gemini reads for each analyzed ad asset.

Use `--download-assets` only when the account token can access downloadable image or video URLs. If only thumbnails or metadata are available, label visual analysis as incomplete and use the handoff to request/source the original assets. For videos, prefer the downloaded MP4. For static images, prefer the ad-image hash URL over `thumbnail_url`.

In synthesis outputs, cite actual Meta ad IDs and short names. Avoid ordinal-only references like "Creative 2" because they are hard to trace back to Ads Manager.

For each top-spending creative, classify:

- Angle
- Hook
- First 3 seconds
- Awareness level
- Avatar
- Core desire
- Core pain
- Mechanism
- Proof type
- Offer frame
- Visual style
- Creator archetype
- CTA
- Comments or objections if supplied

Then produce a portfolio read:

- What the account is over-indexed on.
- What awareness levels are missing.
- Which avatars are under-served.
- Which winning motifs should be expanded.
- Which themes are fatigued or too repetitive.

## Default Output

```markdown
## Angle Map
| Priority | Angle | Customer Insight | Proof Needed | Risk | Why Test |
| --- | --- | --- | --- | --- | --- |

## Hook Bank
| Angle | Hook | Format | Notes |
| --- | --- | --- | --- |

## Creative Test Matrix
| Test | Angle | Creator | Format | Hook | Proof | CTA | KPI |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Creative Portfolio Diagnosis
| Pattern | Evidence | Coverage | Gap | Expansion |
| --- | --- | --- | --- | --- |

## Production Briefs
### Brief 1: [Angle]
- Creator:
- Opening visual:
- Product moment:
- Proof:
- Watchouts:
- Variants:
```

## Quality Bar

- Make angles specific enough to shoot.
- Include the customer belief each angle is trying to change.
- Include proof requirements.
- Avoid making claims the brand cannot support.
- Do not generate 50 shallow ideas when 8 strong testable angles are better.
