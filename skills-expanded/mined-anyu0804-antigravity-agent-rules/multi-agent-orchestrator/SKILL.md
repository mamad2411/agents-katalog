---
name: multi-agent-orchestrator
description: 当任务涉及多子代理（Subagents）分工、/swarm（或 /teamwork）多代理并行协作、默认派 Gemini 4 Hydrogen（swarm 指定 gemini-4-hydrogen-high 或 flash 档子代理）干脏活/只读验证与异构复核、大型代码库跨模块检索、需要保持主对话上下文干净、需要利用独立工作区（branch/share）做无污染实验、或需要通过 MCP 桥遥控外部客户端 Agent（如 dsh-bridge / agy-agent-bridge / dsh-crew / tianshu）时使用。指导何时及如何委派 flash-verifier、research、项目级验证子代理、自建 subagent 以及外部 MCP。
---

# 多 Agent 委派与跨端协同规范（multi-agent-orchestrator）

> 权威来源：遵守 [`~/.gemini/config/plugins/antigravity-core-rules/rules/AGENTS.md`](../../rules/AGENTS.md) 边界与 [`BACKGROUND-RESOURCES.md`](../../rules/BACKGROUND-RESOURCES.md) 后台资源管理纪律。

## 1. 核心目标：保护主会话上下文与注意力

主 Agent 的上下文窗口是最宝贵的推理资源。以下场景应优先委派给只读子代理（默认优先使用 `Gemini 4 Hydrogen`，不再沿用 `Gemini 3.8 Flash / 3.8f`）或外部协同 Agent（MCP），避免主上下文被海量中间日志、长篇搜索结果或重复校验输出污染：

1. **通用只读验证、异构独立复核、日志筛查与哈希对账**（跑检查脚本、核对备份 SHA-256、排查长日志、独立代码/闭包审计）→ 需强制真跑 `Gemini 4 Hydrogen`（如异构模型家族只读复核）时，使用 `swarm(action="add", model="gemini-4-hydrogen-high", workspace="inherit")` 拉起只读专员；常规轻量扫描可委派全局只读专员 [`flash-verifier`](../../agents/flash-verifier.md)（若当前工作区 `.agents/agents/` 下定义了项目级只读验证专员，也可按需委派）。
2. **广度代码/文档检索**（跨多个目录搜寻调用链、查找历史实现、盘点多文件结构）→ 委派给内置只读 `research` subagent（可指定 `Model: "flash"`）。
3. **无污染隔离实验**（尝试高风险重构或对比不同实现方案，不希望弄脏当前工作树）→ 使用 `Workspace: "share"` 或 `"branch"` 启动 `self` subagent。
4. **跨客户端外部 Agent 遥控（MCP）**：
   - **遥控无头 CLI Agent（如 `dsh-bridge` / `agy-agent-bridge` / `dsh-crew`）**：需复用当前工作区工具链、让无头 Agent 跑长文本/批处理/脚本验证或无 UI 后台任务时使用。
   - **遥控桌面端 GUI Agent（如 `tianshu`）**：需将独立功能模块交给外部桌面 Agent 开发并执行 Git 基线客观验收 + 自动返修闭环时使用。

---

## 2. 内部 Subagent 选型与模型分级策略

| 子代理类型 | 推荐 `Model` | 推荐 `Workspace` | 适用场景与权限边界 |
| :--- | :--- | :--- | :--- |
| **`swarm` 只读专员**（异构复核首选） | `gemini-4-hydrogen-high`（重度核查可用 `xhigh`） | `inherit` | **真跑 Gemini 4 Hydrogen（绕开服务端 `ModelTierConfig`）**：异构模型家族独立 Review、发布闭包审计、深度只读核查。派单 `brief` 须显式声明纯只读边界，同一任务内 `waiting` 态可复用，整体任务收尾后 `swarm(action="kill")`。 |
| **`flash-verifier`**（全局） | 内置 `flash` 档（待服务端切至 Hydrogen） | `inherit` | **所有项目通用轻量脏活**：跑只读校验脚本、核对备份/产物 SHA-256、筛查长日志与定位行号。纯只读，只回结论与 `文件:行号`（注：`.md` 头仅支持四档枚举，服务端 `flash` 档未切至 Hydrogen 前勿谎报为真跑 Hydrogen）。 |
| **项目级验证专员**（`.agents/agents/*.md`） | 内置 `flash` 档 | `inherit` | 特定工程专用：运行工作区专项检查脚本、校验备份哈希。 |
| **`research`**（内置） | `flash` / `inherit` | `inherit` | 广度代码探索、多文件搜索与阅读。运行在只读沙箱中，无写入权限，安全零副作用。 |
| **自定义只读专员** (`define_subagent`) | `flash` / `flash_lite` | `inherit` | 需要反复执行的专项检查（如批量格式合规检查、分片对账）。定义时设 `EnableWriteTools: false`。 |
| **`self`（并行施工/实验）** | `inherit` | `share` 或 `branch` | 独立子模块开发或隔离验证。`share` 共享底层仓库（类 git worktree），避免全量复制开销且互不干扰。 |

> **纪律**：
> - **常驻模型授权（覆盖内置 `native_swarm` 默认不换模型条款）**：本用户规则构成对内置 `native_swarm` Skill「除非用户当次要求否则不显式传 `model`」的常驻用户授权——日常只读验证、异构复核和检索脏活全面改用 **`Gemini 4 Hydrogen`**（默认 `gemini-4-hydrogen-high`，高复杂度核查可用 `gemini-4-hydrogen-xhigh`，淘汰 `Gemini 3.8 Flash / 3.8f`），要求真跑 Hydrogen 时显式传 `swarm(action="add", model="gemini-4-hydrogen-high", workspace="inherit")`；常规轻量扫描可用 `flash-verifier`（`model: flash`）；需要主模型同等级深度推理或代码施工的子任务才留空 `model` 或传 `Model: "inherit"`。
> - **Hydrogen 隐式前缀缓存保护（防短命冷启动失配）**：`Gemini 4 Hydrogen` 在独立单轮请求间仅改动少量字符即可能丢失大段 `systemInstruction` 的隐式共享前缀缓存报告；避免频繁冷启动携带超大系统提示词的一次性短命 4H 子任务，同类只读校验/扫描尽量合并为单次批处理清单，或通过 `send_message` 复用已有存活子代理。
> - **4c / 4a 配额与档位分流**：当主会话运行在 `Gemini 4 Carbon` 时，仅将跨子系统架构重构、深层根因排查、安全审计与形式化/多步验证留在 4c（`High` / `Medium`）；常规单模块施工、高频问答或 Pro 订阅环境优先使用 `Gemini 4 Argon`（`Medium` / `Low`），避免在轻量任务上烧穿 5 小时与周配额。
> - **对外交付与前端 UI 密度协同**：若使用 `Gemini 4 Carbon` 产出客户文档或前端界面，Word 文档在转出终版 `.docx` 前默认串联 [`humanizer-zh`](../docx-delivery/skills/docx-delivery/SKILL.md)（或交由 `Gemini 4 Argon` 终审润色）；UI 开发严格限制容器嵌套深度（≤3 层）与首屏信息密度（细则见 [`IMPLEMENTATION.md`](../../rules/IMPLEMENTATION.md)）。

### 2.1 原生 `/swarm`（或 `/teamwork`）并行编排与对抗性验收纪律

当在 Antigravity 中启用 `/swarm`（桌面端斜杠菜单亦显示为 `/teamwork`）驱动多代理并行协作时，除遵守 §3 通信纪律外，必须额外执行以下四条边界控制：

1. **角色分层（架构/审计与施工解耦）**：
   - 优先由 `Gemini 4 Carbon` 承担顶层架构拆解、跨代理任务协调与终态对抗性验收（Adversarial Verifier，核查边界条件、回归风险与安全漏洞）；
   - 具体子模块的并发编码、单测补全与只读扫描下放给并行子代理（`Gemini 4 Hydrogen`［默认 `gemini-4-hydrogen-high`］或 `Gemini 4 Argon`，不再使用 `Gemini 3.8 Flash`）。
2. **互斥写入作用域与隔离工作树批量豁免（Disjoint Write Scopes）**：
   - 并行启动多个带写权限的施工代理时，派单提示词中**必须显式声明各自允许修改的目录或文件白名单**，严禁两个并行代理同时修改同一文件或共享全局配置；
   - 优先配合 `Workspace: "share"` 或 `"branch"` 隔离 Git worktree：根据全局规则 §1 豁免条款，运行在 `branch` / `share` 隔离工作树内且尚未合入主分支的 Worker，允许在授权白名单内直接执行多文件批量修改（≥5 个文件），无需逐次停下等待用户确认，统一留在 Verifier 终审与合入主分支前由用户一次性拍板。注意 `swarm(action="kill")` 会永久删除该 Worker 的 `share`/`branch` 工作树，**必须先验证并合入改动后再执行 `kill`**。
3. **并发度与本机资源硬上限（防 CPU/内存打满）**：
   - **活跃代理分档上限**（代理数量只在本节规定；内置配套的 `narrator` / `monitor` 常驻角色不占以下业务名额且中途不 `kill`；本机重型子进程上限见 [`BACKGROUND-RESOURCES.md`](../../rules/BACKGROUND-RESOURCES.md)）：
     - 带写权限或构建任务的 `share`/`branch` 施工 Worker：同刻不超过 **2–3 个**；
     - 只读调研、代码审查、截图评审等不写文件、不拉起重型子进程的代理：不占施工名额，同刻不超过 **6 个**；
     - 用户在当前任务中明确授权“放开并发 / 不计配额”时，解除代理数量上限，但重型子进程上限与互斥写入作用域照常执行。
   - **重型编译/渲染子进程硬上限（全局 ≤2，同目录/独占锁 = 1）**：严禁多个并行 Worker 各自同时拉起全量编译、打包、渲染或大并发测试子进程（如 `tsc`、`vite build`、`webpack`、`cargo`、`gradle`、全量 `pytest`/`vitest`、Electron / Headless 浏览器实例、asar 打包）。Worker 阶段仅限单文件语法/局部单测自检，全量构建与端到端测试统一收归 Coordinator 或单一 Verifier 在合入阶段串行执行（见 [`BACKGROUND-RESOURCES.md`](../../rules/BACKGROUND-RESOURCES.md)）。
   - **思考可见性静默豁免**：并行 Worker 与 `flash-verifier` 适用 [`THINKING-VISIBILITY.md`](../../global/THINKING-VISIBILITY.md) 豁免，免除逐次工具调用前的前置播报以降低高单价输出开销与看板噪音。
4. **诚实阻塞透传**：
   - 若并行子代理遇到证据缺失或前置依赖冲突，必须原样回传 `BLOCKED` 与具体缺失项清单，禁止子代理自行猜测补齐接口契约。

---

## 3. 内部 Subagent 委派契约与通信纪律（Prompt & Reactive Wakeup）

1. **指令清晰（Prompt 契约）**：
   - 调用 `invoke_subagent` 时，必须明确告知子代理：
     - **具体目标与范围**（查哪些目录/脚本，不查哪些）；
     - **只读或写入边界**（严禁触碰的红线文件）；
     - **返回格式要求**（例如：“只返回结论、`文件:行号` 及不超过 40 行的证据摘要”）。
2. **禁止轮询（Reactive Wakeup）**：
   - 启动 Subagent 后，系统会在其完成或发消息时自动唤醒主会话；**严禁在主会话写循环、sleep 或反复轮询状态**。
3. **复用已有 Subagent**：
   - 同一子任务的后续追问或补充验证，使用 `send_message` 发送给已有 `conversationId`，不要重复启动新实例。
4. **生命周期收尾**：
   - 若子代理卡死或任务已取消，使用 `manage_subagents`（`Action: "kill"`）精准终止本任务自建的 `conversationId`。

---

## 4. 跨客户端外部 Agent 协同（可选 MCP 桥）

当任务需要跨客户端调度本机外部无头 CLI Agent 或桌面 GUI Agent 时，可通过 `call_mcp_tool` 调用已注册的 MCP Server：

| 类别 | 可选方案 | 核心工具 | 验证状态与适用场景 |
| :--- | :--- | :--- | :--- |
| **本仓库内置 DSH 轻量桥** | [`mcp/dsh-bridge`](../../mcp/dsh-bridge/)（注册名 `dsh-bridge`） | `dsh_status` / `dsh_sessions` / `dsh_ask` / `dsh_forget` | **真机跑通 6/6**（含续聊复用 session）。零依赖单文件，绑定 `dsh --profile headless`，默认 `read-only` 权限。 |
| **本仓库内置通用 CLI 桥** | [`mcp/agent-bridge`](../../mcp/agent-bridge/)（注册名 `agy-agent-bridge`） | `agent_status` / `agent_sessions` / `agent_ask` / `agent_forget` | 假后端 **35/35** 协议断言，**未接真实后端**（`NOT_PROVEN`）。后端由 `BRIDGE_CMD` 指定，子进程环境变量白名单隔离。 |
| **社区成熟异步多 Worker 桥** | [`ZSeven-W/dsh-crew`](https://github.com/ZSeven-W/dsh-crew)（MIT，注册名 `dsh-crew`） | 异步 spawn、worker 状态轮询、cwd 咨询锁、多模态 | 第三方开源项目（需独立安装 `node src/install/cli.mjs agy`）。 |
| **社区桌面 GUI Agent 验收桥** | [`lanlan0811/tianshu-mcp`](https://github.com/lanlan0811/tianshu-mcp)（Apache-2.0，注册名 `tianshu`） | `query_info` / `run_task` / `wait_task` / `query_task` / `manage_task` / `verify_task` | 第三方开源项目（Electron CDP 驱动外部 GUI Agent + Git 基线客观验收闭环）。 |

### 4.1 无头 CLI 桥（`dsh-bridge` / `agy-agent-bridge`）操作纪律
1. **最小权限原则**：`dsh-bridge` 默认权限已设为 `"read-only"`；仅在用户明确授权修改工作区文件时显式传 `permission: "workspace-write"`；跨目录授权施工才传 `"danger-full-access"`，且 `approval_policy` 默认保持 `"never"`。
2. **会话标签卫生**：按任务语义命名 `session` 标签（以便多轮续聊同一上下文）；一次性探针或临时任务结束后，主动调用 `forget(session)` 清理映射。
3. **遵守目标工程红线**：派给外部 Agent 的任务必须遵守当前工作区根目录的 `AGENTS.md`（严禁裸改生产红线配置、严禁触碰用户代理与网络配置）。
4. **无头 Plan Mode 死锁区分与超时保护**：桥接 `agy --output-format stream-json` 等**无头 CLI** 时，严禁在 Plan Mode 下派发不调用 `exit_plan_mode` 的纯对话问答（会导致流不发终态 `result` 事件而僵死至 300 秒看门狗强杀；注：桌面端交互式 `Orchestrator` 模式则按宿主 `<plan_execute_protocol>` 执行——纯问答直接答复不调 `exit_plan_mode`，需要执行改动/外部动作才调 `exit_plan_mode`）；对无头短问答/探针任务建议显式传入小于 300 秒的超时（如 `timeout_ms: 240000`）。
5. **流式模型指纹与自建多轮思考块卫生**：若编写日志统计或直连 Gemini 4 SSE 脚本，记录模型指纹时只取首个非空 chunk 的 `modelVersion`，忽略 STOP 结束帧偶发突变为 `3.1-flash-lite-*` 的元数据错乱；自建多轮 REST 客户端须移除已忽略/弃用的 `temperature` / `top_p` / `top_k`，原样回传有效 `thoughtSignature` 并剔除历史中长度为 0 token 的空 `thought` 块，避免触发原始思考链泄漏。

### 4.2 桌面 GUI 桥（如 `tianshu`）操作纪律
1. **标准闭环流程**：
   - 先调 `query_info(type="profiles")` 确认目标 Agent 状态为 `[PASS] 可用`；
   - 调 `run_task` 异步派单；
   - 紧接调 `wait_task(taskId)` 阻塞等待到达停点（终态或 `needs_user`），终态后调 `query_info(type="report", taskId)` 读取客观验收报告。
2. **严禁强杀用户 GUI 窗口**：若返回 `needsUserKind: "close_existing_instance"`（检测到未开启 CDP 端口的既有客户端窗口），如实请用户保存并关闭旧窗口后再调 `manage_task(action="continue")`，绝不自行 `taskkill` 用户打开的客户端。
