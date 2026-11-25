---
name: dev-workflow
description: Use when a development task could change code, behavior, configuration, UI, data flow, integration contracts, or workflow policy, including features, fixes, refactors, and delivery work.
---

# 开发工作流路由与执行指南

## 插件路径约定

本文用 `<plugin-root>` 表示插件仓库根目录，不是 `skills/dev-workflow` 目录。

本仓库结构固定为：

```text
<plugin-root>/
  skills/dev-workflow/SKILL.md
  scripts/workflow-state.sh
  scripts/learnings.sh
  scripts/codegraph-judge.sh
```

如果当前 skill 文件路径是：

```text
.../tiers/skills/dev-workflow/SKILL.md
```

那么 `<plugin-root>` 是：

```text
.../tiers
```

正确脚本路径示例：

```bash
<plugin-root>/scripts/workflow-state.sh check
```

错误示例（不要这样拼）：

```bash
<plugin-root>/skills/dev-workflow/scripts/workflow-state.sh check
```

执行脚本前按以下顺序解析：

1. `DEV_WORKFLOW_PLUGIN_ROOT`
2. `CODEX_PLUGIN_ROOT`
3. `CLAUDE_PLUGIN_ROOT`
4. `CURSOR_PLUGIN_ROOT`
5. `TRAE_PLUGIN_ROOT`
6. 若是从本文件路径推断，则从 `skills/dev-workflow/SKILL.md` 上溯两级到仓库根目录

脚本自身也按同样规则自动推断，Codex 环境不要依赖 Claude 专属变量。

## 控制器硬门（最先执行）

<!-- SELF_HOSTING_CONTROLLER -->

`<plugin-root>/scripts/workflow-state.sh` 是本次会话唯一的工作流 controller。即使当前工作区正好是 tiers/dev-workflow 自身，工作区里的 `scripts/workflow-state.sh` 也只是**待修改代码**，不得拿它代替安装版 controller；controller 必须从当前已加载 skill 的路径或上述环境变量解析。

按以下短契约执行，后文只解释细节：

1. 先用 controller 执行 `init` 与 `check`；若存在同目标未完成状态则续行，已封存或 empty slot 用 `start <task> <level>`，Goal 只用 `continue-goal`。需要切换任务时，合法顺序固定为 `suspend <key>` → `start <task> <level>` → 当前任务封存后 `resume <key>`；禁止伪造 complete 或手换 YAML。
2. 新任务从 `align` 开始。AI 根据用户描述和仓库事实判断 `ready / clarify / challenge`：需求清晰时直接写入理解证据、运行 `understand <evidence>` 并进入 `execute`；只有关键结果不明确时才暂停澄清。
3. brainstorming、grilling、spec、plan 和 TDD 都是按需能力，不是 tier 自动触发的固定阶段。用户显式指定时必须遵循；未指定时由 AI 按不确定性、风险和可验证性选择。
4. L0–L3 进入 `execute`、`tdd`、`review` 或完成验证前，understanding 必须有效且仍匹配当前目标范围。实现、review 和 complete 使用同一个 controller。
5. controller 不可用、路径无法确认或理解/完成硬门失败时，输出 BLOCKED/降级原因并停下，不得改用工作区内同名脚本绕过。

## 使用时机

每次接到新的开发任务时，先跑决策树确定级别，再按对应步骤执行。

## 适应式意图对齐（默认入口）

先判断意图状态，而不是先选择一条固定 skill 流水线：

```text
ready     → understand → execute
clarify   → brainstorming 或逐题澄清 → ready
challenge → grilling 聚焦未决风险 → ready / BLOCKED
```

- **ready**：目标、关键行为、边界和验收方式可由用户描述与仓库事实确定。需求清晰时直接进入 `execute`，不要求用户重复批准，也不强制生成 spec/plan。
- **clarify**：存在会实质改变结果的互斥选择、缺失验收标准或目标与仓库事实冲突。brainstorming 按需使用，每次只问一个真正阻塞的问题。
- **challenge**：已有方向明确，但存在高风险假设、相互矛盾约束或不可逆动作。grilling 按需使用，只挑战未决风险，不重复盘问已确认内容。

brainstorming 与 grilling 不得因 L1/L2 等级自动串联。用户显式指定某个 skill、TDD 或执行模式时，用户指定优先。AI 可以自主决定命名、局部结构、测试组织和仓库内可推断的低风险实现细节；只有新增权限、发布/部署、删除、付费、凭证/隐私访问、不可逆操作或关键产品选择缺失时才必须暂停。

## 能力模式与依赖兜底

本插件的核心路径必须在只安装本插件时可用；外部 skill、MCP、CLI 都是增强能力，不是硬依赖。

开工或排障时可运行：

```bash
<plugin-root>/bin/doctor [--repo <repo>] [--install-deps]
```

- **base**：只依赖本插件内置流程和必需命令。可以完成意图对齐、按需澄清、实现、验证与收尾；spec/plan/TDD 都是可选策略。
- **enhanced**：检测到 superpowers、codegraph 等伴侣能力时，优先调用对应 skill/CLI 增强体验。
- **full**：额外检测到设计保真、已建图 codegraph 等环境时，开启更完整的客观校验。

执行规则：
- 若本文点名的外部 skill 可用，优先按该 skill 执行。
- 若不可用，不要卡住或要求用户先安装；改走本文写明的**内置协议**。
- 不静默安装依赖。只有用户显式要求或传 `--install-deps` 时，才安装可脚本化依赖；MCP/登录类能力只提示下一步。
- 若用户问“为什么某功能不可用”，先跑 `bin/doctor` 给出能力矩阵，再决定是否安装或降级。

## 对抗评审关卡（provider 分层）

对抗评审是独立关卡，不绑定某个外部 CLI。目标是让至少一个“反方视角”专门找风险，主流程负责裁决。

**默认策略：外部评审默认关闭。** L0–L4 先完成与风险相称的本地验证、影响面检查和内置对抗 checklist；外部 CLI / 平台多模型是用户选择的发布前加固，而不是普通实现或小修复的默认完成门。主流程认为高风险值得额外复审时，可以说明风险、推荐并行运行，但必须由用户明确接受后才设置 `requirements.external_review=true`。

触发规则：
- L0/L1：默认执行内置 checklist；用户明确要求发布前外部复审时，再执行外部交叉评审。
- L2：影响面大、安装/配置/数据迁移/权限相关时必须做更深入的本地影响面审查；只有用户选择外部复审时才调用 provider。业务领域关键词不能单独开启外部完成门。
- L3：复杂根因、偶现 bug、修复路径有替代解释时执行内置 checklist；窄修复不等待外部 provider。
- L4：默认跳过对抗评审。

provider 优先级：
1. **外部交叉评审（external-cross-review）**：仅当用户已明确选择外部复审、且 `external-agent` 可用并且 `bin/doctor` 显示 `Adversarial review: external-ready`（或 `external_agent.py --list` 显示 ≥2 个不同家族外部 CLI 候选）时，使用 `external_agent.py --cross-review <a>,<b>` 做只读 review。调用前同时检查 `health_status`、`routing_priority` 与 `recommended_timeout_seconds`：优先 `routing_priority=normal` 的不同家族组合（通常 `grok` / `cursor` / `mimo`）；`antigravity` 标记为 `slow`/`degraded` 时降为后备，用户明确指定时仍按建议超时调用并报告状态。runner 会并行启动 reviewer；standard profile 必须实际返回 ≥2 个不同家族的成功结果且 `quorum=true` 才算通过。认证失败、空产出、部分失败或只剩同家族 provider 时只算二次意见，不算完整交叉评审。符合「小修复快速通道」时，改用下面的显式 small-fix 降级契约。
2. **平台多模型降级（platform multi-model fallback）**：外部交叉评审已真实运行并保存 `success=false`、`quorum=false`、`outcome=failed` 的证据后，若 host 能指定模型，可并行启动两个不同非 root 子代理，要求两个不同模型、两个不同角色：`correctness-regression` 与 `security-degradation`。两者必须审查同一冻结 fingerprint / artifact / prompt，主流程逐条裁决后生成 `tiers.platform-review/v1`。该证据可以满足标准完成门，但必须保持 `quorum=false`、`platform_quorum=true`，不能冒充 external quorum。用户终止外部评审后不得启动 fallback；`outcome=terminated` 永远不能触发降级。
3. **平台子代理补充（platform-agents）**：没有两个可辨识模型、未获得平台子代理授权、或不存在合格外部失败证据时，平台 reviewer 只能作为补充意见，不能满足 `requirements.external_review=true`。可使用不同审查角色，但同模型不同 prompt 不构成正式 platform fallback。
4. **内置对抗 checklist（built-in）**：没有任何 provider 时也必须可执行。检查：最可能的回归点、缺依赖/缺 MCP 降级路径、安装脚本是否静默改环境、README/skill/脚本承诺是否一致、测试是否覆盖失败路径。

纪律：
- 不为对抗评审静默安装 provider；需要安装时只提示 `bin/doctor --install-deps` 或登录步骤。
- 只读 review 默认不允许写文件。外部或子代理输出是证据，不是结论，主流程必须逐条裁决。
- 若用户未选择外部复审、未授权平台子代理/外部 agent，或 provider 超时/degraded，则走内置 checklist 并不阻塞交付；只有已显式开启 `requirements.external_review=true` 的任务必须在 final 里标明外部门未完成，不能写成已过完整对抗评审。
- 收尾时必须展示采用的 provider、review 摘要、主流程裁决；平台降级通过时固定写 `external cross-review failed; platform multi-model fallback passed`，禁止写“external quorum passed”。若本应外部交叉评审但未完成，必须明确写出阻塞原因，禁止静默降级后声明“已完成”。

完整交叉评审使用同一冻结输入并保存本地 JSON 证据。报告绑定当前 Git snapshot fingerprint，并且 `complete` 只接受 24 小时内、仍匹配当前仓库状态的 quorum：

```bash
python3 <plugin-root>/scripts/external_agent.py \
  --cross-review auto --orchestrator-family openai --progress jsonl \
  --cd "$PWD" --context git --format json \
  --PROMPT "只读审查当前改动，只报告有证据的问题" \
  > docs/superpowers/.workflow-evidence/external-review.json
```

若上述调用正常结束但输出 `outcome=failed`，host 才能启动正式平台降级。两个 reviewer 必须收到同一冻结输入并记录唯一 `agent_id`、规范化后不同的 `model`、固定 `role`、`verdict`、结构化 `findings` 与非空 `result`。主流程保存外部失败证据的仓库相对路径及 SHA-256，逐项生成精确 adjudication；blocking finding 必须修复，不能记为 `accepted-risk`。最终先本地验证，再把 `evidence.external_review` 指向 platform 报告：

```bash
python3 <plugin-root>/scripts/platform_review_contract.py \
  --validate docs/superpowers/.workflow-evidence/platform-review.json \
  --fingerprint "$(python3 <plugin-root>/scripts/external_agent.py --fingerprint --cd "$PWD")" \
  --reference "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" \
  --profile standard --repo "$PWD"
```

`external_agent.py` 只负责严格执行外部策略并保存成功、失败或终止证据，不会自行启动平台子代理；平台调度、模型身份校验、裁决与 `tiers.platform-review/v1` 生成均由 host orchestrator 负责。

`--progress jsonl` 把 `cross_review_started` / `review_started` / `review_finished` / `policy_satisfied` / `cross_review_terminated` / `cross_review_finished` 实时写到 stderr；stdout 只保留最终 JSON，可稳定重定向为完成证据。这些事件只提供可观测性，不会降低 standard 双家族 quorum。`auto` 会按安装状态、provider 健康和家族去重选两个 reviewer，`--orchestrator-family` 用于排除主流程自身家族。当 `opencode` 的实际 provider 家族无法证明时，auto 不会把它当成独立家族候选；只有 operator 能核实 provider 时才显式指定。standard 未显式传 `--timeout` 时，provider 建议最多只能把单 reviewer 等待抬到 600 秒；显式 timeout 仍可覆盖该上限。

small-fix 仍从两个不同 family 启动 reviewer，但默认每个 90 秒；第一个有效外部意见返回后即可取消仍在等待的 reviewer：

```bash
python3 <plugin-root>/scripts/external_agent.py \
  --cross-review auto --orchestrator-family openai \
  --review-profile small-fix --progress jsonl \
  --cd "$PWD" --context git --format json \
  --PROMPT "只读审查这个已冻结的窄修复，只报告有证据的问题" \
  > docs/superpowers/.workflow-evidence/external-review.json
```

这时 `success=true` 只表示 small-fix policy 已满足；若只有一个成功 reviewer，报告必须保持 `quorum=false`、`outcome=degraded`，不能宣称完整双家族评审。失败/超时/取消/用户终止统一保存 `review_profile`、`policy`、`outcome`、起止时间、总耗时，以及每个 reviewer 的 `status`、耗时、timeout 与 error/result；用户终止必须是 `outcome=terminated`，永远不能通过完成门。

---

## 快速启动：续行、意图与风险

接到开发需求后快速完成三项内部判断，不把它们变成用户必须逐项确认的仪式：

1. **读续行状态**（见下方「跨 session 续行」）。存在未完成且与当前目标不同的任务时才提示「继续 / 换新任务」；同目标直接续行。
2. **判断意图状态**：`ready / clarify / challenge`。只有后两者存在关键开口时才暂停。
3. **风险判级**：tier 用于决定验证深度与影响面证据。级别会显著影响执行或用户可能关心时，输出：

   ```
   级别 = Lx｜理由 = <一句话，对应决策树哪一问命中>
   ```

   清晰的小任务可以在 commentary 中简短说明或内部记录，不因固定格式阻塞执行。判级被用户纠正时仍按自主进化规则记录。

进化扫描是非阻塞维护动作：发现同类纠正达到阈值时提出固化建议，但不应暂停当前清晰任务；只有真正修改全局规则时才等待用户确认。

### 当前会话两阶段判级

判级对象是**当前会话这一个任务的真实增量**，不是仓库总体复杂度、上一任务遗留 diff、文件所在业务领域或请求里的某个关键词。

1. **初判**：根据当前目标、预计生产改动、是否改变既有消费者/契约，输出初始级别。
2. **影响面校准**：读完消费方、锁定本任务 base/checkpoint、看到实际 diff 或 task-scoped codegraph 后重新判断。证据与初判不一致时必须**自动重判**，可以升级也可以降级，并说明是哪项当前会话证据改变了结论，不等待用户再次纠正。

每次判级至少回答：本会话究竟改变什么生产行为；哪些既有消费者或契约可能回归；是否仅通过新的显式入口可达；是否改变控制流、持久化、API/schema、权限或跨端时序；哪个 task base 与哪些测试界定了影响面。

“新增”不自动等于 L1/L2；“位于业务代码附近”、改动文件数、codegraph risk 或某个领域关键词也不能单独定级。**隔离新增可判 L3**：入口显式、旧消费者/路由完全不变、回归边界可由本地契约测试覆盖。**静态资源路径替换可判 L4**：仅替换等价资源地址，不改变渲染逻辑、控制流、API/schema 或消费者语义，并补构建/资源可达性验证。

**判级 tie-breaker（完成当前会话影响面校准后仍拿不准时）：** 在两级之间犹豫，走更严的那级。禁止跳过消费方/契约检查，直接用 tie-breaker 把所有任务推到 L2。
- L1/L2 之间拿不准 → 按 **L1**（补完整 acceptance 与边界证据）
- L2/L3 之间拿不准 → 按**有回归风险**处理，补测试
- L3/L4 之间拿不准 → 按 **L3**（先复现再改）
- 跨医生端/患者端等双端，并同时涉及 API、IM 或 SSE 编排的业务闭环 → 默认至少 **L1**；即使后端接口和类型已经存在，也不得按普通接口封装降为 L2。只有改动被证明局限于单端、单一既有调用点且不改变跨端时序时，才允许重新评估为 L2。

拿不准时增加验证深度，不自动增加对话步骤。

---

## 决策树

```
Q0: 涉及多个已有模块的结构性重组或架构迁移？
  → 是 → L0
  → 否 → Q1

Q1: 新增完整模块、完整用户流程、跨模块编排，或存在多个未决行为分支？
  → 是 → L1
  → 否 → Q2

Q2: 是否改变既有共享逻辑、契约、消费者、控制流或跨端时序？
  → 是，修复已知错误行为 → L3
  → 是，新增/调整既有行为 → L2
  → 否 → Q3

Q3: 是否为显式入口后的完全隔离新增，旧消费者和旧路由保持不变？
  → 是 → L3（impact evidence + 本地契约测试）
  → 否 → Q4

Q4: 是否仅为文案/样式或等价静态资源路径替换，运行逻辑不变？
  → 是 → L4
  → 否 → 回到消费方与契约检查；证据不足时偏严
```

L2 vs L3 的区分不看“是不是新增”这个词：**改变既有行为/消费者的迭代 → L2；已知 bug，或无既有回归面的隔离新增 → L3**。

---

## 理解度关卡（各级通用）

进入 `execute` / `tdd` 前，先过一道与本级匹配的理解度自检。共同退出标准：**目标、关键边界和验收方式是否足以让 AI 自主完成**。`ready` 可直接生成 evidence 并通过；`clarify/challenge` 才暂停处理未决问题。过不了关卡也可能是判级错了，应重新评估。

| 级别 | 动手前要"懂"的对象 | 没懂时 |
|---|---|---|
| L0 | 架构边界 / 迁移 / 回滚路径 | 留在 spec/architecture review；边界未锁定不得进入实施 |
| L1 | 需求 / 设计（决策树分支、边界） | 关键行为不清则 brainstorming；高风险假设未决则 grilling；否则直接 ready |
| L2 | 改动的影响面 / 回归边界 / 能否写出覆盖测试 | 跑 `codegraph-judge assess` 看 affected flow / test gap，或直接读消费方；**影响面超预期（跨模块/结构性）→ 回去重判级（可能 L1/L0）** |
| L3 | bug 的真正根因；或隔离新增的消费者/契约边界 | bug 答不上根因就留在 `systematic-debugging`；隔离新增答不上“为何旧路径不受影响”就改按 L2/L1 评估 |
| L4 | （风险≈0，免） | — |

L0–L3 把理解证据写入 `docs/superpowers/.workflow-evidence/`，再运行 `workflow-state.sh understand <仓库相对证据路径>`。证据按 tier 分别包含 architecture 的 `boundaries/migration/rollback`、requirements 的 `acceptance/non_goals`、impact 的 `affected/tests`、root-cause 的 `reproduction/root_cause`；L3 bug 使用 root-cause，L3 隔离新增使用 impact；共同要求有且仅有一个 `result: PASS`。清晰任务的 evidence 可由 AI 根据描述与仓库事实直接生成，它不等于用户审批。`execute`、`tdd`、`review`、`business-verify`、`fidelity-verify` 与 `complete` 都会重新校验 scope/evidence hash，目标、范围、requirements 或证据变化后必须重新理解，不能只改 status。

同一 task/target 发生 L3→L1 等重判时，不重写已通过的根因。新 evidence 仍补齐当前 level 的必需字段，并用 `reuses:` 指向上一份 evidence；controller 会校验稳定 objective、旧 kind 与两个文件 hash：

```text
result: PASS
kind: requirements
acceptance: 发送成功清空输入；发送失败保留内容并可重试
non_goals: 不改变 IM 协议、API 或跨端时序
reuses: docs/superpowers/.workflow-evidence/root-cause.txt
```

## 小修复快速通道（small-fix）

这是显式 profile，不是新的风险等级。必须同时满足：已有行为的稳定 bug 复现；同一单端/单目标；预计生产改动 ≤3 文件；有目标 Red/Green；不新增 API/schema、权限、数据迁移、依赖或跨端时序。IM/auth/payment 等领域不自动排除，但只要改变契约、守卫、传输或跨端编排就不合格。实现后发现超出边界，立即切回 `standard`，不得继续使用降级 review。

进入时设置：

```bash
<plugin-root>/scripts/workflow-state.sh set execution.profile small-fix
```

small-fix 只压缩重复流程，不压缩真实性：

- L3→L1 复用 root-cause，只补新增 acceptance/non-goals；这份补充就是轻量 spec，不因重判补写此前并不需要的 brainstorming、grilling、spec 或 plan 文档。
- 能稳定复现的 bug 优先 Red/Green；其他任务选择能覆盖风险的验证方式。再从目标测试、typecheck、lint、build、浏览器或请求演练中选择必要门；只有共享基础设施、配置或影响面扩大时才跑全量四连。
- codegraph 对高风险业务最多跑一次；不可用时保持既有人工影响面降级。
- 用户显式选择外部复审时，冻结 diff 后可与 business verification 并行，墙钟取两者最大值；未选择时不启动 provider。
- 用户明确关注速度时优先判断是否符合 small-fix，不先启动 standard 长评审。用户要求停止时立即终止 reviewer、保存 terminated evidence，并停止后续门禁。
- 等待更新只在 reviewer 成功/失败/超时/取消等**状态变化**时输出；没有新信息不得每 30 秒刷屏。用户主动询问状态时可以简短响应一次。

---

## 设计保真验收关卡（各级通用，收尾 HARD-GATE）

理解度关卡守"动手前懂没懂"，这道关守"做完后是否按设计源完成"。**凡产出可见 UI 且有设计稿（Figma 等）的任务，不论判到 L1/L2/L3/L4，收尾标 done 前必过此关。** 纯逻辑改动、无设计稿的 UI 文案微调豁免。

> ⛔ **HARD-GATE（保真收尾强制，优先级高于"渲染无报错就算完"的直觉）**
> 凭「页面可渲染 / 关键标题在场 / 视觉上大致接近」**不算对齐设计稿**，禁止据此声明 done。必须做完下面**两步，缺一不算过**：
>
> 1. **整屏完整性核对** — 逐区块对设计稿核对「有无漏做整块区域 / 组件范式是否一致」。防止只看到局部元素就误判整屏已完成。
> 2. **逐元素量化比对** — 关键元素的设计稿量化值（尺寸 / 圆角（含单角圆角）/ 色值 / 字号字重 / 间距 / 描边）用 **DOM inspect / 实测**逐项对设计真值，**禁凭"看着像 / 渲染无报错"放行**。
>
> **取数与执行纪律：**
> - 设计真值由**取数中枢 REST 直取**（Figma REST 等：图片导出 + 节点树量化值），不要依赖视觉印象或二手描述猜测。
> - 实现可委派，但**验收必须由主流程本端完成**（preview 逐区 inspect），不能只依赖实现方自报"已对齐"。
> - 配套方法见 skill `figma-fidelity-verification`（含 REST 取真值 → 写 death-spec → 派 agent 实现 → 逐区量化验收的完整 loop，本文不重复其内容）。
>
> **未过此关不得标 done。** 自检红旗：当你准备说"对齐设计稿了 / 这个页面做完了"，但**本任务还没做整屏核对 + 逐元素 inspect**——立即停下，回到关卡。

> 状态机（L1 或高风险 L2/L3）：收尾前进入 `fidelity-verify`，写入 `evidence.fidelity` 后再用 `workflow-state.sh complete`；禁止直接 `set phase done`。见下方「跨 session 续行」。

## 业务闭环验收关卡（L1/L2/L3 通用，收尾 HARD-GATE）

凡涉及 auth / route guard / API integration / order / IM / prescription / payment / 数据写入 / 权限守卫等真实业务链路，收尾标 done 前必须证明业务闭环真实成立。**页面能打开、组件能渲染、mock 数据可见、类型检查通过，都不能替代业务闭环验收。**

> ⛔ **HARD-GATE（业务闭环完成强制）**
> 必须给出本端执行过的证据，缺一项就不能说完成：
>
> 1. **入口与守卫** — 未登录、已登录、深链/刷新、无权限或过期态按需求表现；不能出现未登录可进受保护首页这类绕守卫路径。
> 2. **真实请求** — 关键动作必须触发预期真实接口；记录方法、URL/路由、状态码、关键 request/response 字段。若环境只能 mock，必须明说“未过真实请求验收”，不能标 done。
> 3. **端到端结果** — UI 状态、服务端/持久化状态、错误态/401/403/失败路径至少覆盖任务核心分支。
> 4. **证据清单** — final 输出必须列出测试命令、浏览器/接口演练、codegraph 结果、对抗评审 provider 与裁决、仍未覆盖的风险。
>
> 高风险业务闭环任务（auth、路由守卫、API 写入、订单、IM、处方、支付、权限）在完成前还必须跑 `codegraph-judge assess`；若 codegraph 不可用，只能记录“codegraph 降级为人工影响面审查”的证据，不能省略影响面审查。人工影响面审查至少要列：改动文件清单、每个文件影响、受影响业务 flow、测试缺口、为什么仍满足 L1/L2/L3 判级。
>
> 状态机（L1 及所有高风险业务 L2/L3 强制）：设置 `requirements.business=true`，收尾进入 `business-verify`；若同时有设计稿，再设置 `requirements.fidelity=true` 并进入 `fidelity-verify`。业务闭环不再自动设置 `requirements.external_review=true`；用户明确要求发布前外部复审时才设置它。证据文件齐全后只能用 `workflow-state.sh complete` 完成，禁止直接 `set phase done`。

`business-verify` 未完成只阻塞 `done`、merge、ship、deploy 和“业务已闭环”声明；代码已通过目标验证与必要静态门后，可以创建本地 **checkpoint commit** 保存工作。commit 后状态仍停在 `business-verify`，final 必须明确未闭合证据，不能把“已提交”写成“已完成”。

---

## codegraph 辅助判级与收尾证据（三层降级）

L2 及以上、或判级拿不准时，跑 codegraph 守卫获取客观信号；高风险业务闭环任务在收尾前必须把 codegraph 结果或降级原因写进证据清单：

```bash
<plugin-root>/scripts/codegraph-judge.sh [--repo <repo>] [--base <base>] assess
```

- **退出码 0**：已输出风险摘要，按下表校准级别。
- **退出码 3**：codegraph 不可用 → 降级为纯人工判级，继续流程。

**判级校准阈值（提示非硬覆盖，冲突偏严，与 tie-breaker 一致）：**

| 图信号 | 判级含义 |
|---|---|
| risk ≥ 0.4 / 改动文件 ≥ 8 / 有 affected flow | 至少 L1，判更低要重审 |
| 有 test gap 且改了已有函数 | 锁 L2/L3，必须补测试，禁 L4 |
| risk≈0 且 0 changed functions | L4 可放心 |

**任务范围校准：** 上表阈值只适用于本任务的快照。运行前优先使用 `execution.base_revision` / 本任务 checkpoint 作为 `--base`；若报告混入上一任务或用户已有脏工作区改动，先用正确 base 重跑，或人工列出本任务文件、真实 affected flow 与相关 test gap 后再判级。禁止仅凭混入无关改动后的总文件数或 risk 分数机械升 L1，也禁止因图风险接近 0 降级真实的 auth / API / IM 等业务链风险。无法隔离时按任务自身性质和已证实影响面偏严判定，并把 codegraph 范围污染记为降级证据。

**图风险背离固化规则：** codegraph 只用于校准当前任务的代码影响面，不能替代业务风险判断。若快照混入历史提交或脏改动，必须先锁定本任务 base 重跑；仍无法隔离时，改用人工影响面审查并记录降级原因。无论图风险多低，都不得据此降级 API、IM、订单等高风险业务闭环；反之，也不得因无关历史改动抬高图风险而机械升级。

**验证靶向**：detect-changes 点名的 untested 函数优先进入回归测试；若选择非 TDD 验证，必须说明替代证据如何覆盖该缺口。

**打通自主进化**：若图风险与你判级明显背离（判 L4 但 risk=0.55），按一次「判级被数据纠正」记入：
```
<plugin-root>/scripts/learnings.sh add 判级/图风险背离 <project> "<note>"
```

L4 微调不跑（风险≈0，白跑）。

---

## Tier 只决定风险与验证深度

tier 只决定风险与验证深度，不再决定固定对话或 skill 顺序。任何级别都先走意图路由；`ready` 可以直接 `understand → execute`，`clarify/challenge` 才调用对应能力。

### L0 — 架构 / 迁移风险

跨多模块重构、架构迁移或大范围技术债清理。理解证据需要边界、迁移和回滚。spec/plan 通常有价值，但如果这些内容已经由用户或仓库文档明确，AI 可以复用而不重复生成。执行前识别可独立交付单元；高风险假设才按需 grilling。

### L1 — 完整流程 / 多分支设计

新增完整模块、用户流程或跨模块编排。理解证据需要 acceptance 与 non-goals。需求清晰且验收完整时可以无 spec/plan 直接 `execute`；存在互斥产品选择时按需 brainstorming，存在高风险方案假设时按需 grilling。

### L2 — 共享行为 / 消费者变化

修改既有共享逻辑、契约或消费者。重点是影响面和回归验证，而不是轻量 spec 仪式。读消费方或 codegraph 足以证明边界后直接执行；影响面超预期时重判。

### L3 — 已知 bug / 隔离新增

bug 需要根因，隔离新增需要消费者与契约边界。能稳定复现的 bug 和共享契约变化优先 TDD；无法单元复现或只适合集成验证时，选择足以证明结果的替代验证方式并说明理由。

### L4 — 无逻辑影响微调

文案、样式或等价静态资源路径替换。直接修改并执行与风险匹配的最小验证；有设计源时仍执行保真验收。

## 验证策略（TDD 按需）

TDD 按风险选择，不再是所有代码、配置和文档任务的固定执行顺序：

- 已知 bug、共享契约变化、纯逻辑且可稳定复现的行为，优先用 Red/Green。
- 配置、文档、生成文件、探索性改造或集成环境行为，可以使用静态检查、构建、契约检查、浏览器演练、真实请求或测试后补。
- 用户明确要求 TDD 时，必须严格 test-first，并使用 `phase=tdd`。
- 其他任务使用 `phase=execute`。完成前必须记录验证命令、成功结果、覆盖风险和残余风险。

`evidence.tests` 为兼容字段，语义是“验证证据”，命令不必名为 test；`build`、`lint`、`typecheck`、浏览器脚本或接口验证都可接受，只要能证明本次目标。

## 执行方式（AI 自主，用户可覆盖）

默认 `single`，不需要用户或 AI 额外调用 `choose-execution`。即使存在 plan，未显式选择时仍按 single 执行，plan 可继续细化而不触发重选。

只有任务能拆成真正独立的并行单元时，AI 才选择 `multi-agent`；用户可以覆盖 AI 的选择。multi-agent 必须有真实 plan，并用 `workflow-state.sh choose-execution multi-agent` 绑定 plan hash。宿主原生能力、模型策略与 worktree 隔离原生优先；插件不创建 manifest、worktree、branch 或 worker 生命周期。集成会话负责最终 diff、冲突处理、验证和完成证据。

原生能力不可用或失败时，在 `phase=execute` 或 `phase=tdd` 运行 `workflow-state.sh choose-execution single "<fallback reason>"` 回退顺序执行。外部 CLI 委派仍须显式授权；shared-checkout / 共享 checkout 不得描述为隔离并行写入。

所有级别最后按适用条件完成本地 review、business/fidelity/external-review 证据，并运行 `workflow-state.sh complete`。

---

## 可委派的协作 CLI（各级可选杠杆）

把子任务委派给外部编码 agent CLI（搜集信息 / 实现 / 交叉审核），统一走 **`external-agent` skill** —— 一个 runner、一套路由策略。详见该 skill 的 SKILL.md，这里只给路由速记：

```bash
python3 <plugin-root>/scripts/external_agent.py --agent <name> --cd "$PWD" \
  --PROMPT "bounded task" [--mode review|delegate] [--format text|json] [--SESSION_ID id] [--context git]
```

| agent | 家族 | 默认角色 |
|---|---|---|
| `codex` | OpenAI | 执行（算法 / 补丁 diff） |
| `cursor` | 多模型 | 执行 / 审查（仓库感知） |
| `grok` | xAI | 搜集 / 交叉审查（联网） |
| `antigravity`(`agy`) | Google | 搜集 / 审查（gemini 个人版已停用的继任者） |
| `mimo` | 小米 | 国内兜底 |
| `kimi` | 可配置 provider | 显式执行 / capability-gated 只读审查（不进入 auto） |

- **搜集** → `--mode review`（只读）：联网→`grok`，啃大库→`antigravity`。
- **执行** → `--mode delegate`（可写，需用户授权）：仓库内→`cursor`/`codex`，纯算法→`codex`，国内→`mimo`。
- **交叉审核** → `--cross-review <a>,<b>`，runner 冻结同一产物、计算 hash，并只在 **≥2 个不同家族成功返回**时输出 `quorum=true`；主 Agent 汇总裁决。
- 派之前 `--list` 查可用性；`--SESSION_ID` 多轮续接。

**纪律**：委派不降低结果要求——判级、理解度、验证与最终裁决仍由主流程负责；agent 产出是证据、不是免检的最终答案。`--mode delegate`（可写）须用户授权、且只在 `--cd` 内。`--model` 非用户明确指定不要传。

---

## 常见判断边界

| 情况 | 正确级别 |
|---|---|
| 新增一个已有模式的 API 接口 | L2（改已有逻辑，有回归风险） |
| 新增完全隔离的 provider adapter，显式调用且不进入旧路由 | L3（隔离新增，本地契约测试覆盖） |
| Kimi adapter：`auto_eligible=false`、旧 provider 路由不变 | L3 |
| 仅将静态资源路径替换为等价 OSS URL，不改渲染/控制流 | L4（构建 + 资源可达性验证） |
| 新增全新的问卷流程 | L1（新行为，需要完整 acceptance 与边界） |
| 把多个 store 合并重构 | L0（结构性重组） |
| 修复某个按钮点击没反应 | L3（bug） |
| 改按钮颜色 / 文案 / 间距 | L4 |
| 改按钮点击后的跳转逻辑 | L3 或 L2（看是否有回归风险，拿不准按 L2） |
| 给已有接口加一个可选参数 | L2（有回归风险） |
| 改已有接口的返回结构 / 字段含义 | L2（下游可能回归，必须补测试） |
| 调整某个 store 的字段或 action | L2（多处消费，有回归风险） |
| 新增一个独立的工具函数（无人依赖） | L4（无回归面）；一旦被多处引用就升 L2 |
| 改数据库迁移 / schema | L2 起步，跨表结构性调整升 L0 |
| 复制现有页面改文案做一个新页面 | L4（纯文案）；若新增逻辑分支则 L2 |
| 修一个偶现的线上 bug | L3（必须先复现再改） |
| 升级依赖 / 改构建配置 | L2（可能回归），波及面大升 L0 |
| auth / route guard / API integration / order / IM / prescription / payment / 权限守卫闭环 | L2 起步；新增完整流程或跨模块业务编排升 L1；完成前必须过业务闭环验收与影响面证据，外部评审仅在用户显式选择时启用 |

---

## 跨 session 续行（脚本独占接口）

让 L0/L1 及高风险 L2/L3 任务跨多个对话不丢进度，并把“完成”变成机器可校验的证据门。**脚本独占接口（学 Comet comet-state.sh）。禁手改 YAML。**

**状态文件：** 每个项目按需生成 `docs/superpowers/.workflow-state.yaml`（自动加入 `.gitignore`）。L0/L1 必须维护；auth / route guard / API integration / order / IM / prescription / payment / 数据写入 / 权限等高风险 L2/L3 也必须维护。其他短 L2–L4 可跳过。

**暂存目录：** unfinished task 只能通过 `workflow-state.sh suspend <key>` 停放到 `docs/superpowers/.workflow-suspended/<key>.yaml` + `<key>.meta`；该目录自动忽略，metadata 绑定当前 repository 并校验 state SHA-256。`resume <key>` 只在 active slot 为 absent/完整空模板或 valid sealed state 时恢复，成功安装并核对 active state 后才删除快照。unsafe key、partial pair、tamper、wrong repo、symlink escape 或另一个 unfinished active task 都必须 fail closed。

**证据目录：** `docs/superpowers/.workflow-evidence/`（自动加入 `.gitignore`）。所有 `evidence.*` 必须使用该目录内的仓库相对路径，绝对路径与 `..` 会被完成门拒绝。只存测试输出、Network 方法/URL/状态码摘要、codegraph 报告、评审 JSON 和残余风险；禁止写 token、密码、完整敏感 payload。最低格式：tests 含 `command:` + `exit_code: 0`；business/fidelity 的 `result:` 必须有且仅有一行，内容为 `result: PASS`；requests 同样必须且只能含一行 `result: PASS`，并含 `method:` + `url:` + 三位 `status:`（状态码可以是被验证路径所预期的 2xx/4xx/5xx）；codegraph 含 `result:` 或 `degraded:`；residual_risks 含 `risk:`。任何冲突或失败结果都不得进入 `done`。

**格式**（字段结构刻意设计成将来脚本可直接接管）：

```yaml
task: 一句话描述当前需求
level: L1
phase: align         # align | brainstorm | grill | spec | plan | execute | tdd | review | business-verify | fidelity-verify | done
context:
  repo: /auto-filled/repo
  branch: feat/example
  target: /login + route guard
  sources: OpenAPI + acceptance criteria
  environment: real # real | mock | n/a
  delivery: local-only
execution:
  profile: standard # standard | small-fix
understanding:       # controller-owned hashes; do not set manually
  objective_sha256: ""
  reused_kind: ""
  reused_evidence: ""
  reused_evidence_sha256: ""
requirements:
  business: true
  fidelity: false
  external_review: true
artifacts:
  spec: docs/superpowers/specs/YYYY-MM-DD-xxx-design.md
  plan: ""
evidence:
  tests: docs/superpowers/.workflow-evidence/tests.txt
  business: docs/superpowers/.workflow-evidence/business.txt
  requests: docs/superpowers/.workflow-evidence/network.txt
  codegraph: docs/superpowers/.workflow-evidence/codegraph.txt
  external_review: docs/superpowers/.workflow-evidence/external-review.json
  fidelity: ""
  residual_risks: docs/superpowers/.workflow-evidence/risks.txt
completion:             # script-owned; do not set manually
  completed_at: ""
  repository_fingerprint: ""
  requirements_sha256: ""
updated: YYYY-MM-DD
next: 下一步具体该做什么
```

**维护约定：**
1. **开工时**：跑 `<plugin-root>/scripts/workflow-state.sh check`。如果输出「无续行状态」，直接继续判级；如果已有状态，再 `get phase` / `get task` / `get next`。若 phase != done 且非空，提示续行：「检测到未完成的 {level} 任务【{task}】，停在 {phase}，下一步 {next}。继续，还是换新任务？」若用户明确要切换任务，先 `workflow-state.sh suspend <key>`，再从 empty slot `start <task> <level>`；不得覆盖 unfinished state。若已 done，状态不可再 `set` 或重复 `complete`，直接用 `start`。恢复 parked task 使用 `resume <key>`，且 active slot 必须 empty 或 valid sealed。
2. **定级后**：L0/L1 或高风险 L2/L3 先跑 `workflow-state.sh init`，它只创建、迁移或校验 empty slot，不会凭空创建活动任务。active slot 为 empty 或 valid sealed 时，用 `workflow-state.sh start <task> <level>` 创建 `phase=align` 的活动任务，再设置 context.target、context.sources、context.environment、context.delivery。`ready` 通过 understanding 后进入 `execute`，`clarify/challenge` 才进入可选的 brainstorm/grill。
3. **声明关卡**：业务闭环设置 `requirements.business=true`；它不再自动设置 `requirements.external_review=true`。用户明确要求发布前外部复审时才设置 `requirements.external_review=true`；设计保真设置 `requirements.fidelity=true`。
4. **每过一个阶段**：`set phase/next`，有 spec/plan 则设置 artifacts；每项验收先按上述最低格式写进本地证据目录，再 `set evidence.<field> <path>`。
5. **收尾**：普通任务停在 `review`，业务任务停在 `business-verify`，设计任务停在 `fidelity-verify`。运行 `<plugin-root>/scripts/workflow-state.sh complete`；脚本验证上下文、证据格式和真实业务环境。只有显式设置 `requirements.external_review=true` 时，才额外验证当前仓库 24 小时内的 standard 双家族 quorum 或显式 small-fix 单成功 degraded evidence；随后写入 repository fingerprint 与 `requirements_sha256` seal 再进入 `done`。sealed 状态不可修改，requirements 手工降级或 phase 解封会使 `check` 失败；后续仓库继续开发或自然超过 24 小时不会推翻历史完成。`set phase done` 永远拒绝。

**Goal 模式：** 只有用户已经设置 Goal 时才运行 `workflow-state.sh goal "<objective>"`；tiers 不得自行创建 Goal。自动续行使用 `continue-goal "<objective>"`，显示 `目标续行 = 第 N 次｜phase = <current>｜理解度 = <status>`；`execute` 与旧 `tdd` 状态都兼容。相同 objective 只增加 continuation 并保留 checkpoint；objective 发生变化时清空 checkpoint，并把 understanding 重置为 `pending`。状态只保存 objective SHA-256，不保存目标原文。单次续行结束、token 接近上限或代码写完都不等于 Goal 完成。

**Goal 自治确认：** 理解度通过后依次执行**提案者 → 反方审查者 → 裁决者**。提案者给出 2–3 个可行方案；反方审查者只找误解、影响面、错误根因和越界动作；裁决者逐条处理后给出选择、依据、假设与残余风险。结果只有 **PASS → REVISE → BLOCKED**：`REVISE` 修改提案后重审，最多两轮且保持 pending；只有最终 PASS 才能写 confirmation artifact，无法收敛或越界则 BLOCKED。

reviewer provenance 只能是 `external-cross-review`、`same-model-fresh-context`、`built-in-checklist`；最后一项不是独立 reviewer，不得伪装。删除数据、强制推送、发布、部署、付费、访问凭证/隐私数据、提升权限和无法从目标/仓库判断的重大产品选择都不能自治 PASS。自治 artifact 不得写“用户已确认”，只能记录 `mode: autonomous`。

最小 artifact 形状如下，`scope_sha256` 取 `workflow-state.sh get understanding.scope_sha256`：

```json
{
  "runner": "tiers.autonomous-confirmation/v1",
  "mode": "autonomous",
  "status": "PASS",
  "scope_sha256": "<64-hex>",
  "rounds": 1,
  "requires_user": false,
  "boundary": "safe",
  "proposal": {"options": [{"id": "A", "summary": "..."}, {"id": "B", "summary": "..."}], "recommendation": "A", "assumptions": ["..."]},
  "critic": {"provenance": "built-in-checklist", "verdict": "PASS", "findings": ["..."]},
  "decision": {"choice": "A", "basis": "...", "assumptions": ["..."], "residual_risk": "..."}
}
```

保存到 `.workflow-evidence/confirmation.json` 后运行 `workflow-state.sh confirm docs/superpowers/.workflow-evidence/confirmation.json`。通过后显示 `自治确认 = PASS｜选择 = A｜reviewer = built-in-checklist`。Goal 的执行 phase 与 `complete` 会重新验证 scope、artifact 内容 hash 和 provenance。

---

## 自主进化（全局，跨项目）

让这套工作流参考真实使用方式自我演进。事实源是数据区（`learnings.sh` 自动定位），全局共享，**计数与记录由脚本确定性完成，不靠对话记忆**。模式：自主发现、人工放行。

配套工具（均在 `<plugin-root>/scripts/`）：
- `learnings.sh` —— 记录/计数 helper：`count` / `ready` / `categories` / `add <category> <project> <note>` / `list`。`add` 会校验 category 取自词表、原子追加，并回报当前计数是否达阈值。
- `detect-judging-correction.py` —— Claude/Codex 上挂在 UserPromptSubmit（由 `plugin.json` 声明，启用插件即生效）：用户提交消息时回看上一轮，若疑似纠正判级则注入提醒。**仅 Claude/Codex 有此提醒**：Cursor 的 `beforeSubmitPrompt` 不能向模型注入上下文，故 Cursor 上不安装此 hook —— 此时由我**主动**履行下面的记录职责，不等提醒。

### 记录（被动积累）

每当**用户纠正我一次判级**，或某 tie-breaker 事后被证伪/证实，立即用脚本记录。**这是我的固定职责，不依赖 hook 提醒**——Claude/Codex 上 hook 会顺手提醒一句，Cursor 上没有提醒，但只要本 skill 在跑，判级被纠正时我就必须记：

```
<plugin-root>/scripts/learnings.sh add <category> <project> "<note>"
```
- `category` 必须取自词表（脚本会拒绝非法值）；同类纠正务必贴同一标签，否则计数失效。确属新类时先在数据区（`learnings.sh` 自动定位）词表补一行再 add。
- `note` 写清「我原判 Lx → 用户纠正为 Ly，因为…」。

hook 只是"提醒"不是"代劳"——它从不自动写记录，记不记永远由我执行 `add`。这是本机制保留的人工环节，也保证了去掉 hook（如 Cursor）功能依旧完整。

### 检查与提案（非阻塞维护）

本 skill 被调用时可以运行 `<plugin-root>/scripts/learnings.sh ready`（等价于按 `category` 数 `pending`）。任一 category ≥ 2 时输出提案，否则沉默；提案不暂停当前 `ready` 任务，除非本次目标就是修改全局规则：

> 📈 工作流进化提案：`<category>` 类已被你纠正 N 次（项目 A、项目 B）。建议把「<具体规则>」固化进边界表 / tie-breaker。确认固化吗？

### 固化（人工放行后）

- **用户确认** → 编辑本 SKILL.md（把规则写进边界表或 tie-breaker），并把相关条目 `status` 改为 `folded`。
- **用户否决** → 相关条目 `status` 改为 `dropped`，不再计入。

固化是改全局核心 skill 的动作，**必须用户点头**，绝不自动重写。
