---
name: scientific-figure
description: Generate or edit scientific illustration drafts with OmniScholar, including reference-guided and multi-reference work, or use Ai4Scholar for its declared figure actions. Use for mechanisms, graphical abstracts, workflows, apparatus diagrams, concept art, critique, or vectorization.
license: MIT
---

# Scientific figure workflow

Follow the user's language. Generated content is an illustration draft, never experimental evidence or measured data.

## Define the figure contract

Confirm the scientific message, audience, figure type, required entities and labels, causal arrows, units, language, aspect ratio, background, output format, and whether reference images may leave the machine. Ask only when an assumption would change scientific meaning, privacy, cost, or layout.

## Route by declared capability

1. Call `omnischolar_image_models` with discovery enabled and use only descriptors where `usable=true` and the exact requested capability is declared. Preserve the provider/model choice in the request; if several discovered models are valid but differ in cost, quality, or modality, ask the user to choose. If the user does not choose, prefer the newest usable model for the task.
2. A catalog-visible model with no declared capability remains unusable. Never infer text-to-image, edit, or multi-reference support from a model name.
3. Use `omnischolar_image_generate` for text-to-image or declared image-to-image generation.
4. Use `omnischolar_image_edit` for edit operations; multiple references require an explicit `multi-reference` declaration.
5. Use `ai4scholar_figure` only for its declared actions and configured credentials.
6. Use `omnischolar_image_service` with `action=status` for local configuration status or `action=job` only when a configured provider exposes that job contract.

Pass common image controls using the tool's normalized names only when the selected model descriptor lists them in `supported_parameters`. The current official parameter matrix is:

| Provider/API | Supported normalized parameters | Do not assume |
|---|---|---|
| OpenAI GPT Image | `size`/`resolution`, `background`, `outputFormat`, `quality`, `n` | `aspectRatio` is not a separate native control; use `size` |
| Google Gemini API Interactions | `aspectRatio`, `resolution` (`1K`/`2K`), `outputFormat` | `size`, `background`, `quality`, `n`, `seed` |
| Vertex Gemini image | `aspectRatio`, `resolution` (`1K`/`2K`/`4K`), `outputFormat`, `n` | transparent background and arbitrary pixel `size` |
| Fal Nano Banana 2 | `aspectRatio`, `resolution`, `outputFormat`, `n`, `seed` | `background` and `quality` unless the selected Fal model declares them |
| Fal GPT Image variants | `size`/`resolution`, `background`, `outputFormat`, `quality`, `n` | Nano Banana-specific controls |
| DashScope/Qwen native image | `size`/`resolution`, `n`, `negativePrompt`, `seed` | `background`, `quality`, transparent output |
| Atlas model endpoints | follow the selected model's descriptor; GPT Image commonly exposes `size`, `quality`, `outputFormat` | a provider-wide parameter contract |

Adapters translate supported controls to native names. Unsupported controls must be omitted or reported as `parameter_unsupported`; do not silently drop them. Text-to-image, image-to-image, edit, transparency, aspect ratio, resolution, and batch count are separate capability checks; never infer one from another. Providers without a model-list endpoint must expose only versioned, provider-verified fallback models. `Atlas` and other custom endpoints need an explicit model contract and are never populated by guesses.

Custom providers make a best-effort probe of `baseUrl/models` when no `modelCatalogEndpoint` is configured. A returned model without explicit capability metadata remains unusable until its capability is declared in the configuration; providers without a model-list endpoint fall back to explicit model contracts.

Multiple custom profiles may use distinct provider names with `providerType: "custom"`. Read each selected model's declared `supportedParameters`; for common OpenAI-compatible profiles these may include `size`, `resolution`, `background`, `outputFormat`, `quality`, and `n`, but do not assume all downstream profiles support every control.

Fal image calls default to the provider's documented `sync_mode=true`, so returned data can be saved locally without downloading a result CDN URL. Pass `options.sync_mode=false` only when the selected endpoint requires the normal hosted-URL queue flow.

If the chosen provider is absent, disabled, lacks credentials, lacks entitlement, or has no usable capability pin/curated descriptor, stop and report the exact blocker. Offer another configured provider only after confirming the same capability and informing the user. Atlas and custom providers require explicit endpoint/model contracts. Do not treat a successful model listing as generation entitlement.

The generated configuration enables provider sections by default, but a provider still needs its credential and a usable capability descriptor. Do not ask the user to disable unrelated providers; report only the missing credential or contract for the selected provider.

## Upload and cost

- Paid generation requires an enabled provider with a configured credential.
- Reference images require an enabled provider with a configured credential; local references must still be inside configured workspace roots.
- Use only user-authorized or Agent-generated references. Never substitute a private image.
- Start with one economical image and the smallest useful dimensions. Do not blindly retry an ambiguous paid submission.
- Provider URLs and task identifiers are transport details; use saved local artifacts and do not expose signed URLs.

## Prompt and review

Specify subject/claim, composition, scientific constraints, visual language, output constraints, and exclusions. Prefer deterministic plotting code for quantitative charts, spectra, microscopy measurements, diffraction traces, and axes.

After generation, inspect spelling, notation, units, molecular/crystal geometry, arrows, legends, scale bars, panel order, and hallucinated details. State whether deterministic finishing or domain-expert review is still required.
