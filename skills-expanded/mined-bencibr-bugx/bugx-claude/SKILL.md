---
name: bugx-claude
description: BugX 漏洞挖掘引擎在 Claude Code 宿主下的专属使用手册——开工前必读协议清单、宿主能力映射（AskUserQuestion/Task/MCP）、finding confirmation 与 reproduction 契约、本机实证过的坑位与对策（证据通道、claim 粒度、指纹漂移自锁、大响应体、worker MCP 断线回退）。当用户要在 Claude Code 里启动/排障/收尾 BugX 审计、解释 BugX 门禁报错、或问「为什么审计跑了这么久」时使用本 skill。
---

# BugX × Claude Code 使用手册（实证复盘版）

本手册由 2026-11-09 在 `bugx-audit-claude` 靶场的整轮审计复盘提炼。
所有坑位都在本机实证过；标注【源码已修】的条目已在引擎侧修复。

与通用 `bugx` skill 的关系：通用版承载生命周期协议；本手册是 Claude Code 宿主增补，
**不替代门禁交互纪律**。两者冲突时以通用协议为准。

---

## 〇、开工前必读（这一节能省掉一半时间）

**强制执行**，不要跳过：

```bash
bugx engine path --name AGENT_GUIDE.md   # 362 行，收尾 checklist
bugx engine path --name bugx.md          # 1299 行，读「工作流程」第 5 条「举证与确认」
bugx engine path --name contracts/bugx-runtime-contract.md   # 342 行，claim/rebind 状态机
```

**只读后两份也没关系，但必须读。** 2026-11-09 那次审计里，这些坑在文档里全都写着，
却因为「靶场答案已知、看起来简单」而跳过了，结果多花 45 分钟。

读不下 1299 行就只读这三段：
- `bugx.md:1098-1112` —— 举证与确认：confirmed 的六个硬条件
- `bugx.md:584-586` —— commit_policy 与提交时机
- `bugx.md:875-880` —— cycle-review 契约

---

## 一、Claude Code 宿主能力映射

| BugX 需要 | Claude Code 对应能力 | 注意 |
|---|---|---|
| 门禁单选 | `AskUserQuestion` | 生命周期门禁 `multiSelect=false`；`question_id=tooling:batch` 必须 `multiSelect=true` |
| Worker 并发 | `Task` / 原生 subagent | `subagent_type="bugx-worker"`；**不要传 `process_pid`** |
| 协议通道 | `bugx-supervisor` MCP（host）+ `bugx-supervisor-worker` MCP（worker） | 两个 server 角色分离，host 持 `controller.lock` 单例 |
| MCP 配置 | `.mcp.json`（项目级）+ `.claude/mcp.json`（镜像） | `container_key=mcpServers` |
| 无头调用 | `claude -p <prompt>` | 自治加 `--output-format json --permission-mode bypassPermissions` |
| 断点续跑 | `claude --resume <session>` | |

**ACP 面：Claude Code 上游不存在**（`claude --help` 无 `acp` 子命令/flag）。
`core/host_acp/claude.py` 显式声明 `status="unavailable"`。不要试图走 ACP，
受支持通道是无头 `claude -p` 与插件机制。

---

## 二、实证坑位（按代价从高到低）

### 坑 1：两个独立证据通道 —— 最贵的一个

**症状**
```
确认门禁失败，拒绝写入不可收敛的 confirmed：
缺两个独立证据通道（engine-verify 只从 receipt 的 stdout/stderr 派生第二通道）
```

**根因**：引擎从 verification receipt 派生通道：
- `engine-verify:exit-code` —— 永远有
- `engine-verify:stdout` / `engine-verify:stderr` —— **仅当摘要非空时才有**

纯静默 `sys.exit(1)` 的 stdout/stderr 都是空串（sha256 = `e3b0c442...`），
所以只有 **1 个通道**，门禁拒绝。

**正确写法**：正例探针在退出前**必须打印非空失败观测**：

```python
print(f"DEFECT REPRODUCED: connect_calls={n} thread_errors={errs}")
sys.exit(1)
```

负对照保持安静 `exit 0` 即可。

**判断口诀**：正例 exit 1 **且** stdout 非空；负例 exit 0 且可静默。
着急时记这句就够。

### 坑 2：claim 粒度 —— 一个 worker 一次只能领一个 unit

**症状**
```
每个 Worker 只能领取一个 coverage unit；请由调度器拆分任务后再次 claim
```
传了 `allow_bundle=true` 还会撞：
```
Worker MCP claim 禁止 allow_bundle=true；批量 claim 只能由本地 orchestrator core 调用
```

**正确做法**：一个 worker_id ↔ 一个 unit_id。15 个单元就派 15 次 claim。
批量只能由引擎内部 orchestrator 做，MCP 通道不给。

**推论**：别写"批量领取脚本"，直接循环单发。

### 坑 3：worker 启动不传 PID

**症状**
```
process_pid 999999 不存活：Task 子代理请省略 process_pid，以心跳作为活性证据
```

**正确**：`worker_start(caller_role="worker", worker_id=..., provider="claude-code")`，
**不传 `process_pid`**。原生子 Agent 由心跳证明活性。

### 坑 4：中途 commit 触发指纹漂移自锁 —— 20 分钟白跑

**症状**
```
审计目标已变化；请重新生成当前覆盖计划后再继续
```
随后 `post` 报：
```
并发门禁未满足：Life 未满足（target_drift）
```

**根因**：`workspace_fingerprint = SHA256(manifest单元集 + git HEAD)`。

你在审计中途 `git commit` 修复 → **git HEAD 变了** → 指纹漂移。
更糟的是 `post` 自己也会重写 `module-coverage.md`（重扫发现新函数），
又一次改变指纹 —— **写完清单再校验指纹，自己判自己漂移**。

**正确姿势**：
- **全程不切 git 状态**。要么一直对着漏洞版，最后一次性 commit；要么开 worktree。
- 已经提交了：立刻 `bugx_supervisor_rebind_target`（需要 `reason`）。它把证据
  不再匹配新目标的已覆盖单元迁为 stale；证据仍可复算的单元会被自动恢复
  （`_reinstate_covered_by_evidence`）。**最坏情况仍需重做覆盖**，所以能不做就别做。

【源码已修】坑 4 的自动重绑在 `core/launch_phases/post_phase.py:242` 的
`_reconcile_additive_plan_drift()`，判据在
`core/supervisor/finding_workflow.py`：哪些单元的旧证据还能沿用，看**本轮重扫
结果** `inventory-diff.json`——`changed`/`removed`/`renamed` 列出的单元作废重验，
其余沿用覆盖结论；没有这份文件就退回严格模式，全部重新覆盖。

为什么不能只看指纹：指纹只含「单元 ID + git HEAD」，**不含源码字节**，而 post 是
修复模式、改动的源码此刻尚未提交。也不能拿「清单 sha256 == 当前文件哈希」当证据：
`module_coverage` 门禁本轮会用新字节重写清单里的 sha256，那是自证循环。

### 坑 5：大响应体打爆上下文

**症状**：`confirm_finding` / `verify_finding` / `next_round` 返回 17-25 万字符，
宿主工具层直接拒绝并落盘。注意这是**宿主侧**行为——引擎自身没有响应体上限
（MCP 层只限制请求 512 KiB/行，并截断 `history`/`findings` 等长列表）。

**绕行**（立即采用）：
```bash
# CLI rpc 绕过宿主 framing，输出可控
bugx supervisor rpc --root . --role worker --tool bugx_supervisor_status --args '{}'
```
或直接读权威状态（`open()` 不做通配符展开，必须自己 glob）：
```bash
python3 -c "
import json, pathlib
d = json.load(open(next(pathlib.Path('.bugx/pollings').glob('*/lifecycles/*/state/supervisor.json'))))
print(d['revision'], d['status'], d['confirmation_gate']['ready'])"
```

**别做的**：每次 confirm 后读一遍 200KB 响应。永远读 `supervisor.json`。

### 坑 6：worker MCP 断线 → 走 CLI rpc 回退

**症状**：`bugx-supervisor-worker` server disconnected，`bugx_supervisor_claim` 不可用。

**回退通道**（实测完全等价）：
```bash
bugx supervisor rpc --root . --role worker --tool bugx_supervisor_claim \
  --args '{"caller_role":"worker","worker_id":"w1","worker_role":"recon","unit_ids":["内部:1:main.py"],"lease_seconds":900}'
```
顺序：`claim` → `worker_start` → `run_sandboxed_probe` → `checkpoint`。
`run_sandboxed_probe` 必须原样带 claim 返回的 `lease_id` + `execution_id`。

**注意**：`--role host` 拿不到主控租约（fail-closed，非缺陷），host 写操作走宿主 MCP。

### 坑 7：cycle-review 字段格式

`bugx lesson review --input <json>` 必填：

```json
{
  "lifecycle_id": "life-1",
  "round": 1,
  "finding_count": 9,
  "credited_count": 9,
  "finding_fingerprints": ["<与 credited_count 等长且唯一>"],
  "new_patterns": [{
    "category": "...", "title": "...", "root_cause": "...",
    "reflection": "...", "probes": ["..."], "source_refs": ["src/x.py:3"]
  }]
}
```

两条硬约束（都是撞出来的）：
1. **`pattern_id` 建议一律省略** —— 省略时引擎派生
   `L-<sha256(category\0title\0root_cause)[:12]>`。若手写，必须是
   `^L-[0-9a-f]{12}$`，否则报 `pattern_id 格式无效`；手写的不规则 ID
   不会与既有 pattern 自动去重（`core/ledger/patterns.py:144-147`）。
2. `title` 非空，`finding_fingerprints` 数量必须等于 `credited_count`

输入文件必须落在项目根内（`/tmp` 会被拒）。

### 坑 8：探针自包含

探针里不要依赖 cwd / 环境变量 / shell：
```python
import os, sys
_root = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(_root, "src")):
    _root = os.path.dirname(_root)
sys.path.insert(0, _root)
```
`run_sandboxed_probe` 只接受 argv 数组，**拒绝 `bash`**。
另外探针失败常来自：用 `$p` 变量但 shell 未展开、`cd /tmp` 破坏相对路径。

### 坑 9：覆盖率是怎么锁死的

- `covered` 是**单调**的，但 worker 自己写 `upgrade_tier=deep` 的 note 会被引擎映射成 `stale`
- stale 单元若仍被本轮 active/submitted claim 占用则领不到；跑 `next-round`
  释放占用后可重新 claim，或用 `post` 结算本轮
- **内部单元 100% 之前领不到业务 unit**（`内部单元未完成前不能领取业务 unit`）

### 坑 10：`post --dry-run` 的 identity 门禁

`runtime.json` 的 `round` 与 `supervisor.json` 的 `round_no` 必须一致。
更了 round 之后没重跑 `pre`，就会看到 `supervisor_round_mismatch`。
先 `bugx engine --root . status --json` 对齐，再 dry-run。

---

## 三、Claude Code 专属提速纪律

1. **先读文档再 claim**（见第〇节）。报错信息是结论不是解释，别靠试错反推。
2. **门禁报错先读源码**。`~/.bugx/core/ledger/finding_confirmation.py` 的
   `confirmation_issues()` 就是证据通道的唯一真源，60 行，比跑一轮便宜。
3. **全程一次 commit**。审计期间把修复留在工作区，`post` 通过后再提交。
4. **大响应走 `supervisor rpc`**，状态读 `supervisor.json`。
5. **探针先写对形态，再谈内容**。argv、自包含路径、正例打印失败标记。
6. **别用 `Task` 派 worker 之外的探索**。BugX 的 claim 与 Task 不是一回事；
   派 Task 之前必须先有 claim 返回的 lease。

---

## 四、Finding 确认协议与 reproduction 契约（缺这节，finding 会永久卡在 pending）

L7-6 引擎自检要求**每个宿主 skill 都必须写明** `confirmation` 与 `reproduction`
契约——不是形式要求：这两个字段不齐，`finding_confirmation.py` 的 `confirmation_issues()`
会拒绝把候选晋级为 confirmed，整轮结算卡死。

### 4.1 finding 必备结构

```jsonc
{
  "id": "...", "fingerprint": "...", "title": "...", "severity": "...",
  "confidence": "...", "root_cause": "...", "path": "...", "line": 0,
  "reproducible": true,
  "reproduction": "<最小复现步骤，可多行>",     // ← 必须非空
  "confirmation": {                            // ← 必须齐备，见 4.2
    "state": "reproduced",
    "oracle": { "...": "..." }
  }
}
```

### 4.2 confirmation 块的硬条件（`bugx.md:1101-1106`）

1. `state: "reproduced"`；
2. `oracle.tier` 非 heuristic（`differential` / runtime-invariant 等）；
3. oracle 的 `provenance.independent_from_change: true`（证明不依赖待修代码）；
4. 负对照通过（同一配方在干净基线上不触发）；
5. 根因已验证（非"症状描述"）；
6. `reproduction` 可被第三方独立执行。

### 4.3 两个独立证据通道（与第二节坑 1 同源）

引擎从 verification receipt 派生 `engine-verify:exit-code`（恒有）与
`engine-verify:stdout|stderr`（仅摘要非空时）。所以：

- 正例复现脚本 **必须打印非空失败观测**再 `sys.exit(1)`；
- 负对照安静 `exit 0` 即可；
- 只 silent `sys.exit(1)` ⇒ 单通道 ⇒ 门禁拒绝（错在第 1 条件之外，报错文案是
  "缺两个独立证据通道"）。

### 4.4 落地顺序（照做即可）

1. 写复现脚本 → 实跑，确认 exit code 与输出；
2. `confirm_finding`（host）写入 confirmation 块；
3. `verify_finding`（host）做修复后复验：`status` 应从 `CONFIRMED` 翻转为
   `CANDIDATE`（缺陷不再复现）；
4. 写回 lifecycle `findings.json` → `post` 自动结算。

> 不要手改 `findings.json` 里的 `reproduction` 为单行再 post；直接走
> `confirm_finding` / `verify_finding`，引擎自己落盘。

---

## 五、验收基线（做对了应该看到什么）

```text
confirmation_gate:
  ready: true
  confirmed: N            # = findings 数
  pending: 0
  assurance.average_score: 110   # 画像满分；缺 observation_artifacts 加分时 100

coverage:
  covered: 全部
  stale/pending: 0
```

修复后同配方复验：`status` 从 `CONFIRMED` 翻转为 `CANDIDATE`（缺陷不再复现），
而负对照仍 `exit 0` —— 这就是 Live 复验通过的判据。

---

## 六、常见门禁报错速查

| 报错 | 真正含义 | 下一步 |
|---|---|---|
| 缺两个独立证据通道 | 正例没打印失败观测 | 正例加 `print("DEFECT REPRODUCED: ...")` |
| 每个 Worker 只能领取一个 coverage unit | claim 粒度 | 一个 unit 一次 claim |
| process_pid 不存活 | 传了 PID | 省略 `process_pid` |
| 审计目标已变化 | git HEAD/manifest 变了 | `rebind_target`（代价：全单元 stale） |
| 仍有 active worker | claim 未释放 | `next_round` 或等租约过期 |
| 覆盖清单无效 | 行结构坏了 | `module_coverage.py check` 定位 |
| Finding 确认门禁未通过 | gate 未 ready | 读 `confirmation_gate.findings[].issues` |
