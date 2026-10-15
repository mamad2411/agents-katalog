---
name: creative-scene
description: Generate realistic product-in-use lifestyle scenes. Places the product in believable contexts of use (who, where, when, doing what) with natural lighting and real texture, for lifestyle/editorial/ecommerce. Use when the user says "lifestyle shot", "product in use", "scene", "show it being used", "in-context photography", or needs people/environment around the product. Part of the Creative Production set.
---

# Creative — Scene Explorer

Show the product living in the real world — believable usage moments, not floating studio renders. The job is to make a viewer picture *themselves* using it. Realism and emotional plausibility beat technical perfection.

## When to use
- Lifestyle hero images, social content, editorial, "in-context" ecommerce shots.
- Selling the *experience* or *outcome*, not just the object.
- You need people, environment, or a moment of use around the product.

## When NOT to use
- Clean catalog/PDP angles on a plain background → `creative-shot`.
- Pushing a discount/bundle → `creative-offer`.
- No look locked and brand consistency matters → `creative-explore` first.

## Inputs (ask only what's missing)
- **Product** + how it's *actually* used (ergonomics matter for believability).
- **Target user** who appears or is implied in the scene.
- **Locked visual direction** if available.
- **Aspect/medium**: web hero (wide), social (square/vertical), gallery.

## Workflow
1. **Define 3-5 usage moments**: who + where + when + doing-what. Concrete beats generic ("barista, morning cafe, steaming milk" not "person using product").
2. **Structure each scene prompt**: `backdrop → subject + product → light/lens → constraints`. Favor photoreal-natural styling: candid, real texture, natural light, believable depth of field.
3. **Generate** with your image tool. Save to `./creative/scene/<moment>.png`.
4. **Verify believability + hero**: is the product clearly the focus? Are hands/ergonomics plausible? Regenerate weak ones (bad hands, product too small, staged-feeling).
5. **Present moments**; recommend the strongest for the medium.

## Worked example
Product: insulated water bottle. Audience: trail runners.
```
## Moment "Dawn Trail"
who: runner, late 20s, mid-stride   where: forest trail, first light
when: cool blue-hour → warming   doing: pausing to drink
prompt: "forest trail at dawn -> runner pausing, bottle to lips, breath visible
-> 50mm, shallow DOF, soft directional light -> candid, real sweat/texture,
bottle clearly visible and in focus"
[ref: ./creative/scene/dawn-trail.png]

## Moment "Desk Companion"
who: implied (hand only)   where: tidy work desk   when: midday
doing: reaching for the bottle beside a laptop
prompt: "minimal wood desk, daylight -> hand reaching for bottle next to laptop
-> 35mm, natural light -> candid, real texture, bottle hero"
[ref: ./creative/scene/desk.png]
```
Recommendation: "Dawn Trail" for the hero (aspirational, on-audience); "Desk" for broader appeal.

## Quality bar
- The product is unmistakably the hero and in focus — not lost in the scene.
- Lighting, texture, and ergonomics are plausible; no uncanny hands or impossible grips.
- The moment matches the actual audience and use case.
- Aspect fits the target medium without awkward cropping.

## Common pitfalls
- **Floating/staged feel** — natural light and real texture sell realism; studio-perfect kills it.
- **Product demoted** — the environment overwhelms the hero. Keep it central and focused.
- **Mangled hands/anatomy** — common generation failure; regenerate or switch angle.
- **Real identifiable people without consent** — use generic or implied (hands, back-of-head) subjects.

## Handoff
Winning scenes → `creative-polish` for finish (grade, fix artifacts, conform aspect). Reuse the `creative-explore` stub for cross-asset consistency.

## Tooling
Needs a text-to-image tool. Without one, deliver the structured scene prompts for the user to render.
