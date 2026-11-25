---
name: frontend-motion-prompt-writer
description: 动效文档微观层生成器——把 MOTION-SPEC.md 宏观清单 + 帧序列图 + 具体组件翻译为 LoadingScreen 风格的代码级实现 prompt（Theme tokens / 字体引用 / 组件签名 / 逐元素规格 / 父组件行为 / 时序总表）。产出喂 Agent 写 framer-motion 代码，一组件一份，住在 knowledge/design-docs/motion-prompts/。按需触发——每到阶段 6 代码实现触达一个核心动效组件时现场生成，不是一次性把所有组件写完。触发：用户说"写 LoadingScreen 的动效 prompt""把 Hero 入场动效翻译成代码规格""生成 motion-prompts/*.md"。不用于宏观 MOTION-SPEC（那是 frontend-design-writer 的 §10）、不用于帧序列图本身（那是 frontend-visual-reference 的阶段 4C）、不用于直接写 framer-motion 代码（那是开发实现剧本）。
---

<!-- PACKAGED_KNOWLEDGE_START -->
## Packaged Knowledge Snapshot

This packaged copy includes local note snapshots for portability.
When the original Obsidian absolute path is unavailable, use the packaged snapshot instead:

- `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/AI 前端动效盲区与采访补偿.md` -> `references/packaged-knowledge/AI 前端动效盲区与采访补偿.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/动效文档两层：MOTION-SPEC vs 实现 prompt 集.md` -> `references/packaged-knowledge/动效文档两层：MOTION-SPEC vs 实现 prompt 集.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/视觉锚定三件套：代价结构与资产生成双路径.md` -> `references/packaged-knowledge/视觉锚定三件套：代价结构与资产生成双路径.md`
<!-- PACKAGED_KNOWLEDGE_END -->

# Frontend Motion Prompt Writer

## 这个 skill 在做什么

把动效从**宏观清单**（人读的量化语法）翻译为**微观代码级规格**（Agent 直接读、写 framer-motion 代码的完整 prompt）。一个核心动效组件一份 prompt，参考 LoadingScreen 范式：Theme tokens / 字体引用 / 组件签名 / 逐元素规格 / 父组件行为 / 时序总表六个要素齐备。

## 动效文档两层的分工

本 skill 负责**微观层**，不碰宏观层：

| 层 | 给谁读 | 产出 skill |
|---|---|---|
| **宏观层（MOTION-SPEC.md / design.md §10）** | 人 + Agent 并读 | `frontend-design-writer`（§10） |
| **微观层（motion-prompts/{Component}.md）** | Agent 直接读 → 写代码 | **本 skill** |

两层互补：宏观层定义"整站动效清单 + 量化语法 + 双向性约定"；微观层是单个组件的**完整代码级实现规格**。单独任一层都不够——只有宏观会生成风格各异的实现，只有微观会在没定组件架构时就锁死细节。

详见 [[动效文档两层：MOTION-SPEC vs 实现 prompt 集]]。

## 在阶段化流程里的位置

本 skill 触达于**阶段 4C 尾部 和 阶段 6 代码实现**：

```
阶段4 视觉锚定三件套
  ├─ A. Moodboard
  ├─ B. 完整网页示意图
  └─ C. 动效帧序列（frontend-visual-reference 产出帧序列图）
         ↓
       ★ 本 skill：把帧序列 + MOTION-SPEC + 组件签名翻译成微观 prompt
         ↓
阶段6 代码实现 ── Agent 读 motion-prompts/{Component}.md 写 framer-motion 代码
```

**按需触发，不是一次性写完**——阶段 4C 结束时可能只写最核心的 1-2 个；阶段 6 代码实现每触达一个新核心动效组件，现场生成一份微观 prompt。

## 何时进入本 skill

**要进**：
- 阶段 4C 帧序列完成，需要把最核心动效（如 LoadingScreen、Hero 入场）翻译为代码规格
- 阶段 6 代码实现，Agent 触达某个核心动效组件，需要完整实现 prompt 引导
- 用户说"写 LoadingScreen 的动效 prompt""把 Hero 入场翻译成代码规格""我要一份能直接喂 framer-motion 的 prompt"

**不要进**：
- 写宏观 MOTION-SPEC.md / design.md §10 → `frontend-design-writer`
- 生成动效帧序列图（视觉锚点） → `frontend-visual-reference`（阶段 4C）
- 动效采访（节奏/触发/双向性/层级/反例 5 类） → `frontend-design-research`（阶段 2 的六维之动）
- 直接写 framer-motion 代码 → 开发实现剧本
- 简单 hover / 按钮 scale / 单 fade 等次要动效 → 不写微观 prompt，只在 §10 登记

## 核心动效组件判定

哪些组件需要微观 prompt？三条标准：

1. **跨元素协调**——多个子元素有时序依赖（如 LoadingScreen 4 元素联动）
2. **非标准动效**——不是简单 fade/translate，涉及 stagger / scroll-linked / gesture
3. **品牌承载**——Hero / 转场 / 标志性交互，直接决定产品气质

次要动效（普通 hover / 按钮 scale / 单 fade）只在 §10 宏观层登记，**不单写本 skill**。

## 知识库依赖

| 文件 | 用途 | 何时读 |
|------|------|--------|
| `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/动效文档两层：MOTION-SPEC vs 实现 prompt 集.md` | 两层分工 + LoadingScreen 范式完整样例 + 六要素定义 | **启动必读** |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/视觉锚定三件套：代价结构与资产生成双路径.md` | 帧序列和微观 prompt 的对应关系 | 第一次写本组件时读 |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/AI 前端动效盲区与采访补偿.md` | 双向性约束（scroll-driven 禁止 whileInView once: true） | 处理 scroll-driven 动效时读 |
| 项目内 `knowledge/design-docs/design.md` §10 | 宏观 motion spec（量化语法 + 双向性 + 核心清单） | **必读为输入** |
| 项目内 `knowledge/design-docs/visual-anchors/motion-frames/` | 对应组件的帧序列图 | 有则对照生成 |

## 执行顺序

```
0. 入参检查 → 1. 提取六要素 → 2. 组装微观 prompt → 3. 落盘 + 更新 §14 索引
```

---

## 步骤 0：入参检查

| 输入 | 是否必须 | 缺失时 |
|---|---|---|
| 宏观 §10 Motion Spec 中该动效的量化语法 | 必须 | 回 `frontend-design-writer` Round 3 补 §10 |
| 帧序列图（visual-anchors/motion-frames/{name}.png） | 推荐 | 可缺，但没视觉锚点 prompt 会虚化 |
| 组件签名（props / TS 类型 / 依赖） | 推荐 | 可缺，本 skill 可建议默认签名 |
| design.md §2 Color + §3 Typography（Theme tokens 来源） | 必须 | 回 `frontend-design-writer` 补 token 段 |
| 动效双向性约定（§10 Global Rules） | 必须 | 回 `frontend-design-research` 动维补采访 |

---

## 步骤 1：提取六要素

对目标动效组件，从入参中提取：

| 要素 | 来源 | 示例 |
|---|---|---|
| **Theme tokens** | design.md §2 Colors | `--bg: #0a0a0a / --text: #f5f5f5 / --muted: #888` |
| **字体引用** | design.md §3 Typography | `font-display: Instrument Serif italic 400（Google Fonts）` |
| **组件签名** | 组件上下文 / 用户输入 | `props: { onComplete: () => void }` |
| **逐元素规格** | 帧序列图 + §10 量化语法 | 每个子元素的 position / class / initial / animate / exit / duration / ease |
| **父组件行为** | §10 Global Rules + 组件上下文 | `isLoading state + AnimatePresence mode="wait"` |
| **时序总表** | §10 量化语法汇总 | 0.0s — 0.9s — 1.8s — 2.7s — 3.1s — 3.7s 全景时间轴 |

**时序总表是关键**——必须让 AI 看到"所有元素合起来的节奏"，不是孤立看单元素。

---

## 步骤 2：组装微观 prompt

参考 LoadingScreen 范式（详见 [[动效文档两层：MOTION-SPEC vs 实现 prompt 集]]）。模板骨架：

```markdown
# {ComponentName} 动效实现 prompt

## Theme Tokens
--bg: {color}
--text: {color}
--muted: {color}
--stroke: {color}

## Fonts
font-display: {font} ({source}, {style}, weight {weight})
font-body: {font} ({source})

## Component 签名
props: { {prop1}: {type}, {prop2}: {type} }

## Container
<motion.div> {position classes} {z-index} {bg}
exit: { {property}: {value} }, duration {seconds}s, ease {bezier}
wrap in <AnimatePresence mode="wait">

## Element 1: {name}
位置：{tailwind classes}
文本：{content}
class：{tailwind classes}
entrance：initial={{ ... }}, animate={{ ... }}
duration {seconds}s, delay {seconds}s

## Element 2: {name}
...

## Element N: {name}
...

## Parent Wrapper Behavior
state: {stateName} starts {initialValue}
render {ComponentName} inside <AnimatePresence mode="wait"> only when {condition}
main content: style={{ opacity: {expr}, transition: {expr} }}

## Timing Summary
0.0s — {event}
0.Ns — {event}
...
N.Ns — {event}（onComplete / exit 触发）
N+0.Ns — {event}（fade out）
N+0.Ns — {event}（main content fades in）

## Anti-slop 约束（从 frontend-anti-slop-gate 快扫）
- 动画仅限 transform + opacity，禁 top/left/width/height
- 禁 window.addEventListener('scroll') —— 用 IntersectionObserver / useMotionValue
- 双向性：{scroll-driven 跟随 scrollY / 单次触发仅装饰}
```

### 反 slop 横切

生成的 prompt 必须**内嵌 anti-slop 检查段**（把 `frontend-anti-slop-gate` 的第 10 条代码层禁令直接写进 prompt），让喂进去的 Agent 不撞 slop。

---

## 步骤 3：落盘 + 更新 §14 索引

### 3.1 落盘路径

```
knowledge/design-docs/motion-prompts/
├── LoadingScreen.md
├── HeroEntry.md
├── ScrollDrivenBackground.md
└── ...（一组件一份）
```

文件命名：PascalCase 的组件名 + `.md`。

### 3.2 更新 design.md §14

调用 `frontend-design-writer`（Round 4）或直接编辑 design.md §14：

```markdown
## 14. Motion Prompts

| 组件 | 帧序列 prompt | 实现 prompt | 状态 |
|---|---|---|---|
| LoadingScreen | motion-frames/loading.md | motion-prompts/LoadingScreen.md | locked |
| Hero 入场 | motion-frames/hero-entry.md | motion-prompts/HeroEntry.md | draft |
```

---

## 完成标准

- [ ] 六要素全部覆盖（Theme tokens / 字体 / 签名 / 逐元素规格 / 父行为 / 时序总表）
- [ ] 逐元素规格对应帧序列图的每一帧（若有帧序列）
- [ ] 时序总表给出从 0.0s 到结束的完整时间轴
- [ ] 双向性约束显式写出（scroll-driven 类必须声明）
- [ ] Anti-slop 约束内嵌
- [ ] prompt 文件落盘到 `knowledge/design-docs/motion-prompts/{Component}.md`
- [ ] design.md §14 索引表更新（组件名 / 帧序列路径 / 实现 prompt 路径 / 状态）

## 和其他 skill / 剧本的边界

| 场景 | 走谁 |
|---|---|
| **已定稿项目的二开 / 增量扩展** | `frontend-iteration-planner`（场景 C 入口；T1/T2 若引新核心动效会调用本 skill，T3 改动效参数只改现有条目） |
| 写宏观 MOTION-SPEC / §10 清单 | `frontend-design-writer` Round 3 |
| 生成动效帧序列图（视觉锚点） | `frontend-visual-reference`（阶段 4C） |
| 动效采访（5 类问题） | `frontend-design-research` 动维 |
| 用微观 prompt 真正写 framer-motion 代码 | 开发实现剧本 |
| 简单 hover / fade 等次要动效 | 不进本 skill，只在 §10 登记 |
| 代码后用户说"动效不对" | `frontend-design-review` + 回本 skill 重写 prompt |
| 反 slop 扫描 | `frontend-anti-slop-gate`（横切，本 skill 生成的 prompt 内嵌该段） |

## 本 skill 的 deletion-spec

- **触发删除条件**：当多模态模型能从帧序列图直接出代码规格（不需要中间文字 prompt 层），本 skill 可降级。或者 framer-motion 被新动效库取代，范式不再是 LoadingScreen 结构，本 skill 的模板需重写。当 AI 写动效代码已能从宏观 §10 + 帧序列图一步到位不需要微观 prompt 时，本 skill 退场。
- **禁用方式**：从 `plugins/frontend-suite/skills/` 删除本目录即自动停止发现。
- **卸载清单**：
  - `frontend-design-writer` §14 段引用本 skill 产出路径，需同步清理
  - `frontend-visual-reference` 阶段 4C 段的"代码级 prompt 走本 skill"描述需回退
  - `plugins/frontend-suite/.claude-plugin/plugin.json` description 需回退
  - [[动效文档两层：MOTION-SPEC vs 实现 prompt 集]] 笔记"对应 skill"字段需同步
  - 项目内 `knowledge/design-docs/motion-prompts/` 目录由用户自行决定保留或迁移