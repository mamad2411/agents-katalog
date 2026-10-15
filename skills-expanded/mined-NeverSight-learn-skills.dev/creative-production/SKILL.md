---
name: creative-production
description: Orchestrator for the Creative Production skill set — turn a brief into reviewable visual assets. Routes to the right sub-skill (explore, moodboard, positioning, offer, ads-explorer, scene, shot, polish) based on where you are in the creative process. Use when the user gives a high-level creative goal like "make campaign assets", "I need visuals for X", "produce ad creative", "design product shots", or isn't sure which creative step they need. Delegates to creative-* skills.
---

# Creative Production — Orchestrator

The umbrella for the 8 `creative-*` skills. Your job: read the request, locate it in the creative process, and route to the right sub-skill. **Don't do the work here — dispatch.** Think of yourself as a creative director assigning the task, not executing it.

## When to use
- The user gives a broad creative goal ("make campaign assets", "I need visuals for the launch") and the specific step is ambiguous.
- A creative project spans multiple stages and needs sequencing.
- The user doesn't know which sub-skill they need.

## When NOT to use
- The user explicitly named a step ("write me 25 ad concepts") → go straight to that sub-skill.
- The task is product-design/prototyping, not visual asset creation → `product-design` orchestrator.

## The pipeline
```
DIRECTION                 ASSETS                          FINISH
creative-explore ─────┐
creative-moodboard ───┼──►  creative-scene  ───────┐
creative-positioning ─┘     creative-shot           ├──►  creative-polish
                            creative-ads-explorer    │
                            creative-offer ──────────┘
```
Direction is locked first, assets are generated against it, winners are polished last.

## Routing table
| User intent / phrasing | Route to |
|---|---|
| "what style / which look", no direction locked | `creative-explore` |
| "align the team", "reference board", "territories" | `creative-moodboard` |
| "make visuals match our strategy/positioning" | `creative-positioning` |
| "sell this offer/deal/bundle", "promo creative" | `creative-offer` |
| "ad concepts", "variations to test", "25 ads" | `creative-ads-explorer` |
| "product in use", "lifestyle shot", "show it being used" | `creative-scene` |
| "different angles", "PDP/ecommerce set", "shot list" | `creative-shot` |
| "finalize", "clean up", "production-ready", "fix artifacts" | `creative-polish` |

## How to orchestrate
1. **Check for a locked direction.** If none exists, start with `creative-explore` (single look) or `creative-moodboard` (team alignment) or `creative-positioning` (strategy-led). Never generate final assets against an unlocked direction.
2. **Route asset generation** to `scene` / `shot` / `ads-explorer` / `offer` based on the deliverable.
3. **Always finish** deliverables through `creative-polish`.
4. **Carry the locked direction + prompt stub forward** so every sub-skill stays consistent — this is what makes a set look like one campaign.

## Worked example
Request: "We're launching a coffee subscription. I need everything — a look, a hero, some ads, and a clean set for the site."
```
plan:
 1. no look locked → creative-explore  → user picks "Warm Ritual", stub saved
 2. hero lifestyle  → creative-scene    (reuse stub) → "morning pour" hero
 3. ad test batch   → creative-ads-explorer (reuse stub) → 12 hypotheses
 4. site product set→ creative-shot      (reuse stub) → 6-angle PDP set
 5. finish winners  → creative-polish    → final hero + top 3 ads + PDP set
dispatch order respects: direction → assets → polish
```

## Quality bar
- A direction is locked before any final asset is produced.
- Every dispatched sub-skill receives the same locked direction/stub (coherent set).
- The user sees a clear plan (which skills, in what order) before execution on multi-stage requests.

## Common pitfalls
- **Doing the work here** — this skill decides WHICH skill; the sub-skill executes. Don't generate images in the orchestrator.
- **Skipping direction-lock** to save time — costs far more in inconsistent output later.
- **Losing the stub** between stages — leads to a set that looks like 5 different brands.

## Tooling
Image generation happens inside the sub-skills via a text-to-image tool. If none is available, the sub-skills return prompts to run manually; the orchestrator still sequences the work.
