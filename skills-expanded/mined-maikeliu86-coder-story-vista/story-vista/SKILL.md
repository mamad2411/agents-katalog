---
name: story-vista
description: Build a multilingual, spoiler-safe Reader Visual Codex from complex novels and long-form story text.
---

# StoryVista | Reader Visual Codex

## Mission

Turn complex novels into multilingual visual reading companions: characters, aliases, relationships, locations, maps, objects, lore, highlighted source text, and spoiler-safe evidence.

## Required Inputs

- UTF-8 source text
- output directory
- optional `--ui-language auto|en|zh-CN|...`
- optional `--spoiler-mode safe|full`
- optional explicit visual provider or manual assets

## Install

From a cloned StoryVista repository, create a self-contained Skill directory:

```bash
python3 scripts/install_skill.py --target ~/.codex/skills/story-vista
```

The target must not already exist. The installer copies the Skill instructions, Python runtime, templates, locales, and referenced docs without copying local outputs or credentials. For another Agent, replace the target with that Agent's Skill directory.

## Run

```bash
# From the repository or the installed Skill directory:
python scripts/storyvista.py build input.txt --out output/story --ui-language auto
python scripts/storyvista.py export-prompts output/story --provider jimeng
python scripts/storyvista.py bind-images output/story --assets output/story/assets/generated
python scripts/storyvista.py rebuild-atlas output/story
python scripts/storyvista.py validate output/story
```

## Required Outputs

Create source/chunk indexes, language profile, reader text, entity links, character atlas, relationship web, location atlas, map plan, object/lore codex, visual evidence, visual asset plan, image manifest, spoiler state, provider state, theme profile, provider prompt files, manual generation instructions, actionable image-generation tasks, semantic display fallbacks, `atlas.html`, and `verification-report.md`.

## Product Experience Contract

The final `atlas.html` is the primary product. It should feel like an immersive visual reading atlas: a game codex, worldbuilding archive, or film concept dossier. Lead with story-facing surfaces such as character roster, relationship field, location/map surface, object and lore cards, event timeline, and reader evidence.

Provider diagnostics, fallback status, validation details, prompt packs, and schema contracts are support systems. Keep them available, but do not let them dominate the final reader-facing page.

Use `docs/product-experience-contract.md` and `docs/golden-reference.md` as the experience baseline.

## Language And Locale Rules

- Detect input language and script.
- Detect or accept UI language independently.
- Preserve canonical names and original spelling.
- Add localized labels only when useful; do not force-translate proper nouns.
- Apply language-specific alias rules conservatively.
- Mark uncertain alias merges ambiguous.
- Use English visual prompts by default unless explicitly changed.
- Load interface labels from locale files.
- Record language assumptions and locale status in verification.
- `en` and `zh-CN` are supported; other bundled locales are experimental.

## Core Pipeline

1. Run provider preflight; missing providers are not fatal.
2. Ingest and chunk source text with stable offsets.
3. Detect language, script, name system, and UI locale.
4. Set reader progress and spoiler-safe state.
5. Detect genre/atmosphere and create a spoiler-free theme profile.
6. Extract characters, places, organizations, objects, lore, relations, and events.
7. Resolve full names, titles, surnames, nicknames, and aliases conservatively.
8. Build character visual profiles and relationship/location/object codex data.
9. Build interpretive map data without inventing exact geography.
10. Build visual evidence with confirmed/contextual/inferred/unknown status.
11. Build reader paragraphs and entity links.
12. Create visual asset plan before image manifest or atlas rendering.
13. Export provider-specific prompts and expected filenames.
14. Bind direct, externally generated, or user-provided real assets when available.
15. If no image provider is callable, output a structured `Image Generation Task List` and use semantic fallbacks only as temporary display surfaces.
16. Render localized `atlas.html` with generation status, prompt actions, Reader Sync, and bidirectional jumps.
17. Validate every contract and write the verification report.

## Spoiler Rules

- Default to `safe` mode.
- Hide details marked `locked`.
- Do not place later revelations in portraits, backgrounds, summaries, or alt text.
- Full mode requires explicit user choice.

## Visual Provider Preflight

- Inspect configuration signals without printing secrets.
- A configured key is not a verified callable provider.
- Explicit user selection wins.
- Never auto-install providers, create accounts, or make paid calls.
- Before visual generation, confirm or detect whether an image model is available, whether an API key exists, whether a local service is running, whether the output directory is writable, whether rate limits are likely, and whether the user wants a text-first atlas before batch image generation.
- Provider priority: user-specified model, callable Image2, available SeeDream for mainland/cloud workflows, local ComfyUI/Flux/SDXL, then structured task list.
- Fallback order: configured direct/local provider, external manual generation, prompt pack, structured task list, semantic display fallback.
- Keep Jimeng, Jianying Jimeng, ByteDance Seedream, and Volcengine Seedream as distinct registry entries.
- Default prompt style is `creative-balanced`; `evidence-strict` and `cinematic-free` remain available planning modes.

## Image Generation Safety Rules

When no usable image model is detected, StoryVista must explicitly tell the user that no callable image model is available and list practical options: Image2, SeeDream, ComfyUI, Flux, SDXL, or another cloud/local model.

Forbidden behavior:

- generating blank placeholders as final image results
- inserting nonexistent image links
- pretending images were generated
- using broken image URLs
- using "image generation in progress" as a replacement for a real result
- outputting placeholders with no usable generation prompt

StoryVista must not treat image-link placeholders as completion. It must prioritize usable output: generate real images when possible, otherwise provide high-quality prompts and explain the unavailable provider state.

## Image Generation Task List Format

When direct generation is unavailable, include this table:

| ID | Type | Title | Source Basis | Prompt | Negative Prompt | Recommended Provider | Aspect Ratio | Priority |
|---|---|---|---|---|---|---|---|---|
| image_001 | character/location/object/event | Short asset title | Source paragraph, scene, or evidence note | Copy-ready visual prompt | Exclusions and spoiler limits | Image2 / SeeDream / ComfyUI / Flux / SDXL / other | 16:9 / 4:5 / 1:1 | high/medium/low |

## Theme Engine

- Derive theme from source motifs, not from unsupported plot assumptions.
- Keep backgrounds atmospheric, text-free, character-free, and spoiler-free.
- Record theme ID, palette, motifs, confidence, and background prompt.

## Reader Sync And Entity Jump

- Render source paragraphs with stable IDs.
- Highlight resolved characters, locations, organizations, objects, and lore.
- Clicking a highlight opens the matching codex entry.
- Clicking evidence opens the Reader panel and scrolls to the source paragraph.
- Persist reader open state, width, progress, font size, and line height locally.

## Fallback Rules

- Missing provider: tell the user no callable image model is available, create an actionable prompt workflow, output a structured task list, and continue with semantic SVG only as the temporary display fallback.
- Missing visual fact: use `unknown`, not invention.
- Ambiguous alias: keep candidates and report ambiguity.
- Missing geography: use interpretive map with a disclaimer.
- Missing locale key: fall back to English and keep experimental status.
- Never use initials-only avatars by default.

## Verification Checklist

- All required JSON/HTML files exist and parse.
- Major characters have portrait, half-body, and first-scene plans.
- Locations, map, objects/lore, and background have plans.
- Every asset has a unique manifest record and existing fallback file.
- Relation endpoints resolve and spoiler locks are preserved.
- Reader links resolve to both entities and paragraphs.
- Theme and locale are embedded in the atlas.
- Desktop and mobile Reader layouts are usable.
- No unsupported language or agent runtime is called fully supported.
- No missing-provider path claims image generation succeeded.
- Every ungenerated image has a usable task-list row with source basis, prompt, negative prompt, provider recommendation, aspect ratio, and priority.

## Final Response

Report output path, selected provider/fallback, input/UI language, theme, spoiler mode, test result, warnings, and known limitations.

Actor, writer, and director modes are future extensions, not core workflow steps.
