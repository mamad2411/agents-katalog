---
name: create-xiaohongshu-covers
description: >
  Create exactly two publish-ready Xiaohongshu cover PNGs from a topic, pasted text, Markdown document, article outline, or full article. Use when the user asks to create, generate, design, redo, or export a Xiaohongshu cover, especially requests such as “做两版小红书封面”, “根据这篇文章出封面”, “把这个选题做成 3:4 封面图”, or “生成黑白红手绘纸张风封面”. The workflow extracts truthful short cover copy, intelligently selects one of three fixed decorative labels, keeps the TranFu brand logo fixed at the upper right, selects small content-related app, brand, or subject icons, optionally uses a supporting image, renders two distinct 1080x1440 layouts, and verifies both files. Do NOT trigger when the user only wants post writing, carousel/body images, a cover for another platform, photo retouching without cover design, publishing, analytics, or an editable design source.
---

# Create Xiaohongshu Covers

Create one `XHS_COVER_PAIR` containing two distinct PNG covers for the same topic. Preserve the source's meaning while making the cover readable at thumbnail size.

## Work Contract

**Input**

- MUST require one of: a readable local text/Markdown path, pasted text, an article outline, a full article, or a one-sentence topic.
- Accept an optional readable local image and optional output directory.
- Treat clearly labeled alternatives inside a topic plan as supporting choices, not multiple primary topics; use the document's explicit main topic.

**Ownership: edit file**

- MUST create files only in the user-requested output directory. If none is given, create and use `./xhs-cover-output/` under the current working directory.
- MUST render through `scripts/render_covers.mjs`; NEVER hand-author the final binary.
- NEVER overwrite existing files unless the user explicitly requests replacement.

**Output**

- MUST return exactly two PNG links named as Variant A and Variant B.
- NEVER return SVG, HTML, JSON, or editable design-source deliverables.

**Tool mapping**

- Resolve `SKILL_DIR` to the absolute directory containing this `SKILL.md` before reading resources or running scripts.
- Read the source with the runtime's local file tools.
- Use only browsing, image generation, or acquisition tools exposed by the current runtime; NEVER invent a tool name.
- When network access is available and not prohibited by the user, acquire brand assets only from an official site, official press kit, or official product page.
- Run the deterministic CLIs with Node.js at `$SKILL_DIR/scripts/render_covers.mjs` and `$SKILL_DIR/scripts/verify_pngs.mjs`.

**Done**

- Both files MUST exist, pass `scripts/verify_pngs.mjs`, and be exactly 1080 x 1440.
- When a local-image viewer is available, both files MUST pass every visual check in `references/visual-system.md`. When none is available, the final verification line MUST say `visual inspection unavailable` and MUST NOT claim a visual pass.
- The two covers MUST differ in at least two required composition dimensions.

## Required Workflow

CREATE A TODO LIST FOR THE TASKS BELOW and update it after every completed step.

1. Read the complete source before extracting copy. If the path is missing or unreadable, identify the exact path and request a valid source, then stop. If the source is empty, request a topic or non-empty source, then stop.
2. Select one primary angle. If two or more unrelated angles have equal primary status, ask one focused question naming the choices, then stop until the user answers. Otherwise continue with the explicit main topic.
3. Read `$SKILL_DIR/references/visual-system.md`. View `$SKILL_DIR/assets/xhs-cover-core-template.png` and `$SKILL_DIR/assets/tranfu-logo.png` when a local-image viewer is available; otherwise use the written rules. Draft one truthful shared message and two different title-line arrangements.
4. Validate the copy before rendering. Select the fixed upper-left decorative label with the rules below; do not invent or rewrite a label. If the title adds a fact, number, quote, authority claim, or promise absent from the source, remove it. If a title line exceeds the renderer's safe width, shorten the copy or move words between lines; NEVER solve overflow by making the title unreadably small.
5. Create one task-scoped temporary directory for the render spec and any acquired icon assets. If it cannot be created, report the exact filesystem error and stop.
6. Build `decorative_icons` with two to four distinct content-related items. Prefer named apps or brands in the source; when browsing is available, use a compact transparent mark from the brand's official site, official press kit, or official product page. Check the official usage terms before applying the required doodle treatment; if they prohibit modification, texture, reduced opacity, or similar treatment, treat that mark as unsuitable and use a generic subject icon. Prefer a symbol over a text-heavy wordmark. If fewer than two suitable brand assets are available, fill the remaining slots with generic subject icons from the allowlist below. NEVER repeat one mark merely to reach two items, use brand colors, or imply endorsement.
7. Resolve the optional supporting image. If the user supplied an unreadable image path, request a valid path and stop. If no image was supplied, use an image generation or acquisition tool only when that tool exists in the current runtime and the image materially helps the topic. If optional image work is unavailable or fails, set `image_path` to `null` and continue.
8. Write one JSON render spec in the task-scoped temporary directory using the schema below. If it cannot be written, report the exact filesystem error and stop.
9. Ensure the output directory exists, then run `node "$SKILL_DIR/scripts/render_covers.mjs" --spec <absolute-spec-path> --output-dir <absolute-output-dir>`. If rendering fails because an acquired icon is unreadable, replace that item with a relevant generic subject icon. Set `image_path` to `null` and retry once with `--simple`; this keeps two content icons and removes optional imagery. If the retry fails, report the renderer error and stop without submitting a partial pair.
10. Parse the renderer's JSON stdout and run `node "$SKILL_DIR/scripts/verify_pngs.mjs" <absolute-cover-a> <absolute-cover-b>`. If verification fails, report the failed invariant, correct the render spec, and rerender the pair once. If it still fails, stop without claiming completion.
11. Inspect both PNGs with the runtime's local-image viewer when available. Apply every check in `references/visual-system.md`. If either cover fails, revise the failing copy, icon selection, or layout input and rerender the pair once; if the runtime has no image viewer, disclose that visual inspection was unavailable.
12. Remove only the task-scoped temporary directory, including downloaded icon sources and render files. Keep the two verified PNGs. Output `XHS_COVER_PAIR` using the exact format below and end.

## Copy Rules

- Preserve the source's main claim and tension.
- Prefer 10-22 Chinese characters across one to three title lines.
- Use a subtitle only when it adds necessary context.
- Choose one continuous semantic phrase for red emphasis; the exact phrase must appear in both variants.
- Keep product and technical names exactly spelled when they matter, including names such as Agent, ChatGPT, Claude, and API.
- NEVER fabricate evidence or make a stronger promise than the source supports.

## Fixed Header Branding

Set `eyebrow` to exactly one of these three decorative labels after reading the complete source:

- `Agent开发现场`: choose when the primary subject is building, coding, architecting, debugging, evaluating, deploying, or operating an AI Agent. This takes priority over `干货分享` when practical advice is specifically about Agent development work.
- `团队有话说`: choose when the primary subject is the team's viewpoint, collaboration, culture, management, retrospective, interview, announcement, or collective experience. Do not choose it merely because a team produced the article.
- `干货分享`: choose for tutorials, methods, checklists, tool usage, knowledge summaries, case-study takeaways, and other practical content not primarily covered by the two categories above. Use this as the fallback when the source does not clearly support either specialized label.

Base the choice on the source's primary angle rather than isolated keywords. Use the same selected label in both variants. The renderer places the bundled TranFu logo at the upper right automatically; do not add any right-side header text, ratio, date, issue number, badge, or per-task logo setting.

## Fixed Footer Branding

The renderer places `关注望船夫，持续更新AI干货` at the lower left automatically. Keep this exact text in both variants and do not derive, rewrite, or replace it from the source or render spec. Keep the lower-right corner empty; do not add dimensions, safe-area notes, dates, page numbers, handles, badges, or other small text there.

## Render Spec

Write UTF-8 JSON with this exact shape:

```json
{
  "output_basename": "agent-task-protocol",
  "eyebrow": "Agent开发现场",
  "subtitle": "把模糊想法改成可执行、可检查、可纠偏的任务协议",
  "accent_phrase": "Agent",
  "image_path": null,
  "decorative_icons": [
    {
      "path": "/tmp/create-xhs-covers/openai-mark.png",
      "label": "OpenAI"
    },
    {
      "symbol": "workflow",
      "label": "工作流"
    }
  ],
  "variants": [
    {
      "id": "a",
      "layout": "center-torn-paper",
      "title_lines": ["提示词写再长", "Agent 还是", "会跑偏？"]
    },
    {
      "id": "b",
      "layout": "offset-labels",
      "title_lines": ["Agent 总跑偏？", "真正缺的是", "任务协议"]
    }
  ]
}
```

Use a lowercase ASCII `output_basename` containing only letters, digits, and hyphens. Use each layout and each ID exactly once. Keep one to three non-empty `title_lines` per variant. Make `accent_phrase` occur in at least one line in both variants.

`eyebrow` MUST be exactly `干货分享`, `Agent开发现场`, or `团队有话说`, selected from the complete source using **Fixed Header Branding**. The upper-right TranFu logo is not part of the render spec because the renderer always uses the bundled brand asset.

The footer is also not part of the render spec: the renderer always uses `关注望船夫，持续更新AI干货` at the lower left and leaves the lower right empty.

`decorative_icons` MUST contain two to four distinct items. Give each item a short non-empty `label` and exactly one source:

- `path`: an absolute readable PNG, JPEG, WebP, GIF, or SVG source in the task-scoped temporary directory; this source is never a final deliverable.
- `symbol`: one generic subject icon from `ai`, `chat`, `code`, `document`, `search`, `workflow`, `image`, `video`, `data`, `cloud`, `security`, `idea`, or `tool`.

## Final Output

MUST use exactly this schema after all available checks pass:

```text
XHS_COVER_PAIR
- Variant A: [<basename>-cover-a.png](<absolute-path>)
- Variant B: [<basename>-cover-b.png](<absolute-path>)
Verification: PNG 1080 x 1440 x 2; visual inspection passed | visual inspection unavailable
```

NEVER attach implementation notes or intermediate file paths to this artifact.

## Failure Paths

- Missing, unreadable, or empty source -> request one precise replacement input and stop.
- Multiple equal primary topics -> ask one focused choice question and stop.
- Unreadable user image -> request a valid image path and stop.
- Optional runtime image tool absent or failing -> use a text-led design and continue.
- Browsing unavailable, forbidden, or unable to find an official brand asset -> use relevant generic subject icons and continue.
- Official brand usage terms prohibit the required doodle treatment -> do not modify that mark; use a relevant generic subject icon.
- Acquired icon unreadable or unsupported -> replace only that item with a relevant generic subject icon before the single simplified retry.
- Chrome absent -> report that `CHROME_PATH`, Google Chrome, and Chromium executables were searched; stop.
- First render failure -> replace any failing icon, remove the optional image, and retry once with `--simple`.
- Second render failure -> report the exact renderer error; submit no partial pair.
- Automated PNG verification failure -> revise and rerender once; a second failure stops.
- Visual failure -> revise and rerender once; a second failure stops with the failed check named.
- Visual viewer absent -> deliver only after deterministic verification and state that visual inspection was unavailable.

<example>
User: “根据 `/work/02-选题方案.md` 做两版小红书封面，输出到 `/work/covers`。”

Correct behavior:
1. Read the full file and use its explicit main topic rather than treating labeled backup topics as ambiguity.
2. Create two truthful title arrangements in the shared visual system.
3. Render and verify two 1080 x 1440 PNG files.
4. Return only:

```text
XHS_COVER_PAIR
- Variant A: [agent-task-protocol-cover-a.png](/work/covers/agent-task-protocol-cover-a.png)
- Variant B: [agent-task-protocol-cover-b.png](/work/covers/agent-task-protocol-cover-b.png)
Verification: PNG 1080 x 1440 x 2; visual inspection passed
```
</example>

<bad-example>
WRONG: Return one PNG and one editable vector, or return two files that only change the accent color.

Reason: The contract requires exactly two final PNG covers and a meaningful composition difference, not two export formats or a color-only duplicate.
</bad-example>
