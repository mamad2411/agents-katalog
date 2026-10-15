---
name: codex-app-changelog
description: >-
  Fetch, archive, translate, and render the latest OpenAI Codex App changelog
  from the official OpenAI Developers changelog page. Use when the user asks
  for Codex app release notes, Codex App changelog updates, desktop/mobile app
  updates, Codex app 最新版本, Codex App 更新日志, generate Codex App changelog
  images, draft a Xiaohongshu/rednote post about a Codex App update, or
  generate a Codex App release cover.
metadata:
  short-description: Archive, translate, render, and promote Codex App changelog entries
---

# Codex App Changelog

End-to-end workflow: pull the latest Codex App entry from OpenAI Developers, archive it bilingually, render BOTH the Chinese and the English versions as paste-ready PNG images (图2 / 图3 in the rednote layout), and optionally draft a Xiaohongshu post with a 3:4 cover.

## Paths & dependencies

This skill can be installed into different agent directories, so **its absolute location is not fixed** — do not assume a project-root path or any specific install prefix.

Throughout this document, `<skill-dir>` means **the directory that contains this SKILL.md** (the installed `codex-app-changelog/` folder). Resolve every relative path below against `<skill-dir>`, not against the current working directory. The bundled Python scripts self-locate — they find their own `scripts/`, `changelogs/`, and `assets/` siblings regardless of where the skill was installed — so as long as you invoke the correct script path, every output file lands in the right place automatically.

The cover step (Step 6) depends on a separate skill, **`zenmux-image-generation`**. If it is not installed, install it before running that step:

```bash
npx skills add ZenMux/skills --skill zenmux-image-generation
```

## Source

- Official changelog page: https://developers.openai.com/codex/changelog?type=codex-app
- Entry filter: only archive HTML entries whose `data-codex-topics` contains `codex-app`.

The page is the source of truth. It is not backed by a public GitHub release feed for Codex App, so this skill intentionally does not use `gh`, GitHub releases, or repository tags.

## Workflow

### 1. Fetch the latest Codex App entry

Prefer the helper script. It fetches the OpenAI Developers page, scans changelog list items, and selects the first entry tagged `codex-app`. Always run this upstream check first so the workflow knows the current latest Codex App entry before deciding whether local artifacts are duplicates.

```bash
uv run python <skill-dir>/scripts/fetch_latest_app_changelog.py --json
uv run python <skill-dir>/scripts/fetch_latest_app_changelog.py --save
```

Default output for `--save`:

```
<skill-dir>/changelogs/<version>.md
```

Use `--entry-id <id>` only when the user asks for a specific dated entry. Do not silently include `general` or `codex-cli` entries when the user asked for Codex App.

The `--json` output includes `existing_local_path` and `archive_status` when `changelogs/<version>.md` already exists. Treat `archive_status: "unchanged"` as the duplicate check result: reuse the local markdown and continue only with missing downstream artifacts.

### 2. Save English copy

The helper writes:

```markdown
---
version: "<version>"
entry_id: "<entry_id>"
title: "<upstream title>"
source: https://developers.openai.com/codex/changelog#<entry_id>
published: "<YYYY-MM-DD>"
fetched: <YYYY-MM-DD>
language: en
topic: codex-app
---

# Codex App <version>

## <upstream title>

<entry body converted from HTML to markdown>
```

If `--save` finds an existing file whose content matches apart from `fetched`, skip writing; if the entry content differs, overwrite only this version's files.

### 3. Produce Chinese translation

Write to `changelogs/<version>.zh.md`:

```markdown
---
version: "<version>"
entry_id: "<entry_id>"
title: "<upstream title>"
source: https://developers.openai.com/codex/changelog#<entry_id>
published: "<YYYY-MM-DD>"
fetched: <YYYY-MM-DD>
language: zh-CN
topic: codex-app
---

# Codex App <version>（中文版）

## <translated title>

<translated entry body>
```

If `changelogs/<version>.zh.md` already exists for the latest version, reuse it and skip translation unless the English archive changed or the user asks for a retranslation.

Translation rules:

- Keep technical identifiers untouched: app version numbers (`26.519`), CLI flags, env vars, config keys, commands, file paths, model names, protocol names, JSON field names, error names, keybindings.
- Translate prose: feature descriptions, bug fix explanations, UI behavior, and user-facing release notes.
- Prefer concise, technical Chinese — developer release notes, not marketing copy.
- Preserve bullet order one-to-one; do not merge or reorder.
- Use full-width punctuation `：` `，` `。` in prose; keep half-width inside code identifiers and URLs.
- Common mappings: "Fixed" -> "修复"; "Added" -> "新增"; "Changed" -> "变更"; "Improved" -> "优化"; "Performance improvements and bug fixes" -> "性能优化与问题修复".

### 4. Render changelog images (CN + EN, both required)

Produce dark-themed PNGs of BOTH the translated and upstream-English changelog so they can be pasted directly into chats, slides, or social posts. Always run this step after saving the `.md` and `.zh.md` files unless the user explicitly opts out — the rednote workflow assumes both images exist as 图2（中文版）+ 图3（英文原版）.

Run the renderer twice — once per language — and dispatch the two calls in parallel (independent inputs and outputs):

```bash
# Chinese
uv run --with playwright --with markdown \
  <skill-dir>/scripts/render_changelog.py \
  --input <skill-dir>/changelogs/<version>.zh.md

# English
uv run --with playwright --with markdown \
  <skill-dir>/scripts/render_changelog.py \
  --input <skill-dir>/changelogs/<version>.md
```

Outputs:

- `assets/rendered/<version>.zh.png` — Chinese, retina 2x, ~1600px (becomes 图2 in the rednote)
- `assets/rendered/<version>.png` — English, retina 2x, ~1600px (becomes 图3 in the rednote)

If `assets/rendered/<version>.zh.png` and `assets/rendered/<version>.png` already exist for the latest version, skip rendering. If only one image exists, render only the missing language. The renderer strips YAML frontmatter, removes `（中文版）` / `(中文版)` from the image title, converts markdown to HTML, and screenshots it with a dark theme.

First-time setup requires Chromium:

```bash
uv run --with playwright python -m playwright install chromium
```

### 5. Optional Xiaohongshu post

When the user asks for a rednote / 小红书 post about the update, create a short post directly from the Codex App changelog content. The output goes inside this skill's folder:

```
rednotes/codex-app-<version>.md
```

The body should be extremely short:

1. One natural Chinese sentence that summarizes the release and highlights the most important point(s). Write like a person, not a changelog index. Do not enumerate bullets.
2. A standalone reference line, exactly:

> 完整原版 ChangeLog 见图2（中文版）、图3（英文原版）。

Keep hashtags after the body when useful. The title should include the version number and may reuse the rednote cover title.

Example body shape:

```markdown
Codex App <version> 这版主要补上 <one key user-facing highlight>，顺带优化 <1-2 related details>，适合 <who should care / why it matters> 的开发者留意。

完整原版 ChangeLog 见图2（中文版）、图3（英文原版）。
```

The Xiaohongshu post is laid out as:

- 图1 -> cover generated via `$zenmux-image-generation` (prefer `assets/covers/<version>/<generated-or-returned-filename>.png` when bundling assets here)
- 图2 -> rendered Chinese changelog (`assets/rendered/<version>.zh.png`)
- 图3 -> rendered English changelog (`assets/rendered/<version>.png`)

Both rendered images are produced in Step 4, so the reference line is always accurate. Do not omit or paraphrase it.

### 6. Optional cover image

When the user asks for a cover / 头图 / poster, invoke `$zenmux-image-generation` and let that skill own image generation. Do not duplicate its current commands, setup steps, model routing, prompt-file format, confirmation rules, or troubleshooting details here.

This step requires the **`zenmux-image-generation`** skill. If `$zenmux-image-generation` is not available, install it with `npx skills add ZenMux/skills --skill zenmux-image-generation` before continuing. Do not attempt to hand-roll image generation without it.

Changelog-specific handoff brief:

- Goal: create a 3:4 portrait cover for OpenAI Codex App `<version>` as Xiaohongshu / rednote 图1.
- Literal text: include the rednote title and `Codex App <version>`; keep the version exact.
- Reference image: use `<skill-dir>/assets/openai.png` (the OpenAI logo bundled with this skill) as `[Image #1]`, and pass it to `$zenmux-image-generation` with `--reference-image <skill-dir>/assets/openai.png`. Place the OpenAI logo visibly but tastefully, preserving recognizable geometry and proportions as much as the model allows. Do not invent or fabricate an alternative OpenAI logo.
- Brand grounding: keep the OpenAI logo recognizable when it appears, but do not force every concept into monochrome, terminal UI, app-store screenshots, magazine covers, or any other fixed house style.
- Content grounding: before writing image prompts, distill the changelog into one sharp cover headline, 1-2 supporting phrases, 2-3 release-specific visual motifs, and one reason a developer should care. Do not make a generic "Codex App updated" poster when the release has a clearer product story.
- Creative concept requirement: write 4 fresh, content-driven cover concepts for this specific release. The four concepts must be meaningfully different in metaphor, composition, material / medium, color and light, and typography behavior.
- For each concept, produce a compact handoff brief containing `concept_title`, `style_slug`, `cover_headline`, `supporting_text`, `visual_metaphor`, `composition`, `material_palette`, `reference_usage`, and `generation_params`.
- `style_slug` must be filesystem-safe and prefixed with `concept-01-` through `concept-04-`.
- `generation_params`: `1024x1536`, `quality=high`, `-n 2`, and the intended output folder.
- Optimization requirement: after drafting the four concept briefs, hand them to `$zenmux-image-generation` and let that skill optimize each prompt using its current cookbook, model-selection, confirmation, and API workflow.
- Batch requirement: generate 4 sequential concept batches, 2 candidates per concept with `-n 2`, for 8 total candidates. Do not merge concepts into a grid or ask for all concepts inside one image.
- Output preference: save or place final cover assets under `<skill-dir>/assets/covers/<version>/<concept-slug>/` when bundling the rednote assets.
- After generation: report the output paths only. Do not rank, select, or recommend a final 图1 unless the user explicitly asks.
- Avoid: emoji, fake app screenshots, stock-photo people, malformed words, watermarks, invented logos, bland gradient backgrounds, busy small text, and multi-variant grids inside a single image.

### 7. Report

Output a short summary: version, source entry URL, saved file paths, rendered PNG paths, optional rednote/cover paths, and a one-line headline of what the release contains.

## Output locations

All paths below are relative to `<skill-dir>` (the installed `codex-app-changelog/` folder; its absolute prefix varies by agent).

```
<skill-dir>/
├── SKILL.md
├── scripts/
│   ├── fetch_latest_app_changelog.py       # OpenAI Developers page -> curated markdown
│   └── render_changelog.py                 # Markdown -> dark-themed PNG
├── assets/
│   ├── openai.png                          # Bundled OpenAI logo reference for cover handoff
│   ├── covers/
│   │   └── <version>/
│   │       ├── concept-01-<content-derived-slug>/
│   │       ├── concept-02-<content-derived-slug>/
│   │       ├── concept-03-<content-derived-slug>/
│   │       └── concept-04-<content-derived-slug>/
│   └── rendered/
│       ├── <version>.zh.png
│       └── <version>.png
├── changelogs/
│   ├── <version>.md
│   └── <version>.zh.md
└── rednotes/
    └── codex-app-<version>.md
```

Files are version-named so re-running the skill for the same release is idempotent.
Generated image folders (`assets/rendered/` and `assets/covers/`) are gitignored because they are reproducible local/social assets and can become large.
