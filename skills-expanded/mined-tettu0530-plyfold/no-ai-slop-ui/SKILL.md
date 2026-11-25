---
name: no-ai-slop-ui
description: Always use when building, fixing or reviewing Plyfold UI (screen prototypes, React components, CSS, copy, animation). Prevents the mass-produced look AI tends to generate (gradient washes, emoji icons, pointless cards, fake numbers, everything centered, excessive rounding and shadows) and keeps the work aligned with the shadcn/ui tokens and Plyfold's motion rules. Before showing any UI code or visuals, self-check against the checklist at the end.
---

# UI rules against AI slop

Plyfold is a tool for watching coding agents over long stretches. It puts "see the state at a glance" and "doesn't tire you out" ahead of looking impressive.
Do not ship anything that breaks the rules below unless you can explain why.

## 1. Color

- Use only the shadcn/ui dark theme (neutral) tokens as the base. Never hard-code raw hex values (in prototypes, add the token name in a comment)

  | Token | Value | Use |
  |---|---|---|
  | background | `#0a0a0a` | Window background |
  | card / sidebar / popover | `#171717` | Surfaces |
  | muted / accent / secondary | `#262626` | Emphasized surfaces, hover |
  | border | `rgba(255,255,255,.10)` | Borders |
  | input | `rgba(255,255,255,.15)` | Input outlines |
  | foreground | `#fafafa` | Body text |
  | muted-foreground | `#a1a1a1` | Secondary text |
  | primary | `#e5e5e5` (text `#171717`) | Primary button |

- **Color must carry meaning**. Color is allowed only for "state" and "diff"
  - Working = emerald `#34d399`, waiting for permission = amber `#fbbf24`, stalled = orange `#fb923c`, error = red `#f87171`, idle / stopped = neutral
  - Added = emerald tones, removed = red tones
  - One exception: a slash command recognised in the composer is blue (`text-command`, `--command: #60a5fa`), so a line that runs a command reads differently from a message. Nothing else uses it
- Never convey state by color alone. Always add a **per-state icon** and text
  - Working = the twelve-bar spinner (`Spinner` in `components/icons.tsx`: short bars around a circle that fade in turn), waiting for permission = shield, stalled = hourglass, error = circle with ×, idle = circle, stopped = square
- Don't invent new brand colors. At most one accent color

## 2. Banned (typical AI slop)

- Purple-to-blue gradients, gradient background washes, glowing outlines (glow), neon
- Emoji icons (✨🚀💡 etc.). Icons are lucide line icons only, 16px, stroke width 2
- Decorative cards with no purpose, cards with only a colored left edge, cards inside cards
- Making everything glass (frosted glass). Glass is only for "floating layers" (popovers, dialogs, permission requests)
- Fake numbers, invented track records, lorem ipsum. Write `—` or "Not available" for unknown values
- Centering everything. App screens are left-aligned by default
- Pill shapes from `rounded-full` everywhere. Corner radii follow the tokens (buttons 8px, cards 10px, inputs up to 12px)
- Stacked large shadows. Shadows only on dialogs and popovers
- Overuse of headings or bold, exclamation marks, hype copy like "Let's get started!"
- Overly generic copy ("Welcome to your dashboard", "Get started"). Say concretely what the user can do

## 3. Type and layout

- Fonts: Geist (body), Geist Mono (numbers, paths, commands, token counts). Leave CJK text to the system CJK font (`--font-cjk`: Hiragino for Japanese, PingFang SC for Chinese)
- Only four type sizes: 12 / 13 / 14 / 16 px. Body 13px, secondary 12px
- Numbers are tabular (`font-variant-numeric: tabular-nums` or Geist Mono). Digits must not jitter
- Spacing in multiples of 4 (4, 8, 12, 16, 24)
- **Keep information density low**. Always show only what the current decision needs; move the rest to hover, expansion or another screen (progressive disclosure).
  If you are tempted to put four or more pieces of information in one row or bar, first decide what can be hidden (users have flagged the UI as too dense)
- At most one primary button per screen

## 4. Motion (reproducing Apple's motion)

Prioritize **moving the way Apple's UI moves** over the glass look. The implementation is `apps/desktop/src/components/motion.ts`.

- Springs use the same formula as SwiftUI (duration + bounce → stiffness = (2π/d)², damping = 4π(1−b)/d). Don't make up your own values; pick one of these
  - `smooth` (0.35 s, bounce 0): moving screens and panes, appearing and disappearing, fades
  - `snappy` (0.35 s, bounce 0.3): toggle indicators, switches, rotating chevrons
  - `bouncy` (0.35 s, bounce 0.3): small attention-grabbing things (the permission-request droplet, notifications)
  - The standard is duration 0.35 s, bounce 0.3 (a deliberate choice; SwiftUI's default 0.5 s felt slow)
  - `interactive` (0.15 s, bounce 0.14): while tracking the pointer
  - For CSS transitions, use `var(--ease-snappy)` and `var(--dur-snappy)` (a linear() curve solved from the spring)
- **Interruptible**. If the next action arrives mid-animation, don't stop; carry over the current velocity and retarget
- **Carry the gesture's momentum**. Predict the resting point after release with `project()` (deceleration rate 0.998/ms) and hand the velocity to the spring as its initial velocity. Past the edges, use `rubberBand()`
- Stretch and squash **only while the user is interacting** (`press` swells slightly when pressed, dragging stretches along the drag direction). Don't routinely squash-and-wobble on landing
- Fusion and separation apply the SVG goo filter to **background shapes only**. Never to text. At most one or two places per screen
- **Separation animation** (the standard; always use it when another surface opens or closes): `components/liquid/stage.tsx`
  - Put `ref={liquidAnchor("name")}` on the origin and open with `liquidOpen(id, { anchor, target })`. Close with `liquidClose(id)` (the id that was opened) or `liquidCloseFrom(id, { anchor, target })` (the surface currently shown). Hide the surface's contents until `useLiquidRevealed(id)` is true
  - Motion: it emerges from **behind the origin only** (the origin is the button or row; the body is drawn at z-index 55, above the sidebar background, and only the origin is raised to 57; don't hide it behind the whole sidebar) → position uses snappy, size expands 0.12 s later with 0.42 s / bounce 0.3 (between a one-stage and a two-stage expansion) → color, border, shadow and blur fade from the origin's look to the destination's look as it expands → the corner radius jumps to the in-flight radius (16px) at the start, holds it, and changes to the destination's radius **only in the last 25%** (never fly as a sharp rectangle) → while slipping past an edge it stretches sideways with speed (up to 1.18×) → once fully expanded, show the real surface. Closing is the reverse: it shrinks back behind the origin
  - The origin pops slightly when pressed and keeps its selected color while the surface is open (so you can see where it came from)
  - Full-window screens (settings, profiles) use `cover: true`: the origin is raised only for the first 150ms of opening and after 300ms of closing (don't leave the button on top of the expanded body)
  - Contents of full-window screens don't wait for full expansion: clip them to the body's shape with `useLiquidClip(id, ref)` and fade them in while the area grows from 30% to 80% (reverse on close), so they don't pop in
  - **Liquid fusion** (built the same way as Liquid Glass; `components/liquid/sdf.ts` and the GPU renderer `liquid-gl.ts`): draw the origin and the body as one shape using a smooth minimum of their distance fields (iq's quadratic smin)
    - When the gap is at most k/2 they join (a neck); at most k, their edges lean toward each other. k is origin thickness × 1.2 + 16 (40 to 72px). The bulge is at most k/4
    - Fill, border and shadow blend the origin's look and the body's look by the smin mix factor (no visible seam). Don't fill inside the origin (never paint over the real button)
    - The position spring starts soft (stiffness ramps from 18% to full over 0.16 s): it peels away slowly while joined and speeds up once separated
    - While the neck exists, hold the body back slightly (60% of the gap, capped at k × 0.8); when the neck breaks, release it with a spring (0.45 s / bounce 0.4). At the moment it breaks, tug the origin slightly and let it spring back
    - Shrink k to 0 while the expansion goes from 45% to 90% (even when the destination sits right next to the origin, they always end as separate shapes). Closing is the reverse: widen k as it comes back (it gets sucked in)
    - Don't fuse while the shapes overlap: smin inflates perfectly overlapping shapes by k/4 (producing a blob larger than the origin at the start and end). Multiply k by the center separation (0 → 1 over one origin thickness)
    - While moving, the liquid body is the only "body": hide the real surface's (menu or full-window screen) background, border and shadow, and show only its contents clipped to the body's shape. With two bodies, spring overshoot misaligns their sizes and a gap shows
    - Stop Radix's default fade and zoom with an inline `animation: none` (a class can't override it; tailwind-merge treats animate-in and animate-none as different and keeps both)
    - Don't hand-draw neck or tail shapes (earlier attempts didn't look like Liquid Glass)
    - How to verify: `tools/liquid-probe/sdf-film.mjs` (the formula only) and `app-frames.sh` (captures the real app frame by frame at 1/60 s)
  - Measure small menus after their position settles (Radix positions them right after they appear). Turn off Radix's default fade and zoom (so nothing animates twice). Menus open above the input (popper / side=top)
  - Small menus (model / effort pickers, the context breakdown, etc.) use the same motion: `useLiquidMenu(id, anchor)`. They burst out of the chip and expand; on close they shrink from their last size back into the chip. Contents fade in as it expands
  - Menu stacking order (`rise`; `useLiquidMenu` always uses it): the body emerges from behind the origin only at the start, and partway through opening (openness 0.2 to 0.5) it moves on top of the origin. When a menu opens overlapping its origin, like a context menu, it must not stay buried under the row. The switch is not instant: the GPU renderer gradually layers the body-only shape (shadow, fill, border) over the origin (`over`). Once layering starts, drop the origin from z-[57] (it leaves `useLiquidActiveAnchors`). Keep its selected color via `useLiquidMovingAnchors`. Content fade uses the smaller of area ratio and openness (with a large origin, the area is already sufficient from the start)
  - After opening, the body stays as the menu's frame (`hold`). Don't show the real background, border or shadow until it closes; show only the contents clipped to the body's shape. Swapping to the real frame makes the body look larger at the moment of the swap by the spring's overshoot (especially the top edge). If the destination's size changes, the body follows
  - Full-window screens (cover) also paint the body over the origin once the origin has been lowered (if the "don't fill inside the origin" rule still applied, the expanded body would have a hole and the button would show through)
  - Values that cycle in order, like mode, change with a split-flap: `<SplitFlap>`. The old top half falls (0.16 s), and the new bottom half drops on a spring (0.4 s / bounce 0.35) with a small bounce. While flipping, paint each half with the background color (if it's transparent, the text overlaps)
  - Swapping (replacing a pane's session with another session): the original session starts returning to its row first, and the new session bursts out 140ms later
  - Where it is used: search (⌘K), opening and closing sessions (sidebar row ↔ pane), new session (button → empty pane)
  - When creating a new surface, first consider whether it can open inside an existing screen rather than as a modal (a new session is an empty pane, not a modal)
- Animate only meaningful changes. Decorative looping animations are banned (except the spinner for "working")
- Don't animate when macOS "Reduce motion" is on (Motion's `reducedMotion="user"`; in CSS, a 150ms fade)
- Animate only transform and opacity. Don't animate width / height / top / left directly
  - **Exception: when a region containing text changes size** (e.g. splitting panes), don't use Motion's `layout` (it scales, so the contents stretch). Spring the actual width and height and re-lay out the contents every frame (like Apple's Split View). For rows that only change position when reordered, use `layout="position"`
- When changing values, compare side by side with Finder and System Settings using the app's Motion lab (Settings → Motion, development builds only)

## 5. Choosing components

1. If shadcn/ui (Tailwind v4, Radix flavor) has it, use that
2. For agent-specific components shadcn lacks, use **only the free (MIT) components** from AffectUI (Tool Call Card, Code Block, etc.). Pro components can't go into an OSS project, so don't use them. Build permission requests, the input box and usage displays ourselves
3. Anything still missing, build ourselves and match the shadcn tokens
4. Components from showcase collections (Pin UI, Ruixen, etc.) only when the license is clear and they can be rebuilt to fit the tokens

## 6. UI copy

The app ships English, Japanese and Simplified Chinese UIs.

- **Never write UI strings directly in components**. Add them to the Japanese dictionary (`src/i18n/ja/<namespace>.ts`), write the English (`src/i18n/en/`) and Chinese (`src/i18n/zh/`) versions at the same time, and look them up with `t()`. Rules, glossaries and the English and Chinese style guides are in `docs/i18n.md`. Engine (Rust) strings use `plyfold_i18n::tr!("<Japanese>", "<English>", "<Chinese>")`

All languages:

- Errors say "what happened" and "what you can do next"
- **Don't join words with separator dots** such as "·" ("claude · work" becomes the logo + "work"). When listing items, keep them as separate elements separated by spacing
- Number rows (tok/s, input and output tokens, cost, time) get an icon each, with tight spacing
- No self-evident explanations (e.g. don't write "Diffs are generated from git" on the diff screen)
- Action buttons get an icon (lucide, 14 to 16px). Show providers by logo, not text (Simple Icons, CC0; when none exists, use a generic icon rather than drawing a fake)
- **If an icon can express it, use an icon**. For key combinations use `Keys` (`components/Keys.tsx`, which draws ⌘ ⇧ ⌥ ⇥ ⏎ and arrows as icons in key-shaped frames); never write text like "⌘K" directly

English:

- Short and concrete. Sentence case everywhere, including headings and buttons ("New session", not "New Session")
- Buttons are short imperative verbs without a period ("Stop", "Merge", "Discard"). No exclamation marks, no "Please …"

Japanese (the `ja` dictionary):

- Short and concrete; the polite 「です・ます」 form only in explanatory text, never on buttons. Buttons end with a verb or a short verbal noun (「許可」「停止」「取り込む」)
- Avoid mixing in too much English and katakana. But model / effort / mode, ACP terms and commands stay as they are
- **Don't join words with 「・」 or 「 · 」**
- Prefer short, established terms over descriptive phrasing: use 「初期プロンプト」「ベース URL」「置換」「テスト」「停止」「カスタムプロバイダー」「通知」, not 「最初の指示」「接続先 URL」「置き換える」「確かめる」「止める」「独自の接続先」「知らせ」

Chinese (the `zh` dictionary):

- Simplified Chinese for mainland China (zh-CN). Short, plain terms common in software UIs; buttons are mostly 2 to 4 character verbs (「停止」「合并」「放弃」)
- Put a half-width space between Chinese and Latin letters or digits (「打开 worktree」「3 个文件」)

## 7. Accessibility

- Body text contrast at least 4.5:1 (`#a1a1a1` on `#171717` is about 6.9:1, which is fine. Never use `#737373` for text)
- Anything clickable is a `<button>` or `<a>`. Icon-only buttons get an `aria-label`
- Everything must be operable by keyboard. Never remove the focus ring

## Checklist before shipping

- [ ] Is color used only for state and diff? No gradients, glow or emoji?
- [ ] Are tokens used instead of raw color and size values?
- [ ] No fake numbers, lorem ipsum or generic hype copy?
- [ ] One primary button at most? No overuse of centering or pill shapes?
- [ ] Is the always-visible information kept minimal, with details moved to hover, expansion or another screen?
- [ ] Are numbers tabular?
- [ ] Are springs chosen from smooth / snappy / bouncy / interactive? Interruptible? Carrying momentum? Liquid effects in only one or two places and never on text? Is there a reduced-motion fallback?
- [ ] No Pro components?
- [ ] Are contrast and keyboard operation OK?
