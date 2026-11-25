---
name: design-tips
description: "设计 · 33 条：先出图再写页面、动效库、参考网站、设计 skill。"
disable-model-invocation: true
---

# 设计 · 33 条

Copybook 的 33 条「设计」技巧，收藏多的在前。每条要用的文字、放到哪里、最后得到什么，都在 references/ 里它自己的文件中。

- 用户点名技巧时，用点名的那条。用户只说了要做什么时，从适用于实际执行者的技巧里，选最符合用户目标和限制的一条。几条同样合适时，选一条即可。选中后，用一句话说明选了哪条、为什么，再读它的文件照着做。另一条也合适，而且换用它会明显改变做法或结果时，顺带点出它的名字和区别。
- 用户什么都没说：把下面的列表（每条的名字和做什么）给用户看，问用哪条。
- 都不合适就直说，并建议用 copybook，它会在全部 146 条里找。

| 技巧 | 做什么 |
| --- | --- |
| [AGENTS.md 两行：删多余文字，兼顾 UX、DX、AX](references/two-agents-md-lines.md) `two-agents-md-lines` | 清理页面上重复的标语、眉题等装饰文案，保留功能标签和操作说明。 |
| [Codex 页面设计：先画成一张图，再照着做](references/page-design-as-an-image-first.md) `page-design-as-an-image-first` | 直接让 Codex 写页面，设计总很烂：一句话让内置图像模型先画出页面，再交给写代码的模型照着做。 |
| [huashu-art-motion：35 种画风动画](references/huashu-art-motion-35-art-styles.md) `huashu-art-motion-35-art-styles` | 想要梵高、莫奈或包豪斯风格的动画：用代码画出来，几乎不动的片子交付前会被打回。 |
| [写进 CLAUDE.md 的 8 个前端参考网站](references/8-frontend-reference-sites.md) `8-frontend-reference-sites` | 卡在风格、组件、动效、演示视频或收尾：8 个网站按卡点分好，存进 CLAUDE.md，该用哪个它知道。 |
| [120 个可点选的动效样例库](references/120-sample-motion-library.md) `120-sample-motion-library` | 动效靠点选：120 个带标注的样例分 5 组，勾选喜欢的，Claude Code 就把它们做进你的视频或网站。 |
| [good-css：vibe coding 网站的 CSS 检查](references/good-css-css-check.md) `good-css-css-check` | 手机上 hover 卡住、表单一打开全红框：47 条现代 CSS 写法，先列出网站样式的毛病，不改代码。 |
| [视频配声音：测节拍和响度](references/video-sound-by-measurement.md) `video-sound-by-measurement` | Opus 5.5 听不见自己配的声音：librosa 找节拍，120 Hz 以下波形核对，导出的 MP4 上测响度。 |
| [做动效视频的 4 人小组](references/4-person-motion-video-team.md) `4-person-motion-video-team` | Claude Code 里做动效视频：拆片、分镜、审片 3 个 subagent 配合主会话做片，你只管像导演一样拍板。 |
| [项目动画：Claude Motion 指南](references/claude-motion-project-animation.md) `claude-motion-project-animation` | 哪部分值得做成动画：按 Anthropic 指南挑出候选、写好分镜，你选的那个用 HyperFrames 做出来。 |
| [按你喜欢的网站写的 DESIGN.md](references/design-md-from-sites-you-like.md) `design-md-from-sites-you-like` | 页面一眼 AI 味，是它没见过你喜欢的样子：3 到 5 张截图写成 DESIGN.md，再装两个设计 skill。 |
| [TasteSkill v2：AI 痕迹检查](references/tasteskill-v2-ai-look-check.md) `tasteskill-v2-ai-look-check` | 页面一眼就像 AI 做的：按桌面、平板、手机宽度列出每一处痕迹，FAIL 排在 WARN 前，不改代码。 |
| [仪表盘改版：两个 skill 加两条提示词](references/dashboard-redesign-2-skills.md) `dashboard-redesign-2-skills` | 仪表盘一眼 AI 做的：ui-ux-pro-max 加 frontend-design，改版提示词里点名它们，再从 4 个角度审查。 |
| [先截图再重做的 UI 提示词](references/screenshot-first-ui-rebuild.md) `screenshot-first-ui-rebuild` | UI 层级和密度有问题：每个页面先截图，再只用一套间距、字号和最多 5 种颜色重做。 |
| [Codex computer use 当本地 MCP server](references/codex-computer-use-as-mcp-server.md) `codex-computer-use-as-mcp-server` | Claude Code 缺个好浏览器：ChatGPT 的 computer use 当本地 MCP，点页面、截图，对比线上和本地。 |
| [资深设计师视角的 UI/UX 审查](references/ui-ux-audit-as-a-senior-designer.md) `ui-ux-audit-as-a-senior-designer` | 有实权的设计审查：先定审美基线，正确性直接修，能用但显廉价的地方找出来，大改动只提建议。 |
| [lemo-opuscar：代码做带旁白的发布短片](references/lemo-opuscar-launch-films.md) `lemo-opuscar-launch-films` | 没有视频模型：TTS 旁白、免费采样库配乐，每一帧按 43 种风格之一用代码渲染，30 到 60 分钟。 |
| [纯代码动画的 4 个起点](references/4-starts-for-code-only-animation.md) `4-starts-for-code-only-animation` | 喜欢的动画、一句想法、一张角色图、想要的画风：各一条提示词，渲染成一个 HTML 文件，加配乐。 |
| [awesome-design-md 和 shadcn skill](references/awesome-design-md-shadcn-skill.md) `awesome-design-md-shadcn-skill` | 页面总是默认 shadcn 味：Stripe 或 Linear 风格的 DESIGN.md，整套组件照着改，附一页设计系统。 |
| [Awwwards 评分表自评循环](references/awwwards-scoring-loop.md) `awwwards-scoring-loop` | 只在用户明确想用 Awwwards 评分探索视觉方向时使用，分数用于讨论设计。 |
| [组件每种状态的压力测试](references/component-stress-test.md) `component-stress-test` | 示例数据下能用说明不了什么：真实组件放到临时页面，每种要紧的状态都渲染一遍，只修能复现的。 |
| [6 条 ChatGPT 改照片提示词](references/6-chatgpt-photo-prompts.md) `6-chatgpt-photo-prompts` | 不请摄影师也有专业质感：职业头像、电影剧照、旅行照、杂志大片、老照片修复、黄金时刻补光。 |
| [/design 画出的每个界面状态](references/every-ui-state-with-design.md) `every-ui-state-with-design` | 功能做之前先看到每个状态：/design 配一个设计参考仓库，默认、加载、空、出错、成功都画成稿。 |
| [图片方案并成一张网格图：AGENTS.md 规则](references/image-options-in-one-grid.md) `image-options-in-one-grid` | 图片方案一张张生成太烧额度：一条全局规则让所有方案进同一张带编号的网格图，再做你挑中的。 |
| [视频提示词里的运镜名称](references/camera-moves-for-video-prompts.md) `camera-moves-for-video-prompts` | Opus 5.5 做的视频像幻灯片：6 种运镜的名字和各自效果，外加要写的秒数和速度。 |
| [/learn-taste：设计修正变成规则](references/learn-taste-design-corrections.md) `learn-taste-design-corrections` | 你总在改同样的设计错误：一次会话里的每个修正，都变成一条带理由的严格规则。 |
| [CLAUDE.md 像素画渲染规则](references/pixel-art-rendering-rules.md) `pixel-art-rendering-rules` | 精灵图里清晰的像素到屏幕上变糊：纹理用 Nearest，整数倍缩放，镜头和精灵按同一方式取整。 |
| [happy-path 债务排查和修复](references/happy-path-debt-found-and-fixed.md) `happy-path-debt-found-and-fixed` | 界面只在数据加载快、什么都不出错时才正常：缺的状态和布局错乱逐个组件修好，设计不变。 |
| [Unslop 提示词：去掉页面 AI 味](references/unslop-prompt.md) `unslop-prompt` | 页面第一眼就像 AI 做的：列出每处 AI 味的痕迹，先写 5 行方向等你点头，再一轮一轮改。 |
| [703 条 Opus 5.5 视频提示词，重做一条](references/703-video-prompts-one-remade.md) `703-video-prompts-one-remade` | 给产品做一支爆款那样的视频：703 条提示词里最适合你的 5 条，你选的那条重做成一个 HTML 文件。 |
| [Hallmark：审查和重做 AI 味页面](references/hallmark-audit-and-redesign.md) `hallmark-audit-and-redesign` | 标题上方的小标签一眼暴露是 AI 做的：一条命令列出页面的问题，另一条整页重做，内容和表单保留。 |
| [设计师开源的落地页 skill](references/designers-landing-page-skill.md) `designers-landing-page-skill` | 想要有设计感的落地页：一轮问题问完，布局、文案、字体和间距都替你定。 |
| [Internet Archive 的公有领域素材](references/internet-archive-clips-and-music.md) `internet-archive-clips-and-music` | 镜头需要老电影或老唱片：自动搜 Internet Archive 的免费 API，只用公有领域条目，每条记下来源。 |
| [Refero 风格提示词：先出设计方案](references/refero-style-prompt.md) `refero-style-prompt` | 页面换哪家创业公司都一样：以 Refero 风格为参考，先批方案，再写进 DESIGN.md，截图对照它检查。 |
