---
name: image-effects
description: This skill applies reusable, versioned visual effects to a text idea or an explicitly attached JPEG or PNG through host-native image generation and, when required, deterministic layout. It should be used when a user asks to browse, select, or execute an effect from the bundled image-effects library.
---

# Image Effects

Apply one bundled library effect while preserving the selected effect version, input privacy, required execution stages, and host-native delivery. Every effect card is self-contained; do not require or invoke an upstream Skill.

## Resolve the effect

1. Every effect request must use the complete `<id>@<version>` stable reference before execution.
2. If the user provides no ID, read `references/INDEX.md` and recommend at most five relevant effects. Do not read every effect card to make recommendations.
3. If the user provides an ID without a version, do not infer or substitute a version. Read `references/INDEX.md`, show the matching versioned choices, and require the user to select an exact version before execution.
4. If the ID or version is unknown, return nearby choices from the index and stop. Do not execute a similar effect automatically.
5. After resolving an exact reference, read only its selected card under `references/effects/`. Treat that card as the complete behavior and provenance source of truth.

## Validate the input

Read the selected card's `input_mode`, then follow exactly one branch:

- `image`: accept exactly one JPEG or PNG explicitly attached to the current request. Stop before invoking an image tool when there are zero images, multiple images, or an unsupported format.
- `text-or-image`: accept either a non-empty text idea with zero images, or one explicitly attached JPEG or PNG with optional text direction. Stop when both the text idea and image are absent, when there is more than one image, or when the image format is unsupported.

For both branches:

- Do not scan attachment directories, prior messages, history, or nearby files to guess an input.
- Create a temporary copy only when host transport or deterministic layout requires one. Delete every temporary copy and intermediate asset when the task ends, including after failure.
- Do not add user input, a private path, or intermediate content to the effect library, Gallery, logs, preview assets, or output metadata.

## Execute the effect

Compile the selected card's complete rules together with the user's stated goal. Then follow its `execution_kind` exactly.

### `host-image-generation`

1. Use the host's native image-generation or image-editing capability with the compiled prompt and the validated image, if present.
2. Keep the selected effect reference and subject constraints unchanged. If the tool errors or the result violates a hard quality rule, make at most one targeted retry that addresses that specific failure.
3. If no compatible image capability is available, return the complete compiled prompt for the user to copy and clearly state that no image was generated. Do not write a prompt file unless requested.

### `host-image-generation-and-layout`

1. Before Stage A, verify that the host has both native image generation or editing and local HTML/CSS screenshot capability, or an equivalent deterministic layout-and-rasterization path.
2. If either capability is missing, generate no intermediate or partial image. Return the complete motif prompt, Copy Map, output dimensions, composition plan, and a statement naming each missing capability. Do not claim that the final image was produced.
3. Stage A and Stage B share one total targeted retry budget across the entire effect. Spend it either on Stage A regeneration after an image-tool error or hard-quality failure, or on Stage B repair and recapture after a layout or screenshot tool error or hard-quality failure, never both. If Stage A spends the budget, report any Stage B failure without another retry. When Stage B spends the budget, do not regenerate an already acceptable motif.
4. Stage A generates only the isolated illustrated motif defined by the selected card. Do not ask the image model to render the final page, photo panel, or text.
5. Stage B lays out the validated source image as an unchanged photo anchor together with the generated motif, real text from the Copy Map, rules, and color swatches at the card's fixed dimensions. Rasterize with the preflighted screenshot or equivalent deterministic capability, without browser chrome or scrollbars.
6. Keep text crisp and editable in the layout source, keep the photo anchor truthful, and do not turn the motif into a second rectangular photograph.

Do not substitute one execution kind for the other or silently omit a required stage. Do not implement a global lock, queue, or concurrency limit; each requested effect output succeeds or fails independently under the host's own execution model.

## Deliver the result

Use the host's native image delivery path. When running in Happy and its native image delivery tool is available, send the generated image through that tool. Keep private paths, raw commands, and tool logs out of the final response.
