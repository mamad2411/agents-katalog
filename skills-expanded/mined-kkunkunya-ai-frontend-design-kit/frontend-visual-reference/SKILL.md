---
name: frontend-visual-reference
description: 阶段 4 视觉锚定三件套的主 skill——在写第一行代码前，用 Moodboard（A） + 完整网页示意图（B） + 动效帧序列（C） 三种图像级锚点把视觉方向钉死。探索前移在 Moodboard 阶段（A）以 2-3 张让用户选的方式执行，B/C 是单线生成。资产生成走双路径：主路径 baoyu-imagine skill 自动出图，兜底路径打开 prompt 文件让用户复制到网页端。产出写入 knowledge/design-docs/visual-anchors/ 目录，并在 design.md §12/§13/§14 回填引用。触发：design.md 初稿完成、后轮采访定稿后、用户说"出几张方向图让我选""做 moodboard""生成页面示意图""动效帧序列图"。不用于调研（那是 frontend-design-research）、不用于动效微观代码级 prompt（那是 frontend-motion-prompt-writer）、不用于写 DESIGN.md（那是 frontend-design-writer）。
---

<!-- PACKAGED_KNOWLEDGE_START -->
## Packaged Knowledge Snapshot

This packaged copy includes local note snapshots for portability.
When the original Obsidian absolute path is unavailable, use the packaged snapshot instead:

- `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/AI前端设计认知框架.md` -> `references/packaged-knowledge/AI前端设计认知框架.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/六维：形色字构质动是网站试吃的机械骨架.md` -> `references/packaged-knowledge/六维：形色字构质动是网站试吃的机械骨架.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/动效文档两层：MOTION-SPEC vs 实现 prompt 集.md` -> `references/packaged-knowledge/动效文档两层：MOTION-SPEC vs 实现 prompt 集.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/反 slop 硬禁令：AI 前端的十条视觉红线.md` -> `references/packaged-knowledge/反 slop 硬禁令：AI 前端的十条视觉红线.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/审美是隐性认知，追问是唯一的解压工具.md` -> `references/packaged-knowledge/审美是隐性认知，追问是唯一的解压工具.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/视觉锚定三件套：代价结构与资产生成双路径.md` -> `references/packaged-knowledge/视觉锚定三件套：代价结构与资产生成双路径.md`
<!-- PACKAGED_KNOWLEDGE_END -->

# Frontend Visual Reference

## 这个 skill 在做什么

**阶段 4 视觉锚定三件套**的执行器。在写第一行代码之前，用三种图像级锚点把视觉方向钉死：

| 锚点 | 图像形态 | 凝聚维度 | 探索属性 |
|---|---|---|---|
| **A. Moodboard** | 综合风格板（色板 + 材质样本 + 符号族 + 字体 + UI 片段） | 六维静态 5 维（形/色/字/构/质） | ★ **前移探索**：2-3 张让用户选 |
| **B. 完整网页示意图** | 主页 → 子页的完整页面示意图 | 真实页面布局 + 信息层级 + 叙事推进 | 单线：主页 → OK → 子页 |
| **C. 动效帧序列** | 从左到右的帧变化示例 | 六维动维 | 单线：每个核心动效 1 套 |

核心赌局：**AI 生图便宜 + 视觉传达直接**，所以把"探索"前移到图像层，代码层单线执行。

## 在阶段化流程里的位置

```
阶段3 后轮深度采访 → design.md 定稿
         ↓
阶段4 视觉锚定三件套 ← 本 skill
  ├─ A. Moodboard Prompt（2-3 张，前移探索）
  ├─ B. 完整网页示意图 Prompt（主页 → 子页，单线）
  └─ C. 动效帧序列 Prompt（每个核心动效 1 套，单线）
         ↓
阶段5 资产生成（baoyu-imagine 主 + 手动兜底）
         ↓
阶段6 代码实现（读 design.md + 三件套图像 + 动效微观 prompt）
```

**关键重定位**（和老版的差异）：老版 visual-reference 是"Layer 4 方向选择门"——派生 2-4 个视觉方向候选出图让用户选。2026-04-21 重构后明确：

- 老版"派生 2-4 视觉方向"**吸收进本 skill 的 A. Moodboard 阶段**——2-3 张 Moodboard 做探索分支
- B. 完整网页示意图、C. 动效帧序列 是**新增职责**
- "探索" **只在 A 阶段做**，B/C 是单线执行（A 选定后方向已钉死）
- 产出路径从 `visual-directions/` 改为 `visual-anchors/`（三件套统一收纳）

## 何时进入本 skill

**要进**：
- 前轮采访 + 六维试吃 + 后轮采访都完成，design.md 定稿
- 用户说"出几张方向图让我选""做 moodboard""生成页面示意图""动效帧序列图""在代码前先做视觉锚点"
- 展示型项目必走全 A+B+C；工具型项目走 A+B 跳过 C

**不要进**：
- 调研还没跑 → `frontend-design-research`（阶段 2）
- 主语言 / 后轮采访没做 → `frontend-interview-dualround`
- 方向已锁定，要在该方向内刷多张锚点图 → 本 skill 单线 B 即可
- 要生成某个核心动效组件的**代码级**实现 prompt（Theme tokens / Element 逐一规格） → `frontend-motion-prompt-writer`
- 通用海报 / 人像 / 产品图 → `prompt-builder`
- 需要像素级设计稿 → Figma

## 知识库依赖

| 文件 | 用途 | 何时读 |
|------|------|--------|
| `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/视觉锚定三件套：代价结构与资产生成双路径.md` | 三件套定义 + 每件 prompt 结构 + 双路径执行 | **启动必读** |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/六维：形色字构质动是网站试吃的机械骨架.md` | Moodboard 对 5 维的凝聚（对照 CIVITAS 范式） | 组装 A Prompt 时读 |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/AI前端设计认知框架.md` | 阶段 4 在总流程的位置 + 工具型跳 C 的依据 | 启动时扫阶段 4 段 |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/动效文档两层：MOTION-SPEC vs 实现 prompt 集.md` | C 帧序列 vs 微观实现 prompt 的分工 | 写 C 时读 |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/反 slop 硬禁令：AI 前端的十条视觉红线.md` | 生成 prompt 前加 anti-ref 段 | 每次出图前快扫 |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/审美是隐性认知，追问是唯一的解压工具.md` | A 阶段用户选 Moodboard 时的选择题化 | A 阶段用户选图时读 |
| 项目内 `knowledge/design-docs/design.md` | 主语言 + 六维数据 + 后轮采访结果的真理源 | 必读为输入 |

## 执行顺序

```
0. 入参检查 → 1. A Moodboard（2-3 张分支探索）→ 2. B 完整网页示意图（单线）→ 3. C 动效帧序列（单线，展示型）→ 4. 回填 design.md §12-§14
```

**关键节点**：阶段 A 完成、用户选定 Moodboard 后，方向已钉死。B/C 严格单线，不再派生分支。

---

## 步骤 0：入参检查

| 输入 | 是否必须 | 缺失时 |
|---|---|---|
| 主语言（一句动词式陈述） | 必须 | 回 `frontend-interview-dualround` 前轮 |
| 六维试吃记录 | 必须 | 回 `frontend-design-research` |
| 后轮采访（架构 / section / 文案调性 / 交互） | 必须 | 回 `frontend-interview-dualround` 后轮 |
| design.md 初稿或定稿（§0-§6 + §10） | 必须 | 回 `frontend-design-writer` Round 1-3 |
| anti-ref 清单 | 必须 | 现场补齐（读反 slop 笔记 + 后轮采访反向细节类） |

---

## 步骤 1：A. Moodboard Prompt（前移探索 2-3 张）

### 1.1 选差异轴

从以下维度选 1-2 个作为差异轴（不要超过 2 个，否则用户无法归因）：

| 差异轴 | 举例 |
|---|---|
| 氛围 | 静谧克制 / 激进锋利 / 编辑感 / 温暖手工 |
| 构图 | 对称极简 / 信息密集 / 叙事推进 / 大图主导 |
| 材质 | 哑光 + 颗粒 / 金属光泽 / 纸张质地 / 玻璃折射 |
| 配色 | 冷调单色 / 暖调双色 / 高对比彩色 / 灰阶 + 单点亮色 |
| 字体气质 | sharp geometric sans / editorial serif / humanist neutral / mono |

### 1.2 每方向给一句话口号

口号是**比喻或动词陈述**，不是形容词堆砌。示例（主语言"滚动时混沌收敛为有序"）：

- **v1 冷静图书馆**：哑光金属 + 冷调单色 + editorial 长体
- **v2 深夜工坊**：暖调颗粒 + 手工感材质 + humanist sans
- **v3 激进赛博**：高对比彩色 + 金属光泽 + sharp geometric

### 1.3 Moodboard Prompt 结构（每方向一份）

每方向的 prompt 文件写到 `knowledge/design-docs/visual-anchors/moodboard-v{N}-prompt.md`。

核心要素（以 CIVITAS 为范式）：

1. **主概念**（一句话主语言，所有方向一致）
2. **必含元素清单**：色板 swatches、材质样本、符号族、字体样本、UI 片段
3. **色彩方向**：具体颜色名或 hex
4. **氛围关键词**：5-8 个形容词
5. **反例清单**（avoid）：从 anti-slop 十条 + 项目 anti-ref 合并
6. **Composition 约束**：不是网页截图，是 editorial layout / branding board

**硬约束**：

- 所有方向的"主概念"段完全一致（主语言锁定）
- 差异只在 2-8 这几项
- 不同方向之间差异必须可感知（不是"都是现代简约"这类含糊差异）

### 1.4 出图

走资产生成双路径（见 §4 专门段）。产出：

- `knowledge/design-docs/visual-anchors/moodboard-v{N}-{date}.png`（每方向 1 张）

### 1.5 方向选择门

把 2-3 张图 + 口号并排呈现给用户，请他：

1. **选 1 个主方向**——明确选一个，不接受"介于中间"
2. **说明被放弃方向哪里不对味**——作为 anti-ref 资产

选择题化（用 [[审美是隐性认知，追问是唯一的解压工具]]）：

- 定位：第一眼落在哪张图？
- 对标：和哪张最像心里的样子？哪张最像参考站？
- 量化：给 2-3 个具体维度让用户勾选（"v1 的氛围对但配色偏冷，v2 的配色对但构图太密，你更愿意在 v1 上调暖还是 v2 上减密度？"）

**选不出来时兜底**：

| 用户反应 | 处理 |
|---|---|
| "都不对" | 回 `frontend-interview-dualround` 重拔主语言/后轮——不在本 skill 刷图 |
| "介于 v1 和 v2 之间" | 派生 v4 融合版（v1 氛围 + v2 构图），**最多再派一轮**，超过强制选 |
| "v2 但想换 X" | 选定 v2，X 写进"选定方向上的微调项" |
| 反复犹豫 >3 轮 | 上报"调研层需要回滚"——方向派生无法收敛说明约束不够清晰 |

**本 skill 核心是做选择，不是等完美**。

---

## 步骤 2：B. 完整网页示意图 Prompt（单线）

### 2.1 硬约束：单线执行

A 选定后方向已钉死。B 阶段**不做分支**——只按选定的 Moodboard 出一条线的图。

### 2.2 执行顺序

1. **先出主页**——完整 hero + 所有 section 的高保真示意图
2. **用户确认 OK**——需要调整回到 prompt 改一版
3. **再出子页 / 下滑段**——subpage by subpage，不并行

### 2.3 Prompt 结构

每份 prompt 写到 `knowledge/design-docs/visual-anchors/mockup-{page}-prompt.md`。

核心要素：

1. **页面类型**（landing / hero / feature / product / dashboard）
2. **主叙事**（从上到下讲什么故事，来自 design.md §0）
3. **Section 分解**：每个 section 的目标 + 主元素 + 视觉层级
4. **调色 / 字体 / 材质**（从选定的 Moodboard 复制过来）
5. **真实文案占位**（不是 lorem ipsum，用产品级 placeholder，从后轮采访的文案调性类产出）

### 2.4 出图

走双路径。产出：

- `knowledge/design-docs/visual-anchors/mockup-home-{date}.png`
- `knowledge/design-docs/visual-anchors/mockup-{subpage}-{date}.png`

---

## 步骤 3：C. 动效帧序列 Prompt（单线，展示型走）

工具型项目**跳过本步**（阶段化流程明确写了）。

### 3.1 核心动效清单

从 design.md §10 Motion Spec 的 Core Motion Catalog 取：

- 展示型：Hero 入场 / Scroll-driven 背景 / LoadingScreen / 关键交互动效
- 工具型：无（跳过本步）

### 3.2 每个核心动效一套帧序列

每个动效出**一张从左到右拼接的帧序列图**：起始帧 → 中间关键帧 → 终止帧。

### 3.3 Prompt 结构

每份 prompt 写到 `knowledge/design-docs/visual-anchors/motion-frames/{animation-name}-prompt.md`。

核心要素：

1. **动效目标**（Loading / Hero 入场 / scroll-driven 等）
2. **起始帧、中间关键帧、终止帧**的逐一视觉描述
3. **时长 + 缓动曲线**（帧间过渡的隐性约束）
4. **触发条件**（scroll 到哪个点 / hover / 点击）

### 3.4 和代码级实现 prompt 的分工

帧序列图是**视觉锚点**，不是实现规格：

| 产物 | 角色 | 产出 skill |
|---|---|---|
| 帧序列图（本步产出） | 从左到右的静态帧变化 → 给用户 confirm 方向 + 给 Agent 视觉参考 | 本 skill |
| 微观实现 prompt（LoadingScreen 风格代码级规格） | Theme tokens / Element 逐一规格 / 时序总表 → 喂 Agent 写 framer motion 代码 | `frontend-motion-prompt-writer` |

详见 [[动效文档两层：MOTION-SPEC vs 实现 prompt 集]]。

### 3.5 出图

走双路径。产出：

- `knowledge/design-docs/visual-anchors/motion-frames/{animation-name}-{date}.png`

---

## 步骤 4：回填 design.md §12-§14

三件套完成后，在 design.md 回填引用段（由 `frontend-design-writer` Round 4 执行，本 skill 提供路径清单）：

```markdown
## 12. Moodboard Prompt
- Prompt 文件：visual-anchors/moodboard-v2-prompt.md
- 状态：locked (v2 深夜工坊)
- 选定图：visual-anchors/moodboard-v2-20260421.png

## 13. Page Mockup Prompt
- 主页：visual-anchors/mockup-home-prompt.md → mockup-home-20260421.png
- 子页 pricing：visual-anchors/mockup-pricing-prompt.md → ...

## 14. Motion Prompts
- 帧序列目录：visual-anchors/motion-frames/
- 实现 prompt 目录：motion-prompts/（由 frontend-motion-prompt-writer 填充）
- 核心动效清单：[表格，状态 draft/locked]
```

---

## 资产生成双路径

三件套所有产出都通过 prompt 调用图像生成模型。执行路径分主兜底：

| 路径 | 触发 | 执行方式 |
|---|---|---|
| **主路径** | 默认 | 调用 `baoyu-imagine` skill，用 GPT Image 2 或对应可用模型自动生成 |
| **兜底路径** | 主路径失败（API 限额 / 内容安全拒绝 / 模型不可用） | Agent 告知用户 + 打开 prompt 文件，用户复制到网页端模型手动生成 |

双路径意义：流程不会因 API 临时问题卡死，但主路径能跑就主路径跑。

### 调用约定

- 主路径：`$baoyu-imagine` 传 prompt 文件路径，接收生成图片文件
- 兜底：`open` 命令打开 prompt 文件 + 提示用户"复制到 MJ / 即梦 / Gemini 手动生成，完成后把图放到 `visual-anchors/{file}-{date}.png`"

---

## 样板不进笔记库

笔记库只存方法论——"Moodboard prompt 应该长什么样"的结构定义。

**具体样板**（CIVITAS 那张图的完整 prompt、LoadingScreen 规格）**住在项目的 `knowledge/design-docs/visual-anchors/`**，按项目 context 现场生成，不跨项目复用。

---

## 完成标准

A 阶段（Moodboard）：

- [ ] 派生了 2-3 个候选方向，每个有一句话口号 + 完整 Moodboard prompt
- [ ] 所有候选共享同一主语言（字段完全一致）
- [ ] 差异轴明确（1-2 个维度）且在不同方向间差异可感知
- [ ] 每方向 1 张图产出（或 prompt-only 的可粘贴版）
- [ ] 用户明确选定 1 个方向
- [ ] 被放弃方向的 anti-ref 摘要保留

B 阶段（页面示意图）：

- [ ] 主页 mockup 生成 + 用户确认 OK
- [ ] 所需子页 mockup 逐一生成（每出一张让用户确认再出下一张）
- [ ] 所有图文件入 `visual-anchors/`
- [ ] 文案占位用产品级占位（不是 lorem ipsum）

C 阶段（动效帧序列，展示型）：

- [ ] 每个核心动效都有帧序列图
- [ ] 帧序列图体现起 / 中 / 终 三帧
- [ ] 图文件入 `visual-anchors/motion-frames/`

回填：

- [ ] `frontend-design-writer` Round 4 已被触发，design.md §12-§14 引用段填好

## 与其他 skill / 剧本的边界

| 场景 | 走谁 |
|------|------|
| **已定稿项目的二开 / 增量扩展** | `frontend-iteration-planner`（场景 C 入口；T1 会调用本 skill 的 B 单页 mockup，T2 可选，T3 跳过） |
| 跑调研（六维试吃 / 参考量化） | `frontend-design-research`（阶段 2，上游） |
| 前轮/后轮深度采访 | `frontend-interview-dualround` |
| 视觉叙事 → 图像 prompt 的通用方法论 | `prompt-builder`（通用生图，本 skill 是它的前端专用桥） |
| 调 API 出图 | `baoyu-imagine`（由 prompt-builder 或本 skill 直接调） |
| 阶段 4 完成，写 DESIGN.md kun 15 段 + 回填 §12-§14 | `frontend-design-writer`（下游） |
| 某个核心动效组件的代码级实现 prompt（LoadingScreen 风格） | `frontend-motion-prompt-writer`（阶段 4C / 阶段 6 使用） |
| 方向定了，实现页面 | 开发实现剧本（读 design.md + 三件套图像 + 实现 prompt） |
| 反 slop 硬禁令 | `frontend-anti-slop-gate`（阶段 6 横切 + 本 skill 每次出图前快扫） |
| 通用海报 / 人像 / 产品图 | `prompt-builder` 直接用 |

## 本 skill 的 deletion-spec

- **触发删除条件**：当图像生成成本显著上升（比如模型 API 定价变化）使得"前移探索"的代价优势消失，或 AI 代码生成达到一次通过稳定度（不需要视觉锚定就能正确生成），本 skill 可降级。若三件套缩减为两件（比如帧序列被动效文档吸收）或扩展为四件（增加信息架构图），需重写。
- **禁用方式**：从 `plugins/frontend-suite/skills/` 删除本目录即停止注入（`skills` 字段是目录通配）。无需改 plugin.json。
- **卸载清单**：
  - `frontend-design-research` / `frontend-interview-dualround` / `frontend-design-writer` / `frontend-motion-prompt-writer` 的"边界表"和产出下游流向段引用本 skill
  - `plugins/frontend-suite/.claude-plugin/plugin.json` description 的"visual reference"段需回退
  - 项目内 `knowledge/design-docs/visual-anchors/` 目录由用户自行决定保留或迁移
  - [[AI前端设计认知框架]] 阶段 4 段和 [[视觉锚定三件套：代价结构与资产生成双路径]] 的"对应 skill"字段需同步