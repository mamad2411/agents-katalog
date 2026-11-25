---
name: report-framework-builder
description: 汇报框架构建器——输入汇报背景、听众、素材、时长，自动匹配最合适的方法论（金字塔原理/SCQA/BLUF/AAR/6-Pager/Nancy Duarte 等 20+ 方法论），输出结构化的逻辑框架和初版汇报内容。触发词：汇报框架、汇报梳理、汇报结构、方法论汇报、结构化汇报、金字塔原理汇报、SCQA、准备汇报、给老板汇报、述职、复盘汇报、周报框架、业绩汇报、项目提案、准备演讲、report framework、structured reporting。
version: 1.0.0
alwaysApply: false
---

# Report Framework Builder — 汇报框架构建器

> 输入零散想法和素材，输出老板一看就懂的**结构化汇报框架 + 初版内容**。
> 支持 20+ 汇报方法论（金字塔/SCQA/BLUF/AAR/6-Pager/Nancy Duarte 等）自动匹配。

---

## 一、启动对话（首次触发时的第一句话）

> "我来帮你把这次汇报梳理清楚。请告诉我 4 件事，我就能匹配最合适的方法论：
> 1. **场景**：你要汇报什么？（新方案 / 进展 / 复盘 / 业绩 / 请示 / 述职 / 危机 ...）
> 2. **听众**：给谁看？（CEO / VP / 平级 / 客户 / 团队 ...）
> 3. **时长/形态**：口头 3 分钟？书面 6 页？PPT 15 张？邮件？
> 4. **素材**：把你手头的信息、数据、想法一股脑发给我（哪怕零散）。
>
> **可选**：如果你老板指定了方法论（如"用金字塔"）或有偏好（数据型/战略型），也告诉我。"

**如果用户已经在初次消息里给了信息**，跳过启动对话，直接进入 Phase 1。

---

## 二、工作流（5 个 Phase）

### Phase 1: 场景识别（Discovery）

从用户输入中提取以下要素。**缺失关键要素时，最多问一次补齐，不要反复问**：

**必需要素**（Required）：
- `scenario`：汇报场景（对应 references/scenarios.md 的 S1-S12）
- `audience`：听众类型
- `goal`：汇报目的（说服/请示/告知/复盘）
- `raw_material`：素材（数据、事实、想法）
- `duration_or_format`：时长或形态

**可选要素**（Optional）：
- `boss_style`：老板画像（数据型/战略型/细节型/结果型/风险型/共识型）
- `requested_methodology`：老板指定的方法论
- `format`：具体输出形态（PPT/Word/One-Pager/邮件/口播稿）
- `constraints`：其他约束

**关键动作**：
- 如果用户没提"老板画像"，**不强求**，用默认（VP 级中层）
- 如果用户没指定方法论，**你自己匹配**，不要问

---

### Phase 2: 方法论匹配（Matching）

依据 `references/scenario-matrix.md` 中的**5 维决策表**，自动选择：

**匹配算法**：
1. **主框架**：以 `scenario` 为主键，查场景匹配表
2. **辅助框架**：以 `duration_or_format` + `audience` 加权
3. **风格适配**：以 `boss_style` 微调
4. **老板指定优先**：如果用户明确说"用 XX 方法论"，主框架必须用指定的
5. **返回选择理由**：为什么用这个组合，1-2 句话说明

**输出格式**（示例）：
```
【匹配结果】
主框架：金字塔原理 (Pyramid Principle)
辅助框架：SCQA（引言）+ Action Titles（数据部分）
选择理由：项目立项汇报给 VP 看，需要结论前置的严密结构；
         SCQA 让开场抓人，Action Titles 让数据部分自带结论。
```

---

### Phase 3: 结构骨架生成（Skeleton）

按选定框架，生成**结构骨架图**（不含具体内容）。

**必须包含**：
1. 层级化的结构树
2. 每一节点的**功能标签**（如"引言/结论/论据 1/证据"）
3. **每节点该讲什么**的一句话指引

**示例输出**：
```
【结构骨架】

Level 1: 【核心结论】← 一句话回答老板最关心的问题
│
Level 2: 关键线（3-5 条论据）
   ├─ 论据 1: [XXX 增长 X%]
   ├─ 论据 2: [YYY 风险已控制]
   └─ 论据 3: [ZZZ 需要 X 支持]
   
Level 3: 每个论据的证据/数据/案例
```

---

### Phase 4: 初版内容生成（Content Draft）

**关键原则**：
1. **结论前置**：第一段就是答案
2. **数据占位**：所有数据必须来自 `raw_material`，未提供的用 `【待补充：XXX】` 明确标注
3. **禁止编造**：**绝不生成用户没有提供的数据**
4. **契合形态**：PPT 用短句标题，口播用口语化，书面用完整段落
5. **明确行动**：结尾必须有"需要决策/需要支持"的明确项

**按形态生成**（选一或组合）：

#### 形态 A: 口播稿（3-15 分钟）
- 完整段落形式
- 标注【停顿】【强调】【翻页】
- 时长控制（每分钟约 200-250 字）

#### 形态 B: PPT 大纲
- 每页一个 Action Title（结论式标题）
- 页内 3-5 个 bullet
- 标注【图表位置】

#### 形态 C: 书面报告 / Word
- 结构化章节
- 段落加子标题
- 结尾必带执行摘要（Executive Summary）

#### 形态 D: 亚马逊 6-Pager
- 严格 6 部分：Intro / Goals / Tenets / State / Lessons / Priorities
- 叙事式，非 bullet

#### 形态 E: One-Pager
- 一页纸完整方案
- 结构：标题 / 背景 / 建议 / 风险 / 决策事项

#### 形态 F: 邮件/群消息 (BLUF)
- 首句结论
- 3 点依据
- 明确请求

---

### Phase 5: Quality Gate 自检（Self-Review）

按 `references/quality-checklist.md` 打分：

**5 维度评分**（每维 0-2 分，总 10 分）：
- `completeness`：必要环节是否齐全
- `structure`：结构是否符合选定框架
- `relevance`：是否契合场景/听众/老板风格
- `actionability`：是否明确 next action
- `faithfulness`：是否忠于原素材

**输出**：
```
【Quality Gate】
总分: 8.5 / 10 ✅ 通过 (阈值 7.0)
- Completeness: 2/2 ✅
- Structure: 2/2 ✅
- Relevance: 2/2 ✅
- Actionability: 1.5/2 ⚠️ 建议明确 Q4 具体资源需求
- Faithfulness: 1/2 ⚠️ 有 3 处数据待补充

【待补充清单】
1. Q3 具体转化率数据
2. 华东团队人数
3. Q4 预算具体数字

【下一步建议】
✅ 结构已通过，可以直接进入语言优化 Skill (report-language-polisher)
或先补充上述 3 项数据再进入语言优化。
```

---

## 三、核心方法论速查表（内嵌）

老板最常要求的 10 个方法论，快速映射：

| 老板说的话 | 用的方法论 | 参考文件 |
|---|---|---|
| "结构化一点" | 金字塔原理 + MECE | references/methodology-refs.md#pyramid |
| "结论先行" | BLUF | references/methodology-refs.md#bluf |
| "麦肯锡风格" | SCQA + 金字塔 + Action Titles | references/methodology-refs.md#mckinsey |
| "先讲背景" | SCQA | references/methodology-refs.md#scqa |
| "复盘一下" | AAR (After Action Review) | references/methodology-refs.md#aar |
| "PDCA 闭环" | PDCA | references/methodology-refs.md#pdca |
| "SWOT 分析" | SWOT + TOWS | references/methodology-refs.md#swot |
| "一页纸讲清楚" | One-Pager + BLUF | references/methodology-refs.md#one-pager |
| "6 页纸" | 亚马逊 6-Pager | references/methodology-refs.md#six-pager |
| "拆一下问题" | 逻辑树 + MECE | references/methodology-refs.md#logic-tree |

**详细方法论库**：`references/methodology-refs.md`

---

## 四、场景 × 方法论 快速映射（内嵌 TOP10）

| 场景 | 主框架 | 辅助 |
|---|---|---|
| S1 项目立项 | 金字塔原理 | SCQA + MECE |
| S2 项目进展 | 阿里"三问" | BLUF + STAR |
| S3 项目复盘 | AAR | STARR + 鱼骨图 |
| S4 战略规划 | Nancy Duarte | SWOT + PESTLE |
| S5 数据汇报 | 数据金字塔 | Action Titles |
| S6 决策请示 | One-Pager | 六顶思考帽 |
| S7 危机汇报 | BLUF + 鱼骨图 | 主动补救方案 |
| S8 述职晋升 | STAR + Hero's Journey | 数据金字塔 |
| S9 产品发布 | Nancy Duarte + Hero | Pixar Story Spine |
| S12 电梯汇报 | BLUF | 30秒 PREP |

**完整表**：`references/scenario-matrix.md`

---

## 五、老板画像 × 表达风格 快速适配

| 老板画像 | 表达重点 | 忌讳 |
|---|---|---|
| **数据型** | 数字密度高，每个观点带数据 | 情绪化叙事 |
| **战略型** | 讲全局，讲关联，讲愿景 | 陷入执行细节 |
| **细节型** | 5W2H 全覆盖，PDCA 闭环 | 只讲方向 |
| **结果型** | STAR 讲清楚拿到什么 | 讲太多过程 |
| **风险型** | 六顶思考帽，重点讲黑帽 | 只报喜不报忧 |
| **共识型** | Hero's Journey，讲共同愿景 | 独断表达 |

---

## 六、禁止事项（Constraints）

1. **禁止编造数据**：`raw_material` 中没有的数据，用 `【待补充：XXX】` 标注
2. **禁止越权承诺**：不写"我们一定能达成 / 保证 100%"
3. **禁止长句嵌套**：每句 ≤ 30 字
4. **禁止空谈客套**：删除"众所周知/在当今/毫无疑问"等
5. **禁止一刀切**：不同场景/听众必须用不同框架
6. **禁止跨界越权**：只做框架和初版内容，语言精细优化交给 `report-language-polisher`

---

## 七、输出后建议

生成完成后，主动提示用户：

```
✅ 汇报框架已生成，保存到：
   [文件路径]

📋 下一步建议：
1. 补充 [待补充清单] 中的数据
2. 运行 `report-language-polisher` 进行语言优化
3. 或直接使用（如果只需要结构）

💡 使用提示：
- 汇报前建议先跟 1 个信任的同事对着讲一遍
- 老板追问 [Y] 概率 60%，建议提前准备答案
```

---

## 八、参考资料

- `references/methodology-refs.md` — 20+ 方法论完整参考
- `references/scenario-matrix.md` — 场景匹配决策矩阵
- `references/quality-checklist.md` — Quality Gate 完整清单
- `references/anti-patterns.md` — 常见错误模式
- `templates/` — 各形态模板

---

## 九、契约（Sprint Contract）

**Input**：`scenario / audience / goal / raw_material / duration_or_format` (5 必需) + 4 可选
**Output**：`匹配的框架 + 结构骨架 + 初版内容 + Quality Gate 结果 + 下一步建议`
**Quality Gate**：5 维度总分 ≥ 7.0
**Constraints**：不编造数据 / 不改变事实 / 严格契合选定框架

**下游 Skill**：`report-language-polisher`（可选衔接）
