---
name: html-effectiveness
description: 让 agent 用单文件 HTML 替代 markdown 输出空间性、并行性、可比较或可交互的内容。当用户请求"对比/计划/评审/报告/解释器/幻灯片/编辑器/可视化"或当输出含并排选项、流程图、时间线、代码 diff、可交互元素、需要"指着某处说就是它"的场景时使用。本 skill 是路由器：先用决策框架判断是否走 HTML，再按 9 大类调度对应的子 skill（01-explore / 02-review / 03-design / 04-proto / 05-diagram / 06-slides / 07-research / 08-report / 09-editor），并复用 ../templates/*.html 与 shared/base.css 输出真实可运行的产物。
---

# html-effectiveness — 主路由

> Markdown 把所有信息压成线性文字流。**diff 是空间的、对比是并排的、流程是图状的、交互是可感受的**——这些维度被 markdown 抹平后，人需要在脑中重建它们。HTML 是 agent 真正的画布。

灵感来自 Thariq Shihipar 的 [The unreasonable effectiveness of HTML](https://thariqs.github.io/html-effectiveness/)。本 skill 把 9 大类 20 个范式系统化为可复用的决策框架 + 模板。

## 第 1 步：形状测试（决定要不要走 HTML）

读完用户请求后，对答案做"形状测试"：

| 答案的形状 | 用什么 |
|-----------|--------|
| 一段陈述、一个数字、一句结论 | 直接说 |
| 几个步骤、要点列表、单一代码片段 | markdown |
| **2+ 选项要并排比较**（方案、设计、文案） | **HTML** |
| **空间关系**（架构图、流程图、依赖、调用栈） | **HTML（含 SVG）** |
| **结构化文档**（PR 写作、状态报告、事故报告、计划） | **HTML** |
| **可交互**（滑块调参、拖拽分组、键盘翻页、live preview） | **HTML** |
| **需要导出回 agent**（用户在 UI 改完结果要复制回来） | **HTML（必带"复制"按钮）** |
| **代码 diff + 注释 + 风险标记同时存在** | **HTML** |
| **概念需要"看到"才能懂**（哈希环、token bucket、状态机） | **HTML（含 SVG/canvas）** |

判断更具体的边界案例见同目录下没有但需要时可读的`../examples`（已并入下方各子 skill 的"何时用"章节）。

## 第 2 步：路由到子 skill

命中 HTML 路径后，从下面 9 大类中选**最匹配**的一个，**读取对应子 skill 的 SKILL.md 文件**继续执行。每个子 skill 包含：详细使用场景、空间形状分析、HTML 骨架、关键代码片段、对应的 `../templates/*.html`。

| 子 skill | 触发场景 | 模板 |
|---------|---------|------|
| [`01-explore/`](./01-explore/SKILL.md) | 多方案对比、视觉风格探索、实现计划 RFC | `compare.html` `plan.html` |
| [`02-review/`](./02-review/SKILL.md) | PR 评审、PR 写作（作者侧）、模块图/调用栈 | `pr.html` `diff.html` |
| [`03-design/`](./03-design/SKILL.md) | 设计系统参考、组件变体陈列 | `design-tokens.html` |
| [`04-proto/`](./04-proto/SKILL.md) | 动画沙盒、可点击屏幕流 | `animation.html` |
| [`05-diagram/`](./05-diagram/SKILL.md) | 流程图/状态机、SVG 插图集 | `flowchart.html` |
| [`06-slides/`](./06-slides/SKILL.md) | 键盘翻页幻灯片 | `slides.html` |
| [`07-research/`](./07-research/SKILL.md) | 特性解释器、抽象概念交互式可视化 | `concept.html` |
| [`08-report/`](./08-report/SKILL.md) | 周报、事故报告/postmortem | `status.html` `postmortem.html` |
| [`09-editor/`](./09-editor/SKILL.md) | 拖拽分类板、配置编辑器、Prompt 调参器 | `prompt.html` |

## 第 3 步：执行（每个子 skill 的标准流程）

子 skill 内部统一遵循这个流程：

1. **读** 对应的 `../templates/{name}.html`（如有）作为骨架
2. **嵌** 真实内容（不要 `Lorem ipsum`、不要 `User A`，要具体场景 + 真实姓名 + 真实数字）
3. **检** 6 项产出约束（见下）
4. **写** 到工作区（**永远在工作区内，不写 `~/Downloads/` / 不写 user home / 不写 `/tmp/`**）—— 见下面"输出位置"小节
5. **告** 用户**相对工作区的路径**与打开方式（`xdg-open` / `wslview` / `open` / 双击）

## 输出位置（强制约定）

> **唯一规则：所有 HTML 输出都写到当前工作区里。** 不污染用户的 Downloads、不写 `/tmp/`、不写 home 目录。

工作区根目录 = 用户当前 IDE / shell 打开的项目根（含 `.git/` 的目录，或 agent 启动时的 cwd）。下文中 `<ws>` 代表它。

### 默认目录：`<ws>/.agent-html/`

**所有"一次性消费"的产出**——临时对比、视觉风格探索、组件变体、动画沙盒、可点击流、PR 评审视图、模块图、概念解释器、所有编辑器小工具——都默认写到：

```
<ws>/.agent-html/{slug}-{YYYYMMDD-HHmm}.html
```

- `slug` 是简短英文标识符：`debounce-compare`、`auth-flow`、`task-card-anim`、`cycle-14-triage` 等
- 时间戳避免覆盖同名前作
- 把 `.agent-html/` 加进 `.gitignore`（仓库自带的 `.gitignore` 已包含此项），avoid 误提交

每个子 skill 的默认位置：

| 子 skill | 默认位置 |
|---------|---------|
| 01-explore: compare / 视觉方向 | `<ws>/.agent-html/compare-{slug}-{ts}.html` |
| 02-review: diff (reviewer) / 模块图 | `<ws>/.agent-html/review-{slug}-{ts}.html` |
| 03-design: 组件变体 | `<ws>/.agent-html/variants-{component}-{ts}.html` |
| 04-proto: 动画沙盒 / 可点击流 | `<ws>/.agent-html/proto-{slug}-{ts}.html` |
| 05-diagram: 流程图 / SVG 插图 | `<ws>/.agent-html/diagram-{slug}-{ts}.html` |
| 07-research: 概念解释器 | `<ws>/.agent-html/concept-{topic}-{ts}.html` |
| 09-editor: 拖拽板 / flag / prompt-tuner | `<ws>/.agent-html/editor-{slug}-{ts}.html` |

### 例外：有"长期价值"的产出，提议升级到工作区文档目录

下面这几类产出会被人**反复回看**或**进 PR/Wiki**——agent 应该提议把它们写到工作区的标准文档目录，而不是 `.agent-html/`。提议时给出**两个明确选项**让用户选：

| 子 skill / 模板 | 提议位置（首选 → 备选） | 文件名 |
|----------------|------------------------|--------|
| 01-explore: **plan** (实现计划 / RFC) | `<ws>/rfcs/` → `<ws>/docs/rfcs/` → `<ws>/.agent-html/` | `{NNNN}-{slug}.html` |
| 02-review: **PR writeup** (作者侧) | `<ws>/docs/prs/` → `<ws>/.agent-html/`（更常见做法是直接粘贴到 GitHub PR description） | `pr-{NNN}-{slug}.html` |
| 03-design: **design tokens** | `<ws>/docs/design/` → `<ws>/.agent-html/` | `tokens.html` |
| 05-diagram: **架构 flowchart** / 配图 | `<ws>/docs/architecture/` → `<ws>/docs/figures/` → `<ws>/.agent-html/` | `{slug}.html` |
| 06-slides: deck | `<ws>/docs/slides/` → `<ws>/.agent-html/` | `{date}-{topic}.html` |
| 07-research: feature explainer | `<ws>/docs/explainers/` → `<ws>/.agent-html/` | `{feature}.html` |
| 08-report: **status** | `<ws>/reports/status/` → `<ws>/docs/status/` → `<ws>/.agent-html/` | `{YYYY-WW}.html` |
| 08-report: **postmortem** | `<ws>/postmortems/` → `<ws>/docs/postmortems/` → `<ws>/.agent-html/` | `INC-{id}-{slug}.html` |

### 路径选择决策树

```
用户请求 → 选目录的判断顺序：
1. 用户在 prompt 里指定了路径？        → 用用户指定的，结束
2. 工作区里已经有同类目录？           → 用现有的（保持仓库结构一致）
   例：已有 docs/rfcs/ → plan 写这里
3. 上表里这类产出有"首选 → 备选"？    → 提议首选（如果不存在就 mkdir -p）
4. 否则                              → .agent-html/{slug}-{ts}.html
```

第 2 步的"已有目录"检测：在执行前用 `ls`/Glob 检查 `<ws>/{docs,rfcs,reports,postmortems}/` 是否存在，**如已存在就直接用**，不要在工作区里创建第二个并列名字的目录（比如已有 `rfcs/` 就别再开 `docs/rfcs/`）。

### 报告给用户

写完后**总是**给一个简短的两行确认：

```
✓ Saved to .agent-html/compare-debounce-20260514-1103.html (relative to /home/you/proj)
  Open: xdg-open .agent-html/compare-debounce-20260514-1103.html
```

或在 WSL 上：

```
  Open: wslview .agent-html/compare-debounce-20260514-1103.html
```

路径**优先用工作区相对形式**——便于用户复制到 IDE 里直接 Cmd+Click 打开。完整绝对路径只在第一行尾部用括号附注。

## 6 项产出约束（每个 HTML 输出都必须满足）

1. **单文件自包含** — HTML/CSS/JS/SVG 全内联，不依赖 CDN（可以从 `shared/base.css` 复制 token，但要内联进 `<style>`）
2. **`file://` 可运行** — 不需要 server，不需要 build，不调外部 API
3. **现代但克制** — system font 栈、暖色调（来自 [`shared/base.css`](./shared/base.css)）、克制动画
4. **真实内容** — 禁占位符；用具体场景：`comments.create p99 1.4s → 180ms`，不写 `latency improved`
5. **编辑器必带导出** — 任何让用户操作的 HTML 必须有"复制为 markdown / Copy diff / Copy prompt"按钮，让 UI 状态能回到 agent
6. **桌面响应式** — 1280px 笔记本和 1920px 外接显示器都看得舒服；不强求手机端

## 共享资源

- [`shared/base.css`](./shared/base.css) — 通用 CSS baseline（CSS 变量 / 字体 / 配色 / 间距 / 组件）。生成新模板时把这份内联到 `<style>` 里
- [`shared/components.html`](./shared/components.html) — 常用 HTML 片段库：badges、cards、buttons、SVG arrow markers、diff lines、KPI tiles、carryover items 等

## 反模式（不要做）

| 错误做法 | 正确做法 |
|---------|---------|
| 用 markdown 表格放 4 列方案对比 | 走 `01-explore`，用 `compare.html` |
| 用 ASCII art 画流程图 | 走 `05-diagram`，用内联 SVG |
| 引用 Tailwind / shadcn / Chart.js CDN | 内联 CSS，从 `shared/base.css` 复制需要的部分 |
| 用 `Lorem ipsum` / `User A, User B` | 用具体场景 + 真实姓名 + 真实数字 |
| 编辑器没有"复制结果"按钮 | 永远带导出按钮，把 UI 状态变成可粘贴文本 |
| 输出 HTML 后用户找不到文件 | 总是给"工作区相对路径 + 打开命令"两行 |
| 写到 `~/Downloads/` / `/tmp/` / user home / 任何工作区外 | **永远写工作区**——默认 `<ws>/.agent-html/`，长期价值的提议升级到 `docs/` `rfcs/` `reports/` `postmortems/` |
| 在工作区已有 `rfcs/` 时还另建 `docs/rfcs/` | 先 `ls` 检测已有目录，复用，不并列 |
| 不读子 skill 直接拍脑袋写 | 命中类别后**先读** `01-09/*/SKILL.md` 再动手 |

## 元信息

- 版本：v0.2.0
- 仓库：https://github.com/Azhi-ss/html-effectiveness
- 安装：`npx html-effectiveness --all`
