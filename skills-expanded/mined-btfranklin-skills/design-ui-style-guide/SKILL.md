---
name: design-ui-style-guide
description: >-
  Create a visual system for a new or redesigned user interface. Generate exactly three image concepts and stop for user approval. After approval, create an HTML and CSS style guide with a representative demo. Do not use when the user supplies an approved design, requests a small edit, or skips visual exploration.
---

# Design UI Style Guide

Turn a user-interface idea into an approved concept and a reusable HTML style guide. Use two explicit checkpoints. First, get approval for one concept. Then deliver the style guide.

Control the requirements for the concepts and style-guide files. Do not implement the full product unless the user makes a separate request after the guide exists.

## Required Capabilities

- Select an image-generation method in this order:
  1. In Codex, use `$imagegen` when it is available and follow that skill's generation and image-editing workflow.
  2. In another agent or harness, use its image-generation skill or tool when one is available.
  3. If no image-generation capability exists, use the text-only fallback below.
- Do not replace available image generation with prose, SVG mockups, or CSS sketches.
- During the file-creation phase, use `design-html-first-web-uis` when available. It supplies instructions for semantic HTML, native browser behavior, progressive enhancement, accessibility, and minimal JavaScript.

If `design-html-first-web-uis` is missing, continue with the semantic HTML and accessibility requirements in this skill. Do not interrupt the task to propose installation of this optional companion. Install it only when the user requests installation.

If image generation is not available, state this limitation. Provide prompt-ready concept briefs. Ask whether to continue with text-only planning. Do not state or imply that you generated images. Outside Codex, do not require a specific image skill, plugin, model, or vendor.

## Workflow

1. Inspect the brief. Inspect existing repository guidance, content, brand assets, screenshots, and technical limits.
2. Identify the audience, product purpose, primary screen or workflow, required content, device priority, brand limits, and prohibited designs. Infer defaults that have low risk. Ask only when an unresolved choice will change the concepts.
3. Write one sentence that defines each concept. Describe the composition, surface treatment, typography, and visual tone.
4. Read [references/concept-prompt-patterns.md](references/concept-prompt-patterns.md) and [references/visual-quality-and-ai-tells.md](references/visual-quality-and-ai-tells.md).
5. Generate exactly three concept images. Use these categories: Traditional, Futuristic/Advanced, and High-concept/Strange. Give each concept its own prompt and image.
6. Review the concepts against the visual-quality reference. Regenerate a generic, repetitive, or unreadable concept. Also regenerate a concept that is outside the brief, incomplete, or difficult to implement in HTML and CSS.
7. Present all three images with the exact prompt and a short rationale for each.
8. Stop at the selection checkpoint. Ask the user to choose one, request another batch, or give targeted iteration guidance.
9. For a new set, preserve the three categories. The user can instead request variants of one concept or a combination of concepts.
10. After approval, read [references/style-guide-contract.md](references/style-guide-contract.md). Use the approved concept and user-supplied content as the authoritative visual and editorial references.
11. If an important region is too small, unclear, or cropped, use the approved visual system to complete the detail when its rules are sufficient. Otherwise, generate a detailed concept for that region. Preserve the approved design direction.
12. Create the output under `ui-style-guide/` in the current project or workspace:
    - `style-guide.html`
    - `style-guide.css`
    - `demo.html`
    - `assets/selected-concept.*` when the image is project-bound
13. Match the approved concept closely. Replace details that are impossible, fragile, or inaccessible with maintainable HTML and CSS. Record important compromises.
14. Verify the structure and appearance of the guide and demo. Report the approved concept, file paths, completed checks, and intentional differences.

## Constraints

- Do not generate the style guide before the user approves a concept.
- Do not implement the full product in the default workflow. Deliver a style guide plus one representative screen.
- Do not invent product claims, company names, testimonials, metrics, or precise values without evidence. Clearly label sample data when examples are necessary.
- Keep visible copy specific, purposeful, and consistent with the product context. Preserve exact supplied copy.
- Keep interactive UI text and controls in HTML. Use generated imagery for visual assets, not as a substitute for working UI.
- Use CSS custom properties for tokens. Make `demo.html` depend on `style-guide.css` so the demo proves the guide is reusable.
- Prefer native HTML controls and accessible state styling. Add JavaScript only for small interactions that cannot be represented declaratively.
- Use the undesired-pattern reference to identify common model defaults. Apply judgment to each pattern. Keep an undesired pattern when the brief, brand, domain, or approved concept gives it a clear purpose.

## Handoff

After concept generation, provide:

- The three images labeled `1. Traditional`, `2. Futuristic/Advanced`, and `3. High-concept/Strange`
- The exact prompt and one-sentence rationale for each
- A direct selection checkpoint

After style-guide delivery, provide:

- The approved concept category and saved image path when applicable
- Paths for `style-guide.html`, `style-guide.css`, and `demo.html`
- A concise description of the extracted visual system
- Structural and visual verification performed
- Any fidelity compromises or intentionally retained undesired patterns
