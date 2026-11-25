---
name: game-copycat
description: >-
  复刻网页小游戏，可选部署到 Cloudflare。当用户想"复刻/克隆/仿/照着做/copy/clone"某款游戏——
  给出游戏名、X/推特帖子链接、App Store/Google Play 页面、游戏截图或视频——或说"做一个像 XX
  的游戏""把这个手游/小程序游戏做成 web 版""实现一个 2048/数织/Queens/Tango/Zip/Wordle/
  Connections/数独/消除/合成/纸牌类小游戏""找个热门小游戏复刻一个"时使用，即使用户没说
  "复刻"二字、只丢来一个游戏链接问"能不能做一个"也算。覆盖调研原作 → 玩法复刻 + 原创
  换皮 → Vite+React+TS 实现与测试 → 浏览器自验 → 可选 wrangler 部署的端到端流程。
  Use whenever the user wants to clone, replicate, remake, or "build something like"
  a casual puzzle/board/card web game from a name, link, or screenshot.
---

# game-copycat：复刻 web 小游戏

输入一个游戏参考，输出一款**成品级**可玩游戏：UI 精致、有手感、部署在 workers.dev 上可直接分享。整个流程八个阶段，每个阶段有出口门禁，门禁不过不进下一阶段。

## 适用范围

- **适用**：益智休闲类——棋盘逻辑（Queens/数织/数独/Zip）、文字（Wordle/Connections）、数字合成（2048）、消除、纸牌、回合制小游戏。DOM + CSS 能做精致的都算。
- **不适用**：3D、实时对战、物理引擎重度（跑酷/弹球）、需要后端的游戏。遇到时明说不适用并给降级建议（如"物理类建议 Canvas + 专门引擎，本 skill 范式不适配"），不要硬做。

## 全局约定

- **技术栈统一**：Vite + React + TypeScript，模板已固化（`assets/template/`），不引路由库/状态库/UI 组件库，不加后端。
- **原创化默认尺度**：玩法机制忠实复刻，但名称、品牌、配色、图形资产、关卡数据与代码**全部原创重新实现**；README 写原创化声明。用户明确要求更贴近原版时可以贴近视觉布局，但仍不复制任何原作素材文件。
- **产出路径**：默认 `games/<slug>/`（目录不存在就创建）；用户指定了路径则用用户的。
- **任务跟踪**：开工即建 8 个阶段的 todo，逐段推进，用户随时能看到进度。
- **诚信**：关卡不硬编码答案进 prompt 或代码注释；汇报只用实跑出来的数据；测试失败原样贴出。

## 八阶段工作流

### ① 调研原作

按 `references/research.md` 执行。三类输入（链接/截图/名字）各有处理路径。

- 用 web-access skill 抓原作页面与媒体，落 `games/<slug>/.research/`（此时 slug 未定就先落临时目录，③ 阶段移入）。
- 写规则说明书 `.research/rules.md`：核心循环、操作、胜负、计分、关卡结构、约束规则、边界情况、不确定项。
- **出口门禁**：规则说明书完整（不确定项已列出）+ 至少 2 张参考截图落盘。抓取失败 2-3 次就停，请用户补截图或口述规则。

### ② 开工确认

向用户一段话汇报，拿到认可或无异议再动手：

> 我理解的目标：复刻 <原作>（<一句话玩法>）。原创名称提案：<slug/中文名>。改版尺度：<默认原创换皮/用户特殊要求>。风格方向：默认 <一句话视觉基调>，另出 <n> 套备选主题，交付后设置里可切换。验收标准：本地可玩、npm run check 绿、浏览器审计全绿。计划：脚手架 → 内核+测试 → UI+手感 → 自验审计 →（用户要求时）部署。
>
> 待确认：<规则说明书里的不确定项，逐条问>。

- 玩法歧义**必须在此问清**，之后不再打断用户；无歧义且用户在场确认过方向，直接继续。
- **风格方向必须带质感样板**：用户点名过认可的作品/项目（"要像 XX 那样"）就以它为质感真源，⑤ 阶段逐屏对照它收敛；没有样板时用一句话形容词不算确认——先给 1-2 个具体锚点（参考截图本身的气质 vs 卡通圆润等方向）让用户挑。实战教训：对标参考图做了奢华风、审计全绿，但用户要的是卡通感，整套视觉返工。
- **出口门禁**：规则零歧义，原创名与 slug 确定（slug 会成为 `<slug>.workers.dev` 子域名）。

### ③ 工程脚手架

```bash
node <skill目录>/scripts/new-game.mjs <slug> [games]
```

复制模板、替换占位名、npm install、`npm run check`。把 ① 的 `.research/` 移入项目。

- **出口门禁**：空骨架 `npm run check` 绿。

### ④ 游戏内核先行

UI 一行都不写，先把规则做成可证明正确的纯函数库。按 `references/engineering.md` 执行：

- 分层：types → prng（模板已给）→ engine（纯函数，零 DOM）→ 逻辑谜题类再加 solver（`countSolutions(limit=2)` 唯一解判定）→ generator（种子确定性）。
- 关卡构建期固化：`npm run gen:levels` 离线生成 → `src/data/levels.ts` 静态导入，运行时零生成。
- vitest 属性式门禁：全部关卡断言唯一解（或非唯一解类的状态机不变量：守恒、合法性、终局判定）。
- **出口门禁**：`npm run check` 绿；engine 层无任何 DOM/React import；唯一解类全部关卡 `countSolutions === 1` 测试通过。

### ⑤ UI + 原创化 + 手感

- **设计令牌先行**：对照 `.research/` 截图提取布局结构与视觉语言，但换成原创色板/品牌，全部写进 `src/styles/tokens.css`，组件只用 var()。
- **原创 ≠ 无锚点**：换皮前先把新视觉的基线定死——展示字体（@fontsource 真装，交付物的 --font-display 不得是纯 system 栈）、完整色板、图标体系（lucide 或自绘 SVG，**UI 控件里禁止拿 emoji 当图标**，分享文案除外）、背景质感（无纹理纯色底=未完成）、组件规格（图标 chip、双行按钮等结构照参考抄）。之后**每屏与参考图并排对照收敛**：抄结构、密度与质感档次，只换皮肤。精致来自对照收敛的循环，不来自模型即兴发挥——没有锚点的"原创"必然落进 emoji 按钮 + 系统字体的 AI 默认审美。
- **多主题**：默认主题写 `:root` 并深耕到底；再出 1-2 套备选主题（`[data-theme="<name>"]` 覆盖同名变量，如一套贴近原作氛围、一套大胆原创），settings 加主题切换并持久化。默认主题直接交付，用户不必选——备选是切换项不是待办项。
- 界面完整成品四件套：首页、游玩、玩法说明、设置（音效/语言/触感/主题），View 联合类型路由。
- 渲染惯例（稳定 id + FLIP、pointer 手势、双击陷阱、版本化 localStorage、中英 i18n、clamp 响应式）见 `references/engineering.md` 渲染层一节。
- **手感清单**：`references/juice.md` 逐项过，必做项（操作反馈、squash & stretch、过关庆祝、首局引导）缺一不可；加分项按游戏类型选。
- 图形资产手写 SVG 或用 lucide-react，不放原作任何图片。
- **出口门禁**：与参考截图并排对照，布局/交互对应但品牌视觉原创；390×844 无横向溢出；prefers-reduced-motion 下功能完好；`npm run check` 绿。

### ⑥ 浏览器自验审计

按 `references/audit.md` 的四组清单逐项过：功能与规则完备性（**失败路径必须玩到**，不能只验证赢）、移动端专项（横向滚动/触控目标/hover 粘滞/safe-area/极窄与横屏）、UI/UX 专项（双语溢出/对比度/键盘可达/reduced-motion）、截图对照。用 agent-browser 对 `npm run dev` 本地站真实操作，能写 DOM/CSS 断言的不靠截图目测——用户不是 QA，交付后被用户指出的每个问题都是本阶段的漏检。

- **出口门禁**：audit.md 四组全绿。发现问题回 ⑤/④ 修，修完重跑全部四组。

### ⑦ 部署（须用户确认）

**部署前必须过两道确认，不确认不部署**：
1. `wrangler whoami` 查当前认证的是哪个账号，把账号名报给用户——个人项目部到公司账号是事故，不是便利。
2. 用户在本轮对话里明确要求部署才部；只说"复刻一个游戏"默认停在 ⑥ 的本地验证，交付本地 URL。

确认后按 `references/deploy.md`：`npm run deploy`（build + wrangler deploy），curl 冒烟 200，真实浏览器打开线上 URL 玩一局。认证失败/name 冲突的兜底见该文档，认证操作提示用户自己做、不代做。

- **出口门禁**：（部署时）workers.dev URL 在线可玩；（不部署时）本地 `npm run dev` 可玩即交付。

### ⑧ 交付汇报

- 补全 README：玩法、运行方式、**原创化声明**、与原作已知差异清单。
- 汇报格式：干了什么 → 证据（线上 URL、check 输出、E2E 截图）→ 自评分（功能完整性/UI 还原度）→ 已知差异与下一步建议。
- **出口门禁**：用户拿到 URL 一键打开可玩。

## 并行执行点

有 subagent 能力时用并行换时间，没有就按序执行，产出与门禁不变：

- ①：多渠道调研（页面抓取、规则检索、商店截图）并行发出。
- ④ 与 ⑤ 的令牌提取可并行——设计令牌只依赖参考截图，不依赖内核；但 UI 组件必须等 ④ 门禁绿了再写。
- ⑤：备选主题变体可各派一个 subagent——组件只消费 var()，主题是纯 tokens 覆盖块，互不冲突；关卡生成调参（跑不同种子/尺寸）也可并行。
- 不可并行的不要硬并：②的确认必须阻塞，⑥ 的审计要在完整产物上跑。

## 组合其它 skill

- 联网抓原作页面/媒体：**web-access**。
- 参考图 UI 还原思路：**image-to-code**；无参考图需要设计发挥：**frontend-design**。
- 浏览器自动化与截图：**agent-browser**。

以上 skill 缺失时降级执行，各阶段的产出与门禁不变：抓取用内置 WebFetch/WebSearch；浏览器自验用 playwright（`npx playwright`）或宿主自带的浏览器工具，⑥ 的四项验证照跑。

## 参考文件

| 文件 | 何时读 |
|---|---|
| `references/research.md` | ① 阶段开始时 |
| `references/engineering.md` | ④ 阶段开始时（⑤ 的渲染惯例也在此） |
| `references/juice.md` | ⑤ 阶段开始时 |
| `references/audit.md` | ⑥ 阶段开始时 |
| `references/deploy.md` | ⑦ 阶段开始时 |
