---
name: canon-micro-interactions
description: Use when designing small, functional animations tied to user actions — toggle switches, like buttons, checkbox ticks, pull-to-refresh, swipe-to-dismiss. Covers the trigger-feedback loop, animation budgets, spring physics, and when micro-interactions become distractions. Trigger when the user mentions micro-interaction, toggle animation, feedback animation, or interaction detail.
---

# CANON · Micro-interactions

A micro-interaction is an animation that acknowledges an action. Toggle flips, hearts fill, checkmarks draw. The test is always: does removing it leave the user unsure whether the action worked?

## The feedback loop

Every micro-interaction has four parts: trigger → rules → feedback → loop/exit.

- **Trigger**: user taps, hovers, or the system state changes.
- **Rules**: what should happen (toggle on, add to favorites, validate).
- **Feedback**: the visual response (switch slides, heart fills, check draws).
- **Loop/exit**: does it repeat? Reset? End?

## Duration budget

Micro-interactions live in the 100–300ms envelope (`canon-motion` micro and short ranges). Longer and they block the next interaction.

| Interaction | Duration |
|---|---|
| Toggle switch slide | 150–200ms |
| Checkbox check-draw | 150ms |
| Like heart fill | 200–300ms |
| Button press scale | 100ms |
| Pull-to-refresh spin | continuous until complete |
| Swipe-to-dismiss | 200ms exit after threshold |

## Easing

- **Snappy**: `cubic-bezier(0.2, 0, 0, 1)` — quick start, soft land. For most toggles and taps.
- **Spring**: acceptable for mobile-native feel (draggable elements). Use carefully — bounce can look childish.
- **Linear**: almost never. Feels mechanical.

## What earns a micro-interaction

| Earns it | Doesn't |
|---|---|
| State changed (on→off, liked→unliked) | Data loaded (use skeleton, not animation) |
| Item added/removed from list | Passive content appearing |
| Drag threshold crossed | Hover on non-interactive element |
| User achieved something (completed task) | Every page transition |

## prefers-reduced-motion

Every micro-interaction must degrade to instant state change under `prefers-reduced-motion: reduce`. No exceptions.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Micro-interaction > 500ms | Blocks next action |
| Bouncing on every tap | Childish, exhausting |
| Animation on passive content | Unnecessary distraction |
| No reduced-motion fallback | Accessibility fail |
| Micro-interaction obscures the result | User unsure what happened |

## Audit checklist

- [ ] Duration ≤ 300ms for direct-feedback interactions
- [ ] prefers-reduced-motion degrades to instant
- [ ] Animation acknowledges the action, doesn't delay it
- [ ] Result is clear even without the animation
- [ ] No decorative animations on passive elements

## Sources

- Dan Saffer · Microinteractions (book)
- Material Design 3 · Motion (micro-interactions)
- `canon-motion` for duration and easing tokens
