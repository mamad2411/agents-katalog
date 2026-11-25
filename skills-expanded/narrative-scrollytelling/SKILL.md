---
name: narrative-scrollytelling
description: Turn an ordered sequence of ideas into a readable scroll-based story with canonical document order, deliberate step or progress transitions, native scrolling, and static, reduced-motion, keyboard, touch, and no-JavaScript fallbacks. Use when a method, argument, timeline, process, or visual explanation should unfold as the reader scrolls rather than behave like a slide deck. Triggers on scrollytelling, scroll story, narrative scroll, sticky story, scroll-driven narrative, scroll animation, step story, chapter reveal, pinned visual, interactive article.
handoffs:
  - to: semantic-micro-interactions
    when: the story contains a bounded control or committed state transition that needs local feedback behavior
  - to: walkthrough
    when: the scroll story is operable and its reading, navigation, fallback, and embedded task paths need verification
---

# Narrative Scrollytelling

**Announce at start:** "I'm using the humane:narrative-scrollytelling skill to turn this sequence into a scroll story that remains a readable document."

Scrollytelling is a document before it is choreography. The ordered ideas,
headings, prose and media alternatives form a complete canonical reading order;
scroll position may change their presentation, never their existence or meaning.

## Quick reference

| Need | Read |
| --- | --- |
| Story shapes, drivers, sticky stages and pacing | `references/patterns.md` |
| The story-map fields and fallback invariants | `references/contract.md` |

## Build the story map

1. Establish the ordered beats outside the visual treatment. Each beat carries
   one claim or change in understanding and a stable id.
2. Choose the least demanding driver that expresses the relationship:
   `discrete-intersection` for prose steps, `view-progress` for a visual whose
   change follows its visibility, and `scroll-progress` only when intermediate
   states themselves communicate meaning.
3. Decide what remains in normal document flow and what may be sticky. A sticky
   visual stage is normally non-focusable; interactive content stays in logical
   source order.
4. Specify navigation and fallbacks before transition polish: anchors,
   previous/next where useful, skip-story, no-JavaScript, reduced-motion,
   no-motion and unsupported-driver behavior.
5. Only then name transition intents and token references.

Write the result using `references/contract.md`. When the user wants a saved
artifact, resolve `artifact_path(name, "narrative-scrollytelling", "json")`;
never assemble a `.design` path at the call site. Validate a saved map with
`python3 scripts/validate_map.py <map.json>`.

## Hard boundaries

- `steps[]` order is canonical DOM and reading order. Every essential fact is
  present as semantic content outside canvas frames, keyframes and transition
  labels.
- Native page scrolling remains in control. Do not hijack wheel/touch input,
  lock the reader into a scene, require scroll speed/direction, or turn the
  document into an inaccessible slide deck.
- Scrolling does not move focus or announce every step. Sticky authored content
  cannot obscure focused controls; reserve safe offsets and scroll padding.
- Default snap is `none`; `proximity` is optional. `mandatory` requires an
  explicit audited exception proving all content remains reachable at zoom,
  reflow, large text and short viewports.
- Reduced motion removes parallax, scrubbed spatial travel, smooth scrolling
  and long pinning. The fallback uses discrete static states or the linear
  document; meaning never depends on an exact progress fraction.
- No-JavaScript and unsupported-feature modes expose the whole story. Native
  CSS scroll timelines are progressive enhancement, not a prerequisite.
- Continuous automatically started movement is absent by default. If an
  essential presentation exceeds five seconds alongside other content, provide
  pause, stop or hide controls and name the reason.

## Embedded interactions and sound

This skill owns chapter activation and presentation, not feedback for buttons,
toggles, maps or other controls inside a chapter. Hand those bounded transitions
to `humane:semantic-micro-interactions`.

Passive scroll crossings do not play sound. If the experience has opted into
audio, explicit chapter navigation or a genuinely committed milestone may emit
a semantic `soundEvent` through its micro-interaction map; `sound-effects` then
owns the audio asset and playback layer. Narrative ambience, scoring and
narration are outside this skill.

## Verification and handoff

Read the complete story with CSS and JavaScript disabled, then with reduced and
no motion. Test forward and reverse keyboard traversal, anchors, previous/next,
skip-story, zoom/reflow, short and narrow viewports, touch scrolling, back/forward
navigation, refresh at a deep anchor, and fast bidirectional scrolling. Confirm
that every visual state resolves and that no focused control is hidden.

Record observed coverage and mark the rest **Not verified**. Hand the operable
story to `humane:walkthrough`; this skill owns the narrative mechanism, while
`walkthrough` determines whether a reader can actually understand and complete
the intended path.

## What this skill does not own

| Concern | Owner |
| --- | --- |
| The source wording of headings and prose | `ux-writing` |
| Duration, dimension, color and typography values | `design-tokens` |
| Bounded component feedback inside a chapter | `semantic-micro-interactions` |
| Sound generation, assets and playback | `sound-effects`, reached through the micro-interaction hook |
| Task success and contextual verification | `walkthrough` |
| Framework-specific scroll-animation craft and accessibility engineering depth | `interfaces` when installed; otherwise mark the implementation depth Not reviewed |
