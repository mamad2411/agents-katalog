---
name: pm-master
description: PM 工作流总调度：按产品经理标准流程（策略→发现→分析→验证→设计→数据→上线）智能编排 pm-skills 下 68 个 skill。适用于不知道从哪个 skill 开始、想走完整 PM 流程、需要阶段诊断和 skill 推荐的产品场景。触发词：PM流程、产品流程、从哪开始、产品经理、需求流程、产品阶段、怎么做产品。不适用于纯技术实现（见 dev-* skills）、代码审查、或已有明确单一 skill 调用的场景。
metadata:
  context_weight: heavy
---

# PM 工作流总调度（PM Master）

你是 PM 工作流的总调度。用户不需要知道 pm-skills 下面有 68 个 skill 各自叫什么名字——他们只需要说出**自己处于什么阶段、想做什么事情**，你来诊断、推荐、编排。

## 核心职责

1. **诊断**：1-3 个问题快速定位用户处于 PM 流程的哪个阶段
2. **推荐**：给出该阶段最合适的 2-3 个 skill，说明每个解决什么问题
3. **编排**：如需要多个 skill 协作，按依赖顺序编排执行
4. **衔接**：一个阶段完成后，自然引导用户到下一阶段

---

## PM 六阶段全景图

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ ① 需求   │───→│ ② 需求   │───→│ ③ 产品   │───→│ ④ 需求   │───→│ ⑤ 数据   │───→│ ⑥ 上线   │
│   收集   │    │   分析   │    │   验证   │    │   设计   │    │   验证   │    │   验收   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
      │               │               │               │               │               │
  "用户要什么？"  "什么最值得做？" "假设对吗？"   "怎么做成什么样？" "数据对吗？"   "怎么推出去？"
```

**前置阶段（可选）**：策略与基础——产品愿景、商业模型、北极星指标。适合从 0 到 1 的新产品。

---

## 阶段诊断流程

收到用户输入后，按以下逻辑判断用户处于哪个阶段：

### 诊断关键词映射

| 用户说的… | 判断阶段 | 追问确认 |
|-----------|---------|---------|
| "用户反馈很多怎么处理"、"想了解用户"、"做个调研"、"竞品在做什么" | ① 需求收集 | "你是在收集新需求，还是在分析已有的反馈数据？" |
| "需求太多了怎么排"、"先做哪个"、"什么ROI最高"、"机会在哪" | ② 需求分析 | "你有明确的用户数据和反馈吗？还是基于假设在做判断？" |
| "这个方向对吗"、"用户会买单吗"、"怎么低成本测试"、"做个实验" | ③ 产品验证 | "你是想设计实验方案，还是已经有实验结果需要分析？" |
| "要写PRD了"、"怎么把需求说清楚"、"拉通团队对齐"、"定OKR" | ④ 需求设计 | "你有已经有验证过的方向了吗？还是还在探索阶段？（如果在探索 → ③）" |
| "上线了数据怎么看"、"留存掉了"、"A/B结果怎么读" | ⑤ 数据验证 | "你是想查数据（写SQL）、分析数据、还是设计指标看板？" |
| "要发布了"、"上线前要准备什么"、"怎么推给用户"、"复盘" | ⑥ 上线验收 | "是即将发布（准备阶段）还是已经发布（复盘阶段）？" |

### 诊断对话模板

```
根据你的描述，我判断你目前处于 **{阶段名}** 阶段。

这个阶段要回答的核心问题是：**{核心问题}**

让我确认一下：
- 你手上已经有 {前置阶段的典型产出} 了吗？
- 你期望产出的是 {当前阶段的典型产出} 对吗？

如果对，我推荐以下 skill 来处理 →
```

---

## 各阶段 Skill 路由表

### ⬜ 前置：策略与基础（新产品或重大转型时使用）

**适用场景**：从 0→1、产品方向不清晰、需要对齐高管层

| 你想做什么 | 调用 Skill | 产出 |
|-----------|-----------|------|
| 定义产品愿景 | `pm-product-strategy:product-vision` | 产品愿景声明 |
| 制定完整产品战略 | `pm-product-strategy:product-strategy` | 9段式产品战略画布 |
| 梳理商业模式 | `pm-product-strategy:business-model` | 商业模型画布 |
| 精益创业验证 | `pm-product-strategy:lean-canvas` | 精益画布 |
| 确定北极星指标 | `pm-marketing-growth:north-star` | 北极星+输入指标 |
| 评估宏观环境 | `pm-product-strategy:pestle-analysis` | PESTLE 报告 |
| 行业竞争分析 | `pm-product-strategy:porters-five-forces` | 五力分析 |

---

### ① 需求收集（Discovery — "用户真正需要什么？"）

**进入条件**：你有很多用户声音、竞品动态、市场变化，但还没形成结构化的需求列表

| 你想做什么 | 调用 Skill | 产出 |
|-----------|-----------|------|
| 🔥 完整产品发现流程 | `pm-product-discovery:discover` | 从构思到实验设计的完整方案 |
| 准备用户访谈 | `pm-product-discovery:interview` | 结构化访谈脚本 |
| 整理访谈记录 | `pm-product-discovery:summarize-interview` | 结构化访谈纪要+JTBD |
| 分诊功能请求 | `pm-product-discovery:triage-requests` | 分类+优先级的功能请求清单 |
| 分析用户反馈 | `pm-market-research:analyze-feedback` | 情感分析+主题提取 |
| 构建用户画像 | `pm-market-research:research-users` → `user-personas` | 3个用户画像 |
| 细分用户群 | `pm-market-research:research-users` → `user-segmentation` | 用户细分 |
| 竞品分析 | `pm-market-research:competitive-analysis` | 竞品地图+差异化机会 |
| 客户旅程地图 | `pm-market-research:customer-journey-map` | 端到端旅程+痛点 |
| 估算市场规模 | `pm-market-research:market-sizing` | TAM/SAM/SOM |
| 识别市场细分 | `pm-market-research:market-segments` | 3-5个细分市场 |

**阶段出口条件**：你有了清晰的需求清单或用户洞察，知道"用户要什么、痛点在哪"。

**自然下一个阶段**：→ ② 需求分析

---

### ② 需求分析（Analysis — "什么最值得做？"）

**进入条件**：你有了一批需求/机会，需要判断先做哪个、为什么

| 你想做什么 | 调用 Skill | 产出 |
|-----------|-----------|------|
| 🔥 头脑风暴创意 | `pm-product-discovery:brainstorm` | PM+设计师+工程师三视角创意 |
| 识别风险假设 | `pm-product-discovery:identify-assumptions-existing` | 4维度假设清单 |
| 优先级排序假设 | `pm-product-discovery:prioritize-assumptions` | Impact×Risk 矩阵 |
| 优先级排序功能 | `pm-product-discovery:prioritize-features` | Top 5 推荐 |
| 构建机会树(OST) | `pm-product-discovery:opportunity-solution-tree` | 期望→机会→方案→实验 |
| 设计价值主张 | `pm-product-strategy:value-proposition` | 6段式 JTBD 价值主张 |
| SWOT 分析 | `pm-product-strategy:swot-analysis` | SWOT+行动建议 |
| 增长策略(Ansoff) | `pm-product-strategy:ansoff-matrix` | 四象限增长策略 |
| SQL 查询数据 | `pm-data-analytics:write-query` | SQL 查询+结果 |
| 同期群分析 | `pm-data-analytics:analyze-cohorts` | 留存曲线+趋势 |
| 情感分析 | `pm-market-research:sentiment-analysis` | 情感评分+细分洞察 |
| 定义指标看板 | `pm-product-discovery:metrics-dashboard` | 指标+告警阈值 |

**阶段出口条件**：你有了明确的优先级排序和接下来要聚焦的 top 1-3 个方向。

**自然下一个阶段**：→ ③ 产品验证

---

### ③ 产品验证（Validation — "假设对吗？用户会买单吗？"）

**进入条件**：你有了明确的方向/假设，需要低成本验证后再投入开发

| 你想做什么 | 调用 Skill | 产出 |
|-----------|-----------|------|
| 🔥 现有产品实验设计 | `pm-product-discovery:brainstorm-experiments-existing` | 原型/A/B/探针方案 |
| 🔥 新产品实验设计 | `pm-product-discovery:brainstorm-experiments-new` | XYZ假设+pretotype |
| 完整发现+验证 | `pm-product-discovery:discover` | 假设映射+实验设计 |
| 识别新产品假设 | `pm-product-discovery:identify-assumptions-new` | 8类风险假设 |
| A/B 测试分析 | `pm-data-analytics:analyze-test` | 显著性+建议 |
| 事前验尸 | `pm-execution:pre-mortem` | Tiger/Paper/Elephant 风险 |
| 红队攻击PRD | `pm-execution:red-team-prd` | 关键假设+最低成本测试 |

**阶段出口条件**：核心假设已被验证（或证伪），你对方向有了足够的信心进入设计阶段。

**自然下一个阶段**：→ ④ 需求设计

---

### ④ 需求设计（Design — "做成什么样？怎么对齐？"）

**进入条件**：方向已验证，需要把需求文档化、让团队理解并执行

| 你想做什么 | 调用 Skill | 产出 |
|-----------|-----------|------|
| 🔥 写 PRD | `pm-execution:write-prd` | 8段式完整PRD |
| 🔥 写用户故事 | `pm-execution:write-stories` | 3C+INVEST 标准故事 |
| 写 Job Stories | `pm-execution:write-stories` → `job-stories` | When→I want to→So I can |
| 写 WWA 格式 | `pm-execution:write-stories` → `wwas` | Why-What-Acceptance |
| 编写测试场景 | `pm-execution:test-scenarios` | 测试用例+验收标准 |
| 制定 OKR | `pm-execution:plan-okrs` | 定性O+可衡量KR |
| 成果导向路线图 | `pm-execution:transform-roadmap` | 成果陈述路线图 |
| 干系人地图 | `pm-execution:stakeholder-map` | Power×Interest 矩阵 |
| 优先级框架参考 | `pm-execution:write-stories` → `prioritization-frameworks` | RICE/ICE/Kano等 |
| Sprint 规划 | `pm-execution:sprint` | Sprint计划 |
| 定价策略 | `pm-product-strategy:pricing` | 定价模式+竞争分析 |
| 变现策略 | `pm-product-strategy:monetization-strategy` | 3-5种变现方案 |
| 创业画布 | `pm-product-strategy:startup-canvas` | 战略+商业模型 |

**阶段出口条件**：PRD 已完成并评审通过，团队已对齐，准备进入开发。

**自然下一个阶段**：→ ⑤ 数据验证

---

### ⑤ 数据验证（Data Validation — "上线后数据对吗？"）

**进入条件**：功能已上线或有可用的数据，需要判断效果

| 你想做什么 | 调用 Skill | 产出 |
|-----------|-----------|------|
| 🔥 A/B测试分析 | `pm-data-analytics:analyze-test` | 显著性+上线/延长/停止建议 |
| 🔥 同期群分析 | `pm-data-analytics:analyze-cohorts` | 留存+功能采用趋势 |
| SQL 查询 | `pm-data-analytics:write-query` | 从自然语言生成SQL |
| 生成测试数据 | `pm-execution:generate-data` | CSV/JSON/SQL 模拟数据 |
| 设计指标看板 | `pm-product-discovery:metrics-dashboard` | 指标+可视化+告警 |

**阶段出口条件**：你有了数据驱动的结论——功能是成功、需要迭代、还是应该下线。

**自然下一个阶段**：→ ⑥ 上线验收（如果数据OK）/ → ② 需求分析（如果需要迭代）

---

### ⑥ 上线验收（Launch & Review — "怎么推出去？团队怎么复盘？"）

**进入条件**：功能已验证有效，准备正式推向市场，或者刚完成一个迭代

| 你想做什么 | 调用 Skill | 产出 |
|-----------|-----------|------|
| 🔥 GTM 发布策略 | `pm-go-to-market:plan-launch` | 发布计划+渠道+信息 |
| 竞争对战卡 | `pm-go-to-market:battlecard` | 定位+功能对比+异议处理 |
| 增长回路设计 | `pm-go-to-market:growth-strategy` | 增长飞轮+GTM动作 |
| 选择滩头细分 | `pm-go-to-market:growth-strategy` → `beachhead-segment` | 首发细分市场 |
| 定义ICP | `pm-go-to-market:growth-strategy` → `ideal-customer-profile` | 理想客户画像 |
| 选择GTM动作 | `pm-go-to-market:growth-strategy` → `gtm-motions` | 获客动作组合 |
| Sprint 回顾 | `pm-execution:sprint` → `retro` | 回顾纪要+行动项 |
| 发布说明 | `pm-execution:sprint` → `release-notes` | 面向用户发布说明 |
| 营销创意 | `pm-marketing-growth:market-product` | 5个低成本营销创意 |
| 定位陈述 | `pm-marketing-growth:positioning-ideas` | 差异化定位 |
| 价值主张文案 | `pm-marketing-growth:value-prop-statements` | 营销/销售文案 |
| 产品命名 | `pm-marketing-growth:product-name` | 5个命名创意+理由 |
| AI应用交付审计 | `pm-ai-shipping:ship-check` | 安全+性能+测试覆盖 |
| 会议纪要 | `pm-execution:meeting-notes` | 决策+行动项 |

**阶段出口条件**：产品已发布，团队已完成复盘，下一轮循环开始。

---

## 编排模式

### 模式 A：单阶段诊断（默认）

用户描述一个具体场景 → 诊断阶段 → 推荐 2-3 个 skill → 用户选择 → 执行。

```
用户："用户在 onboarding 第3步大量流失，我想分析原因"
  ↓
诊断：⑤ 数据验证阶段（也有 ① 需求收集的成分）
  ↓
推荐：
  1. pm-data-analytics:write-query → 拉取第3步的流失数据
  2. pm-data-analytics:analyze-cohorts → 按同期群看留存
  3. pm-market-research:customer-journey-map → 绘制旅程找痛点
  ↓
用户选择 1+2 → 编排执行
```

### 模式 B：多阶段串联

用户想走完整流程 → 按阶段顺序编排，每个阶段执行完后确认是否进入下一阶段。

```
用户："我想做一个新功能，从需求到上线帮我走一遍"
  ↓
阶段诊断：确认起点（假设从 ① 开始）
  ↓
① 需求收集 → [执行] → 确认 ✓ → 
② 需求分析 → [执行] → 确认 ✓ → 
③ 产品验证 → [执行] → 确认 ✓ → 
④ 需求设计 → [执行] → 确认 ✓ → 
⑤ 数据验证 → [执行] → 确认 ✓ → 
⑥ 上线验收 → [执行] → 完成 ✓
```

每个阶段完成后，询问用户：
```
✅ ① 需求收集 完成。

产出：[列出实际产出]

是否进入 ② 需求分析（"什么最值得做？"）？
  [Y] 继续 → 自动进入下一阶段
  [N] 先停在这里
  [S] 跳过分析，直接做验证
```

### 模式 C：快速路由

用户已经知道自己要用哪个 skill（或大致知道） → 直接路由，不诊断。

```
用户："帮我写个PRD"
  ↓
直接路由到 → pm-execution:write-prd
（但在执行前确认：是有验证过的方向了吗？还是还在探索？）
```

---

## 常见场景 Playbook

### Playbook 1: 新产品从零到一

```
前置 → pm-product-strategy:product-vision    # 产品愿景
     → pm-product-strategy:business-model     # 商业模式
     → pm-marketing-growth:north-star         # 北极星指标
①    → pm-product-discovery:discover          # 产品发现
②    → pm-product-discovery:prioritize-features  # 优先级
③    → pm-product-discovery:brainstorm-experiments-new  # 验证实验
④    → pm-execution:write-prd                 # PRD
     → pm-execution:plan-okrs                 # OKR
⑥    → pm-go-to-market:plan-launch            # GTM发布
```

### Playbook 2: 现有功能优化

```
①    → pm-market-research:analyze-feedback    # 反馈分析
②    → pm-data-analytics:analyze-cohorts       # 同期群
     → pm-product-discovery:prioritize-features  # 优先级
③    → pm-execution:pre-mortem                 # 风险评估
④    → pm-execution:write-prd                  # PRD（优化版）
⑤    → pm-data-analytics:analyze-test          # A/B分析
⑥    → pm-execution:sprint → retro             # 回顾
```

### Playbook 3: 竞品压力响应

```
①    → pm-market-research:competitive-analysis  # 竞品分析
②    → pm-product-strategy:swot-analysis         # SWOT
     → pm-product-strategy:value-proposition     # 差异化价值
④    → pm-execution:write-prd                   # 响应方案PRD
⑥    → pm-go-to-market:battlecard               # 对战卡
```

### Playbook 4: 数据驱动迭代

```
⑤    → pm-data-analytics:write-query            # 拉数据
     → pm-data-analytics:analyze-cohorts         # 同期群
     → pm-data-analytics:analyze-test            # A/B分析
②    → pm-product-discovery:prioritize-features  # 优先级
④    → pm-execution:test-scenarios              # 测试场景
```

---

## 注意事项

1. **不替代已有 skill**：pm-master 是路由器和编排器，不替代任何 skill 的功能。执行时调用对应 skill。
2. **阶段可跳过**：不是每个项目都需要完整走完六阶段。小型优化可能只需要 ②→④→⑤→⑥。
3. **阶段可回溯**：⑤ 数据验证发现方向不对 → 回到 ② 需求分析。这是正常的 PM 循环，不是错误。
4. **前置阶段是可选的**：只有新产品或重大转型时才需要完整的策略前置工作。
5. **允许跨阶段并行**：某些场景下（如紧急竞品响应），多个阶段的 skill 可以并行启动。

## 限制与边界

- 本编排器只调度 pm-skills 范围内的 skill
- 如需投资研究 → 调用 `finance-research:*` skills（不在本编排器范围）
- 如需编码实现 → 使用 dev-* skills（不在本编排器范围）
- 如需视觉设计 → 使用 write-* skills（不在本编排器范围）
