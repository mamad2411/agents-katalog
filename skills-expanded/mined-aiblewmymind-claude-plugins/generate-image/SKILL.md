---
name: generate-image
description: "Guide for generating and refining AI images using Daria's AI Blew My Mind (AIBMM) image prompts. Use this skill when the user wants to generate, create, make, or refine an image, picture, illustration, logo, or any visual content using Daria's prompts or the AIBMM image generation tools. Also use when the user asks about image generation, image refinement, reference images, or image quota."
user-invocable: true
argument-hint: "[what to generate]"
---

# Generating and Refining Images with Daria's AIBMM Prompts

You have three image tools. Pick the right one based on what the user is asking for.

| Tool | When to use |
|---|---|
| `generate_image` | First-time generation, or a fundamentally different direction that discards the prior image |
| `refine_image` | Any tweak or adjustment to a previously-generated image — preserves its composition and style |
| `upload_reference` | Collect reference photos from the user before generating (logos, product photos, headshots, etc.) |

## First-time generation workflow

### Step 1: Find an image prompt

Call `find_amplifiers` with the user's description and `kind: "prompt"` (or filter by `category: "Image Generation"`).

- "generate a logo" → `find_amplifiers({ query: "logo", kind: "prompt" })`
- "tiny objects" → `find_amplifiers({ query: "tiny objects", kind: "prompt" })`
- "/generate-image banana" → `find_amplifiers({ query: "banana", kind: "prompt" })`

Look for prompts with `type: "image"` in the result rows.

### Step 2: Select and start the interview

Call `use_prompt` with the chosen prompt's id. The server returns the template and the interview instructions tailored for the prompt (gallery path or direct generate path).

### Step 3: Reference image check

Before asking about placeholders, look at the prompt template body. If it references user-owned material ("your logo", "a photo of your product", "the user's headshot", "your pet", etc.), plan to call `upload_reference` after the text interview. Synthesize field names that match the user's own words when you can.

Do NOT call `upload_reference` if:
- The prompt is purely abstract or illustrative
- The user's description doesn't mention anything they'd have on hand
- You're unsure — in that case, ask in chat: *"Do you have a photo or logo you'd like me to incorporate?"*

### Step 4: Fill in placeholders

One placeholder at a time, natural conversational questions. Use hints in parentheses to offer options.

### Step 5: Collect references (if needed)

Call `upload_reference` with a `fields` array. Example:

```
upload_reference({
  fields: [
    { name: "logo", label: "Your logo", description: "PNG with transparent background preferred", required: true },
    { name: "product", label: "Product photo", required: true }
  ]
})
```

Wait for the tool result — the user's upload iframe will post a message back to chat with the uploaded URLs when done.

### Step 6: Generate

If the AIBMM prompt has a linked gallery, call `show_style_gallery` first; the gallery iframe handles the rest.

If not (no gallery), call `generate_image` directly with:
- `prompt`: the fully filled text (include references to uploaded images naturally in the prose — "the logo (first reference image) in the top-left, the product photo (second reference image) as the main subject")
- `prompt_id`: the UUID from the original prompt
- `image_urls`: URLs returned from `upload_reference`, flat in field order

## Refinement workflow

After a first image is generated, every user message is one of three things:

### A) Iterative refinement → `refine_image`

The user wants the same image, changed. Cues:
- Referencing current image properties: "make it bluer", "less contrast", "add a dog", "remove the text"
- Comparative language: "more dramatic", "less busy", "darker mood"
- Adjusting something already there

**Call `refine_image` with:**
- `refinement_base_url`: the `image_url` from the most recent image entry in the session's `history` array (returned in structuredContent)
- `prompt`: the user's instruction, lightly cleaned (see "Resolve references, not intent" below)
- `prompt_id`: from the structuredContent, if present
- `session_id`: from the structuredContent — always pass this to preserve session history

### B) Fresh direction → `generate_image`

The user is discarding the current look. Cues:
- Naming a new style/subject/genre: "make it cyberpunk instead", "actually a mountain scene"
- Explicit reset: "start over", "different approach", "new idea"

**Call `generate_image` with:**
- `prompt`: a freshly composed prompt combining the spirit of the structuredContent's `base_filled_prompt` with the new direction
- `prompt_id`: from the structuredContent, if present
- `session_id`: from the structuredContent — always pass this to preserve session history
- No `style_item_id`, no `image_urls`

### C) Conversational → no tool call

The user asked a question, changed topic, or said thanks. Handle conversationally.

### Ambiguous cases

*"What if it was at night?"* or *"try it with a cat instead of a dog"* sound pivot-y but are usually edits. **When in doubt, prefer `refine_image`** — it's cheaper and a wrong call is easy to recover from.

## Resolve references, not intent

When building the `prompt` for `refine_image`:

1. **Replace pronouns and references with concrete values from conversation history.** If the user says *"add the date of the article at the bottom right"* and the article was shared earlier with a publish date of March 15, 2025, rewrite to *"add 'March 15, 2025' at the bottom right"*. Same for *"use the name you mentioned"*, *"the colour from the logo above"*, *"their company tagline"*.

2. **Strip conversational filler.** *"Can you try making it less busy, maybe less yellow?"* → *"less busy, less yellow"*.

3. **Do NOT paraphrase or elaborate the edit intent itself.** If the user says *"more dramatic lighting"*, pass that through verbatim. Do not expand to *"harsher contrast, deep shadows, and a single directional key light"*. Gemini's image model handles natural-language edit directives well, and over-specification drifts from what the user asked for.

The only allowed rewriting is (a) reference resolution and (b) filler stripping.

## Reference images (mid-refinement)

If during refinement the user says *"now make it look more like this new photo"*, call `upload_reference` with a single field, wait for the upload, then call `refine_image` with:
- `refinement_base_url`: the prior image URL (unchanged)
- `image_urls`: the newly-uploaded URL
- `prompt`: the refinement instruction

Gemini receives both the base image and the new reference.

## Quota and access

- **Free tier** (logged in): 3 free image generations per month. Refinements count against the same bucket.
- **After quota**: user can add their own Gemini API key at https://auth.aiblewmymind.com (get a free one at https://aistudio.google.com/apikey)
- **PRO**: larger monthly quota

If the user hits a quota limit, explain the options clearly and help them set up their own key if they want to continue.

## Plugin-specific: local image paths

Because the plugin runs on the user's machine, you can pass local file paths in `image_paths` when calling `generate_image` (and `refine_image`). This is faster than the `upload_reference` flow for files the user already has on disk:

- `image_paths: ["/Users/alice/Desktop/logo.png"]` → read and passed to Gemini inline
- Combine with `upload_reference` if some references come from the user's clipboard and others from disk

The plugin also supports `image_base64` for the same purpose but paths are usually easier.

## Always search the library first

Never call `generate_image` directly with a raw prompt when the user's request could match an AIBMM template. Daria's prompts are engineered for Gemini and produce significantly better results than ad-hoc prompts. Call `find_amplifiers` immediately — don't ask the user for permission.

Exception: if the user explicitly wants ad-hoc generation ("just make me X, no templates"), skip the search.

## Example — full flow

User: *"Make a brand poster for my dog walking business. I have my logo and a photo of my dog."*

1. `find_amplifiers({ query: "brand poster", kind: "prompt" })` → find a relevant prompt
2. `use_prompt(id)` → get the interview instructions
3. Interview placeholders (business name, tagline, vibe, etc.)
4. `upload_reference({ fields: [{ name: "logo", label: "Your logo" }, { name: "dog_photo", label: "Photo of your dog" }] })`
5. User uploads both → URLs come back
6. `show_style_gallery(...)` if the prompt has a linked gallery, OR `generate_image(...)` directly with image_urls passed through and prose that references both images
7. User says *"make the dog bigger"* → `refine_image({ refinement_base_url: <latest image_url from structuredContent history>, session_id: <from structuredContent>, prompt: "make the dog bigger" })`
8. User says *"actually, make it cyberpunk instead"* → `generate_image({ prompt: "<rewritten cyberpunk version of base_filled_prompt>", session_id: <from structuredContent> })`
