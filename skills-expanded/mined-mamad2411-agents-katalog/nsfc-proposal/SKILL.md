---
name: nsfc-proposal
description: Use when drafting, restructuring, or polishing Chinese NSFC proposals (2026 template), especially when strict section-by-section gating, hypothesis-objective-content-problem consistency, literature verification via paper-search MCP, and anti-AI Chinese academic writing constraints are required. 触发词：国自然、国家自然科学基金、基金申请书、科研申请、NSFC、标书、本子、面上项目、青年基金。
---

# NSFC Proposal Skill

## Overview
This skill manages end-to-end NSFC proposal writing and polishing under the 2026 structure. It enforces section-level gates, cross-section consistency, literature verification, and restrained academic Chinese style.

Use two modes:
- Write Mode: build from zero in phased gates.
- Polish Mode: import an existing draft, diagnose first, then revise section by section.

## Mode Handshake Gate (Mandatory)
Before any drafting/revision action, the assistant must ask exactly one mode-selection question and wait for the user answer:
- `Write Mode` (from scratch)
- `Polish Mode` (revise existing draft)

Hard rules:
- If mode is not explicitly confirmed, do not run section writing, diagnosis, citation verification, or merge commands.
- First actionable response in this skill must be the mode-selection question when mode is missing.
- If the user already explicitly states `Write Mode` or `Polish Mode` in the opening message, do not ask again; proceed directly with the specified mode.
- After user confirms mode, record it in project state/profile and continue with that mode workflow only.

## Core Terminology
SQ is the upstream root; H/O/RC/KSQ form the 1:1 consistency backbone derived from it.

| Symbol | Chinese | Role | Example |
|--------|---------|------|---------|
| SQ | 科学问题 (Scientific Question) | Field-level open problem distilled in P1; root for H and KSQ (not part of the 1:1 chain). SQ 不持有下行映射字段，关联由 H/KSQ 的 `mapped_from_sq` 反向建立 | "XXX的分子机制尚不清楚" |
| H | 假说 (Hypothesis) | Causal claim derived from SQ | "A蛋白通过B通路调控C过程" |
| O | 目标 (Objective) | What you **do** (action-oriented) | "阐明XXX的机制" |
| RC | 研究内容 (Research Content) | Specific investigation; links to methods | "通过ChIP-seq分析A蛋白的结合位点" |
| KSQ | 关键科学问题 (Key Scientific Question) | What you **answer** (question-oriented), distilled from SQ | "XXX如何调控YYY？" |

Mapping constraint: H-n ↔ O-n ↔ RC-n ↔ KSQ-n (strict one-to-one, no cross-linking allowed).
SQ vs KSQ: SQ is the broad open problem stated in P1; KSQ is the focused, answerable question distilled from SQ and bound 1:1 to its H/O/RC. One SQ may seed one or more KSQ; each SQ must trace to ≥1 H and ≥1 KSQ (rule V-01).

**If user asks a conceptual question about any of H/O/RC/KSQ/SQ/mapping:** load `references/02_核心机制.md` and answer from it before continuing with workflow phases.

## Inputs Required
Collect before execution:
- Project basics: title, discipline code, project type, research attribute, duration, budget.
- 🔴 **科学问题属性（四选一，强制）**：与"研究属性"是两个独立必填字段。研究属性=分类评审的「自由探索类/目标导向类」；科学问题属性=申请书独立必填项，四类官方标准措辞如下，Phase 0 必须选定其一并写入 profile 的 `science_problem_attribute`：
  - 鼓励探索、突出原创
  - 聚焦前沿、独辟蹊径
  - 需求牵引、突破瓶颈
  - 共性导向、交叉融通
- Existing materials: draft files, prior work, platform/conditions, related projects.
- User constraints: word targets per section, preferred P2 sub-structure, H/O/RC/KSQ mapping count.

### 2026模板硬约束速查表
| 项目 | 硬限 |
|------|------|
| 正文总页数 | ≤30页（约18000-25000字），页数估算替代字数硬门控 |
| 中文摘要 | ≤400汉字 |
| 英文摘要 | ≤300英文词 |
| P4 其他需要说明的情况 | ≤500字 |
| P3_4 完成基金项目情况总结 | ≤500字 |
| 研究属性（分类评审） | 必选「自由探索类」或「目标导向类」二选一 |
| 科学问题属性（独立必填，≠研究属性） | 四选一：鼓励探索·突出原创 / 聚焦前沿·独辟蹊径 / 需求牵引·突破瓶颈 / 共性导向·交叉融通；Phase 0 未选定则 gate-check 阻断（`failed_at=profile`） |
| 伦理审查（涉人类受试者/实验动物/生物安全/人类遗传资源时） | 须在可行性分析中说明伦理审查批件或送审计划 |

## Tooling Rules
Academic literature retrieval follows topic-dependent routing (Mandatory):

1. **Determine field type first:**
   - Life science / Medicine / Clinical / Biochemistry / Pharmacology → **PubMed CLI first**
   - CS / AI / Engineering / Physics / Interdisciplinary → **paper-search MCP first** (arXiv/Google Scholar)

2. **PubMed CLI** (life science primary): Use `esearch`/`efetch`/`einfo` (path `~/edirect/`). Must append `< /dev/null`, use proxy `http_proxy=http://127.0.0.1:<PROXY_PORT>`.
   Example: `export http_proxy=http://127.0.0.1:<PROXY_PORT> && esearch -db pubmed -query "xxx" < /dev/null | efetch -format abstract`
   Auto-install if `~/edirect/esearch` missing: `sh -c "$(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"`

3. **paper-search MCP** (CS/AI primary / preprints / fallback when PubMed yields no results):
   Tool names: `mcp__paper-search-mcp__search_pubmed`, `mcp__paper-search-mcp__search_arxiv`, `mcp__paper-search-mcp__search_biorxiv`, `mcp__paper-search-mcp__search_medrxiv`

Do not use generic web search/fetch tools for citation evidence in proposal claims.
**严禁** 使用 `tavily`、`websearch` 或 `openalex`（pyalex），无论有无 DOI/PMID. 该禁令已脚本级强制：literature_index 条目的 `search_source` 字段若属上述被禁家族，`citation_validator.py` 触发 `source_provider_forbidden` 硬失败，与 DOI/PMID/标题核验同级阻断门禁。
**Serial Search (MANDATORY):** Execute all retrieval calls sequentially (including both PubMed CLI and paper-search MCP). Never parallelize search requests. Enforce ≥1s interval between consecutive calls.

## Non-Conflict Canon (Conflict Resolution Rules)
> These rules resolve specific contradictions discovered during operation. When any instruction in SKILL.md or its references conflicts with a rule here, this section takes precedence.

Apply these resolutions when references conflict:
1. No-bullet narrative applies to proposal body sections only; diagnostics/review reports may use structured lists.
2. Interaction extras (reverse questioning, suggested follow-up questions, extended thinking) are optional by context, not mandatory on every response.
3. Merge order is fixed: references at the end of final merged manuscript.
4. P2 should not include numbered literature markers; citation numbering is restricted to P1.

(V-01 validation implementation note: SQ nodes carry no `mapped_to_h` field. Moved to `references/02_核心机制.md` §2.3.)

*Source: accumulated from operation feedback; last reviewed 2026-05.*

## Execution Workflow

### Write Mode
Follow phased gates in order:
1. Phase 0: initialize project profile, section targets, mapping cardinality.
   - 🔴 **必须选定「科学问题属性」四选一**（四类官方措辞见 Inputs Required 节），写入 profile `science_problem_attribute`。注意与「研究属性（自由探索类/目标导向类）」区分，二者是独立字段。未选定将在 Phase 7 `gate-check` 触发 `failed_at=profile` 阻断。

2. **Phase 0.5: 实验设计与技术路线结构化问询**（H/O/RC/KSQ mapping count 确定后、P1 撰写前的强制问询环节）
   - **触发时机**：Phase 0 完成 mapping count（RC 数量）确定 → Phase 0.5 → Phase 1。问询主体在主 agent 与用户对话，不写脚本。
   - **静默跳过禁令**：若主 agent 判断用户已在 Phase 0 自然语言中提供了实验设计细节、信息已充足，**不得静默跳过**，必须先用 ✓ 列表向用户回放当前已收集的设计信息（按下文 5 字段分类逐 RC 列出），并明确询问"是否需要补充或修正？是否同意以此为依据进入 Phase 1？"，用户显式确认后方可跳过追问环节，但仍须落盘 `data/experimental_design.json`。
   - **逐 RC 结构化追问（5 字段）**：对每个已立项的 RC（数量等于 Phase 0 mapping count），按顺序逐条追问：
     1. **实验/方法路径（methods）**：关键步骤、关键技术、关键试剂/仪器/动物模型或细胞系/样本来源。
     2. **预实验数据（preliminary_data）**：已有数据（图/表/统计数）vs 待补数据；已有数据说明出处（本课题组/合作单位/文献）。
     3. **可行性证据（feasibility）**：团队相关经验、依托平台/设备、合作单位、配套资金或前期项目支撑。
     4. **备选方案（alternative_plan）**：主路线失败时的触发条件、替代技术路线、切换代价（V-12 备选路线的实质内容，Phase 2 将直接复用）。
     5. **伦理审查（ethics）**：是否涉及人类受试者 / 实验动物 / 生物安全 / 人类遗传资源；任一涉及则说明审批状态（已获批号 / 已送审待批 / 计划送审时间节点）；均不涉及则填 "N/A 不涉及"。
   - **落盘**：把追问结果结构化写入 `data/experimental_design.json`，结构如下（每个 RC 一条 entry）：
     ```json
     {
       "metadata": {"schema_version": "1.0", "collected_at": "YYYY-MM-DDTHH:MM:SS+08:00"},
       "entries": [
         {
           "rc_id": "RC-1",
           "methods": ["步骤1：...", "步骤2：..."],
           "preliminary_data": "已有/待补 + 数据出处",
           "feasibility": "团队/平台/合作/资金证据",
           "alternative_plan": "触发条件 + 替代方案 + 切换代价",
           "ethics": "涉及类型 + 审批状态 / 或 N/A 不涉及"
         }
       ]
     }
     ```
   - **下游约束**：Phase 2 撰写 M（研究方案与技术路线）和 Phase 3 撰写 P3_1 可行性时，必须先 `Read data/experimental_design.json` 作为事实依据，禁止脑补；M.alternative_plan 字段（V-12 依赖）直接来自本 JSON 的 `alternative_plan` 字段。

   **Phase 0.5 DoD（收口自检）：未逐项确认通过，不得进入 Phase 1**

   - [ ] ①`data/experimental_design.json` 已生成，`entries` 数量等于 Phase 0 mapping count（每个 RC 一条）
   - [ ] ②每个 entry 的 `methods`、`feasibility`、`alternative_plan` 三个字段非空（不接受 "待定"/"TBD" 等占位符）
   - [ ] ③`preliminary_data` 字段明确区分了"已有"与"待补"，已有数据标注了出处
   - [ ] ④`ethics` 字段：涉及人/动物/生物安全/遗传资源任一情形者，已说明审批状态（含批号或送审计划时间节点）；均不涉及者填 "N/A 不涉及"
   - [ ] ⑤用户已显式确认 `experimental_design.json` 覆盖全部 RC、设计无遗漏（回放 ✓ 列表 + 用户书面同意）

3. Phase 1: write P1 with full citation pipeline and verification.
   - **🔴 开写前置闸门 (Mandatory，脚本硬拦截)**：开写前先跑 `python3 scripts/prewrite_gate.py --section P1 --root .`，exit≠0 禁止开写（硬检查上一节完成/`consistency_map` 就位/占位符清零；上一节盲检结果（`.review_pass/<上一节>.json`）缺失即 prewrite_gate 硬拦 exit 1，禁止开写；必须先跑 delegate_review verify --section <上一节> 落盘通过标记——仅跨 Phase 边界生效，同 Phase 子节 N/A）。P1 为首节，上一节检查自动放行。
   - 每节先跑 `python scripts/state_manager.py --root . write-cycle --section P1`（逐节预算/上下文注入的预写门控，完整参数见 references/08）；不得跳过直接硬写。
   - Input: confirmed project profile (title, discipline, H/O/RC/KSQ mapping counts).
   - Output: `sections/P1_立项依据.md` + `data/literature_index.json` (all P1 citations verified) + updated `context_memory.md`.
   **Citation Type by Context for P1 (立项依据，MANDATORY):** specific mechanistic/experimental claims (具体科学论点) must cite Original Articles as primary evidence; clinical evidence cites Clinical Trials at the same priority; preprints are last-resort, labeled `[Preprint]`, used only when no peer-reviewed equivalent exists. Full context-to-type mapping and the `role` taxonomy (gap_evidence / method_support / prior_work / comparison / background) live in `references/04_文献管理.md`.

   **Phase 1 DoD（收口自检）：未逐项确认通过，不得向用户声明 P1 完成**

   **🔴 进入下一部分前置闸口（适用所有 Phase）：本部分 delegate_review verify 必须 exit 0（含结构完整性），否则不得进入下一部分撰写。写完即检，不过不进。**

   **🔴 委托盲检（不得主 agent 自评）**：P1 自评易漏项、易默认通过。落盘前必须把 DoD 清单**委托给独立上下文的子代理盲检**，自己不直接打勾：
   1. 生成任务包：`python scripts/delegate_review.py pack --checklist references/dod_checklist.json --gate p1-dod --files sections/P1_立项依据.md`
   2. **派一个独立子代理**（Claude Code 用 `academic-blind-reviewer`；其他平台派通用子代理），把任务包原样给它、**不要给它 P1 的写作上下文**，要求按任务包返回 JSON 数组。
   3. 校验返回：`python scripts/delegate_review.py verify --checklist references/dod_checklist.json --gate p1-dod --return <子代理返回.json> --section P1 --root <项目根>`；退出码非 0（任一缺项/fail/无证据）= **fail-closed**，据子代理证据修复后重跑，**未过不得声明完成**。verify 通过会落盘 `.review_pass/P1.json`，下一部分 `prewrite_gate.py` 跨 Phase 时会**硬校验**它（缺失即拒绝开写）。
   - **降级路径**（当前环境无法派子代理时）：主 agent 切换审稿人视角、清空对 P1 的写作记忆，逐项独立重核，绝不因刚写完而默认通过；仍跑 `verify` 把关。

   下列清单与 `references/dod_checklist.json` gate=`p1-dod` 逐项对应（改清单先改 JSON），供人工对照；能脚本核的项子代理会先跑脚本：

   - [ ] ①引文 [n] ↔ REF 列表一一对应（无孤儿编号、无缺号、连续无断档）
   - [ ] ②本节新增引用已过 `citation_guard`（`python scripts/citation_validator.py verify-all`）
   - [ ] ③论述符合 SQ/H/KSQ 主线，未出现与 consistency_map 矛盾的表述
   - [ ] ④占位符清零（grep `CITE_PENDING\|DATA_PENDING\|【待` P1 返回空）
   - [ ] ⑤去 AI：`python scripts/humanizer_zh.py scan sections/P1_立项依据.md` 无 ERROR，WARNING 已逐条处理或标注豁免理由；`rhythm-check` 无 `cn_sentence_too_long`
   - [ ] ⑥字数在目标范围内（`python scripts/word_counter.py count sections/P1_立项依据.md`）
   - [ ] ⑦H/O/RC/KSQ 与 P1 中 SQ 表述一致（V-01；`python scripts/consistency_mapper.py --path data/consistency_map.json validate --rules V-01` 无 ERROR）
   - [ ] ⑧科学问题属性四选一已在 profile 中写入且与 P1 论述对应
   - [ ] ⑨撤稿检测：所有 PMID 已过撤稿核查（`python scripts/citation_validator.py verify-all --index data/literature_index.json --p1 sections/P1_立项依据.md`，撤稿检测已内置）

4. Phase 2: write P2 研究内容（contains all sub-content: H/O/RC/KSQ, methods, innovations, annual plan）.
   - **🔴 开写前置闸门 (Mandatory，脚本硬拦截)**：开写前先跑 `python3 scripts/prewrite_gate.py --section P2 --root .`，exit≠0 禁止开写（硬检查 P1 完成、`consistency_map` 就位、`data/experimental_design.json` entries 非空、占位符清零；P2←P1 跨 Phase，缺 `.review_pass/P1.json` 盲检标记即硬拦 exit 1，须先跑 `delegate_review verify --section P1` 落盘；P2 正是产出 M 的阶段，M 尚空只降级 warning）。
   - 每节先跑 `python scripts/state_manager.py --root . write-cycle --section P2`（逐节预算/上下文注入的预写门控，完整参数见 references/08）；不得跳过直接硬写。
   - **撰写 M（研究方案与技术路线）前必须 `Read data/experimental_design.json` 作为事实依据**，禁止脑补；每个 M 的 alternative_plan（V-12 字段）直接来自该 JSON 对应 RC 的 `alternative_plan`。
   - Input: verified P1; H/O/RC/KSQ mapping counts from Phase 0; consistency_map.json with SQ entries; `data/experimental_design.json` 全量 RC 设计。
   - consistency_map 条目结构（mapped_from_sq / mapped_to_objective / supports_method 等字段名）见 `references/02_核心机制.md` §2.2，按其字段名产出避免 validate 报错。
   - Output: `sections/P2_研究内容.md` + updated `data/consistency_map.json` (H→O→RC→KSQ→M→IN all links validated) + `sections/figure_prompts.md`.
   - **V 规则分层说明（机制级防假通过）：** Phase 2 门控统一用 `python scripts/consistency_mapper.py --path data/consistency_map.json validate --phase 2`，该参数只计算且只报 V-01/V-02/V-03/V-04/V-05/V-08/V-10（H/O/RC/KSQ/IN 结构链路），从机制上不输出 V-06/V-12 的结论，无需靠自觉跳读全量。V-06（M→F）、V-07（F来源）、V-09（预算追溯）、V-11（代表作匹配）依赖 F/预算字段，分别在 Phase 3/Phase 5 填齐后才有意义，强制点在 Phase 7 `gate-check`；V-12 只依赖 M 的 alternative_plan 字段，该字段在 Phase 3 Step 3.1 撰写，自 Phase 3 起进入 `--phase 3` 集合并为 ERROR 硬门控（gate-check 也会复验）。
   - Sub-content order: 研究假说(H) → 研究目标(O) → 研究内容(RC) → 关键科学问题(KSQ) → 研究方案与技术路线(M) → 特色与创新之处(IN) → 年度研究计划.
   - No literature numbers anywhere in P2. Paragraph narrative throughout; annual plan may use year-based paragraphs.
   - Every M must trace back to a specific RC; every IN must trace to RC and M.
   - **Figure Prompt Generation（AI绘图提示词）：** Phase 2 完成后，为技术路线图等必要图表生成绘图提示词，保存至 `sections/figure_prompts.md`。模板与生成规则见 `references/10_Figure_Prompt规范.md`。

   **Phase 2 DoD（收口自检）：未逐项确认通过，不得向用户声明 P2 完成**

   **🔴 委托盲检（不得主 agent 自评）**：落盘前委托独立子代理盲检：
   1. 生成任务包：`python scripts/delegate_review.py pack --checklist references/dod_checklist.json --gate p2-dod --files sections/P2_研究内容.md`
   2. 派独立子代理（Claude Code 用 `academic-blind-reviewer`），不给写作上下文，要求返回 JSON 数组。
   3. 校验：`python scripts/delegate_review.py verify --checklist references/dod_checklist.json --gate p2-dod --return <返回.json> --section P2 --root <项目根>`；非 0 = fail-closed，修复后重跑。verify 通过会落盘 `.review_pass/P2.json`，P3_1 开写时 `prewrite_gate.py` 会**硬校验**它。
   - **降级路径**：无法派子代理时，主 agent 切换审稿人视角逐项独立重核，仍跑 `verify`。

   下列清单与 `references/dod_checklist.json` gate=`p2-dod` 逐项对应（改清单先改 JSON）：

   - [ ] ①H/O/RC/KSQ 1:1 映射无交叉（`consistency_mapper validate --phase 2` V-01~V-05 全 PASS）
   - [ ] ②每个 M 可追溯到具体 RC，每个 IN 可追溯到 RC 和 M（`--phase 2` 输出中的 V-08/V-10）
   - [ ] ③P2 全文无文献编号引用 [n]（grep `\[[0-9]` P2 返回空）
   - [ ] ④占位符清零（CITE_PENDING/DATA_PENDING/【待AI】）
   - [ ] ⑤去 AI：`humanizer_zh.py scan` 无 ERROR，`rhythm-check` 无 `cn_sentence_too_long`
   - [ ] ⑥字数/页数在目标范围内
   - [ ] ⑦V-06（M→F）/V-07（F 来源）/V-09（预算追溯）/V-11（代表作匹配）依赖 F/预算字段，本阶段用 `validate --phase 2` 即不输出其结论，强制点在 Phase 7 gate-check；V-12（备选路线）只依赖 M.alternative_plan，自 Phase 3 起进入 `--phase 3` 集合为 ERROR 硬门控
   - [ ] ⑧P2 末尾含独立预期成果小节（论文/专利/人才培养目标三类均有明确数字目标）
   - [ ] ⑨figure_prompts.md 已生成，技术路线图提示词映射到 ≥1 个 RC

5. Phase 3: write P3 研究基础（4 sub-files）.
   - **🔴 开写前置闸门 (Mandatory，脚本硬拦截)**：每个子节开写前先跑 `python3 scripts/prewrite_gate.py --section P3_1 --root .`（其余子节同理 P3_2/P3_3/P3_4），exit≠0 禁止开写（硬检查上一节完成、`consistency_map` 含 M、占位符清零；P3_1 额外要求 `data/experimental_design.json` 非空；盲检按 Phase 粒度：P3_1←P2 跨 Phase，缺 `.review_pass/P2.json` 硬拦 exit 1；P3_2/P3_3/P3_4 同属 P3 一次性盲检，同 Phase N/A 不拦）。
   - 每节先跑 `python scripts/state_manager.py --root . write-cycle --section P3_1`（其余子节同理 P3_2/P3_3/P3_4；逐节预算/上下文注入的预写门控，完整参数见 references/08）；不得跳过直接硬写。
   - Input: P2 confirmed; team CV, platform data, and prior publications from Phase 0 profile.
   - Output:
     - `sections/P3_1_研究基础与可行性分析.md` (prior work + feasibility evidence per M + risk mitigation)
     - `sections/P3_2_工作条件.md` (equipment, facilities, missing conditions and remedies)
     - `sections/P3_3_正在承担的相关项目.md` (ongoing projects; explain overlap/difference from this project)
     - `sections/P3_4_完成基金项目情况.md` (completed grants summary ≤500字 + deliverables list)
   - Each M in consistency_map must have at least one feasibility entry (F) sourced from P3_1 or P3_2.
   - **伦理审查（涉人类受试者/实验动物/生物安全/人类遗传资源时为硬项）：** P3_1 可行性分析须说明已获或计划申请的伦理审查批件（如医学伦理委员会、实验动物福利伦理、生物安全审批、人类遗传资源采集/保藏/利用审批），尚未取得的注明送审计划与时间节点。不涉及上述情形则无需展开。
   - P3_3 and P3_4 may use list format (tables allowed).

   **Phase 3 DoD（收口自检）：未逐项确认通过，不得向用户声明 P3 完成**

   **🔴 委托盲检（不得主 agent 自评）**：落盘前委托独立子代理盲检：
   1. 生成任务包：`python scripts/delegate_review.py pack --checklist references/dod_checklist.json --gate p3-dod --files sections/P3_1_研究基础与可行性分析.md sections/P3_2_工作条件.md sections/P3_3_正在承担的相关项目.md sections/P3_4_完成基金项目情况.md`
   2. 派独立子代理（Claude Code 用 `academic-blind-reviewer`），不给写作上下文，要求返回 JSON 数组。
   3. 校验：`python scripts/delegate_review.py verify --checklist references/dod_checklist.json --gate p3-dod --return <返回.json> --section P3_1 --root <项目根>`；非 0 = fail-closed。verify 通过会落盘 `.review_pass/P3_1.json`（代表 P3 整体盲检；P3_2/P3_3/P3_4 同 Phase 内不单独硬校验）。
   - **降级路径**：同 Phase 1。

   下列清单与 `references/dod_checklist.json` gate=`p3-dod` 逐项对应（改清单先改 JSON）：

   - [ ] ①四个子文件均已生成（P3_1/P3_2/P3_3/P3_4）
   - [ ] ②consistency_map 中每个 M 至少有一条 F（可行性条目）来自 P3_1 或 P3_2
   - [ ] ③P3_4 总结字数 ≤500 字（`word_counter` 核验）
   - [ ] ④涉及人类受试者/动物/生物安全/遗传资源时，P3_1 含伦理审查说明或送审计划
   - [ ] ⑤占位符清零
   - [ ] ⑥去 AI：P3_1/P3_2 已过 `humanizer_zh.py scan`，无 ERROR；`rhythm-check` 无 `cn_sentence_too_long`
   - [ ] ⑦H/O/RC/KSQ 与 P1/P2 一致性未因 P3 新增内容产生新矛盾，且 V-12 备选路线已就位（`consistency_mapper validate --phase 3` 仍 PASS）
   - [ ] ⑧代表作与 H/RC 方向匹配（V-11 人工确认：每篇代表作能对应至少一条 H 或 RC）

6. Phase 4: write P4 其他需要说明的情况（≤500字）.
   - 每节先跑 `python scripts/state_manager.py --root . write-cycle --section P4`（逐节预算/上下文注入的预写门控，完整参数见 references/08）；不得跳过直接硬写。
   - Input: P3 confirmed.
   - Output: `sections/P4_其他需要说明的情况.md`.
   - Cover: concurrent grant applications, senior PI prior grants, postdoc status, AI usage declaration, ethics/biosafety/human-genetic-resource approvals (若涉及，与 P3_1 伦理说明呼应), any other required disclosures.

   **Phase 4 DoD（收口自检）：未逐项确认通过，不得向用户声明 P4 完成**

   **🔴 委托盲检（不得主 agent 自评）**：落盘前委托独立子代理盲检：
   1. 生成任务包：`python scripts/delegate_review.py pack --checklist references/dod_checklist.json --gate p4-dod --files sections/P4_其他需要说明的情况.md`
   2. 派独立子代理（Claude Code 用 `academic-blind-reviewer`），不给写作上下文，要求返回 JSON 数组。
   3. 校验：`python scripts/delegate_review.py verify --checklist references/dod_checklist.json --gate p4-dod --return <返回.json>`；非 0 = fail-closed。
   - **降级路径**：同 Phase 1。

   下列清单与 `references/dod_checklist.json` gate=`p4-dod` 逐项对应（改清单先改 JSON）：

   - [ ] ①总字数 ≤500 字（`word_counter` 核验）
   - [ ] ②涉及伦理/生物安全/遗传资源的说明与 P3_1 无矛盾（人工核查呼应关系）
   - [ ] ③AI 使用声明已包含（若使用了 AI 辅助写作）
   - [ ] ④占位符清零
   - [ ] ⑤去 AI：`humanizer_zh.py scan` 无 ERROR；`rhythm-check` 无 `cn_sentence_too_long`

7. Phase 5: write 预算说明书（B1-B3）.
   - Input: P2 confirmed (M entries define budget items); project profile (budget_total, duration).
   - Output:
     - `sections/B1_预算说明_直接费用.md` (equipment; materials; tests; travel/conference; publications; labor; consulting; three-line tables where required)
     - `sections/B2_预算说明_合作外拨.md` (co-institution allocation, or "无")
     - `sections/B3_预算说明_其他来源.md` (other funding sources)
   - Budget total must equal profile `budget_total`; each major budget item traces to an M entry.

   **Phase 5 DoD（收口自检）：未逐项确认通过，不得向用户声明 P5/预算完成**

   **🔴 委托盲检（不得主 agent 自评）**：落盘前委托独立子代理盲检：
   1. 生成任务包：`python scripts/delegate_review.py pack --checklist references/dod_checklist.json --gate p5-dod --files sections/B1_预算说明_直接费用.md sections/B2_预算说明_合作外拨.md sections/B3_预算说明_其他来源.md`
   2. 派独立子代理（Claude Code 用 `academic-blind-reviewer`），不给写作上下文，要求返回 JSON 数组。
   3. 校验：`python scripts/delegate_review.py verify --checklist references/dod_checklist.json --gate p5-dod --return <返回.json>`；非 0 = fail-closed。
   - **降级路径**：同 Phase 1。

   下列清单与 `references/dod_checklist.json` gate=`p5-dod` 逐项对应（改清单先改 JSON）：

   - [ ] ①三个子文件均已生成（B1/B2/B3）
   - [ ] ②各项目预算求和 = profile `budget_total`（人工核算）
   - [ ] ③每个主要预算条目可追溯到至少一条 M 条目（V-09 人工确认）
   - [ ] ④直接费用各类别说明完整（设备/材料/测试/差旅/出版/劳务/咨询）
   - [ ] ⑤占位符清零

8. Phase 6: write 中英文摘要（abstract-last, based on full draft）.
   - Input: all sections P1–P4 confirmed; run `python scripts/state_manager.py --root . load --global` for full-text summary.
   - Output: `sections/00_摘要_中文.md` (≤400汉字) + `sections/00_摘要_英文.md` (≤300英文词).
   - Keywords must align with `consistency_map.keywords_trace`.

   **Phase 6 DoD（收口自检）：未逐项确认通过，不得向用户声明摘要完成**

   **🔴 委托盲检（不得主 agent 自评）**：落盘前委托独立子代理盲检：
   1. 生成任务包：`python scripts/delegate_review.py pack --checklist references/dod_checklist.json --gate p6-dod --files sections/00_摘要_中文.md sections/00_摘要_英文.md`
   2. 派独立子代理（Claude Code 用 `academic-blind-reviewer`），不给写作上下文，要求返回 JSON 数组。
   3. 校验：`python scripts/delegate_review.py verify --checklist references/dod_checklist.json --gate p6-dod --return <返回.json>`；非 0 = fail-closed。
   - **降级路径**：同 Phase 1。

   下列清单与 `references/dod_checklist.json` gate=`p6-dod` 逐项对应（改清单先改 JSON）：

   - [ ] ①中文摘要 ≤400 汉字（`word_counter` 核验）
   - [ ] ②英文摘要 ≤300 英文词（`word_counter` 核验）
   - [ ] ③摘要关键词与 `consistency_map.keywords_trace` 吻合（人工核查）
   - [ ] ④摘要中的 H/O/RC/KSQ 表述与正文各 Phase 一致（V-01~V-05 范围内，人工核查）
   - [ ] ⑤占位符清零
   - [ ] ⑥去 AI：`humanizer_zh.py scan sections/00_摘要_中文.md` 无 ERROR；`rhythm-check` 无 `cn_sentence_too_long`

9. Phase 7: 全文自审与终稿 + merge.
   - Input: all sections (00, B1-B3, P1-P4, REF) confirmed.
   - Run `diagnosis_engine.py full-review` and `consistency_mapper.py validate` (完整参数见 Script Entry Points); fix all ERROR-level issues.
   - Run `python scripts/word_counter.py summary sections` and `python scripts/state_manager.py --root . page-estimate --sections-dir sections`; if >30 pages, trim specific locations.
   - Run `humanizer_zh.py scan-all` before final output.
   - Output: `output/申请书_合并.md` (merge order: 00摘要 → B1-B3预算 → P1 → P2 → P3_1~P3_4 → P4 → REF).

   **Phase 7 DoD（收口自检）：未逐项确认通过，不得向用户声明全文终稿完成**

   **🔴 委托盲检（不得主 agent 自评）**：merge 前委托独立子代理盲检：
   1. 生成任务包：`python scripts/delegate_review.py pack --checklist references/dod_checklist.json --gate p7-dod --files sections/P1_立项依据.md sections/P2_研究内容.md sections/P3_1_研究基础与可行性分析.md sections/P4_其他需要说明的情况.md sections/00_摘要_中文.md`
   2. 派独立子代理（Claude Code 用 `academic-blind-reviewer`），不给写作上下文，要求返回 JSON 数组。
   3. 校验：`python scripts/delegate_review.py verify --checklist references/dod_checklist.json --gate p7-dod --return <返回.json>`；非 0 = fail-closed，**未过不得声明完成、不得 merge**。
   - **降级路径**：同 Phase 1。

   下列清单与 `references/dod_checklist.json` gate=`p7-dod` 逐项对应（改清单先改 JSON）：

   - [ ] ①`diagnosis_engine.py full-review` 无 ERROR 级问题
   - [ ] ②`consistency_mapper.py validate` V-01~V-12 全量验证 PASS（V-06/V-07/V-09/V-11/V-12 首次强制执行）
   - [ ] ③`gate-check --require-mcp` PASS（引文矩阵 / MCP 缓存 / 撤稿检测 / 科学问题属性）
   - [ ] ④页数 ≤30 页（`page-estimate` 核验；超出则已按报告定位修剪）
   - [ ] ⑤`humanizer_zh.py scan-all` 无 ERROR，WARNING 已逐条处理或标注豁免理由；无 `cn_sentence_too_long`
   - [ ] ⑥全文占位符清零（CITE_PENDING/DATA_PENDING/【待AI】/【待翻译】）
   - [ ] ⑦V-11 代表作：每篇代表作能对应 ≥1 条 H 或 RC（`consistency_mapper validate` + 人工确认）
   - [ ] ⑧V-12 备选路线：每条主研究路线（M）含 ≥1 条备选方案或风险应对措施
   - [ ] ⑨合并顺序正确（00摘要 → B1-B3 → P1 → P2 → P3_1~P3_4 → P4 → REF），输出文件存在且可读

At each phase:
- snapshot
- sync required state files
- halt for user confirmation

### Polish Mode
1. Import draft and split into atomic section files by original heading hierarchy.
   - Fallback: if heading hierarchy is ambiguous or absent, present detected section list to user for manual confirmation before splitting.
2. Generate strict review report first (`polish_review_report`).
   - Fallback: if `diagnosis_engine.py` fails, output a manual checklist covering: consistency / citation / writing style / format/length dimensions.
3. Agree priority with user (rewrite vs polish vs keep).
   - **Hard block:** do not proceed to step 4 until user explicitly confirms priority order per section or sets a global default. Accept responses like "rewrite P1, polish P2, keep P3".
4. Revise section by section following issue order:
   - academic design/hypothesis
   - consistency
   - writing style
   - format/length
5. Run global consistency repair and full review.
6. Merge final output.

## State and Artifacts
Maintain and sync after each section edit:
- `data/consistency_map.json`
- `data/literature_index.json`
- `data/mcp_literature_cache.json`
- `data/manual_review_queue.json`
- `context_memory.md`
- `project_state.json`
- `history_log.json`

Any missing sync blocks phase progression.

**State Corruption Fallback:** If any required state file is missing or unparseable (JSON decode error), run `python scripts/state_manager.py --root . sync-all --auto-fix` to restore defaults. (`init --repair` does not exist; `sync-all --auto-fix` is the correct repair command.) Do not proceed without valid state files.

### Mandatory Field Contracts (Hidden Trip-Wires)

The following fields are silently required by scripts. Missing them causes hard failures that are **not** obvious from error messages alone.

**`data/mcp_literature_cache.json` — MCP 缓存条目必填字段：**

每条缓存记录必须包含时间戳字段 `verified_at` 或 `checked_at`（二选一即可，`_is_mcp_fresh` 按此顺序查找）。使用 `retrieved_at` 或其他名称时脚本视为时间戳缺失，触发 `mcp_timestamp_missing` 硬失败。

最小合规样例：
```json
{
  "metadata": {"schema_version": "1.0"},
  "entries": [
    {
      "doi": "10.1234/example",
      "pmid": "12345678",
      "title": "Example Paper Title",
      "verified_at": "2026-06-01T12:00:00+00:00"
    }
  ]
}
```

**`data/literature_index.json` — 文献索引条目必填字段：**

凡 `"P1_立项依据"` 在 `used_in_sections` 中的条目，若 `key_finding` 字段为空或缺失，`_context_check` 直接返回 `False`，触发 `context_mismatch` 软失败并降低 `confidence_score`。

最小合规条目：
```json
{
  "ref_number": 1,
  "title": "Example Paper Title",
  "doi": "10.1234/example",
  "pmid": "12345678",
  "used_in_sections": ["P1_立项依据"],
  "key_finding": "该研究发现X蛋白通过Y通路调控Z过程（主要数据点）",
  "is_recent_5yr": true,
  "is_cn_journal": false
}
```

字段名速查：
| 字段 | 所在文件 | 若错用 | 触发失败类型 |
|------|---------|--------|------------|
| `verified_at` 或 `checked_at` | mcp_literature_cache.json 每条记录 | 写成 `retrieved_at` | `mcp_timestamp_missing`（HARD） |
| `key_finding` | literature_index.json 每条 P1 引用条目 | 字段为空/缺失 | `context_mismatch`（SOFT） |
| `search_source` | literature_index.json 每条 | 填 `tavily`/`websearch`/`openalex`/`pyalex` | `source_provider_forbidden`（HARD） |

## Quality Gates
Block progression when any of the following fails:
- ERROR-level consistency rules.
- Unverified references in P1 citation set.
- Citation-index-reference matrix mismatch.
- Any D-grade in global review dimensions.
- More than 3 C-grade dimensions in global review.
- Page estimate beyond configured hard limit.

Use atomic gate command for final checks:
- `python scripts/state_manager.py --root . gate-check --sections-dir sections --index data/literature_index.json --p1 sections/P1_立项依据.md --ref sections/REF_参考文献.md --mcp-cache data/mcp_literature_cache.json --mcp-ttl-days 30 --require-mcp`

### ❌ 反例黑名单（Anti-Patterns，门控人读版总览）

- ❌ 把「科学问题属性」当成「研究属性」填，或四类官方措辞（鼓励探索·突出原创／聚焦前沿·独辟蹊径／需求牵引·突破瓶颈／共性导向·交叉融通）未在 Phase 0 选定写入 profile，会触发 gate-check `failed_at=profile` 阻断。
- ❌ 跳过 Mode Handshake，未确认 Write Mode 或 Polish Mode 就直接开写、做诊断或跑文献核验。
- ❌ H/O/RC/KSQ 不做严格 1:1 对应，出现交叉映射、数量不等或某个 SQ 没有对应的 H 与 KSQ（违反 V-01／V-02）。
- ❌ 把研究目标写成问题、把关键科学问题写成动作，混淆“做什么”（O）与“回答什么”（KSQ）。
- ❌ 创新点写成空话（“首次系统研究”“开创性”“革命性”），不追溯到具体 RC 和 M，无技术／方法／理论突破的实证（违反 V-05／FC-05）。
- ❌ 给每个 M 留空 alternative_plan，或备选方案只写“调整参数”而无触发条件／替代方案／切换代价（违反 V-12，阻断 Phase 3）。
- ❌ 可行性靠自夸撑场，每个方法 M 找不到来自 P3_1／P3_2 的可行性证据 F，预实验或代表作与 H/RC 方向对不上（违反 V-06／V-11）。
- ❌ 虚构或不核验引用，PMID／DOI／标题不反查、跳过撤稿检查，或带着 `verified=false` 的文献进入 Phase 2。
- ❌ 用 tavily、websearch、openalex／pyalex、webfetch 等通用工具检索文献证据，而非 PubMed CLI 或 paper-search MCP。
- ❌ 并行发起检索请求，未串行执行、未保证连续调用间隔 ≥1 秒。
- ❌ 在 P2 研究内容里使用文献编号引用 [n]，或把编号引用用在 P1 之外的部分。
- ❌ 正文用项目符号或编号列表展开论述，而非段落式叙事（年度计划、P3_3／P3_4 清单、预算三线表是仅有的例外）。
- ❌ 使用禁用句式与修辞：“不是…而是…”“不仅…而且…”“值得注意的是”“至关重要”“综上所述”、排比、比喻、反问、夸张。
- ❌ 留下装饰性破折号、scare quotes、解释性冒号，或中文单句超 50 字、定语从句嵌套超 2 层（humanizer_zh／rhythm-check 报错）。
- ❌ 超篇幅：正文 >30 页、中文摘要 >400 字、英文摘要 >300 词、P4 或 P3_4 >500 字。
- ❌ 在任一 Phase 不跑委托盲检（或降级独立重核），主 agent 写完就自评打勾、verify 未 exit 0 就声明完成或执行 merge。

Failure handling playbook:
- `failed_at=profile`: 科学问题属性未选定或取值非四类官方措辞之一。回到 Phase 0 与用户确认四选一，写入 profile `science_problem_attribute`（`python scripts/state_manager.py --root . profile --json '{"science_problem_attribute":"聚焦前沿、独辟蹊径"}'`），再 re-run `gate-check`。
- `failed_at=sync`: run `sync-all --auto-fix`, then re-run `gate-check`.
- `failed_at=citation`: repair index/cache, re-run `verify-all --require-mcp`, then `gate-check`.
- `failed_at=matrix`: run `matrix-check` and `reorder`, then `gate-check`.
- `failed_at=review`: fix D/C dimensions from review report, then `gate-check`.

**Dual-Track Citation Verification:** Provide MCP retrieval cache in `data/mcp_literature_cache.json` and run online validation without `--offline` whenever network is available. Final gate must enforce `--require-mcp`.

## References
Load only what is needed:
- `references/00_设计方案_总览.md`
- `references/01_目录结构与配置.md`
- `references/02_核心机制.md`
- `references/03_写作规范与反AI.md`
- `references/04_文献管理.md`
- `references/05_Write_Mode流程.md`
- `references/06_Polish_Mode流程.md`
- `references/07_自审与评审模块.md`
- `references/08_脚本清单与合并规则.md`
- `references/09_交互规范与回复模板.md`
- `references/10_Figure_Prompt规范.md`

## Output Contract
Deliverables should include:
- section files under `sections/` (canonical filenames):
  `P1_立项依据.md`, `P2_研究内容.md`（含独立预期成果小节：论文/专利/人才培养目标），
  `P3_1_研究基础与可行性分析.md`, `P3_2_工作条件.md`, `P3_3_正在承担的相关项目.md`, `P3_4_完成基金项目情况.md`,
  `P4_其他需要说明的情况.md`,
  `B1_预算说明_直接费用.md`, `B2_预算说明_合作外拨.md`, `B3_预算说明_其他来源.md`,
  `00_摘要_中文.md`, `00_摘要_英文.md`, `REF_参考文献.md`
- updated state and data files
- review reports in `data/`
- merged manuscript in `output/` (md/docx if requested)

When reporting to user, state:
- what was changed
- which gate passed/failed
- what is blocked and exact unblock action

## Script Entry Points
正文仅保留5条最常用核心命令；write-cycle 各节 token 预算、verify-entry / matrix-check / validate-one / polish-review / validate-order / 阶段稿 merge / word_counter 等完整调用与子命令清单见 `references/08_脚本清单与合并规则.md`。

- init: `python scripts/state_manager.py --root . init`
- sync-all (repair): `python scripts/state_manager.py --root . sync-all --auto-fix`
- gate-check (full, requires MCP): `python scripts/state_manager.py --root . gate-check --sections-dir sections --index data/literature_index.json --p1 sections/P1_立项依据.md --ref sections/REF_参考文献.md --mcp-cache data/mcp_literature_cache.json --mcp-ttl-days 30 --require-mcp`
- merge: `python scripts/section_merger.py merge --sections-dir sections --output output/申请书_合并.md`
- full-review: `python scripts/diagnosis_engine.py full-review --sections-dir sections --consistency data/consistency_map.json --index data/literature_index.json --p1 sections/P1_立项依据.md --ref sections/REF_参考文献.md --output data/diagnosis_report.json`

Phase 7 引用的 `consistency_mapper.py validate` 完整形式：`python scripts/consistency_mapper.py --path data/consistency_map.json validate`。
其余脚本（write-cycle 逐节预算、citation_validator verify-all/verify-entry/matrix-check、humanizer_zh scan-all、load 变体、word_counter summary）为生产级工作流工具，完整 flag 见 references/08。


## Regression Tests
`tests/` directory not yet built. Unit test suite is planned but not implemented.
`test-prompts.json` 仅验证触发与门禁交互，脚本逻辑需人工抽查。

---

## Figure Prompt 触发规则
- 技术路线图：Phase 2 必须生成；研究框架图：Phase 1 推荐生成；预期结果用占位符 `[Preliminary Data Fig N]`。
- 统一色板（深蓝=主线索，绿色=创新点，橙色=预期产出），每张图须映射到 consistency_map 中至少一个 RC。
- 完整提示词模板与生成规则见 `references/10_Figure_Prompt规范.md`。
