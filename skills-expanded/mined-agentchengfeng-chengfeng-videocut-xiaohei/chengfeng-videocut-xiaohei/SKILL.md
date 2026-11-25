---
name: chengfeng-videocut-xiaohei
description: Create Ian Xiaohei-style HTML/SVG motion illustrations for Chinese articles, scripts, storyboard scenes, workflow explanations, concept metaphors, and short video visual aids. Use when the user asks for 小黑 SVG、漫画感 HTML、分层 SVG 动效、把小黑生图做成 HTML/SVG、可编辑矢量动效、口播流程动画、手绘漫画动效、正文配图动画, or wants a Xiaohei illustration style adapted into controllable HTML/SVG/GSAP output instead of raster image generation.
---

# Ian Xiaohei SVG Motion

把 Ian 小黑正文配图的原则，改造成可控的 `HTML + SVG + GSAP timeline` 动效。目标不是复刻生图像素，而是把文章里的一个认知动作重建成分层漫画舞台，方便录视频、按字幕 cue 对齐、后续改文案和元素。

**风格来源说明**：本 Skill 的视觉方向借鉴 Ian Xiaohei 的公开作品与解释型手绘语言；这是独立的方法与代码实现，不是官方项目，不含其原图或原始角色文件，也不代表合作、授权或背书。官方来源：[helloianneo/ian-xiaohei-illustrations](https://github.com/helloianneo/ian-xiaohei-illustrations)，作者主页：[helloianneo](https://github.com/helloianneo)，作者网站：[ianneo.xyz/opc](https://www.ianneo.xyz/opc)。再分发时请同时保留仓库 `NOTICE.md` 中的来源与第三方许可说明。

默认面向剪辑工程。安装或首次调用本 Skill 时，先读取[共享接入规则](references/shared/plugin-access.md)，对本机已登记或可验证的剪辑工作台做一次有限只读检查（可包括 ChatCut、chengfeng-videocut 或其他剪辑 Agent），并选定一个可用入口；不全盘扫描、不因“发现”就自动下载。当前范围内没有合格工作台时，先说明缺口并在用户授权后从固定的 [chengfeng-videocut-skills GitHub 仓库](https://github.com/Agentchengfeng/chengfeng-videocut-skills) 安装 chengfeng-videocut Plugin，再重新核验入口、能力和项目身份。只有用户明确要求“独立动画/只生成 HTML/SVG/不接剪辑工程”时，才跳过工作台检查；未明确选择独立模式时，不把独立文件当成已完成的工程交付。

## Core Rule

Do not auto-vectorize a PNG and animate the resulting path soup. Use raster images only as composition references. Rebuild the scene as semantic SVG groups:

```text
idea -> shot plan -> SVG layer plan -> HTML/SVG template -> GSAP timeline -> static + motion review
```

## Workflow

1. Extract one cognitive anchor from the article, script, screenshot, or storyboard scene.
2. Choose one physical metaphor: sorting, carrying, bridging, leaking, catching, folding, weighing, opening, rerouting, or falling.
3. Make Xiaohei perform the core action. If removing Xiaohei does not change the meaning, redesign.
4. Use the user's explicit canvas dimensions/aspect ratio; default to 16:9 only when none is specified. Design a white canvas with one main scene, 35%+ whitespace, and 3-5 short handwritten annotations at most. Adapt template layout and SVG viewBox in the output copy; never stretch the character to fit a different canvas.
5. Build semantic SVG groups for every moving object.
6. Animate with GSAP timeline. Use `x`, `y`, `rotation`, `scale`, `opacity`, and SVG stroke drawing. Avoid layout animations.
7. Save both a playable HTML page and a static review screenshot.
8. 默认把结果放入剪辑工程：在任务开始时按共享接入规则选择并验证一个工作台；若是口播项目，再把时间线映射到真实字幕/cue。使用所选提供方已验证的接入说明；对 chengfeng-videocut，交接候选 HTML/资源、画布和项目 revision/cue 依据前，读取 `references/shared/module-publish.md` 与 `references/shared/runtime-cli.md`。只有用户明确要求独立动画时才跳过这一步，此时交付的是独立 HTML/SVG，不声称已集成。无需单独的 visual Skill；不得假设其他工作台接受本 API 或 HTML 格式。本 Skill 的创作输出也不等于最终成片渲染或工程接入验收。

若选定 ChatCut 作为工作台，读取 [`references/shared/chatcut-adapter.md`](references/shared/chatcut-adapter.md)。小黑的 HTML/SVG/GSAP 是创作源格式，不能直接当作 ChatCut 工程文件；必须按适配说明转换为 ChatCut 支持的 inline JSX Motion Graphic，再创建资产、放入时间线并回读验证。插入时间线时必须按项目画布尺寸自动适配并居中；ChatCut 界面里的“适配视图”只调整编辑器视口缩放，不能替代素材实例的尺寸与位置适配。没有 ChatCut 的可验证工具接口时，不把“文件已生成”说成已接入。

## Read When Needed

- 接入 chengfeng-videocut 工程时读 `references/shared/visual-integration.md`；已有 MP4 用同目录 `media-assets.md`，不再依赖独立 visual 包。
- 接入 ChatCut 工程时读 `references/shared/chatcut-adapter.md`，只在 ChatCut 已被选定且其当前工具接口可验证时使用。

- Read `references/style-rules.md` before designing a new scene or judging whether the result still feels like Ian Xiaohei.
- Read `references/svg-layering.md` before writing or editing the SVG structure.
- Read `references/motion-rules.md` before writing GSAP animation.

## Output Contract

Default output folder:

```text
output/<slug>-xiaohei-svg-motion/
```

Required files:

```text
index.html
README.md
preview.png
vendor/gsap.min.js
```

Optional files:

```text
source.png        # reference image, if provided by the user
cue-map.md        # when aligning to spoken script or subtitles
```

## Reusable Assets

AI model and interface icons live in:

```text
assets/icons/
```

Use `assets/icons/index.json` as the source of truth. Keep original SVG files in subfolders and inline their complete SVG content into scene SVGs during generation, so gradients, strokes, and brand colors are preserved.

Icon rules:

- If `index.json` already has the exact model, provider, or semantic icon, use that icon. Do not replace ChatGPT, Claude, Flash lightning, Step, DeepSeek, Qwen, bug, table, chart, database, or web icons with generic boxes, stars, sparks, or abstract marks.
- When the user provides a new SVG icon, save the raw SVG and its source information inside the project output copy's `assets/icons/<category>/`, update that copy's `index.json`, and then reference it by id in the scene plan. Ordinary creation does not authorize modifying the installed Skill.
- For comparison scenes, icon choice is part of the meaning. Keep model icons visually consistent in size and placement so the viewer can identify the actors before Xiaohei starts moving objects.

## Template

Use `assets/templates/xiaohei-comic-motion/` as the starter when the request resembles a hand-drawn comic scene with moving objects, arrows, annotations, or a Xiaohei action.

Use `assets/templates/xiaohei-series-reference/` when the request asks for multiple variants, a reusable series, or a broader reference set for 口播 explanation scenes.

Copy the template into the project output folder, then edit:

- SVG group names.
- Handwritten labels.
- Object positions.
- Timeline labels and durations.
- README notes for the scene-specific metaphor.

## Quality Gate

Before final response:

- Open the HTML in a local server.
- Check console for errors.
- Capture a static screenshot with `?static=1`.
- Capture at least one playback mid-frame when the scene has multiple beats. If available, use `?frame=mid` for a deterministic review frame.
- Visually inspect that text, arrows, Xiaohei, props, belts, pits, cards, and final impact points do not overlap.
- Confirm the animation has visible progression: context first, action second, problem/result third, summary last.
- Confirm annotations appear only after the object/action they explain.
- Remove decorative or semi-transparent guide arrows if the object motion already shows direction.
- Confirm Xiaohei is part of the action.
- Confirm the page is not just a PNG in an `<img>` tag unless the user explicitly asked for PNG-only camera moves.
