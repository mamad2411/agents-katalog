---
name: card-motion
description: 'Use when a card should animate: elements entering and leaving, a list or grid rearranging, a tile opening into a detail view, drag and reorder, scroll-linked effects, or several elements moving in a sequenced scene. Covers which of glimmer-motion''s patterns to reach for ({{motion}}, <Presence>, layout / layoutId, drag and <ReorderGroup>, scrollProgress / InView) and when to escalate to a <Choreo> timeline, the imports a realm can resolve (motion-dom only through glimmer-motion), the four Glimmer rules that silently stop motion, and the card-specific rules that follow from cards sharing the host''s copy of both libraries. Activates on glimmer-motion, @cardstack/choreo, {{motion}}, Presence, layoutId, Choreo, "animate", "transition", "enter/exit animation", "reorder", "parallax", "magic move".'
boxel:
  kind: skill
---

# Animating a card

_glimmer-motion animates elements; Choreo sequences a whole render pass. Both come from the host — nothing to install._

```gts
import { CardDef, Component } from '@cardstack/base/card-api';
import { motion, spring, to } from 'glimmer-motion';

const soft = spring({ visualDuration: 0.4, bounce: 0.2 });

export class Notice extends CardDef {
  static isolated = class Isolated extends Component<typeof this> {
    <template>
      <article
        {{motion
          initial=(to opacity=0 y=12)
          animate=(to opacity=1 y=0)
          transition=soft
        }}
      >
        <@fields.cardTitle />
      </article>
    </template>
  };
}
```

## What a realm can import

The host hands cards its own copies of both libraries through its module shims:

| Specifier | What it is |
| --- | --- |
| `glimmer-motion` | The `{{motion}}` modifier, `<Presence>`, `<LayoutGroup>`, `<MotionConfig>`, `<ReorderGroup>` / `<ReorderItem>`, the `to` / `spring` / `tween` / `stagger` / `styles` helpers, `scrollProgress`, `InView`, `viewTransition`, and the engine's imperative surface |
| `glimmer-motion/presence`, `/layout-group`, `/motion-config`, `/reorder/group`, `/reorder/item` | The same components by their own entry points |
| `@cardstack/choreo` | `<Choreo>`, `beacon`, `at` / `after`, `createArming`, and the `Sprite` / `Changeset` types |
| `@cardstack/choreo/film` | Film (scored, seekable sequences) |
| `glimmer-motion/test-support`, `@cardstack/choreo/test-support` | Test helpers for `.test.gts` files ([references/testing.md](references/testing.md)) |

**motion-dom is reached only through glimmer-motion.** `motion-dom`, `motion` and `framer-motion` do not resolve in a realm. glimmer-motion re-exports the imperative subset a card needs — `motionValue` (and the `MotionValue` type), `animate`, `transformValue`, `styleEffect`, `frame` — and those are the engine's own functions, sharing the frame loop `{{motion}}` runs on. Do not pull a second copy of Motion from an ESM CDN: it would run its own frame loop and know nothing about the host's layout animations.

## Pick the smallest pattern that states the intent

Escalation order: element → presence → layout → Choreo.

| The ask sounds like | Pattern | Read |
| --- | --- | --- |
| "fade/slide/scale this in", hover/tap states, keyframes, variants, stagger | `{{motion}}` with `initial` / `animate` / `transition` | [element.md](references/element.md) |
| "animate it when it's removed", list add/remove, a panel opening and closing | `<Presence>` + `exit` | [presence.md](references/presence.md) |
| "it moved because the layout changed", a filtered grid, a list that re-sorts, a tab indicator, a thumbnail opening into a detail view of the SAME thing | `layout=true` / `layoutId` inside a `<LayoutGroup>` | [layout.md](references/layout.md) |
| drag, swipe-to-dismiss, a reorderable list or grid | `drag` / `<ReorderGroup>` | [drag-and-reorder.md](references/drag-and-reorder.md) |
| parallax, a scroll progress bar, reveal-on-scroll | `scrollProgress` / `InView` / `whileInView` | [scroll.md](references/scroll.md) |
| "first X, THEN everyone moves, THEN Y"; z-index for the span of a move; one element's motion computed from another's box; flying to a place that must not deform; two views of the card swapping as one Magic Move | `<Choreo>` timeline (+ `{{beacon}}`) | [choreo.md](references/choreo.md) |
| a deliberate snapshot morph of part of the card | `viewTransition(update, element)` | [view-transitions.md](references/view-transitions.md) |

The classic wrong reaches:

- **A view transition for live content.** `startViewTransition` animates bitmaps, so anything running inside — a demo, a video, a canvas — freezes for the crossfade, and the document-wide form snapshots the host's whole page. `layout=true` moves the real elements.
- **`layoutId` to fly an item into a trash can.** `layoutId` morphs one element into another; the bin would stretch into a row. A destination that is a _place_ is a `{{beacon}}` and `<c.Move @to>`.
- **`setTimeout` to sequence animations.** That is what `<Choreo>`'s `c.Sequence` replaces: its "after" comes from real durations, including a spring's settle time.
- **`<Choreo>` for one element.** One element, no ordering, no cross-element measurement: `{{motion}}` (or `<Presence>` if it leaves).
- **A one-off CSS entrance is fine as CSS.** A single keyframed fade needs no library; follow the resting-state rule in `boxel-ui-guidelines/references/template-patterns.md` (the resting CSS state is the final one). Reach for glimmer-motion when the motion depends on state, interrupts, leaves the DOM, or follows layout.

## The four Glimmer rules (each silently stops motion)

1. **Motion owns the inline style.** Never put a bound `style="…"` attribute on a motion element: Glimmer rewrites the whole declaration on re-render and wipes the transform the engine just wrote. Pass styles through the modifier instead.
   ```gts
   {{! ✗ }} <div style={{this.accent}} {{motion drag=true}} />
   {{! ✓ }} <div {{motion style=(styles background=this.accent) drag=true}} />
   ```
   (Static styling belongs in `<style scoped>` as always; this is about values you bind.)
2. **Declare what should be tweened or corrected.** A stylesheet `border-radius` is invisible to the engine, so a layout-animating tile grows with oval corners. Pass radius and shadow through the modifier: `{{motion layout=true style=(styles borderRadius='14px')}}`.
3. **A leaving element stays live.** Glimmer re-runs a leaver's block from current tracked state while its exit plays, so whatever the exit shows must ride on the item `<Presence>` yields, not be re-read from state that has already moved on.
4. **`layout=true` and `layoutId` animate only inside a `<LayoutGroup>`.** The box a layout animation starts from has to be measured before Glimmer changes the DOM, and a `<LayoutGroup>` above the element measures it on every render. `<ReorderGroup>` and `<Choreo>` measure too, and so does `<Presence>`, but only on a render that adds, removes or reorders its own `@items`: an item that grows inside a Presence-only list still jumps. A list or grid of `layout=true` items that reorders, filters or sorts with no group above it jumps instead of gliding, and so does a `layoutId` hand-off: the outgoing element's box is known only if something measured it before it left. Put the `<LayoutGroup>` around the `{{#each}}` in the template that renders the list, so it animates wherever the card renders, and never inside a row or a row card's own template: Glimmer moves a row before it re-renders anything inside it, so a group there measures too late. Key each row by something that stays with it, never by its position: a linked card's `id`, or an id field a row is given when it is added. `key='@index'` keeps every element where it is and swaps its content, so nothing moves at all; a key built from a position changes when the rows before it shift, and a row whose key changes is a new element with no earlier box to animate from. `@identity` breaks the same way when the code replaces a row's object (`list[i] = new Item({ … })`).
   ```gts
   {{! ✗ re-sorts in a single frame: nothing measured the rows before they moved }}
   <ul>{{#each this.sorted key='id' as |item|}}<li {{motion layout=true}}>{{item.name}}</li>{{/each}}</ul>

   {{! ✓ }}
   <LayoutGroup>
     <ul>
       {{#each this.sorted key='id' as |item|}}
         <li {{motion layout=true}}>{{item.name}}</li>
       {{/each}}
     </ul>
   </LayoutGroup>
   ```

## Cards share the host's copy

Every card on the page and the host's own UI run on one instance of each library, so their module-global state is shared: the beacon registry, Choreo's region registry, far matching, the layout scheduler and the global motion speed. The same card can also render twice at once (in two stacks, or isolated in one and embedded in another). So:

- **Scope every name a card registers by the card's id.** Beacon names are document-wide and the first registration wins; a `<Choreo @id>` is looked up host-wide; an id that leaves one `<Choreo>` region and appears in another in the same render pass far-matches and flies between them; `layoutId`s pair across the page unless a `<LayoutGroup @id>` namespaces them. Build them with `concat` from `@ember/helper` (`(concat @model.id '-trash')`), or wrap a card's `layoutId`s in `<LayoutGroup @id={{@model.id}}>`. Leave `<Choreo @id>` off unless something addresses the region.
- **Do not change global tempo.** `setMotionSpeed` slows every animation in the host. A card that wants slow motion for a demo scales its own transitions.
- **Animate inside the card's own box.** The host owns the stack, the card container and the format chrome around your template. Put `<Choreo>` around the part of the card that is the scene — the list, the panel — never try to choreograph outside the template.
- **A card scrolls in its stack item, not the window.** Scroll-linked motion names its scroller explicitly ([scroll.md](references/scroll.md)).
- **Tracked state lives on a top-level component.** Motion is driven by tracked state, and `boxel parse` rejects decorators inside a `static isolated = class {…}` expression. Declare the view as its own class and assign it: `class InboxView extends Component<typeof Inbox> { @tracked open = false; … }`, then `static isolated = InboxView;`.
- **Reduced motion is respected by default.** `<MotionConfig @reducedMotion>` defaults to `"user"`: under `prefers-reduced-motion`, transform and layout animation are off while opacity and colour still animate. Don't override it to make a demo "work".
- **Fitted and embedded formats render many instances.** Keep per-instance motion cheap (opacity and transform) and let the card that owns a list choreograph it, not each item.

## References

- [references/element.md](references/element.md) — `{{motion}}`: targets, transitions, keyframes, variants, gestures, motion values.
- [references/presence.md](references/presence.md) — `<Presence>`: exits, modes, the single-conditional-element form.
- [references/layout.md](references/layout.md) — `layout`, `layoutId`, `<LayoutGroup>`.
- [references/drag-and-reorder.md](references/drag-and-reorder.md) — `drag`, drag controls, `<ReorderGroup>` / `<ReorderItem>`, touch rules.
- [references/scroll.md](references/scroll.md) — `scrollProgress`, `InView`, `whileInView`.
- [references/choreo.md](references/choreo.md) — `<Choreo>` scenes, steps and selectors, beacons, nested regions and far matching.
- [references/view-transitions.md](references/view-transitions.md) — `viewTransition` scoped to the card, and when not to.
- [references/testing.md](references/testing.md) — testing animated cards under `boxel test`.
