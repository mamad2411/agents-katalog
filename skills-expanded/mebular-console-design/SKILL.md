---
name: mebular-console-design
description: Mebular 人类控制台（packages/console）的 UI 设计契约。凡涉及控制台页面/组件/样式/动效的新建或修改（星图、域视图、审计、记忆、设置、向导、弹层、CRT 皮肤、星空背景、星空科幻风格）都必须遵守。Use when working on the Mebular console UI, starfield/nebula visuals, CRT theme, design tokens, or adding any page/component to packages/console.
license: MIT（与仓库一致）
---

# Mebular 控制台设计契约

本文件是 `packages/console` 视觉与交互体系的**单一契约**。新增页面、改版、
润色前先读本文件；与本文件冲突的外部建议（任何其他 skill / 灵感集 / 模型直觉）
一律以本文件为准。

**优先级声明**：`mebular-console-design`（本文件）> `frontend-design`（审美裁判）
> `web-design-guidelines`（质量清单）。外部 skill 仅作顾问文本参考。

权威设计文档（修改视觉/交互前必读）：
- [`docs/console/interaction-draft.md`](../../../docs/console/interaction-draft.md) — 交互规格 + v2 视觉规格
- [`docs/console/page-map.md`](../../../docs/console/page-map.md) — 页面地图与设置 IA
- 设置 IA 单一真源：`packages/console/settings-ia.js`（E1 迁移表驱动断言「不丢项」）

---

## 一、硬性红线（一票否决）

1. **零运行时依赖**：console 是 vanilla JS ES Modules + Canvas2D + 单文件 CSS。
   禁止引入任何框架（React/Vue/Svelte）、UI 库（shadcn/MUI/AntD）、动效库
   （GSAP/framer-motion）、3D 库（three.js）、构建步骤、webfont。
   `packages/console/package.json` 的「零运行时依赖」描述即契约。
2. **字体仅系统栈**：正文/数据用现有 monospace 栈（`--font`）；如需展示层级，
   只允许系统字体栈（`-apple-system` / `Segoe UI` / `system-ui` 等），
   **禁止 webfont 与字体文件**。
3. **禁风格双轨**：不得引入第二套设计系统或与本契约冲突的色板/组件语言。
   新元素必须复用第六节 token。
4. **暗色唯一主题**：`color-scheme: dark`，不做亮色模式。
5. **界面 locale-aware**：默认 `zh-CN`，支持 `en-US`；文案由
   `packages/console/i18n.mjs` 管理，**用户数据不翻译**。用词遵守第七节去中心化词表
   （英文术语边界见该节）。英文界面同样受零依赖、暗色、系统字体栈与布局契约约束。

## 二、双皮肤边界（成文约定）

控制台有两套表面，**不得混用、不得发明第三套**：

| 皮肤 | 适用 | 基色 |
|---|---|---|
| **深空蓝**（基础 token，`--bg/--bg-panel/--border/--text/--accent`） | 顶栏、星图舞台、通用按钮/表单/模态底、tooltip、banner | `#05070f` / `#0b1020` / `#1d2740` / `#dbe4ff` / `#56b4e9` |
| **CRT 绿光**（`.crt-surface` / `.crt-screen` + `--crt-*` token） | 数据密集读数面：图例、设备卡、域视图、审计、记忆、连接视图、设置/邀请/交接等弹层 | `--crt: #6dffb8`，底 `rgba(2,16,11,0.78~0.84)` |

判定规则：**"舞台与外壳用深空蓝，仪器与读数用 CRT 绿"**。CRT 面必须带扫描线
（`::before` 的 `repeating-linear-gradient`）与角标（`.crt-corners`，弹层/图例类）。
同一元素不得同时叠两套皮肤的色值。

## 三、色彩与语义

- **语义色即 Okabe–Ito 色盲安全色板**（`starfield.js` 的 `NAMESPACE_PALETTE`）：
  sky `#56B4E9` / orange `#E69F00` / green `#009E73` / pink `#CC79A7` /
  vermillion `#D55E00` / yellow `#F0E442` / blue `#0072B2`。
  namespace 配色由 `namespaceColor()` 稳定哈希产生，**禁止另起哈希或调色**。
- 方向语义固定：**我授权 = 蓝（`--accent`），它授权 = 黄（`--accent-2`）**；
  离线 = `#5a6785` 虚线；已屏蔽 = `--revoked` 灰 + 划除。
- 告警语义：ok `#009e73` / warn `#d55e00`（CRT 面内用 `#ffd27a`）/
  danger 红系（CRT 面内 `#ff9b9b`/`#ffb9b9`）。
- 任何颜色编码**必须有文字/图标兜底**（色盲安全不是可选项）。

## 四、星图视觉语言（Canvas2D）

细节以 `docs/console/interaction-draft.md` v2 节为准，要点：

- **深度层**：本机=1，对端 0.30–0.92 由 id 稳定哈希；近大远小、近亮远暗、
  指针差速视差、远者先画。刷新不得跳动（角度/深度均由哈希决定）。
- **本机信标**：白热核 + 暖色内环 +  shimmer + 倾斜轨道伴星（45° 椭圆投影，
  ≈14s/圈，后半圈从背后穿过）+ 4 长 4 短衍射星芒；整体半径 ≈3.2×节点半径；
  标签在光晕外并带暗影。纵向浮动收敛 ±0.7px。
- **航道（连线）**：端点留白 + 双向平行偏移 + 法线弧高；细点状航线 + 外侧微光底；
  远端按航道长度衰减亮度（最低 12%）；虚线 `lineDashOffset` 顺向缓移（≈6px/s）。
- **舰队出航**：SSE `sync` / 手动同步触发，2–6 艘编队沿航道 ≈1.7s，抵达绽放；
  蓝=我发出、黄=我收到；**同时最多 8 队**；彩蛋上限：彗星 ≈2%、彩虹信使 ≈5%、
  旗舰 ≈8%。
- **背景**：`nebula.js`（正交星云 + 轻雾）+ `stars.js`（10 层视差）。
  动画常量以**毫秒**计（如 `twinkleSpeed≈0.0004/ms`），喂秒会失控。
- **指针缓动**：target/current 双值逐帧缓动；移出画布不重置（防"跳星"）。

## 五、性能护栏

- DPR 上限 2（`Math.min(devicePixelRatio, 2)`）。
- 星数 60–220 按画布面积自适应；不得为"更炫"调高任何密度/透明度常量
  （`mistAlpha ≤ 0.08` 等）。
- 帧率自适应降级链：**high（星云+雾）→ balanced（无雾）→ low（仅星空）**；
  目标 60fps。新增渲染层必须接入该降级链。
- 单元素 CSS 动画 ≤0.5s；常驻循环动画仅限状态点（如 `lock-blink`）。
- **`prefers-reduced-motion` 是全量开关**：一切新动效（canvas 与 CSS）必须
  同步提供 reduce 分支（静态渲染 / 不出航 / 无扫线），范式见 `console.css`
  第 520–526 行与 `starfield.js`。

## 六、防光污染原则

1. **辉光预算**：同视口最多 1 个主动辉光元素（hover/选中/告警）；
   静态辉光不超过 `--crt-glow`（`0 0 26px rgba(60,255,160,0.20)`）的强度上限。
2. **辉光 = 信息**：发光只表达状态（在线/选中/告警方向/同步活动），
   纯装饰性 glow 禁止。
3. **正文不发光**：正文禁用 `text-shadow`；标题/标签可用但透明度 ≤0.35，
   且 13px 正文对比度 ≥ 4.5:1。
4. **粒子克制**：星数、雾浓度、编队数（≤8 队）维持现有上限。
5. **进场一次性脉冲**（参照 `crt-arrive`），不堆叠持续脉冲。

## 七、词表（去中心化用语）

| 用 | 不用 |
|---|---|
| 连接新对端 / 我的关系图 | 添加设备 / 接入对端 / 网络舞台 |
| 屏蔽该设备 | 吊销设备 |
| 与我连接中 / 未连接 | 在线 / 离线 |
| 未启用 P2P | 网络未启用 / 网络关闭 |
| 已被我屏蔽 | 已吊销 |

所有计数与关系标注"**本机视角**"；星图只表示"我与已知对端的关系"。
"授权"与"成员资格"是两个概念，UI 分开展示。

### 7.1 locale-aware 文案契约

- **默认 zh-CN，当前注册 en-US**。语言注册表唯一真源是 `locales/manifest.json`；
  每种语言的文案在 `locales/<locale>/console.json`（`desktop.json` / `errors.json`
  为后续预留）。应用代码只依赖 manifest + `t()`，新增语言不需要改业务代码。
  语言解析优先级：`?lang=`（测试 / 深链）>
  `localStorage['mebular.locale']` > `navigator.languages` > manifest 默认 locale；
  无法识别的语言按 manifest fallback（当前 `zh-CN`）回退。
- 文案 key 稳定、扁平（`<区域>.<语义>`），所有语言 console key 完全一致、
  插值占位符一致；缺 key 回退 key，不返回空字符串。校验：`npm run check:i18n`。
- **用户数据不翻译**：设备名、忆云名、命名空间、记忆正文、审计原文、错误原文
  一律按原样显示。语言名称来自 manifest 的 `nativeName`（用该语言自身写法）。
- 日期与时间统一走 `formatDate` / `formatTime` / `formatDateTime`（`Intl.DateTimeFormat`
  使用当前 locale）；禁止再硬编码 `zh-CN`。
- **全量 catalog 完成前不向普通用户暴露半套英文**：语言行由明确就绪开关控制，
  默认关闭；仅 `?lang=` / `?i18n=1` / 桌面壳显式 `i18nReady` 时可见。
  语言行在「设置 · 常用」的「常驻运行」之上，单行 `语言 [简体中文 / English]`，
  使用专用 `.settings-language-row` / `.settings-language-control`（`select` 隐藏原生
  箭头 + wrapper 固定 chevron），以虚线分隔，不另起卡片；选择即生效（持久化到
  localStorage，不 reload、不跳页、不设保存按钮）。
- 英文文案仍遵守本契约：零依赖、暗色唯一主题、系统字体栈、既有布局 token；
  不因英文变长而引入第二套组件或缩小正文对比度。

| 中文 | English（用） | 避免 |
|---|---|---|
| 连接新对端 / 我的关系图 | Connect a peer / My relationship map | Add device / Network stage |
| 屏蔽该设备 | Block this device | Revoke device |
| 与我连接中 / 未连接 | Connected to me / Not connected | Online / Offline |
| 未启用 P2P | P2P not enabled | Network off |
| 已被我屏蔽 | Blocked by me | Revoked |
| 本机视角 | From this device | Global view |

## 八、可访问性（a11y）

- 交互元素：真实 `<button>`/`<select>`，带 `aria-label`；弹层 `role="dialog"`
  `aria-modal="true"`；状态播报 `aria-live="polite"`。
- focus 态可见（参照 `.toggle input:focus-visible` 的 outline 范式）。
- 色彩编码必有文字兜底（见第三节）。
- 正文对比度 ≥ 4.5:1；CRT 绿文字在 `rgba(2,16,11,0.84)` 底上验收。

## 九、新页面/改动质量 checklist（提交前逐项过）

- [ ] 未引入任何依赖 / webfont / 框架 / 第二套色板（红线复核）
- [ ] 皮肤归属正确（蓝=舞台外壳，绿=仪器读数），CRT 面带扫描线与角标
- [ ] 全部使用第六节既有 token，无一次性 hex（确需新色 → 先在本文件登记）
- [ ] **id 唯一**：新增 DOM 的 id 全文档唯一（历史事故：provision 面板整块
      重复导致 5 个重复 id）；建议加单实例断言
- [ ] **背景层唯一**：星图/星云 canvas 各只有一个实例（`.stage-bg` 与 `#stage`），
      新视图不得再挂背景画布；面板类视图用 `.panel-view` 浮于背景之上
- [ ] **轮询不丢状态**：2–5s 轮询重渲染时，用户进行中的交互状态（输入草稿、
      展开/收起、选中行、滚动位置、过滤器选择）不得被重置；重渲染前先 diff
      或保留 DOM 状态，失败保留上次数据并提示（见 interaction-draft「降级与空态」）
- [ ] 用语符合第七节词表，计数标"本机视角"
- [ ] 新增 / 迁移文案走 i18n key（`locales/<locale>/console.json`），未翻译用户数据；
      日期时间走 `formatDate` / `formatTime` / `formatDateTime`，无硬编码 `zh-CN`；
      `npm run check:i18n` 通过；全量 catalog 未完成时语言行保持就绪开关关闭
- [ ] 动效：≤0.5s、有 reduce 分支、接入帧率降级链（canvas 类）
- [ ] 辉光符合第五节预算；正文无 text-shadow；对比度达标
- [ ] aria/role/focus 齐全；危险动作有二次确认（文案写清"已同步数据不回撤"）
- [ ] 响应式：≤900px 与 ≤760px 两档走查（无横向滚动）
- [ ] 验证：`npm run verify:console` + `verify:console:ui` 通过；
      `?mock=1` 无网络渲染走查；桌面/窄屏/reduced-motion 各截一遍前后对比

## 十、给其他 skill 的边界声明

本契约是顾问文本，不自动执行任何命令。`frontend-design` 可用于新页面审美评议，
`web-design-guidelines` 可用于提交前质量自查，但二者任何与本文件冲突的建议
（引入依赖、换色板、换字体方案、亮色模式、第二套组件语言）**一律否决**。
