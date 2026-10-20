# 酒馆助手前端界面或脚本编写

@.cursor/rules/项目基本概念.mdc
@.cursor/rules/mcp.mdc
@.cursor/rules/酒馆变量.mdc
@.cursor/rules/酒馆助手接口.mdc
@.cursor/rules/前端界面.mdc
@.cursor/rules/脚本.mdc
@.cursor/rules/mvu变量框架.mdc
@.cursor/rules/mvu角色卡.mdc

<!-- TAVERN-RULES:START v1.1.0 -->
<!-- 本块由 tavern-harness/scripts/sync_tavern_rules.py 自动生成，请勿手动编辑 -->
<!-- 真源: tavern-harness · rules/ · 仓群 js-slash-runner · v1.1.0 -->
<!-- 同步时间: 2026-09-24T14:03:12+08:00 -->
<!-- 内容哈希: sha256:8b5878b07beb5dcc（仅覆盖规则正文，不含本头部与「项目覆盖」节） -->
<!-- 覆盖声明: 本仓如需覆盖某条规则，请在文末「项目覆盖」节声明并说明理由 -->

# 统一开发规则（v1.1.0）

> 本块为**自包含全文**，不依赖任何外部路径；由 `tavern-harness` 真源仓同步生成，请勿手动编辑。
> 适用仓群：**JS-Slash-Runner 仓群（酒馆助手脚本 / 工作区）**。

## 规则层级

- **MUST** — 硬性要求，违反即审查不通过
- **SHOULD** — 强烈建议，除非有充分理由
- **MAY** — 可选实践

## L0 全局规则（跨仓群通用）

> 适用于 `My-repo` / `Myfork` / `JS-Slash-Runner` 三大仓群的全部仓库。
> 标注「与全局同源」的条目同时存在于用户级 `~/.claude/CLAUDE.md`；在此重复收录是为了让
> Codex / Cursor / Gemini / Copilot 等**非 Claude** agent 也能读到（全局配置只对 Claude 生效）。

### L0-1 实例隔离铁律 (MUST) ｜与全局同源，仓群实践强化

**规则**：开发与测试只在**代码库工作区**内进行。**严禁**向本地酒馆实例目录（`D:\Repo\Tavern-repo\Instance\**`）复制、写入、删除、覆盖任何文件。实例获取插件/扩展只走三条路：`git clone` / `git pull`、酒馆原生扩展安装器、酒馆助手。

**原因**：`Instance/Real/**` 下是用户的**真实聊天数据**（GB 级，且含会话密钥文件）。人工复制文件是最容易发生的污染路径。

**违反后果**：真实聊天记录被覆盖或污染、会话密钥泄漏，且**不可恢复**（无回滚手段，属红线）。

---

### L0-2 计划先行铁律 (MUST) ｜与全局同源

**规则**：Trellis 任务在 `task.py start` 前必须回填 `prd.md`（Requirements / Acceptance Criteria 不得为 `TBD`）；复杂任务另需 `design.md` + `implement.md`。`implement.md` 的复选框**随执行实时勾选**，禁止任务结束后凭记忆批量补勾。

**原因**：前作 `09-12-multi-repo-rules-dev-env` 的教训——代码写完三片后 PRD 仍为 `TBD`，人机意图发生漂移，事后无法判断"完成"的定义。

**违反后果**：验收标准缺失 → 无法判断任务是否完成 → 返工重做。

---

### L0-3 检索先行（双通道）(MUST) ｜与全局同源

**规则**：动手实现任何功能前，**必须先检索**是否存在现成方案 / 工具 / 库 / 技能，不造轮子。双通道（两者都应尝试）：
1. `WebSearch` / `WebFetch`（可用时）
2. **GitHub API 检索**：`api.github.com/search/repositories`（可用 `gh search repos` 或 curl）

**国际搜索引擎被屏蔽时，用 GitHub API 替代**（`api.github.com` 在本机可访问）。**发起调用即算满足**——无命中结果同样放行。

**原因**：本机网络环境下通用搜索引擎不可靠，但 GitHub API 稳定可达；用户明确要求不重复造轮子。

**违反后果**：重复实现已有成熟方案，浪费工时并引入自维护负担（用户明确表示要避免"自己维护的地狱"）。

---

### L0-4 变更必须可审：diff 工具 + 块级编辑 (MUST) ｜与全局同源

**规则**：比较代码/文件变更**一律使用 diff 类工具**，不得仅靠肉眼通读全文。修改现有文件必须**块级替换**（`Edit`），禁止 `Write` 整文件覆盖；禁止用 shell 重定向 / `node -e` / `echo` 直接改写源码与数据。

**原因**：整文件覆盖会把未读到的内容静默丢弃；肉眼比对无法发现细微差异。

**违反后果**：静默丢失他人或历史的修改，且 diff 无法审出，事后追溯困难。

---

### L0-5 交互问答规范 (MUST) ｜与全局同源

**规则**：需要用户决策时**必须使用交互式问答工具**（Claude Code 的 `AskUserQuestion` 或其平台等价物），**严禁在正文里提问然后结束回合**（会阻塞流程）。每次聚合 ≥2 个问题。凡涉及**重大方向性决策**（架构取舍、重构 vs 重写、技术选型、大范围删除/迁移），必须先列出候选方案与利弊、给出推荐，经用户选定后再动手。

**原因**：正文提问会让用户面对无结构的长文本，且容易被忽略而卡住任务；结构化选项能让用户几下点完。

**违反后果**：流程阻塞或用户未注意 → agent 擅自拍板 → 方向性返工。

---

### L0-6 高风险操作安全门禁（PARDON）(MUST) ｜与全局同源

**规则**：执行任何高风险或不可逆操作前，**必须显式向用户确认并获得授权**：

| 触发场景 | 门禁要求 |
| --- | --- |
| 删除 / 覆盖任何已有文件 | 列出目标文件路径与删除理由，等待批准 |
| 安装任何包（npm / pip / cargo / go get） | 说明包名、版本、用途并获授权 |
| 大规模重构或分支清理 | 先给完整设计、影响范围与回滚预案 |
| 不确定该怎么做 | **先问，不猜**（走 L0-5） |

**原因**：这些操作多数不可逆，且影响面常超出当下任务。

**违反后果**：不可逆的数据或历史丢失。

---

### L0-7 Git 与推送纪律 (MUST) ｜仓群实践（SillyTavern-Timelines 成文政策）

**规则**：
- 每次 `git commit` 完成后**必须推送到远程**，禁止只做本地提交。推送目标固定为 `origin`（自己的 fork 或自有仓），**绝不推送到 `upstream`**。
- **凡承载共享知识或工具的仓库（规则真源、脚手架、同步器、脚本集），必须建立远程仓；默认建为私有仓**
  （`gh repo create <name> --private`），因为这类仓常含本机路径、实例配置等不宜公开的细节。确需公开时先脱敏。
- **缺 remote 的仓视为"未完成"**，不得当作已交付。
- 例外仅当用户在同一轮明确说"先不要推"。
- 拉取上游只用 `git pull --ff-only`；**不要把 `reset --hard` 当默认排障步骤**。
- 签名材料（证书、Profile、密钥库、密码）**不得提交**到仓库。

**原因**：真源/工作成果不在任何会被推送的版本库里 → 迟早丢失。前作「统一规则」系统的真源仓 `Center` 与同步脚本正是因为从未推送而整体消失，是本次重建规则的直接教训。

**违反后果**：成果丢失；或误推上游造成对外事故、污染公开 fork。

---

### L0-8 子代理模型与并发纪律 (MUST) ｜本仓群专用（**修正前作过时条目**）

**规则**：
- 本仓群的子代理**一律使用能力较低的小模型**，禁止用旗舰模型做子代理。当前指定：`DeepSeek-V4-Flash[free]`（模型 ID `claude-haiku-4-5-20251001`）。**禁止使用 Kimi K3 做子代理**。
- 子代理**并发控制在 ≤3**：本机走免费端点，实测 6 并发即出现 `502` 熔断。失败时**先落盘部分结果再重试**。
- 子代理任务必须**自包含**：明确检索范围、具体问题、期望输出。

**原因**：子代理承担的是"读多写少"的检索/提炼工作，小模型成本低且够用；旗舰模型用于主脑判断。免费端点有并发熔断。

**违反后果**：成本浪费与端点熔断；任务中断且中间结果丢失。

> **修正记录**：前作 v1.0.0 §5 写 `gemini-3-flash-preview`、§9 又写 `claude-sonnet-4`，自相矛盾。本条为唯一有效版本。

---

### L0-9 宿主适配只许进桥接层 (MUST) ｜仓群实践

**规则**：平台差异（SillyTavern / Luker / PureTavern / TauriTavern）必须集中在**单一 host-bridge 模块**内处理，不得散落到业务层。

**原因**：四个宿主的 API 面差异大且各自演进；散落判断会导致每加一个宿主就要改遍全仓。

**违反后果**：新增宿主支持变成全仓大改；宿主差异判断互相矛盾。

---

### L0-10 宿主 CSS 作用域纪律 (MUST) ｜仓群实践（**有真实事故**）

**规则**：注入宿主的样式**严禁全局选择器泄漏**——不得使用 `*` / `body` / `:root` / 裸酒馆原生类名；所有自定义类必须带**双前缀**；配色一律继承宿主变量（`--SmartTheme*`）并提供回退值，**禁止硬编码颜色**。

**原因**：插件样式泄漏会污染整个酒馆 UI。**2026-09 已在本仓群实际发生并修复过一次**（`ST-zip-converter/AGENTS.md:51` 记有该事故）。

**违反后果**：宿主人机界面被破坏，用户直接可见的故障。

---

### L0-11 纯前端优先 + 适配器降级 (MUST) ｜与全局同源（仓群多仓独立收敛）

**规则**：纯前端项目引入服务端能力时，一律走「**适配器 + 特性检测 + 静默降级**」：后端可用时增强，不可用时纯前端路径（IndexedDB / OPFS / 内存）**保持全功能**。后端调用必须 fire-and-forget 或显式降级，**严禁纯前端主路径阻塞或失败于后端不可用**。适配器通过依赖注入接缝与核心状态机对接，核心层不感知后端存在。

**原因**：`SillyTavern-Timelines` 与 `PureTavern` 两个仓**各自独立收敛到同一模式**，说明这是用户的实际设计偏好而非偶然。`Authority` 自身即此范式的样板（Host Bridge 失败仅 `console.warn`，不阻断插件加载）。

**违反后果**：用户没装后端就整个插件不可用——违背"插件可独立运行"的产品定位。

---

### L0-12 跨宿主插件禁用 Host Bridge (MUST) ｜**本仓群新增硬约束**（2026-09 判定）

**规则**：需要**跨宿主**（SillyTavern + Luker 等）运行的插件，**禁止依赖 Authority 的 Host Bridge**（宿主补丁路径）。必须使用 Authority 的**可移植子集**（SQL / KV / Blob / 文件 / HTTP / Jobs / Events / Trivium 的公开适配层 API），并在代码里显式标注所用能力的宿主可用性。

**原因**：Host Bridge 是**逐宿主打补丁**的机制——它按宿主版本号做门禁（`supportedPackageVersions: ["1.18.0"]`）且补丁面在宿主间分叉。Luker 上实测被版本门禁拒绝。但 Authority 的**能力内核与宿主解耦**（Host Bridge 失败仅 `console.warn`，不阻断插件加载），所以禁用 Host Bridge 不会损失核心能力。

**违反后果**：插件在 Luker 上静默失去聊天修订/事务语义，产生**难以排查的数据不一致**（表现为功能时好时坏，而非直接报错）。

---

### L0-13 测试即质量门、零回归 (MUST) ｜仓群实践

**规则**：发版前测试必须全绿，**不接受回退**。改动涉及构建/产物时，必须跑对应的产物一致性校验（Authority 仓为 `npm run sync:installable && npm run check:installable`）。端到端测试**只允许对 Dev 实例**运行。

**原因**：本仓群已有以测试规模换稳定性的先例（`ST-shujuku-rebuild` 约 7700 条用例、零回退）。

**违反后果**：回归上线；对 Real 实例跑 E2E 会污染真实数据（触发 L0-1 红线）。

---

### L0-14 文档先行 (SHOULD) ｜仓群实践

**规则**：改动前先读 `.trellis/spec/` 中对应层的规范；复杂功能先写设计文档再写代码。工具/插件的对外说明必须与实现同步更新。

**原因**：spec 是跨会话、跨 agent 的知识载体；不先读就会重复踩已经记录过的坑。

**违反后果**：重复踩坑，且经验无法沉淀。

---

### L0-15 中文（文档 / 注释 / 回复）(SHOULD) ｜与全局同源

**规则**：文档、代码注释、与用户的回复**一律中文**（代码标识符、命令输出、专有名词除外）。

**原因**：用户为中文母语者；且本仓群文档现状已全部中文（与 Trellis spec 模板默认的"English only"相反，属**有意覆盖模板默认**）。

**违反后果**：可读性下降，用户需要额外翻译成本。

---

### L0-16 端口申请段位（实例段独占 · 出厂默认禁用 · 周边工具自 3010 起）(MUST) ｜仓群实践（2026-09 定稿）

**规则**：酒馆生态的端口按段位管理，新服务选端口前必须对照：
- **实例段 `8001–8004` 独占**（8001 Dev ST / 8002 Real ST / 8003 Dev Luker / 8004 Real Luker），禁止挪用；
- **`8000` 为出厂默认，禁止直接使用**：任何脚本/CI/服务启动不得绑定或请求 8000，需要 ST 兼容默认值的场景必须显式覆盖环境变量/配置（不改上游分发物）；
- **`3000` 划归系统保留**：任何酒馆项目不再使用（实测被系统 `svchost` 实占，且多个工具默认撞车）；
- **周边工具自 `3010` 起申请**（Tavern-Viewer → 3010、TavernHeadless → 3020、PureTavern remote-server 显式注入 3030），间隔 10 为后续同类工具留号；
- 已登记独占端口：`8899`（PureTavern web dev，`strictPort`）、`4173`（Vite preview）、`8233`（nocturne 后端内部）、`6080`（noVNC）。

**原因**：8000 六处出厂默认互抢、3000 三方撞车（工具默认 + 系统实占）都是实测形态；且 Dev/Real 实例仅差 1 个端口，端口混乱直接放大误连真实数据的风险（P-11/P-14/P-15）。

**违反后果**：服务按默认配置启动必然失败；或误占实例段端口造成误连真实数据区（不可逆）。

## L1 仓群规则 — JS-Slash-Runner（酒馆助手脚本 / 工作区形态）

> 适用于 `JS-Slash-Runner` 仓群（ST-chatfile-improve、ST-msg-btn-mgr、ST-PanelReset、tavern_helper_template、tavern_helper_workspace）。
> 这些项目运行在**酒馆助手**提供的 iframe / 脚本沙箱里，因此有一套与"扩展插件"完全不同的宿主约束。

### L1-JSR-1 加载/卸载时机：禁止 `DOMContentLoaded` (MUST)

**规则**：
- **禁止** `document.addEventListener("DOMContentLoaded", ...)` —— 产物可能以 `$('body').load(网络链接)` 或 `import '网络链接'` 方式加载，该事件**根本不触发**。
- 加载用 `$(() => { ... })`；卸载用 `$(window).on('pagehide', ...)`；**禁止**用 `'unload'`。

**原因**：酒馆助手的加载方式使 `DOMContentLoaded` 成为不可靠时机。

**违反后果**：脚本在真实使用场景（远程引用加载）下**完全不动**，本地测试却正常。

---

### L1-JSR-2 `index.html` 只允许静态 `<body>` 内容 (MUST)

**规则**：`index.html` 保留空 `<head>`（webpack 打包时插入样式与脚本）。**禁止**手写 `<link rel="stylesheet" href="./index.css">`、**禁止** `<script src="./index.ts">`、`<img>` **禁止**用 `src=""` 占位。

**原因**：webpack 会自行注入；手写引用会导致打包失败或重复加载。

**违反后果**：打包报错，或运行时样式/脚本重复。

---

### L1-JSR-3 iframe 高度与布局适配禁令 (MUST)

**规则**：iframe 内的界面——
- **禁止 `vh`** 等受宿主高度影响的单位（用 `width` + `aspect-ratio` 让高度随宽度变化）；
- 避免 `min-height`、`overflow: auto` 等会撑高父容器的元素；
- 主体内容**禁止 `position: absolute`** 等脱离文档流的样式；
- **不得产生横向滚动条**；
- 适合卡片形状时**不加背景色**（除非用户明确要求）。

**原因**：iframe 高度由宿主决定，使用视口单位会得到错误的可用高度。

**违反后果**：界面被裁切、出现无效滚动条。

---

### L1-JSR-4 IFrame 与 teleport 的样式分叉规则 (MUST)

| 场景 | 挂载方式 | 样式策略 |
| --- | --- | --- |
| 组件是**酒馆网页的补充** | 挂到非 iframe DOM，用 `teleportStyle()` 复制样式到酒馆 `<head>`，`pagehide` 时 `destroy()` | **禁止 tailwindcss**（避免与酒馆既有类名冲突） |
| 组件**独立、需隔离** | 用 `createScriptIdIframe()` 挂到 iframe 内部 body | **优先 tailwindcss class** |

**原因**：两条路径的样式作用域完全不同，混用即冲突。

**违反后果**：样式污染酒馆 UI，或组件在 iframe 内样式失效。

---

### L1-JSR-5 接口优先级：酒馆助手高层接口 > 原生 / STScript (MUST)

**规则**：优先使用 `@types/function/*` 高层接口（`getChatMessages` / `setChatMessages`、`getWorldbook` / `replaceWorldbook`、`getVariables` / `replaceVariables` 等），而非 `@types/iframe/exported.sillytavern.d.ts` 的低层接口或 `triggerSlash` 调用的 `/STScript` 命令。

`exported.ejstemplate`（提示词模板插件）除非明确要求**不考虑**；`tavern_regex` 只应偶尔用 `formatAsTavernRegexedString`。

**原因**：高层接口是酒馆助手的稳定契约；低层接口随宿主变动。

**违反后果**：代码在宿主升级后失效。

---

### L1-JSR-6 技术栈约定 (MUST)

**必须**：TypeScript（而非 JS）；**优先 vue**（+ pinia + vue-router）写界面；用 **zod** 做校验纠错（配 `z.prettifyError()`）而非 if/else；用 **jquery/jqueryui** 而非原生 DOM；用 **gsap** 做动画；样式优先 tailwindcss 写在 `<template>` 内，否则 `<style scoped>`；多媒体多时用 `@pixi/react` + pixi.js。

**禁止**：**nodejs 库**（运行在浏览器）。

**违反后果**：打包失败或运行时 `require is not defined`。

---

### L1-JSR-7 响应式数据写回酒馆前必须 `klona()` 去 proxy (MUST)

`watchEffect(() => replaceVariables(klona(settings.value), ...))`

**原因**：vue 响应式对象是 Proxy，直接写回酒馆会存进不可序列化的代理对象。

**违反后果**：变量写坏，酒馆侧数据异常。

---

### L1-JSR-8 vue-router 双约束 (MUST)

- `createRouter()` **不能**写在 `$(() => {})` 内，必须全局执行；
- 前端界面与脚本都是 iframe，**必须**用 `history: createMemoryHistory()`。

**违反后果**：路由在 iframe 环境下失效或抛错。

---

### L1-JSR-9 MVU 使用前置等待 (MUST)

涉及 MVU 的脚本/界面**必须**在代码顶部（一次即可）`await waitGlobalInitialized('Mvu')`；前端界面另需 `await waitUntil(() => _.has(getVariables({type:'message'}), 'stat_data'))`；脚本用 `waitUntil` 等变量就绪。

**违反后果**：MVU 未就绪时读变量得到 `undefined`，静默出错。

---

### L1-JSR-10 zod 4 schema 硬性写法约定 (MUST)

- 优先 `z.prefault` 而非 `z.default`；
- **禁止 `z.passthrough`、`z.strict`**；
- 数字优先 `z.coerce.number()`，但**其他类型不得用** `z.coerce.xxx()`；
- 限制条件用 `z.transform`（如 `_.clamp`）而非 `.min()` / `.max()`（除非明确要求）；
- `Schema.parse` 必须**幂等**；
- `z.transform` 的 `fn` **只能接收已解析输出**、**不得使用 `context` 参数**；
- `z.extend` 只能作用于 `z.object` / `z.looseObject` / `z.strictObject`（`.prefault({})` 后不可 `extend`）。

**违反后果**：MVU 变量结构解析失败，角色卡初始化出错。

---

### L1-JSR-11 MVU 角色卡目录约定 (MUST)

```
角色卡/脚本/*/          脚本
角色卡/界面/*/          前端界面
角色卡/世界书/*/        设定提示词
角色卡/schema.ts        zod 4 变量结构（pnpm build / watch 时生成同级 schema.json，
                        供 initvar.yaml 的 # yaml-language-server: $schema= 使用）
角色卡/界面/store.ts    pinia 预设的楼层变量读取，供所有界面导入
```
世界书除 `[initvar]变量初始化勿开` 外，还应有 `变量列表`、`[mvu_update]变量更新规则`、`[mvu_update]变量输出格式` 三条目。

**另**：「用户提供的变量结构」若含 `import { registerMvuSchema } ...` 开头与 `$(() => { registerMvuSchema(Schema); })` 结尾，**必须去掉首尾**只保留 `export const Schema`；`schema.ts` 只应有 `export const Schema` 且无其他副作用。

---

### L1-JSR-12 必须区分「独立脚本/界面」与「MVU 角色卡增补」 (MUST)

用户只要**独立脚本/界面**时，**不得**参考 `mvu角色卡` 规则文件。

**违反后果**：给独立脚本套上角色卡专属约束，产出结构错误的项目。

---

### L1-JSR-13 流式楼层界面本质是脚本 (MUST)

因酒馆限制，前端界面不支持流式渲染；项目通过 `util/streaming.ts` 的 `mountStreamingMessage` 提供方案。**流式楼层界面本质是脚本——所有脚本编写规则依旧适用**。

---

### L1-JSR-14 项目/界面判定规则 (MUST)

`src/xxx`（或 `示例/xxx`）文件夹内：**同时有 `index.ts` 和 `index.html`** = 前端界面项目；**仅有 `index.ts`** = 脚本项目。

---

### L1-JSR-15 `示例` 文件夹禁止删除 (MUST)

AI 需要参考其中代码。如需避免打包，可在 `webpack.config.ts` 约第 54 行把 `{示例,src}/` 改为 `src/`。

---

### L1-JSR-16 `dist/` 冲突用 ours 策略 (SHOULD)

`.gitattributes` 设 `dist/** merge=ours`（CI 会重新打包，本地 dist 内容无关紧要）；需一次性执行 `git config --global merge.ours.driver true` 才生效。

---

### L1-JSR-17 `.vscode/launch.json` 防泄漏 (MUST)

该文件含**云酒馆地址**，须执行 `git update-index --skip-worktree .vscode/launch.json`。

**违反后果**：私有云酒馆地址进入公开仓库。

---

### L1-JSR-18 用 chrome-devtools MCP 自读自操酒馆网页 (SHOULD)

以 `.vscode/launch.json` 的 `url` 连接已开浏览器，读取 DOM / 显示 / Console 并点击。

**先检查 `$('#extensions_settings')` 中「酒馆助手-实时监听-允许监听」开关是否启用**——启用后代码变更会自动热重载到酒馆网页，因此**不需要刷新酒馆网页、也不需要自己跑 `pnpm build`**。

---

### L1-JSR-19 ⚠️ 本仓群规则分发现状：符号链接范式已腐烂（警示）

**现状**：本仓群历史上采用「真源 `.cursor/rules/*.mdc` 八件套 + 其余为符号链接/@ 引用」的分发方式。

**实测腐烂**（2026-09-21）：

| 项目 | `.cursor/rules` 真源 | 后果 |
| --- | --- | --- |
| ST-chatfile-improve | ✅ 存在（8 项） | 正常 |
| ST-msg-btn-mgr | ❌ 不存在（实体在 `.agent/rules`） | 8 行 `@.cursor/rules/*.mdc` **全部悬空** |
| tavern_helper_template | ❌ 不存在 | 8 行引用**全部悬空** |
| ST-PanelReset | —— 从未有 agent 规则文件 | 无规则可读 |
| tavern_helper_workspace | —— 仅有 `scripts/` | 无规则可读 |

**后果性质**：符号链接/`@` 引用的失效是**静默的**——文件本身看起来完好，agent 读不到任何规则却不会报错。这比"内容被截断"更隐蔽。

**据此**：本仓群**不再使用符号链接分发统一规则**；统一规则改由 `TAVERN-RULES` 自包含块分发（块内不引用任何外部路径，见仓群根规则 L0）。上述悬空引用应作为独立待修项处理，不在统一规则同步范围内。

---

### L1-JSR-20 酒馆助手开发资料（本仓群参考资料索引）

仓群根目录 `D:\Repo\Tavern-repo\skills\` 下有用户整理的酒馆助手脚本/MVU 专题资料：
`00-手写mvu变量卡.md`、`02-设置和初始化变量.md`、`03-变量提示词让 AI 理解变量.md`、`04-提示词模板动态发送提示词.md`、`05-酒馆助手脚本后台控制和利用变量.md`、`06-酒馆助手界面显示和允许玩家修改变量.md`、`07-手写变量结构.md`。
涉及 MVU 变量卡、提示词模板、界面变量交互时，**先读对应文件**。

## 坑与教训（跨仓真实案例）

> **收录标准**：每条必须**带真实案例与后果**（"违反会怎样"）。只有标题没有正文的条目一律不收——前作规则体系正是这样腐烂的。
> 影响**多个仓**的坑进本节；只影响单仓的坑留在该仓 `AGENTS.md` 的自有区域（块外）。

### P-1 规则真源不在会被推送的版本库里 → 整体消失

**案例**：前作统一规则系统（v1.0.0，2026-09-12）把真源放在 `Tavern-repo/Center/`——**一个不属任何仓库、从未推送的平级目录**。结果：`Center/` 目录与 `sync-rules.ps1` 脚本**双双消失**，只剩 3 个仓库里内容相同、且被同步器截断的残留块。

**后果**：整套规则系统归零，且无处可恢复。

**防护**：真源必须落在**带 remote 且实际推送**的 Git 仓（本仓 `tavern-harness`）；副本块自包含，即使真源丢失副本仍可用。

---

### P-2 同步器有损（截断）比"不同步"更糟

**案例**：前作块内**大量章节只剩标题**——"**禁止的命令**:" 后为空、FAQ 只剩 "A:"。同步器做了有损摘要/截断，且无校验。

**后果**：agent 读到"半截规则"，比没有规则更危险（会误以为规则已覆盖）。

**防护**：块**原样承载完整正文**，禁止任何摘要；同步后以内容哈希校验；`--verify` 可随时检测漂移。

---

### P-3 规则条目自相矛盾且过时 → 无人可信

**案例**：前作 §5 写"子代理模型 `gemini-3-flash-preview`"，§9 又写"本项目用 `claude-sonnet-4`"；实例路径写作 `D:\Repo\Instance\Real\Luker`（实为 `D:\Repo\Tavern-repo\Instance\Real\Luker`，且**根本没有 `Test` 目录**）。

**后果**：规则失去权威性，agent 各取所需，等于没有规则。

**防护**：同一事实只允许有一处权威表述；过时条目在同步时修正并记录（见本文件末"变更记录"）。

---

### P-4 符号链接 / `@` 引用分发：失效是静默的

**案例**：`JS-Slash-Runner` 仓群真源为 `.cursor/rules/*.mdc` 八件套，各项目的 `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` 是 10 行 `@` 引用，其余平台文件是符号链接（25 条 mode `120000` 已入 git）。实测：**5 个项目中只有 1 个存在真源** → `ST-msg-btn-mgr`、`tavern_helper_template` 的 8 行引用**全部悬空**。

**后果**：文件本身看起来完好，agent **静默拿不到任何规则**、不报错。比"内容截断"更隐蔽。

**防护**：不用符号链接/`@` 引用分发统一规则；用**自包含块**（块内不引用任何外部路径）。

**同一坑的第二次事故（2026-09-21，本次建设过程中）**：新同步器按"文件名"逐个写入时，
把 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md` 当成三个目标——但它们其实是**同一个物理文件**
（前者是后者的符号链接）→ **同一个文件被写入三次，叠出三个规则块**。

**教训**：处理"多文件分发"时，**必须按物理路径（realpath）去重**，不能信任文件名。
符号链接的坑不只在"分发方式"上，也在"消费方"上。

---

### P-5 裸 CSS 选择器污染整个酒馆 UI（已实际发生）

**案例**：`ST-zip-converter` 的 `style.css` 使用了酒馆全站类名（`.menu_button` / `.inline-drawer` / `.text_pole` / `.checkbox_label` 等）的裸选择器。**2026-09 实测发生并修复**，此后定为"双前缀铁律"。

**后果**：用户整个酒馆界面被破坏——用户会认为"酒馆本身坏了"。

**防护**：见 L1-MR-3；CI 自查 grep 必须为 0。

---

### P-6 Worker terminate 后未置空引用 → 此后每次调用永久静默挂死

**案例**：`ST-zip-converter` 中 `worker.terminate()` 之后未把 `workerInstance` 置回 `null`（commit `034b7ab`）。被 terminate 的 Worker 会**静默忽略**所有 `postMessage`。

**后果**：功能"不报错但就是不动"，且**每一次后续转换都挂死**，排查成本极高。

**防护**：见 L1-MR-8。

---

### P-7 无界等待（promise 永不 settle）→ 测试挂死

**案例**：`ST-zip-converter` 的 `IframeRenderer.render` 只等 iframe `onload`；快速切换时 iframe 被 destroy，promise **永久悬置**，导致 stress test 3 挂死。

**后果**：测试卡死，CI 无法收敛。

**防护**：见 L1-MR-7（有界等待）。

---

### P-8 高频回调未合帧 → 宿主整页卡顿

**案例**：`ST-zip-converter` 流式 fetch 约 50 chunk/秒，同步调用 `setProgress` 累积出 **14 个 80–107ms 长任务**。

**后果**：宿主页面可感知卡顿。

**防护**：见 L1-MR-9（rAF 合帧）。

---

### P-9 把"浏览器存储"当事实源 → 方向性返工

**案例**：`ST-BgLoader` 一度按"浏览器优先"设计媒体存储，**2026-09-13 被用户当面纠正**："媒体从设计上就该存酒馆服务端原生目录"，随后做了存储倒置重构。

**后果**：大量返工；用户资产变成"藏在浏览器里、用户看不见也管不了"的东西。

**防护**：见 L1-MR-2（事实源在服务端原生目录）。

---

### P-10 Luker 扩展目录嵌套 `third-party` → 该目录下所有子插件覆没

**案例**：Luker 用户私有扩展应平铺在 `data/<user>/extensions/<name>/`。若嵌套成 `third-party/third-party`，该目录下**所有**子插件失效。

**后果**：一次性弄坏用户安装的全部扩展。

**防护**：见 L1-MR-12。

---

### P-11 Dev / Real 实例只差一个端口号 → 误连真实数据

**案例**：本机实测端口为顺序分配且**无冲突**：`8001` Dev ST / `8002` Real ST / `8003` Dev Luker / `8004` Real Luker。且 Dev 与 Real 的**宿主版本完全一致**——版本号无法用于区分。

**后果**：自动化脚本指向 Real 侧的端口即操作真实聊天数据（GB 级、上千个会话），**不可逆**。这是当前环境的最大风险点，且**风险不是端口冲突而是误连**。

**防护**：见 L0-1 与 L1-MF-10；E2E 只允许对 `Instance/Dev/**`。

---

### P-12 本地实例仓的 `origin` 可能误指上游

**案例**：本机某个从上游 fork 出来的宿主实例仓，其 `origin` 指向了**上游仓库**（而该 fork 自己的 remote 另起了名字）。

**后果**：在该目录执行 `git push origin` **会误推上游仓库**——对外事故。

**防护**：见 L1-MF-1。推送前先 `git remote -v` 确认 `origin` 是谁；修复前**不要**在该目录做任何 push。

---

### P-13 把内部实现当公开 API（翻源码找 API）

**案例**：宿主源码中的内部函数不构成公开契约，随版本可改。

**后果**：宿主升级后代码静默失效。

**防护**：见 L1-MR-5（API 事实以官方文档为准）。

---

### P-14 8000 出厂默认值六处互抢

**案例**：本机六处配置使用 ST 出厂默认 8000（Luker 两份 compose、ST/Luker 两份 `default/config.yaml`、PureTavern remote-server 默认、TauriTavern default），任何两个同时启动即互抢端口。

**后果**：服务按出厂默认启动必然失败，且报错形态是「端口被占」而非「配置撞车」，排查时容易误判。

**防护**：见 L0-16。8000 标记「出厂默认、禁止直接使用」；启动必须显式指定端口，不改上游分发物。

---

### P-15 3000 三方撞车 + 系统实占

**案例**：Tavern-Viewer 与 TavernHeadless 均默认 3000，且该端口被系统 `svchost` 实占——两个工具按默认配置启动**必然失败**（谁先启动谁占，后到者挂）。

**后果**：工具启动即失败；若误以为「端口被占是残留进程」而反复清理，会浪费时间且可能误杀系统进程。

**防护**：见 L0-16。3000 划归系统保留；周边工具按段位自 3010 起申请（Viewer→3010、Headless→3020）。

---

### P-16 Dev/Real 目录名不可假设语义（TauriTavern 倒挂实例）

**案例**：`Instance/Dev/TauriTavern` 一度是**残缺仓**（src-tauri 等 1289 个被跟踪文件被从工作区删除），而 `Instance/Real/TauriTavern` 反而完整——与「Dev 完整、Real 是数据区」的直觉**完全倒挂**。

**后果**：若按目录名假设「Dev 一定可构建」，E2E 测试目标会在构建阶段静默失败；反向假设「Real 不完整不能碰」也会漏掉真实数据风险。

**防护**：见 L1-MF-10。实例状态以**现场取证**为准（git status / 文件清单），不以目录名推断；E2E 目标必须先验证端口白名单与实例实际可用性。

---

### 变更记录

| 版本 | 日期 | 变更 |
| --- | --- | --- |
| v1.1.0 | 2026-09-21 | 首次以「自包含块」形式发布；修正前作过时条目（实例路径、子代理模型）；新增 L0-12「跨宿主插件禁用 Host Bridge」；新增本节「坑与教训」并强制「每条带后果」 |

## 项目覆盖

<!-- TAVERN-RULES:END -->
