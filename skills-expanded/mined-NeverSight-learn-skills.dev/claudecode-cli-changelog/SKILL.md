---
name: claudecode-cli-changelog
description: >-
  Fetch, archive, translate, and render the latest Claude Code changelog from
  the official GitHub CHANGELOG.md. Use when the user asks to pull Claude Code
  release notes, sync the latest version, save bilingual changelog markdown,
  create dark-themed changelog images, draft a Xiaohongshu/rednote post about a
  Claude Code update, or generate a 3:4 cover image. Trigger on phrases like
  "claude code changelog", "Claude Code 更新日志", "Claude Code 最新版本", "拉取
  changelog", "同步 Claude Code 更新", "生成 changelog 图片", "写 Claude Code
  小红书", or "生成 Claude Code 封面图".
metadata:
  short-description: Archive, translate, render, and promote Claude Code changelog entries
---

# Claude Code Changelog

End-to-end workflow: pull the latest Claude Code CHANGELOG entry, archive it bilingually, render BOTH the Chinese and the English versions as paste-ready PNG images (图2 / 图3 in the rednote layout), and optionally draft a Xiaohongshu post with a 3:4 cover.

## Paths & dependencies

This skill can be installed into different agent directories, so **its absolute location is not fixed** — do not assume a project-root path or any specific install prefix.

Throughout this document, `<skill-dir>` means **the directory that contains this SKILL.md** (the installed `claudecode-cli-changelog/` folder). Resolve every relative path below against `<skill-dir>`, not against the current working directory. The bundled Python scripts self-locate — they find their own `scripts/`, `changelogs/`, and `assets/` siblings regardless of where the skill was installed — so as long as you invoke the correct script path, every output file lands in the right place automatically.

The cover step (Step 7) depends on a separate skill, **`zenmux-image-generation`**. If it is not installed, install it before running that step:

```bash
npx skills add ZenMux/skills --skill zenmux-image-generation
```

## Source

- Upstream file: https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
- Browseable view: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md

The file uses semver-style headings (`## X.Y.Z`) in reverse chronological order — the FIRST heading is always the latest version.

## Workflow

### 1. Fetch

Fetch the raw CHANGELOG with `curl`, piping through `head -100` to cap payload size. The latest version heading is always at the top of the file, so the first 100 lines contain at minimum the latest entry (and usually the prior 1–2 entries for hotfix-check context):

```bash
curl -sSL https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md | head -100
```

Do not use `WebFetch` for this — the raw markdown is small, deterministic, and curl output drops straight into the parser without HTML-to-markdown rewriting. If 100 lines isn't enough (unusually long release), bump to `head -200`.

### 2. Extract latest version entry

Parse the first `## X.Y.Z` heading and capture every line until (but not including) the next `## ` heading.

- `<version>` = the string after `## ` on the first heading (e.g. `2.1.114`)
- `<body>` = the bullet lines that follow until the next version heading

When the latest version is a tiny hotfix, check the version immediately below it — often a richer release is one step behind. Offer the user the choice of (a) strictly latest, (b) broader previous version, or (c) merged summary of both.

After deciding the exact `<version>` or merged `<version-a>-<version-b>` bundle, check for an existing English archive for that selected version:

```bash
uv run python <skill-dir>/scripts/find_existing_changelog.py --version <version> --json
```

If this reports `"reused_local": true`, treat the local file as the duplicate check result: skip saving the English markdown and continue only with missing downstream artifacts. This check happens **after** fetching and extracting the latest upstream entry, never before.

### 3. Save English copy

Write to `changelogs/<version>.md`:

```markdown
---
version: <version>
source: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
fetched: <YYYY-MM-DD>
language: en
---

# Claude Code <version>

<body — upstream bullets verbatim>
```

If the selected version's English archive already exists and the fetched body matches, skip writing. If content differs, overwrite.

### 4. Produce Chinese translation

Write to `changelogs/<version>.zh.md`:

```markdown
---
version: <version>
source: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
fetched: <YYYY-MM-DD>
language: zh-CN
---

# Claude Code <version>（中文版）

<translated bullets>
```

If `changelogs/<version>.zh.md` already exists for the selected latest version or merged bundle, reuse it and skip translation unless the English archive changed or the user asks for a retranslation.

**Translation rules:**

- Keep technical identifiers untouched: CLI flags (`--foo`), settings keys (`sandbox.network.deniedDomains`), env vars (`CLAUDE_CODE_EXTRA_BODY`), tool/command names (`/loop`, `Bash`, `ToolSearch`), file paths, keybindings (`Ctrl+A`, `Shift+↑`), error codes.
- Translate prose: feature descriptions, bug fix explanations, user-facing behavior.
- Prefer concise, technical Chinese — match the style of developer release notes, not marketing copy.
- Preserve bullet order one-to-one; do not merge or reorder.
- Use full-width punctuation `：` `，` `。` in prose; keep half-width inside code identifiers.
- Common mappings: "Fixed" → "修复"；"Added" → "新增"；"Changed" → "变更"；"Improved" → "优化"；"Security" → "安全"。

### 5. Render the changelog as images (CN + EN, both required)

Produce dark-themed PNGs of BOTH the translated and the upstream-English changelog so they can be pasted directly into chats, slides, or social posts. Always run this step after saving the `.md` and `.zh.md` files unless the user explicitly opts out — the rednote workflow assumes both images exist as 图2（中文版）+ 图3（英文原版）.

Run the renderer twice — once per language — and dispatch the two calls in parallel (independent inputs and outputs):

```bash
# Chinese
uv run --with playwright --with markdown \
  <skill-dir>/scripts/render_changelog.py \
  --input <skill-dir>/changelogs/<version>.zh.md

# English (upstream verbatim)
uv run --with playwright --with markdown \
  <skill-dir>/scripts/render_changelog.py \
  --input <skill-dir>/changelogs/<version>.md
```

Outputs:

- `assets/rendered/<version>.zh.png` — Chinese, retina 2x, ~1600px (becomes 图2 in the rednote)
- `assets/rendered/<version>.png` — English, retina 2x, ~1600px (becomes 图3 in the rednote)

If `assets/rendered/<version>.zh.png` and `assets/rendered/<version>.png` already exist for the selected version or merged bundle, skip rendering. If only one image exists, render only the missing language.

The renderer:

1. Strips YAML frontmatter.
2. Extracts the first H1 and **removes `（中文版）` / `(中文版)` from the title** — the rendered image shows `Claude Code <version>` only. English files have no suffix to strip and render as-is.
3. Converts the body markdown to HTML with inline `code`, bullet lists, fenced blocks, tables.
4. Loads it in headless Chromium with a dark theme (`#17191c` bg, white text, `#2a2d31` code pills) and screenshots `full_page`.

First-time setup requires Chromium:

```bash
uv run --with playwright python -m playwright install chromium
```

Optional flags:

- `--output <path>` — override destination
- `--width <px>` — logical width (default 1600)
- `--scale <N>` — device pixel ratio (default 2 for retina)

### 6. (Optional) Draft a Xiaohongshu post

When the user asks for a rednote / 小红书 post about the update, create a short post directly from the changelog content. **The output goes inside this skill's folder**, not in rednote-generator's own published dir:

```
rednotes/claude-code-<version>.md
```

The body should be extremely short:

1. One natural Chinese sentence that summarizes the release and highlights the most important point(s). Write like a person, not a changelog index. Do not enumerate bullets.
2. A standalone reference line, exactly:

> 完整原版 ChangeLog 见图2（中文版）、图3（英文原版）。

Keep hashtags after the body when useful. The title should include the version number and may reuse the rednote cover title.

Example body shape:

```markdown
Claude Code <version> 这版主要修了 <one key user-facing or architecture-facing issue>，顺带补上 <1-2 related highlights>，属于 <who should care / why it matters> 的一次更新。

完整原版 ChangeLog 见图2（中文版）、图3（英文原版）。
```

The Xiaohongshu post is laid out as:

- 图1 → cover generated via `$zenmux-image-generation` (prefer `assets/covers/<version>/<generated-or-returned-filename>.png` when bundling assets here)
- 图2 → rendered Chinese changelog (`assets/rendered/<version>.zh.png`)
- 图3 → rendered English changelog (`assets/rendered/<version>.png`)

Both rendered images are produced in Step 5, so the reference line is always accurate. Do not omit or paraphrase it.

### 7. (Optional) Generate 3:4 cover image(s)

When the user asks for a cover / 头图 / poster, **invoke `$zenmux-image-generation` and let that skill own the image-generation workflow**. Do not duplicate its current commands, setup steps, model routing, prompt-file format, confirmation rules, or troubleshooting details here, because that skill is the source of truth and may change frequently.

This step requires the **`zenmux-image-generation`** skill. If `$zenmux-image-generation` is not available, install it with `npx skills add ZenMux/skills --skill zenmux-image-generation` before continuing. Do not attempt to hand-roll image generation without it.

This skill only supplies the changelog-specific handoff brief:

- Goal: create a 3:4 portrait cover for Claude Code `<version>` as Xiaohongshu / rednote 图1.
- Literal text: include the rednote title and `Claude Code <version>`; keep the version digits exact.
- Reference image: use `<skill-dir>/assets/claude.png` (bundled with this skill) as the Claude logo / wordmark reference.
- Brand grounding: keep the Claude identity recognizable when a logo / wordmark is used, but do **not** force every concept into Claude orange, a dark theme, terminal UI, editorial layout, workflow map, or any other fixed house style.
- Content grounding: before writing image prompts, distill the changelog into one sharp cover headline, 1-2 supporting phrases, 2-3 release-specific visual motifs, and one reason a developer should care. Do not make a generic "Claude Code updated" poster when the release has a clearer product story.
- Creative concept requirement: write **4 fresh, content-driven cover concepts** for this specific release. The four concepts must be meaningfully different in metaphor, composition, material / medium, color and light, and typography behavior. Invent the directions from the changelog itself; do not reuse a fixed style menu across releases.
- For each concept, produce a compact handoff brief containing:
  - `concept_title`: a memorable name derived from the release story.
  - `style_slug`: a filesystem-safe slug derived from the concept title, prefixed with `concept-01-` through `concept-04-`.
  - `cover_headline`: the exact short title to place on the cover.
  - `supporting_text`: 1-2 optional short phrases; keep text minimal.
  - `visual_metaphor`: the central image idea tied to the changelog.
  - `composition`: framing, focal object, depth, negative space, and text placement.
  - `material_palette`: color, texture, lighting, and medium choices; vary these across the four concepts.
  - `reference_usage`: how to use the Claude reference image, or when to omit it.
  - `generation_params`: `1024x1536`, `quality=high`, `-n 2`, and the intended output folder.
- Optimization requirement: after drafting the four concept briefs, hand them to `$zenmux-image-generation` and let that skill optimize each prompt using its current cookbook, model-selection, confirmation, and API workflow. This changelog skill should not hand-write final API prompts when `$zenmux-image-generation` can optimize them.
- Batch requirement: generate **4 sequential concept batches**, **2 candidates per concept** with `-n 2`, for 8 total candidates. Do not merge concepts into a grid or ask for all concepts inside one image.
- Output preference: save or place final cover assets under `<skill-dir>/assets/covers/<version>/<concept-slug>/`, preserving the image-generation skill's filenames unless the user asks for canonical names.
- After generation: report the output paths only. Do not rank, select, or recommend a final 图1 unless the user explicitly asks.
- Avoid: emoji, stock-photo people, cluttered fake app screenshots, malformed words, watermarks, bland gradient backgrounds, busy small text, and multi-variant grids inside a single image.

Operational rules:

- Follow `$zenmux-image-generation` exactly for prompt optimization, user confirmation, model choice, API invocation, references, output count, dependencies, and error handling.
- For this changelog cover workflow, request 4 sequential concept batches with `-n 2` each. Do not run the 4 batches in parallel unless each batch has a distinct output folder or otherwise cannot collide.
- If `$zenmux-image-generation` defaults change, use its current defaults rather than the older assumptions in archived changelog runs.
- If the generated files land in `$zenmux-image-generation`'s own output folder, report those paths and only copy or reorganize them into this skill's cover folder when the user asks or the current run explicitly needs the rednote asset bundle.

### 8. Report

Output a short summary: version, saved file paths (changelog EN/ZH + rendered PNG + optional rednote + optional cover), and a one-line headline of what the release contains.

## Output locations

All paths below are relative to `<skill-dir>` (the installed `claudecode-cli-changelog/` folder; its absolute prefix varies by agent).

```
<skill-dir>/
├── SKILL.md
├── scripts/
│   ├── find_existing_changelog.py          # Local archive duplicate check
│   └── render_changelog.py                 # Markdown → dark-themed PNG (Playwright)
├── assets/
│   ├── claude.png                          # Bundled Claude logo reference for cover handoff
│   ├── covers/
│   │   └── <version>/                      # Folder named by version
│   │       ├── concept-01-<content-derived-slug>/
│   │       ├── concept-02-<content-derived-slug>/
│   │       ├── concept-03-<content-derived-slug>/
│   │       └── concept-04-<content-derived-slug>/
│   └── rendered/
│       ├── <version>.zh.png                # Rendered Chinese changelog (图2 in rednote)
│       └── <version>.png                   # Rendered English changelog (图3 in rednote)
├── changelogs/
│   ├── <version>.md                        # English, upstream verbatim
│   └── <version>.zh.md                     # Chinese translation
└── rednotes/
    └── claude-code-<version>.md            # Xiaohongshu draft (if requested)
```

Files are version-named (not date-named) so re-running the skill for the same release is idempotent.
Generated image folders (`assets/rendered/` and `assets/covers/`) are gitignored because they are reproducible local/social assets and can become large.
