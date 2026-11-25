---
name: image-first-frontend
description: Generate a polished frontend reference screenshot through a configurable GPT-image-2-compatible generations endpoint, save and show versioned previews inside the project, revise selected previews through a configurable /images/edits endpoint, and reproduce only the user-approved design as functional frontend code with high visual fidelity. Use when Codex is asked to design, build, restyle, or recreate a web page, application screen, dashboard, landing page, or UI component through an image-first workflow, design approval loop, screenshot-driven implementation, pixel matching, or a 1:1 frontend recreation.
---

# Image-first Frontend

Generate a visual target before writing UI code. Let the user approve, edit, or redo versioned previews, then recreate the approved target at its exact viewport and adapt it responsively without using the screenshot as the page itself.

## Preconditions

1. Read `scripts/generate_reference.py` before the first API call.
2. Configure `GENERATIONS_API_URL`, `EDITS_API_URL`, and `API_KEY` at the top of the script. The URLs may point to any compatible provider; no OpenAI connection is required. Require the generations URL for a new design and the edits URL only when revising an existing preview.
3. Work inside the user's existing project and preserve its framework, design system, dependency choices, and local conventions.
4. Save every preview inside the current project under `design-previews/<page>/`. Use numbered files such as `reference-v01.png`; the helper refuses to overwrite an existing output.
5. Make one billable generation or edit at a time. Make another request only after technical failure or an explicit user request to revise or redo the design.

## Workflow

### 1. Establish the brief

- Inspect the repository, relevant route, existing styles, assets, and run commands.
- Identify the page purpose, audience, required content, required states, and target viewport. Default to `1536x1024` for a desktop page when no viewport is specified.
- Preserve exact user-provided product names and copy. Infer ordinary supporting copy when it does not create a meaningful product decision.
- Decide which content must appear inside the reference viewport. Do not ask preference questions that can be resolved from the project or brief.

### 2. Generate a versioned preview

Write a concise product brief and call the configured generations endpoint:

```bash
python <skill-dir>/scripts/generate_reference.py --brief "<product and page requirements>" --output <workspace>/design-previews/<page>/reference-v01.png --size 1536x1024
```

Use `--brief-file <path>` instead of `--brief` when the prompt is long. The helper requests a flat, implementation-ready webpage screenshot without browser chrome, device frames, perspective, or surrounding scenery.

Inspect the generated file only for technical failure such as an empty image, severe corruption, or an unusable crop. Do not silently discard a successful preview for aesthetic reasons and do not begin implementation yet.

### 3. Present the preview and wait

1. Display the generated image in the conversation with the available local image-viewing capability. Also give the user its project-relative path and version number; do not merely state that the file exists.
2. Stop before extracting an implementation spec or editing frontend files. Ask the user to choose one of three outcomes: approve this version, request specific changes, or redo it with a new direction.
3. On explicit approval, record the approved preview path and continue to implementation. Do not infer approval from silence, unrelated feedback, or a request to inspect the image.
4. On specific changes, edit the currently selected preview through `EDITS_API_URL`. Merge the original hard requirements with two clear blocks, `Preserve` and `Change`, then run:

```bash
python <skill-dir>/scripts/generate_reference.py --input-image <workspace>/design-previews/<page>/reference-v01.png --brief "Preserve: <accepted elements>. Change: <requested edits>." --output <workspace>/design-previews/<page>/reference-v02.png --size 1536x1024
```

Add `--mask <path>` only when a compatible mask is available and the configured endpoint supports it. Display the new version and return to this approval gate. If the edits endpoint rejects the request, surface its error; do not silently fall back to text-only generation because that loses image-conditioned fidelity.

5. On a redo request, preserve only the original product and content constraints, choose a materially different visual direction, and call the generations endpoint again without `--input-image`. Save the next numbered version, display it, and return to this approval gate.
6. If dissatisfaction is vague, ask one concise direction question before spending another request. Each explicit revise or redo request authorizes one new image, not a batch of alternatives.
7. Keep all preview versions for comparison. Do not delete, import into the application, or add them to version control unless the user asks.

### 4. Extract an implementation spec

Read the approved reference image and record the following in working notes:

- Exact reference viewport and major section bounds
- Container width, column grid, alignment, gaps, and padding
- Typography roles, approximate sizes, weights, and line heights
- Color palette, borders, radii, shadows, and surface hierarchy
- Icons, imagery, controls, interaction states, and responsive implications

Estimate measurements from pixels rather than replacing the design with generic defaults. Treat garbled image-generated text as a visual placeholder; correct user and product copy takes precedence.

### 5. Implement the page

- Reproduce only the explicitly approved reference with semantic HTML and real components. Never embed the full reference screenshot as a background or slice it into a fake interface.
- Match macro geometry first: page bands, section heights, container width, columns, and major assets. Then match typography, spacing, controls, borders, colors, and shadows.
- Reuse the project's components, tokens, icon library, and assets where they fit. Use a familiar icon library already present in the project instead of drawing replacement SVG icons.
- Source or generate standalone visual assets when the reference contains imagery that code and CSS cannot reproduce. Do not substitute unrelated placeholder imagery.
- Implement expected interactions and states; a visually accurate inert control is incomplete.
- Match the reference at the target viewport. Add intentional responsive behavior for other widths without scaling the entire desktop canvas.
- Keep the change scoped to the requested page and avoid unrelated refactors or dependency churn.

### 6. Compare and iterate

1. Start the application using its normal local command.
2. Capture a browser screenshot at the exact reference viewport.
3. Compare the implementation and reference side by side or with an overlay/diff tool when available.
4. Fix the largest visible deltas in this order: geometry, typography and wrapping, spacing, imagery, color, borders and shadows, then small details.
5. Repeat until remaining differences are minor and explainable.
6. Check at least one narrow viewport, browser console errors, loading states, focus/hover behavior, clipping, overlap, and horizontal overflow.

Do not claim a 1:1 result without a same-size screenshot comparison. Report the approved reference path, implemented route, validation viewports, and any unavoidable divergence.

## Fidelity Contract

- Interpret `1:1` as visual fidelity at the reference viewport plus functional, responsive code.
- Treat the user's explicitly approved preview version as the sole visual source of truth.
- Preserve business and content correctness when generated text conflicts with the brief.
- Recreate appearance through layout, styles, components, and proper assets, not screenshot embedding.
- Prefer a close measured implementation over redesigning the approved reference from personal taste.
- Surface ambiguity when an image does not reveal behavior; implement the conventional behavior that best fits the existing application.

## API Helper

Configure `GENERATIONS_API_URL`, `EDITS_API_URL`, `API_KEY`, and optionally `MODEL` in `scripts/generate_reference.py`. The generations request uses JSON. Supplying `--input-image` switches to `multipart/form-data` at the edits URL with `image`, `prompt`, `model`, `n`, `size`, and `quality`; `--mask` adds the optional `mask` file. The helper uses only the Python standard library and accepts compatible responses containing base64 image data or an image URL.

Inspect secret-free request summaries before making a billable call:

```bash
python <skill-dir>/scripts/generate_reference.py --brief "A focused analytics dashboard" --output reference-v01.png --dry-run
python <skill-dir>/scripts/generate_reference.py --input-image reference-v01.png --brief "Preserve the layout. Change the accent color to green." --output reference-v02.png --dry-run
```

Keep credentials out of prompts, command arguments, logs, screenshots, and committed project files.
