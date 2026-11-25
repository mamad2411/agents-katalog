---
name: motion-design
description: Design and implement distinctive, usable web interfaces from a brief, or improve an existing frontend's composition, typography, surfaces and interaction states. Use alongside motion-3d-ui for cinematic scenes; preserve established product design systems.
---

# Design an interface with intent

Read the brief and the existing frontend before choosing a look. Preserve the requested product, stack and brand. For a redesign, inspect the running page before changing it.

## Pick a direction that changes the code

State the audience, primary task and visual direction in one short sentence. Choose three contextual settings: compositional freedom, motion energy and information density. A professional tool may need compact predictable structure; a character-led launch page can use a spacious asymmetric stage. There is no preset palette or mandatory library.

Make one memorable move, then support it with a quiet system: an oversized product crop, an editorial type scale, a spatial scene, a crisp technical grid, or an unusually clear interaction. Do not stack all of these. If a reference is provided, extract its hierarchy, rhythm and material logic rather than copying its mascot, layout or assets.

## Build a coherent visual system

- Establish tokens for background, foreground, muted text, accent, border, surface, spacing and radii. Keep hue temperature and component roles consistent. Accent can guide action; semantic status colors remain distinct when needed
- Choose typography for the audience and available licensed assets. Pair a display voice with readable body text; use fewer weights and intentional line breaks. Measure heading and button fit at actual breakpoints, including font fallback and italic descenders
- Compose the first viewport as a relationship between copy, action and visual. Give the main task a clear path. Empty space should separate meanings, not strand the controls. Use asymmetry when it strengthens that relationship, not as a required trick
- Use cards for discrete objects or genuinely separate tasks. Group continuous content through alignment, rules and spacing instead of wrapping every sentence in another rounded box
- Give repeated sections different jobs and appropriate structures. A product demonstration, specifications and explanation need not repeat the same three-column template. Avoid adding decorative sections merely to make the page longer
- Build an original relevant visual. For spatial illustration, route to `motion-3d-ui`; for supplied photos or assets, preserve provenance. A wireframe box labelled “preview” is not a finished hero visual

Keep the existing component system when it fits. Check installed dependencies before importing another package; a trend name is not an official design system. External fonts/assets must not become a hidden network requirement for local recording.

## Finish the interaction, not just the screenshot

Implement the states that the task actually has: initial, pending, success, empty, error, disabled and interrupted. Match loading geometry to the settled layout when stability is intended. Controls need actual effects, visible focus, readable labels and clear pressed/selected states. Avoid fake customer quotes, invented specifications or unsupported performance numbers; label illustrative data.

At narrow widths, reorder deliberately: task copy and controls remain usable, visuals resize or simplify, and sticky elements cannot cover content. Test keyboard access, contrast and reduced motion. Expressive motion can communicate depth or a state change without making basic navigation depend on animation.

## Inspect before calling it polished

View the real page at desktop and a narrow viewport. Check headline clipping, line lengths, focal balance, contrast, control reachability and overflow. Then exercise the principal interaction and its interruption. Use `motion-build-inspect-repair` for the recorded build/review/repair loop. Change the implementation based on visible evidence, not adjectives in the source.

## Provenance

This is an independently worded adaptation of selected brief inference, contextual design controls, visual consistency and interaction-state ideas from [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill/tree/ce26fc25c0e5e8cab638f883de62d9a86ee5e45b). See [the exact source and retained MIT notice](references/taste-provenance.md). It does not adopt upstream's fixed stack, numeric presets, font bans or mandatory asset-generation rules. Motion Debugger's project license is unchanged.
