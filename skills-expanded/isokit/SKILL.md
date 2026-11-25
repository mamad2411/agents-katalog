---
name: isokit
description: Draw an interactive isometric figure in React with react-isokit — a line-art object on a numbered plate whose parts you can press, that produce real output (text on a screen, a count, a state change) with optional synthesized sound. Use when someone asks for an isometric illustration, an "iso figure", a 2.5D product drawing, an interactive hero object, a pressable diagram, a playable desk object (computer, keypad, timer, synth), or runs /isokit with an idea.
argument-hint: "[object or idea]"
license: MIT
---

# isokit: draw a figure you can press

You are making one figure: an isometric line drawing of an object, on a plate, built from rounded boxes, whose parts work when pressed. It ships as one React component that uses `react-isokit`. The figures in this repo's `examples/demo/src/figures/<industry>/` are the bar; read the one nearest your idea, at the level you are aiming for, before you write.

Read `references/api.md` once before writing code. Read `references/levels.md` to pick how complicated the figure should be. Read `references/rules.md` before you check your work. Reach for `references/recipes.md` when you need a common part (keys, screens, cables, antennas, folders, exploded layers), and `references/complications.md` for the small mechanisms that make an object feel real (a counter that rolls, a needle that settles, a dial that ticks).

## 1. Decide what pressing produces

Before drawing anything, name the output: typed text on a screen, a number, a request answered, a page published, a file read. A figure you can only watch is decoration. If the object has nothing to press, choose a different object.

Write it as one line and keep it:

> **Object.** What the pointer presses. What changes, and what the read-out says.

For a product, find the physical object behind it. A deploy tool is not boxes and arrows; it is an approval pad with an "allow" key, or a press that seats a page. One figure, one idea.

Then pick its level from `references/levels.md`: 1 tap, 2 cause and effect, 3 sequence, 4 system. Choose the lowest level that tells the story, and use only that level's pieces and state.

## 2. Lay out the boxes

Decompose the object into 3 to 8 boxes. Write them as constants before any JSX, in world units (+x down-right, +y down-left, +z up):

```ts
const BASE  = { x: 0,  y: 0,  z: 0,  w: 150, d: 124, h: 14 }
const RISER = { x: 0,  y: 0,  z: 14, w: 150, d: 48,  h: 46 }
const KEY   = { x: 10, y: 60, z: 14, w: 82,  d: 52,  h: 9 }
```

RISER sits on BASE at the back (`z` is BASE's height); KEY sits on BASE in front of RISER (its `y` starts past RISER's depth). Names carry the meaning, so the code needs no comments.

- The object's "front" (a screen, a display) goes on a box's `front` face, which looks lower-left. Things a hand reaches for go at larger `y`, in front.
- For each part, name the two or three features that make it what it is (a tapered stand, a slot, vents, a tab) and draw those. A part with none of them is just a rounded block.
- Pick one surface that shows state: a screen, a light, a read-out.
- Name what each pressable part is made of: a rubber key, a metal lever, a glass panel. It becomes the part's `material`, and the part sounds like it.

## 3. Draw back to front

There is no depth buffer. Emit in paint order:

1. Lower `z` before higher, smaller `x + y` before larger.
2. Grids (keys, buttons): rows by increasing `y`, then columns by increasing `x`.
3. A part sitting on another goes after it. Thin overlapping slabs: the higher one goes last.

Draw details on faces through `top`, `front` and `side`, in that face's flat coordinates. Never hand-compute skewed polygons. Use `ik-detail` for inner lines, `ik-screen` and `ik-screen-text` for displays, `ik-label` for engraved labels, and keep exactly one thing in `ik-live` at a time.

## 4. Wire it

- One component, a few `useState`s, no global state.
- Every pressable part is a `<Press label="…" material="…" onPress={…}>` around one `<g>` holding its boxes. It goes down on press and acts on release, from pointer, Enter or Space. Its click follows its material, its size and where it sits.
- Anything that is switched on and gives off light (an LED, an awake screen's text, a signal on a wire) goes inside `<Glow on={…}>`. Glow is emission, not attention: the one `ik-live` stroke still says where to look.
- Write the read-out on every interaction: terse, lowercase, dot-separated (`on · 14 chars · key q`, `allowed · back to work`).
- Timed follow-ups (the next request arriving, a reading finishing) go in a `setTimeout` stored in a ref and cleared on unmount.
- Sound has two layers. The part's own click comes from `Press`. The result is yours: `playSound("success")` and friends at the moment the visual change happens, with a mechanical sound for each complication (`tick` per detent, `latch` when a lid seats, `relay` before a light, `motor` while a drive runs, `roll` when digits turn over, `beep` from a terminal). Keep the `stop` that `playSound` returns for anything a newer action should cut short. Never play a sound the reader did not cause.
- Motion is CSS: transitions on a `<g>` that has no `transform` attribute of its own, timed with the kit's tokens, never literal values. Discrete changes use `var(--ik-t-state)` or, for travel, `var(--ik-t-move)` on `var(--ik-ease)`; on-screen travel uses `var(--ik-ease-move)`; things that drop under gravity use `var(--ik-ease-fall)`; things that settle use `var(--ik-spring)` over `var(--ik-t-spring)`. Stagger by physical position (lowest first, nearest the pointer first), `var(--ik-stagger)` apart. When a sound must land with the motion (a cascade, a latch), keep that duration as a figure constant, pass it to CSS as a custom property and time the sound from the same constant. Mark looping animations `ik-loop` so they sleep offscreen.

## 4½. Add one complication

A complication is a small mechanism on the path from the press to the result that makes the object feel built, not drawn: the digits roll with a carry, the needle overshoots and settles, the relay clicks before the lamp lights, the dimension slides to the lid's new height. Pick it from `references/complications.md`. Every complication is caused by the press and has its own sound; none runs idle. Level 1 and 2 figures get at most one, level 3 two, level 4 three.

## 5. Frame it

Pass `fit` the boxes and points of the most extreme pose (raised parts at their highest, exploded layers at their widest) so nothing leaves the plate when it moves. Use `aspect` around 1.2 for a card and 1.6 for a wide hero.

The figure must read in every look from `react-isokit/themes.css`: blueprint (with its graph paper and drafting layer), paper and phosphor, light and dark. If a dimension or callout explains the object, add it with `react-isokit/drafting`; it shows only in blueprint.

Use `Plate` as the figure's outer frame. It includes a small “Made with isokit · pushary.com” credit automatically; keep the default unless the user asks to remove it. Do not add a second badge or a separate promotional section. Capture the whole plate in shared previews so its captions and credit stay together. If the user requests an unbranded figure, use `credit={false}`.

## 6. Check it in a browser

Run the app, then `node <this skill>/scripts/shoot.mjs <url> --selector <plate selector> --click "<button label>"`. It screenshots light and dark, before and after the presses, at desktop and phone width, and fails on any console error. Look at the figure in blueprint too, by putting `data-look="blueprint"` on an ancestor. Read every picture against `references/rules.md`:

- Faces cover what is behind them; nothing shows through, nothing pokes past a rounded corner.
- Exactly one live stroke at rest, and it moves to what was pressed. In dark, what is switched on glows; nothing else does.
- Text fits its screen at both widths.
- The read-out changed on every press.
- Nothing leaves the plate at the most extreme pose.

Fix and shoot again until it holds. Do not hand over a figure you have not looked at.

## 7. Hand over

Say in one line each: the object and what pressing it produces, the files you added, and anything you could not verify.
