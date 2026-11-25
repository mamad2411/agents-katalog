---
name: bugx-dsh
description: BugX 漏洞挖掘引擎在 DeepSeek Harness (DSH) 宿主下的专属使用手册——新环境快速接入（构建/安装/doctor）、启动挖掘标准流程（pre 门禁→workers→checkpoint→post）、原生交互适配、Token 与模型用量采集。当用户在 DSH 里启动/排障/重置 BugX 审计、配置新环境或需要查看 DSH 本地模型与 Token 用量报告时使用本 skill。
---

# BugX × DeepSeek Harness (DSH) 使用手册（实战复盘版）

本手册专为 **DeepSeek Harness (DSH)** 宿主环境深度定制，支持切换环境后秒级快速接入、零交互 `--dev` 调试与原生审计闭环。

---

## 一、新环境快速接入（Fresh Machine Checklist）

切换新环境或新机器时，执行以下标准接入动作：

```bash
# 1. 确认 Python 与 Node 环境（Python >= 3.11，推荐 3.14；Node >= 20）
python3 --version && node --version

# 2. 从源码构建安装最新 bugx-agent（避免 wheel 滞后）
cd <repo-root> \
  && python3 -m build --wheel \
  && python3 -m pip install dist/bugx_agent-*.whl --force-reinstall --no-deps

# 3. 为 DSH 安装专属 Agent 与 MCP 插件双通道
bugx install --root <项目根路径> --agent dsh --non-interactive --force

# 4. 体检（确保环境全绿无死锁）
bugx doctor --root <项目根路径>
```

> **要点**：
> 1. DSH 的 MCP 插件配置由安装器自动注入至 Cordis Profile（`~/Library/Application Support/dsh-desktop/harness/profiles/headless/cordis.patch.yml`）。
> 2. DSH 插件采用低层 JSON-RPC 绕过 `@modelcontextprotocol/sdk` 的 Zod 版本断言冲突，确保工具调用零异常。

---

## 二、启动挖掘标准流程（DSH 宿主）

### 1. 初始化
```bash
cd <项目根路径>
bugx init
```
- 自动完成项目画像对齐与本地基线构建。
- 只有需要跨设备同步时才追加 `--cloud-sync sync`：`sync` 是显式授权（会写盘共享状态），不传则维持 `local`；`--dev` 同样默认 `local`，不会替你开同步。

### 2. 免交互极速启动（--dev 模式）
在调试或快速排查阶段，使用 `--dev` 跳过所有宿主问答阻塞：
```bash
bugx engine --root . pre --dev
```
- **自动初始化 Git 基线**：仅当目录还不是仓库时才 `git init`；缺身份时写入仓库级 `user.name=BugX Dev` / `user.email=bugx-dev@localhost`；仅在暂存区为空时提交空基线，索引非空则打印 `⚠ 暂存区已有内容` 并跳过——全程不会 `git add` 你的任何文件；
- **自动批准作战方案**：自动确认策略计划（`--strategy-plan approve`）；
- **全自动预设模式**：轮询 `auto`、审查 `mcp-auto`、修复 `auto`、提交 `round`、恢复 `resume`、启动动作 `start`；
- **云策略默认 `local`**：需要同步时显式传 `--cloud-sync sync`，或写入项目/全局配置的 `cloud_sync`。

### 3. 生成并发 Worker 与任务切片
```bash
bugx engine --root . workers --count 1
```
- 输出原子预占的 coverage unit 提示词切片（包含 `worker_id`、`lease_id` 与 `artifact_root`）。
- DSH 主智能体派发 Task 子智能体（`subagent_type: bugx-worker`），或者由当前会话并发承接。

### 4. Worker 执行、举证与 Checkpoint
在 Worker 子智能体中：
1. **立即确认开工**：
   ```bash
   python3 "$(bugx engine path --name audit_supervisor.py)" worker-start \
     --root . --state <supervisor.json> --worker <worker_id> \
     --provider dsh --execution-id exec-<lease_id>
   ```
2. **生成测试与证据**：
   - 将 PoC、Traceback、断言差异全部写入分配的 `artifact_root`。
3. **提交 Checkpoint**：
   ```bash
   python3 "$(bugx engine path --name worker_checkpoint.py)" finalize \
     --root . --state <supervisor.json> --worker <worker_id> \
     --status covered --artifact <artifact_path> \
     --command "<repro_cmd>" --exit-code 0 --tokens <tokens>
   ```

### 5. 封存报告与结算
```bash
export BH_PRE_BASELINE=<pre-baseline.json 绝对路径>
bugx engine --root . post
```
- 自动结算当前 Round、更新复盘账本，并输出结构化 Round 报告。

---

## 二·五、确认协议（candidate → confirmed）

> **这一章缺了会导致整轮 BLOCKED。** 实测：OctoPrintMCP 真实项目，dsh 产出 2 条
> 高质量 finding（high 路径穿越 + low 目录创建），有 severity/confidence/root_cause/
> reproduction/3-4 条 path+line evidence，唯独 `confirmation` 为空 →
> `finding_confirmation_pending` → 整轮判 blocked，`recovery_required: true`。
> 工作白做。根因是 dsh SKILL 此前没有本章，而 zcode SKILL 有。

### 为什么不能「产出即成功」

`_validate_incoming_findings` 在**摄入侧**就校验 `reproducible=True` 必须带非空
`reproduction`，完成门禁再查 confirmation。这是刻意的：未确认的 finding 若被
当成成功，用户会以为审计过了，而实际没人验证过该缺陷真的存在。

### 两步

**第 1 步：同指纹 ≥2 次独立运行**

同一个 finding 用**两个不同 channel** 各复现一次，各落一份 artifact：

```bash
# 两次运行，run_id / channel 必须不同，各自记录 artifact_path + sha256
python3 <你的探针>.py > state/host-confirmation/<slug>-a.json
python3 <你的探针>.py > state/host-confirmation/<slug>-b.json
```

**第 2 步：按 schema 提交 transition**

```bash
# 注意：transition 必须同时给 --id 和 --state，只给 --input 会被拒
python3 core/ledger/finding_confirmation.py transition \
  --input <payload>.json \
  --id <finding-id> \
  --state reproduced \
  --output <写回目标>.json
```

先用 `validate` 自检 schema，再用 `gate` 看还缺什么：

```bash
python3 core/ledger/finding_confirmation.py validate --input <payload>.json
python3 core/ledger/finding_confirmation.py gate     --input <payload>.json
```

payload 逐项必须，缺一即拒：

```json
{
  "schema_version": 1,
  "duration_seconds": 0,
  "findings": [{
    "id": "...", "fingerprint": "...", "title": "...",
    "severity": "high", "confidence": 0.95,
    "root_cause": "...",
    "evidence": [{"path": "src/x.py", "line": 64}],
    "reproducible": true,
    "reproduction": "python3 ...",
    "root_cause_verified": true,
    "confirmation": {
      "state": "reproduced",
      "oracle": {
        "tier": "differential",
        "reference": "...",
        "provenance": {
          "kind": "runtime-invariant",
          "independent_from_change": true,
          "verified": true
        }
      },
      "observations": [
        {"run_id": "run-a", "channel": "channel-a", "fingerprint": "...",
         "reference": "...", "outcome": "failure",
         "artifact_path": "...", "artifact_sha256": "..."},
        {"run_id": "run-b", "channel": "channel-b", "fingerprint": "...",
         "reference": "...", "outcome": "failure",
         "artifact_path": "...", "artifact_sha256": "..."}
      ],
      "negative_control": {"outcome": "pass", "reference": "..."},
      "root_cause": {"location": "...", "mechanism": "..."}
    },
    "target_execution": {
      "target_platform": "darwin-arm64-cpython-3.14",
      "executed_platform": "darwin-arm64-cpython-3.14",
      "executed": true, "simulated": false,
      "outcome": "failure", "errors": []
    }
  }]
}
```

### 四个实测踩过的坑

| 症状 | 原因 | 对策 |
|------|------|------|
| 目标平台与实际执行平台不一致 | `"darwin"` ≠ `"darwin-arm64-cpython-3.14"` | 两个字段**逐字相同** |
| negative_control 被拒 | `outcome` 写成 `"OK"` | 只能是 `failure` / `pass` / `blocked` |
| 两条 observation 不算独立 | 用了同一个 channel | 必须**两个不同** channel |
| post 快照校验失败 | `findings.json` 缺 `run_binding` | 顶层 `run_id` + `run_binding{run_id,lifecycle_id,round}` 与 `runtime.json` 逐字一致 |

### 确认之后

写回 lifecycle `findings.json`（confirmed 状态 + confirmation 块）→ post 自动结算 →
复盘自动落账 → Round 报告封存。

**只产出 candidate 不转 confirmed = 这一轮不算完成。** 宁可早期把
`reproducible` 显式置 `false` 并说明原因，也不要留下 `reproducible: true`
却没有 confirmation 的半成品——后者会让整轮卡住且难以定位。

## 三、Token 与模型用量核验（DSH 专属）

针对 DSH 宿主，系统内置专属用量收集器（`core/hosts/_dsh_usage.py`）：
1. **自动读取会话归档**：
   - 扫描 `~/Library/Application Support/dsh-desktop/harness/sessions/--<项目根>--/*.zstd` 日志；
   - 提取当前 Lifecycle 时间窗（`started_epoch` 至结算）内的所有交互记录。
2. **测试报告展示**：
   在 Round 结束报告中与 ZCode 保持一致，自动呈现细分指标：
   - `调度侧 Token（本地宿主采集）`：包含主控制面上下文 Token；
   - `Worker Token（宿主本地核验）`：Worker 执行开销；
   - `模型用量`：按模型展示调用次数、Input/Output/CacheRead/Total Token 及流式响应总耗时；
   - `模型调用时长汇总`：精确格式化时长（如 `12m 34s`）。
3. **明细持久化**：
   - 完整明细落盘于 `.bugx/.../state/dsh-usage.json`，只进本地报告，不污染云端 Schema。

---

## 四、重置与故障恢复

若运行态出现死锁或脏状态：
```bash
# 1. 清理残留 MCP 进程
ps aux | grep "mcp serve" | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null || true

# 2. 项目级状态重置
bugx reset --scope project --root . --yes

# 3. 重新以 dev 模式跑通
bugx init && bugx engine --root . pre --dev
```
