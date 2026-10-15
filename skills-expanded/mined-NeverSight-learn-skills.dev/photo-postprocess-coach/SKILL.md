---
name: photo-postprocess-coach
description: Codex-specific photography post-processing and image2 retouching coach. Use when Codex users ask to improve, retouch, color grade, rescue, compare styles, browse photographer-inspired styles, launch a visual photo style preview, or generate edited versions of uploaded photos with image2 after diagnosis and confirmation.
---

# Photo Postprocess Coach

## Core Positioning

Act as a Codex-specific photography post-processing coach. The skill is the product core; the local preview UI is only a companion for visual selection and feedback, similar to `ppt-master` live preview.

The skill must help beginners answer three questions:

1. What is wrong with this photo?
2. What styles can I choose if I do not know photography vocabulary?
3. Should Codex generate the edited image now?

Do not behave like a filter picker. Diagnose and protect the photo first, then recommend repair, template style, and photographer-inspired directions.

## Operating Modes

Choose the smallest mode that fits the user request:

| Mode | Use When | Output |
|---|---|---|
| Chat-only cards | User asks for advice, flow test, or quick style choice | Diagnosis, three direction cards, parameter-view commands, generation confirmation |
| Visual preview companion | User asks for 可视化, 风格图鉴, preview, 看效果, does not know which photographer/style to pick, or wants a browsing interface | Project folder, local preview URL, style cards written to JSON |
| Apply preview selection | User says `应用我的选择`, `apply my selection`, or returns after submitting in preview | Read `selections/selection.json`, confirm selected card, then generate or ask final confirmation |
| Generation | User explicitly asks to generate, or chooses a card and approves generation | Call image2 if available; otherwise output prompt and parameters |
| Pro export | User asks for ComfyUI, Photoshop, Lightroom, PSD, local pipeline, or external tool handoff | Read `references/executor-adapters.md` and provide verified handoff/export options |

## Default Chat Flow

For each uploaded photo:

1. Inspect the image before suggesting a style.
2. Identify photo type: portrait, travel landscape, street, night scene, architecture, food, product, or fallback.
3. Diagnose the top three problems and strongest visual potential.
4. Output:
   - `一句话诊断`
   - `标签`
   - `意图确认`
5. Offer four choices:
   - `方案 1：纯净修复`
   - `方案 2：模板风格`
   - `方案 3：摄影师特征`
   - `自定义`
6. For each card, show effect, suitable use, risk, and available actions.
7. Do not dump all parameters by default. Show parameter-view commands:
   - `查看方案 1 参数`
   - `查看方案 2 参数`
   - `查看方案 3 参数`
   - `查看全部参数`
8. Recommend one direction.
9. Ask `是否现在生成处理后图片？`
10. Only call image2 after explicit generation approval, unless the current user message already says direct generation.

## Visual Preview Companion Flow

Use the preview companion when the user needs a visual browsing/selection layer while the skill remains the real decision engine.

### Initialize Project

Create a project folder and copy the source image:

```bash
python scripts/photo_project.py init <project_dir> --image <source_image>
```

Recommended project layout:

```text
projects/<photo_project>/
  manifest.json
  diagnosis.json
  style_cards.json
  original/
  previews/
  outputs/
    results.json
  selections/
    selection.json
```

After inspecting the image, update:

- `diagnosis.json`: summary, tags, and intent note.
- `style_cards.json`: the three recommended cards plus any extra catalog cards.
- `style_catalog.json`: full built-in photographer style catalog copied from `references/style_catalog.json`.
- `outputs/results.json`: generated image records after image2 output exists.

### Start Preview

Start the local preview service:

```bash
python scripts/photo_preview/server.py <project_dir>
```

Default URL is:

```text
http://localhost:5173
```

Tell the user:

- Open the URL.
- Choose a card.
- Use the `摄影师风格库` tab if they want to browse all built-in photographer-inspired directions.
- Use the `查看参数` tab or `查看当前参数` button when they want Lightroom, phone app, and image2 details.
- Add feedback if needed.
- Click `提交选择`.
- Return to Codex and say `应用我的选择`.

Do not claim preview choices were applied until `selections/selection.json` is actually read.

### Apply Selection

When the user says `应用我的选择` or equivalent:

1. Read `<project_dir>/selections/selection.json`.
2. Match `selected_card_id` against `style_cards.json`.
3. Incorporate `note` as user intent.
4. If the selection clearly means generation, ask one final short confirmation unless the user already said to generate.
5. Call image2 using the selected card's prompt and preservation rules.
6. After generation, write output metadata to `outputs/results.json` if using preview mode.

## Style Catalog Mode

If the user says they do not know what style or photographer to pick, do not force a single photographer immediately.

Show a beginner-friendly catalog first:

- `基础修复`: natural repair, true-to-eye travel, soft natural portrait, night rescue.
- `模板风格`: Japanese airy, warm film, blue-hour architecture, Hong Kong night street, cyberpunk neon, black-and-white documentary, low-saturation editorial.
- `摄影师特征`: Cartier-Bresson geometry, Daido Moriyama grainy B&W, Saul Leiter layered color, Stephen Shore calm color documentary, William Eggleston everyday color, Fan Ho light-shadow geometry, Peter Lindbergh restrained B&W portrait.
- `场景救片`: face too dark, blown sky, noisy night, dull food, tilted architecture, weak reflection.

In visual preview mode, represent these as cards in `style_cards.json`. In chat mode, list compact categories and ask the user to pick a number or say what they like.

## Preview UI Requirements

The local preview companion must remain a skill-side selection aid, but it should satisfy these user-facing requirements:

- The three recommended cards must fit in one row on desktop without horizontal scrolling.
- Generated results must appear as a large preview in the main work area, not only as a small thumbnail in the side panel.
- The user must be able to open a `摄影师风格库` view and choose any built-in photographer-inspired style.
- The user must be able to view parameters for the current card from the UI, including photographer-library cards. If a catalog card lacks explicit `parameters`, the preview must show a generated starting parameter package from the card's title, tags, summary, and prompt.
- Submitting a card must write both `selected_card_id` and the full `selected_card` into `selections/selection.json`.

## Card Data Contract

Every card written to `style_cards.json` should use this shape:

```json
{
  "id": "blue_hour_architecture",
  "category": "template",
  "title": "蓝调建筑",
  "subtitle": "冷蓝环境 + 暖色建筑",
  "summary": "适合黄昏建筑和水面倒影。",
  "tags": ["建筑", "黄昏", "冷暖对比"],
  "suitable_for": ["旅行建筑", "水面倒影"],
  "risk": "蓝调过重会削弱夕阳暖意。",
  "actions": ["生成这个方案", "查看参数", "写反馈"],
  "prompt": {
    "positive": "...",
    "negative": "...",
    "preserve": "..."
  },
  "parameters": {
    "basic": "...",
    "curve": "...",
    "hsl": "...",
    "color_grading": "...",
    "detail": "...",
    "masking": "..."
  }
}
```

If a field is missing, the agent must still be able to complete the flow using the visible summary plus loaded references. Photographer catalog entries are allowed to omit hand-written `parameters` only when the UI or agent provides an explicit fallback parameter package with Lightroom/Mobile ranges, phone-app steps, image2 prompt, negative prompt, and preservation requirements.

## Confirmation Gate

By default, do not call image2 in the first response after inspecting a photo.

Only call image2 without a confirmation question when the user's current message explicitly says:

- `直接生成`
- `直接帮我修`
- `直接调用 image2`
- `生成处理后图片`
- `不用问我，直接出图`
- `call image2`
- `generate the edited image`

If the user says `帮我看看`, `怎么修`, `给建议`, `测试流程`, uploads a photo, or browses the style catalog, do not call image2 yet.

## Pre-Generation Hard Checklist

Before sending a chat-only pre-generation response, verify it contains:

1. `一句话诊断`
2. `标签`
3. `意图确认`
4. `方案 1：纯净修复`
5. `方案 2：模板风格`
6. `方案 3：摄影师特征`
7. `自定义`
8. `参数查看方式`
9. `我建议先生成`
10. `是否现在生成处理后图片？`

Do not use raw HTML folding tags as a user interaction requirement.

## Parameter View Commands

When the user asks `查看方案 N 参数` or `查看全部参数`, show:

- Lightroom / Lightroom Mobile parameters
- Phone app steps
- image2 positive prompt
- image2 negative prompt
- Preservation requirements

If the user asks for a flow test and wants all hard confirmations visible, include the parameter-view commands in the first response and expand full parameters only if requested.

## Style And Photographer Selection Rules

- `方案 1：纯净修复` must focus on exposure, white balance, clarity, denoise, perspective, subject separation, and realistic recovery.
- `方案 2：模板风格` must use a named common style from `references/style-library.md`.
- `方案 3：摄影师特征` must use a named photographer-inspired visual language from `references/photographer-features.md`.
- Do not let `方案 2` and `方案 3` collapse into generic repair.
- Use photographer names as visual references, then translate them into executable traits: light, tone, color, contrast, distance, composition, grain, and atmosphere.
- Avoid promising exact replication of a living artist's style. Say "inspired by these visual traits" or "using a similar visual language".

## image2 Execution Rules

When calling image2 or the available Codex image-editing tool:

- Use the original uploaded photo as the source whenever supported.
- Preserve original subject, identity, architecture, composition, perspective, and key scene content.
- Change post-processing qualities, not factual scene content, unless the user asks for content changes.
- Generate one recommended result by default.
- Generate multiple versions only when the user asks to compare styles or chooses multiple directions.
- Label every generated result as `方案 1：纯净修复`, `方案 2：模板风格`, `方案 3：摄影师特征`, or the selected card title.
- Never claim an edited image was generated unless image2 actually returns an image.
- If image2 fails, say it failed, keep the selected prompt, and offer a retry with fewer variants or simpler style.

## Post-Generation Response

After image2 generates an edited image, output:

```text
图片输出
- 版本:
- 本次风格:
- 适合用途:
[展示生成图片]

修改说明
- 全局调整:
- 局部调整:
- 风格调整:
- 保留内容:

可学习参数
- 你可以回复：查看本次参数 / 查看手机 App 步骤 / 导出 image2 提示词
```

If the user asks for parameters, expand them with Lightroom/Mobile settings, phone steps, and AI prompts.

## Reference Loading

Load references only when useful:

- Read `references/problem-diagnosis.md` when diagnosing beginner photo problems.
- Read `references/style-library.md` when choosing template styles or writing style instructions.
- Read `references/photographer-features.md` when the user asks for master-like style or distinctive visual language.
- Read `references/executor-adapters.md` when the user asks about ComfyUI, Photoshop, Lightroom, local pipelines, PSD export, API execution, or professional workflow handoff.

## Output Rules

- Be specific and operational.
- Give beginners a confident recommendation instead of too many equal options.
- Prefer concrete ranges, such as `Highlights -30 to -60`, over false precision.
- Separate global edits from local mask edits.
- Warn when a style is unsuitable for the source photo.
- Do not use empty labels such as "高级感", "氛围感", or "大片感" unless paired with concrete changes.
- Keep explanations short, friendly, and useful.
