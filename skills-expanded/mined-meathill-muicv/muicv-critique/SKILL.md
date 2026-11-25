---
name: muicv-critique
description: 对 `versions/` 下已生成的简历版本做质量评审，从 STAR 完整度、量化比例、关键词对齐、长度、结构等维度给出具体、可操作的改进建议。使用场景：用户说「评审我的简历」「帮我看看这份简历」「这份还能怎么优化」「跟 JD 对照检查一下」「为什么这个简历一般」等。评审不直接改文件，只产出建议清单，由用户决定是否应用。
---

# muicv-critique

对一份已经生成的简历做 **结构化评审**。核心产物是**建议清单**——不擅自改写用户的简历。

## 前置检查

1. 素材库根下 `versions/` 里是否有简历？如果为空 → 提示先调 `muicv-generate`（路径相对素材库根）
2. 用户指定了哪份？
   - 明确指定（文件名或路径）→ 用它
   - 没指定 → 列出最近 3 个 version 让用户选（按 mtime 排序）
3. 该 version 的 frontmatter 里是否有 `target`？有 → 同时 Read 对应 target 做关键词对齐检查
4. 如果同 slug 下还有 `*.resume.json`：**只评 markdown 版本**（JSON 跟 markdown 应该是同一份事实的两种格式）。
   - 评审建议里如果让用户改 bullets / summary / 项目描述，**提醒用户两份都改**——不然 t1~t6 模板渲出来跟 markdown 不一致
   - 评审本身不做 JSON 校验（schema 校验由 `assertTemplateResumeData` 在 render 阶段把关）

## 评审维度

按以下顺序评估，每个维度给出具体问题 + 建议。

> **P0 判定标准的唯一来源是 [docs/p0-rules.md](../../docs/p0-rules.md)**
> （三类 P0：SPEECH / FAB / KW-MISS）。本文件只负责评审输出格式和 P1 / P2 维度。
> 修改 P0 判定规则只改 docs/p0-rules.md，不要改这里。
>
> muicv-generate 在写文件前已经跑过一轮 P0 自检（self_check: passed / partial）。
> critique 的角色：
> - `self_check: passed` 的版本：仍要复审（generate 自己评自己有 bias），重点在 P1 / P2
> - `self_check: partial` 的版本：generate 已经把无法自动修正的 P0 写在交付摘要里，
>   critique 要确认这些条目并给出具体补素材建议

### 1. 事实完整度 / 空话检测（P0 → SPEECH）

判定标准见 [docs/p0-rules.md 的 SPEECH 章节](../../docs/p0-rules.md#1-空话speech)。
扫每条 highlight：

- 空心动词开头（「负责」、「参与」、「协助」、「帮忙」、「支持」、「配合」）且无具体动作和结果 → P0
- 纯形容词描述（"一个关键的项目"、"重要的系统"）→ P0
- "做了 X"但没说结果的 → P1（不算硬伤，但提醒用户看有没有可补充的）

修正建议直接套 [docs/p0-rules.md](../../docs/p0-rules.md) 的"修正动作"小节里的实动词替换表。

### 2. 量化比例（P1 + 编造检测 P0 → FAB）

> **「量化」= Action 之后产出的 outcome 指标**（成果/效率/收益变化），不是 scope/编制/时长/件数。
> ✅ 转化率 +12% · 退货率 8%→3% · P75 800ms→320ms · GMV ¥80k→¥260k · 排名 #1（绑结果）
> ❌ "覆盖 3 个站点" · "带 4 人团队" · "维护 30+ 仓库" · "做了 3 年"——这些是 scope，写进 Action，**不要单独标"量化"**
> 素材里没有 outcome 数字时，保留定性描述，**不要为了凑量化而编数字、也不要把 scope 升格成量化**。
> 完整定义见 [docs/quantification-guideline.md](../../docs/quantification-guideline.md)。

**P1 部分**——量化比例统计：

- 统计**仅 outcome 类数字**的 highlight 比例：% / 倍数 / 前后对比 / 收益金额变化 / 排名（绑结果时）。
  **显式排除**：单纯计数（站点数、团队人数、产品数、仓库数、篇数）、时长（年/月）、技术广度（用了 N 种语言）。
- 参考线：至少 30% 的 highlight 带 outcome 数字；低于 20% 则明显偏弱
- **不要擅自建议用户加上"30%""50%"这类数字**。只能提醒"这一条可以考虑补一个 outcome 量化指标，如果你手头有数据"

**P0 部分**——编造检测（FAB），判定标准见 [docs/p0-rules.md 的 FAB 章节](../../docs/p0-rules.md#2-编造fab)：

- 简历里的数字逐个回 `source_files` 比对，对不上 → P0
- 把 scope 数字升格成 outcome 量化（"3 个站点"→"提速 3 倍"）→ P0
- 能力声称、职责描述跟素材不符 → P0
- 修正动作直接套 docs/p0-rules.md 的"修正动作"小节

### 3. STAR 结构

检查每条 highlight 是否有：
- Situation / Task（情境/任务）：为什么做
- Action（动作）：做了什么
- Result（结果）：产生什么影响

常见问题：
- 只有 Action，缺 Result
- 只有 Result，读者不知道做了什么
- S/T 描述过长，Action 被埋没

### 4. 关键词对齐（有 target 时）（P0 → KW-MISS + P1）

判定标准见 [docs/p0-rules.md 的 KW-MISS 章节](../../docs/p0-rules.md#3-关键词重缺失kw-miss)。

- 从 target 的 JD 正文抽关键词（按频次和位置；核心关键词 = 标题 + Requirements 前 3 项 + 出现 ≥ 2 次的）
- 对比简历正文，列出：
  - **覆盖的**关键词（好的，允许同义命中：Golang ↔ Go、性能优化 ↔ 提速）
  - **JD 核心关键词但简历没有** → **P0**（KW-MISS）。先确认是不是被 generate 裁掉了；
    确实素材里没有 → 建议"考虑向 muicv-core 补充相关素材"或评估岗位匹配度
  - **JD 非核心关键词但简历没有** → P1（建议补充但非硬伤）
  - **简历有但 JD 不要**的关键词 → P2（建议降权或移除，非硬性）
- 注意：**JD 有但素材没有 ≠ 应该编造**。如果素材里确实没有，建议是"考虑向 muicv-core
  补充相关素材"而不是"在简历里补上"。如果 generate 已经写了 `missing_keywords`，
  在评审报告里复述并强调"未编造，符合规则"

### 5. 长度与密度

- 总长度估计（按字数 / 预估页数）
- 目标：1 页（少于 5 年经验）或 2 页（5 年以上）
- 每段 experience 的 highlight 数量（2~4 合理，>5 冗长，<2 薄弱）
- Summary 长度（2~4 句合理）

### 6. 排序与结构

- 相关度最高的经历是否在前？（跟 target 比对）
- 时间顺序是否清晰（倒序）？
- Education、Skills 位置是否合理（资深 = 后置；应届 = 前置）

### 7. 表达质量

- 动词是否主动、具体
- 是否有套话（"认真负责、团队合作、沟通能力强" 这类）
- 术语一致性（同一个技术栈不要一会叫 "Next.js" 一会叫 "nextjs"）
- 拼写 / 格式

## 输出格式

**必须用 `write_file` 工具**写到 `critiques/<version-name>-<YYYY-MM-DD>.md`
（相对素材库根，公约见 prelude）。`<version-name>` 取被评审 version 文件的
basename 不含扩展，例如评审 `versions/google-l5-2026-04-24.md` → 写到
`critiques/google-l5-2026-04-24-2026-04-28.md`。

**不要在对话里粘整份评审报告**——只在对话里给一句结论 + 路径，详情让用户去
右栏预览。

文件内容用这个结构：

```markdown
---
type: critique
version: versions/<file>.md
target: targets/<file>.md   # 如有
generated_at: <ISO>
---

# 评审报告：versions/<file>.md

**整体评估**：<🟢 良好 / 🟡 可改进 / 🔴 需要重做>（给出一句话理由）

## 维度评分

| 维度 | 评价 | 简评 |
|---|---|---|
| 事实完整度 | 🟢/🟡/🔴 | … |
| 量化比例 | 🟢/🟡/🔴 | X 条里 Y 条带数字 |
| STAR 结构 | 🟢/🟡/🔴 | … |
| 关键词对齐 | 🟢/🟡/🔴 | JD 要 A/B/C，简历覆盖 A；B 缺，C 有 |
| 长度密度 | 🟢/🟡/🔴 | 总长 ~ N 字，预估 ~ X 页 |
| 排序结构 | 🟢/🟡/🔴 | … |
| 表达质量 | 🟢/🟡/🔴 | … |

## 具体问题（按优先级）

### P0（影响录用决策）

1. **<问题简述>**  
   位置：`## 工作经历 > ACME Corp > 第 2 条`  
   现状："负责前端开发工作"  
   建议：这是典型的空话 highlight。考虑改成具体的动作 + 结果，比如你素材里写的 "主导 dashboard 重构"（见 `experience/acme-2023.md`）就更有力。

### P1（明显可改进）

…

### P2（润色）

…

## 可能需要补素材

如果以下内容在素材里找不到但对这个 JD 很重要，考虑用 `muicv-core` 补充：

- <关键词> — JD 里出现 N 次，素材里未找到
- …

## 下一步

- 如需我按上述建议修改简历，告诉我 "按 P0 改" 或具体说"改第 N 条"
- 如需重新生成整份，调 `muicv-generate`
- 如需补素材，切到 `muicv-core` 的 add-experience / add-project / update
```

## 严守边界

- **不直接改文件**。评审就是评审。用户明确说"按这个改"再动手。
- **不编造数字或事实**来让简历看起来更好。缺就是缺，诚实报告。
- **不做风格之争**。评审基于 STAR、量化、关键词对齐这些可操作维度，不要因为个人偏好说用户"语气太平"之类。
- **不扩大战场**。评审只看 version 文件和对应 target；除非用户要求，不去翻用户所有素材挑毛病。

## 反例

- ❌ 看到"负责前端开发"，直接改成"主导前端架构设计，提升开发效率 40%"（空话变编造）
- ❌ 先自己 Edit 简历，再告诉用户"我改好了"（越界了）
- ❌ 评论"你这份经历太单薄"（主观判断，没有基于维度）
- ❌ 把所有能提的都列出来，用户看一百条不知道改哪个（没分优先级）

## 与其他 skill 的协作

- **muicv-core**：评审发现素材不足时，指引用户用 muicv-core 补素材，然后重新 generate
- **muicv-generate**：评审后如果要大改，建议重新 generate（因为 generate 里的相关度裁剪逻辑也会受新素材影响）
- **muicv-render**：评审完毕、用户满意后再 render 成 PDF
