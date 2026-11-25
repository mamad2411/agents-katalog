---
name: frontend-design-research
description: 阶段 2 试吃——对 4-5 个该领域设计优秀的真实网站跑六维机械拆解（形 / 色 / 字 / 构 / 质 / 动），综合成本项目 design.md 初稿。六维是上位骨架，DOM 量化工作流 + 动效采访 5 类是落地肌肉。每次一站，保护上下文。不做前轮/后轮深度采访（那是 frontend-interview-dualround）、不做视觉锚定三件套（那是 frontend-visual-reference）、不写最终交付的 design.md（那是 frontend-design-writer）、不做组件库 / 动效资产库选型（那部分由 frontend-design-writer 的 §11 Resources 段 + 项目级 components.json 决定）。触发：新项目六维调研、整站重做、前端方向大迭代。
---

<!-- PACKAGED_KNOWLEDGE_START -->
## Packaged Knowledge Snapshot

This packaged copy includes local note snapshots for portability.
When the original Obsidian absolute path is unavailable, use the packaged snapshot instead:

- `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/AI前端设计认知框架.md` -> `references/packaged-knowledge/AI前端设计认知框架.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/主语言是设计的第一原则.md` -> `references/packaged-knowledge/主语言是设计的第一原则.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/六维：形色字构质动是网站试吃的机械骨架.md` -> `references/packaged-knowledge/六维：形色字构质动是网站试吃的机械骨架.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/AI 前端动效盲区与采访补偿.md` -> `references/packaged-knowledge/AI 前端动效盲区与采访补偿.md`
- `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/从参考案例复刻高级感：量化工作流.md` -> `references/packaged-knowledge/从参考案例复刻高级感：量化工作流.md`
<!-- PACKAGED_KNOWLEDGE_END -->

# Frontend Design Research

## 这个 skill 在做什么

**阶段 2 试吃**的纯化执行器。输入是已锁定的主语言 + 初步目标，输出是本项目的 `design.md` 初稿（可能还包含参考站六维记录）。

核心方法论是**六维机械骨架**——AI 试吃参考站时常见失败是"偷懒只抄色板"或"感觉驱动说不清楚哪里好"，六维（形 / 色 / 字 / 构 / 质 / 动）把感觉机械化成可量化的正交维度，避免靠"感觉"收敛。

## 在阶段化流程里的位置

本 skill **严格限定在阶段 2**（见 [[AI前端设计认知框架]]）：

```
阶段1 需求 + 前轮深度采访 ─→ 主语言 + 目标（← 前提）
         ↓
阶段2 试吃六维 × 4-5 站    ─→ design.md 初稿（← 本 skill 产出）
         ↓
阶段3 后轮深度采访         ─→ design.md 定稿
         ↓
阶段4 视觉锚定三件套
```

和老版的差异：老版 research 包含"主语言收敛 + 参考调研 + 动效采访 + 资源路由"四件事；2026-04-21 重构后：

- **主语言收敛**：由 `frontend-interview-dualround` 前轮产出，本 skill 只做**验证**（主语言必须已经是动词句式）
- **参考调研**：重组为**六维骨架** × 4-5 站，**一次一站**保护上下文
- **动效采访**：归到**六维之动**，作为六维之一，不再是独立步骤
- **资源路由**：**拆出**——组件库 / 动效资产库选型由 `frontend-design-writer` 写入 §11 Resources 段

## 何时进入本 skill

**要进**：
- 阶段 1 完成（主语言 + 目标已定），需要跑参考站调研
- 整个站点/单个关键页面重做
- 前端方向大迭代（主语言不变但视觉气质换）
- 用户说"帮我找几个参考学习"/"跑一下前端调研"/"做六维试吃"

**不要进**：
- 主语言还没定 → `frontend-interview-dualround` 前轮先拔出来
- 六维都调研完了要定稿 → `frontend-interview-dualround` 后轮
- 要派生 Moodboard / 示意图 / 动效帧序列 → `frontend-visual-reference`（阶段 4）
- 要写交付版 design.md kun 15 段 → `frontend-design-writer`
- 要生成某个动效的微观实现 prompt → `frontend-motion-prompt-writer`
- 纯后端/纯脚本/无 UI 任务

## 知识库依赖

本 skill 只是剧本，方法论住在笔记里，不复制。

| 文件 | 用途 | 何时读 |
|------|------|--------|
| `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/六维：形色字构质动是网站试吃的机械骨架.md` | 六维定义 + 每维量化手段 + 现有 checklist 挂接 | **启动必读** |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/AI前端设计认知框架.md` | 阶段化流程总图（本 skill 在阶段 2 的位置） | 启动时扫阶段 2 段 |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/01-认知框架/主语言是设计的第一原则.md` | 主语言的 5 问验证法（本 skill 只验证不收敛） | 用户说不清主语言时读 |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/从参考案例复刻高级感：量化工作流.md` | DOM 量化测量法（六维之形/色/字/构/质 的落地） | 步骤 2 跑每站时读 |
| `/Users/kunkun/note/01-AI工程/AI设计与前端/02-执行方法/AI 前端动效盲区与采访补偿.md` | 动效采访 5 类（六维之动 的落地） | 步骤 2 跑到"动"维时读 |

启动时拉前两份，其他按触发条件读。

## 执行顺序

```
0. 判型 → 1. 验证主语言 → 2. 六维试吃 × 4-5 站（一次一站）→ 3. 综合成 design.md 初稿
```

每站跑一次六维，**不一次性吃完 4-5 站**——上下文会挤垮。

---

## 步骤 0：判型

先问用户（或从上下文推断）：**这是展示型还是工具型？**

| 类型 | 代表 | 六维侧重 |
|---|---|---|
| **展示型 / 品牌型** | landing page、官网、营销页、作品集 | **六维全跑**，动维最重（展示型命根子） |
| **工具型 / 应用型** | dashboard、agent 产品、工作台、管理台 | 构 + 字最重，动维可近空（轻交互反馈够用） |

混合情况（"内部工具但想做得漂亮"）：倾向工具型主干 + 借鉴展示型某一两维（常见是"形"或"质"）。

---

## 步骤 1：验证主语言（不收敛）

本 skill **不收敛主语言**——那是 `frontend-interview-dualround` 前轮的职责。本 skill 只做**入参验证**：

| 检查 | 通过条件 |
|---|---|
| 主语言存在 | `knowledge/design-docs/design.md` §0 或等价位置已经有一句话叙事 |
| 动词句式 | "滚动时混沌收敛为有序" ✓；"高级极客感" ✗（回 dualround） |
| 5 问有答 | 主语言笔记的 5 个验证问题都能回答 |

**硬规则**：答不出来或还是形容词 → 路由到 `frontend-interview-dualround`，不要自己往下走。

---

## 步骤 2：六维试吃 × 4-5 站

本 skill 的核心步骤。**一次一站**，每站跑一次六维。

### 2.1 找 URL（用户主场）

写一个搜索提示词（产品类型 + 目标用户 + 期望气质 + 主语言），让用户用 **Grok / Manus / Perplexity** 跑一轮交回 URL 清单。Claude 的 web search 触达不了 Twitter/Reddit/设计社区的口碑层——这一步**必须用户出手**。

### 2.2 每站跑六维（机械骨架）

对每个参考站独立跑一次六维拆解：

| 维 | 落地手段 | 产出 |
|---|---|---|
| **形** | 图标族盘点 + SVG 路径采样 + `border-radius` token 表 | 一张标注图 + radius 表 |
| **色** | DOM 量化（`getComputedStyle`）+ Coolors 对比 + token 导出 | color token 表 + 明暗饱和度分布 |
| **字** | DOM 量化（字号 / 行高 / 字距 / 字重） | type scale 表 + 字体族 |
| **构** | 截图栅格标注 + DOM 量化（spacing / grid / 宽度） | 栅格截图 + spacing token 表 |
| **质** | 背景层采样 + noise 密度 + 阴影量化 + 渐变采样 | material 表（噪点 / 光泽 / 渐变 / 阴影） |
| **动** | [[AI 前端动效盲区与采访补偿]] 5 类采访（节奏 / 触发 / 双向性 / 层级 / 反例） | 量化语法清单 + 双向性约定 |

### 2.3 六维落地的核心机械动作

#### DOM 量化硬步骤（形 / 色 / 字 / 构 / 质）

真实浏览器打开 + `getComputedStyle` + `getBoundingClientRect` 逐元素测量。

| 测量项 | 记录 |
|---|---|
| 字号 / 行高 / 字重 | 关键层级各一组 |
| 容器宽度 / 最大宽度 / 内外边距 | 主栅格 + 内容容器 |
| 颜色（主色/背景/文字/边框） | HSL 或 Hex |
| 动画 duration / easing | DevTools Animations 面板或读 transition CSS |

浏览器工具陷阱（Lenis 劫持 scrollTo、chrome-in-claude 截图 bug）见 [[从参考案例复刻高级感：量化工作流]]，遇到问题时读。

#### 动效采访 5 类（动）

让用户亲自在每个主参考站滚动 + hover + 点击，Claude 在旁边问：

| 类别 | 问什么 |
|---|---|
| **节奏类** | duration 感觉多少秒？快还是慢？easing 像弹簧还是缓冲？stagger 有没有？多大间隔？ |
| **触发类** | 在 scroll 哪个位置触发？hover 瞬间触发还是延迟？点击后多久响应？ |
| **双向性类** | 滚回去会逆放吗？还是保留在末态？ |
| **层级类** | 多个动效共存时谁压谁？主动效哪个？装饰动效哪个？ |
| **反例类** | 什么是你不想要的？哪种动效是"俗套" / "AI 味"？ |

**量化语法**（每条一行）：

```
[触发条件] → [主体] → [变化] → [时序/范围]
```

示例：
```
scroll 进入视口 100px → hero 标题 → 从 y=60 opacity=0 到 y=0 opacity=1 → 0.8s ease-out 双向连续
hover 卡片 → 卡片阴影 → 从 shadow-sm 到 shadow-xl → 0.2s ease-out 单向
```

#### 硬约束

- **展示型核心动效默认双向连续**：跟随 scrollY 位置实时变化，**禁止** `whileInView` + `once: true` 用于核心动效
- 所有动效必须有明确 duration + easing
- 每条动效标明来源（哪个参考站的哪个交互）

### 2.4 每站记录三类标签

调研结果每站按三类打标：

- **直接借鉴**：整体方向可以参考，列出要借鉴的具体元素（对应哪一维）
- **局部学习**：某个具体做法值得提取（单维单点借鉴）
- **反面参考（anti-references）**：明确要避开的模式 + 为什么

### 2.5 数量约束

- **默认 4-5 站**：少于 4 难以识别品类共性，多于 5 上下文不够
- **每站记录到 `knowledge/design-docs/research/{site}-sixdim.md`**（可选）或直接综合到 design.md 初稿
- 不跨站对比——横向对比留到步骤 3 综合

### 2.6 常见误区

- ==不要把六维当权重评分表==：不是给每站打 6 维分数选最高的，六维是**观察维度**不是评价维度
- ==不要每维都穷尽==：每维记录"和本项目主语言最相关的部分"即可
- ==不要跳过"质"这一维==：质是最容易被忽略也最容易出 AI 味的维（默认渲染扁平、无材质）

---

## 步骤 3：综合成 design.md 初稿

把 4-5 站的六维记录综合成**一份**本项目的 `design.md` 初稿（不是每站一份）。这步不是简单拼贴，要按本项目主语言筛选。

### 3.1 筛选原则

每维记录"**最支持本项目主语言**的条目"：
- 主语言是"克制 + 叙事推进"？→ 形维选几何圆角 + 直线分割线
- 主语言是"激进 + 锋利"？→ 形维选尖角 + zero radius

### 3.2 落盘位置

初稿写到 `knowledge/design-docs/design.md`（不是交付版，是待后轮采访定稿的版本）：

```yaml
---
status: signal
last_updated: YYYY-MM-DD
source: frontend-design-research skill
stage: 2-initial-draft
---
```

初稿段落（对应 kun 15 段的前 9 段子集）：
- §0 Main Language（从前轮采访复制）
- §1 Visual Theme & Atmosphere（六维综合的一段话描述）
- §2 Colors（色维量化）
- §3 Typography（字维量化）
- §4 Components（形 + 字 + 质 综合）
- §5 Layout（构维量化）
- §6 Depth（质维量化）
- §10 Motion Spec（动维量化）

§7/§8/§9/§11 留到 `frontend-design-writer` 的 Round 3 组装；§12-§14 留到阶段 4 完成后回填。

---

## 完成标准

- [ ] 步骤 0 判型完成，记录展示型/工具型
- [ ] 步骤 1 主语言验证通过（动词句式 + 5 问有答）
- [ ] 跑完至少 4 个参考站的六维（工具型可降到 3 站）
- [ ] 每站六维都有量化数据（不是"感觉像……"）
- [ ] 至少 1 个反面参考（anti-reference）且说明原因
- [ ] 动维采访五类都被问过（节奏/触发/双向性/层级/反例），至少 3 条量化语法
- [ ] 展示型项目核心动效标明双向性约定
- [ ] `knowledge/design-docs/design.md` 初稿落盘，含 §0-§6 + §10，frontmatter 含 `status: signal`
- [ ] 已告知用户下一步是 `frontend-interview-dualround` 后轮采访

## 与其他 skill / 剧本的边界

| 场景 | 走谁 |
|------|------|
| **已定稿项目的二开 / 增量扩展**（design.md 定稿 + 加新页面 / section / 微改） | `frontend-iteration-planner`（场景 C 入口路由器） |
| 前轮 / 后轮深度采访（产品设计师视角） | `frontend-interview-dualround` |
| 派生 Moodboard / 完整网页示意图 / 动效帧序列 | `frontend-visual-reference`（阶段 4） |
| 把初稿写成交付版 kun 15 段 | `frontend-design-writer` |
| 某个核心动效的微观实现 prompt（LoadingScreen 风格） | `frontend-motion-prompt-writer` |
| 整个项目 knowledge/ 骨架从零搭 | `req-suite:project-spec` |
| 已定稿项目改按钮颜色、调文案、修 bug | 开发实现剧本 |
| 用户看实现说"感觉不对" | `frontend-design-review`（阶段 7） |
| 反 slop 硬禁令扫描 | `frontend-anti-slop-gate`（阶段 6 横切） |
| 组件库 / 动效资产库选型（shadcn / Lottie / Rive / Spline） | 由 `frontend-design-writer` §11 Resources 段记录；实际 MCP 分发走项目级 `components.json` 与 mcp-bootstrapper |
| 项目收尾把开发中调过的动效回灌 | 本 skill 跑动维汇总采访，再回 writer 更新 §10 / §14 |

## 本 skill 的 deletion-spec

- **触发删除条件**：当 AI 试吃参考站默认就能稳定覆盖六维（不偷懒只抄色板、不忽略材质和动效），或六维骨架被证伪 / 扩缩维度（比如拆成 7 维 / 合并成 5 维），本 skill 需要重写。
- **禁用方式**：从 `plugins/frontend-suite/skills/` 删除本目录即自动停止发现；marketplace 刷新后生效。
- **卸载清单**：
  - 同步检查 `~/.agents/agent_prompt_core/shared/playbooks/前端设计_剧本.md` 阶段 2 路由
  - 同步检查 [[AI前端设计认知框架]] 阶段 2 段 + [[六维：形色字构质动是网站试吃的机械骨架]] "对应 skill" 引用
  - 同步检查 `frontend-design-writer` / `frontend-interview-dualround` / `frontend-visual-reference` 的"边界表"
  - 资源路由章节已迁到 writer §11，迁出时需同步写 writer 的 deletion-spec