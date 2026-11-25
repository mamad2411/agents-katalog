---
name: frontend-anti-slop-gate
description: 前端代码生成前或评审时的反 slop 硬门禁。扫十条作者硬判断的视觉红线——Inter 字体、紫/蓝 AI 渐变（Lila Ban）、3 列等宽卡片、纯黑 #000、Lucide 默认图标、h-screen 全屏、通用占位数据（John Doe、99.99%）、AI 文案词（Elevate、Seamless、Unleash）、window.addEventListener('scroll')、圆形 spinner——给出违规项和具体修正参数。无状态门禁（不读取项目 knowledge/），和主语言软约束正交互补。触发信号：写前端代码前、review 代码时、看到"生成的页面像 AI 做的"、前端剧本显式路由。
---

<!-- PACKAGED_KNOWLEDGE_START -->
## Packaged Knowledge Snapshot

This packaged copy includes local note snapshots for portability.
When the original Obsidian absolute path is unavailable, use the packaged snapshot instead:

- `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/AI前端设计认知框架.md` -> `references/packaged-knowledge/AI前端设计认知框架.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/反 slop 硬禁令：AI 前端的十条视觉红线.md` -> `references/packaged-knowledge/反 slop 硬禁令：AI 前端的十条视觉红线.md`
<!-- PACKAGED_KNOWLEDGE_END -->

# Frontend Anti-Slop Gate

## 这个 skill 在做什么

把作者对"AI 默认输出视觉 slop"的反向观察编码成十条机械可扫的硬禁令，在生成或评审代码时强制过一遍，防止主语言再强也被 AI 默认倾向拉回俗套。

本 skill 是**无状态门禁**——不读项目 knowledge/、不看主语言、不知道项目叫什么。它只做一件事：代码片段在 → 违规清单 + 修正项出。

核心认知：约束先于生成的原则里有两种约束——**作者硬判断**（每个项目都触发的不变量）和**项目软诉求**（主语言驱动的变量）。本 skill 管前者，[`frontend-design-research`](../frontend-design-research/) / [`frontend-design-writer`](../frontend-design-writer/) 管后者。

在阶段化流程（见 [[AI前端设计认知框架]]）里，本 skill 位于**阶段 6 代码实现的横切**——每次 Agent 准备落代码时强制过一遍，和"完整性验收"并列为阶段 6 的两条常驻横切。

## 何时进入本 skill

**要进**：
- Agent 写前端代码前先过一遍（常驻式）
- 用户说"看起来像 AI 做的" / "没什么差异化" / "感觉很模板"
- 评审代码时显式调用："走一遍 anti-slop 检查"
- 前端设计剧本路由到本 skill
- 生成的代码里出现 `Inter` / `purple-` / `3 equal columns` / `Lucide` / `h-screen` / `#000` / 任一硬禁令信号词

**不要进**：
- 用户的主语言明确要求某条禁令（如项目本身就是 Brutalist 要求纯黑）——优先走项目软约束，本门禁的该条 skip 并记录豁免
- 还没有代码片段（只有文字讨论设计方向）

## 知识库依赖

| 文件 | 用途 | 何时读 |
|---|---|---|
| `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/反 slop 硬禁令：AI 前端的十条视觉红线.md` | 十条红线完整版 + 每条的 rationale + 替代方案 | **启动必读** |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/AI前端设计认知框架.md` | 阶段化流程里本 skill 的横切位置、约束二元性（硬判断 vs 软诉求） | 有歧义时回查 |

## 十条硬禁令（扫描清单）

### 排版层
1. **Inter 字体（高级语境）** → 替代：Geist、Outfit、Cabinet Grotesk、Satoshi、Switzer
2. **通用衬线字体（Times / Georgia / Garamond）** → 替代：Fraunces、Instrument Serif、Newsreader；仪表盘**禁衬线**

### 色彩层
3. **紫/蓝 AI 渐变（Lila Ban）**：`purple-600`、`indigo-500`、`from-purple-to-blue` → 替代：Zinc/Slate + 单一高对比重音（Emerald / Electric Blue / Deep Rose），饱和度 < 80%
4. **纯黑 `#000000`** → 替代：`#0a0a0a` / `#121212` / Zinc-950 / 炭灰 / 深海军蓝

### 布局层
5. **3 列等宽卡片特征行** → 替代：2 列 Zig-Zag / 非对称 Grid (`2fr 1fr 1fr`) / 水平滚动 / 砌体
6. **居中对称 Hero（variance > 4 时）** → 替代：Split Screen / 左对齐文本+右资产 / 非对称留白
7. **`h-screen`** → 改为 `min-h-[100dvh]`（iOS Safari 地址栏跳跃）

### 资源层
8. **Lucide / Feather 默认图标独占** → 替代：Phosphor (Bold/Fill) / Heroicons / Radix UI Icons / 自定义集；描边宽度一致
9. **通用占位数据**：
   - 人名 John Doe / Jane Smith → 多样逼真名字
   - 数字 99.99% / 50% / $100.00 → 有机数据（47.2%、$99.00、+1 (312) 847-1928）
   - 公司 Acme / Nexus / SmartFlow → 发明可信品牌名
   - AI 文案词 Elevate / Seamless / Unleash / Next-Gen / Delve / Tapestry / "In the world of..." → 具体动词

### 代码层
10. **`window.addEventListener('scroll')` + `useState` 连续动画** → 替代：
    - 滚动 → `IntersectionObserver` 或 Framer Motion `whileInView`
    - 连续动画 → `useMotionValue` + `useTransform`
    - 动画仅限 `transform` 和 `opacity`，禁 `top` / `left` / `width` / `height`

## 次级禁令（可选启用）

- 圆形 loading spinner → 骨骼屏匹配布局
- 霓虹外部发光 → 精妙内阴影或微妙 `box-shadow`
- 自定义鼠标光标 → 系统默认
- 标签 `SECTION 01` / `QUESTION 05` / `ABOUT US` → 移除或替代
- "Scroll to explore" / 滚动箭头 / 弹跳 v 形 → 内容自然吸引

## 使用方式

### 模式 A：生成前（Agent 主动）
写代码前先自检：主语言是否明确豁免某条？不豁免的十条一条一条过，确保输出不撞 AI 默认。

### 模式 B：评审时（用户触发）
用户说"走一遍 anti-slop"：逐条扫代码 → 列违规项 → 给每项具体修正参数。

### 模式 C：剧本路由
前端设计剧本阶段 6 代码实现期间常驻调用；同时挂在阶段 4 视觉锚定三件套的 prompt 生成前（防止反 slop 元素进入图像锚点）。

## 产出格式

```markdown
## Anti-slop 扫描结果 — [日期]

### P0 违规（必改）
- [ ] §1 排版：Hero 用了 `font-inter`，违反禁令 1 → 改为 `font-geist` 或 `font-cabinet-grotesk`
- [ ] §3 色彩：`from-purple-600 to-indigo-500` 渐变，违反 Lila Ban → 改为 Zinc 基础 + Emerald 重音

### 项目豁免（已记录）
- §2 色彩：Brutalist 项目主语言要求纯黑 → 禁令 4 豁免

### 次级建议（可选）
- CTA spinner 是圆形 → 考虑改骨骼屏
```

## 和其他机制的边界

| 场景 | 走谁 |
|---|---|
| **已定稿项目的二开 / 增量扩展** | `frontend-iteration-planner`（场景 C 入口；本 skill 在 T1/T2/T3 的阶段 6 代码环节常驻横切） |
| 阶段 1 前轮需求采访 / 阶段 3 后轮定稿采访 | `frontend-interview-dualround`（产品设计师视角横切） |
| 阶段 2 试吃六维（形色字构质动） | `frontend-design-research` |
| 阶段 4 视觉锚定三件套（Moodboard / 示意图 / 帧序列） | `frontend-visual-reference` |
| 阶段 4C + 6 微观动效 prompt（LoadingScreen 风格） | `frontend-motion-prompt-writer` |
| 阶段 1-7 持续产出 design.md（kun 15 段） | `frontend-design-writer`（可把本 skill 的 10 条作为 §7 Don't 基线） |
| 阶段 7 迭代微调（用户提感觉"不对"） | `frontend-design-review`（三段式追问 + 参数外显 Tweaks） |
| 代码交付完整性（`// TODO` / 占位 / 空实现） | `dev-essentials:verification-before-completion` |

## 抗腐化

硬禁令的风险是随潮流过期。每条禁令的 rationale 必须可追溯到知识库笔记；当某条过期时（如 Inter 再度变好），更新本 skill 要同步更新 `反 slop 硬禁令：AI 前端的十条视觉红线.md`。

## 完成标准

- [ ] 十条全部扫描完毕
- [ ] 每条违规都有具体修正参数（不是"换一个字体"）
- [ ] 项目豁免项单独列出并记录 rationale
- [ ] P0 违规全部修正后通过

## deletion-spec

- **触发删除条件**：当前沿模型默认输出不再撞这十条（比如训练数据分布更新，Inter/紫蓝/3 列等不再是默认倾向）时，本 skill 可降级为提醒或删除。
- **禁用方式**：从 `plugins/frontend-suite/skills/` 删除本目录即自动停止发现；marketplace 刷新后生效。
- **卸载清单**：
  - 同步检查 `~/.agents/agent_prompt_core/shared/playbooks/前端设计_剧本.md` 是否显式引用本 skill
  - 同步检查 [[AI前端设计认知框架]] 笔记的"阶段化流程总表"横切机制段（反 slop 硬禁令行）是否仍指向本 skill
  - 同步检查 [[反 slop 硬禁令：AI 前端的十条视觉红线]] 笔记的"对应 skill"字段
  - 同步检查 frontend-suite 其他 skill（design-research / design-writer / visual-reference / motion-prompt-writer）的"边界表"是否引用本 skill 作为阶段 6 横切