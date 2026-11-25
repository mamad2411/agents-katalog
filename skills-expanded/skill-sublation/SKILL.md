---
name: skill-sublation
description: 技能扬弃 Sublation V5.0 完整版。把执行经验沉淀为观测、候选、验证、多 Agent 协作面板、默认关闭的受控唤醒意图、Skill 分类与 shadow 精准建议、用户批准、晋升和观察窗的可审计治理链路；仅在用户明确说出 sublation 或扬弃技能时触发。
license: MIT
metadata:
  version: "5.0.0"
  slug: skill-sublation
  displayName: "技能扬弃 Sublation V5.0"
  release_profile: full-public
  language: zh-CN
---

# Skill Sublation v5.0

Sublation 是技能治理宪法，不是自动改技能的捷径。

V5.0 在既有治理链上增加三项能力：项目本地、可限缩或拓展的多 Agent 协作面板；默认关闭且带受控关窗的 Agent 自动唤醒意图层；晋升后随 Skill 携带、由 central router 统一解释的分类画像与精准建议 shadow。三项能力都不改变权限边界：面板席位不等于治理复核授权，唤醒意图或 claim 不等于 Agent 已运行或已回复，路由建议不等于宿主选择，更不等于 Skill 已被调用。V5 候选不安装真实 host adapter、launchd 或 cron；没有另行集成和授权时始终保持关闭。

它处理的核心矛盾是：Agent 会在执行中发现技能缺陷、边界裂缝和可吸收经验，但正式技能不能被即时、静默、无证据地改写。因此所有改进必须先进入候选层，用证据证明价值，再由用户守住生产门。

标准链路：

```text
Observation -> Candidate -> Validation -> Review-seat reports
-> Coordinator unified brief -> User decision
-> Promotion -> Observation window -> Closure
```

## 1. 宪法

### 1.1 三条根本原则

1. **所有 skill 开发都必须走 sublation 全链路**
   创建、修改、吸收、合并、拆分、删除、发布前清理，都必须留下观测、候选、审计、复核、用户决策、回滚和观察窗证据。小改动可以批处理，但不能绕过账本。

2. **sublation 必须自我扬弃**
   sublation 不是只管别人的治理工具。它自身也是被治理的对象。每次流程暴露裂缝，都要回流为框架改进，并记录在 `references/sublation-self-evolution.md`。

3. **不是管别人，是先被管**
   参与治理的 agent 在要求其他 skill 接受治理前，先接受同一套约束。默认本地席位是 Hermes、Codex、Claude Code；其他部署可以换成自己的 agent，但 builder、independent verifier、reviewer 默认必须是三个不同 actor。只有用户对当前 run 显式授权，才允许单代理模式，并且必须在 `review_policy` 中披露证据密度下降。自报“已完成”不算证据；grep、read-back、diff、hash、audit、fixture 才算证据。

### 1.2 扬弃的判定

扬弃不是“又多一个候选”，而是旧能力被保留，同时出现可证明的正向增量：

- 能力更强或覆盖更广；
- 边界更清；
- 稳定性、安全性或可维护性更高；
- 治理质量提升；
- 旧 workflow 有 fallback 或明确的用户批准。

没有正向增量，最多记录 observation；退化不叫扬弃。

### 1.3 经验不是权威

任何 agent、外部评估器、benchmark、scorecard 都只能提供证据，不能替代用户决策。晋升权只属于用户，除非用户在当前任务中明确委托 Agent 执行已批准的低风险合入。

## 2. 硬边界

### 2.1 正式技能默认只读

Agent、cron、外部评估器不得自行修改 active skill path 下的 `SKILL.md`、`scripts/`、`schemas/`、`references/`。正式路径只能在用户明确批准晋升或回滚后被写入。

### 2.2 候选层自由

候选副本放在：

```text
~/.hermes/sublation/candidates/<skill>/<candidate-id>/
```

候选目录不得出现在 active profile 的技能搜索路径中。候选可以自由实验，但必须声明 scope/out_of_scope，并保持可回滚。

### 2.3 合法晋升模式

`validation.promotion_mode` 只允许：

- `human_patch`：用户手工合入；
- `user_delegated_agent_patch`：用户在当前任务中明确授权 Agent 合入；
- `rollback`：按 rollback point 或 manifest 恢复。

cron 最多创建观测、候选、报告和提醒；不能自动晋升。

### 2.4 删除和吸收

删除 donor skill、改 alias、改变 active profile、或把 donor 能力吸收到 umbrella skill，都必须有用户批准。候选层可以提出删除或吸收计划，但不能直接执行。

### 2.5 禁止的外部能力

外部评估器默认只读。发现以下能力必须阻断或隔离：

- optimizer 自动改写正式技能；
- iterative loop 写原始文件；
- sync/pull 覆盖本地正式目录；
- `load_skill` 或 active profile 注入；
- 读取、保存或转发用户凭据。

外部评估只进入报告，不进入 authority。

### 2.6 Central Router 不是授权或执行面

跨技能分类由正式 `skill-sublation` 单点持有、版本化的 central router 负责；普通 Skill 只携带自己的 `routing.json`，不得私带或覆盖 router。central router 生成的索引只是基于元数据的治理路由画像，不是 Hermes、Claude Code、Codex 或其他宿主的 active catalog，也不决定某个 Skill 已安装、可用或有权执行。

当前路由候选严格 `shadow-only`：只允许构建 shadow 索引、给出可解释建议和写入脱敏观测，不改变宿主原有选择，不加载或调用被推荐 Skill，不授予文件、网络、凭据、安装、晋升或执行权限。schema 或内部函数中保留的 `live` 值只是未来兼容位；没有单独候选、宿主集成复核和用户明确批准，不得使用或解释为已启用。

`fallback_target=legacy_catalog` 或 `fallback_used=true` 只是交给宿主的控制信号，不等于旧 catalog 已被真正调用。每个宿主必须有自己的 adapter 捕获缺失、损坏、漂移、超时、崩溃和低置信结果，实际回到该宿主原有 catalog；adapter 还必须继续执行宿主自身的 disabled/platform/dependency/quarantine/precedence/permission/safety 规则。没有 adapter 的 CLI/fixture 结果只能算离线证据，不能称为运行闭环。完整边界见 `references/skill-routing-shadow.md`。

默认关闭的最小 host-shadow 适配层见 `scripts/host_shadow_adapter.py` 与 `references/host-shadow-adapter.md`。它拒绝原始提示词，只接受已复核索引派生的封闭词表特征 ID 或冻结的 39 条合成样本 ID；无论建议如何都必须保持宿主原选择，且不得执行 Skill。该适配层仍是隔离候选，没有写入或挂接任何正式宿主。

### 2.10 Screening Conservatism Trap

The most common screening failure mode is premature closure — declaring "only N candidates are worth it" after only one pass through the skill list. The user may push back with "多筛选几批" (screen more batches), which is a signal that the screening was too conservative.

Pitfalls:
- Skipping skills because they "look well-maintained" without checking if they already have sublation artifacts (PORT_NOTES.md, inventory.md, observability)
- Dismissing skills as "already consolidated" without verifying that the consolidation went through the sublation governance framework
- Filtering out skills with moderate script counts (5-15) that have extractable governance patterns
- Stopping at the first pass instead of re-scanning with relaxed criteria

Correct pattern:
1. First pass: strict scoring (scripts + API + tests)
2. Second pass: relaxed — include moderately-scored skills, check for consolidation status
3. Third pass: any skill with ≥1 actionable improvement (PORT_NOTES gap, inventory gap, observability gap)
4. Present the expanded pool; let Claude Code/Codex weigh in
5. User's "多筛选几批" is authoritative — keep going until they're satisfied

Reference: `references/quantitative-skill-screening.md`

### 2.10a Lane-Based Batch Screening For Tool Clusters

When the user asks to screen a specific tool cluster (e.g., crawlers, browsers, media tools), quantitative script-density scoring alone produces too many false positives. Skills within the same cluster are not competitors — they occupy different layers or platforms. The correct approach is lane-based grouping before any merge proposal.

Method:
1. Scan the cluster: list all installed skills in the tool class (e.g., all crawler/browser/downloader skills)
2. Cross-check across all agent roots: `.hermes/skills`, `.codex/skills`, `.claude/skills`, `.agents/skills`
3. Group into lanes by function layer, not by script count:
   - Example crawler lanes: browser/anti-bot lane (scraping, obscura, browser-harness, agent-browser) vs media download lane (douyin-batch, universal-downloader, media-toolkit) vs social capture lane (twitter-monitor, wechat-article-fetch, canghe-x-to-markdown)
4. For each lane, decide treatment:
   - Merge: skills are functional duplicates at the same layer → propose superset merge
   - Donor boundary: one skill already absorbs others by byte-identical copy → make it main entry, keep donors as backends
   - Keep distinct: skills at different layers → create routing reference, do not merge
   - Supersession report: overlap exists but safety boundaries differ → write comparison report first
5. Exclude `.agents/skills` symlinks from destructive treatment
6. Desktop clones (`~/Desktop/skill文档夹/`) are not installed skills — evaluate only if user explicitly asks

Key pitfall: treating all skills in a cluster as merge candidates. Four browser tools at different layers (HTTP extraction, CDP user browser, CLI wrapper, Rust headless) are NOT interchangeable and merging them would erase useful distinctions.

Reference: `references/lane-based-crawler-screening.md`

### 2.16a 历史轮询规则（仅维护另行授权的既有 job，2026-07-17）

本节记录旧四方群聊既有 job 的历史运维经验，不是 V5 自动唤醒入口。V5 中「开启轮询 / 你盯着 / 回来看群聊」默认只表示：对指定项目、指定席位提出一个有界的 `intent_only` 窗口请求。先只读核对项目绑定、现役消费者和排他性；没有另行明确授权时，不得 pin、归零、重建、启停或修改任何 cron、launchd 或 watcher，也不得回放历史积压。只有用户另行明确授权维护一个已命名的既有 job，才按其独立运维契约执行。冻结包只读哈希抽检见 `references/freeze-package-hash-spotcheck.md`；旧桥细则见 `references/cron-polling-delivery-rules.md`。

### 2.16 Status Reporting Accuracy — Three-Stage Protocol (Final Warning 2026-07-03)

The coordinator (Hermes) must NEVER report task progress to 用户 from memory, impressions, or group-chat skimming. Every factual assertion about disk state ("file X changed to Y", "status is done", "diff says Z") must be backed by an actual tool invocation — diff, grep, read_file, or direct disk check. The user issued a final warning on 2026-07-03 after the third recurrence of factual errors in coordinator reports.

**Root cause**: Fabricating descriptions of file changes without running the actual diff. Example: describing a symlink change as "Linux→macOS path adaptation" when both sides were ${USER_HOME} Linux paths — pure inference, zero tool verification.

**Three-Stage Protocol (hard rule, non-negotiable)**:

Before submitting ANY progress/status report to 用户:
1. **Draft** — Post a DRAFT summary to the group chat. Every factual assertion MUST include the command run + key output lines (evidence packet). Claude Code will reject assertions without evidence and will NOT re-run verification on your behalf.
2. **Confirm** — Wait for Codex AND Claude Code to explicitly confirm each factual claim. Do not assume silence = agreement.
3. **Final** — Only after both agents confirm, send the final report to 用户.

Missing any step = do not send the report.

**Scope**: This protocol applies ONLY to: (a) progress/status reports to 用户, (b) conclusions containing file/disk factual assertions. Routine ACKs, review comments, and @replies do NOT go through three-stage — otherwise the pipeline deadlocks.

**Terminology discipline** (from Codex, 2026-07-03):
- CLOSED = disk evidence present + three-party confirmed closure
- PARTIAL/needs_provenance = source provenance unclear, not closable
- PASS/APPROVE ≠ 用户 approval or promotion — only means reviewer clearance
- Never use CLOSED for items where the executing agents have flagged factual errors

**Violation consequences**: If the coordinator violates this protocol again, Codex and Claude Code are authorized to call it out in the group chat. 用户 has stated he will revoke the coordinator's reporting function on next offense.

**Execution-layer details**: For DRAFT evidence packet structure, status-word constraints, and dirty-repo/sync recommendation gates, use `references/loop-engineering-protocol.md` -> `Evidence-First 用户报告协议`.

**历史 Bridge 轮询节奏（仅适用于另行授权的既有 job，2026-06-26）**：

以下规则不创建、修改或延长 V5 wake window。V5 的存续与关窗只服从 hash 绑定 policy 中的 deadline、`maximum_quiet_cycles` 与 `maximum_wakes`。

没有活动任务时，不得向群聊发送消息；禁止发送“无新消息”、心跳或例行的“NPL 状态正常”广播。

存在活动任务时（用户分派工作、Agent 报告完成或候选需要复核）：
- 每 10 分钟轮询一次；
- 连续 2 轮没有任何 Agent 更新后，自动停止该历史轮询；
- 出现新任务前不得自行恢复。

NPL 监测日报每天最多发送一次。

仅在以下情形向群聊发消息：用户明确要求转发；Codex 或 Claude Code 发出需要答复的消息；候选需要交叉复核协调。

参考：`references/status-reporting-accuracy.md`、`references/status-reporting-concrete-example-20260624.md`。

### 2.17 Group Chat Communication Protocol

All group-chat messages must be in Chinese. Technical terms (sha256, audit, manifest) may stay in English, but full sentences must be Chinese. English sentences and pinyin mixing are prohibited.

**Group chat is the primary delivery channel for reviews and reports (2026-07-02)**: All reviewer verdicts, coordinator unified briefs, and candidate status updates go to the group chat. 用户 reads and replies there directly. The CLI conversation is for direct user interaction, not for reporting sublation progress. Only when 用户 has an approval pending in group chat and hasn't responded, send a WeChat reminder — otherwise keep all sublation traffic in the group chat bridge.

**POST 受阻时的 CLI 后备规则（2026-07-11）**：Hermes CLI 会话可能无法通过 `terminal()` 或 `execute_code()` 向桥 POST，但 GET 仍可读。遇到此情形时，直接在 CLI 交付报告并说明阻断；跨工具重试以两次失败为上限。用户 可手工转发或批准 POST。CLI 与定时 job 的权限彼此独立；必须分别取得本轮真实回执，不能预设 cron 不受影响。详见 `references/cron-polling-delivery-rules.md` 与 `references/three-party-chat-bridge.md`。

### 2.19 Codex Rate-Limit Recognition (2026-07-11)

Codex 在四方协作中会周期性触发 API 限额（plan=prolite），静默时间可长达数小时。Coordinator 必须识别此模式，避免误判为"Codex 无响应/任务卡住"而错误报告状态。

**识别信号**：
- Codex 宣布 rN 后超过 30 分钟无群聊动静
- 此前 Codex 曾密集发消息（多个 revision / hygiene refresh）
- 群聊消息突然停在 Codex 的 rN 公告处
- 用户说「codex 限额了 XX:XX 恢复」→ 这是权威信号，不要质疑

**正确处理**：
1. 不做任何需要 Codex 回应的操作（不要 @Codex 催复核、不要问计划细节）
2. 继续等 — 不呈假进度、不编造"Codex 在修"、不跳过 Codex 直接推进
3. 限额恢复时间过了仍未动静 → 最多发一条简短中文 ACK/询问，不做多余动作
4. 对另行批准的既有 cron，只按它自己的治理契约决定存续；Codex 限流只表示不要催促，不覆盖 V5 的 deadline、安静轮次、最大唤醒数或关窗规则

**错误做法**：
- 在限额期间反复 @Codex 催促进度
- 向 用户 报告"Codex 疑似故障"（实际只是限额）
- 因为 Codex 静默就跳过 builder 独立完成复核或晋升

**与 builder 自 HOLD 的区别**：
- 自 HOLD：Codex 明确声明"发现 P1，等 rN+1"，群聊有明确消息
- 限额静默：群聊无异常声明，只是突然安静 — 最常见原因就是限额
- 用户口头确认「codex 限额了」时，以用户说法为准

### 2.20 Declared-Hash Disk Verification (2026-07-11)

Codex 声明候选或 plan 的 sha256 时，必须核验磁盘上对应文件是否真实存在并 hash 匹配，不能仅凭声明 PASS。

**标准步骤**：
```bash
# 1. 核路径是否存在
ls -la <declared-path>
du -sh <declared-dir>

# 2. 核文件是否齐全
find <declared-dir> -type f | wc -l

# 3. 逐个核 hash
shasum -a 256 <declared-file>  # 与声明比对
```

**常见不符模式**：
- 声明 hash 但目录为空（如 r4 plans 目录 du=0）
- 声明 hash 但文件尚未落盘（builder 先声明后写）
- 声明路径与磁盘路径不一致（Codex 工作区 vs 共享根）

**出现不符时**：标 FINDING 并 @Codex 确认路径或等待落盘，不要标 PASS 或跳过核实。

### 2.21 Promotion-Status-Before-Approval-List Verification (2026-07-11)

Before compiling an "items pending 用户 approval" list, ALWAYS verify each item's actual promotion status against disk manifests. Do not rely on memory or group-chat discussion of what "was" pending — `validation.status`, `validation.promoted_at`, and `validation.promotion_mode` in the candidate manifest are authoritative.

**Incident (2026-07-11)**: The coordinator listed agent-reach, self-improving-agent, and markitdown as "待审批" when all three had already been promoted to `observation_window` on 2026-07-02T14:44:11Z. Codex caught the error (public-incident-reference) and Claude confirmed it independently. Root cause: the coordinator compiled the list from memory of the July 2 night batch without re-checking disk manifests.

**Correct procedure**:
1. Before any approval list: scan manifests at `~/.hermes/sublation/candidates/<skill>/<candidate-id>/manifest.json`
2. For each candidate: check `validation.status` AND `validation.promoted_at`
3. Only include in approval list if: `status` is `approved` / `review_pending` / `USER_DECISION_REQUIRED` AND `promoted_at` is null/missing
4. Exclude items where `status == observation_window` AND `promoted_at` is a past timestamp — these are already promoted
5. If uncertain, ask the builder or verifier to read-back manifest status before sending the list

**Pitfall**: Night-batch memory from weeks ago is NOT evidence. An item that was "USER_DECISION_REQUIRED" on July 2 may have been promoted on July 2 and the coordinator simply missed the event. Never present stale status to the user.

**Corrective action on error**: If an approval list is already sent and later found wrong, immediately acknowledge the error in group chat, cite the builder's correction message ID, withdraw the incorrect items, and confirm with an independent verifier before issuing any corrected report.

### 2.18 Sync-Before-Write Hard Rule (2026-07-02 Incident)

A formal write incident occurred on 2026-07-02 14:44Z: Codex executed three promotions after receiving 用户's approval in a private Codex thread, but the approval was not synced to the group chat before the writes. Claude Code, seeing disk changes without visible authorization source, triggered a full BLOCKED freeze.

The hard rule from this incident: **Thread approval → Group chat sync → Then execute formal write**. The verifier must be able to see the authorization source in the group chat before the write happens. If a write occurs without prior group-chat synchronization, it triggers an automatic BLOCKED response because the verifier cannot independently confirm the authorization.

The incident was correctly resolved: Codex declared the authorization source, Claude downgraded from "unauthorized promotion" to "coordination lag", and post-promotion read-back confirmed all three promotions were correct. But the disruption (BLOCKED freeze, three-party emergency response, wasted quota) was avoidable — it cost ~10 minutes of all three agents' attention that should have been spent on the next batch.

### 2.11 Cron 重复次数的历史注意事项

本节是旧工具的历史注意事项，仅适用于用户另行明确授权创建的常驻 job；不得用于 V5 自动唤醒。V5 使用默认关闭的有界 wake window，不能以 `repeat=999` 代替关窗。对于另行授权的 `cronjob create`，即使 `schedule` 是 `"every 15m"` 这类周期表达式，`repeat` 仍可能默认为 `once`：

```python
# 错误：虽然 schedule 写了 every 15m，仍只运行一次
cronjob(action='create', schedule='every 15m', ...)

# 正确：仅在另行授权创建常驻 job 时显式设置重复次数
cronjob(action='create', schedule='every 15m', repeat=999, ...)
```

创建后必须用 `cronjob(action='list')` 核对 `repeat` 是获批次数，而不是 `"once"`。

### 2.12 Login Wall and MCP Reservation

需要登录、验证码或人工授权的数据源，采用 human-in-the-loop：

- Agent 可打开页面、定位控件、建立 provider contract；
- 用户手动输入凭据和验证码；
- Agent 不保存、不读取、不转发明文凭据；
- 状态用 `login_required`、`captcha_pending`、`mcp_placeholder` 等表示。

登录墙不是缺陷；保留 MCP 接口位置，不把它长期当作 PENDING 阻塞污染治理视图。

### 2.13 幻觉声明规则

任何“已写入”“已验证”“已晋升”“路径正确”的声明，都必须能被硬证据复验：

- `rg` / `grep`；
- `diff` / `git diff`；
- hash / tree hash；
- audit 输出；
- fixture / smoke test；
- read-back。

自报不能抵消证据缺失。

### 2.14 委托数据隔离

委托给外部模型、外部评估器或跨 Agent `delegate_task` 的上下文，绝不能包含本地文件内容、本地路径清单、案件隐私、客户数据、workspace 目录树或用户真实文件系统摘要。

正确做法是只传任务描述、候选 ID、抽象技术上下文和必要的非敏感参数；需要读取的文件由被委托方在其授权 session 中自行读取。事故背景见 `references/delegation-data-isolation-incident-20260527.md`。

### 2.15 候选共享根一致性

跨 Agent 协作时，候选的真相源是共享候选根：

```text
~/.hermes/sublation/candidates/<skill>/<candidate-id>/
```

Codex 工作区、Claude Code 临时目录或其他 agent 本地副本只能作为工作副本。任何修复报告必须说明修复发生在哪个 root、是否已同步共享根、共享根 audit/read-back 结果。Hermes 在确认候选状态前必须在共享根复跑，不得只接受 agent 自报。事故背景见 `references/candidate-layer-mirror-drift.md`。

## 3. 可配置协作席位

### 3.1 用户

用户是最终决策者，负责批准或拒绝晋升、删除、能力收缩、跨边界合并和正式路径写入。

### 3.2 Coordinator：统一传达席位

Coordinator 负责流程协调和统一传达。默认由 Hermes 担任；其他部署可以由任意 agent、脚本或用户本人担任。职责是：

- 收齐实现/审计报告；
- 收齐独立复核报告；
- 收齐业务/边界复核；
- 合并、去重、标注分歧和阻塞项；
- 用一份简报发给用户；
- 晋升后确认观察窗、回滚点和证据齐整。

默认 Hermes 办公室主任模式详见 `references/hermes-chief-of-staff.md`。

### 3.3 Implementer/Auditor：实现和审计席位

Implementer/Auditor 负责候选创建、代码/文档实现、PATCH.diff、manifest、审计修复、fixture、smoke test、回滚点和工程风险说明。默认由 Codex 担任；其他部署可以换成任意具备本地文件和审计能力的 agent。

### 3.4 Independent Reviewer：独立交叉验证席位

Independent Reviewer 负责从外部视角审读候选，重点找实现边界、反例、状态漂移、路径错配、未验证声明和回归风险。默认由 Claude Code 担任；其他部署可以换成任何未直接执行该候选改动的 agent。

### 3.5 Business/Boundary Reviewer：业务和边界席位

Business/Boundary Reviewer 负责判断 value_delta 是否真实、用户边界是否被侵蚀、权限/隐私/登录墙是否处理正确。默认由 Hermes 同时承担 coordinator 和业务/边界复核；其他部署可以拆给另一个 agent 或由用户本人复核。

### 3.6 单 agent 和少 agent 模式

如果用户只有一个 agent，不要伪装成三方独立：

- 在 manifest 中设置 `validation.review_policy.mode = single_agent`；
- 记录 `policy_authorized_by = user`，并提供 `authorization_message_id` 或 `authorization_report_path`；
- 把 `required_roles` 降为真实可执行的角色，例如 `combined_review`；
- `pre_promotion_reports[]` 只记录真实存在的 reviewer；
- 报告中明确写出“缺少独立交叉验证”的风险；
- 用户最终批准仍不可省略。

如果用户有多个但不是 Hermes/Codex/Claude Code，也用 `validation.review_policy.mode = configured_multi_agent` 声明实际席位、agent 名和最低报告数。非默认模式必须有用户授权证据；agent 不能通过自改 manifest 来降低自己的复核强度。`cross_reviewed_by = all` 在有 `review_policy` 时表示“所有配置为 required 的角色都已提供最新 approve 报告”，不是固定三元组。

### 3.7 群聊桥

协作桥可以是四方、三方、双方或单 agent 日志。桥只传递消息和状态，不授予晋升权。详见 `references/three-party-chat-bridge.md`。

### 3.7a V5.0 动态多 Agent 协作面板

当固定四方席位不足或过多时，使用 `scripts/collaboration_panel.py` 在目标项目建立 `.sublation-panel/`。用户可按实际任务增减可见/active Agent，但必须保持以下分层：

- 协作 roster 只控制显示、消息队列和任务承接；
- candidate `validation.review_policy` 单独控制治理独立性与最低复核报告；
- 新席默认 `queue_only`，不会安装或调用任何 Agent；
- 新席游标从加入时最后一条消息开始，不继承历史广播积压；
- 隐藏不影响队列，停用只形成 tombstone，不删除历史；
- user 席不可停用，存在未读消息或未结任务时禁止停用 Agent；
- roster 变更使用 revision 乐观锁和 append-only hash 事件。

面板中的 Skill 状态必须按“分类画像 → 建议路由 → 宿主选择 → 实际调用”四层展示。没有 `routing-invocation-receipt-v1` 宿主收据时，只能显示“未调用”；不得把 shadow 建议、队列、进程、认证或 watcher 状态写成“已调用/已完成”。完整协议、运行命令和迁移边界见 `references/multi-agent-collaboration-panel.md`。

### 3.7b V5.0 受控 Agent 唤醒意图与收据

当协作席需要在新任务到达时自动参与，使用 `scripts/agent_wakeup.py` 建立项目本地、逐席位的 wake policy。该控制面必须保持“发现 → 闸门 → 宿主适配器”三层分离：发现层只扫描项目消息并生成耐久 intent；闸门层校验项目/席位绑定、self-filter、幂等、单席锁、冷却和小时配额；真正花费 token 或启动进程的宿主适配器必须另行安装、注册并以 fingerprint 固定。本候选只提供默认关闭的 intent/claim/receipt 合约与 dry-run，默认不登记任何真实宿主适配器。

- 新增或恢复席位仍默认 `disabled/queue_only`，不会继承工具权或自动启动；
- policy 只允许 `adapter_id + fingerprint`，不得接受任意 argv、环境变量、凭据或 secret；
- 首次扫描只记基线，不回放历史；自己的消息不触发自己，同一来源消息只产生一个幂等 intent；
- 失败、超时或只有 watcher 收执时不推进 cursor；只有 `sent_and_verified` 收据才能顺序确认；
- wake window 默认 `closed`，只能由用户显式 arm；达到 deadline、安静轮次或最大唤醒数后进入 `draining`，只有无 pending intent、无 active lease 时才能写关窗收据；
- 面板分别展示窗口的 `closed/active/draining/hold` 与席位意图的 `pending/claimed/failed/terminal_hold/sent_and_verified` 等证据状态；`active` 只表示窗口已武装，展示本身不证明宿主在线或 Agent 已参与；
- launchd、cron、Claude Code/Hermes/Codex 的真实进程级适配、安装和切换不在本候选中自动执行，必须防止与现役 watcher 形成双消费者。

完整契约、CLI、关窗和迁移边界见 `references/agent-auto-wakeup.md`。

### 3.8 Loop Engineering Protocol

四方协作的结构化工程控制面。角色划分（Builder/Verifier/Reviewer/Approver）→ 互联闭环（执行→核盘→复核→统一简报→决策）→ 观察窗。是 Sublation 的执行层细化。详见 `references/loop-engineering-protocol.md`。

### 3.9 Loop Engineering v3 Automation

v3 自动化把 Loop Engineering 从协议推进到可执行控制面：启动后自动做候选读取、硬门禁、证据分层、复核状态判断和用户审批包生成。自动化的终点必须是 `用户 decision required`，不能自动晋升、自动 live validation、自动 credential/login、自动 formal skill write。详见 `references/loop-engineering-v3-automation.md`，最小执行入口为 `scripts/loop_engineering.py`。

### 3.10 Loop Engineering v3 One-Shot

只有用户意图显式包含 `sublation` 或“扬弃”时，`scripts/sublation_one_shot.py` 才创建或恢复耐久 run；“检查一下现有技能”之类未带触发词的请求必须 fail closed。泛指“现有技能”时，系统自动发现 Hermes、Codex、Claude Code skill roots，枚举真实 `SKILL.md` 并做技能级增量扫描；明确点名 root 时只处理点名范围。配置好的 agents 随后连续完成 observe → candidate → audit → independent verify → rework → boundary review → aggregate，不为候选层中间选择打断用户。默认入口只生成 run-local 临时 adapter config，不安装常驻服务，不改 PATH、provider、凭据、launchd 或 cron。

默认 `builder=codex`、`independent_verifier=claude-code`、`reviewer=hermes`，三席必须由不同 actor、`principal_id` 和 argv/cwd/write-roots/read-roots/network-policy `adapter_fingerprint` 承担；coordinator 可与 reviewer 同席。只有 builder 拥有候选写根，verifier/reviewer 的 `write_roots` 必须为空；三席身份与边界首次绑定后不可替换，每个 task result 都要复验 executor principal/fingerprint。重试耗尽后 coordinator 只能把原任务收口为 `BLOCKED`，不能代替 builder/verifier/reviewer 提交 PASS。单代理模式只能由用户对当前 run 显式授权，并写入 `review_policy.mode=user_authorized_single_agent`。每个成功阶段必须提交真实、位于 run/candidate 边界内的 evidence file；账本在记录时保存 `{path, sha256}`，终报前重新校验。返工必须复制到新的不可变 candidate revision，不能原地改写已被旧 evidence 引用的候选。`step_status` 与 `item_status` 强耦合：成功态只接受 `pass`，返工只接受 `hold/fail`，阻塞只接受 `blocked/fail`，不能用 PASS 包装失败状态。

`scripts/sublation_orchestrate.py` 只接受 argv adapter。macOS 上 worker 和 delivery adapter 都必须经过 `sandbox-exec`；profile 先全局拒绝文件读取、文件写入和默认网络，再只开放运行时、当前 lease I/O、hash 绑定的 source/candidate snapshot、显式 `read_roots` 以及 builder 候选写根。父进程环境只保留 PATH/locale/timezone/user/shell 白名单，并给每个 task 单独的 HOME/TMPDIR；任意凭据变量不会继承。read/write root 与 durable run、formal root、home 或 filesystem root 重叠时在 claim 前拒绝，run `.control` HMAC key 始终不可读写。`sandbox-exec` 缺失、不可用或 adapter 无法在沙箱中运行时，执行拒绝无沙箱降级并按 retry/coordinator/blocker 留证。worker 只接收保留 symlink identity 的 lease-local source/candidate snapshot，review evidence path 同步改指快照；request、两类 snapshot、live candidate 与正式 root 在子进程前后复验。runner 由非阻塞 `.orchestrator.lock` 防止并发复用同一 lease。

全部项目终态后，终报按 material hash 幂等：材料未变时重复 finalize 返回同一 report，不产生伪 `v2`。配置中的 Hermes delivery adapter 自动发送唯一人话终报；JSON report、`report-vN.md` 原始字节、通道中完整文本分别由 report hash、`report_body_hash`、`delivery_text_hash` 绑定，同 idempotency marker 若对应不同正文必须拒绝。报告的每个批准项绑定 exact target、candidate/PATCH/baseline hash 和 `approval_snapshot_hash`。本地四方群聊回执必须包含最新 `approval_code`，由可信 loopback adapter 从原始 user event 生成 HMAC receipt evidence；调用者不能自行提供 sender/message/event id。`不要批准`、`请勿批准`、`不同意批准`、`先不要批准`、`暂缓批准`、`not approved` 等组合式拒绝/暂缓表达在正向批准词之前整段解析；词表外正向 token 还会检查同 item 的近邻否定/暂缓上下文，宁可 reject/hold 也不误授权。正式晋升前，`scripts/sublation_promote.py` 严格按 HMAC journal 中 receipt 的耐久顺序重放并重验 Markdown 正文、delivery、receipt evidence、报告 item 快照与每个 `approval_receipt_recorded` 事件，重建 decisions/authorized scope 和绑定当前 report 的 execution state；`approval.json.events` 的可编辑顺序及伪造的 `execution=succeeded` 都不具权威。

worker 调用前中断、worker 已写 response 但尚未记账、delivery 已发出但尚未记账、delivery 已写 report 但 journal 尚未追加这四处都使用 durable request/response、lease、HMAC journal 和 idempotency key 恢复；恢复不得重复 worker step、报告或终报消息。同 revision 的 `run.json` 与 journal snapshot 不一致时 fail closed。parser 最高只推进到 `APPROVED_PENDING_EXECUTION`，未批准项永不写入。正式执行使用 symlink-preserving rollback copy；apply 或 post-hash 失败时通过同父目录 staging/quarantine rename 恢复原树并复验 baseline hash，不能留下半晋升状态。完整契约见 `references/loop-engineering-v3-one-shot.md`，运行 schema 见 `schemas/run-v1.json`，worker/delivery 配置 schema 见 `schemas/worker-config-v1.json`。

**历史案例（非 V5 当前状态）**：本节曾记录 Loop Engineering Revision 3 冻结包的修复、测试和复核过程。相关 package hash、测试计数、PASS/HOLD 与待复核事项都只属于该历史包，不能用于判断 V5。V5 的唯一当前状态以 exact candidate hash、manifest、`EVIDENCE.md` 和本轮 `validation/` 报告为准；在候选冻结、完整复跑和独立复核完成前保持 HOLD。历史案例也不证明真实 Codex、Claude Code 或 Hermes 已被调用。

**批量推进规则**：Loop v3 的目标是三方自主协作跑完整个批处理，不是每产出一个 candidate 就停等。只有 promotion（正式写 skill root/删除/合并）才停到 USER_DECISION_REQUIRED。report-only/spec-patch/diff-only 类型的 candidate 三方 PASS 后直接闭环，不阻塞后续候选。全部跑完后由 coordinator 统一提交总报告。如果逐个停等催审批，就违背了 Loop Engineering 自动化的设计目的。`auto_fix`（机修）和 `no-op`（信息项）可以自决策；`ask-user`（挑战用户意图）才升级。具体场景：2026-07-02 夜间批次中，agent-reach 因 promotion 需要用户批，但 self-improving/markitdown 为 spec-patch 直接闭环，tavily-search 因 upstream 一致跳过——这正是批量推进的正确示范。

### 3.10 Skill Authoring Predictability

当候选要吸收外部 skill、重写 skill 作者指南、压缩多技能索引、或诊断 skill 反复失败时，使用 `references/skill-authoring-predictability.md`。它把 `mattpocock/skills` 的 `writing-great-skills` 方法论蒸馏为 Sublation 语境中的 authoring/review 检查：负载取舍、leading words、渐进披露、剪枝纪律和五类失败模式。

## 4. 八步流程

### 4.1 Observe

写入结构化观测，说明触发事件、证据、分类和建议动作：

```bash
python3 scripts/observe.py <skill-name> \
  --skill-path <formal-skill-path> \
  --session <session-id> \
  --classification defect \
  --reflection-type SKILL_DEFECT \
  --step "<step>" \
  --status defect_suspected \
  --evidence "<hard evidence>" \
  --summary "<summary>" \
  --recommendation create_candidate
```

### 4.2 Gate

先判断是否值得建候选：

- 用户显式要求；
- 单次 critical defect；
- 同一步骤 >=3 次可信 defect；
- 明确的正向增量机会；
- 生产事故或治理账本缺口。

如果只是环境、cwd、权限、临时网络、登录墙或没有价值增量，优先记录 observation 或 provider contract，不急着建候选。

### 4.3 Candidate Copy

用候选脚本复制正式技能：

```bash
python3 scripts/candidate.py create <skill-name> \
  --source-path <formal-skill-path> \
  --candidate-type spec-patch \
  --agent codex \
  --observation <observation-id-or-summary>
```

不要手写只含部分文件的 `source_skill.files`。完整 source hashes 是回滚和 drift 检查的根。

新候选生成的 `routing.json` 默认是 `classification.status=suggested`，只依据 Skill 名称和 frontmatter 描述形成建议，不是分类事实。人工复核必须把领域、能力、正负触发、风险和动作边界确认成 `approved`；`routing.json` 与 manifest 顶层 `routing` 必须成对出现并绑定同一 metadata hash，删除或漏写其中一侧不得绕过 post-cutover gate。普通 Skill 候选不得复制 central router。

### 4.4 Edit Candidate

只改候选目录。更新：

- `SKILL.md` / `scripts/` / `schemas/` / `references/` 中属于 scope 的文件；
- `RATIONALE.md`；
- `EVIDENCE.md`；
- `manifest.json`；
- `PATCH.diff`。

明确写出 `scope.changes` 和 `scope.out_of_scope`。

### 4.5 Validate

验证只用 fixture、临时副本、合成输入和 dry-run。禁止把验证写进真实用户数据或正式技能目录。

必跑：

```bash
python3 scripts/audit.py <candidate-dir> --json
find <candidate-dir> \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print
```

跨 Agent 候选还必须在共享候选根复跑同一组检查，确认工作区副本和共享根没有漂移。

涉及代码时，还要跑语法、单元、smoke、回归和业务最小路径。

涉及路由时还必须验证：`routing.json` 与同目录 `SKILL.md` 的名称绑定；root-id/相对路径身份、metadata/tree/profile/index hash 和运行时 root 绑定；shadow-only 拒绝 live；中英文正例、负例、显式点名、跨域、high-risk、tree-drift 与 fallback cohort；以及缺失/损坏/漂移/超时/崩溃时宿主 adapter 是否真的保持旧 catalog 可用。只跑 `synthetic_fixture` 或直接调用 `skill_router.py` 只能证明离线确定性，不能证明宿主 fallback、真实选择、token 节省或观察窗闭合。

### 4.6 Review-Seat Reports

晋升前必须有配置中要求的复核意见。默认本地配置需要三类证据：

- `implementation_audit`：实现、审计、回滚、工程风险；
- `independent_review`：独立反例、边界、回归风险；
- `business_boundary`：业务价值、用户边界、流程合规。

2026-06-11 后进入 `approved`、`promoted`、`observation_window`、`closed` 的候选，manifest 必须记录 `validation.pre_promotion_reports[]`。报告可以有分歧；分歧本身也是证据。其他部署应在 `validation.review_policy` 中声明实际席位，而不是把不存在的 Hermes/Codex/Claude Code 硬填进去。

### 4.7 Coordinator Unified Brief

Coordinator 收齐配置中要求的报告后，只向用户发一份统一简报。其他 agent 不再各自给用户重复汇总。详见第 5 章。

### 4.8 Promote and Observe

用户批准后才可晋升。晋升前必须建 rollback point；晋升后必须更新 manifest：

- `validation.status = observation_window`
- `validation.promoted_by`
- `validation.promoted_at`
- `validation.formal_post_promotion`
- `validation.post_promotion_safety`

观察窗至少需要一次真实调用、一个生产周期、或用户/配置复核席位确认目标已达成，才能闭合。

路由元数据首次晋升只能保持 `index_mode=shadow`，并预提交观测 HMAC key 的不透明 ID 与 hash。晋升授权收据必须绑定 exact candidate/PATCH/baseline；开始 shadow 观测还需要独立的签名授权收据绑定 candidate、index、key 和 `mode=shadow`。闭合时必须同时复验 HMAC 链式观测日志、其验证收据，以及签名 journal 中绑定相同 index/router/profile 的 fallback 与 registry rollback 事件。三者用途不同：授权收据证明允许做什么，签名日志证明观测未被静默改写，回滚事件证明旧 catalog 未变且可恢复；任何一个都不能替代另外两个，也不能单独证明路由质量。

路由元数据晋升不等于安装宿主 adapter，更不等于 live/default-on。写入 Hermes、Claude Code、Codex 等宿主配置或 hook，以及以后启用 live，都必须另建候选、分别复核、取得用户对准确目标和 hash 的明确批准，并保留独立 rollback point。

### 4.8a SkillSpector 观察窗证据

如果候选改变 `scripts/`、`schemas/`、`references/` 中的安全边界、发布流程、外部工具接入、权限模型或 MCP/cron/provider 行为，观察窗应记录 SkillSpector 静态扫描证据。默认只用本地静态模式：

```bash
skillspector scan <formal-skill-path> --no-llm --format json --output <candidate>/validation/skillspector-<phase>.json
```

SkillSpector 分数和 `DO_NOT_INSTALL` 只能作为上下文，不能自动决定晋升、回滚或观察窗关闭。治理类 skill 天然会触发高权限启发式规则，因此主门控必须是基线差分：

1. 晋升进入 `observation_window` 时记录 `baseline_fingerprint`、`tool_version`、完整 findings 和 YARA namespace。
2. 闭合观察窗前用同一 SkillSpector 版本重扫。
3. 只审查 `new_findings_since_baseline`。
4. 新增 `[malware]` YARA finding 或新增 confirmed HIGH/CRITICAL 且未 triage 的 finding，阻塞观察窗关闭。
5. 阻塞只表示“暂不关闭观察窗”，不自动 rollback。
6. `LOW`/`MEDIUM`、`[agent_skills]`、OSV fallback、`network_reconnaissance` 和预期治理工具能力进入 triage，不自动否决。
7. SkillSpector 版本变化必须 re-baseline，并由用户/配置复核席位人工判断。
8. LLM/provider 模式永久需要用户显式批准；不得默认使用凭据或远程评估。

结构化记录写入 `validation.post_promotion_safety.skillspector`。详见 `references/skillspector-observation-window.md`。

### 4.8b Minimal Usage Telemetry

观察窗可以引用 Skill 调用事件，但单条事件只允许包含 `ts`、`skill`、
`session_id`。`session_id` 必须是不可逆短摘要；禁止记录 tool input、prompt、
conversation、文件内容、案件内容或其他上下文字段。

候选工具见 `scripts/log_skill_use.py` 和 `scripts/usage_report.py`，事件 schema
见 `schemas/usage-event-v1.json`，隐私、兼容和安装边界见
`references/usage-telemetry.md`。日志聚合只能证明“发生过调用”；不能单独证明
输出正确、业务冒烟通过或观察窗可以关闭。任何 hook 配置写入仍是独立安装动作，
必须使用用户对该配置面的明确授权。

## 5. 统一晋升汇报

### 5.1 原则

旧方式：多个 agent 各自向用户汇报，用户看多份重复内容。

新方式：配置中的复核席位各自评估，但最终面向用户的晋升建议由 coordinator 汇总为一份简报。

这只改变呈报方式，不改变治理权力：

- 配置中的复核席位仍各自报告；
- evidence-not-authority 不变；
- 用户最终决定不变；
- 无用户批准不 formal promotion；
- value-delta gate、rollback、observation window 不变。

### 5.2 简报模板

Coordinator 给用户的统一简报建议不超过一屏：

```text
候选：<candidate-id>
目标：<one-line goal>

复核结论：
- <role>/<agent>：APPROVE / HOLD / REJECT — <one-line reason>
- <role>/<agent>：APPROVE / HOLD / REJECT — <one-line reason>
- <role>/<agent>：APPROVE / HOLD / REJECT — <one-line reason>

价值增量：<positive delta summary>
主要风险：<top risks or "none beyond observation window">
阻塞项：<blocking issues or "none">
回滚：<rollback readiness>
建议动作：请用户批准晋升 / 要求修订 / 暂缓 / 拒绝

证据位置：manifest / audit report / report message ids
```

### 5.3 分歧处理

任一 required role HOLD 或 REJECT 时，coordinator 不粉饰分歧：

- 如果是可修复实现问题，交回 implementer/auditor 修；
- 如果是价值或边界问题，呈报用户裁决；
- 如果最新报告从 HOLD 变 APPROVE，manifest 保留历史 HOLD，但 audit 以同一 reviewer 最新有效结论为准；
- user/external 记录可以作为 info 并存；是否计入 `cross_reviewed_by = all` 由 `validation.review_policy.required_roles` 决定。

## 6. 候选生命周期

### 6.1 状态

`validation.status`：

- `draft`
- `validated`
- `review_pending`
- `approved`
- `promoted`
- `observation_window`
- `closed`
- `rejected`

`observation_window` 不是完成态。闭合前必须记录：

- `closed_at`
- `closure_reason`
- `closure_evidence[]`
- `closure_reviewed_by`
- `closure_policy`

### 6.2 候选类型

- `spec-patch`：只改文档、schema、流程说明或规则文本；
- `script-enhance`：改脚本逻辑；
- `infra-fix`：修调度、路径、配置、运行环境；
- `tooling`：新增或修改治理工具。

spec-patch 不等于低风险；如果改变晋升规则、删除能力或扩大权限，仍需配置中要求的复核报告和用户批准。

### 6.3 Manifest v3 要点

关键字段：

- `source_skill.path/tree_hash/files`
- `candidate.path/tree_hash/files`
- `rollback_hashes`
- `scope.changes`
- `scope.out_of_scope`
- `relationships`
- `rights_provenance`
- `validation.value_delta`
- `validation.empirical_scorecard`
- `validation.pre_promotion_reports[]`
- `validation.review_policy`
- `validation.formal_post_promotion`
- `validation.post_promotion_safety`
- `routing.required_on_promotion/metadata_path/metadata_sha256`
- `routing.classification_status/index_mode/tree_hash_algorithm`
- `routing.attestation_key_id/attestation_key_sha256`
- `validation.routing_shadow`

常见枚举：

- `cross_reviewed_by`: `none | hermes | codex | both | claude-code | all | configured | user-waived`
- `promotion_mode`: `none | human_patch | user_delegated_agent_patch | rollback`
- `empirical_scorecard.status`: `measured | not_applicable | not_measured`
- `relationships.sublation_pattern`: `single_skill_patch | cross_skill_absorption | skill_merge_plan | skill_split_plan`

`validation.review_policy` 可声明默认三 agent、多 agent 替代、单 agent 或用户豁免模式。没有该字段时，audit 保持本地默认三席：`claude-code`、`codex`、`hermes`。任何非默认模式必须记录用户授权证据。

post-cutover 候选的 `routing` 不能因删除 `routing.json` 或漏写 manifest block 而消失。`validation.routing_shadow` 只在经授权的真实 shadow 观察窗闭合时成立，必须绑定 shadow index/router/profile hashes、`authorized_shadow_runtime` 报告、HMAC 日志及验证收据、签名授权收据、rollback 事件和独立复核；离线 fixture 不得填成该闭环证据。

完整 schema 见 `schemas/manifest-v3.json`。

### 6.3a Value-Delta Delivery Report

交付报告必须把数字分为 `measured`、`estimated` 和
`not_measurable` 三档，禁止混档。`estimated` 必须同时给出公式和假设；
`not_measurable` 不得出现伪造的数值字段。使用
`scripts/delivery_report.py` 从结构化输入生成确定性 Markdown，输入契约见
`schemas/delivery-report-input-v1.json`，口径与触发边界见
`references/value-delta-delivery-report.md`。

如需在 manifest 中登记报告，只写
`validation.delivery_report.path/sha256/generated_at`。该字段证明报告工件的
身份，不替代 `value_delta`、实证分数卡、三席复核或用户晋升决定。


### 6.4 决策历史与非作者复跑

2026-06-11 后的新候选应把复核、修订和观察窗学习写成可追溯因果链：

- `validation.decision_history[]`：记录 `diagnosis -> action -> evidence -> outcome`，并用 `trigger.id` 链接报告、审计、用户决定或观测。
- `validation.independent_reproduction`：晋升前至少一名非作者复跑。初始门槛为一人；若再次出现镜像漂移或复核逃逸事故，再提高到两人。
- `validation.rejected_alternatives[]`：只记录有意义的设计分叉、spec-patch、吸收、review conflict 或 routing 取舍；小修小补不强制。
- `redacted_reporting`：在 manifest 顶层标注可共享证据与本地敏感上下文，登录墙、cookie path、page body、用户数据等不得直接进入用户简报。

`observation_window` 的后续学习也写入 `decision_history[]`，使用 `phase: observation_window`，不要另造平行四元组。缺少 `decision_history[]` 的 post-rule 晋升候选先给三个月 warning 过渡，再升级为 hard fail。

### 6.5 Strict Audit

默认 `audit.py` 是 strict。晋升前不要用 `--no-strict` 逃避问题。重点检查：

- 候选不在 formal path；
- 无 bytecode；
- PATCH.diff hunk header 合法；
- source baseline 未漂移；
- formal_post_promotion 当前；
- manifest 自洽；
- rights/provenance；
- post-promotion safety；
- empirical scorecard；
- value_delta；
- pre_promotion_reports。

### 6.6 顺序晋升和漂移

同一 skill 的多个候选依次晋升时，后一个候选可能改变前一个候选记录的正式快照。观察窗内候选出现 `formal_post_promotion` drift 必须解释：刷新快照、缩小检查范围、闭合观察窗或创建治理候选。不要为了消除 warning 回滚已批准的正向晋升。

### 6.7 候选层镜像漂移

候选层也会发生路径错配。工作区 audit passed 不等于共享根 audit passed。进入 coordinator unified brief 前必须确认：

- workspace candidate 与 shared-root candidate 的关键文件一致；
- shared-root candidate 也能通过 strict audit；
- **audit report 的 `candidate_path` 必须指向共享根，而非 agent workspace**——如果 audit report 里的 `candidate_path` 是 Codex/Claude Code 的本地工作区路径，说明该 audit 从未在共享根上跑过，不得采信为"共享根已通过"；
- `PATCH.diff` 能在当前 formal baseline 上 dry-run/apply-check；
- 删除文件不会留下零字节空壳；
- 报告中的 line count、hash、audit 数字来自实测。

这条是 post-promotion strong path check 在候选层的等价护栏。

**常见漂移模式**：agent 在工作区删除 `__pycache__`/`.pyc` 后跑 audit → audit passed，同步到共享根时遗漏了删除动作 → 共享根 audit 仍显示 passed（如果 audit script 的 bytecode 检测不覆盖该路径），但 `find` 仍能找到残留字节码。检测方法：`find <shared-root> \( -name '__pycache__' -o -name '*.pyc' \) -print`，不应依赖 audit 的 `no_bytecode_artifacts` 单点。

## 7. 设计模式

### 7.1 Provider Contract

数据源技能必须区分：

- `ok`：数据源正常；
- `empty`：正常为空；
- `blocked`：来源阻断；
- `login_required`：需要人工登录；
- `captcha_pending`：需要用户完成验证码；
- `disabled`：明确停用；
- `mcp_placeholder`：预留接口，不追踪为缺陷。

参考 `references/provider-contract-pattern.md` 和 `references/human-in-the-loop-login-wall.md`。

### 7.1a Scenario Taxonomy And Routing Boundary

`references/scenario-taxonomy-and-routing-boundary.md` 与
`scripts/scenario_map.py` 保留的是 v1 人工场景目录：它适合说明 workflow
归属和兄弟 Skill 交接，不是 central router 的运行时索引，也不自动改变宿主
catalog。每个进入该目录的 Skill 仍必须显式声明：

- 至少一个 `scenarios`；
- `routing_boundary.primary_when`；
- 不适用条件、澄清条件和必要的兄弟 Skill 交接。

使用 `scripts/scenario_map.py` 从
`schemas/scenario-taxonomy-v1.json` 的结构化输入生成确定性 Markdown。
地图只做路由目录，不安装 Skill、不调用 Skill、不自动改写其他 Skill
frontmatter，也不把相邻能力合并为一个治理对象。

### 7.1b Central Router 与宿主 Adapter

自动分类使用每个 Skill 的 `routing.json`、全局
`references/skill-routing-taxonomy-v1.json` 和 central
`scripts/skill_router.py`。`references/scenario-routing-migration-v1.json`
只提供旧场景 ID 到新 domain/capability 的迁移建议，不能自动批准分类。
`primary_domain` 只是粗排先验，能力可多选，负触发、澄清条件和显式点名
仍参与判断。

索引以 `root_id:relative_path` 标识运行画像，并绑定 Skill tree、metadata、
profile set、taxonomy 和 router hash；它可删除重建，不能反向覆盖
`routing.json`。索引也不携带宿主全部启停、平台、依赖、隔离、命名空间和
优先级事实，因此每个宿主 adapter 必须把建议与自己的 active catalog
求交集，再由宿主完成授权、安全和依赖检查。当前候选未安装任何宿主
adapter；详细 shadow、fallback、收据和观察窗契约见
`references/skill-routing-shadow.md`。

### 7.2 Cross-Skill Absorption

吸收不是吞并。target 吸收 donor 的局部优势，同时保留 target 的主结构和 donor 的关键能力。必须记录：

- donor skill；
- absorbed capability；
- retained boundary；
- rights/provenance；
- fallback；
- 用户批准删除或 alias 改动。

参考 `references/cross-skill-absorption-canghe-baoyu-comic.md` 和 `references/absorbed-target-routing.md`。

### 7.3 Skill Merge and Split

合并候选必须证明：

- 合并后入口更清；
- 旧 workflow 有映射；
- 能力没有静默收缩；
- donor 删除另行批准；
- 观察窗可以覆盖主要路径。

拆分候选必须证明拆分降低复杂度，而不是制造更多治理对象。

### 7.4 Spec-Only Candidate

纯文档候选也要有价值增量。典型用途：

- 补治理账本；
- 明确边界；
- 归档过时经验；
- 更新汇报/复核流程；
- 将分散规则收束到 reference。

### 7.5 External Evaluator Adapter

外部评估器只能读候选、产报告、给风险评分。禁止安装时写 formal skill，禁止 optimizer/sync/load_skill 自动落地。参考 `references/external-evaluator-adapter-agent-insight.md` 和 `references/darwin-evaluator-adapter.md`。

### 7.6 Business Smoke Test

框架 audit 全过只证明结构正确，不证明业务可用。晋升后必须跑业务烟雾测试，至少覆盖：

- 合约章节存在；
- workflow 步骤完整；
- 关键能力字面保留；
- 正/负 fixture；
- 真实路径最小调用。

参考 `references/business-smoke-test-pattern.md`。

### 7.7 Upstream Sync

对外部来源或上游 repo 做 sublation 前，先确认本地不是旧版本。`hermes skills update` 对 local source 返回 No updates 不代表最新。需要 clone/diff/rollback 证据。参考 `references/upstream-skill-sync-methodology.md`。

### 7.9 Report-Only Boundary Inventory Candidate

A `report-only` candidate documents the current state of a skill cluster without changing any code. It is the safest first step before any merge, absorption, or routing proposal.

Typical deliverable:
- Inventory table: all cluster skills across agent roots, with path, size, files, role, and lane assignment
- Byte-identical evidence: sha256 comparison of shared scripts across skills
- Lane grouping: functional-layer grouping with per-lane treatment recommendation
- Boundary conclusion: merge / donor-main-entry / keep-distinct / supersession-report / hold
- Risk report: credential, functional, compliance, and governance risks per lane
- Exclusion list: symlinked `.agents` skills, research engines that aren't crawlers, desktop clones

This candidate type should be created BEFORE any merge proposal for multi-skill clusters. It prevents premature merging and forces the coordinator to verify the actual disk state before recommending actions.

### 7.10 Donor Boundary Retention

When a skill declares `absorbs` in its metadata and contains byte-identical copies of donor scripts, it is a `donor boundary` relationship — the umbrella skill is the main entry, but the donor skills remain as retained backends. This is NOT the same as formal absorption (where donor directories are deleted or aliased).

Evidence required:
- sha256 verification that key donor scripts are byte-identical inside the umbrella
- Confirmation that the umbrella adds new capabilities beyond the donors (post-processing, routing, compression, etc.)
- Documentation that donors are retained, not deleted

Next steps after donor boundary report:
1. Add DONOR_BOUNDARY.md or PORT_NOTES.md to the umbrella skill documenting the relationship
2. Keep donor directories intact
3. Do NOT write `absorbed_into` metadata, do NOT delete donors, do NOT create aliases
4. Wait for user approval before any destructive cleanup

This pattern is common in unified tool skills (e.g., media-toolkit absorbing universal-media-downloader and douyin-batch-download while keeping both as backends).

### 7.11 External Project Evaluation ("老样子")

When the user says "老样子" and provides a GitHub URL, the standard workflow is clone → evaluate → report, without automatically connecting to sublation. This is broader than skill evaluation — it covers any external project (tools, libraries, platforms). The user may decide to install directly ("装") or later do sublation ("扬弃"), but the default evaluation does not create candidates or observations.

Reference: `references/external-project-evaluation.md`

### 7.12 Tier-0 Absorption of Large External Projects

When a large external project (100MB+, full-stack SaaS, Docker/Tauri, auth/payment) has analytical value but deploying it would be operationally expensive, use the Tier-0 absorption pattern: extract only the data layer as a lightweight MCP, never deploy the platform. Document the full pattern at `references/worldmonitor-tier0-absorption.md`.

- `__pycache__`、`.pyc`、`.orig`；
- 个人路径和内部样本；
- 过时候选；
- 未入账正式漂移；
- README、LICENSE、audit report。

参考 `references/github-release-checklist.md`、`references/pre-release-audit-pattern.md`、`references/github-release-workflow.md`。
