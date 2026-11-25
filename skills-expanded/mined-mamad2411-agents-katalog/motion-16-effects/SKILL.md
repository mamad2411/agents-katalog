---
name: motion-16-effects
description: The 16 interface and type motion effects from the "Opus 5.5 Motion Graphics" sheet (button to player, search to results, card to workspace, tabs to panels, chart morph, dashboard zoom, spring stack, magnetic dock, masked type, elastic type, text to layout, image reveal, perspective shift, glass focus, flowing paths, particle logo), each with a plain description and a prompt template to build it in HTML, CSS and JavaScript. Use when the user wants a specific UI animation, a motion reference list, or example effects for a landing page or dashboard. Source 51ultron.com sheet (Batch 101); the sheet shows previews only, so the descriptions are inferred from the thumbnails and captions.
---

# 16 motion effects

The sheet title says "16 examples: interfaces, type and data". The previews are tiny, so each description below is inferred from the thumbnail and its caption, not from source code. Treat the model name on the sheet as the source's claim.

| # | Effect | What the thumbnail shows |
|---|---|---|
| 1 | Button to player | a Preview button expands into an audio player with a progress bar |
| 2 | Search to results | typing in a search box fills a results list |
| 3 | Card to workspace | a small card opens into a full workspace panel |
| 4 | Tabs to panels | switching tabs swaps the content panel |
| 5 | Chart morph | a line chart animates between data states with a highlighted point |
| 6 | Dashboard zoom | a dashboard card zooms in to a detail view |
| 7 | Spring stack | stacked cards settle with spring physics |
| 8 | Magnetic dock | dock icons grow as the cursor approaches |
| 9 | Masked type | big type reveals through a mask |
| 10 | Elastic type | text stretches by width and weight, "STRETCH" |
| 11 | Text to layout | a headline rearranges into a page layout |
| 12 | Image reveal | an image appears over a coloured field |
| 13 | Perspective shift | flat panels tilt into a 3D stack |
| 14 | Glass focus | a frosted lens magnifies one row of a report |
| 15 | Flowing paths | nodes connected by animated curved lines |
| 16 | Particle logo | particles assemble into a logo |

## Prompt template

```
Build a self-contained HTML, CSS and JavaScript demo of the "[EFFECT NAME]" interface motion: [DESCRIPTION FROM THE TABLE].
Constraints: no libraries unless the effect needs one (then GSAP from cdnjs, pinned), respect prefers-reduced-motion, keyboard accessible, works at phone width, under 150 lines of JavaScript, with real-looking content instead of lorem ipsum.
Show the start state, the motion, and the end state, and add one control to replay it.
```

Related installed skills: `motion-foundations`, `motion-patterns`, `motion-advanced`, `ui-motion-design`, `gsap-core`, `gsap-timeline`, `make-interfaces-feel-better`.
