---
name: steam-launch-readiness
description: Prepare Steam launch readiness for PC games including store page, capsule art, trailer, screenshots, tags, wishlist funnel, demo, playtest, achievements, cloud saves, controller support, localization, pricing, discounts, refund expectations, community hub, patch notes, reviews, and launch operations. Use when launching, auditing, or improving a game on Steam.
---

# Steam Launch Readiness

Use this skill to turn a Steam release into a coordinated product, store, community, and live-ops launch.

## Workflow

1. Identify game genre, audience, launch stage, monetization model, languages, and release strategy.
2. Read `references/steam-launch-systems.md`.
3. Audit store page promise, wishlist funnel, demo/playtest plan, build quality, community readiness, pricing, and support.
4. Separate pre-launch, launch-day, first-week, and post-launch operations.
5. Produce a readiness matrix with blockers, assets, telemetry, and review-risk mitigations.

## Guardrails

- Do not ship a store promise the build cannot fulfill.
- Do not treat wishlists as a vanity metric; connect them to demo, updates, launch timing, and conversion.
- Do not ignore refund, save loss, performance, controller, or community issues during launch week.

## Output format

```text
Game/launch context:
Release strategy:

Readiness matrix:
- Store page:
- Build/platform:
- Community/support:
- Launch operations:

P0 blockers:
- <blocker> -> owner, proof needed

Wishlist/review plan:
- <action> -> metric, timing
```
