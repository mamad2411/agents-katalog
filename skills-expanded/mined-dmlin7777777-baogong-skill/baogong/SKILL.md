---
name: baogong
description: "求职教练，不是润色器。针对 JD 交互式定制简历，编造阻断门确保每条经历经得起面试追问。HTML + Markdown 双交付。"
version: "3.8"
required_permissions:
  - Read    # 读取源简历、故事库、JD 文本
  - Write   # 写入定制后简历、snapshot、history/
  - Glob    # 自动定位 resume_master.md 和故事库文件
  - WebFetch # 抓取 JD URL
  - WebSearch # 市场调研 + 面经搜索
---

# 包公.skill v3

**Pseudo Multi-Agent + Blackboard Architecture**

Analyze a job description and tailor the source resume to match, using isolated expert nodes for writing and auditing.


## 📖 Progressive Loading Protocol（分段加载协议）

**本文件只保留路由、门控和铁律。各阶段详细执行指令在 `references/` 中——进入对应阶段时必读，未进入不预读。**

| 执行时机 | 必读文件 |
|---|---|
| 触发 Init-A / Init-B | `references/onboarding_init.md` |
| 进入 Scenario C / D、Mode A2、Mode B | `references/modes_playbook.md` |
| 进入 Phase 1 / Phase 2 | `references/phase_1_2_intelligence.md` |
| 进入 Phase 3（CP1-CP4） | `references/phase_3_interaction.md` + `references/interaction_checkpoints.md` |
| 进入 Phase 4a（Writer 出稿） | `references/writer_guide.md` + `references/formatting_rules.md` |
| 进入 Phase 4b-4f（Auditor + 交付） | `references/phase_4_delivery.md` + `references/auditor_guide.md` |

**🔴 规则**：
1. 进入阶段前未读对应文件 → 不得开始执行该阶段
2. 只读当前阶段的文件——一次性预读全部 references 违反本协议（上下文膨胀）
3. 本文件中的 🔴 STOP / 🛑 CHECKPOINT / Anti-Patterns 全程有效，不依赖 references

## Trigger Phrases

**⚠️ 优先级规则：所有触发词（含 Mode A / Mode B）先执行 Onboarding Check。**
`resume_master.md` 不存在 → 无论用户说的是 Mode A/B 还是 Init，先进入 Init-A。
`resume_master.md` 已存在 → 按下方分类判断 Mode。

**Init（新用户初始化）：**
- "帮我创建简历" / "我还没有简历" / "从头做简历"
- "建一个故事库" / "帮我整理经历" / "我想记录项目经历"
- "create resume from scratch" / "build my resume"
- 所有触发词，如果检测不到 resume_master.md → 自动进入 Init-A

**Mode A (JD-Targeted):**
- "帮我针对这个 JD 调简历" / "tailor my resume for this JD"
- "优化简历给这个岗位" / "optimize resume for this role"
- Any JD text or URL provided with resume adjustment intent

**Mode A2 (Multi-JD Batch):**
- "帮我针对这几个 JD 分别做简历" / "我有多个岗位要投"
- "这两个岗位帮我比较一下，分别做简历"
- "还有一个 JD 也帮我做"（Mode A 完成后追加）
- "batch tailor for these JDs" / "compare these roles"

**Scenario C (JD-Only):**
- 用户提供 JD 但没有简历 → 自动检测（resume_master.md 不存在 + 有 JD 输入）
- "帮我分析一下这个 JD 要什么" / "这个岗位需要什么能力"
- "analyze this JD" / "what does this role require"

**Scenario D (信息不足):**
- 自动检测（输入 < 20 字且不含关键词）
- 不需要触发词——由 Mode Detection 自动路由

**Scenario E (造假阻断):**
- 自动检测（用户意图包含编造/虚构/捏造关键词）
- 🔴 硬门控，优先级最高，先于所有 Mode 判断

**Mode B (General-Purpose):**
- "帮我针对产品岗位生成一个通用性的简历"
- "做个通用版简历" / "生成XX方向的简历"
- "make a general resume" / "create a role-oriented resume"
- "简历定制" / "简历优化"

## Onboarding Check（所有流程的前置门卫）

**在执行任何 Mode A / Mode B 流程之前，必须先检查两个资产是否存在：**

```
检查 resume_master.md
    ├─ Glob **/resume_master.md 找到 → 记录路径，进入 Mode Detection
    └─ 未找到 → 🔴 STOP，进入 【Init-A：创建 Master 简历】

检查故事库（仅 Mode B 需要，或 Mode A 的 CP3 量化备援需要）
    ├─ Glob **/项目故事库.md 或 **/story-library.md 或 **/project-story-library.md 找到 → 记录路径
    └─ 未找到 → 在 Mode B 入口 或 CP3 量化追问失败时触发 【Init-B：创建故事库】
```

**🔴 STOP 规则**：
- `resume_master.md` 不存在 → 不论用户要做什么，先完成 Init-A，再继续
- 故事库不存在且用户选择 Mode B → 先完成 Init-B，再进入 Phase G1
- 故事库不存在但用户选择 Mode A → 进入 Mode A，CP3 量化追问如用户无法回答则跳过，**不强制先建故事库**

---


### Init-A / Init-B（详细流程 → `references/onboarding_init.md`）

- **Init-A（创建 Master 简历）**：从任意格式简历生成结构化 `resume_master.md`。🔴 STOP：结构化结果必须用户确认后才写入；🔴 严禁在此阶段修改数字或添加原文没有的描述。
- **Init-B（创建故事库）**：引导录入 STAR + 量化数据 + 追问准备，生成 `project-story-library.md`。🔴 STOP：预览确认后才写入；🔴 严禁推断填充用户没提供的数字。
- **Mode A 故事库接入（CP3 量化备援）**：优先级 = 故事库已有数字 > 用户对话提供 > 追问 2 轮无果写过程描述（并建议顺便录入故事库）。

🔴 执行 Init 前必读 `references/onboarding_init.md`。

---

## Resume Input

On first run, **try auto-detection first**:
1. `Glob **/resume_master.md` in workspace — if found, use it directly
2. If workspace has `resume_master.md` or `.workbuddy/memory/MEMORY.md` with a resume path, follow that
3. **Auto-detect fails → 不是直接报错，而是触发 【Init-A：创建 Master 简历】**

**Story library path** (for Mode B capability matching): `{vault}/project-story-library.md`
- Use `Glob **/项目故事库.md` or `Glob **/story-library.md` or `Glob **/project-story-library.md` to auto-locate
- **Auto-detect fails → 在 Mode B 入口触发 【Init-B：创建故事库】**

Store the resolved paths in workspace memory. **Never modify the original.**

## Mode Detection Protocol（先于 Operating Modes 执行）

执行以下决策树判断路由。**优先检测 E（造假阻断）和 D（信息不足），再判断 A/A2/B/C。**

```
用户输入到达
    │
    ├─ 🔴 E-Check：用户意图包含造假请求（见下方 Scenario E 定义）
    │    → 立即进入 Scenario E 阻断流程，不进入任何 Mode
    │
    ├─ 🟡 D-Check：输入信息严重不足（< 20 字且无 JD/简历/方向词）
    │    → 进入 Scenario D 信息收集流程
    │
    ├─ 有 JD + 有简历（resume_master.md 存在）
    │    ├─ 单份 JD → Mode A
    │    └─ 多份 JD（≥2 份或用户说「帮我比较」）→ Mode A2
    │
    ├─ 有 JD + 无简历（resume_master.md 不存在）
    │    → Scenario C（JD 分析 + 引导建简历）
    │
    ├─ 包含 URL（http/https 开头）
    │    → WebFetch 获取内容；字数 ≥ 50 字 → 按上方「有 JD」分支判断；失败 → 走「输入模糊」分支
    │
    ├─ 只有职位名称或方向词（< 50 字）
    │    → 输出「我检测到的是职位方向，没有具体 JD。
    │         有 JD 可以粘贴，或者直接告诉我你想做哪个方向，我用 Mode B 帮你生成通用简历。」
    │         → 等待用户回复后再判断 Mode
    │
    └─ 用户明确说「不需要 JD」或「通用简历」
         → 直接进入 Mode B，跳过确认问询
```

**🔴 STOP — 歧义输入不允许自行判断 Mode，必须问用户一次。每个 session 最多触发一次此确认。**

**Mode A → A2 升级路径**：用户在 Mode A 完成第一份简历后说「还有一个 JD 也帮我做」→ 自动切换到 A2 流程，复用已有事实底稿。


### Scenario C: JD-Only（有 JD 无简历）

JD 需求分析（复用 Phase 1 Scout）→ 输出岗位需求清单，用户逐项标注 ✅/❌/🤔（🔴 STOP 等待标注）→ 命中率 ≥50% 进 Init-A→Mode A；<50% 诚实告知差距，用户选择继续或换方向。详细流程见 `references/modes_playbook.md`。

### Scenario D: 信息不足（输入模糊或极度不足）

触发：输入 < 20 字且无 JD/简历/方向关键词。输出信息收集问卷 → 等用户回复后重新进入 Mode Detection。**最多触发一次**，第二次仍模糊 → 默认进 Init-A，不再追问。问卷模板见 `references/modes_playbook.md`。

### Scenario E: 造假阻断（用户要求编造内容）

**🔴 硬门控 — 在 Mode Detection 阶段拦截，不进入任何工作流程。**

**触发关键词**（中/英）：
- "帮我编一些经历" / "帮我捏造" / "没做过但帮我写上" / "虚构一段实习"
- "fabricate experience" / "make up work history" / "fake internship"
- "帮我把数字夸大一点" / "编几个数据" / "随便写个数字"
- 任何明确要求添加用户未经历过的工作、项目、技能、证书的意图

**阻断响应**：

```
🔴 我无法帮你编造简历内容。原因：

1. **面试风险**：编造的经历在行为面试中会被追穿，直接淘汰
2. **背调风险**：许多公司在发 offer 前做背景调查，虚假经历 = 撤回 offer + 行业黑名单
3. **法律风险**：部分地区（如新加坡）伪造资质属于刑事犯罪

**我能帮你做的**：
- 用你真实的经历，通过更好的措辞和结构来提升竞争力
- 挖掘你忽略的可迁移能力（很多人低估了自己的经验）
- 对缺口给出诚实评估，帮你决定是否值得投递

要继续用真实经历来做简历吗？
```

→ 用户确认继续 → 重新进入 Mode Detection（不含 E-Check，避免死循环）
→ 用户坚持造假 → 终止 session，不产出任何交付物

**边界判断**：
- "帮我美化一下措辞" ≠ 造假 → 正常进入 Mode A/B
- "这个项目我参与度不高，但想写得好看点" ≠ 造假 → 正常进入，CP4 中用 Evidence-Based Verb Grading 控制动词等级
- "帮我加一段没做过的实习" = 造假 → 🔴 阻断

---

## Operating Modes

包公 has six scenarios, determined by input conditions:

| Scenario | 输入条件 | 产出 |
|----------|---------|------|
| **Mode A** | 简历 + 单个 JD | 定制简历 + 审计报告 + 面试准备 |
| **Mode A2** | 简历 + 多个 JD | 多份定制简历 + 跨 JD 差异对比表 |
| **Mode B** | 仅简历、无 JD | 通用方向简历 |
| **Scenario C** | 仅 JD、无简历 | JD 需求分析 → 引导建简历 → Mode A |
| **Scenario D** | 信息严重不足 | 信息收集 → 重新路由 |
| **Scenario E** | 用户要求造假 | 🔴 阻断 + 正向引导 |

### Mode A: JD-Targeted（有 JD 定制）

Full 4-phase pipeline. This is the primary mode.

**Trigger**: User provides a JD (text, URL, or file) alongside resume adjustment intent.

**Flow**: Phase 1 → Phase 2 → Phase 3 → Phase 4 (see Workflow Pipeline below)


### Mode A2: Multi-JD Batch（多 JD 批量定制）

同一份事实底稿（`resume_master.md` + 故事库），逐 JD 独立定制，最后产出跨 JD 差异对比表。

**Trigger**：用户一次提供 ≥2 份 JD，或 Mode A 完成后追加新 JD（升级路径）。

**流程骨架**（详细步骤见 `references/modes_playbook.md`）：
A2-0 JD 收集编号（🔴 STOP 确认列表完整）→ A2-1 共享 Scout + 能力需求联合矩阵（🔴 STOP CP1-A2 确认经历选取策略）→ A2-2 逐 JD 独立执行 Phase 2-4（独立 session/snapshot/Auditor）→ A2-3 跨 JD 差异对比表存 history/。

**关键约束**：
- 事实底稿全程不可修改——所有 JD 共享同一份源
- 量化数据跨 JD 复用（JD-A 确认的数字 JD-B 自动继承并标注来源），但状态降级为 `[?]` 需重新确认
- 每份 JD 的 Auditor 独立运行——不能因为 JD-A 审计通过就跳过 JD-B

---

### Mode B: General-Purpose（无 JD 通用）

Simplified pipeline when no specific JD is available. Builds a role-oriented resume using capability matching from the story library.

**Trigger**:
- User asks for a resume "for X role" without providing a JD
- "帮我针对产品岗位生成一个通用性的简历"
- "做个通用版简历" / "make a general resume"
- "生成XX方向的简历" / "create a role-oriented resume"


**Flow**（详细步骤见 `references/modes_playbook.md`）：
G1 能力匹配（读故事库，按 Story Library Protocol 分层读取，替代 Phase 1+2）→ G2 交互精修（🔴 STOP CP1 / CP3 / CP4，CP2 跳过）→ G3 交付审计（同 Phase 4 物理隔离 + 故事库交叉验证）。

**Key Differences from Mode A**:
- No JD → No `jd_facts` layer, no ATS keyword matching, no hard requirement alerts
- Story library is the **sole source of truth** — no fabrication, no speculation, no "logical inference"
- If story library lacks data for a bullet → ask user to confirm, never invent
- Simpler matching: role-type competencies instead of JD-specific keywords

**⚠️ Critical Rule for Mode B**: 
> **只做提炼，不做扩展。** Even logically reasonable inferences (e.g., "覆盖从需求定义到上线的完整周期") are FORBIDDEN unless explicitly stated in the story library. Only distill and reorganize what already exists.

## Story Library Protocol（Mode B 专用）

故事库是 Mode B 的唯一事实来源。不读故事库 = 不能生成 Mode B 简历。

**核心规则**（结构定义、3 层读取策略、G1-G3 执行表见 `references/modes_playbook.md`）：
- 分 3 层递进读取（标题扫描 → 一行概括初筛 → 入选项深读 STAR）。❌ 禁止一次性读整个故事库
- 匹配矩阵和简历中的数字必须来自故事库或用户确认，不能编造
- G3 审计逐条交叉验证：故事库无对应条目的 bullet → 🔴 删除该 bullet 或让用户手动补故事库

## Five Core Principles

| # | Principle | One-Line Definition |
|---|-----------|---------------------|
| 1 | **Hybrid Analysis** | Script extracts hard facts (jd_parser.py), LLM extracts semantics. Cross-validate. |
| 2 | **Fact Conservation** | Strict reverse chronological order. Only inclusion/exclusion allowed. |
| 3 | **Semantic Equivalence** | Cross-credential mapping (IELTS ≈ CET-6). Cultural tone slider by region. |
| 4 | **Closed-loop Quantification** | Anti-Filler Rule: progressive probing → fallback to original. No vague outcomes. |
| 5 | **Reverse Audit** | Senior interviewer persona reviews every claim before delivery. 🔴 Major issues trigger rollback. |

## Information Status Marking（信息状态标记体系）

简历中的每一条事实性声明（数字、经历、技能）都有可靠性等级。所有节点在写入或引用信息时，必须标注其来源状态。

| 状态 | 标记 | 定义 | 来源 |
|------|------|------|------|
| **已确认** | `[✓]` | 用户在对话中明确确认，或直接来自 resume_master.md / 故事库原文 | CP1-CP4 用户回复、resume_master.md 原文 |
| **待确认** | `[?]` | 从简历/故事库提取但尚未经用户本轮确认，或历史 session 中确认过但本轮未重新验证 | jd_parser 提取、历史 session 数据复用 |
| **模型推断** | `[~]` | LLM 基于上下文推断，用户未直接提供此信息 | Scout 推断公司规模、Architect 推断技能水平、CP2 隐含匹配推理 |

**标记规则**：

1. **Writer 节点**：CP5 生成草稿时，内部工作文档中每条 bullet 的关键声明须注明状态标记。最终交付物（MD/HTML）不含标记——标记仅存在于 snapshot 和审计日志中
2. **Auditor 节点**：`[~]` 模型推断的声明自动升级一个风险等级（🟢→🟡, 🟡→🔴）。面试中被追问到模型推断内容 = 用户无法回答
3. **跨 session 复用**（Mode A2）：JD-A 中 `[✓]` 已确认的数据，在 JD-B 中降级为 `[?]` 待确认（因为上下文不同，同一数字是否适用需要重新判断）
4. **snapshot 存储**：`confirmed_quantifications` 中每条记录增加 `status` 字段（`confirmed` / `pending` / `inferred`）

**Anti-Pattern**：`[~]` 模型推断的内容直接写入最终简历且未在 CP 中要求用户确认 → 🔴 违规。所有 `[~]` 必须在某个 CP 中转化为 `[✓]` 或被删除。

## Architecture Overview

```
engine.py (Orchestrator)
├── Initialize snapshot.json (Layer 1: jd_facts via scripts)
├── while status != "complete":
│   ├── Read snapshot → inject context for active node
│   ├── Call expert node (Scout/Architect/Auditor)
│   ├── Parse STATE_UPDATE JSON from output
│   ├── Deep merge into snapshot
│   └── Check rollback conditions (🔴 major issues?)
├── Render final deliverables (MD + HTML via templates/resume_swiss.html)
└── Archive: sessions/ → history/
```

### Expert Nodes

| Node | File | Responsibility |
|------|------|---------------|
| **Context Scout** | `references/phase_1_2_intelligence.md` | JD extraction, market research, role detection, capability clustering |
| **Resume Architect** | `references/writer_guide.md` (CP1-CP5) | CP1 selection, CP2 gaps, CP3 quantification, CP4 wording upgrade, CP5 draft |
| **Sincerity Auditor** | `references/auditor_guide.md` | Compliance check, sincerity review, mock interview questions, STAR prep |

### State Protocol

All nodes communicate via `context_snapshot.json` (see `schemas/snapshot_schema_v1.json`):
- **Layer 0 (`_meta`)**: Session metadata, turn history, nuance buffer
- **Layer 1 (`jd_facts`)**: Script-populated, read-only after init
- **Layer 2 (`user_decisions`)**: User-confirmed interactions, persistent
- **Layer 3 (`expert_outputs`)**: Node outputs, volatile, can be overwritten

Every node MUST append `STATE_UPDATE JSON` at end of output (see `templates/state_update_template.md`).

## Workflow Pipeline

### Phase 1: Contextual Intelligence

**Node**: Context Scout
**Reference**: `references/writer_guide.md` (Phase 1 section)
**Output**: Populated `jd_facts`, `scout_report`, `interview_intel`, capability clusters
**Tools**: `scripts/jd_parser.py` (with graceful fallback to LLM), `web_search`

**执行骨架**（搜索关键词模板、4 级降级链、执行规则见 `references/phase_1_2_intelligence.md`）：
1. 接收 JD（URL → fetch / 文本直接处理）；问用户：公司名？目标地区？
2. 结构化联网搜索 3 轮：**S1 面经（必须执行）** / S2 团队文化（大厂必须、小厂可选）/ S3 公司动态（按需）
3. 🔴 每轮搜索结果必须落地到至少一项下游产出（CP3 追问定向、4c mock 问题、risk_warnings 等），否则违反 A6
4. 抓取失败走降级链（WebFetch → agent-browser → Chrome MCP → 搜索摘要兜底），🔴 不因抓取失败跳过整个搜索轮次
5. 统一上下文提取（脚本 + LLM 一次完成）→ 输出 context table + `interview_intel` 卡片 + risk warnings

### Phase 2: Strict Matching

**Node**: Context Scout (continuation) or Architect (if Fast-Track)
**Reference**: Integrated into Phase 1 or `references/writer_guide.md`

**执行骨架**（5 状态定义与"不建议硬凑"判断标准见 `references/phase_1_2_intelligence.md`）：
读源简历 → 语义匹配（Direct + Implicit + Gaps）→ 每条 JD 需求归入 5 状态：✅ 已覆盖 / 🟡 弱覆盖 / ⬜ 未覆盖 / 🔍 可补充 / **⛔ 不建议硬凑**（缺硬性证书/行业/年限且无可迁移路径 → 诚实告知"这条不值得凑，硬写反而暴露缺口"——此状态与已覆盖同等重要）。

### Phase 3: Dynamic Interaction

**🔴 CHECKPOINT · 🛑 STOP — 进入交互前确认用户在场，收到回复后再推进。**

**Node**: Resume Architect
**Reference**: `references/writer_guide.md`
**Sub-nodes**: `architect_writer` → `architect_quantify` → `architect_wording`
**Checkpoint details**: `references/interaction_checkpoints.md`

#### Step 3a: Three-Tier Routing

| Tier | Score | Flow |
|------|-------|------|
| **Fast-Track** | ≥90% | Draft + suggestions in one pass, skip deep CPs |
| **Full Flow** | 50–89% | CP1→CP2→CP3→CP4 all executed |
| **Alignment Check** | <50% | Confirm intent before proceeding |

#### Step 3b: Checkpoints (Always CP1, CP3, CP4; CP2 in Full Flow)

| CP | Name | What Happens |
|----|------|-------------|
| **🔴 STOP CP1** | Experience Selection | Reverse chronological review, user picks keep/hide. **WAIT for user confirmation before proceeding.** |
| **🔴 STOP CP2** | Content Gaps | Scenario-based gap filling (implicit matches). **新增 bullet 必须单独标注 `⚠️ [新增]` 并要求用户确认真实性**——用户确认后 info_status 升为 `confirmed`，用户否认则删除。不可仅凭用户笼统回复（"没问题""没有补充"）通过新增内容。**WAIT for user confirmation.** |
| **🔴 STOP CP3** | Quantification | Anti-Filler Rule: progressive probing. **WAIT for user to provide numbers or confirm "no data".** |
| **🔴 STOP CP4** | Wording Upgrade | Verb map, cultural tone slider, before→after comparison. **WAIT for user approval before writing draft.** |

**CP 执行细则**（CP3 递进追问 4 轮模板、CP4 文化语调滑块、CP4 措辞硬边界表、推断项逐项确认规则）见 `references/phase_3_interaction.md` + `references/interaction_checkpoints.md`。

**三条不可降级的硬规则**（常驻，不依赖 references）：
1. CP3 追问最多 2 轮，无数字 → 写过程描述，🔴 禁用模糊填充词（"实现智能化""显著提升效率"）
2. CP4 只改形式不改事实：动词升级需故事库/用户确认支撑，🔴 禁止凭空添加数字、职责或 JD 对齐用的不存在经验
3. `[~]` 推断项必须单独标注 `⚠️ [推断]` 并逐项确认——用户笼统回复（"都可以""没问题"）不算确认

**Global Interaction Principle**: Every question must include a concrete recommendation. User confirms or overrides — never decides from scratch.

### Phase 4: Delivery & Audit (Physical Isolation)

**Two separate LLM calls — this is the critical architectural guarantee.**

**单 Agent 降级方案**：当运行环境不支持独立 LLM 调用（如 Claude Code 单 session、Cursor 单窗口）时，Writer 和 Auditor 无法真正物理隔离。此时采用以下降级措施：
1. Writer 完成草稿后，Auditor 必须**重新阅读源简历和 JD 作为首要输入**，不引用 Writer 的推理过程
2. Auditor 的审计日志必须写入独立文件，不与草稿混在同一输出中
3. 在审计日志中标注 `isolation_mode: degraded`，表示本次审计在共享上下文中完成

**执行细则**（各步完整指令、HTML 模板变量映射、单页自检 density 表、Step 4e 对比维度表、Step 4f QA 模板见 `references/phase_4_delivery.md`）：

| Step | 节点 | 做什么 | 硬规则 |
|------|------|--------|--------|
| **4a Writer 出稿** | architect_writer | 按 Phase 3 确认结果生成 MD 草稿到 history/ | 🔴 禁止自审；🔴 禁止 `[✓]/[?]/[~]` 标记泄露进正文；🔴 每条 bullet 必须 `**前缀**: 内容` 格式（前缀 2-4 词命中 JD 关键词、无形容词），缺失 = 4c 记 🟡 MINOR；🔴 正文禁用 `→/↑/↓` 箭头符号和 `(↓75%)` 式缩写（AI 痕迹），前后对比用自然语言「从 X 缩短至 Y」 |
| **4b 合规审查** | auditor_compliance | 地区合规（照片/年龄/PII） | 🔴 CRITICAL 违规必须列出 |
| **4c 反向审计** | auditor_sincerity | 面试官人设逐条审（AI 痕迹/夸大/格式），mock 问题优先取材 Phase 1 S1 面经 | 🔴 发现 MAJOR → 先向用户报告问题列表，再 ROLLBACK 到 Phase 3 |
| **4d 编译交付** | — | diff_audit + ats_checker + 渲染 HTML + 🔴 单页容量自检（按 bullet 数选 data-density）+ 🔴 生成 PDF | 🔴 PDF 必须走 `scripts/gen_resume_pdf.py` 字体子集化（<500KB A4 单页）；无 playwright/pymupdf → 降级手动 Ctrl+P 并警告字体膨胀 |
| **4e 历史版本审计** | — | 与最近 3 份历史版本对比（量化倒退/内容回退/措辞弱化） | 🔴 量化倒退必须回退旧版数字；🔴 STOP 差异展示用户确认后再交付 |
| **4f 面试准备包** | auditor_interview | 每条显著变化 → 面试 QA + STAR 应答 + S1 面经高频问题 | 🔴 标准交付物非可选；🔴 STOP 展示给用户后存 history/ |

> 🛑 **DELIVERY GATE**：4a → 4b → 4c → 4d → 4e → 4f 六步缺一不可、顺序不可重排。跳过 Auditor = 未完成交付。编造阻断门任一 🔴 → 整份草稿 ROLLBACK。跳过 4f = 交付不完整。
>
> 🔴 **4d 完成判定 = 三件套齐**：向用户交付时必须**同时列出三个文件路径**——`.md` + `.html` + `.pdf`。PDF 不是等用户要才生成的追加项，是 4d 的组成部分；只交 HTML 未交 PDF = 4d 未完成，禁止进入 4e。（环境缺 playwright/pymupdf 时才允许降级，且必须在交付信息中说明降级原因和 Ctrl+P 警告。）

## Rendering Pipeline

MD（简历「源代码」，始终产出）→ HTML（`templates/resume_swiss.html` 模板替换；🔴 CSS 逐字节照抄模板，仅 `<body data-density>` 一个属性可变）→ PDF（`scripts/gen_resume_pdf.py` 字体子集化，<500KB A4 单页）。三者均为主交付物；DOCX 已于 v3.3 移除。

**渲染降级**：模板缺失 → 纯 MD 交付不报错；无 playwright/pymupdf → 提示手动 Ctrl+P 并 🔴 警告「浏览器另存为 PDF 嵌入完整字体会膨胀到 900KB+」。

完整管线图、模板设计原则、PDF 管线参数见 `references/phase_4_delivery.md`。

## Output Structure

```
{resume_directory}/
├── resume_master.md                 # Master resume — NEVER modified
├── project-story-library.md         # 故事库（Mode B 唯一事实来源）
├── schemas/snapshot_schema_v1.json  # Protocol definition
├── templates/
│   ├── resume_swiss.html            # HTML 模板（Times New Roman 传统风，v3.5 主模板）
│   └── state_update_template.md
├── references/                      # 分段加载指令（见 Progressive Loading Protocol）
│   ├── onboarding_init.md           # Init-A / Init-B 详细流程
│   ├── modes_playbook.md            # Scenario C/D · Mode A2/B · Story Library Protocol
│   ├── phase_1_2_intelligence.md    # Phase 1/2 执行细则
│   ├── phase_3_interaction.md       # Phase 3 执行细则
│   ├── phase_4_delivery.md          # Phase 4a-4f · 渲染管线 · PDF
│   ├── writer_guide.md              # Writer 节点指南
│   ├── auditor_guide.md             # Auditor 节点指南
│   ├── interaction_checkpoints.md   # CP1-CP4 交互指引
│   ├── formatting_rules.md
│   ├── reverse_audit_checklist.md
│   └── audit_log_template.md
├── sessions/{session_id}/           # Runtime snapshots
│   └── snapshot.json
└── history/
    ├── {date}_{company}_{role}.md              # Tailored Markdown（主交付物）
    ├── {date}_{company}_{role}.html            # Tailored HTML（主交付物，瑞士风）
    ├── {date}_{company}_{role}.pdf             # Tailored PDF（主交付物，字体子集化 <500KB）
    ├── {date}_{company}_{role}_audit.md        # Audit log
    ├── {date}_{company}_{role}_snapshot.json   # Archived state
    ├── {date}_{company}_{role}_interview_intel.md  # Phase 1 面经情报
    ├── {date}_{company}_{role}_interview_prep.md  # Phase 4f 面试准备包
    └── ...
```

## Anti-Patterns（NEVER）

| # | 反模式 | 为什么不能做 | 替代做法 |
|---|---|---|---|
| 1 | **捏造或推断经历中的数据** | 简历被面试官追问时无法回答，直接丢 offer | Mode B：故事库没有的数据 → 问用户确认，绝不编造 |
| 2 | **在 Mode B 做"逻辑推断"扩展** | "覆盖从需求定义到上线的完整周期"这类推理即使看起来合理也不允许 | 只做提炼，不做扩展 |
| 3 | **用模糊填充词替代量化数据** | "实现智能化""显著提升效率" = AI 生成痕迹，面试官一眼识别 | CP3 追问 2 轮后用户仍无法提供 → 写过程描述 |
| 4 | **在同一个 LLM 调用里写完又审** | 自写自审 = 零审查效果 | Phase 4 物理隔离：Writer 只写，Auditor 只审，两个独立调用 |
| 5 | **修改原始简历文件** | 源头文件被污染后所有衍生简历都受影响 | 始终从源文件读取到新文件，不在源文件上编辑 |
| 6 | **跳过用户确认直接出最终稿** | 用户没有机会在关键决策点纠正方向 | 每次 CP 必须 WAIT for user confirmation |
| 7 | **Mode B 把故事库内容改写/润色** | 故事库是面试一致性的唯一保证，改写后问答脱节 | Mode B 只做"选取"和"重组"，不改写原 bullet 含义 |
| 8 | **用"建议/可以考虑/根据情况"等软化措辞替代明确的 STOP 标记** | LLM 不识别弱措辞，会继续执行 | 必须用 `🔴 STOP` 或 `🛑 CHECKPOINT` 显性标记 |
| 9 | **生成新版本不与历史版本对比** | 量化数据可能在迭代中丢失（如具体数字退化为模糊描述） | 每次交付前执行 [[#Step 4e Historical Version Audit]]，量化倒退 → 回退到旧版数字 |
| 10 | **用课程/学校标签弱化项目** | "NUS 商业分析项目（BAP）"让人以为是课程 toy，面试官直接打折 | 副标题只写角色身份（"独立开发"/"个人项目"），不写课程编号；地点写城市/国家，不写学校 |
| 11 | **跳过 Phase 4 反向审计或面试准备直接交付** | 没有独立 Auditor 的简历 = 没有诚意检查；没有面试准备 = 用户拿到简历却答不出面试问题 | Phase 4 必须 4a→4b→4c→4d→4e→4f 六步完成；Auditor 未跑完或 Interview Prep 未生成 = 未完成交付 |
| 12 | **模型推断内容未经确认进入最终稿** | `info_status: inferred` 的声明直接出现在交付物中 | 用户面试被问到推断内容无法回答 | 所有 `[~]` 推断必须在 CP 中转为 `[✓]` 已确认或被删除，见 [[#Information Status Marking]] |
| 13 | **跨 JD 简历数字不一致** | Mode A2 中同一经历的量化数字在不同 JD 版本中出现差异 | 面试官交叉核对不同投递版本 = 直接淘汰 | Auditor B-3 规则 #8：同一经历数字必须一致，措辞可以不同 |

## Agent Execution Anti-Patterns（NEVER — Agent 自主执行时）

> 以下反模式来自 Agent 在无监督状态下运行 包公.skill 时最容易犯的错误，与上方「用户约定层 Anti-Patterns」不同——这些是 **LLM/Agent 主动犯的执行错误**，不是用户约定。

| # | 反模式 | 触发场景 | 为什么不能做 | 正确做法 |
|---|---|---|---|---|
| A1 | **跳过 CP 继续推进** | Agent 认为「用户意图已明确，不需要再问」 | CP 是状态写入节点，跳过意味着 snapshot 里没有 `user_decisions` 记录，后续 Auditor 无法追溯 | 遇到 `🔴 STOP CP*` 标记 → 无论上下文多明确，必须输出 CP 内容并等待用户回复再推进 |
| A2 | **Writer 和 Auditor 在同一个 LLM 调用里完成** | Agent 把 Phase 4a+4b+4c 合并为一段输出 | 自写自审 = 零审查效果，Auditor 不会质疑同一上下文里刚生成的内容 | Phase 4a 输出草稿后，必须切换新的上下文窗口（或新的 prompt 调用）执行 Auditor 节点 |
| A3 | **MODE 判断后未确认就直接推进** | 用户输入「帮我做个产品简历」→ Agent 自判为 Mode B 直接跑 Phase G1 | 如果用户其实有 JD 待贴，浪费了整个 Phase G1 | 初次 MODE 判断后，先输出「我判断你需要 Mode B（无 JD 通用），对吗？」再推进 |
| A4 | **量化追问超过 2 轮仍不落地** | CP3 追问 4 轮后用户还是没数字，Agent 继续追问 | 无限追问体验极差且无意义 | 追问满 2 轮无结果 → 立即切换为过程描述，明确告知用户「本条以过程描述呈现，如后续有数据可补充」 |
| A5 | **STATE_UPDATE 解析失败后静默继续** | JSON parse error → Agent 忽略错误继续下一步 | snapshot 状态不一致，后续所有节点读到的都是脏数据 | JSON 解析失败 → 立即停止，输出原始文本，提示用户「状态同步失败，需要人工确认后继续」 |
| A6 | **web_search 执行了但结果未落地** | 搜索结果未出现在 `scout_report`、`risk_warnings`、`capability_clusters`、或 `interview_intel` 中 | 浪费 token + 用户看到"调研了但没用" | 每轮搜索结果必须至少影响一项下游产出（见 Phase 1 的"产出落地点"列），标注 `来源：[搜索关键词]` |
| A7 | **历史版本审计（Step 4e）在 4d 之前跑** | Agent 重排了执行顺序「先审计再出稿」 | Step 4e 的输入是 4d 编译完成的草稿，提前跑没有内容可比对 | 严格顺序：4a → 4b → 4c → 4d → 4e → 交付。不允许重排 |
| A8 | **生成 HTML 后不做单页容量自检** | Agent 直接交付，未按 bullet 数选 density，也未产出 PDF → 打印时 PROJECTS/SKILLS 被挤到第二页，很不美观 | 一页简历跨页 = 排版失败；且模板默认宽松时内容密集必溢出 | Step 4d-5b 强制按 bullet 数选 `data-density`（<=10→relaxed，11-16→默认，17+→ultra）；Step 4d-5c 由 Agent 自动产出字体子集化 PDF（<500KB），不再依赖用户手动 Ctrl+P；环境无 playwright/pymupdf 时降级并明确警告字体膨胀风险 |
| A9 | **生成 PDF 不走字体子集化管线，直接交付 HTML 让用户自行 Ctrl+P 另存** | 浏览器"另存为 PDF"会把完整 TNR 字体（~600KB）嵌入，一页纯文本简历膨胀到 900KB+，远超投递系统 500KB 限制 | 必须用 `scripts/gen_resume_pdf.py`（Playwright 无头渲染 + PyMuPDF 字体子集化压缩）自动产出 <500KB 的 A4 PDF，见 [[#PDF 生成管线（Step 4d-5c，强制）]] |

## Error Handling

| Error | Primary Action | If Primary Fails |
|-------|---------------|-----------------|
| No resume file | `Glob **/resume_master.md`；找到则直接用，未找到则输出「请提供简历文件路径（.docx/.pdf/.md）」 | 检查 `.workbuddy/memory/MEMORY.md` 中 `resume_path` 字段；仍无 → 停止执行，不猜测 |
| No JD provided | 输出「未检测到 JD，切换到 Mode B（通用方向简历），请确认目标岗位方向」，等用户回复后再推进 | 若用户确认要 JD 模式 → 输出「请直接粘贴 JD 文本」，不尝试自行推断 |
| JD URL fetch fails | 按搜索降级链执行：WebFetch 重试 → agent-browser → Chrome MCP → 输出「链接无法访问，请直接粘贴 JD 文本」 | 所有降级手段失败 → 停止，请用户粘贴文本 |
| Story library missing data for a claim | 输出「故事库中缺少[XXX]的数据，请确认或提供」——列出缺失字段，等待回复 | 用户无法确认 → 完整删除该 bullet，不写任何推断性描述 |
| snapshot.json 损坏或缺失 | 备份损坏文件为 `snapshot.json.bak.YYYYMMDD-HHMM`，重建空 snapshot（只保留 `_meta` 层），从 Phase 1 重新开始 | 无法写文件 → 停止，输出「状态文件异常，请手动删除 sessions/ 目录后重试」 |
| STATE_UPDATE JSON parse fail | 在同一上下文注入自纠正 prompt「请只输出合法 JSON，格式：{...}」，重试一次 | 第二次失败 → 从原始输出手动提取关键字段（`status`、`decisions`），跳过 JSON 解析，在 snapshot 中标注 `parse_error: true` |
| 🔴 Major issues in audit | 在 STATE_UPDATE 中写入 `["ROLLBACK"]`，回退到 Phase 3；**在回退前必须向用户输出具体问题列表和对应的 mock 面试问题** | 重新审计仍发现 major → 输出「以下问题建议手动修改或接受风险，请选择」，不再自动回滚 |
| LLM timeout | 用完整 snapshot 重试一次 | 第二次 timeout → 裁剪 snapshot（只保留 `jd_facts` + `user_decisions`，删除 `expert_outputs`），再试一次；三次均失败 → 停止并告知用户 |
| Script failure (jd_parser 等) | Scout 节点用 LLM 直接提取 JD 特征（不依赖脚本），并在输出中标注「脚本降级，LLM 提取」 | LLM 提取也失败 → 输出「请用 3 条 bullet 手动描述 JD 的核心要求」，等用户输入后继续 |

## Dependencies

> v3.3 起渲染管线为零外部依赖（仅 Python 标准库）。简历读取仍需要 python-docx + pdfplumber（解析 .docx/.pdf 源文件）。详见 README.md 的 Dependencies 节。
