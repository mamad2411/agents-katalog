---
name: ux-mobile
description: "Apply medium-specific UX reasoning for MOBILE (phone) applications: touch input, small screen, one-handed use, single-surface focus. Use alongside ux-first-principles when the target is a phone app (iOS or Android) and the decision is affected by touch target sizing, the absence of hover, thumb reach, limited screen real estate, or single-task focus. USE FOR: 'design a mobile screen', 'lay out this phone app', 'what should the mobile navigation be', touch target sizing, thumb-reach layout, single-task handheld flows. DO NOT USE FOR: the invariant principles (use ux-first-principles); desktop or tablet layouts (use ux-desktop or ux-tablet); picking colors, fonts, or platform chrome (use a styling/execution skill)."
---

# UX for Mobile (Phone)

A thin medium layer. The reasoning lives in `ux-first-principles`; read it first or alongside. Here is only what the phone *medium* changes — driven by the body-to-device interface, not by which OS it is.

## What defines the mobile medium
A coarse touch input (fingertip, not a point), a small screen held at arm's length, frequent one-handed and on-the-move use, and a single app in focus filling the screen. These change six things — and several are the mirror image of desktop.

## The six things that change

1. **Target sizing is a floor, not a budget.** A fingertip is roughly 10–14mm wide and *occludes* the thing it taps. Interactive targets must be large and well-spaced or users mis-tap. Treat a generous minimum tap target as a hard floor and add spacing between adjacent targets to prevent errors. You cannot use the dense, tiny controls that work on desktop. (The exact minimum is a platform metric — see handoff.)

2. **There is no hover.** The finger is either off the glass or committing to a tap; there is no idle-pointer state. Anything desktop would put behind hover — tooltips, reveal-on-hover controls, hover previews — **must not** carry essential information or actions on mobile. Surface it persistently, or behind an explicit tap/long-press with a visible signifier. This is the most common porting bug from desktop UI.

3. **Screen real estate is scarce — density must drop.** The same content that reads as efficient on desktop reads as cramped and overwhelming on a phone. Reduce per-screen density, shorten navigation depth, and accept more screens / more scrolling rather than packing one. Lead with the single primary task; defer the rest (progressive disclosure is heavily used here).

4. **Reach and thumb zones matter.** Held one-handed, the thumb comfortably reaches the bottom-center of the screen; the top corners are a stretch. Put primary, frequent actions in the easy bottom zone; put rare or destructive actions where they're harder to hit by accident. This consideration has no desktop analog — the cursor reaches every pixel equally.

5. **Single-surface, single-task focus.** One app, fullscreen, one task at a time. Design a focused linear flow rather than the multi-panel, multi-window layouts desktop affords. Carry context forward between screens so users don't have to remember it (Miller's Law, recognition over recall — recall is costlier on mobile because there's no room to keep things visible).

6. **Gestures replace precision and right-click.** There is no right-click and no fine pointer. Swipe, long-press, pinch, and pull are the equivalents — but they're invisible unless signified. Provide a visible button path for anything important; never make a hidden gesture the only way to reach an action.

## How principles shift on mobile
- **Fitts's Law:** target size is now a usability floor; distance matters less than reachability (thumb zones).
- **Hick's Law:** show fewer choices per screen than desktop — small screens make long option sets punishing.
- **Progressive disclosure:** your main tool, used aggressively; lead with the common case, defer everything else to taps and subsequent screens.
- **Aesthetic-Usability / Peak-End:** mobile moments are short and frequent; smooth, fast, focused flows matter more than feature breadth.

## Render-time platform handoff (NOT design decisions)
Mechanical per-platform substitutions, handled in styling / at render time (e.g., by .NET MAUI), not reasoned from principles:
- Exact minimum tap-target metric, system fonts, control styling, corner radii, and material/elevation conventions.
- Platform navigation chrome styling and the standard system affordances.
- OS-global gestures: respect the platform's system back / home / edge gestures rather than fighting or overriding them.

**Everything else — including structural choices like tab bar vs. navigation drawer, bottom-sheet vs. full screen, and flow depth — is a design decision. Reason it from first principles (information architecture, Hick, hierarchy) and commit to ONE answer; both tabs and drawers are acceptable on either OS, so don't fork the structure per platform.**

## Deliberate scope note
This optimizes for a coherent cross-platform product over maximal single-OS idiomaticity, which is the right trade-off for cross-platform work. It would only bite an app whose whole value proposition is feeling 100% hand-built-native on one OS.
