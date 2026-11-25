---
name: imagegen
description: This skill should be used when the user asks to "generate an image", "create a cover image", "make an illustration", "generate artwork", "create a hero image", "generate a logo", "make a banner", "create an image for", "generate a thumbnail", "make an icon", "create visual content", "edit this image", "restyle this image", "compose these images", or needs AI-generated or AI-edited images for their project. Provides a CLI with JSON output optimized for LLM consumption.
---

# imagegen

Text-to-image and image-editing CLI backed by Google Gemini's Nano Banana 2 family. JSON output.

## CLI

- Path: `./imagegen-cli/imagegen` (relative to this SKILL.md).
- Requires `uv` ([install](https://docs.astral.sh/uv/)). First call provisions the Python environment automatically.
- Subcommands: `generate` (alias `gen`). Pass `--image <path>` (repeatable) to edit, restyle, or compose existing images instead of generating from scratch.
- Always run `imagegen generate --help` to discover current flags and defaults. Do not memorize flag values — they evolve with the API.

## API key

The CLI looks for the key in this order:

1. `GEMINI_API_KEY` environment variable.
2. `.gemini-key` file (raw key, no quotes) found by walking up from the current working directory — project-local override. Add `.gemini-key` to `.gitignore`.
3. `~/.gemini-key` in the user's home directory — machine-wide default.

If none is found, the CLI returns `code: "API_KEY_MISSING"` with a recovery hint. Get a key at <https://aistudio.google.com/apikey>.

## Models

The `--model` choice gates which other flags work. Pick the cheapest that meets the need.

| Model                              | Sizes (`--size`)        | Aspect ratios (`--aspect-ratio`)                                            | `--thinking`             | Max `--image` inputs |
| ---------------------------------- | ----------------------- | --------------------------------------------------------------------------- | ------------------------ | -------------------- |
| `gemini-3.1-flash-image-preview` (default) | `512`, `1K`, `2K`, `4K` | `1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9`   | `minimal` (def.) / `high` | 14 |
| `gemini-3-pro-image-preview`       | `1K`, `2K`, `4K`        | `1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9`                       | always on, not user-set  | 14 |
| `gemini-2.5-flash-image`           | not configurable        | `1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9`                       | n/a                      | 3  |

Use the default for almost everything. Switch to `gemini-3-pro-image-preview` for high-stakes assets (legible long text, complex multi-element compositions). Switch to `gemini-2.5-flash-image` only for cost reasons on simple prompts.

## Prompting (these are thinking, creative models)

These models reason about composition and fill creative gaps on their own. Provide intent and context — not exhaustive specs.

- Give what only the user knows: brand, audience, where the asset goes, mood, must-include elements, must-avoid elements.
- Let the model choose lens, lighting, palette, and layout unless the user specified them.
- One narrative sentence beats a tag list. Describe the scene, not keywords.
- For exclusions, prefer rewriting the prompt positively (e.g. "an empty street" instead of `--negative-prompt "people, cars"`). Use `--negative-prompt` only as a last resort.
- Iterate by saving the output and re-invoking with `--image <previous-output>` plus a small directive (e.g. "warmer lighting, keep everything else").

## Output rules

- Always pass `--output <path>` and place the file in a project-appropriate assets directory (e.g. `src/assets/`, `public/images/`). Use a descriptive filename matching the content.
- After the call returns `ok:true`, use the Read tool on the produced `file` path to confirm the image landed and looks right.
- Never generate copyrighted characters, real people's likenesses, or harmful content.

## Editing / composition

Pass `--image <path>` one or more times in addition to the prompt. Same `generate` command. Examples of when to use it:

- Add or remove elements from an existing image.
- Apply a style transfer.
- Compose a scene from multiple references (e.g. a model + a garment).
- Maintain character consistency across renders.
- Refine a previous generation.
