---
name: web-clone-prompt
description: 网页复刻提示词生成器。输入一张/多张网页截图或一个网页 URL，反推出一份「确定性复刻 prompt」——用于授权页面、用户自有页面、内部研究或本地视觉回归。方法论抽离自 motionsites.ai 的成熟复刻提示词：精确到每个 hex、每条 Tailwind class、每个动画参数、每段文案、每个字体加载地址、每个素材生成简报或真实资源地址。当用户明确说"复刻这个网页/页面""把这个截图做成网页""仿这个落地页""1:1 还原这个网站""根据这个 URL 生成复刻提示词""clone this site / landing page""给我这个页面的复刻 prompt"时触发。也适用于用户只丢一张网页截图说"照着做一个"且语义是复刻。产出是一份可直接粘贴的 prompt；第一步不直接出代码，必须先问用户是否继续本地生成网站。不用于：原创设计、参考某站做一个新页面、品牌/文案/素材独立的新落地页（这些用 web-design-pro）、后端逻辑、非网页复刻任务。
---

# Web Clone Prompt · 网页复刻提示词生成器

**一句话**：用户给**截图**或 **URL** → 你**反推**出一份**确定性复刻 prompt** → 先交付 prompt → **询问用户是否继续用这份 prompt 生成网站** → 用户确认后再进入 Codex 构建与视觉回归。

**唯一目标**：在授权/内部研究范围内尽可能精确复刻。不要把任务降级成「风格类似」「视觉参考」或「受启发的重做」。如果输入事实不足以严格复现，必须主动补证据或标注推断；如果原站包含大型 3D/WebGL/物理/视频合成等高风险工程，先给出成功率和替代方案，让用户确认是否继续。

这套方法论抽离自 motionsites.ai 的真实复刻提示词风格（目标是让 AI 靠一段 prompt 高确定性重建整个落地页）。它们之所以能高保真复刻，靠的是**把每一个视觉/行为决策都预先定死、写成字面量**——精确到 hex、Tailwind class 串、framer-motion 数值、逐字文案、字体加载地址、素材生成简报或真实资源 URL。**你的任务就是即使在「推断」而非「转录」时，也产出同样精确、同样确定的 prompt。**

> ⚠️ 本 skill 的第一产物永远是一份 prompt 文本。不要在交付 prompt 的同一动作里擅自开始写代码；必须先问用户是否继续生成网站。用户确认后，才进入 Codex 构建、截图回归和修正。

> ⚠️ 授权边界：只对用户拥有、已获授权、内部研究、或本地视觉回归的页面做严格复刻。若参考对象是第三方品牌/商业站且用户要公开发布，prompt 必须把原品牌名、文案、商标、专有图片/视频/字体替换成用户自有或可授权素材；可把原站 URL 写成 `internal reference only` 的证据源，但不能把第三方资源描述成可直接上线复用的生产素材。

---

## 何时用 / 不用

| ✅ 用本 skill | ❌ 不用 |
|---|---|
| 复刻 / 仿照 / 1:1 还原一个**已存在**且可授权分析的网页 | 从 0 原创设计一个新页面 → 用 `web-design-pro` |
| 输入是网页**截图**或 **URL**，目标是 prompt-first 复刻 | 输入是 PRD / 纯文字需求 / 品牌新页 → 用 `web-design-pro` |
| 想要一份**可移植的复刻 prompt** 喂给别的 AI | 直接要可运行代码且无参考页 |
| 落地页 / Hero / 作品集 / 产品页 / SaaS 首屏 | 后端、数据库、纯逻辑 bug |

和 `web-design-pro` 的边界：
- 用户明确要 **clone / 1:1 / 复刻 / 按截图像素级还原 / 生成复刻 prompt** → 本 skill。
- 用户要 **参考某站风格做一个新页面 / 设计一个 landing page / 根据 PRD 或品牌资料实现网页 / 先建 Design Token 再编码** → `web-design-pro`。
- 两者可接力，但顺序固定：本 skill 先出授权范围内的复刻 prompt；用户确认后，才可进入本地实现和回归。不要让 `web-design-pro` 的“参考迁移/原创设计”默认逻辑覆盖本 skill 的 prompt-first 门禁。

---

## 工作流（4 步）

```
Phase 0 接收&定范围  →  Phase 1 反推填槽  →  Phase 2 按模板组装  →  Phase 3 自检&交付prompt  →  Phase 4 用户确认后实现&回归
```

### Phase 0 · 接收输入，定范围

1. **认输入类型**：
   - **截图（1 张）** → 先判断用户要的是「只复刻可见区域」还是「生成完整落地页/网站」。只复刻可见区域时按截图精确落地；用户说网页/网站/落地页时，必须把截图视为被截断的上半段：可见区域精复刻，未截到的下方段落按 nav、主题、行业和视觉系统推理补全，并标注 `[inferred from visible design system]`。截图模式拿不到源码，但截图本身就是事实锚点：必须自动做裁切、分屏解析、局部元素登记，后续实现逐屏/逐段和原截图对比。若截图明显截断，自动补齐完整落地页结构，不把截断当作页面结束。
   - **截图（多张）** → 先确认：是「同一页的多个段落（按此顺序）」还是「同一段的多个备选」？（见 inference-guide §5）。确认后把每张截图登记为 `REFERENCE_FRAME_N`，实现回归逐张对比，不能只看首屏。
   - **URL** → 信号最足但风险最高：可抓 DOM 段落结构、computed 字体/颜色、真实资源 URL、`<title>`。同时必须抓脚本/样式里的运动系统：custom elements、`canvas`/WebGL、shader、GSAP/Lenis、smooth scroll、`pointermove`/`mousemove`、`requestAnimationFrame`、`fontVariationSettings`、scroll progress、hover handlers；并用浏览器从 first paint / loading / opening sequence 到稳定首屏做定时截帧，再继续采样滚动、鼠标和 hover 状态。**源码实测 + 浏览器截帧 > 推断值**。URL 只用于取证和填槽；第一产物仍然是复刻 prompt，不能跳过 prompt 直接实现。
     - **复杂工程确认门禁**：如果发现 three/OGL/Babylon/WebGL shader、多 canvas 叠层、复杂 3D 场景、物理粒子、视频合成、音视频同步、登录/付费资源或大量不可复用私有脚本，先向用户说明「完全复刻 / 高相似重建 / 静态近似」三档成功率和成本，再继续。
   - **截图 + URL 都有** → URL 取精确值，截图核对视觉。
2. **认消费端能力**：
   - **截图模式默认** `target_asset_mode = image-gen-capable`：按当前消费端具备图像生成能力的情况写（如有可用的 OpenAI image generation、Gemini、v0、Lovable、bolt 等）。素材用生成简报，不附 stock 直链；如果当前工具/组织没有生图权限，消费端应保留 brief 或切到 `fetch-only`。
   - **URL 模式默认** `target_asset_mode = url-extracted-assets-primary`：公开稳定的源站图片、视频、字体、SVG、Lottie/JSON、CSS 背景资源能抓取就写真实 URL；抓不到、不稳定、登录/付费/403/临时签名时，才退回生成简报。
   - 只有用户明确说目标工具不会生图，或要给纯 Claude Code/fetch-only 工具用，才改为 `target_asset_mode = fetch-only`，为无法抓取的关键素材加一条已核验 stock 直链。
   - 截图裁切是最后兜底；不要把裁切当作 URL 模式的主资产策略。
3. **判断范围歧义**：一张「占满视口」的截图可能是「整页」也可能是「长页的首屏」。如果用户说的是「复刻这个 hero/首屏/截图里这块」，只输出可见范围；如果用户说的是「网页/网站/落地页」，默认输出完整 landing page：先列出可见 section，再根据 nav 标签和行业补全剩余 section。只有当 section 数量会影响业务含义且无法从 nav 推断时才追问（**最多 2–3 个问题，批量问一次**），否则**默认推断+继续**，把假设列在产物顶部。
4. **认出设计系统血统**：若命中暗色电影感 + 全屏视频 + 液态玻璃 + 斜体衬线标题这套家族脸，→ 直接复用 `references/component-library.md` 里的招牌零件，复刻精度立刻拉满。
5. **确认当前任务阶段**：
   - 默认阶段是 `prompt-only`：只生成可移植复刻 prompt。
   - 如果用户已经说"测试生成网站/做出来/开始复刻"，仍先输出或确认将使用的复刻 prompt，然后问一次：`是否继续用这份 prompt 在本地生成测试站？`
   - 只有用户明确确认后，进入 `implementation-confirmed`，执行 Phase 4。

### Phase 1 · 反推填槽（核心）

打开 **`references/inference-guide.md`**，按它的**视觉分析清单**把下面这套 slot 全部填满。原则：**能读到就转录，读不到就给一个"看起来精确"的推断值**——永远不要写"大圆角""深色背景"这种模糊话。

要填满的 slot（详见 inference-guide §0 的「截图来源 / URL 来源」对照表）：
- 开场锁定句（stack + 品牌名 + 段落地图 + 关键库 + 美学）
- **字体（必须落到具体可加载字款）** — 见下方「🔴 硬规则 1」，详见 `references/font-matching.md`
- 颜色 token（背景/主文/次文/强调/边框，每个 **exact hex + 所painted的表面**）
- 自定义 CSS 工具（玻璃/噪点/渐变文字）
- **资源（写成「拍摄级生成简报」让消费端 AI 自己生成；可选附一条 stock 兜底）** — 见下方「🔴 硬规则 2」，详见 `references/asset-sourcing.md`
- 段落清单与顺序、每个元素的 Tailwind class 串、**逐字文案**
- 动效（入场/滚动/hover/鼠标跟随/canvas）— URL 模式先按源码和渲染态取证；静态图才按 archetype 给确定数值
- 响应式断点阶梯、页面 title

> 静态截图也**必须**给大标题配入场动画、给 CTA 配 hover、给全屏区配 `100dvh`。首屏背景如果是摄影/航拍图，不能只静态贴图：必须给出代码级微动效（Ken Burns、慢速 pan/rotate、parallax、clip-mask drift 等）来模拟原站可能的视频/航拍运动，见 inference-guide §1.5。

#### 回归暴露出的硬门禁

1. **锚点对齐门禁**：`EST.`、年份、编号、侧边标签这类微文案必须锚定到它视觉上对齐的元素，而不是整段/整屏容器。例：`EST.` 与 `1998` 若贴着 wordmark 中线，就放进 wordmark wrapper，用 `top-1/2 -translate-y-1/2`。
2. **推演布局平衡门禁**：截图外推出来的 section 尤其容易失衡。任何左右分栏都要写 `Layout QA / alignment contract`：列宽、`items-*`、左右视觉重量、media/text 等高策略、长词是否会裁切、圆角媒体是否露出空白边。
3. **动效可感知门禁**：首屏摄影/航拍伪视频不能只是“有 animation 代码”。prompt 要给可感知幅度；实现回归时用 computed transform 或相隔 3-5 秒截图验证确实变化。
4. **生成图参考锁定门禁**：截图里真实存在的摄影/mockup图（电脑、手机、手持设备、卡片、空间、人物）必须走 image-gen 生成主体，不能为了工程可控改成 CSS 形状。生成简报要锁定画幅、主体比例、位置、屏幕内容、光影几何、裁切边界和页面叠层；`blank screen` 只能用于原图空屏或已规划 live perspective overlay 的情况。
5. **遮挡动效双状态门禁**：如果图片在静帧里挡住大标题/字标/CTA，prompt 不能只写最终遮挡位置。必须写 initial state（标题先完整可见、图片在下方/透明/缩小）和 final captured state（图片上移/淡入后遮挡标题），并给出 delay 或 scroll progress 的 exact transform。
6. **URL 源码动效门禁**：URL 模式下，只要原站存在 `canvas`、WebGL/OGL/three、custom element、液态光标、变量字体鼠标波纹、depth-map parallax、smooth-scroll timeline、hover shader/视频交互，就必须把它们写进 prompt 的 motion/component block。不能把 `c-aurora` 降级成静态渐变，不能把 `c-parallax-depth` 降级成普通图片，不能把 `fontVariationSettings` 鼠标波纹降级成普通 hover。
7. **原站 vs 复刻交互对比门禁**：URL 实现回归不能只截静态首屏。至少采集原站与复刻在同 viewport 下的 rest、mouse-left、mouse-center、mouse-right、scroll/hover 状态；比较 `canvas` 数量/尺寸、关键 custom element、字体变量变化、cursor rect/label、背景/景深 transform、hover 前后样式。缺失任何核心交互都不能判定完成。
8. **首屏开场截帧门禁**：URL 模式必须从页面刚开始加载时就截帧，不只等 `networkidle` 或最终首屏。若原站有 loader、品牌开场、人像/产品遮挡、颜色场切换、字标切换、视频首帧切换，prompt 必须写 `OpeningSequence`：每一阶段的素材、颜色、层级、timing、退出方式。当前测试站 `theunknown.tv` 的 `head-C5MOojJn.webp + loading-rays-BQXV9Jjo.svg → THE UN KNOWN wordmark → stable hero` 就是这种模式。
9. **URL 色调采样门禁**：首屏背景和动效色调不能靠肉眼概括。至少抽取 `:root` 变量、关键 canvas/背景容器 computed style，并从原站截帧采样 5-9 个代表像素/区域，prompt 中绑定到具体渐变 stops、shader uniforms、overlay opacity 或资产调色参数。若复刻首屏「颜色家族对但氛围错」，视为失败。
10. **滚动连续性门禁**：URL 模式的 scroll 不是只做页面可滚动。必须识别 smooth-scroll、sticky pin、section progress、横向 scrub、卡片堆叠、背景色场切换、canvas resize/repaint、cursor 文案变化。实现后至少采样 `0%, 10%, 25%, 50%, 75%, 100%` 或源站关键锚点，并记录 clone 同点截图/JSON；缺一段关键滚动动效就不能判定完成。
11. **交互流畅性门禁**：复刻不是只“有交互”。实现时要避免每帧 React state 驱动大 DOM；pointer/cursor/canvas/variable-font 更新优先用 refs + rAF + transform/CSS variables。回归时观察 hover/pointer/scroll 是否卡顿；若出现明显掉帧、抖动、事件滞后，先降采样/合并 rAF/减少重排再交付。
12. **时间序列层级门禁**：元素堆叠错误通常来自截帧时间点错。URL 模式必须把每个关键层写成 `stage/timestamp/z-index/opacity/transform/exit condition`，并注明「该层只在开场阶段存在」或「稳定态仍存在」。实现回归要按同一时间序列比对，而不是把不同时间点的元素同时堆到稳定首屏。
13. **同视口锚点对比门禁**：URL 实现回归必须用同一 CSS viewport、同一 DPR、同一滚动锚点对比原站和复刻；优先按源站真实 section 文案/选择器定位（如 `THE MODEL...`、`GOOD HOUSING...`），不要只按百分比滚动。每个锚点输出 `original_*.png`、`local_*.png`、`compare-report.json` 和可浏览的双栏 `index.html`。没有记录就不能说“已逐屏对比”。
14. **fresh profile 开屏复现门禁**：URL loader/opening 只出现一次时，必须用全新浏览器 profile、禁用 cache、cache-busting URL 重新请求原站；不能用已经看过一次的浏览器判断开屏。至少记录 `t80/t2600/t3600/t5200/t5600/t6000/t6400/t7000` 或覆盖源站变化点的帧。
15. **CSS 框架污染门禁**：实现时必须审计框架默认样式是否污染复刻。Tailwind 的 `.container`、全局 `max-width`、默认 `box-sizing`、body font/letter-spacing、section `overflow`、sticky/fixed wrapper、image reset 都要用浏览器读 computed/bounding rect 验证。若容器宽度被 Tailwind 默认断点夹成 768/1024/1280 而源站是栅格全宽，必须显式覆盖 `max-width: none` 或不用 `.container`。
16. **真实数据基数门禁**：URL 模式不能把源码中的循环数据、项目卡、图片列表写成占位或无限重复。先从 DOM/脚本/资源中数清真实条目、真实图片 URL、真实缺口；缺图才生成 brief。复刻里出现重复模块、placeholder 图、循环陷阱或无图卡片，视为失败。
17. **源站断点状态门禁**：不要把不同 viewport/缩放/截帧状态混成一个布局。原站在 1000px、1440px、移动端可能有不同卡片列数、sticky 行为、文字换行、footer auto layout；prompt 和实现都必须记录该截图/对比使用的 viewport，并按同一 viewport 判定差异。
18. **无新增蒙层门禁**：若原站没有稳定态 dark overlay、渐变遮罩或灰色遮挡层，复刻不能为了“增强对比”添加。overlay 只能来自源码/截帧证据，并且要注明开场态或稳定态；尾幕/CTA/footer 尤其要核对是否存在额外蒙层。
19. **首屏前景遮挡层级门禁**：若 hero 里有「背景山/渐变场 + 内嵌 mockup/弹窗/UI + 前景山/树/雾/黑场」这类纵深构图，必须把每层写成 `role/z-index/DOM order/scroll transform/mask or clip/exit condition`。前景山体必须在 mockup 上方形成形状遮挡；黑色收尾只能填补前景层下方的真实黑场，不能压住 mockup 的可见主体，也不能在滚动中露出 mockup 的矩形尾巴、顶部切割条、灰/紫色残片或源站不存在的稳定蒙层。实现后必须采样首屏出场动画和第一段滚动的连续帧，而不是只看 `scrollY=0`。

#### 🔴 硬规则 1 · 字体永远落到具体可加载字款（不留占位）

我们做的是**复刻**，不是原创——字体必须给到一个**真实存在、能直接加载**的字款，并附**真实加载地址**：
1. 截图按字形分类（衬线/无衬线、对比度、x-height、字脚、宽窄、是否斜体/花体），匹配到具体字款。
2. **优先 Google Fonts**（注意西里尔/中文等字符集支持）。
3. Google Fonts 没有的花体/异形显示字 → **联网识别+找替代**（WhatTheFont / Fontspring Matcherator 识别 → Fontshare / Bunny Fonts / onlinewebfonts CDN 找真实免费字款），给出真实 `@import`/`<link>` 地址。
4. URL 模式直接读 `getComputedStyle().fontFamily` + `<link>`/`@font-face` 真实地址。
- **绝不**写 `[inferred, swap]` 这种让用户自己换字体的占位。完整方法见 `references/font-matching.md`。

#### 🔴 硬规则 2 · 素材必须能被「消费端 AI」零负担地变出来（绝不甩给用户）

目标不是让**用户**补素材，而是让拿到 prompt 的 **AI 自己完成素材闭环**。区别于占位：`REPLACE-ME` 是给用户留空（错），**真实稳定 URL** 或 **生成简报** 是给 AI 留可执行素材规格（对）——用户始终零负担。

**截图默认机制 = 在 prompt 里为每个图/视频写一段拍摄级「生成简报」**：媒介 / 拍摄视角 / 镜头焦段感 / 构图骨架 / 主体与主体细节 / 前中后景 / 焦点与留白 / **色调对齐本页色板** / 光线 / 质感 / 宽高比 / `object-position` / 「**无文字、无水印、无 logo**」/ 风格。这样自带图像生成的工具（具备 OpenAI image generation 权限的 Codex 环境、Gemini、v0、Lovable、bolt 等）能直接生成；没有生图权限时，这些 brief 仍然是可移植素材规格。
**URL 默认机制 = 真实可抓资源优先**：公开稳定的源站图片、视频、字体、SVG、Lottie/JSON 要作为 prompt 主资产写入；只对不可抓取或不可稳定复用的资源写生成简报。
- 两种机制都保持**单文件、可移植、跨工具**：prompt 里只有文字规格、真实 URL 或生成简报，没有要用户随附的文件。
- 想兼容**不会生图**的工具（如纯 Claude Code/fetch-only 环境）→ 每个素材**可选**再附**一条**真实免费 stock 直链兜底（见 asset-sourcing.md 的已核验源）。默认不附；只有 `target_asset_mode = fetch-only` 时才附。
- 只有当**截图模式**必须复用截图里的那张照片（强 1:1 像素级）才退而求其次从截图裁切；这是兜底，不是默认。
- 完整写法（生成简报怎么写、stock 直链、裁切命令）见 `references/asset-sourcing.md`。

### Phase 2 · 按模板组装

打开 **`references/prompt-template.md`**，把填好的槽渲染进它的 12 个 BLOCK 骨架（开场锁定句 → 字体 → 颜色 → 资源 → 自定义 CSS → 自定义组件 → **逐段子模板** → 共享动画组件 → 响应式 → 设计原则护栏 → tech stack 复述）。

同时全程遵守 **`references/conventions.md`** 的精度规则（这是让复刻确定化的"家规"）：
- **transcribe, never paraphrase**：能复制就复制。
- 颜色一律 exact hex/rgba 且绑定表面；近似色要说清各自怎么应用。
- Tailwind class 串**逐字照抄**，含 `[..]` 任意值 + 完整 `sm/md/lg/xl` 阶梯。
- 布局/对齐也必须写成字面量：左右列比例、等高策略、微文案锚点、长词断点字号、圆角媒体裁切/`object-position`，不能只说“左右排版”。
- 动效给齐 from→to / duration / delay / easing 数组 / stagger 公式 / 触发 hook。
- 招牌 CSS（liquid-glass/noise/渐变文字）**整段 CSS 贴出**，变体写成 diff。
- 重复行为**定义一次为具名组件契约**，再按名引用（直接取自 component-library.md）。
- 加**否定约束**压掉"看起来合理但错"的默认（`No overlay`、`No purple`、`No other UI libraries`、`loop OFF`）。

命中招牌效果时，**直接从 `references/component-library.md` 把对应小节的精确代码搬进 prompt**，不要口头重描。

### Phase 3 · 自检 & 交付

1. 跑一遍 prompt-template 末尾的 **「QUICK CHECKLIST」**（每个颜色都是 hex？每个素材都有生成简报或稳定 URL？每段文案都逐字带引号？每个动画都有数值？等）。
2. 在产物**顶部**放一个简短的 **「素材与字体清单」** 块：用了哪些字款（附真实加载地址）、`target_asset_mode` 是什么、每个图/视频的授权/内部用真实稳定 URL、`replace before production` 原站参考，或**生成简报**（`fetch-only` 时再加 stock 兜底直链）。**不应有 `REPLACE-ME`**——每个素材要么是一条真实可用直链，要么是一段可生成的简报。
3. 做一遍 **Image Brief QA**：检查每个生成图 brief 是否与参考图逐项一致：画幅/裁切、主体占比、主体位置、屏幕是否有内容、光影方向、遮挡关系、最终 object-position。发现 `blank screen`、通用产品照、CSS 替代真实摄影主体等偏差，先改 brief 再交付。
4. 做一遍 **Layout QA**：检查每个 inferred section 是否存在左右失衡、大块空白、长词裁切、圆角媒体露出空白边、微文案锚点错误；发现风险就在 prompt 中补具体 class 和约束。
5. 做一遍 **Screenshot Frame QA**（截图模式）：把用户给的每张截图列成 `REFERENCE_FRAME_N`，prompt 中明确哪些内容是截图可见事实、哪些是截图外推断；实现后必须逐张截同 viewport 对比。
6. 做一遍 **URL Motion QA**（仅 URL 模式）：列出从源码/渲染态确认的 motion primitives，并确保 prompt 中都有对应的具名组件或 CSS/JS 算法：loader/opening sequence、canvas/WebGL、鼠标跟随、变量字体、scroll timeline、hover state、首屏前景遮挡/mask/clip 层级。若只写了“添加微动效/渐变背景”，或把前景山/树遮挡降级成矩形黑块，视为失败。
7. 交付这份**可直接粘贴**的复刻 prompt。然后告诉用户：它可以喂给 Codex / Claude Code / Cursor / v0 / bolt 使用。
8. **实现门禁（硬规则）**：交付 prompt 后必须停在一个明确确认问题上：`是否继续用这份 prompt 在本地生成网站？` 用户确认前，不创建项目、不写代码、不调用生图、不启动 dev server。

### Phase 4 · 用户确认后实现 & 回归（Codex 专用）

只有用户明确确认继续生成网站时才执行。

1. **创建临时测试项目**：默认放在当前工作区的测试文件夹，避免安装到用户级/项目级 skill 库。
2. **按 prompt 构建**：优先 `React + Vite + TypeScript + Tailwind + Framer Motion + lucide-react`；若 prompt 指定单文件 HTML，则遵守 prompt。
   - 若使用 Tailwind，先决定是否禁用/绕开默认 `.container`；任何自定义 `.container` 必须显式 `max-width: none` 或写清断点约束，避免框架默认断点破坏源站栅格。
3. **素材执行策略**：
   - 能从 URL 稳定抽取真实资源时，优先用真实资源。
   - 截图模式默认根据 prompt 的拍摄级 brief 调用当前可用的图像生成工具；如果本环境没有生图工具/API 权限，就保留 brief、切到 `fetch-only` 兜底或明确记录素材缺口。生成成功后把图片复制进项目 `public/assets/`。
   - 不使用 `REPLACE-ME`、`placehold.co`、死链或要求用户补图。
4. **首屏和动效实现**：摄影/航拍背景必须有真视频或代码微动效；大标题、CTA、nav hover、section reveal 必须落到具体数值。URL 模式若原站使用 canvas/WebGL/custom elements，应优先复用源码中可公开读取的资源和参数，或按同等算法实现，而不是用普通 CSS 静态近似替代。
5. **动效回归**：首屏伪视频必须验证“可感知”：读取背景层 `getComputedStyle(el).transform`，或相隔 3-5 秒抓两张截图对比；如果几乎看不出来，增大 translate/scale/rotate 幅度，而不是加装饰。URL 模式还要按 `references/url-regression-protocol.md` 做原站/复刻同点位对比：fresh opening frames、stable rest、mouse-left/center/right、source anchors scroll、关键 hover、mobile/menu。
6. **视觉回归**：构建后至少抓桌面和移动截图；长页则补 full-page 或高视口截图。截图模式必须逐张对齐用户上传的 `REFERENCE_FRAME_N`；URL 模式必须同时对齐源码事实和浏览器截帧。重点检查：横向溢出、层级、静态背景、字体/色板偏差、推演区块左右失衡、圆角/对齐问题、长词裁切、URL 源站存在但复刻缺失的 loader/canvas/鼠标/scroll/hover 动效、首屏前景遮挡与 mockup 裁切泄漏、CSS 框架默认样式污染、源站不存在的额外蒙层、重复模块/placeholder 图。发现就直接修到可用。
7. **最终只汇报高信号结果**：项目路径、预览 URL、截图路径、`compare-report.json`/双栏对比页路径、构建状态、原站/复刻 motion 对比结论、已知偏差。

---

## 参考文件（按需读取）

| 文件 | 何时读 | 内容 |
|---|---|---|
| `references/inference-guide.md` | **Phase 1 必读** | 截图/URL → 槽位的反推方法论：视觉清单、字体/颜色/动效如何从像素猜、URL 模式抓什么、ask-vs-infer 决策、worked example |
| `references/prompt-template.md` | **Phase 2 必读** | 复刻 prompt 的 12-BLOCK 主骨架 + 逐段可复用子模板 + 出货前 checklist |
| `references/conventions.md` | **Phase 2 必读** | 让复刻确定化的精度"家规"：exact-value 规则、资源 pinning、组件契约、否定约束、反模式对照表 |
| `references/font-matching.md` | **每次定字体必读** | 截图字形 → 具体可加载字款：视觉分类、Google Fonts（含西里尔）映射、花体/异形字的联网识别与真实加载地址（Fontshare/Bunny/onlinewebfonts）|
| `references/asset-sourcing.md` | **每次处理素材必读** | 让消费端 AI 变出素材的方法：图像生成 brief 怎么写（首选）+ fetch-only 免费图/视频直链兜底（Unsplash/Pexels…需现查核验）+ URL抽取/截图裁切（强 1:1 兜底）+ 授权/生产替换边界 + 决策优先级 |
| `references/component-library.md` | 命中招牌效果时 | liquid-glass / FadingVideo / BlurText / ScrambleIn / Magnet / 光标聚光 / ScaledDashboard 等精确可复用代码 + 「截图信号→命中组件」速查 |
| `references/external-benchmarks.md` | 更新流程或评估效果时 | 从 screenshot-to-code / Motionity / CopyWeb 提炼的可借鉴机制与不可照搬边界：prompt routing、asset extraction、preview loop、timeline motion、实现门禁 |
| `references/url-regression-protocol.md` | **URL 实现回归必读** | 从 theunknown + Eleos 回归中固化的低自由度流程：fresh profile 开屏截帧、同视口锚点对比、CSS/Tailwind 审计、真实数据基数、断点状态、双栏证据产物和失败判定 |
| `references/examples/` | 想看语料风格时 | 5 个旧版真实复刻 prompt 语料样本。只用于观察写法、组件和数值密度；最终交付必须按 `prompt-template.md` 的当前模板补齐授权范围、素材清单、Reference Frames、回归计划和确认门禁。 |

> **可选本地语料库（非 skill 依赖）**：`网页复刻-参考提示词库/` 是作者本机可能存在、会持续扩充的原始 prompt 语料库，不随本 skill 安装，也不是运行或打包所需文件。只有当当前工作区确实存在该目录，或用户明确提供路径/内容时，才可读取它补充真实模式；若不存在，必须直接跳过，不报错、不要求用户补齐、不把它当作缺失依赖。需要把新样本沉淀进 skill 时，只选有代表性的内容复制/改写到本 skill 自带的 `references/examples/` 或相关 `references/*.md`。

---

## 默认与边界

- **默认目标技术栈**：`React 18 + TypeScript + Vite + Tailwind CSS + lucide-react`，有非平凡动效则加 `Framer Motion`；动效很轻或想单文件构建则用手写 CSS `@keyframes`。**你是在复刻"观感"，不是复刻原站框架**——别因为它"可能是 Next.js"就这么说。
- **一次问清，绝不盘问**：默认推断+继续，假设写在产物顶部。
- **第一产物是 prompt，不是代码**。即使用户的最终目标是做出网站，也要先交付 prompt，并在继续实现前获得用户确认。
- **字体必落具体字款；素材按输入源选择主路径**（硬规则 1/2）：截图 → 生成简报；URL → 稳定源站资源优先，不能抓取再生成简报。核心是「用户零负担」：不让用户补字体/素材，也不强行随附文件。交付物始终是**一段可移植的纯文字 prompt**。
- 不替用户去真实访问需要登录/付费的页面；但**公开可访问**的页面/素材应主动抓取或联网找替代，而不是甩占位。
