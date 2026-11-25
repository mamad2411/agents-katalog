---
name: frontend-iteration-planner
description: 前端项目二开 / 增量改进的入口路由器——已定稿 design.md 的项目要加新页面 / 新 section / 微改 token 时，先读老资产（design.md + visual-anchors/ + motion-prompts/），按三档 tier 判定（T1 新页面 / T2 新 section / T3 微改）输出本轮最小流程路径，阻止模型"假装新项目"把已定风格冲掉。本 skill 只做路由和前置防呆，不自己执行具体阶段——执行仍委给 dualround / visual-reference / design-writer / design-review 等原 skill。触发：用户说"加个新页面""在首页加一个 section""改一下这个按钮颜色""design.md 已经有了，现在要扩展 X""新路由 /blog / /pricing"。不用于全新项目从零启动（那是阶段 1-7 完整流程，走 frontend-interview-dualround 前轮）、不用于整站视觉重写（全站重写需要回阶段 2-4 重跑）、不用于纯 bug 修复（那是开发实现剧本）。
---

<!-- PACKAGED_KNOWLEDGE_START -->
## Packaged Knowledge Snapshot

This packaged copy includes local note snapshots for portability.
When the original Obsidian absolute path is unavailable, use the packaged snapshot instead:

- `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/AI前端设计认知框架.md` -> `references/packaged-knowledge/AI前端设计认知框架.md`
<!-- PACKAGED_KNOWLEDGE_END -->

# Frontend Iteration Planner

## 这个 skill 在做什么

**二开场景的入口路由器**。已有 design.md 定稿 + visual-anchors/ 选定 + motion-prompts/ 产出的项目要扩展时，先强制读老资产（防"假装新项目"），再按三档 tier 输出本轮的**最小执行路径**，避免每次扩展都从阶段 1 重跑。

本 skill 不自己跑采访 / 出图 / 写代码——它只**决定**本轮走哪几步、跳哪几步、老资产怎么读、新产出往哪写，然后移交给对应的原 skill 执行。

## 在阶段化流程里的位置

本 skill 是**场景 C（二开 / 增量）的专用入口**，横入于阶段 1 前。原 7 阶段流程的 skill 都在它下游：

```
场景 A：全新项目
  阶段 1 → 2 → 3 → 4 → 5 → 6 → 7（完整 7 阶段）

场景 B：整站视觉重写
  回阶段 2 重跑六维 + 阶段 3 后轮 + 阶段 4 视觉锚定三件套（全量重生）

场景 C：二开 / 增量（本 skill）
  ★ frontend-iteration-planner
     ↓（读老资产 + tier 判定）
  按 Tier 1/2/3 输出最小路径：
     T1 新页面  ：轻量后轮 → 4B 局部 mockup → 6 代码 → 7 review + 反写 design.md
     T2 新 section：最小后轮 → 可选 4B → 6 代码 → 7 review + 反写
     T3 微改    ：直接 6 代码 → 7 review + 反写对应段
```

## 核心赌局

**老 design.md 是资产，不是债务**。用户已经花过一轮心思钉死主语言 / 六维 token / 动效双向性，二开必须**沿用**不能**重新发明**。模型默认倾向"看到任务就从零开始"——本 skill 是这条倾向的硬杀手。

## 何时进入本 skill

**要进**：

- 用户说："加个新页面" / "新路由 /X" / "在首页加一个 section" / "改一下这个按钮 / token / 动效参数"
- 用户说："design.md 已经有了，现在要扩展 / 迭代 / 加功能"
- 项目根目录存在 `knowledge/design-docs/design.md` 且 frontmatter `stage` ≥ `3-finalized` 或等价状态
- `frontend-anti-slop-gate` / `frontend-design-review` 等下游 skill 检查时发现本次任务是**增量**而非新建

**不要进**：

- 项目是全新的（没有 `knowledge/design-docs/` 目录或只有空骨架） → `frontend-interview-dualround` 前轮
- 用户明确说要**整站视觉重写**（主语言不变但视觉方向换） → 回阶段 2-4 重跑
- 纯 bug 修复 / 纯脚本改动 / 无 UI 表面 → 开发实现剧本
- 单纯改 copy 文案（不涉及视觉 / 交互 / 架构） → 直接改代码 + 反写 design.md §9

## 知识库依赖

| 文件 | 用途 | 何时读 |
|------|------|--------|
| `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/AI前端设计认知框架.md` | 阶段化流程总图（场景 C 在总图的位置） | **启动必读** |
| 项目内 `knowledge/design-docs/design.md` | 主语言 + 六维 token + §9 Agent Prompt Guide + §14 Motion Prompts 索引 | **步骤 0 必读** |
| 项目内 `knowledge/design-docs/visual-anchors/` | Moodboard 选定版 + 已有页面 mockup + 帧序列图 | 步骤 0 若存在必扫目录清单 |
| 项目内 `knowledge/design-docs/motion-prompts/` | 已有核心动效的微观 prompt | 步骤 0 若存在必扫目录清单 |

启动时只拉总图 + 项目 design.md，visual-anchors / motion-prompts 扫目录索引（不读全文）。

## 执行顺序

```
步骤 0 老资产前置读取 + 成熟度判定
  ↓
步骤 1 tier 判定（用户一次问答定档）
  ↓
步骤 2 输出最小流程路径 + 移交下游 skill
  ↓
步骤 3 回写 design.md 迭代日志段
```

---

## 步骤 0：老资产前置读取（硬防呆）

### 0.1 必读三件套

不管 tier 是什么，进入本 skill 后**必须**先做：

| 动作 | 目标 | 缺失时处理 |
|---|---|---|
| Read `knowledge/design-docs/design.md` | 拿到主语言 / 六维 token / §9 Agent Prompt Guide / §10 Motion Spec / §14 Motion Prompts 索引 | **中止**——告知用户"没找到 design.md，这是新项目，请走 `frontend-interview-dualround` 前轮" |
| Glob `knowledge/design-docs/visual-anchors/*.md` 和 `*.png` | 拿到 Moodboard 选定版 + 已有 mockup + 帧序列图清单 | 若目录不存在——**降级标记**"visual-anchors 缺失"，但不中止（早期项目可能跳过了阶段 4） |
| Glob `knowledge/design-docs/motion-prompts/*.md` | 拿到已写的微观动效 prompt 清单 | 若目录不存在——**降级标记**"motion-prompts 缺失"，但不中止 |

### 0.2 老资产摘要回显

读完后给用户一段**摘要回显**（让用户确认老资产没读错）：

```
已读老资产：
- 主语言（§0）：<从 design.md §0 复制动词句式一句>
- 设计阶段：<frontmatter stage 字段>
- Moodboard：<visual-anchors/ 下的 locked 版本文件名>
- 核心动效：<motion-prompts/ 下的组件名清单>
- 产品类型：<展示型 / 工具型，从 research 阶段或后轮记录判断>
```

如果用户说"这里读错了" → 先纠正再往下，不直接进步骤 1。

### 0.3 deadline trigger

**中止条件**：
- design.md 不存在 → 中止，路由到 `frontend-interview-dualround` 前轮
- design.md 的主语言（§0）为空或是形容词堆砌 → 中止，路由到 `frontend-interview-dualround` 前轮
- design.md frontmatter 标记 `stage: 2-initial-draft` 或更早 → 中止，路由回 `frontend-design-research` + 后轮采访定稿

**警告但不中止**：
- visual-anchors/ 缺失 → 告知用户"这个项目跳过了阶段 4，本次若需出图建议补"，但让用户决定
- motion-prompts/ 缺失且当前是展示型 → 告知用户"核心动效微观 prompt 缺失，若本次涉及动效建议现场生成"

---

## 步骤 1：Tier 判定

### 1.1 单问题判定

对用户问一次：

```
这次要加 / 改什么？选一个最贴近的：
A. 新增独立页面 / 路由（例：加 /blog、/pricing、全新 section 组）
B. 在已有页面加新 section / feature block（例：home 加 testimonials、product 加 compare 表）
C. 改现有 token / 单组件 / 动效参数（例：改主按钮颜色、调 hero duration 从 0.8s 到 0.6s）
```

用户答什么 → 对应进 T1 / T2 / T3。如果用户答不准：

- **跨档**（比如"加一个新页面，而且想改主色"）→ 拆成两次执行：先 T1 加页面（不改主色），再 T3 调主色。**禁止**把两档合成一次，否则流程预算失控
- **介于中间**（"加一个很大的 section，大到像小页面"）→ 看是否独立路由，有独立路由走 T1，没独立路由走 T2
- **完全说不清**（"就是想改改看"）→ 回 `frontend-design-review` 做三段式追问，先把反馈语言化

### 1.2 判定记录

把 tier + 本轮范围描述写到 design.md §15 迭代日志段（见步骤 3）。

---

## 步骤 2：按 Tier 输出最小流程路径

### Tier 1：新页面（独立路由 / 全新 section 组）

**最小路径**：

```
读老资产（步骤 0 已完成）
  ↓
Gate 1：主语言沿用吗？
  → 沿用 → 继续
  → 想换方向 → 回场景 B（整站重写），不走 T1
  ↓
轻量后轮采访 ← frontend-interview-dualround（后轮，但只问新页面的架构/section/文案/交互）
  ↓
阶段 4B 局部 mockup ← frontend-visual-reference
  （跳 A Moodboard——方向已钉；跳 C 帧序列除非新页面引入新核心动效）
  ↓
阶段 6 代码 ← 开发实现剧本 + frontend-anti-slop-gate
  （读取顺序：design.md §0-§14 + visual-anchors/ 新 mockup + 已有 motion-prompts/）
  ↓
阶段 7 review + 反写 ← frontend-design-review
  （反写回 design.md：新增路由写 §5 Layout + §9 Example Prompts；新组件追加 §4；新动效追加 §14）
```

**老资产保护**：
- §0 主语言锁定，新页面必须在该语言下
- §2 Colors / §3 Typography / §5 Spacing 直接沿用，不改
- §4 Component Stylings 只增不改（可加新变体，不动老变体）
- §14 Motion Prompts 若新页面引入新核心动效，调用 `frontend-motion-prompt-writer` 新增一份

**完成标准**：
- [ ] 新页面 mockup 在 `visual-anchors/mockup-{new-page}.png` 就位
- [ ] 代码实现通过 `frontend-anti-slop-gate` 扫描
- [ ] design.md §5/§9 新增引用、§14 新动效（如有）入表
- [ ] design.md §15 迭代日志追加一条（tier / 范围 / 日期 / 影响段）

---

### Tier 2：新 section / feature block

**最小路径**：

```
读老资产（步骤 0 已完成）
  ↓
最小后轮采访 ← frontend-interview-dualround（后轮轻量模式，只问三类）
  - section 类：这个 section 的目标 / 主元素 / 视觉层级
  - 文案调性类：是否沿用既定调性？有没有参考句？
  - 交互路径类：用户从这个 section 期望做什么？（CTA / 继续滚 / 跳转）
  ↓
可选阶段 4B 单 section mockup ← frontend-visual-reference
  - 复杂 section（多列 / 有插图 / 有动效）→ 出图
  - 简单 section（标题 + 文字 + CTA）→ 跳过，直接进代码
  ↓
阶段 6 代码 ← 开发实现剧本 + frontend-anti-slop-gate
  （读取 design.md §4 Component Stylings + §9 Example Prompts + 该页已有 mockup）
  ↓
阶段 7 review + 反写 ← frontend-design-review
  （反写回 design.md：新 section 写入 §9 Example Prompts 对应页面；新组件变体追加 §4；新增文案调性参考句追加 §1 / §9）
```

**老资产保护**：
- §0-§3 所有 token 锁定
- §4 Component Stylings 优先复用已有组件，不为单个 section 新建组件
- §5 Layout Principles spacing 体系沿用，新 section 只能从已有 spacing scale 里选值

**完成标准**：
- [ ] 代码实现通过 `frontend-anti-slop-gate` 扫描
- [ ] 新 section 用的是 §4 已有组件或合理变体
- [ ] design.md §4 / §9 更新（若引入新组件变体）
- [ ] design.md §15 迭代日志追加一条

---

### Tier 3：微改（token / 单组件 / 单动效参数）

**最小路径**：

```
读老资产（只读 design.md 对应段，不扫 visual-anchors 全目录）
  ↓
直接阶段 6 改代码 ← 开发实现剧本 + frontend-anti-slop-gate
  （不做采访 / 不出图 / 不重 review 老方向）
  ↓
阶段 7 轻量 review + 反写 ← frontend-design-review（微改模式）
  （反写回 design.md 对应段：改 token 更新 §2/§3/§5/§6；改动效参数更新 §10 / §14 对应行）
```

**老资产保护**：
- 改的是**该段内部的值**，不改结构
- 改 token 必须同步所有引用处（用 Grep 扫用该 token 的组件）
- 改动效 duration / easing 必须更新 §10 量化语法 + §14 对应组件 prompt

**警戒边界**：
- Tier 3 看起来最小，但**最容易滑向 Tier 2**（"改一个按钮颜色"→"加一个新按钮 variant"→"加一个带新按钮的新 section"）。如果改着改着超出单 token / 单组件 / 单参数范围，**立即中止 Tier 3，回步骤 1 重判**

**完成标准**：
- [ ] 改动范围确实是单 token / 单组件 / 单参数
- [ ] design.md 对应段更新（hex / size / duration 等具体值）
- [ ] 所有引用处同步（用 Grep 扫）
- [ ] design.md §15 迭代日志追加一条

---

## 步骤 3：design.md §15 迭代日志

二开场景必须留痕。在 design.md 末尾加一段（如不存在则创建）：

```markdown
## 15. Iteration Log

| Date | Tier | Scope | Affected Sections | Planner |
|---|---|---|---|---|
| 2026-04-21 | T1 | 加 /blog 路由 + 列表页 | §5 / §9 / §14 | frontend-iteration-planner |
| 2026-04-25 | T2 | home 加 testimonials section | §4 / §9 | frontend-iteration-planner |
| 2026-04-27 | T3 | 主按钮 primary 色从 #2b6cb0 → #1a4d8f | §2 | frontend-iteration-planner |
```

日志意义：
- 下次二开可以看历史避免撞车
- entropy-scan 和 project-retrospective-closedloop 可以从这里提取"本阶段视觉层变动"
- 老资产腐化判定的锚点（看 Affected Sections 集中在哪里）

---

## 场景 C 的硬边界

- **禁止合并 tier**：一次任务只走一档，跨档拆成多次
- **禁止绕过步骤 0**：即便用户说"我知道 design.md 里写什么"，也要 Read 一次（模型记忆不可靠）
- **禁止在 T3 微改里加新组件**：那是 T2
- **禁止在 T1/T2 里换主语言或换 Moodboard 方向**：那是场景 B 整站重写
- **样板不入笔记库**：沿用阶段 4 的硬规则，本 skill 不产出任何需要住在 Obsidian 的样板
- **反 slop 横切仍生效**：T1/T2/T3 的阶段 6 代码环节都挂 `frontend-anti-slop-gate`

## 完成标准

- [ ] 步骤 0 三件套读取完成，摘要回显获用户确认
- [ ] 步骤 1 tier 判定明确（T1 / T2 / T3 之一），跨档情况已拆分
- [ ] 步骤 2 最小流程路径按 tier 执行，不多做、不少做
- [ ] 下游 skill（dualround 后轮 / visual-reference / design-review）已按流程触发
- [ ] design.md §15 迭代日志追加条目（tier / scope / affected sections / date）
- [ ] 所有产出（代码 / 新 mockup / 新 motion-prompts）回写到 design.md 对应段

## 与其他 skill / 剧本的边界

| 场景 | 走谁 |
|---|---|
| 全新项目从零启动 | `frontend-interview-dualround` 前轮（阶段 1） |
| 整站视觉重写（换主 Moodboard 方向） | 回阶段 2-4 重跑（research → dualround 后轮 → visual-reference） |
| 本 skill 判定完的后轮采访 | `frontend-interview-dualround`（按 tier 裁剪问题） |
| 本 skill 判定完的局部 mockup | `frontend-visual-reference`（跳 A 阶段，只走 B 单页 / 单 section） |
| 本 skill 判定完的动效微观 prompt 新增 | `frontend-motion-prompt-writer` |
| 本 skill 判定完的代码实现 | 开发实现剧本 + `frontend-anti-slop-gate` |
| 本 skill 判定完的 review | `frontend-design-review` |
| 本 skill 判定完的 design.md 反写 | `frontend-design-writer`（Round 2/3/4 对应段增量更新） |
| 六维骨架本身需要重做 | `frontend-design-research`（回阶段 2） |
| 纯 bug 修复 / 无 UI 表面 | 开发实现剧本 |
| 对外说明书 / README / 客户交付文档 | 走独立 `docs/` / `deliverables/`，不进 knowledge/ |

## 本 skill 的 deletion-spec

- **触发删除条件**：当模型能默认稳定识别"已定稿项目的扩展任务" + 主动执行"先读老资产再扩展"且三档 tier 裁剪被下游 skill 自行吸收（比如 dualround 能自己判定前轮/后轮/二开轻量后轮）时，本 skill 可降级为剧本层提醒或退场。若三档 tier 被证伪（实际执行发现两档够 / 四档更准）需重写。若二开场景整体被 req-suite 吸收进项目生命周期管理，本 skill 可并入 req-suite。
- **禁用方式**：从 `plugins/frontend-suite/skills/` 删除本目录即自动停止发现；下游 skill 的"边界表"里本 skill 对应行也要一并清理。
- **卸载清单**：
  - `plugins/frontend-suite/README.md` 的 8 skill 表格需回退到 7 skill
  - `plugins/frontend-suite/.claude-plugin/plugin.json` description 需回退
  - `plugins/.claude-plugin/marketplace.json` frontend-suite 描述需回退
  - `~/.agents/agent_prompt_core/shared/playbooks/前端设计_剧本.md` 场景 C 路由段需删除
  - 下游 skill（`frontend-design-research` / `frontend-interview-dualround` / `frontend-visual-reference` / `frontend-motion-prompt-writer` / `frontend-design-writer` / `frontend-design-review` / `frontend-anti-slop-gate`）的"边界表"里"二开 / 新页面 / 新 section / 微改"对应行需改回直接路由老版
  - 项目内 `knowledge/design-docs/design.md` §15 迭代日志段由用户自行决定保留或删除