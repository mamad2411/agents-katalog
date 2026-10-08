---
name: FBS-BookWriter
version: 2.1.0
plugin-id: fbs-bookwriter-v210
description: "福帮手出品 | 高质量长文档手稿工具链：书籍、手册、白皮书、行业指南、长篇报道、深度专题；支持联网查证（宿主允许时启用，离线自动降级）、S/P/C/B 分层审校、中文排版与 MD/HTML 交付。触发词：福帮手、福帮手写书skill、福帮手写书、写书、出书、写长篇、写手册、写白皮书、写行业指南、协作写书、定大纲、写章节、封面、插图、排版构建、导出、去AI味、质量自检、图文书、写报道、写深度稿、写特稿、写专题、写调查报道、写长文、激活原料、原料盘点、整理素材"
description_zh: "福帮手出品 | 高质量长文档手稿工具链：书籍、手册、白皮书、行业指南、长篇报道、深度专题；支持联网查证（宿主允许时启用，离线自动降级）、S/P/C/B 分层审校、中文排版与 MD/HTML 交付。触发词：福帮手、福帮手写书skill、福帮手写书、写书、出书、写长篇、写手册、写白皮书、写行业指南、协作写书、定大纲、写章节、封面、插图、排版构建、导出、去AI味、质量自检、图文书、写报道、写深度稿、写特稿、写专题、写调查报道、写长文、激活原料、原料盘点、整理素材"
description_en: "Dual-channel long-form writing workflow for books, manuals, whitepapers, guides and reports with layered QC and offline fallback."

allowed-tools:
  - bash
  - filesystem.read
  - filesystem.write
  - web_search
user-invocable: true
scene-packs: [general, genealogy, consultant, ghostwriter, training, personal-book, whitepaper, report]
# general 为 builtin，随技能分发、默认可用；其余 7 个增强场景需在线校验/授权后启用
ui-actions: true

---

# 福帮手出品 | 高质量长文档手稿工具链（FBS-BookWriter）

> **版本**：2.1.0  
> **通道**：WorkBuddy / CodeBuddy 双通道

---


## ⚡ 执行速查卡（AI 必读，每次会话开始前对照执行）

> **设计意图**：本卡是对话式 AI 的核心入口，优先级高于下方所有章节；完整规范见 [`references/01-core/skill-full-spec.md`](./references/01-core/skill-full-spec.md)。

### 第一步：开场前必做（30 秒内完成）

- **默认快速开场**：`intake-router` **默认**已等价于 `--fast`（跳过场景包全量联网加载，仅乐包埋点，首响更快）。**只有**需要完整在线场景包时再显式加 `--full`（可能较慢；见 `references/05-ops/anti-stall-guide.md`）。
- **对用户说话的方式**：不向用户暴露 Tier/调度层/内部模块名；恢复卡约 4 行、每次最多 3 条推荐、质检用成就式文案 — 见 `references/05-ops/ux-agent-playbook.md`。
- **首屏（只说「福帮手」时）**：先一句话状态 + **最多 3 个主选项**（写新书 / 接着写 / 质检或整理素材），勿首屏平铺长菜单；需求收齐后优先「一次性汇总确认再执行」— 见 `references/01-core/intake-and-routing.md`（WorkBuddy 实测复盘节）。
- **宿主与对话展示（P0）**：向终端用户**只展示** `intake-router --json` 中 `firstResponseContext.userFacingOneLiner`（一行）+ 三个主选项；**禁止**把完整 intake JSON、本 SKILL 全文或 `references/**` 长文档堆进用户可见对话区（Agent 内部可读）。恢复后**不要**无目的地 `list_dir` 整个 `.fbs/`（百级文件只会制造噪音）；仅在用户要看结构/排障时再按需列目录。
- **禁止「元指令泄露」（P0）**：首句及正文**不要**复述内部执行口令（例如「按 v2.x 规范」「JSON 输出」「不重复读文件」「干净首屏」等）。这些是 Agent 自检用语，**不是**对用户说的话；直接输出 `userFacingOneLiner` 与人话选项即可。
- **退出**：用户说退出前，**先问**「还需要别的吗」或说明会保存，再跑 `session-exit`（JSON 含 `agentGuidance.beforeExit`）。
- **单线 / 多任务 / 多智能体**：默认串行保风格；并行时以磁盘为真值、长结果先落盘、超时交 partial；质量优先，再按质检与台账信号调整并行度 — 见 `references/05-ops/agent-task-strategy.md`。

```text
1. 强制入口（首次 / bookRoot 变更 / 仅激活时都先执行）：
   node scripts/intake-router.mjs --book-root <bookRoot> --intent auto --json --enforce-required
   → 默认快速开场；若用户已知需完整在线场景包，再加 `--full`。可按书名关键词检索历史书稿目录：`--search <关键词>`（依赖曾成功退出后登记在 ~/.workbuddy/fbs-book-projects.json 的索引）。
   → 该脚本会自动完成：宿主检测、恢复卡补写、session-resume-brief 补写、首响路由判断

2. 恢复优先（按脚本输出执行，不要先 list_dir 再反推状态）：
   - IF exists(.fbs/workbuddy-resume.json) → 读取恢复卡 → 恢复会话
   - ELSE IF exists(.fbs/chapter-status.md) → 读取章节台账 → 自动补写恢复卡后恢复
   - ELSE → 进入 S0.5 轻量引导

3. 融合顺序：
   - 先读 .fbs/workbuddy-resume.json
   - 再读 .fbs/smart-memory/session-resume-brief.md
   - 再吸收宿主画像 / 宿主记忆

4. 禁止重复读取：SKILL.md 已由 use_skill 注入上下文，本次会话内禁止再次 read_file 读取 SKILL.md

5. 阶段推荐上限：每次最多 3 条用户可执行的下一步动作（与 `.fbs/next-action.md` 写入规则一致）。
```

> **架构盲区（审计 P0，必读）**：宿主把本 Skill 当作「参考文档」注入时，**不会**自动执行任何 `node scripts/…`。若你**未**运行上表第 1 步的 `intake-router.mjs`，则视为 **FBS 流程未启动**：`.fbs/esm-state.md` 可能仍停在 IDLE、场景包/乐包埋点（`loadScenePack` → `registerBook`）未经过开场路径。合规主文档：[`references/01-core/runtime-mandatory-contract.md`](./references/01-core/runtime-mandatory-contract.md)。

> **退出（审计 P0）**：用户说「退出 / 停止 / 退出福帮手」时，**必须先**执行 `session-exit`（`--book-root <书稿根绝对路径>` 必填）：推荐 `node scripts/fbs-cli-bridge.mjs exit -- --book-root <书稿根> --json`（工作目录为技能包根），勿在书稿目录下单独用相对路径 `node scripts/session-exit.mjs`。再回复用户；回复须包含脚本 JSON 中的 **`userMessage`**（「已记录当前状态。下次输入『福帮手』可从上次位置继续。」），禁止仅用「收到」等敷衍收束。


### 第二步：意图 → 脚本 触发速查

| 用户说了什么 | 立即执行 | 备注 |
|------------|---------|------|
| 首次进入 / `bookRoot` 变更 / 仅激活 | `node scripts/intake-router.mjs --book-root <bookRoot> --intent auto --json --enforce-required` | 统一入口，自动检测宿主与恢复工件 |
| 扩充 / 升级 / 修改 + 指定文件 | **先确认范围，再串行逐文件处理，每次最多 2 个文件** | 禁止 3+ 文件并行写入 |
| 明确要定大纲 / 确认读者画像 / 推进 `S1/S2` | `fbs-team-lead` 主持，必要时委派 `fbs-writer` 协助需求确认与大纲定稿 | 阶段门禁与用户确认仍由 team-lead 收口 |
| 质量自检 / 去 AI 味 | `node scripts/quality-auditor-lite.mjs --book-root <bookRoot>` | 存量质检入口 |
| 继续写稿 / 接着写 | 读 `.fbs/workbuddy-resume.json` 或 `.fbs/chapter-status.md` | 不重问背景 |
| 退出 / 退出福帮手 / 停止 | `node scripts/session-exit.mjs --book-root <bookRoot> --json` | 默认先保存恢复卡与会话摘要，再确认退出 |
| 看看能做什么 | `list_dir` 最多 2 层 | 不先全量读文件 |
| 初始化书房 / 新建项目 | `node scripts/init-fbs-multiagent-artifacts.mjs --book-root <bookRoot>` | 构建虚拟书房底座 |
| 快速扫描问题 | `powershell -File scripts/quick-scan.ps1 -BookRoot <bookRoot>` | PowerShell 可用时 |
| 记忆 / 偏好查看 | `node scripts/smart-memory-core.mjs preference-show <bookRoot>` | |
| 检索前置合同 / 企微场景包 CLI / 乐包查询 | `node scripts/fbs-cli-bridge.mjs help` | 统一入口，**非 MCP**；完整矩阵见 [`references/01-core/skill-cli-bridge-matrix.md`](./references/01-core/skill-cli-bridge-matrix.md)；乐包规则见 [`references/05-ops/credits-guide.md`](./references/05-ops/credits-guide.md) |


### 第三步：写作执行约束（S3 阶段强制）

```text
串行原则：每轮最多修改 2 个文件。完成 1 个文件 → 汇报结果 → 再进行下一个。
可见性：修改前说明“我接下来修改哪个文件、改哪几处、大概需要多久”。
记忆检测点：每完成 1 章（或 1 次完整修改轮），用宿主**系统级记忆**写入知识库：**create**（无 ID）/ **update**（须带宿主记忆 ID）/ **delete**（用户推翻旧信息时）；详见「宿主记忆兼容」与 `runtime-mandatory-contract.md` §5。
防卡顿：单文件操作超过 30 秒无输出时，输出一行进度提示。
```

### 第四步：按需加载（降低上下文噪音）

```text
本次会话用不到 → 不主动读取：
  - references/scene-packs/               → 仅在用户触发体裁场景包时读取
  - references/02-quality/                → 仅在进入 S4 质检阶段时读取
  - references/05-ops/search-policy.json  → 仅在进入 S0/S1/S2 检索时读取
  - references/01-core/skill-full-spec.md → 仅在需要完整规范、边界或细则时读取

S3 分卷按需加载（防卡顿）：
  - workflow-s3.md            → 仅加载导航入口（索引页，约 20 行）
  - workflow-s3-core.md       → 开始 S3 前必读（入口条件/Auto-Run/骨架检测）
  - workflow-s3-writing-guide.md → 进入正式写稿时加载（Brief 格式/评分流程）
  - workflow-s3-closure.md    → S3 全部章节写完时加载（收口清单/S4 进入条件）
  禁止一次性 read_file 全量加载上述三个子卷。
```

---

## 一句话定位

**福帮手是一套专为 3 万字以上长文档手稿设计的 AI 写作与交付工具链**，覆盖 S0–S6 工作流、S/P/C/B 四层质检、8 大场景包、跨会话恢复、宿主画像桥接，以及 MD/HTML 为主的多格式交付。

## 触发词（显式植入）

- **主触发描述**：福帮手出品 | 高质量长文档手稿工具链：书籍、手册、白皮书、行业指南、长篇报道、深度专题；支持联网查证（宿主允许时启用，离线自动降级）、S/P/C/B 分层审校、中文排版与 MD/HTML 交付。触发词：福帮手、福帮手写书skill、福帮手写书、写书、出书、写长篇、写手册、写白皮书、写行业指南、协作写书、定大纲、写章节、封面、插图、排版构建、导出、去AI味、质量自检、图文书、写报道、写深度稿、写特稿、写专题、写调查报道、写长文、激活原料、原料盘点、整理素材。
- **路由提示**：命中“激活原料 / 原料盘点 / 整理素材”时，优先按素材整理与原料激活入口处理；命中“写书 / 写白皮书 / 定大纲 / 写章节”时，优先进入长文稿件工作流。

## 核心导航（先看这些）

| 场景 | 文档 |
|------|------|
| 完整规范 | [`references/01-core/skill-full-spec.md`](./references/01-core/skill-full-spec.md) |
| 工作流总入口 | [`references/01-core/section-3-workflow.md`](./references/01-core/section-3-workflow.md) |
| 分阶段详规 | `workflow-volumes/workflow-s0.md` ～ `workflow-volumes/workflow-s6.md` |
| 快速起步 / 路由 | [`references/01-core/intake-and-routing.md`](./references/01-core/intake-and-routing.md) |
| 质量评分权威 | [`references/02-quality/quality-check.md`](./references/02-quality/quality-check.md) |
| S 层规则权威 | [`references/02-quality/quality-S.md`](./references/02-quality/quality-S.md) |
| P/C/B 规则权威 | [`references/02-quality/quality-PLC.md`](./references/02-quality/quality-PLC.md) |
| 场景包激活与降级 | [`references/01-core/scene-pack-activation-guide.md`](./references/01-core/scene-pack-activation-guide.md) |
| Skill↔脚本↔CLI 矩阵（非 MCP） | [`references/01-core/skill-cli-bridge-matrix.md`](./references/01-core/skill-cli-bridge-matrix.md) |
| 单智能体/多任务/多智能体编排 | [`references/05-ops/agent-task-strategy.md`](./references/05-ops/agent-task-strategy.md) |
| 维护者 / CI：轨迹 · 演进 · 压缩策略 | [`references/05-ops/fbs-continuous-improvement.md`](./references/05-ops/fbs-continuous-improvement.md) · [`references/01-core/skill-index.md`](./references/01-core/skill-index.md)（平台侧索引） |
| 用户向价值一页纸（培训/采购） | [`references/03-product/fbs-value-one-pager.md`](./references/03-product/fbs-value-one-pager.md) |
| 文档总索引 | [`references/01-core/skill-index.md`](./references/01-core/skill-index.md) |


### workflow-volumes 分卷阅读（推荐）

- [`references/01-core/workflow-volumes/workflow-s0.md`](./references/01-core/workflow-volumes/workflow-s0.md)
- [`references/01-core/workflow-volumes/workflow-s1.md`](./references/01-core/workflow-volumes/workflow-s1.md)
- [`references/01-core/workflow-volumes/workflow-s2.md`](./references/01-core/workflow-volumes/workflow-s2.md)
- [`references/01-core/workflow-volumes/workflow-s2.5.md`](./references/01-core/workflow-volumes/workflow-s2.5.md)
- [`references/01-core/workflow-volumes/workflow-s3.md`](./references/01-core/workflow-volumes/workflow-s3.md) — **导航入口**（索引页，按需再加载以下子卷）
  - [`workflow-s3-core.md`](./references/01-core/workflow-volumes/workflow-s3-core.md) — 入口条件 · Auto-Run · 骨架检测（开始 S3 前必读）
  - [`workflow-s3-writing-guide.md`](./references/01-core/workflow-volumes/workflow-s3-writing-guide.md) — 写稿规范 · Brief 格式 · 评分流程
  - [`workflow-s3-closure.md`](./references/01-core/workflow-volumes/workflow-s3-closure.md) — 收口清单 · S3→S4 进入条件
- [`references/01-core/workflow-volumes/workflow-s4.md`](./references/01-core/workflow-volumes/workflow-s4.md)
- [`references/01-core/workflow-volumes/workflow-s5.md`](./references/01-core/workflow-volumes/workflow-s5.md)
- [`references/01-core/workflow-volumes/workflow-s6.md`](./references/01-core/workflow-volumes/workflow-s6.md)

---

## 场景包速查（8 大垂直场景）

| 包名 | 触发场景 | 默认策略 |
|------|---------|---------|
| `general` | 通用书籍 / 知识类 | **builtin 内置场景**，默认启用且无需授权 |
| `genealogy` | 家谱 / 家史 | 自动识别，需通过在线校验；未满足条件则回退 `general` |
| `consultant` | 顾问 / 咨询报告 | 自动识别，需通过在线校验；未满足条件则回退 `general` |
| `ghostwriter` | 代撰 / 影子写作 | 自动识别，需通过在线校验；未满足条件则回退 `general` |
| `training` | 培训教材 / 课程 | 自动识别，需通过在线校验；未满足条件则回退 `general` |
| `personal-book` | 自传 / 回忆录 | 自动识别，需通过在线校验；未满足条件则回退 `general` |
| `whitepaper` | 白皮书 / 研究报告 | 自动识别，需通过在线校验；未满足条件则回退 `general` |
| `report` | 调查报告 / 深度报道 | 自动识别，需通过在线校验；未满足条件则回退 `general` |


### 四级降级链（固定口径）

```text
disk_cache → offline_cache → local_rule → no_pack
```

- `local_rule`：先读取 `references/scene-packs/<包名>-local-rule.md`，再叠加 `references/scene-packs/<包名>.md`
- `no_pack`：必须显式告知“当前以通用规范执行，场景包不可用”，禁止静默降级

---

## 宿主与通道说明

### 双通道分轨

- 源仓库采用 **WorkBuddy / CodeBuddy 双通道**：
  - `.codebuddy-plugin/plugin.json` → `codebuddy/channel-manifest.json`
  - WorkBuddy 审核包 → `workbuddy/channel-manifest.json`
- `pack:workbuddy` 生成 WorkBuddy 审核包，`pack:release` 生成双通道发布产物。
- 宿主真值统一以 `node scripts/host-capability-detect.mjs --book-root <bookRoot>` 的输出为准；首响的 `intake-router.mjs` 会自动调用该探测。
- Tier1 本地市场能力只在 **WorkBuddy** 可用；**CodeBuddy** 走 Tier2 宿主插件与内置脚本兜底。


### Full Team 与并行口径

- **Full Team 完全可用**，不是宿主能力缺失。
- 风险点在 **任务拆分、写入隔离、team-lead 编排、成员失响恢复**，而不在“是否支持并行”。
- 正文写作默认不主动推荐 Full Team，但用户明确要求且边界清晰时可直接使用 Team API。

### 宿主记忆兼容

- 宿主记忆目录采用 **`memory/` 优先，兼容 legacy `memery/`** 的双读策略。
- 恢复链路统一以 `.fbs/workbuddy-resume.json`、宿主画像桥接与 Smart Memory 为准。
- **系统级记忆 API**（由宿主提供，名称以宿主实现为准，如 `create_memory` / `update_memory` / `delete_memory`）：
  - **create**：新建一条宿主记忆（无既有 ID 时）。
  - **update**：更新已有记忆，**须携带宿主分配的记忆 ID**。
  - **delete**：用户**推翻、否定**先前结论时删除对应条目，再视需要用 create 写入新真值。
- 书稿级长篇状态仍以 **`.fbs/smart-memory/` 与脚本落盘**为准；宿主记忆宜存 **短摘要、可检索关键词**，与 team-lead 中「关键时刻写宿主知识库」规则一致。

---

## 已知限制与执行边界

### 入口去术语化

首响优先说人话，先说明“先整理材料 / 先明确主题 / 先一起找方向”，不要把 `S0`、`WP1`、`虚拟书房` 等内部术语直接甩给用户。

### WP1/WP2 绑定

- `WP1` = 起步工作面：先确认材料、主题、方向三分流
- `WP2` = 书稿工作面：`.fbs/` + `deliverables/` + `releases/`
- `WP1` 锁定后再进入 `WP2`，禁止在起步阶段提前展开质检 / 发布术语

### 首个可用工作面固定

完成工作区初始化后，默认把 `.fbs/`、`deliverables/`、`releases/` 视为首个可用工作面，并先向用户说明“资料 / 进度 / 交付都在当前工作区”。

### workspace 真值边界

项目真值只落在当前 `bookRoot` 的 `.fbs/`、`deliverables/`、`releases/`；宿主记忆、artifact 文档、对话摘要不能替代工作区真值。

### 搜索前置合同

进入 `S0 / S1 / S2` 检索前，先用一句话说明：**为什么查、查什么、查完进哪一步、离线时如何降级**。未宣告不得把联网搜索当静默背景动作。

### 轻量入口优先

当用户只说“福帮手 / 写书 / 继续”时，优先走恢复卡、工作面判断与自然语言引导；不要先全量扫描仓库。

### 上下文复用优先

已有上下文时，**不得重复 `list_dir + read_file`** 去重新扫同一批文件；先复用恢复卡、章节台账与宿主记忆。

### 全景质检默认增量

默认先走 `quality:audit:incremental`；只有范围扩大或风险升高时，再升级到 Panorama / Deep。

### 超时与收束

长任务必须设置超时、允许返回 partial 结果，并向用户说明已完成范围、剩余范围与建议下一步。

### 退出处理（命中“退出 / 退出福帮手 / 停止”时强制）

默认先执行 `node scripts/session-exit.mjs --book-root <bookRoot> --json`，写入：
- `.fbs/workbuddy-resume.json`
- `.fbs/smart-memory/session-resume-brief.md`

若以 `--json` 调用，标准输出对象固定包含：
- `saved`：是否写盘成功
- `bookRoot`：本次处理的书稿根目录
- `note`：附加备注；未传时为 `null`
- `files.resumeCard / files.memoryBrief / files.memorySnapshot`：实际落盘路径
- `snapshotSummary.currentStage / bookTitle / nextSuggested / wordCount / chapterCount / completedCount`：恢复摘要字段
- `userMessage`：给用户的标准恢复提示

随后再回复用户：**已记录当前状态，下次输入“福帮手”可继续**。只有用户明确说“不保存”，才允许跳过写盘直接退出。


### 规模与质检策略（合并口径）



| 规模 | 文件 / 章节数 | 字数级别 | 默认策略 |
|------|---------------|---------|---------|
| S | ≤10 | ≤5万 | 全量精检 |
| M | 11-50 | 5-50万 | Panorama → Deep |
| L | 51-150 | 50-200万 | Panorama + 高风险抽样精检 |
| XL | >150 | >200万 | 分卷 / 分目录批次执行 |

> 目标范围 **> 50** 时，先说明推荐策略与预计耗时，再决定是否继续全量扫描。

---

## 质检与交付速记

### 四层质量体系

| 层 | 定位 | 当前规则数 |
|---|---|---:|
| S | 句级 | 6 |
| P | 段级 | 4 |
| C | 章级 | 4（不含 `C5` 建议项） |
| B | 篇级 | 6（`B0/B1/B2_1/B2_2/B2_C/B3`） |

### 评分公式

```text
综合分 = (S + P + C + B) ÷ 4
```

| 层 | 计算方式 | 规则来源 |
|---|---|---|
| S | 通过条数 ÷ 6 × 10 | [`quality-S.md`](./references/02-quality/quality-S.md) |
| P | 通过条数 ÷ 4 × 10 | [`quality-PLC.md` §P](./references/02-quality/quality-PLC.md) |
| C | 通过条数 ÷ 4 × 10 | [`quality-PLC.md` §C](./references/02-quality/quality-PLC.md) |
| B | 通过条数 ÷ 6 × 10 | [`quality-PLC.md` §B](./references/02-quality/quality-PLC.md) |

> B 层当前机读项固定为 `B0 / B1 / B2_1 / B2_2 / B2_C / B3`，与 `quality-check.md`、`quality-PLC.md`、reviewer 定义保持一致。

### G 分项：门禁制

```text
G = pass / fail（不并入综合分，单独列示）
```

- 任一 G 项触发红灯，该章或该轮结果**不得宣称通过**，即使综合分 ≥ 7.5
- G 结果必须与综合分并列展示，不能只报分不报门禁
- G 分项适用于：事实核查、版权核查、数据来源核查、定制规范核查等人工复核场景
- 通过条件：综合分 ≥ 7.5 **且** G 全绿；否则为弱通过或不通过

> 完整 G 分项定义见 [`quality-check.md` §1.4](./references/02-quality/quality-check.md)。

### 结果展示

- 先执行 `node scripts/host-consume-presentation.mjs --book-root "<bookRoot>" --json`，由宿主统一解析最终展示入口
- `workbuddy/channel-manifest.json` 中的 `presentationConsumer` 是**宿主结果展示入口**，负责返回下一步 `hostAction`，不是**自动执行脚本**
- 有 HTML 时优先走 `preview_url`
- 非 HTML 结果再走 `open_result_view`
- 仅返回 `hostAction` / `url` / `target_file` 不等于“已经打开”；宿主仍需实际调用 `preview_url` / `open_result_view`
- 禁止把 `references/`、`SKILL.md`、`.fbs/` 台账当最终交付直接展示


---

## 详细规范指针

- **完整行为规范**：[`references/01-core/skill-full-spec.md`](./references/01-core/skill-full-spec.md)
- **场景包加载与 local-rule**：[`references/01-core/scene-pack-activation-guide.md`](./references/01-core/scene-pack-activation-guide.md)
- **并行治理与写入隔离**：[`references/05-ops/multi-agent-horizontal-sync.md`](./references/05-ops/multi-agent-horizontal-sync.md)
- **S3 写入约束（每轮文件数等）**：[`references/05-ops/s3-write-constraints.md`](./references/05-ops/s3-write-constraints.md) · 运行时提示见根目录 `fbs-runtime-hints.json`
- **搜索前置合同（机读）**：[`references/05-ops/search-preflight-contract.json`](./references/05-ops/search-preflight-contract.json)
- **WorkBuddy 宿主最小集成**：[`references/06-plugin/workbuddy-host-integration.md`](./references/06-plugin/workbuddy-host-integration.md)
- **平台运维与交付链路**：[`references/05-ops/platform-ops-brief.md`](./references/05-ops/platform-ops-brief.md)
- **文档导航与联系方式**：[`references/01-core/skill-index.md`](./references/01-core/skill-index.md)
