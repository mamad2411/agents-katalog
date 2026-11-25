---
name: creative-ads-explorer
description: Rapidly generate up to 25 distinct ad creative hypotheses for testing. Produces a matrix of angles (pain, benefit, social proof, urgency, curiosity, comparison) x formats (static, carousel hook, UGC-style, bold-text overlay) with headline, visual prompt, and rationale for each, then generates the visuals with any image tool. Use when the user wants "ad variations", "ad concepts", "creative testing batch", "give me 25 ads", or paid-social creative ideation. Part of the Creative Production set.
---

# Creative — Ads Explorer

Pump out a broad, diverse batch of ad hypotheses for A/B/n testing. This is the *exploration* stage: quantity + diversity beat polish. The goal is to cover the message space so the market tells you what works — not to perfect one ad.

## When to use
- Launching paid social/display and need a test batch.
- An existing ad is fatiguing and you need fresh angles.
- Validating which *message* resonates before investing in production.

## When NOT to use
- You already know the winning angle and just need it finished → `creative-polish`.
- You're merchandising a specific discount/bundle → `creative-offer` (sharper for that).
- No visual direction exists and brand look matters → lock it via `creative-explore` first.

## Inputs (ask only what's missing)
- **Product + core offer** (what they get).
- **Audience + their #1 pain or desire** (the emotional hook).
- **Platform**: Meta, TikTok, Google Display, X, YouTube — sets aspect + length limits.
- **Locked visual direction** (from `creative-explore`) if available, so the batch stays on-brand.

## The angle × format matrix
Build hypotheses by crossing **angles** with **formats**:
- **Angles**: pain, benefit, social-proof, urgency/scarcity, curiosity/pattern-interrupt, comparison/vs-incumbent, founder/origin story, transformation/before-after.
- **Formats**: static hero, hook-frame (thumb-stopper top third), UGC mock (handheld, casual), bold-text overlay, before/after split, problem→solution 2-panel.

Not every cell is worth filling — pick the combinations most likely to resonate for THIS audience.

## Workflow
1. Pick the count (default 12, max 25). Choose the highest-potential angle×format cells.
2. For each: **headline** (≤7 words), subtext, **visual prompt**, and *why it might win* (the hypothesis being tested).
3. Kill near-duplicates aggressively — two ads testing the same idea waste spend.
4. Generate visuals with your image-generation tool at platform ratio (`1024x1024` square, `1792x1024` landscape, or vertical for stories/TikTok). Save to `./creative/ads/<NN>-<angle>.png`.
5. Output a ranked table; mark the top 3-5 to launch first and state what each one is testing.

## Worked example
Product: AI meeting-notes app. Audience pain: "I forget action items." Platform: Meta feed (1:1).
```
| #  | angle      | format       | headline                   | tests hypothesis              | pri  |
|----|------------|--------------|----------------------------|-------------------------------|------|
| 1  | pain       | hook-frame   | "Forgot the action item again?" | pain-first beats feature  | HIGH |
| 2  | benefit    | static hero  | "Every decision, captured"  | calm-benefit framing          | HIGH |
| 3  | social     | UGC mock     | "My team stopped taking notes" | testimonial credibility    | HIGH |
| 4  | comparison | 2-panel      | "Otter vs us"               | switcher intent               | MED  |
| 5  | urgency    | bold-text    | "Your next meeting starts in 10" | urgency relevance        | LOW  |
```
Launch 1-3 first (distinct emotional levers); 4 if switcher traffic exists.

## Quality bar
- Each ad tests a *different* hypothesis — you can name what you'd learn from each.
- Headlines respect platform character limits (Meta primary ≤125, headline ≤40, etc.).
- Text baked into images is short and exact; passed verbatim in the prompt.
- Top picks are justified, not arbitrary.

## Common pitfalls
- **Variation theater** — 25 near-identical ads. Diversity of *angle* is the point.
- **Fabricated proof** — never invent stats, reviews, or testimonials. Flag any the user must supply real.
- **Ignoring platform specs** — wrong aspect/length gets rejected or cropped badly.
- **Polishing too early** — these are disposable hypotheses; only winners go to `creative-polish`.

## Handoff
Winning ads (post-test or top-ranked) → `creative-polish` for production finish. On-brand consistency check → reuse the `creative-explore` stub.

## Tooling
Needs a text-to-image tool to render. Without one, deliver the full matrix (headlines + prompts + hypotheses) and the user generates manually.
