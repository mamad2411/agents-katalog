---
name: gpt-image-2-ecommerce
description: Plan, prompt, and review product-preserving ecommerce image sets for GPT Image 2 or other image models. Use when the user needs marketplace main images, white-background product photos, product detail page or PDP sequences, lifestyle scenes, feature graphics, ad crops, product-image prompt packs, or QA against source product references. Also use when generated product images change geometry, color, material, labels, logos, controls, ports, packaging, accessory counts, or verified claims.
---

# GPT Image 2 Ecommerce

Build the smallest useful ecommerce image set while treating source product references and verified facts as immutable evidence. Optimize for product accuracy and purchase clarity before style variety.

## Non-negotiable rules

- Treat source images, packaging, manuals, and user-confirmed facts as the only product truth.
- Never invent dimensions, materials, certifications, performance data, ingredients, compatibility, awards, reviews, or included accessories.
- Separate invariants from allowed changes in every prompt.
- Assign one primary sales job to each image.
- Do not ask an image model to typeset factual packaging or dense sales copy when exact text matters. Prefer an unlettered base image and downstream layout.
- Reject an attractive asset if it changes the product or communicates an unsupported claim.
- Use the fewest assets that cover the purchase questions. Do not fill a fixed template count.

## Workflow

### 1. Establish the source of truth

Identify the available evidence:

- Product reference images and which views they show.
- Product name, category, actual use, audience, and included items.
- Verified claims and the source for each claim.
- Platform, placement, aspect ratios, safe zones, and text policy.
- Brand references that define color, light, and visual tone.

If a missing fact affects product identity or claim accuracy, ask for it. If it only affects creative direction, state a conservative assumption and continue.

Use [references/brief-format.md](references/brief-format.md) for the normalized brief. When the user supplies JSON, validate it with:

```bash
python3 scripts/validate_brief.py path/to/brief.json
```

### 2. Write the product identity lock

List observable invariants before writing any creative prompt:

- Geometry: silhouette, proportions, count, openings, controls, ports, seams.
- Appearance: real colors, materials, finish, transparency, texture.
- Identity: label area, logo position, packaging structure, distinctive marks.
- Set contents: included product, accessories, quantity, relative scale.

Also list allowed changes, usually background, lighting, camera angle within supported views, crop, and composition.

Do not infer unseen rear or internal structure from a single front view. Request another reference or avoid that angle.

### 3. Plan the minimum asset sequence

Map each unresolved purchase question to one asset. Typical jobs are:

1. Identification: clean hero or white-background main image.
2. Context: one realistic use scene that establishes scale and purpose.
3. Evidence: material, construction, texture, or visible feature detail.
4. Explanation: one verified benefit or feature per graphic.
5. Fit: dimensions, compatibility, or included parts only from supplied facts.
6. Acquisition: ad crop with a deliberate copy-safe area.

Remove duplicate jobs. If three images answer the purchase questions, propose three—not six.

### 4. Write one complete prompt per asset

Every prompt must contain:

1. Source reference role.
2. Product identity lock.
3. One asset objective.
4. Composition and subject occupancy.
5. Environment, lighting, camera, and depth.
6. Aspect ratio and copy-safe area.
7. Text and claim policy.
8. Explicit exclusions tied to likely failure modes.

Read [references/prompt-patterns.md](references/prompt-patterns.md) for patterns. Adapt them to the product; do not emit bracketed boilerplate as a finished deliverable.

### 5. Generate only when requested and supported

If the user asks only for a plan or prompts, return those without generating images.

If the user asks for images and an image-generation tool is available, generate the first identity-sensitive asset before the full set. Review it against the source. Continue only after the product lock is holding.

When editing an existing image, describe both the requested change and what must remain unchanged. Prefer small, focused revisions over rewriting the entire scene.

### 6. Run the four-gate QA

Use [references/qa-checklist.md](references/qa-checklist.md) on every generated asset:

1. Product identity.
2. Composition and asset job.
3. Text, claims, and factual integrity.
4. Cross-set consistency.

Return `PASS`, `REVISE`, or `REJECT` per asset. `REJECT` is mandatory for product substitution, changed geometry, fabricated claims, incorrect included items, or unsafe/misleading use.

## Output contract

Return sections in this order:

1. **Known facts and evidence**
2. **Missing facts or stated assumptions**
3. **Product identity lock**
4. **Minimal asset plan**
5. **Production prompts**
6. **QA criteria**
7. **Review results**, when assets exist

For each asset include: job, placement, ratio, prompt, required references, exact text policy, and rejection conditions.

Keep explanations short. Spend detail on constraints that prevent product or claim errors.
