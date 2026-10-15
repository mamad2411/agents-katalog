---
name: codex-cli-changelog
description: >-
  Fetch, filter, archive, translate, and render the latest OpenAI Codex CLI
  changelog from the official GitHub releases page. Use when the user asks for
  Codex CLI release notes, Codex CLI changelog updates, the latest Codex CLI
  version, Codex CLI 更新日志, Codex CLI 最新版本, generate Codex CLI changelog
  images, draft a Xiaohongshu/rednote post about a Codex CLI update, or
  generate a Codex CLI release cover. It intentionally skips prereleases and
  rejects GitHub auto-generated PR-list release notes unless the user
  explicitly asks for them.
metadata:
  short-description: Archive, translate, render, and promote Codex CLI GitHub release notes
---

# Codex CLI Changelog

End-to-end workflow: pull the latest usable OpenAI Codex CLI GitHub release, archive it bilingually, render BOTH the Chinese and the English versions as paste-ready PNG images (图2 / 图3 in the rednote layout), and optionally draft a Xiaohongshu post with a 3:4 cover.

Codex CLI differs from Claude Code: there is no single upstream `CHANGELOG.md` to slice. The source of truth is the `openai/codex` GitHub releases feed, and this skill must filter release metadata carefully.

For Codex App changelog entries from OpenAI Developers, use `$codex-app-changelog` instead. Do not mix App page entries into this CLI GitHub-release workflow.

## Paths & dependencies

This skill can be installed into different agent directories, so **its absolute location is not fixed** — do not assume a project-root path or any specific install prefix.

Throughout this document, `<skill-dir>` means **the directory that contains this SKILL.md** (the installed `codex-cli-changelog/` folder). Resolve every relative path below against `<skill-dir>`, not against the current working directory. The bundled Python scripts self-locate — they find their own `scripts/`, `changelogs/`, and `assets/` siblings regardless of where the skill was installed — so as long as you invoke the correct script path, every output file lands in the right place automatically.

The cover step (Step 6) depends on a separate skill, **`zenmux-image-generation`**. If it is not installed, install it before running that step:

```bash
npx skills add ZenMux/skills --skill zenmux-image-generation
```

## Source

- Browseable releases: https://github.com/openai/codex/releases
- GitHub CLI latest full release: `gh api repos/openai/codex/releases/latest`
- GitHub CLI release list scan: `gh api 'repos/openai/codex/releases?per_page=30'`

GitHub's latest-release endpoint returns the latest published full release, not drafts or prereleases. Still apply this skill's extra filters because the Codex repo may also publish dependency/tooling releases, prerelease-like names, or GitHub-generated PR rollups.

This skill intentionally uses `gh` only. Do not fall back to `curl`, `WebFetch`, browser scraping, or a direct Python HTTP client. If `gh` auth is missing or expired, stop and ask the user to run `gh auth login -h github.com` or provide `GH_TOKEN`.

## Hard Rules

- Only use OpenAI's `openai/codex` GitHub releases as the Codex CLI source.
- Do not archive releases marked `draft: true` or `prerelease: true`.
- Do not archive tag/name patterns containing `alpha`, `beta`, `rc`, `pre`, `preview`, `nightly`, `snapshot`, or `canary`.
- Do not archive dependency-only releases such as `rusty-v8-*`.
- Do not convert auto-generated PR lists into a user-facing changelog. If the body is only `What's Changed`, `New Contributors`, `Full Changelog`, PR numbers, and usernames, skip it and scan older releases.
- If the release body has a curated section before generated PR notes, keep the curated section and strip the generated sections.
- If no usable non-prerelease, non-generated CLI release exists in the scanned window, stop and report that no publishable Codex CLI changelog was found.

## Workflow

### 1. Fetch latest usable CLI release

Prefer the helper script. It invokes `gh api` as the only GitHub access path, tries `/releases/latest`, then scans recent releases with `gh api` if the latest body is unusable because it is empty, dependency-only, prerelease-like by name, or only GitHub-generated PR notes. Always run this upstream check first so the workflow knows the current latest usable version before deciding whether local artifacts are duplicates.

```bash
uv run python <skill-dir>/scripts/fetch_latest_release.py --json
uv run python <skill-dir>/scripts/fetch_latest_release.py --save
```

Default output for `--save`:

```
<skill-dir>/changelogs/<version>.md
```

Use `--max-pages <N>` if the recent release list is unusually noisy. Use `--allow-generated` only if the user explicitly asks to keep PR-generated notes.

The `--json` output includes `existing_local_path` and `archive_status` when `changelogs/<version>.md` already exists. Treat `archive_status: "unchanged"` as the duplicate check result: reuse the local markdown and continue only with missing downstream artifacts.

If `gh` authentication is missing or expired, do not switch tools. Ask the user to authenticate:

```bash
gh auth login -h github.com
# or
GH_TOKEN=<token> uv run python <skill-dir>/scripts/fetch_latest_release.py --save
```

### 2. Save English copy

The helper writes:

```markdown
---
version: <version>
tag: "<tag_name>"
source: https://github.com/openai/codex/releases/tag/<tag>
published: "<published_at>"
fetched: <YYYY-MM-DD>
language: en
generated_notes_handling: "<ok | kept curated sections and removed generated PR notes>"
---

# Codex CLI <version>

<release body, with generated PR sections removed>
```

If the helper output still says `# Codex <version>` because it came from an older script, normalize the saved H1 to `# Codex CLI <version>` before translating/rendering. If `--save` finds an existing file whose content matches apart from `fetched`, skip writing; if the release content differs, overwrite only this version's files.

### 3. Produce Chinese translation

Write to `changelogs/<version>.zh.md`:

```markdown
---
version: <version>
tag: "<tag_name>"
source: https://github.com/openai/codex/releases/tag/<tag>
published: "<published_at>"
fetched: <YYYY-MM-DD>
language: zh-CN
---

# Codex CLI <version>（中文版）

<translated release body>
```

If `changelogs/<version>.zh.md` already exists for the latest version, reuse it and skip translation unless the English archive changed or the user asks for a retranslation.

Translation rules:

- Keep technical identifiers untouched: CLI flags, env vars, config keys, commands, file paths, model names, protocol names, JSON field names, error names, keybindings.
- Translate prose: feature descriptions, bug fix explanations, user-facing behavior.
- Prefer concise, technical Chinese — developer release notes, not marketing copy.
- Preserve bullet order one-to-one; do not merge or reorder.
- Use full-width punctuation `：` `，` `。` in prose; keep half-width inside code identifiers and URLs.
- Common mappings: "Fixed" -> "修复"; "Added" -> "新增"; "Changed" -> "变更"; "Improved" -> "优化"; "Security" -> "安全"; "TUI" stays `TUI`; "MCP" stays `MCP`.

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

When the user asks for a rednote / 小红书 post about the update, create a short post directly from the curated Codex CLI changelog content. The output goes inside this skill's folder:

```
rednotes/codex-cli-<version>.md
```

The body should be extremely short:

1. One natural Chinese sentence that summarizes the release and highlights the most important point(s). Write like a person, not a changelog index. Do not enumerate bullets.
2. A standalone reference line, exactly:

> 完整原版 ChangeLog 见图2（中文版）、图3（英文原版）。

Keep hashtags after the body when useful. The title should include the version number and may reuse the rednote cover title. Do not summarize generated PR lists. If the source body was rejected as PR-generated, do not write a rednote from it.

Example body shape:

```markdown
Codex CLI <version> 这版主要修了 <one key user-facing or architecture-facing issue>，顺带补上 <1-2 related highlights>，属于 <who should care / why it matters> 的一次更新。

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

- Goal: create a 3:4 portrait cover for OpenAI Codex CLI `<version>` as Xiaohongshu / rednote 图1.
- Literal text: include the rednote title and `Codex CLI <version>`; keep the version exact.
- Reference image: use `<skill-dir>/assets/openai.png` (the OpenAI logo bundled with this skill) as `[Image #1]`, and pass it to `$zenmux-image-generation` with `--reference-image <skill-dir>/assets/openai.png`. Place the OpenAI logo visibly but tastefully in the poster, preserving its recognizable geometry and proportions as much as the model allows. Do not invent or fabricate an alternative OpenAI logo.
- Brand grounding: keep the OpenAI logo recognizable when it appears, but do not force every concept into monochrome, terminal UI, architecture diagrams, magazine covers, or any other fixed house style.
- Content grounding: before writing image prompts, distill the changelog into one sharp cover headline, 1-2 supporting phrases, 2-3 release-specific visual motifs, and one reason a developer should care. Do not make a generic "Codex CLI updated" poster when the changelog has a stronger story.
- Creative concept requirement: write 4 fresh, content-driven cover concepts for this specific release. The four concepts must be meaningfully different in metaphor, composition, material / medium, color and light, and typography behavior.
- For each concept, produce a compact handoff brief containing:
  - `concept_title`: a memorable name derived from the release story.
  - `style_slug`: a filesystem-safe slug derived from the concept title, prefixed with `concept-01-` through `concept-04-`.
  - `cover_headline`: the exact short title to place on the cover.
  - `supporting_text`: 1-2 optional short phrases; keep text minimal.
  - `visual_metaphor`: the central image idea tied to the changelog.
  - `composition`: framing, focal object, depth, negative space, and text placement.
  - `material_palette`: color, texture, lighting, and medium choices; vary these across the four concepts.
  - `reference_usage`: how to use the bundled OpenAI logo reference without turning the cover into a generic brand poster.
  - `generation_params`: `1024x1536`, `quality=high`, `-n 2`, and the intended output folder.
- Optimization requirement: after drafting the four concept briefs, hand them to `$zenmux-image-generation` and let that skill optimize each prompt using its current cookbook, model-selection, confirmation, and API workflow. This changelog skill should not hand-write final API prompts when `$zenmux-image-generation` can optimize them.
- Batch requirement: generate 4 sequential concept batches, 2 candidates per concept with `-n 2`, for 8 total candidates. Do not merge concepts into a grid or ask for all concepts inside one image.
- Execution note: use `1024x1536` with `quality=high` for the default OpenAI Codex CLI rednote cover. Run the 4 concept batches sequentially with `-n 2` each, or use distinct output folders per concept if the image-generation skill supports that. Avoid parallel same-folder runs because timestamp-based filenames can collide.
- Output preference: save or place final cover assets under `<skill-dir>/assets/covers/<version>/<concept-slug>/` when bundling the rednote assets.
- After generation: report the output paths only. Do not rank, select, or recommend a final 图1 unless the user explicitly asks.
- Avoid: emoji, fake GitHub screenshots, stock-photo people, malformed words, watermarks, invented logos, bland gradient backgrounds, busy small text, and multi-variant grids inside a single image.

Operational rules:

- Follow `$zenmux-image-generation` exactly for prompt optimization, user confirmation, model choice, API invocation, references, output count, dependencies, and error handling.
- For this changelog cover workflow, request 4 sequential concept batches with `-n 2` each. Do not run the 4 batches in parallel unless each batch has a distinct output folder or otherwise cannot collide.
- If `$zenmux-image-generation` defaults change, use its current defaults rather than older assumptions in archived changelog runs.
- If the generated files land in `$zenmux-image-generation`'s own output folder, report those paths and only copy or reorganize them into this skill's cover folder when the user asks or the current run explicitly needs the rednote asset bundle.

### 7. Report

Output a short summary: version, source release URL, saved file paths, rendered PNG paths, optional rednote/cover paths, and a one-line headline of what the release contains.

## Output locations

All paths below are relative to `<skill-dir>` (the installed `codex-cli-changelog/` folder; its absolute prefix varies by agent).

```
<skill-dir>/
├── SKILL.md
├── scripts/
│   ├── fetch_latest_release.py             # GitHub releases -> curated markdown
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
    └── codex-cli-<version>.md
```

Files are version-named so re-running the skill for the same release is idempotent.
Generated image folders (`assets/rendered/` and `assets/covers/`) are gitignored because they are reproducible local/social assets and can become large.
