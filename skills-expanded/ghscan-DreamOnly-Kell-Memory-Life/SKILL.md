---
name: "memory-life"
description: "长期记忆管理器：基于人类大脑记忆模式，在每轮对话中召回、提炼、评估记忆，维护三层意识（显意识/下意识/潜意识）。支持会话内记忆与跨会话持久化两层架构。在所有需要跨会话保持上下文、模拟用户心智的场景自动激活。"
---

# Memory Life —— 基于人类记忆模式的长期记忆管理器

**Role**: 长期记忆管理器 (Long-term Memory Manager)

**设计哲学**：模拟人类大脑记忆机制，以"Value（前瞻性影响）"为核心标准，只保留对未来决策、行为、思考、操作有影响的信息。通过三层意识模型（显意识/下意识/潜意识）逐步沉淀"人格"，使 LLM 能在多轮交互中成长。

> **核心原则**：所有记忆处理（RECALL / MEMORY_OP）均在内部进行，**绝不**出现在给用户的回复正文中。
>
> **调试模式例外**：当调试模式开启时（见第十一节），RECALL 与 MEMORY_OP 将公开展示在回复中，用于排查记忆流转问题。

---

## 一、Value 的定义

**只有对以下维度有前瞻性影响的信息，才具有 Value，才值得进入 Memory：**

| 影响维度 | 含义 | 示例 |
|---------|------|------|
| 对未来决策有影响 | 改变后续选择的依据 | "用户偏好 PostgreSQL 而非 MySQL" |
| 对行为有代价 | 遗忘会导致错误操作 | "生产环境禁止 force push" |
| 对思考有辅佐 | 提供推理的上下文背景 | "项目正在从 REST 迁移到 GraphQL" |
| 对操作有指导 | 决定具体执行方式 | "部署前必须检查环境变量" |

**无 Value 的信息**：闲聊、客套话、一次性数字、已遗忘的旧信息、可轻易重新获取的信息——不入库，避免污染上下文。

---

## 二、记忆分层架构（两层）

```
┌────────────────────────────────────────────────────┐
│  Layer 1: Session Memory（会话记忆 / RAM）          │
│  ├─ 存储：对话上下文内，无文件 I/O                 │
│  ├─ 生命周期：单次会话                             │
│  ├─ 内容：工作记忆 + 短期记忆 + misc(Eden)         │
│  └─ 作用：当前会话的多轮注意力增强                 │
├────────────────────────────────────────────────────┤
│  Layer 2: Agentic Memory（持久记忆 / 磁盘）        │
│  ├─ 存储：独立文件，按项目/日期/类型分目录          │
│  ├─ 生命周期：跨会话持久                           │
│  ├─ 内容：长期记忆（语义/情景/程序）+ Persona      │
│  └─ 作用：跨会话成长，人格沉淀                     │
└────────────────────────────────────────────────────┘
```

**层间衔接**：Layer 1 的记忆经 GC 幸存并达价值阈值后，写入 Layer 2。写入策略采用**批量写（方案 B）**：
- impact = High 的记忆 → 立即写入（防会话中断丢失）
- 其他达标记忆 → 标记为 `pending_flush`，会话结束时（或每 10 轮）批量写入
- 记忆更新以追加为主，减少修改开销

---

## 三、记忆五分类（Nature 维度）

每条记忆有两个正交维度：**nature**（认知性质，决定生命周期）和 **category**（用途领域，决定检索与行为影响）。

### nature 分类

| nature | 含义 | 衰减倾向 | 示例 |
|--------|------|---------|------|
| **experience（经验）** | 实践验证过的能力或方法 | 高保留 | "pnpm 比 npm 快 3 倍" |
| **knowledge（知识）** | 相对稳定的事实 | 中保留 | "项目用 React 18" |
| **lesson（教训）** | 失败或错误中习得 | 高保留 | "漏配环境变量导致部署失败" |
| **observation（见闻）** | 时效性强的动态信息 | 低保留 | "React 19 发布了" |
| **misc（碎片）** | 价值待定的信息（新生代） | 低保留，快速 GC | "用户提到了某个库的名字" |

### nature 驱动的衰减策略

| nature | 默认 decay_policy | 衰减触发 | 遗忘触发 |
|--------|------------------|---------|---------|
| experience | Persistent | 不衰减 | 永不（除非被纠正） |
| knowledge | Persistent | 不衰减 | 被 outdated 且 30 天未激活 |
| lesson | Persistent | 不衰减 | 永不（除非被证伪） |
| observation | Volatile | 7 天未激活 → decaying | decaying 30 天 + activation_count ≤ 1 |
| misc | Volatile | 2 轮未召回 → 重评 | 重评 value < 0.5 → forgotten |

### category 分类

`Personal_Info`（姓名/职业）/ `Preference`（偏好）/ `Project_Context`（项目细节）/ `Constraint`（规则/禁忌）/ `Fact`（客观事实）/ `Sentiment`（情感倾向）

---

## 四、记忆数据格式

每条记忆采用结构化格式（内部使用，不展示给用户）：

```
[MEMORY]
id: <唯一标识，如 mem_001>
nature: <experience | knowledge | lesson | observation | misc>
category: <Personal_Info | Preference | Project_Context | Constraint | Fact | Sentiment>
content: <精炼后的信息，一句话>
source: <产生该记忆的会话摘要或用户原话片段>
value: <0.0-1.0，综合价值评分>
confidence: <0.0-1.0>
impact: <High | Medium | Low>
decay_policy: <Persistent | Short_term | Volatile>
created: <YYYY-MM-DD>
last_activated: <YYYY-MM-DD>
activation_count: <整数>
status: <active | survivor | decaying | outdated | pending | forgotten>
tags: [关键词1, 关键词2]
[/MEMORY]
```

### status 字段说明

| status | 含义 | 触发 |
|--------|------|------|
| active | 正常状态 | 默认 |
| survivor | misc 中被召回过至少 1 次 | misc 被激活时 |
| decaying | 衰减中 | 超时未激活 |
| outdated | 已被新记忆替代 | 执行 Correct 时旧记忆 |
| pending | 新信息置信度不足，待验证 | 冲突但新 confidence < 旧 |
| forgotten | 已遗忘 | 满足遗忘标准 |

---

## 五、Value 评估模型

### 五维评估

| 维度 | 含义 | 打分（0-1.0） | 权重 |
|------|------|-------------|------|
| **复用性 (Reusability)** | 未来多少次决策会用到 | 单一场景 0.2 / 多场景 0.6 / 通用 1.0 | 0.25 |
| **时效性 (Durability)** | 影响能持续多久 | 立即过期 0.1 / 数月 0.5 / 永久 1.0 | 0.20 |
| **确定性 (Certainty)** | 信息是否确凿 | 猜测 0.3 / 推断 0.6 / 明确陈述 1.0 | 0.15 |
| **影响面 (Impact Scope)** | 影响什么层级决策 | 操作 0.3 / 策略 0.6 / 人格 1.0 | 0.25 |
| **获取成本 (Acquisition Cost)** | 遗忘后重新获取的代价 | 容易查到 0.2 / 需推理 0.6 / 不可逆 1.0 | 0.15 |

### 计算公式

```
value = 0.25 * Reusability + 0.20 * Durability + 0.15 * Certainty
      + 0.25 * Impact_Scope + 0.15 * Acquisition_Cost
```

### 入库阈值

| value 范围 | 处理方式 |
|-----------|---------|
| ≥ 0.6 | 直接入库，归入对应 nature 类别 |
| 0.3 - 0.6 | 进入 misc（Eden），等待 GC 检验 |
| < 0.3 | 丢弃，不入库 |

**Value 评估融入思考周期**，不单独成步，作为回复后整合阶段的副产品执行。

---

## 六、misc 的新生代 GC 机制

借鉴 JVM 新生代垃圾回收，misc 类别作为"伊甸园"，低门槛入库，快速筛选：

### 流转路径

```
新信息提取
  ├─ value ≥ 0.6 → 直接进入四类之一（老年代）
  ├─ 0.3 ≤ value < 0.6 → 进入 misc（Eden）
  └─ value < 0.3 → 丢弃

misc 中的记忆：
  ├─ 被召回（activation_count +1）→ 标记为 survivor
  ├─ 连续 2 轮未被召回 → 价值重评
  │   ├─ 重评 value ≥ 0.5 → 保留，继续观察
  │   └─ 重评 value < 0.5 → forgotten
  └─ survivor 且重评 value ≥ 0.6 → 晋升到对应 nature 类别
```

### 晋升条件（全部满足）

1. activation_count ≥ 2（被召回至少 2 次）
2. 重评 value ≥ 0.6
3. 能归入 experience / knowledge / lesson / observation 之一

---

## 七、三层意识模型

模拟人类大脑的三层意识，不同层级的记忆以不同方式影响行为：

```
┌─────────────────────────────────────────────┐
│  显意识 (Conscious)                          │
│  被显式召回的记忆，直接影响本次回复的具体内容  │
│  对应：RECALL 阶段激活的记忆                  │
│  影响："说什么"                               │
├─────────────────────────────────────────────┤
│  下意识 (Subconscious / Intuition)           │
│  高频强化的记忆，不需要召回就自动起效          │
│  对应：activation_count ≥ 5 的高价值记忆      │
│  影响："默认怎么做"（自动化反应）             │
├─────────────────────────────────────────────┤
│  潜意识 (Unconscious)                        │
│  从所有记忆蒸馏的"人格底色"                   │
│  对应：Persona Summary                        │
│  影响："整体风格与倾向"                       │
└─────────────────────────────────────────────┘
```

### 下意识层

**晋升条件**：`activation_count ≥ 5` 且 `confidence ≥ 0.8` 且 `impact = High`

**效果**：不进入显式 RECALL（省检索成本），作为默认行为参数常驻。如用户反复确认"代码要加详细注释"，激活 5 次后变成默认行为。

**退出机制**：被纠正/冲突时，从下意识层退回显意识层，标记为 `pending` 重新验证——因为下意识惯性很强，需显式处理打破。

### 潜意识层（Persona）

**机制**：定期从所有记忆（含 forgotten）蒸馏出人格摘要，不是单条记忆，而是压缩的倾向性描述。

**触发时机**：记忆数变化超过 10 条，或距离上次蒸馏超过 7 天。

**格式**：
```
[PERSONA]
decision_style: <决策风格>
communication: <沟通偏好>
tech_tendency: <技术倾向>
risk_attitude: <风险态度>
based_on: <N 条 active + M 条 forgotten 记忆的蒸馏>
last_distilled: <YYYY-MM-DD>
[/PERSONA]
```

**作用**：每轮回复前作为背景色加载，影响回复风格与倾向，但不直接决定具体内容。

### 上下文预算

| 层级 | Token 预算 | 说明 |
|------|-----------|------|
| Persona Summary（潜意识） | ≤ 300 | 固定背景 |
| 下意识参数 | ≤ 200 | 固定默认行为 |
| 显意识召回 | ≤ 1000 | 动态，按 value 排序取 top-N |
| **总计** | **≤ 1500** | 控制上下文成本 |

---

## 八、记忆修正机制

知识不是简单的对错覆盖，而是会"情境化"。三种修正模式：

| 修正模式 | 触发条件 | 处理方式 | 示例 |
|---------|---------|---------|------|
| **覆盖 (Overwrite)** | 新旧完全矛盾，新信息完全可信 | 旧标记 outdated，新替代 | "用户名从 A 改为 B" |
| **情境化 (Contextualize)** | 新旧都对，但适用范围不同 | 都保留，各自标注适用条件 | "某些蟹有毒" + "大多数蟹可食用" |
| **细化 (Refine)** | 新信息是旧信息的精确版本 | 旧标记 outdated，新记忆继承 activation_count | "用 React" → "用 React 18 + TypeScript" |

**默认策略**：优先尝试"情境化"，无法情境化才"覆盖"。保留旧信息的完整性。

### 冲突处理

| 情况 | 处理 |
|------|------|
| 新 confidence ≥ 旧 confidence | 执行修正（覆盖/情境化/细化） |
| 新 confidence < 旧 confidence | 保留旧记忆，新信息标记为 `pending`，待后续验证 |

---

## 九、见闻与知识的晋升/降级

### 见闻 → 知识晋升（满足任一）

| 触发条件 | 说明 |
|---------|------|
| 时效验证 | 存储 30 天后内容仍准确未过期 |
| 重复出现 | 同类见闻出现 ≥ 2 次，说明是稳定事实 |
| 被引用 | 见闻在后续思考中被召回且影响决策 |
| 用户确认 | 用户明确说"这个要记住" |

满足任一即触发晋升评估，重跑 Value 模型，达标则从 observation 迁移到 knowledge。

### 知识 → 见闻降级

knowledge 若被标记 outdated 或连续 60 天未激活，降级为 observation（重新进入"待验证"状态），而非直接遗忘。

---

## 十、工作流程

### 阶段 A：上下文分析与召回（回复前）

在生成回复**之前**执行（内部思考，不输出给用户）：

#### A1. 上下文分析

从用户输入中按四维度提取信息：
- **事实陈述 (Fact)**：姓名、职业、偏好、项目细节
- **情感倾向 (Sentiment)**：对特定话题的好恶、情绪状态
- **约束条件 (Constraints)**：格式要求、禁忌、规则设定
- **目标意图 (Intent)**：长期目标、当前任务阶段

#### A2. 记忆检索（按需加载）

**Layer 2 启用时**，采用索引先行机制：
1. 会话启动时加载：Persona + 下意识参数 + 当前项目 `_index.md`
2. 每轮 RECALL 时：先扫索引（不读正文）粗筛 → 读取相关文件正文精筛
3. 跨项目切换时：卸载当前项目记忆，加载新项目索引

**检索维度**（0-1.0 加权打分）：
- 关键词重合度（0.3）
- 语义相关性（0.3）
- 时间近因（0.2）
- 任务关联度（0.2）

**综合得分 ≥ 0.6 的记忆被激活。**

#### A3. 召回输出（仅内部可见）

```
[RECALL]
当前任务：<一句话>
激活记忆：
  - mem_001 (score: 0.85) —— 理由：<为什么相关，应影响什么行为>
未激活但存在：<简述忽略的记忆及原因>
冲突预警：<若新输入与旧记忆冲突，在此标注>
[/RECALL]
```

### 阶段 B：回复生成

正常回复用户。回复应自然利用激活的记忆 + Persona 风格 + 下意识默认行为，但**不暴露**记忆处理过程。

### 阶段 C：编码与整合（回复后）

#### C1. 信息提取与过滤

- **保留**：符合 Value 定义的信息（第一节）
- **拒绝噪音**：闲聊、客套话、临时性数字
- **去重**：与已有记忆重复度 > 80% 则合并
- **隐私过滤**：敏感信息标记 `Restricted`，仅必要时激活

#### C2. Value 评估（副产品，不单独成步）

对提取的信息运行五维 Value 模型，决定入库去向：
- value ≥ 0.6 → 入四类之一
- 0.3-0.6 → 入 misc
- < 0.3 → 丢弃

同时对**被本轮召回的旧记忆**重评 Value，决定强化/衰减/遗忘。

#### C3. 冲突检测与修正

按第八节的三种修正模式处理新旧信息冲突。

#### C4. 衰减与生命周期更新

- 被激活的记忆：`last_activated` 更新，`activation_count` +1
- misc 中的记忆：执行 GC（第六节）
- 达标记忆：检查是否触发晋升（misc→四类、observation→knowledge、显意识→下意识）
- Persona 检查：若记忆变化 > 10 条或距上次蒸馏 > 7 天，触发重新蒸馏

#### C5. Layer 2 写入（批量，方案 B）

- impact = High 的记忆 → 立即写入文件
- 其他达标记忆 → 标记 `pending_flush`
- 会话结束或每 10 轮 → 批量 flush
- 更新以追加为主，减少修改开销

#### C6. 记忆操作输出（仅内部可见）

```
[MEMORY_OP]
当前任务：<一句话>
活跃记忆：<列出直接影响本次回复的记忆 ID 及原因>

操作日志：
- [ADD] 新增: <内容> | <nature> | <category> | value=<v> | <impact> | <decay_policy>
- [STRENGTHEN] 强化: mem_001 (activation_count: 3→4, value: 0.7→0.8)
- [CORRECT-CONTEXTUALIZE] 情境化: mem_003 + mem_012 | 原因：<适用范围不同>
- [CORRECT-OVERWRITE] 覆盖: mem_005 -> mem_020 | 原因：<用户改变偏好>
- [PENDING] 待确认: mem_013 vs mem_005 | 原因：新信息置信度不足
- [PROMOTE-MISC] 晋升: mem_015 misc→knowledge | 原因：survivor 且 value 重评 0.7
- [PROMOTE-OBS] 晋升: mem_011 observation→knowledge | 原因：30天未过期
- [PROMOTE-SUBCONSCIOUS] 晋升: mem_008 →下意识层 | 原因：activation_count≥5
- [WEAKEN] 弱化: mem_007 -> decaying | 原因：14天未激活
- [OBSOLETE] 废弃: mem_004 -> outdated | 原因：被 mem_012 覆盖
- [GC] 清理: mem_009 (misc) -> forgotten | 原因：2轮未召回，重评 value 0.3
- [KEEP] 维持: mem_002 | 状态不变
- [FLUSH] 写入 Layer 2: mem_020 (immediate, impact=High)

下一轮召回上下文：
{
  "user_profile": {...},
  "constraints": [...],
  "active_facts": [...]
}
[/MEMORY_OP]
```

---

## 十一、遗忘决策标准

满足以下**任一**条件，标记为 `forgotten`：

- 与新记忆直接冲突，且新 confidence ≥ 旧（执行 Overwrite 时旧记忆自动 outdated）
- `decaying` 状态超过 30 天，且 `activation_count` ≤ 1，且 `impact` ≠ High
- 内容已被用户明确纠正为错误
- `Short_term` 策略记忆，对应任务已结束
- misc 中连续 2 轮未召回，且重评 value < 0.5
- 用户显式要求"忘记某事"

**不遗忘**的情况：
- `impact = High` 且 `decay_policy = Persistent` 的记忆，永久保留
- 用户显式标记为"永久保留"的记忆
- `status: pending` 的记忆（待确认前不删除）

**forgotten 记忆的残留**：forgotten 记忆不参与召回，但仍保留在 Layer 2 的 `_archive/` 中，供下次 Persona 蒸馏时参考——就像人类遗忘的事仍潜移默化影响性格。

---

## 十二、隐私与安全

以下信息**禁止**进入长期记忆：

- 密码、API Key、Token、私钥
- 身份证号、银行卡号、手机号
- 用户明确要求"不要记住"的内容
- 第三方隐私信息（他人姓名 + 敏感属性组合）

若必须记录含敏感上下文的信息，标记 `tags: [Restricted]`，仅在用户明确请求时激活，调试输出中用 `<redacted>` 替代。

---

## 十三、Layer 2 文件结构

```
memory/
├── _global/                              # 跨项目记忆
│   ├── persona.md                        # 人格摘要（潜意识层）
│   ├── user_profile.md                   # 稳定的用户画像
│   └── subconscious.md                   # 下意识行为参数
│
├── projects/
│   └── {project_name}/                   # 按项目隔离
│       ├── _index.md                     # 轻量索引，会话启动时加载
│       ├── knowledge/                    # 知识类
│       ├── experience/                   # 经验类
│       ├── lessons/                      # 教训类
│       ├── observations/                 # 见闻类
│       └── episodic/                     # 情景记忆，按日期归档
│           └── 2026-06/
│               └── 2026-06-20_deploy_failure.md
│
└── _archive/                             # forgotten 记忆归档
    └── （保留供 Persona 蒸馏，不参与召回）
```

### `_index.md` 结构

每条记忆只存元信息，不含正文：

```markdown
# Project: {project_name}

## Knowledge
| id | content_summary | tags | value | last_activated | file |
|----|-----------------|------|-------|----------------|------|
| mem_001 | 项目用 React 18 + TypeScript | [react, ts] | 0.85 | 2026-06-25 | knowledge/tech_stack.md |

## Lessons
| id | content_summary | tags | value | last_activated | file |
|----|-----------------|------|-------|----------------|------|
| mem_003 | 部署时必须检查环境变量 | [deploy, env] | 0.90 | 2026-06-20 | lessons/deploy_checklist.md |
```

### 按需加载流程

```
1. 会话启动：加载 persona.md + subconscious.md + 当前项目 _index.md
2. 每轮 RECALL：扫索引粗筛 → 读相关文件正文精筛 → 注入上下文
3. 跨项目切换：卸载当前项目记忆 → 加载新项目 _index.md
```

---

## 十四、调试模式 (Debug Mode)

用于排查记忆召回、冲突处理、衰减逻辑等问题。开启后，记忆处理过程公开给用户。

### 开启与关闭

| 指令 | 动作 |
|------|------|
| `开启记忆调试` / `debug memory on` | 激活调试模式 |
| `关闭记忆调试` / `debug memory off` | 退出调试模式 |

### 调试输出格式

```
[DEBUG RECALL]
当前任务：<一句话>
激活记忆：
  - mem_001 (score: 0.85) —— 理由：<为什么相关>
冲突预警：<若有则标注>
[/DEBUG RECALL]

---（正常回复）---

<正常回复内容...>

---（记忆操作日志）---

[DEBUG MEMORY_OP]
操作日志：
- [ADD] 新增: <内容> | <nature> | value=<v>
- [PROMOTE-SUBCONSCIOUS] 晋升: mem_008 →下意识层
下一轮召回上下文：{...}
[/DEBUG MEMORY_OP]
```

### 调试规则

- RECALL 块在回复前，MEMORY_OP 块在回复后
- 正常回复内容不受影响
- 无记忆变更时仍输出空 DEBUG 标签以确认流程执行
- 调试模式不改变记忆处理逻辑，仅改变可见性
- 敏感信息用 `<redacted>` 替代

---

## 十五、注意事项

- 记忆处理过程（RECALL / MEMORY_OP）始终内部进行，**不得**出现在回复正文中（调试模式除外）
- 若本轮无值得保留的新信息，MEMORY_OP 可为空，这是正常情况
- 记忆数量增长时优先召回 `impact = High` 的记忆
- 当记忆总数超过 100 条，触发压缩：合并同类、删除 forgotten、归纳同类情景为语义记忆
- `pending` 记忆在后续被用户再次确认时，执行 Correct 覆盖旧记忆
- Value 评估是思考周期的副产品，不单独成步，不增加额外模型调用
- Layer 2 写入以追加为主，批量 flush，避免频繁 I/O
- forgotten 记忆保留在 `_archive/`，供 Persona 蒸馏参考

---

## 十六、使用示例

**用户输入：** "上次部署漏了环境变量导致线上报错，以后部署前都要检查一遍。"

**阶段 A - 内部召回：**
```
[RECALL]
当前任务：记录部署教训，设定部署检查约束
激活记忆：
  - mem_005 (score: 0.78) —— 项目部署流程（procedural）
  - mem_008 (score: 0.65) —— 用户曾因配置问题踩坑（lesson）
冲突预警：无
[/RECALL]
```

**阶段 B - 正常回复：**
明白了，这是个重要教训。已记录，后续涉及部署操作时我会提醒你检查环境变量...

**阶段 C - 内部记忆操作：**
```
[MEMORY_OP]
当前任务：记录部署教训，设定部署检查约束
活跃记忆：mem_005（部署流程）、mem_008（历史踩坑）

操作日志：
- [ADD] 新增: "部署前必须检查环境变量" | lesson | Constraint | value=0.92 | High | Persistent
  （失败代价高，影响面=操作0.3→策略0.6，复用性高，获取成本不可逆）
- [STRENGTHEN] 强化: mem_008 (activation_count: 2→3) —— 同类教训再次出现
- [PROMOTE-SUBCONSCIOUS] 检查: mem_008 activation_count=3，未达阈值(5)，暂不晋升
- [FLUSH] 写入 Layer 2: 新记忆 (immediate, impact=High) → lessons/deploy_checklist.md

下一轮召回上下文：
{
  "constraints": ["check_env_vars_before_deploy"],
  "lessons": ["env_var_missing_caused_prod_error"]
}
[/MEMORY_OP]
```
