---
name: frontend-design-writer
description: 阶段 1-7 持续维护的 design.md 主写手——把调研（六维试吃）+ 双轮深度采访 + 视觉锚定三件套 + 动效实现 prompt 集全部压缩为 Agent 可执行的设计契约。kun 版 15 段三轮写作顺序（原 12 段 + 新增 §12 Moodboard Prompt / §13 Page Mockup Prompt / §14 Motion Prompts 三段视觉锚定引用）。同时维护 DESIGN-LANGUAGE.md（低频）+ design.md（高频）+ MOTION-SPEC.md（中频）三份。不用于调研本身（那是 frontend-design-research）、不用于从零搭 knowledge/ 骨架（那是 req-suite:project-spec）、不用于单 token 微调（直接编辑即可）、不用于生成微观动效实现 prompt（那是 frontend-motion-prompt-writer）。
---

<!-- PACKAGED_KNOWLEDGE_START -->
## Packaged Knowledge Snapshot

This packaged copy includes local note snapshots for portability.
When the original Obsidian absolute path is unavailable, use the packaged snapshot instead:

- `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/AI前端设计认知框架.md` -> `references/packaged-knowledge/AI前端设计认知框架.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/主语言是设计的第一原则.md` -> `references/packaged-knowledge/主语言是设计的第一原则.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/六维：形色字构质动是网站试吃的机械骨架.md` -> `references/packaged-knowledge/六维：形色字构质动是网站试吃的机械骨架.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/AI 前端动效盲区与采访补偿.md` -> `references/packaged-knowledge/AI 前端动效盲区与采访补偿.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/动效文档两层：MOTION-SPEC vs 实现 prompt 集.md` -> `references/packaged-knowledge/动效文档两层：MOTION-SPEC vs 实现 prompt 集.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/深度采访双轮：产品设计师视角的横切机制.md` -> `references/packaged-knowledge/深度采访双轮：产品设计师视角的横切机制.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/视觉锚定三件套：代价结构与资产生成双路径.md` -> `references/packaged-knowledge/视觉锚定三件套：代价结构与资产生成双路径.md`
<!-- PACKAGED_KNOWLEDGE_END -->

# Frontend Design Writer

## 这个 skill 在做什么

把前端阶段 1-4 的所有产出（主语言、六维试吃数据、双轮采访记录、视觉锚定三件套、资源选型）压缩成三份 Agent 可执行的交付文件。核心过程是**三轮写作**，不是从 §1 顺着写到 §14。

## 在阶段化流程里的位置

本 skill **贯穿阶段 1-7**（见 [[AI前端设计认知框架]]），是所有其他前端 skill 的汇总写手：

```
阶段1 前轮采访 ─┐
阶段2 六维试吃 ─┤
阶段3 后轮采访 ─┼─→ design.md 初稿 → 定稿
阶段4 视觉锚定 ─┘    ↓
                    §12 §13 §14 引用视觉锚定三件套
                    ↓
阶段6 代码实现 ──── Pre-flight 外显化读本文件
                    ↓
阶段7 迭代微调 ──── review 反写回本文件
```

kun 15 段分工：
- §0-§11：原 12 段（主语言 + token + Agent prompt guide + motion spec + interview）
- **§12 Moodboard Prompt**（视觉锚定 A）：引用 `knowledge/design-docs/visual-anchors/moodboard-prompt.md`
- **§13 Page Mockup Prompt**（视觉锚定 B）：引用 `knowledge/design-docs/visual-anchors/mockup-*.md`
- **§14 Motion Prompts**（视觉锚定 C + 动效微观层）：引用 `knowledge/design-docs/visual-anchors/motion-frames/` 和 `knowledge/design-docs/motion-prompts/`

## 何时进入本 skill

**要进**：
- 阶段 2 试吃六维刚完成，`knowledge/design-docs/` 下已有调研产出，需要落成 design.md 初稿
- 阶段 3 后轮采访完成，design.md 定稿
- 阶段 4 视觉锚定三件套选定后，§12-§14 引用段落要更新
- 阶段 7 迭代微调收敛的 token/motion/Tweak 要反写回 design.md
- 用户说"写 DESIGN.md" / "把调研结果转成交付文件" / "生成设计文件"
- 项目迭代后需要更新 DESIGN.md（已有旧版，需要根据新调研或新决策刷新）

**不要进**：
- 还没有调研产出 → 先走 `frontend-design-research`
- 还没做双轮采访（产品边界模糊） → 先走 `frontend-interview-dualround`
- 整个项目 knowledge/ 骨架从零搭 → 先走 `req-suite:project-spec`
- 生成某个核心动效的微观实现 prompt（LoadingScreen 风格） → 走 `frontend-motion-prompt-writer`
- 派生 Moodboard / 示意图 / 帧序列图 → 走 `frontend-visual-reference`
- 纯代码实现任务 → 走开发实现剧本
- 只改一个颜色值或字号 → 直接编辑对应文件

## 知识库依赖

本 skill 只是"写作剧本"，方法论住在下面这几份笔记里，不复制。

| 文件 | 用途 | 何时读 |
|------|------|--------|
| `/Users/kunkun/note/01-AI工程/AI设计与前端/03-交付契约/DESIGN.md 写作与分发手册.md` | kun 15 段完整模板 + 三轮写作顺序 + CLI 双路径 + 字数预算 | **启动必读** |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/03-交付契约/DESIGN.md 格式与七层框架的位置.md` | 为什么拆三份、和 alexpate/Stitch 的关系 | 用户问"为什么要三份文件"时读 |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/AI前端设计认知框架.md` | 阶段化流程总图（本 skill 的定位） | 启动时扫阶段总表 |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/主语言是设计的第一原则.md` | 主语言的 5 问验证法 + 通道分工 | Round 1 写 §0 时读 |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/六维：形色字构质动是网站试吃的机械骨架.md` | 六维骨架——把调研产出挂到六维下 | Round 2 组织 token 时读 |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/视觉锚定三件套：代价结构与资产生成双路径.md` | §12-§14 的内容来源 | 写 §12-§14 时读 |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/动效文档两层：MOTION-SPEC vs 实现 prompt 集.md` | §10 宏观 vs §14 微观 prompt 的分层 | 写 §10 和 §14 时读 |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/AI 前端动效盲区与采访补偿.md` | 动效量化语法 + 双向性约束 | Round 3 写 §10 时读 |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/深度采访双轮：产品设计师视角的横切机制.md` | §11 Interview 的采访来源结构（双轮） | 写 §11 时读 |

启动时只拉第一份，其他按触发条件读。

## 前置检查

进入写作前先确认五个前提（§12-§14 的前提非强制，等视觉锚定完成后回来补）：

| 前提 | 检查方式 | 缺失时怎么办 |
|------|---------|-------------|
| **前轮采访完成** | design.md §0-§1 目标与主语言有值，来自 dualround 前轮 | 路由到 `frontend-interview-dualround` 前轮 |
| **六维调研产出存在** | `knowledge/design-docs/` 下有六维试吃记录或等价 DESIGN-CONTEXT.md | 路由到 `frontend-design-research` |
| **主语言已定义** | Main Language 段非空，且是动词句式不是形容词 | 路由回 `frontend-design-research` 主语言步骤 |
| **后轮采访完成**（定稿时） | 架构 / section / 文案调性 / 交互路径四类有答案 | 路由到 `frontend-interview-dualround` 后轮 |
| **动效素材存在** | motion 记录有至少 1 条量化语法条目（工具型可近空但要显式"动效极简"声明） | 路由回 `frontend-design-research` 动效采访 |

§12-§14 视觉锚定引用段的前提（阶段 4 完成后回填）：
- §12 Moodboard 选定 → 回填 moodboard-prompt.md 路径
- §13 完整网页示意图产出 → 回填 mockup-*.md 路径
- §14 帧序列 + 实现 prompt 到位 → 回填 motion-frames/ 和 motion-prompts/ 索引

## 执行顺序：四轮写作（原三轮 + Round 4 视觉锚定回填）

```
Round 1 定调 → Round 2 量化 → Round 3 组装 → Round 4 视觉锚定引用（§12-§14）
```

**不要从 §1 顺着写到 §14**。顺着写的常见失败：先写 §4 组件，发现没有 §0 主语言指导就不知道按钮应该 sharp 还是 round。

Round 1-3 覆盖原 12 段（§0-§11），Round 4 在阶段 4 完成后回填 §12-§14 三段视觉锚定引用——**不是一次性写完 15 段，是分两次**。

---

### Round 1：定调（§0 + §7 + §11）

**目标**：先建叙事透镜，后面所有 token 取舍被它约束。这一轮**不写任何 hex 值**。

**§0 Main Language**（30-50 行，最重要）
- One-Sentence Narrative：动词句式，不是形容词。"滚动时混沌收敛为有序" ✓，"高级极客感" ✗
- Time Dimension：用户从打开到离开经历什么变化（初始状态 / 中段 / 终态）
- Channel Assignments：8 个通道（动效/字体/布局/背景/颜色/文案/细节/交互）各承载什么
- Intentional Rejections：为了主语言清晰，主动放弃什么
- Anchor Reference：哪个已有作品体现了类似主语言

**§7 Do's and Don'ts**（20-30 行）
- Do 8-10 条：写清楚参数，不写抽象原则
- Don't 8-10 条：列出反模式和它会破坏什么

**§11 Interview & References**（20-40 行）
- Visual Thesis Source：主语言从用户哪段话追问出来
- Anti-References：明确不想要的方向 + 理由
- Validation Log：留空，后续迭代填写
- Open Questions：尚未拍板的事项

---

### Round 2：Token 量化（§2 + §3 + §5 + §6 + §8）

**目标**：从 DOM 量化数据机械提取。这是机械劳动，可选 `npx getdesign` 起手。

**§2 Color Palette & Roles**（30-50 行）
- 按 Background Surfaces / Text & Content / Brand & Accent / Status / Border 五类分组
- 每个颜色必须有语义名 + hex + 用途描述

**§3 Typography Rules**（40-60 行）
- Font Family + OpenType features
- Hierarchy 表：Role / Font / Size / Weight / Line Height / Letter Spacing / Notes
- 覆盖 Display XL 到 Mono 至少 10 个层级
- Principles 3-5 条非显然规则

**§5 Layout Principles**（20-30 行）
- Spacing System（base unit + scale）
- Grid & Container（max width + hero + feature sections）
- Whitespace Philosophy
- Border Radius Scale

**§6 Depth & Elevation**（15-25 行）
- 5-6 级 elevation 表（Level 0 到 Level 5）
- Shadow Philosophy

**§8 Responsive Behavior**（20-30 行）
- Breakpoint 表（5 档）
- Touch Targets
- Collapsing Strategy（字号/nav/卡片/间距各自怎么缩）
- Image Behavior

**CLI 起手式**：如果时间紧，先跑 `npx getdesign@latest add <气质最近的站>` 拿到 Stitch 9 段骨架，再用调研的 DOM 量化数据逐段校正。

---

### Round 3：组装（§1 + §4 + §9 + §10）

**目标**：把 Round 1+2 的材料组装成 Agent 可执行的形式。这是创造性劳动。

**§1 Visual Theme & Atmosphere**（15-25 行）
- 一段主叙事描述（250-400 字）
- Key Characteristics 6-10 条

**§4 Component Stylings**（60-100 行，最长的段）
- Buttons（Primary / Ghost / Icon / Pill 各自 default/hover/focus 三态参数）
- Cards & Containers
- Inputs & Forms
- Badges & Pills
- Navigation
- Image Treatment

**§9 Agent Prompt Guide**（30-50 行，DESIGN.md 最有价值的一段）
- Quick Color Reference（7-8 个常用颜色快速查表）
- Example Component Prompts（至少 5 条覆盖 hero / card / badge / nav / special）
- Iteration Guide（3-7 条 Agent 迭代时的不变量）

**§10 Motion Spec**（40-80 行，最难写的段）
- Motion Philosophy（动效在主语言里扮演什么角色）
- Global Rules（双向性默认、Easing 库、Duration 库、Stagger）
- Core Motion Catalog（用量化语法 `[触发] → [主体] → [变化] → [时序]`）
- Layer Hierarchy（多动效共存时的优先级）
- Motion Don'ts
- Source（每条动效的采访来源）

§10 是 MOTION-SPEC.md 给 Agent 的压缩版，两份内容应同步。

---

### Round 4：视觉锚定引用（§12 + §13 + §14，阶段 4 完成后）

**目标**：把视觉锚定三件套（由 `frontend-visual-reference` 产出）+ 动效微观 prompt（由 `frontend-motion-prompt-writer` 产出）的路径**索引**进 design.md。这一轮只写引用+元信息，不复制正文。

**§12 Moodboard Prompt**（8-15 行）
- Prompt 文件路径：`knowledge/design-docs/visual-anchors/moodboard-prompt.md`
- 状态：draft / generating / **locked**（选定哪张）
- 选定版本：v1 / v2 / v3
- 核心要素清单一行概述（色板 / 材质 / 符号族 / 字体 / UI 片段 / 反例）

**§13 Page Mockup Prompt**（10-20 行）
- 主页 prompt 文件：`knowledge/design-docs/visual-anchors/mockup-home.md`
- 子页 prompt 文件清单：`mockup-{feature/pricing/...}.md`
- 每个 mockup 的状态：draft / locked
- 生成顺序说明（先主页 → OK → 子页，单线）

**§14 Motion Prompts**（15-30 行）
- 帧序列 prompt 目录：`knowledge/design-docs/visual-anchors/motion-frames/`
- 实现 prompt 目录：`knowledge/design-docs/motion-prompts/`
- 核心动效组件清单表格：
  ```
  | 组件 | 帧序列 prompt | 实现 prompt | 状态 |
  | LoadingScreen | motion-frames/loading.md | motion-prompts/LoadingScreen.md | locked |
  | Hero 入场 | motion-frames/hero-entry.md | motion-prompts/HeroEntry.md | draft |
  ```
- §14 vs §10 分工提示：§10 宏观清单（人读），§14 微观 prompt 索引（Agent 写代码时读）

---

## 产出规格

三份文件写入项目 `knowledge/design-docs/`：

### DESIGN-LANGUAGE.md（给人读，低频更新）

| 内容 | 来源 |
|------|------|
| 一句话主叙事（动词） | Round 1 §0 |
| 时间维度 | Round 1 §0 |
| 8 个通道各自角色 | Round 1 §0 |
| "不做什么"清单 + 理由 | Round 1 §0 + §7 |
| 参考锚点 | Round 1 §0 |
| 采访溯源 | Round 1 §11 |

项目第一周定完就锁。后续迭代不动这份。

### DESIGN.md（给 Agent 读，kun 15 段，高频更新）

400-600 行。格式见上方四轮写作的 §0-§14 完整结构。前 9 段保持与 Stitch / getdesign CLI 生态兼容，§10-§14 是 kun 版差异化段。

Frontmatter：
```yaml
---
status: signal
last_updated: YYYY-MM-DD
source: frontend-design-writer skill
---
```

### MOTION-SPEC.md（人+Agent 并读，中频更新）

| 内容 | 来源 |
|------|------|
| 每个核心动效的量化语法 | 调研阶段 motion-spec.md + Round 3 §10 |
| 双向性约定 | 动效采访 |
| 层级关系 | 动效采访 |
| 反例清单 | 动效采访 |
| 采访来源 | 动效采访记录 |

DESIGN.md 的 §10 是本文件给 Agent 的压缩版，两份同步维护但各服务不同读者。

> **小项目合并规则**：小项目 / 原型可以把三份合成单份 `DESIGN-CONTEXT.md`，但要保留三段结构（主语言段 + token 段 + 动效段），不退回到"一段话模糊描述"。

---

## CLI 快速路径

时间紧或原型阶段的简化流程：

1. 跑 `npx getdesign@latest add <气质最近的站>`（30 秒拿到 Stitch 9 段骨架）
2. 手写 §0 Main Language（哪怕只有 2-3 行，也比没有强）
3. 手写 §10 Motion Spec（哪怕只有 3 条核心动效的量化语法）
4. 跳过 §11
5. 在文件头标注 `## ⚠️ Fast-path delivery — 缺少完整动效采访和参考溯源`

CLI 的三个硬限制（始终记住）：
- 没有主语言（§0 空）→ 做出来的网站像"XX 风格的皮肤"，没有自己叙事
- 没有动效（§10 空）→ 静态像，动起来像 PPT
- 没有反向追溯（§11 空）→ 只能照搬不能灵活迁移

## 项目类型裁剪

| 项目类型 | 写哪几段 | 大约行数 | 说明 |
|---------|---------|---------|------|
| **小项目 / 原型** | §0 + §2 + §3 + §9 | ~80 行 | 剩下让 Agent 自由发挥 |
| **工具型 / 应用型** | §0 + §2 + §3 + §4(重) + §5 + §8(压缩) + §9 + §12 + §13 | ~250 行 | §4 最重，§10/§14 近空（工具型跳过动效帧序列），§8 桌面优先 |
| **单页 landing** | §0 + §1 + §4 + §9 + §10 + §12 + §13 + §14 | ~350 行 | §10/§14 是关键，展示型动效决定品质 |
| **完整品牌站** | 全 15 段 | 400-600 行 | 标准流程 |

## 完成标准

初稿（Round 1-3，§0-§11）：

- [ ] 三份文件都已写入 `knowledge/design-docs/`
- [ ] DESIGN.md 的 §0 主语言是动词句式（不是"高级""极客"这类形容词）
- [ ] DESIGN.md 的 §9 Agent Prompt Guide 有至少 5 条 Example Component Prompts
- [ ] DESIGN.md 的 §9 Agent Prompt Guide 可直接复制到生成 prompt 使用
- [ ] MOTION-SPEC.md 每条核心动效有量化语法 `[触发] → [主体] → [变化] → [时序]`
- [ ] MOTION-SPEC.md 每条核心动效标注采访来源
- [ ] 展示型项目核心动效标明双向性约定（禁止 `whileInView` + `once: true`）
- [ ] §11 Interview 记录前轮 + 后轮双轮采访来源
- [ ] 三份文件都有 `status: signal` frontmatter
- [ ] 用户确认主语言和动效约束无歧义

定稿（Round 4，§12-§14 回填，阶段 4 完成后）：

- [ ] §12 Moodboard Prompt 路径就位，locked 版本已选定
- [ ] §13 Page Mockup Prompt 主页 + 所需子页都有文件路径
- [ ] §14 Motion Prompts 核心动效清单表格填满（组件 / 帧序列路径 / 实现 prompt 路径 / 状态）
- [ ] §14 和 §10 分工提示存在（避免 Agent 把宏观清单和微观 prompt 混淆）

## 与其他 skill / 剧本的边界

| 场景 | 走谁 |
|------|------|
| **已定稿项目的二开 / 增量扩展**（反写 §4 / §5 / §9 / §14 增量条目 + 追加 §15 迭代日志） | `frontend-iteration-planner`（场景 C 入口；完成后回本 skill 做增量反写） |
| 产品边界模糊，需要前轮/后轮采访 | `frontend-interview-dualround`（阶段 1 前轮 / 阶段 3 后轮） |
| 还没做六维调研 | `frontend-design-research`（阶段 2） |
| 派生 Moodboard / 示意图 / 帧序列图 | `frontend-visual-reference`（阶段 4） |
| 某个核心动效组件要生成 LoadingScreen 风格的微观实现 prompt | `frontend-motion-prompt-writer`（§14 实现 prompt 的具体内容生成器） |
| 整个项目 knowledge/ 骨架从零搭 | `req-suite:project-spec`（搭到占位后移交本 skill） |
| 已有三份交付文件，要写代码实现 | 开发实现剧本（读本 skill 产出的文件作为约束），同时挂 `frontend-anti-slop-gate` |
| 实现后发现"感觉不对"要评审 | `frontend-design-review`（阶段 7） |
| 只改一个颜色 / 字号 | 直接编辑对应文件 |
| 项目收尾要把开发中调过的动效回灌 | 回到 `frontend-design-research` 跑汇总采访，再回本 skill 更新 §10 / §14 |