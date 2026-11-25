---
name: bugx-opencode
description: "BugX 对抗审计在 OpenCode 宿主的操作手册。当宿主发起/执行 BugX 漏洞挖掘、代码审计、对抗测试，或遇到 bugx engine pre 门禁、MCP 会话冲突（session_occupied）、Worker 派发（bugx-worker subagent）、headless/ACP 验收、判读式审计（judge）、findings 确认协议、post 结算封存等问题时使用。触发词：bugx 审计、漏洞挖掘、pre 门禁、session_occupied、bugx-worker、judge collect、post --final。"
---

# BugX × OpenCode 使用手册（实战复盘版）

引擎源码仓库（本仓 dev 分支）。本手册共性部分继承
`bugx-zcode` skill（判读式审计/确认协议/坑位），特性部分按 OpenCode 宿主契约
（`core/contracts/bugx-opencode.md`）微调。所有坑位均实证。

## 〇、最短路径决策树

```text
要审计一个项目
└─ cd <项目根> && opencode            # 必须在项目根启动（MCP 是 --root . 相对绑定）
   └─ agent 列表选 bugx（或默认对话说「用 bugx 审计」）
      └─ bugx engine --root . pre     # 交互 TUI：启动门禁逐组原生 question 询问
      └─ 判读式五步（见 §四）→ post --final
   └─ 失败先查 .bugx/.../state/judge/judge-log.jsonl（结构化事件流）
```

## 一、OpenCode 特性事实（先记牢再动手）

1. **项目级 MCP**：`opencode.json` 在**项目根**（三个 bugx MCP：host/worker/docs，
   `command: ["bugx", ...]` 走 PATH，`--root .` 相对绑定）。与 ZCode 的用户级单例
   不同——**换项目无需 rebind，切靶场即换上下文**；但必须从项目根启动 TUI。
2. **agent 入口**：`.opencode/agents/bugx.md`（mode: all）+ `bugx-worker.md`；
   全局软链 `~/.config/opencode/agents/`。
3. **权限形态**：agent 权限矩阵 `execute: deny`（仅白名单例外，含
   `*bugx engine* pre*` / `*bugx engine* post*`）。**一切动作走 MCP 工具或
   白名单 shell**，禁止绕过。
4. **交互原语**：TUI `interaction=question` 必须用宿主原生 `question` 工具
   （单选 `multiple=false`，**一次只传一个阶段问题**），禁止普通文本提问替代；
   无效/取消/失败留在当前阶段，不得自行降级。

## 二、启动与门禁（含 --dev 场景闸门）

1. **交互 TUI（用户在场）**：`bugx engine --root . pre` **不带任何跳过旗标**——
   启动门禁（云端/方案/审查/轮询/修复/提交/报告处置）逐组原生 question 询问用户，逐项确认。
2. **⚠ --dev 场景闸门**：`pre --dev` 仅允许 ①用户明确要求无人值守 ②同一靶场
   重验快审。**用户在场禁止默认用 --dev**；拿不准就先问用户选哪种模式。
   headless/ACP 场景用 `pre --autonomous`（见 §三.4），也不是 --dev。
3. **resume 语义坑**：`runtime.active=true`（上一轮没跑 `post --final`）时，
   pre 走会话恢复（resume）**静默跳过门禁**。中断后必须先收口（`post --final`
   或确认 aborted 终态）再重跑 pre，否则永远不询问。
4. **pre 必须前台同步**：OpenCode v2 原生 shell 显式 `workdir`=项目根、
   `timeout=300000`；禁止 `timeout` 包装、`&`/`nohup`/后台会话、sleep/ps 轮询、
   输出重定向到项目根之外。工具超时记 `BLOCKED`，不得伪造退出码。
5. **门禁防逃逸锁**：严禁在对话文本里自述「我选选项 1」绕过门禁——启动决策必须
   由 pre 写入 `.bugx/` 状态机，未写入前拒绝配 Worker。

## 三、OpenCode 特有纪律

1. **MCP 会话证明优先**：先调当前会话已加载的 `bugx-supervisor` Host MCP
   （真实 MCP 在 tools/list 后写入短期会话证明，CLI 子进程读取该证明）。
   **禁止**从 shell 再启动 `bugx mcp serve` / `bugx mcp probe` / stdio 探针——
   会与 host controller lease 冲突得到 `session_occupied`。
2. **Worker 派发（C 路径代表）**：主 Agent 用 OpenCode v2 原生 `subagent` 工具，
   agent ID `bugx-worker`，**每次调用必须显式传 `background=false`**（前台等结果）。
   主 Agent 自己读 `bugx engine --root . workers` 完整输出，把完整任务块原样交子
   Agent；严禁把 CLI 命令文本当 Worker prompt、不得省略 `WORKER_CLAIM_FACTS`。
   Worker 首个工具调用：无预占事实 → `claim`；有完整预占事实 → `worker_start`。
   两者成功前禁止任何项目探索。父 Agent 不代跑探测、不写 artifact、不调 Worker
   MCP；必须等到每个 Worker 结果返回再推进，Worker 仍 active 时不得结束回合。
3. **headless/ACP 验收**：`opencode run --format json -f <prompt_file> <message>`；
   `question` 工具会被宿主静默阻断（interaction=blocked）⇒ 此场景走
   `pre --autonomous` + 显式门禁参数。ACP `session/new` 默认选项目主 Agent——
   验收客户端必须先 `session/set_mode` 显式选 `bugx`，不可用则 fail-closed，
   不得拿默认 Agent 结果冒充 BugX 验收。
4. **状态机与账本**：`.bugx/` 是运行态账本与证据库，严禁把运行时产物写进生产
   源码与依赖（与所有宿主一致）。

## 四、判读式五步标准流（共性，每步一条命令）

```bash
bugx engine --root . pre                # 交互场景：启动门禁逐组询问（用户逐项确认）
bugx engine --root . judge --all        # 一次领满容量内全部单元；判读包并发给 bugx-judge
bugx engine --root . judge --settle-dir <verdicts目录>
bugx engine --root . findings-confirm --from-verdicts <verdicts.json>
bugx engine --root . post --final       # 会话最后一条引擎命令必须是 --final
```

- **回合自检**：`state/judge/judge-log.jsonl` 里 `collect_summary` >2 次 = 在
  浪费回合（judge collect 必须单轮领满）；findings-confirm 拆多轮同理
  （一条命令 ~6s，实测拆散拖到 235s）。
- **submit_finding 定级口径**：必带 `confidence`（≥2 独立通道 observations +
  negative_control pass ⇒ ≥0.75；差分哨兵 SENTINEL ⇒ ≥0.85）；severity 按
  CWE 口径（任意代码执行/命令注入 = CRITICAL；SQL 注入/路径穿越/硬编码云凭据
  = HIGH），不得因不确定保守降级——否则引擎 fallback 会把 confirmed 缺陷
  兜底成 0.35。
- **证据落盘**：验收要求 artifact 在案时，probe 输出写 claim 的 `artifact_root`
  相对路径，checkpoint finalize 用 `--artifact`（多单元 `--artifacts-json`）。

## 五、确认协议要点（共性）

finding 转 confirmed：同指纹 ≥2 次独立运行 + ≥2 独立通道 + negative_control
`pass`（不是 "OK"）+ `root_cause_verified`；`target_execution` 的
`target_platform` 与 `executed_platform` **逐字相同**（darwin ≠
darwin-arm64-cpython-3.14）。findings.json 顶层 `run_binding.run_id` 用
`lifecycle-<polling>-<lifecycle>` 形式，`round` 与 runtime 当前轮逐字一致。

finding 的 `reproduction` 字段必须非空且可被第三方独立执行；`confirmation`
块必须带 `state:"reproduced"` 与非 heuristic 的 `oracle`（含
`provenance.independent_from_change:true`）。这两个字段名由
`core/ledger/finding_confirmation.py` 的 `confirmation_issues()` 直接读取，
写错或省略都会使候选永久停在 pending。复现脚本必须打印非空失败观测再
`exit 1`，否则只有 `engine-verify:exit-code` 单通道，门禁拒绝。

## 六、坑位表

| 症状 | 根因 | 对策 |
|---|---|---|
| pre 没弹门禁询问 | runtime 悬挂（上轮没 `--final`）→ resume | 收口后重跑；交互场景 pre 不带跳过旗标 |
| `session_occupied` | shell 重复起 serve / stdio 探针 | 只用会话内已装配的 MCP；禁 shell 探针 |
| Worker 没跑 / 提前结束回合 | subagent 未传 `background=false`，或父 Agent 先输出了结束文本 | 每次显式 `background=false`；Worker active 时主 Agent 必须等待 |
| ACP 验收拿默认 Agent 冒充 | `session/new` 默认主 Agent | 先 `session/set_mode` 选 `bugx`，不可用 fail-closed |
| pre 超时被记失败 | 工具级 timeout 包装/后台化 | 前台 300s 同步等待，超时如实记 BLOCKED |
| checkpoint 三连拒 | 手拼 payload | 用 `worker_checkpoint.py finalize`（自动绑指纹与 receipt） |
| post 报「必须紧接活动 pre」 | runtime aborted | 重跑 pre 走恢复；supervisor 冻结则 `pre --session-recovery new` |
| 引擎从 `~/.bugx/core` 加载 | 改了源码没同步 | `bugx install` 同步全局；只 pip install 不够 |

## 七、验收基线

- 交互 TUI 首轮 pre 启动门禁逐组原生 question 询问（用户逐项确认）
- 覆盖单元恰等于产品文件；judge 单轮领满；settle/确认秒级；judge-log 事件齐全
- post --final 收口后 runtime 终态明确（COMPLETE / ABORTED / BLOCKED /
  RECOVERY_REQUIRED），无 NEXT_ROUND 悬挂
- 结构化失败原因输出，无静默降级；退出码 0 即收口成功
