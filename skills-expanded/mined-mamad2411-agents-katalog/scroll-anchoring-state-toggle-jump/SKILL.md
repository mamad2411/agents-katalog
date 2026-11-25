---
name: scroll-anchoring-state-toggle-jump
description: |
  Fix for scroll position "jumping" hundreds of px on a slight trackpad drag when a
  scroll event handler toggles UI state (compact mode, collapsing headers) based on
  scrollTop thresholds. Use when: (1) a slight scroll causes an instant deep jump
  instead of smooth scrolling, (2) a scroll handler has both an "atTop → expand" and
  a "scrolled → collapse" branch, (3) two components both own the same expand/collapse
  state (event-driven + scroll-driven), (4) a wheel-based Playwright repro can't
  reproduce a user-reported jump. Root cause: expanding/collapsing content ABOVE the
  scroll position triggers browser scroll anchoring, which shoves scrollTop past the
  collapse threshold; the next scroll event re-collapses, leaving the view stranded deep.
author: Claude Code
version: 1.0.0
date: 2026-07-16
---

# Scroll jump from scroll-position-driven state toggles (scroll anchoring thrash)

## Problem
A slight scroll gesture instantly jumps the scroll container hundreds of px deep
instead of scrolling smoothly.

## Context / Trigger Conditions
- A `scroll` listener toggles state: `atTop (scrollTop <= N) → expand chrome` and
  `scrollTop > M → collapse chrome`, where the chrome lives ABOVE the scrolled content.
- The same state is ALSO set by another owner (e.g. a parent layout dispatching an
  event when it pins/expands the container). If the other owner set "collapsed" while
  scrollTop is still ~0, the first tiny scroll delta lands in the atTop window.
- Real trackpad gestures always begin with 1–5px deltas, so users hit the atTop
  window reliably.

## Mechanism (juicy-vision WelcomeLayout dock, ChatContainer.tsx)
1. Dock pinned → `juice:dock-scroll` event sets `dockScrollEnabled=true` (compact,
   ~180px of greeting/controls collapsed). scrollTop = 0.
2. Next gesture, first wheel delta of 2px → scroll handler sees `atTop` →
   `setDockScrollEnabled(false)` → chrome expands, scrollHeight 747→924.
3. Browser scroll anchoring compensates for content inserted above the viewport:
   scrollTop jumps 2→179 in one frame.
4. Next scroll event: `scrollingDown && scrollTop > 50` → re-collapse → scrollHeight
   back to 747, scrollTop stays ~160. View is stranded ~160px deep = perceived jump.

## Solution
Give the state exactly one owner per mode. In juicy-vision: the scroll-driven toggle
effect returns early in `bottomOnly` mode (`if (bottomOnly) return`), because
WelcomeLayout owns compact state via the pin/unpin events there. The scroll-driven
path remains for mobile, where it is the only owner.

General fixes, pick one:
- Guard the scroll-driven toggle out of contexts where another owner sets the state.
- Or make thresholds hysteretic AND anchored: only expand at top on an intentional
  upward gesture (deltaY < 0), never on a downward one.
- `overflow-anchor: none` on the container ALSO stops the anchoring shove, but leaves
  the expand/collapse flicker; prefer fixing ownership.

## Verification / Repro technique
Synthetic wheel repros MUST start with tiny deltas — a realistic trackpad ramp like
`[2, 3, 5, 8, 15, 30, 40, 30, 15, 5, 3, 2]` at ~12ms spacing. Constant 15px ticks skip
the `<= 10px` atTop window and mask the bug entirely. Instrument with a rAF sampler
recording `{scrollTop, scrollHeight}` each frame; the bug shows as a single-frame
scrollTop discontinuity paired with a scrollHeight spike.

## Notes
- Seeding welcome-screen chats for repro: localStorage `juice-chat` gets wiped by the
  server sync (`fetchMyChats` → `setChats`); instead intercept `GET */chat?*` with
  `page.route` and return `{ success: true, data: [...chats], total }`.
