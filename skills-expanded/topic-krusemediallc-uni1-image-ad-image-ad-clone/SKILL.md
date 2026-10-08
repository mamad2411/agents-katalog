---
name: image-ad-clone
description: Use when the user wants to reverse-engineer an existing image ad into a reusable, parameterizable prompt template that can be reused with any brand and any product. Triggers on phrases like "clone this ad as a template", "reverse engineer this ad", "turn this ad into a prompt", "extract a template from this image", "make this ad reusable", "add this to my prompt library", "study this ad and make a template". Anchors on input being an EXISTING ad image the user provides — does NOT trigger for fresh ad generation requests (use uni1-image-ad for that).
---

# image-ad-clone

Take an existing image ad and turn it into a reusable, parameterizable uni-1 prompt template that can be plugged into any brand. Output: a new entry appended to the user's prompt library, ready to be used by `uni1-image-ad` (or anywhere else) on future generations.

This is the **template-creation** skill. The companion skill `uni1-image-ad` is the **template-using** skill (it generates and uploads ads from filled-in templates). They're meant to be installed together.

## Hard rules — never relax

1. **Strip platform/screenshot chrome from analysis.** When you describe what's in the reference, you're describing the actual ad creative, not the screenshot wrapper. Do not include iOS status bars, "Sponsored"/"Saved" badges, post text/captions surrounding the image, link-card footers, engagement rows, platform tab bars. If the reference is a screenshot of an ad-in-feed, mentally crop the wrapper. The output template must produce a standalone image that would be uploaded as a Meta creative.

2. **Always validate by generating.** A template that hasn't been round-tripped through uni-1 against the original isn't validated. Run at least one generation with `--image-ref <original>` and compare. Refine the prompt until the structure matches.

3. **Always test the generalized version.** Before saving, fill the placeholders with a *different brand* (use AG1 if the user has no preference — there's a known reference at `iterations/ag1-v2/T1-ios-notes/` or the user can supply one) and generate. If the structure breaks, the placeholder set is wrong — fix it.

4. **Never write brand-specific text into the final template.** Wordmarks, product names, slogans, specific photographs, hex colors specific to the source brand — all become `{placeholders}`. Only structural content (layout descriptions, photography style, typography family, composition rules) remains literal.

5. **Save to the user's library, do not silently overwrite.** Default save target is `~/.claude/skills/uni1-image-ad/references/prompt-library.md` if it exists; otherwise propose a project-local `prompt-library.md` and ask. If the target template name (e.g., `T8 — Apple Notes listicle`) collides with an existing entry, ask the user before overwriting.

## Inputs the user must provide

| Input | Notes |
|---|---|
| **Reference ad image** | Path to a local file (PNG/JPG/WEBP). The thing being reverse-engineered. |
| Brand to test against (optional) | If they want the test fill to use a specific brand. Default: AG1 if any AG1 assets exist at `ag1-assets/`, otherwise ask. |
| Save target (optional) | Defaults to `~/.claude/skills/uni1-image-ad/references/prompt-library.md`. |
| Template tag (optional) | Short identifier like `T8`, `Lifestyle Hero`, `Carousel Cover` — Claude proposes one based on the analysis if not given. |

## Workflow

### Phase 1: Preflight

1. The reference image path resolves to an existing file. If not, stop and ask.
2. `LUMA_API_KEY` is set in the project `.env`. If not, instruct the user how to get one.
3. The companion `generate_image.py` script is available. Look in this order:
   - `~/.claude/skills/uni1-image-ad/scripts/generate_image.py`
   - `<repo>/skills/uni1-image-ad/scripts/generate_image.py`
   - If neither: stop and ask the user to install `uni1-image-ad` (this skill's hard dependency).
4. Read the save target. If the file exists, read its current entries to know what tags are taken. If not, plan to create it.

### Phase 2: Visual analysis

This is the most important phase. Read the reference image and describe what you see, structurally separating brand-specific content from format/structure. Document each of these:

- **Aspect ratio.** Measure or estimate (W:H). Map to the closest Luma-supported ratio: `16:9, 1:1, 1:2, 1:3, 2:1, 2:3, 3:1, 3:2, 9:16`. (`4:5` and `1.91:1` are NOT supported — use `2:3` and `16:9` respectively.)
- **Format type.** What this ad pretends to be: editorial article, product flatlay, comparison table, fake search results, story composite, native UI mimic, etc.
- **Layout structure.** Header / hero / footer / grid — how regions are arranged.
- **Typography.** Family (geometric sans, condensed sans, serif, handwritten marker, monospace), weight, hierarchy. Do NOT name specific fonts unless they're iconic and necessary; instead describe the *feel*.
- **Color palette.** 3-6 hex codes. Identify which are brand-specific (will become `{brand.color_*}` variables) vs neutral/structural (white/black/grey backgrounds — stay literal).
- **Photography style.** Studio product flatlay, lifestyle UGC, editorial portrait, stock-photo-grid, etc. Describe lighting and lens.
- **Text content (verbatim).** Every visible string in the image. Mark which strings are *brand-specific* (e.g. "AG1", "Drink AG1") vs *structural* (e.g. "AS SEEN ON", "VS").
- **Decorative / non-text elements.** Icons, divider lines, badges, emojis, hand-lettering, sticky-note props.
- **Branded vs structural elements.** This is the key column. For everything you've described, mark each piece as `[BRAND]` (will become a variable) or `[STRUCTURE]` (stays literal in the template).
- **Chrome to strip.** Anything you saw that's a screenshot/platform artifact (iOS status bar, Sponsored badge, engagement row). Note it for explicit exclusion in the prompt.

State this analysis to the user as a compact summary. Don't move on until it's complete.

### Phase 3: Draft v1 prompt (faithful, brand-specifics intact)

Write a prompt that, paired with the reference image as `--image-ref`, would reproduce the ad faithfully. At this stage, leave brand-specific content **literal** — do not placeholder-ize yet.

Structure the prompt with these sections (omit any that don't apply):
- Aspect ratio + canvas (e.g. "1:1 static ad creative, 1080x1080, edge-to-edge")
- Background description
- Header section (top X% of the image)
- Main content / hero section
- Decorative elements (badges, dividers)
- Bottom section / footer band
- Typography note (weight, family-feel, hierarchy)
- Composition / spacing rules
- **Explicit chrome exclusion** — name what NOT to render (the script's no-chrome suffix is a safety net; the prompt should also explicitly exclude)

Show the v1 prompt to the user.

### Phase 4: Generate with reference

Use the discovered `generate_image.py` to fire one generation. Pass the original reference as `--image-ref` and the matched aspect ratio.

```bash
<path-to>/generate_image.py \
  --prompt "$(cat /tmp/v1.prompt)" \
  --aspect-ratio <matched_ratio> \
  --image-ref <reference_path> \
  --out iterations/clone-tmp \
  --env-file .env
```

(Write the prompt to a temp file to avoid shell-quoting hell.) Wait for completion (~50s with reference). Read the generated image.

### Phase 5: Compare and iterate

Show user the original side-by-side description with the generated. Identify deltas:
- Layout regions misplaced or missing
- Typography weight wrong
- Wrong aspect ratio interpretation
- Brand color drifted
- Decorative elements (icons, badges) wrong or missing

Refine the prompt based on the deltas. Regenerate. Repeat until the structure is faithful enough to call it "good." Cap at 4 iterations — beyond that, the prompt has a structural problem and needs more dramatic editing rather than tweaking.

### Phase 6: Generalize into placeholders

This is where the template becomes reusable. Walk back through the v1 prompt and replace every `[BRAND]`-marked element from Phase 2 with a `{placeholder}` variable. Use the standard placeholder vocabulary:

**Standard variables** (use these names where they fit):
- `{brand.name}` — wordmark text
- `{brand.color_primary}` — primary brand color hex (e.g. `#1A4731`)
- `{brand.color_accent}` — secondary accent color hex (if used)
- `{brand.product_image_description}` — one-line description of the product visible in the ad
- `{brand.tagline}` — short brand promise
- `{brand.competitor_category}` — for comparison templates: what's being compared against
- `{ad.headline}` — top-line headline copy
- `{ad.subcopy}` — sub-headline / supporting copy
- `{ad.body}` — primary text block
- `{ad.cta_phrase}` — CTA button text

**Template-specific variables** — name them clearly when needed:
- `{checklist_items[]}` (Notes-style)
- `{tweet_body}` (story templates)
- `{rows[]}` (comparison templates)
- `{publication}` (editorial templates)
- `{ugc_subject}` (UGC photo composite templates)

For each variable: write a 1-line description of what it represents and what kind of value goes in it.

### Phase 7: Test the generalized template

Pick a different brand (default AG1 if assets exist; otherwise ask). Substitute test values into every placeholder. Generate again with `--image-ref` set to the test brand's product photo (NOT the original ad). The output should:
1. Have the same layout/composition as the original
2. Show the test brand instead of the source brand
3. Read as a coherent ad, not a frankenstein

If the test fails the structure breaks under different brand assumptions, return to Phase 6 and refine the placeholder set. Often the fix is making a placeholder that was missed (e.g. you hardcoded a font feel that's specific to one brand).

### Phase 8: Document the template

Compose the library entry. Use the format in `references/template-format.md` — it has the markdown skeleton.

The entry must include:
- **Tag and one-line title** (e.g. `T8 — Lifestyle hero with overlay text`)
- **When to use** — 1-2 sentences on positioning fit
- **Aspect ratio** recommendation
- **Reference image guidance** — what kind of `--image-ref` to pass when reusing this template (product hero? logo? lifestyle portrait?)
- **Variable schema** — every `{placeholder}` with a 1-line description
- **Template prompt** in a fenced code block, ready to copy-paste-fill
- **Example fill** — the test fill from Phase 7, showing the variables substituted
- **Validated example path** — pointer to the iteration dir (e.g. `iterations/clone-2026-05-04/T8/`)

### Phase 9: Save and confirm

1. Append the entry to the configured library file. If overwriting an existing tag, ask first.
2. Print the entry's path so the user can review.
3. Move the validated PNGs from `iterations/clone-tmp/` to a permanent dir keyed by the template tag (e.g. `iterations/clone-2026-05-04/T8/`).
4. Tell the user the template is now available for use by `uni1-image-ad`. Suggest a follow-up: *"Want me to make a real ad with this template right now?"*

## Naming convention for new templates

If the save target already has T1–T7 (the seeded templates), continue with T8, T9, … Use semantic suffixes if helpful: `T8 — Lifestyle hero`, `T9 — Carousel cover`. Keep the `T<n>` part for cross-skill referencing.

## Out of scope

- **Generating real ads / uploading to Meta.** That's `uni1-image-ad`. This skill produces templates, period.
- **Reverse-engineering video ads.** Image only. Refuse with: *"This skill is for static image ads. Video reverse-engineering isn't supported in this version."*
- **Multi-template extraction in one run.** One reference → one template per skill invocation. If the user has 5 references, do 5 sequential runs (or batch via the same flow once you've done one).
- **Modifying existing templates in the library.** If the user wants to revise T3, treat it as a new run pointed at the same library entry — show the diff and ask before overwriting.

## Files this skill owns

- `~/.claude/skills/image-ad-clone/SKILL.md` — this file
- `~/.claude/skills/image-ad-clone/references/template-format.md` — load this in Phase 8 before composing the library entry
- `<cwd>/iterations/clone-<date>/<tag>/` — per-run iteration outputs (gitignored PNGs, kept prompts)

## Files this skill writes to (in user space)

- The configured prompt library (default: `~/.claude/skills/uni1-image-ad/references/prompt-library.md`) — appended, never silently overwritten
- `<cwd>/iterations/clone-<date>/<tag>/prompt.txt` — the final validated prompt
- `<cwd>/iterations/clone-<date>/<tag>/v1.png`, `v2.png`, … — each iteration's output

## Dependencies

- The `uni1-image-ad` skill must be installed (this skill uses its `generate_image.py` for iteration). If not installed, fail Phase 1 with a clear instruction.
- `LUMA_API_KEY` in `.env`.
- Python 3.12+ (for the helper script).
