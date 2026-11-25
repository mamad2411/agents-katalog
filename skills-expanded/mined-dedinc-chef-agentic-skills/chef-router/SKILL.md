---
name: chef-router
description: >-
  Entry point for the Chef Agentic Skills library. Use first for general cooking,
  recipe creation or repair, meal planning, learning, adaptation, preservation,
  food-safety questions, and any request where several chef skills could apply.
  Route to the smallest useful chain and keep attention, experience, equipment
  and measurement needs separate.
---

# Chef Router

The library is a brigade, not a checklist. Classify -> select -> read -> cook. Every selected skill must change the result.

## Shared contracts

- `chef-constraints-adaptation` defines cue-first, equipment-aware recipe writing. Read it when execution detail or equipment adaptation matters.
- `chef-food-safety` owns safety controls. **Read it when a safety number/process governs the answer**; do not treat an "always-on" label as if an unloaded table were already in context.
- `chef-accessible-cooking` is an explicit execution modifier for ADHD/СДВГ, fatigue, overwhelm, one-thing-at-a-time workflows, household measures, burner choreography or live stage-by-stage help. It counts as one routed skill and does not imply beginner technique.

## Step 1 — Primary verb

| Verb | Purpose | Usual lead |
|---|---|---|
| MAKE | create/cook a dish | named dish/cuisine skill, or `chef-recipe-developer` |
| FIX | rescue/audit | `chef-recipe-optimizer`, `chef-sauces-guide` or `chef-flavor-balance` |
| JUDGE | evaluate | `chef-culinary-inspector` |
| PLAN | menu/event/meal prep | `chef-menu-event-planning` or `diet-goal-nutrition` |
| LEARN | build skill | `chef-training-progression` |
| ADAPT | fit equipment/diet/substitution/execution | relevant owner |
| PRESERVE | ferment/pickle/can/cure | `chef-fermentation-preservation` |

## Step 2 — Material modifiers

| Signal | Add only when it changes the answer |
|---|---|
| iconic named dish with an actual bundled spec | `chef-world-classics` |
| Chinese/Japanese/French/Italian/Mexican/German/Indian/Silk Road context | one cuisine skill |
| meat / seafood / vegetables / grains-legumes as the main technical question | one ingredient guide |
| sauce failure | `chef-sauces-guide` |
| bread/dough | `chef-baking-doughs-guide` |
| pastry/chocolate/sugar | `chef-pastry-confectionery` |
| spices/blends/dosing | `chef-spice-guide` |
| appliance conversion | `chef-equipment-gastrophysics` |
| pantry improvisation | `chef-pantry-improviser` |
| unavailable ingredient | `chef-ingredient-localizer` |
| budget | `chef-kitchen-economics` |
| leftovers/scraps | `chef-zero-waste` |
| children/picky or food-sensory eating | `chef-kids-sensory` |
| allergy/restriction | one matching `diet-*` owner; add safety when cross-contact matters |
| ADHD/СДВГ, low focus, fatigue, one thing at a time, can't estimate by eye, household measures, burner-by-burner or explicit beginner execution help | `chef-accessible-cooking`; preserve the cook's actual technique level |

Negative triggers: an ADHD question unrelated to cooking is outside this library; a historical mention of ADHD does not force verbose execution for "what is cumin?"; "short answer" stays short. Adult attention support does not route to the kids skill unless food-sensory/child context is actually present.

## Step 3 — Chain discipline

Target **1–4 skills**, hard ceiling **5 per active route**. Complex projects may use separate bounded waves; do not create a 12-skill simultaneous context.

`chef-world-classics` wins only when it contains the named dish. A famous name is not proof that a spec exists. A cuisine skill usually beats a generic ingredient guide for cuisine-specific method; add the guide only for a missing hard number/failure mode. For live rescue, speed wins: one repair skill can be enough.

## Examples

| Request | Chain |
|---|---|
| "Курица по-китайски, СДВГ, без параллельной суеты" | `chef-cuisine-chinese` + `chef-accessible-cooking`; add safety if a chicken endpoint is needed |
| "Придумай мясо с рисом, новичок, нужны ложки и конфорки" | `chef-recipe-developer` + `chef-meat-guide` + `chef-grains-legumes-guide` + `chef-accessible-cooking` |
| "Я опытный повар с СДВГ, распиши порядок карбонары" | `chef-world-classics` + `chef-accessible-cooking`; no knife kindergarten |
| "Сметана сворачивается прямо сейчас" | `chef-sauces-guide`; immediate rescue first |
| "Какие специи к нуту?" | `chef-spice-guide` |
| "Можно ли этот рис есть завтра вечером?" | `chef-food-safety` |

## Output shape

MAKE -> executable recipe. FIX -> immediate cause/fix, full audit only if requested. JUDGE -> verdict + prioritized fixes. PLAN -> plan/timeline. LEARN -> next drill. ADAPT -> adapted artifact + tradeoffs. PRESERVE -> complete controlled method + source/safety gates.

Do not stack audit prose, legal boilerplate and a recipe unless the user asks. Project-level responsibility is in `/DISCLAIMER.md`; local safety warnings still appear exactly where they change an action.
