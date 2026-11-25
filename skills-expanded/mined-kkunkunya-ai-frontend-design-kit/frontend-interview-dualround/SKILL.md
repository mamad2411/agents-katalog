---
name: frontend-interview-dualround
description: 产品设计师视角的双轮深度采访横切——前轮（阶段 1 需求后）建产品边界 + 主语言收敛，后轮（阶段 3 Moodboard 选定后）拔架构 + section + 文案调性 + 交互路径。五类引导式提问：前轮是定位/用户/反向/资源/时间；后轮是架构/section/文案调性/交互路径/反向细节。角色显式从"前端设计师"切到"产品设计师"，选择题优先+开放题兜底，一次问 3-5 个不批量甩 20 个。产出反写回 design.md。触发：新项目启动 brief 模糊、六维调研完成但未定稿、用户说"帮我问清楚这个产品""我脑子里有个想法但说不清"。不用于代码后纠偏（那是 frontend-design-review 的三段式追问）、不用于需求判定机械门禁（那是 req-suite:requirement-clarifier）。
---

<!-- PACKAGED_KNOWLEDGE_START -->
## Packaged Knowledge Snapshot

This packaged copy includes local note snapshots for portability.
When the original Obsidian absolute path is unavailable, use the packaged snapshot instead:

- `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/AI前端设计认知框架.md` -> `references/packaged-knowledge/AI前端设计认知框架.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/主语言是设计的第一原则.md` -> `references/packaged-knowledge/主语言是设计的第一原则.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/审美是隐性认知，追问是唯一的解压工具.md` -> `references/packaged-knowledge/审美是隐性认知，追问是唯一的解压工具.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/深度采访双轮：产品设计师视角的横切机制.md` -> `references/packaged-knowledge/深度采访双轮：产品设计师视角的横切机制.md`
<!-- PACKAGED_KNOWLEDGE_END -->

# Frontend Interview Dualround

## 这个 skill 在做什么

用**产品设计师视角**做双轮深度采访，把用户脑子里隐性的"架构 + 文案 + 交互"主动拔出来。前轮建立目标边界，后轮结合视觉参考拔细节，两轮**共同防止**代码阶段走偏。

AI 默认只扮演"前端设计师"——接"做个官网"就直奔视觉，导致架构错或文案像 GPT 生成的营销话术。**产品设计师视角**是本 skill 的关键差异化：不仅解决"长什么样"，先解决"讲什么 + 怎么组织"。

## 在阶段化流程里的位置

本 skill 是**横切机制**（见 [[AI前端设计认知框架]]），贯穿阶段 1 和阶段 3：

```
阶段1 需求定义 ← ★ 前轮采访（本 skill）
         ↓        → 主语言 + 目标 + 产品边界
阶段2 试吃六维
         ↓
阶段3 Moodboard 生成 + 选定 ← ★ 后轮采访（本 skill）
         ↓        → 架构 + section + 文案调性 + 交互 + 反向细节
design.md 定稿
         ↓
阶段4 视觉锚定三件套
         ↓
阶段6 代码实现
         ↓
阶段7 迭代微调 ← 用 frontend-design-review 做三段式追问（代码后）
```

和 `frontend-design-review` 的关键分工：

| 机制 | 阶段 | 目的 | 隐性来源 |
|---|---|---|---|
| **本 skill（深度采访双轮）** | 代码**前**（阶段 1 + 阶段 3） | **建立**目标 / 架构 / 文案的边界 | 用户脑子里的产品愿景 |
| **frontend-design-review（三段式追问）** | 代码**后**（阶段 7） | **纠正**"感觉不对"的评审反馈 | 用户看完代码后才涌现的审美直觉 |

两者都依赖"用户脑子里有隐性认知，Agent 必须主动问"的前提，但阶段严格分离。

## 何时进入本 skill

**要进**：
- 阶段 1：新项目启动，用户给了一句"做个 X"的 brief 但细节含糊 → 跑**前轮**
- 阶段 3：六维试吃完成 + Moodboard 生成后、design.md 定稿前 → 跑**后轮**
- 用户说"帮我把这个产品想清楚""我有个想法但说不清""帮我定架构"
- 前端设计剧本阶段 1/阶段 3 路由到本 skill

**不要进**：
- 代码已跑起来，用户看实现说"感觉不对" → `frontend-design-review`（阶段 7）
- 用户要的是**机械判定**的需求澄清（产品 brief 质量门禁） → `req-suite:requirement-clarifier`
- 用户已明确给出架构和文案，不需要采访 → 直接进 writer
- 纯视觉方向选择（Moodboard 选一张） → `frontend-visual-reference`

## 知识库依赖

| 文件 | 用途 | 何时读 |
|------|------|--------|
| `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/深度采访双轮：产品设计师视角的横切机制.md` | 双轮定义 + 五类提问完整模板 + 双轮 vs 三段式边界 + Agent 执行规范 | **启动必读** |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/主语言是设计的第一原则.md` | 主语言 5 问（前轮定位类的验证器） | 前轮定位类提问时读 |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/审美是隐性认知，追问是唯一的解压工具.md` | 选择题优先 + 用户是 vibe coder 的降负担原则 | 组装问题时读 |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/AI前端设计认知框架.md` | 阶段化流程总图（前轮/后轮触发点） | 启动时扫 |

## 执行顺序

```
0. 角色显式切换 → 1. 判断前轮/后轮 → 2. 分批追问（3-5 问/批）→ 3. 反写回 design.md
```

---

## 步骤 0：角色显式切换

进入本 skill 时，Agent 必须**明确宣告**从"前端设计师"切到"产品设计师"：

> 进入深度采访阶段。接下来我会从产品设计师视角问你几组问题，不是聊视觉，是把这个产品想清楚。每批 3-5 个问题，你按感觉回答就行，答不出来的可以跳过。

目的：让用户知道**这轮不是决定配色**，避免用户用视觉语言回答架构问题。

---

## 步骤 1：判断前轮/后轮

| 信号 | 走哪轮 |
|---|---|
| design.md 还没有 §0 主语言 / 只有一句 brief | **前轮** |
| 主语言已定，Moodboard 已选定，design.md 初稿存在但未定稿 | **后轮** |
| 用户说"帮我问清楚这个产品" + 上下文无主语言 | **前轮** |
| 用户说"Moodboard 选定了，还有哪些要确认" | **后轮** |
| 两轮都没做 | **先跑前轮，跑完再走 research，再回来跑后轮** |

---

## 前轮采访：需求阶段建边界

前轮触发条件：用户给了 brief 但细节含糊，**还没跑调研**。

### 前轮五类提问

| 类 | 提问模板 | 为什么问 |
|---|---|---|
| **定位类** | "这个产品在一句话内告诉陌生人，你会怎么说？" / "三个月后这个站成功了，你怎么知道？" | 避免 Agent 对产品没有清晰定位 |
| **用户类** | "谁会来看这个站？他们之前在看什么？离开这个站要去哪里？" | 建立 user journey 语境 |
| **反向类** | "你不想变成什么样？哪些竞品的样子让你觉得反感？" | 反例比正例信息密度高 |
| **资源类** | "这个站要支持多少个页面？有没有真实文案或者需要我帮你生成？" | 建立规模预算 |
| **时间类** | "这个站什么时候要上线？是一次性交付还是持续迭代？" | 影响 scope 控制 |

### 前轮产出

写回 `knowledge/design-docs/design.md`：

- **§0 Main Language**：从定位类 + 反向类收敛的一句动词式主语言（用 [[主语言是设计的第一原则]] 的 5 问验证）
- **§1 Visual Theme 占位**：留待六维试吃填充
- **§11 Interview 前轮段**：记录五类原始问答 + 对应采访日期

### 前轮完成标准

- [ ] 产品一句话（非形容词）有答案
- [ ] 用户画像 + user journey 有答案
- [ ] 至少 1 个反向/反例
- [ ] 规模 + 时间预算定了
- [ ] 主语言通过 5 问验证（否则继续追问）

---

## 后轮采访：视觉定稿前拔细节

后轮触发条件：六维试吃完 + Moodboard 生成 / 选定 + 初稿已写但未定稿。

### 后轮五类提问

| 类 | 提问模板 | 为什么问 |
|---|---|---|
| **架构类** | "首页要不要导航栏？有几级？信息架构是 SPA 还是多页？各页目标是什么？" | AI 默认走最 generic 的 landing 八股，必须逐层确认 |
| **section 类** | "首页从上到下我列 N 个 section 给你，你看哪个要加、删、调顺序？" | 把"首页叙事"从黑箱变成可选择题 |
| **文案调性类** | "Moodboard 是 X 风格，对应文案应该是 A 学院派 / B 口语化 / C 诗意化，你倾向哪个？给个参考句。" | 文案调性必须和视觉调性对齐 |
| **交互路径类** | "用户第一眼看 hero 后，你希望他的下一个动作是什么？往下滑？点 CTA？看 demo 视频？" | 确定转化路径 |
| **反向细节类** | "Moodboard 里的 X 元素你会担心用户看不懂吗？Y 动效会不会太花？" | 用户看到具体视觉后才能识别的担忧 |

### 后轮产出

写回 `knowledge/design-docs/design.md`：

- **§1 Visual Theme**：从文案调性类 + 反向细节类细化描述段
- **§2-§5 架构段**：从架构类 + section 类补 layout / navigation / spacing 的具体约束
- **§7 Don't**：从反向细节类补充
- **§9 Agent Prompt Guide**：从交互路径类 + 文案调性类提炼 example prompts
- **§11 Interview 后轮段**：记录五类原始问答 + Moodboard 选定版本

### 后轮完成标准

- [ ] 架构定稿（导航层级 / 页面数 / 路由方式）
- [ ] 首页 section 清单 + 顺序已确认
- [ ] 文案调性明确（选一个具体方向 + 至少 1 句参考句）
- [ ] 转化路径定了（用户从 hero 到 CTA 的预期动作链）
- [ ] 至少 1 条反向细节（用户对 Moodboard 某元素的担忧）
- [ ] design.md 定稿（frontmatter 升级到 `status: verified` 或保持 signal 但 stage 改为 `3-finalized`）

---

## 步骤 2：分批追问（3-5 问/批）

**硬规则**：不一次性甩 20 个问题给用户。按以下节奏：

1. 一次问 3-5 个
2. 按用户回答追问（往深问）
3. 一类答完再进下一类
4. 用户答不上来的问题**先跳过**，不纠缠

### 选择题优先，开放题兜底

用户画像是 vibe coder，**选择题降低回答负担**。优先结构：

```
Q：首页从上到下我列 4 个 section：
  A. Hero + Tagline + CTA
  B. 核心价值三宫格
  C. 客户案例 / 社会认证
  D. 底部 CTA + Footer

你想要：
- 保留这个顺序
- 加一个 section（你想加什么？）
- 删一个 section（哪个？）
- 调顺序（改成什么顺序？）
```

**不要**这样问：

```
❌ "你希望首页有几个 section？"（用户不知道该答几个）
❌ "首页结构你希望是什么样？"（太开放）
```

### 反模式清单

- ==跳过前轮直接试吃==：看参考站前先定位
- ==跳过后轮直接写代码==：最常见的失败模式
- ==把采访做成问卷==：20 题一次性甩给用户
- ==采访完不回写 design.md==：结果只留对话里，下次 session 丢失

---

## 步骤 3：反写回 design.md

**硬约束**：所有采访结果必须落回 `knowledge/design-docs/design.md` 对应段落，不能只留在对话里。

每轮采访完产出：

- design.md 对应段更新
- §11 Interview 段补充一条记录：
  ```markdown
  ### 前轮采访 (2026-04-21)
  - 五类原始问答摘要
  - 收敛出的主语言 / 目标
  - 遗留未决问题（下次采访追问）

  ### 后轮采访 (2026-04-25)
  - 五类原始问答摘要
  - 架构定稿 / 文案调性选项
  - 遗留：...
  ```
- frontmatter `last_updated` 更新

---

## 和其他 skill / 剧本的边界

| 场景 | 走谁 |
|---|---|
| **已定稿项目的二开 / 增量扩展** | `frontend-iteration-planner`（场景 C 入口，本 skill 会被其按 tier 轻量调用） |
| 代码前建目标 / 架构 / 文案 | 本 skill（前轮 / 后轮） |
| 代码**后**用户说"感觉不对" | `frontend-design-review`（阶段 7 三段式追问） |
| 机械判定 product-brief 质量 | `req-suite:requirement-clarifier` |
| 六维试吃本身 | `frontend-design-research`（阶段 2） |
| 派生 Moodboard | `frontend-visual-reference`（阶段 4） |
| 写 design.md kun 15 段交付版 | `frontend-design-writer` |
| 纯视觉评审（没有 product 层问题） | `frontend-design-review` |

## 完成标准

前轮：

- [ ] 角色切换显式宣告
- [ ] 前轮五类都过了一遍（未决项明确标记）
- [ ] design.md §0/§1/§11 前轮段更新
- [ ] 用户确认主语言通过 5 问验证

后轮：

- [ ] 角色切换显式宣告
- [ ] 后轮五类都过了一遍
- [ ] design.md §1-§5/§7/§9/§11 后轮段更新
- [ ] 架构定稿 + section 顺序 + 文案调性 + 转化路径都有明确答案
- [ ] design.md 从 signal 升级到 `stage: 3-finalized`（或等价标记）

## 本 skill 的 deletion-spec

- **触发删除条件**：当 AI 默认能自主识别"产品设计师视角缺位"并主动触发引导式提问（不需要本 skill 提醒），且前轮/后轮时序被稳定执行时，本 skill 可降级为剧本层提醒或退场。若"双轮"模型被证伪（单轮足够 / 三轮更好），需重写。
- **禁用方式**：从 `plugins/frontend-suite/skills/` 删除本目录即自动停止发现。
- **卸载清单**：
  - `frontend-design-research` / `frontend-design-writer` / `frontend-visual-reference` / `frontend-design-review` 的"边界表"和前置检查段引用本 skill，需同步清理
  - `plugins/frontend-suite/.claude-plugin/plugin.json` description 需回退
  - `~/.agents/agent_prompt_core/shared/playbooks/前端设计_剧本.md` 阶段 1 / 阶段 3 路由需改回老版（原来混在 research 里）
  - [[深度采访双轮：产品设计师视角的横切机制]] 笔记"对应 skill"字段需同步