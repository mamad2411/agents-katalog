---
name: ppt-deck-builder
description: Use when building or revising a PPT/演示文稿 in a portable, self-contained workflow folder, especially when the job spans storyline design, page briefs, page-level text compression, fixed-text image prompts, style-selectable slide image generation, sample-pack generation, page repair, and PPTX packaging without depending on repo files outside this skill folder.
version: 0.3.0
metadata:
  openclaw:
    requires:
      bins:
        - bash
        - python3
---

# PPT Deck Builder

This is a portable, single-folder PPT generation skill.
Everything needed by the workflow lives inside this skill folder: process guidance, references, templates, helper scripts, and packaging tools.

## Use When

- The user wants a reusable PPT production workflow that can be copied to another machine or repo.
- The user wants to build a new deck from notes, PDFs, spreadsheets, or an existing deck.
- The user wants to generate slide images with fixed text and package them into a `.pptx`.
- The user wants one skill folder instead of multiple linked skills.
- The user wants the image provider to stay replaceable so OpenClaw or another agent can switch providers later.
- The user wants to choose a visual direction such as dark blue business, light consulting, or whiteboard hand-drawn before generation.

## Do Not Use When

- The user only wants one sentence rewritten.
- The user only wants speaking advice, with no deck production.
- The user needs fully editable theme engineering beyond this workflow's image-based packaging path.

## Setup

Read `references/setup.md` before first use.
This workflow expects:
- `bash`
- `python3`
- `requests`
- `python-pptx`
- an image provider selected by CLI, plan file, or environment variable
- provider-specific environment variables only for the chosen provider

Before first generation:
- Ask whether a RunningHub API key is available.
- Default model is `rhart-image-n-g31-flash`.
- If no provider is specified, stay on `runninghub_g31`.

OpenClaw-safe paths use `{baseDir}`.
Plain shell usage still works from the root of this skill folder with `bash scripts/...`.

## Workflow Decision Tree

1. If the input is messy or vague, start with story design.
2. Choose one deck-level style preset or define a custom style direction before prompt writing.
3. If the page sequence exists, define the page type, page identity sentence, and reading path before prompt writing.
4. Compress page titles and visible text before adding style language.
5. If the deck is image-based, generate a small reference pack before the full batch.
6. If one page sets the desired visual standard, treat it as a style anchor for later pages when the provider supports reference images.
7. If text looks unstable, simplify the page before adding more visual detail.
8. After full-batch generation, build review contact sheets and inspect the whole deck.
9. If any page has text, layout, tone, or style-drift issues, rerun only that page and review again.
10. Package only after the full image set is reviewed and approved.

## Core Workflow

### 1. Define the deck job

- Identify audience, objective, and expected action.
- Choose a storyline pattern.
- Choose a deck-level style preset early. Default to a business presentation style unless the user explicitly wants a stronger style such as whiteboard hand-drawn.
- Reduce the deck to one message per page.
- Draft a page list with title, role, and key takeaway.

Read when needed:
- `references/story-patterns.md`
- `references/audience-and-goals.md`
- `references/style-presets.md`
- `references/workflow-playbook.md`

### 2. Build the page map

- Assign a page type to each page.
- Write one page identity sentence for each page such as `This is a Chinese client-facing PPT path page, not a poster.`
- Lock the deck style at the same time. Put style exceptions on the page only when a page genuinely needs to break the deck standard.
- Keep a clear reading order.
- Choose a visual job for the page: decision, diagnosis, path, matrix, rollout, results, or conclusion.
- Avoid dense structures before the narrative is stable.
- If the user wants a text-heavy image page, define the text regions before expanding the copy.

Read when needed:
- `references/page-types.md`
- `references/layout-patterns.md`
- `references/style-presets.md`
- `references/workflow-playbook.md`

### 3. Compress page language

- Shorten titles before writing prompts.
- Keep card titles short and stable.
- Prefer noun phrases over spoken-sentence titles.
- Remove repeated text and low-value labels.
- Decide what absolutely must appear as visible text.
- If the user wants higher information density, first decide where each sentence belongs before adding more text.
- Do not raise information density by repeating the same idea in both the diagram area and the footer area.
- Treat the page as an integrated text-and-background PPT page, not as a background image that will be fixed later.
- For Chinese image pages, prefer fewer but larger text groups over many scattered micro-labels.
- For whiteboard-style pages, reduce visible text even earlier and prefer 3-6 large handwritten groups instead of many tiny labels.

Use these local resources:
- `assets/page_brief_template.md`
- `references/prompt-rules.md`
- `references/workflow-playbook.md`

### 4. Build prompt-ready page plans

- Work one page at a time.
- Start each prompt with page identity and page type before style words.
- Carry the chosen `style_preset` into each page plan. Only use page-level style overrides when the deck needs a controlled exception.
- Fix the exact text lines allowed on the page.
- Map each text line to one region.
- State the reading path directly.
- Give each page a clear composition, not just a generic style.
- Keep provider choice separate from page story and layout decisions.
- Preserve the page's native structure when adding more text. A path page should stay a path page, a matrix page should stay a matrix page, and a comparison page should stay a comparison page.
- Keep the deck's primary business visual standard first.
- Use a light consulting-style layout with dark text only as a fallback when dense text remains blurry or repetitive after prompt repair.
- When a model supports richer text rendering, still avoid long paragraph blocks until a reference pack proves the layout is stable.
- If the chosen style is `whiteboard_handdrawn`, explicitly lock the whiteboard borders, zero room background, handwritten Chinese, hand-drawn illustration behavior, and mascot policy if any.

Use these local resources:
- `references/prompt-rules.md`
- `references/provider-adapters.md`
- `references/style-presets.md`
- `assets/slide_plan_template.json`
- `assets/page_brief_template.md`

### 5. Generate a reference pack first

Use a small sample to validate:
- text sharpness
- card consistency
- title wrapping
- reading order
- overall business tone
- style fidelity to the selected preset
- dense-page readability
- no repeated footer or summary text
- whether the page reads like a client-facing slide instead of a poster or training handout
- whether one approved page can act as a style anchor for later pages

OpenClaw-safe reference pack:
```bash
bash {baseDir}/scripts/run_reference_pack.sh plan.json output_dir
```

Plain shell from the skill root:
```bash
bash scripts/run_reference_pack.sh plan.json output_dir
```

### 6. Generate the full batch

Important:
- Do not stop after writing the plan file.
- Do not package a deck before slide images exist.
- If the user asked to actually generate a PPT, the workflow is not complete until image generation has run, the generated pages have been reviewed, and the deck has been packaged.

The image provider can be selected in this order:
1. Slide-level `image_provider`
2. CLI `--provider`
3. Plan-level `image_provider`
4. Environment variable `PPT_IMAGE_PROVIDER`
5. Default `runninghub_g31`

Notes:
- The built-in `runninghub_g31` adapter targets the RunningHub `rhart-image-n-g31-flash/text-to-image` path by default.
- If the backend should use reference images, image editing, or multi-image style anchoring, switch to `command` and let OpenClaw own that adapter logic.
- If the user wants strong cross-page style continuation such as a whiteboard course deck, prefer a sample-first workflow and treat one approved page as the style anchor for later reruns.

Built-in providers:
- `runninghub_g31`
- `command`

`command` is the generic escape hatch.
It lets OpenClaw or another agent replace the image backend without changing the main workflow script.

OpenClaw-safe full batch:
```bash
bash {baseDir}/scripts/run_image_batch.sh plan.json output_dir
```

Plain shell from the skill root:
```bash
bash scripts/run_image_batch.sh plan.json output_dir
```

OpenClaw-safe end-to-end generate + package:
```bash
bash {baseDir}/scripts/run_full_deck.sh plan.json output_dir deck.pptx
```

Plain shell from the skill root:
```bash
bash scripts/run_full_deck.sh plan.json output_dir deck.pptx
```

OpenClaw-safe single-page rerun:
```bash
bash {baseDir}/scripts/rerun_single_page.sh plan.json output_dir 8
```

### 7. Review the generated deck, then package

Check every page for wording accuracy, text sharpness, hierarchy, layout noise, repeated text, and client-facing business tone.
Do not treat generation success as delivery success.
Build review contact sheets, inspect the whole deck, rerun only the bad pages, and package only after the corrected image set is approved.

OpenClaw-safe contact sheet review:
```bash
python3 {baseDir}/scripts/build_contact_sheet.py output_dir
```

Plain shell from the skill root:
```bash
python3 scripts/build_contact_sheet.py output_dir
```

OpenClaw-safe single-page repair:
```bash
bash {baseDir}/scripts/rerun_single_page.sh plan.json output_dir 8
```

OpenClaw-safe packaging after review:
```bash
bash {baseDir}/scripts/package_image_deck.sh output_dir deck.pptx plan.json
```

Plain shell from the skill root:
```bash
bash scripts/package_image_deck.sh output_dir deck.pptx plan.json
```

Read when needed:
- `references/qa-checklist.md`

## Failure Recovery

- If the provider returns busy or queue-related failures, rerun a smaller sample with `max-workers=1`.
- If text quality drops, simplify the page, shorten titles, and rerun only that page.
- If the backend should change, switch to `command` instead of rewriting the deck workflow.
- If a page keeps failing, repair the story or prompt first, not the packaging step.
- If a page looks stylish but not presentation-ready, strengthen page identity, reading path, and text-region mapping before changing colors or effects.
- If a whiteboard-style page starts adding the wrong mascot, wrong title, or extra handwritten notes, tighten the exact text list and explicitly forbid replacement or summary text before rerunning that page.

## Local Tools In This Folder

- `scripts/generate_from_plan.py`
- `scripts/build_pptx_from_images.py`
- `scripts/run_reference_pack.sh`
- `scripts/run_image_batch.sh`
- `scripts/run_full_deck.sh`
- `scripts/rerun_single_page.sh`
- `scripts/package_image_deck.sh`
- `scripts/build_contact_sheet.py`
- `scripts/check_env.sh`
- `scripts/provider_command_template.py`
- `scripts/provider_mock_png.py`

## Guardrails

- One page should do one job.
- Prefer fewer, larger text groups in image-based pages.
- Shorten titles before prompting; do not hope the model will solve crowded copy.
- Give each page a composition job, not just a style direction.
- Define page identity and reading path before adding visual styling.
- Treat image pages as final text-and-background slides, not as background art to be fixed later.
- Approve a small reference pack before full-batch generation.
- Review the full generated deck before final delivery.
- Do not treat plan writing as deck generation.
- Do not package before validating that the expected slide images exist.
- Do not hide story problems with visual polish.
- Keep provider logic replaceable and isolated from the story and layout logic.
- Keep this folder self-contained when sharing it.
