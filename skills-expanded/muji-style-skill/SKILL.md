---
name: muji-style-skill
description: Create original quiet-living visuals from any theme, object, product, article, event, space, or supplied photograph using natural materials, restrained color, functional typography, asymmetric whitespace, honest photography, and human imperfection. Always use this skill when the user asks for MUJI-inspired, 无印良品感, 日系极简, Japanese minimalism, quiet living, natural minimalism, understated lifestyle design, 素朴生活美学, 留白产品海报, or asks to make a visual feel quieter, simpler, more natural, and less designed. Preserve the underlying design principles without copying MUJI logos, packaging, campaigns, store layouts, product silhouettes, wording, or identifiable compositions. Return a production-ready prompt and generate a raster image when image-generation tools are available, unless the user explicitly asks for prompt-only.
---

# MUJI Style Skill

Turn the user's subject into an original visual that feels quietly useful rather than visibly styled:

> natural material + functional order + generous emptiness + ordinary human presence

This is not a brand imitation skill. Extract principles associated with restrained Japanese domestic design, then create a new composition with no brand identifiers or recognizable campaign language.

## Default Deliverable

Create:

1. one production-ready image-generation prompt;
2. one generated raster image when an image-generation tool is available;
3. a one-line recipe naming the palette, composition, material, and image treatment.

Save generated files under `~/Desktop/Claude skills/muji-style-skill/` when file access is available. Return prompt-only only when the user requests it or no image-generation capability exists.

## Read the Input

Resolve these fields before composing. Do not expose the manifest unless the user asks for process details.

```yaml
subject: <one primary object, person, place, or idea>
purpose: <product study, editorial poster, information notice, packaging concept, spatial mood, or illustration>
audience: <who must understand or use it>
exact_text: <user-supplied wording, a short factual phrase, or none>
ratio: <user choice or 3:4>
material_anchor: <one primary material>
palette: <one neutral family plus optional muted red>
composition: <one family from Composition Decision Flow>
empty_space: <percentage>
image_mode: <honest photograph, material still life, line illustration, or type-only>
human_trace: <one subtle sign of use or imperfection>
```

For a broad theme, choose one ordinary object or daily action as the visual metaphor. Do not illustrate every idea.

Preserve user-supplied text exactly. When no display text is supplied, use no headline by default. Add a factual label of 2-6 words only when the purpose needs identification.

## Composition Decision Flow

Walk from top to bottom and use the first matching rule:

1. Is the user presenting one physical product or object?
   - Use **small-object field**: subject occupies 18%-36% of the canvas, with one clear alignment edge and 55%-75% empty space.
2. Is the content instructional, scheduled, categorized, or data-bearing?
   - Use **quiet information grid**: 2-3 columns, left-aligned labels, thin rules only where they clarify grouping, and 35%-55% empty space.
3. Is a supplied photograph the main evidence?
   - Use **observed-life crop**: keep the scene recognizable, crop without drama, and reserve one broad empty zone for pacing or factual text.
4. Is material, texture, or craft the subject?
   - Use **material study**: one close view plus one small contextual detail; let fibers, grain, glaze, or wear carry the visual interest.
5. Is the request conceptual or text-led?
   - Use **editorial pause**: one short left-aligned phrase, one tiny supporting image or line drawing, and at least 65% empty space.
6. Is the request for an illustration?
   - Use **useful line drawing**: one black or charcoal line system, one muted accent at most, and only details needed to explain the object or action.
7. Otherwise use **domestic still life**: one main object, no more than two supporting objects, natural light, and visibly ordinary arrangement.

Never center every element. Never distribute several small objects evenly to fill the page. Emptiness must create sequence and attention, not merely surround a centered subject.

## Visual System

### Color

Use material colors before invented colors.

- Paper white: `#F3F0E8`
- Unbleached paper: `#E7DFCF`
- Warm gray: `#B8B2A8`
- Sand: `#C9B99F`
- Natural wood: `#A88967`
- Charcoal: `#34332F`
- Muted red accent: `#8F3D32`

Choose one light base, one dark text color, and no more than two supporting neutrals. Use muted red only for a functional cue such as a date, index, seal-like marker, or state; keep it below 5% of the image area.

Do not use gradients, neon colors, high-saturation accents, glossy black, or more than four visible colors. Low saturation alone is not enough: the colors must plausibly belong to paper, wood, cloth, clay, glass, or metal.

### Space and Grid

- Default to a flat `3:4` canvas; obey a user-specified ratio.
- Keep 50%-75% visibly empty in image-led work and 35%-55% in information-led work.
- Keep outer margins at 7%-12% of canvas width.
- Use one left alignment axis or a simple 2-3 column grid.
- Use asymmetry by changing visual weight, not by tilting elements randomly.
- Limit the composition to one primary subject and zero to two supporting objects.
- Use one deliberate quiet tension: a small off-center subject, an unexpectedly large margin, a cropped edge, or a tiny isolated label.

Do not add cards, floating panels, decorative badges, ornamental frames, or repeated rounded containers. Structure should come from spacing and alignment.

### Typography

Typography carries information and then gets out of the way.

- Use one neutral sans-serif family; add a restrained serif only for long editorial reading.
- Use regular or medium weight for almost all text; reserve bold for one factual emphasis.
- Left-align by default.
- Use a clear three-level hierarchy: title, supporting fact, micro label.
- Keep display text compact and naturally spaced. Do not use exaggerated tracking to manufacture luxury.
- Use sentence case for human language and uppercase only for short codes or categories.
- Keep line length between 35 and 65 characters for paragraphs.

Never use outlined type, drop shadows, 3D type, condensed fashion-magazine headlines, giant motivational slogans, or text used as decorative filler.

### Photography

Prioritize tactile evidence over spectacle.

- Use soft window light or open shade from one believable direction.
- Keep shadows soft but present; do not flatten the object into a cutout unless the purpose is cataloging.
- Show honest fibers, grain, glaze variation, fingerprints, folds, wear, or minor irregularity.
- Use a neutral environment that feels inhabited but not staged.
- Keep the camera at eye, table, shelf, or hand level; avoid cinematic low angles and dramatic perspective.
- Use moderate depth of field so the material remains readable.
- Retouch only distractions. Preserve material variation and signs of use.

Do not use luxury-product lighting, hard rim lights, glossy reflections, heavy bokeh, dramatic haze, perfect showroom styling, or stacks of aesthetic props.

### Illustration

Make the drawing useful before making it charming.

- Draw only contours, joints, folds, labels, and gestures required to identify the subject or explain an action.
- Use one consistent charcoal or graphite line with slight pressure variation.
- Permit small misalignment and uneven curves, but keep proportions legible.
- Use flat paper exposure instead of digital shading; add sparse hatching only to clarify material or depth.
- Add no more than one muted color field.

The target is a careful human diagram, not childish decoration. Never add mascots, kawaii faces, sticker clusters, polished vector gradients, or ornamental doodles unless the user explicitly requests them.

### Material as Structure

Choose one primary material and let its physical behavior determine the composition:

- **Paper:** visible fibers, folds, deckled or clean-cut edge; organize with sheets, labels, or stacked planes.
- **Wood:** grain direction and joinery establish alignment; avoid orange varnish and rustic nostalgia.
- **Cotton or linen:** folds create rhythm; keep color unbleached and texture matte.
- **Clay or ceramic:** small glaze variations and weight create focus; avoid artisanal clutter.
- **Glass:** use transparency and one soft reflection to reveal function; avoid jewel-like sparkle.
- **Metal:** use brushed or softly worn surfaces; avoid chrome glamour.

Texture must provide evidence about the object. Never overlay generic paper grain merely to make a digital image look tasteful.

### Human Tone

Keep exactly one concrete human trace in the entire image: a softened fold, a cup ring, a slightly shifted stack, a hand entering the frame, a repaired edge, a penciled note, or one area of natural wear. Once selected, explicitly exclude all other signs of handling, use, repair, and human action.

The trace must result from handling, use, repair, or a present human action. Wood grain, uneven glaze, firing marks, paper fibers, and other manufacturing or material variations do not count as a human trace. When the subject already has strong material variation, add one restrained sign of use instead of relabeling that variation as human evidence.

The trace prevents sterility. It must suggest ordinary use, not become a nostalgic prop or lifestyle performance.

## Originality Firewall

- Never include the MUJI name, wordmark, Japanese brand text, product codes, price labels, red brand block, or recognizable packaging system unless the user supplies them for factual analysis and explicitly requests preservation.
- Never recreate a known advertisement, catalog spread, store interior, product silhouette, campaign photograph, or copy line.
- Never ask an image model to imitate a named living designer, photographer, studio, or brand.
- Translate references into abstract decisions: restrained palette, material honesty, functional hierarchy, asymmetric whitespace, and signs of use.
- When the user requests a direct replica, explain that the output will preserve the quiet-living principles while using an original composition and unbranded details.

## Prompt Construction

Write the final image prompt in this order:

1. original subject and daily-life context;
2. selected composition family with numeric subject and empty-space proportions;
3. primary material and its visible physical evidence;
4. exact palette with color roles;
5. light, camera, crop, and shadow behavior;
6. typography placement and exact supplied text, if any;
7. one human trace;
8. output ratio and production medium;
9. explicit exclusions.

Resolve every choice before writing the prompt. Do not use `or`, slashes, optional alternatives, or multiple possible placements; name one material, one crop, one light direction, one human trace, and one subject position. Include a palette color only when a visible object, surface, text role, or physical shadow requires it. Do not add wood, cloth, paper, or another neutral material merely to make the palette feel complete.

Do not use `MUJI-style` or `in the style of MUJI` in the generation prompt. Describe the visual decisions directly so the result is original and the model cannot substitute brand clichés for composition.

## Quality Gate

Before delivering, verify every item:

- [ ] One primary subject is readable at thumbnail size.
- [ ] Empty space meets the selected composition's numeric range.
- [ ] One light base, one dark color, and at most two supporting neutrals are visible.
- [ ] Muted red, if used, has a functional role and covers under 5%.
- [ ] The layout has one dominant alignment axis and is not fully centered.
- [ ] Typography is left-aligned unless the content provides a concrete reason otherwise.
- [ ] One material is visually specific rather than simulated with a generic texture overlay.
- [ ] Exactly one concrete human trace is present; no second sign of handling, use, repair, or human action appears.
- [ ] No gradients, glossy effects, decorative cards, luxury lighting, or filler props appear.
- [ ] No protected brand identifier or recognizable campaign composition appears.
- [ ] The result communicates its purpose before it communicates a style.

If three or more checks fail, simplify the composition and regenerate. Remove elements before adding new ones.
