---
name: meeting-minutes-comparison
description: 政策会议横向比对。用 mx MCP 搜索，HITL 确认会议与维度，脚本仅生成 docx，比对由主模型完成。触发于「政策会议对比」「政治局会议比对」等。
version: 1.0.5
---

# Policy Comparison（AgentLoop 版）

## ⚠️ 执行规则（最高优先级 — 加载后必读）

用户要求政策会议比对时，**立即真实执行**，且**所有产物必须落盘为本地文件**：

| 必须做 | 禁止做 |
|--------|--------|
| **Step -1** 环境门禁（见下方「Shell 调用」）；失败则终止 | `cd /opt/...` 等宿主机绝对路径；`bash` 在 Windows 上 |
| 用 **mx MCP** `mx_finance_search_news` 取真实数据 | 调用 `scripts/main.py`、妙想 HTTP 直连接口 |
| **Step 2 HITL**：向用户确认会议列表与对比维度后再继续 | 未经用户确认就生成报告或比对 |
| `scripts/generate_policy_document.py` 逐会生成 docx，最多并发 2 场 | 在脚本内调用 LLM |
| 主模型按 [comparison_prompt.md](references/comparison_prompt.md) 生成比对 | 调用 `llm_client.py` 或脚本内 LLM |
| **Write** 全部 JSON + `comparison_result.md` 到 `skills/policy-comparison/output/{date}/` | 只在聊天里贴结果而不写文件 |
| 覆盖**已存在**文件前 **必须先 Read** | 对已存在文件直接 Write |

**路径根目录**（相对 workspace，Linux 优先）：

```
skills/policy-comparison/output/{YYYY-MM-DD}/
```

**Python 运行时**：见 [references/runtime.md](references/runtime.md)。**Shell 工具的 cwd 已是 workspace 根目录**，不要 `cd` 到 `/opt/app/...`。

加载后第一个动作：环境门禁 → Write 初始 `manifest.json`（status=running）→ MCP 搜索（Step 1）。

---

## Shell 调用（Windows / Linux）

> ⚠️ midas Agent 的 Bash 工具在 **Windows 上走 `cmd.exe`**，没有 `bash`，也**不存在** `/opt/app/...` 路径。

**不要**执行：
```text
cd /opt/app/applications/llm-platform-midas/workspaces/...   ← 必失败
find /d/ ...
```

**Windows（cmd，workspace 根目录下直接执行）：**
```text
skills\policy-comparison\scripts\run_py.cmd scripts\ensure_env.py --check
```

**Linux / macOS：**
```bash
bash skills/policy-comparison/scripts/run_py.sh scripts/ensure_env.py --check
```

Read/Write/Glob 路径一律用 **workspace 相对路径**，例如：
`skills/policy-comparison/references/defaults.md`

---

## Step -1：Python 环境门禁

按上一节「Shell 调用」执行 `ensure_env.py --check`（Windows 用 `run_py.cmd`，Linux 用 `run_py.sh`）。

- exit ≠ 0 → Write manifest `status=failed`；按 runtime.md 回复「环境不满足」，**不得**继续

---

## Step 0：初始化运行目录

1. 确定 `run_date`（默认今天北京时间 → `YYYY-MM-DD`）
2. `RUN_DIR = skills/policy-comparison/output/{YYYY-MM-DD}`
3. **Write** `{RUN_DIR}/manifest.json`：

```json
{
  "template_id": "policy_comparison",
  "run_date": "{YYYY-MM-DD}",
  "report_title": "政策会议横向比对分析",
  "status": "running",
  "mode": "agent_loop",
  "started_at": "<ISO8601 北京时间>",
  "run_dir": "skills/policy-comparison/output/{YYYY-MM-DD}"
}
```

4. **Write** `{RUN_DIR}/mcp_trace.json`：`{"run_date":"...","calls":[]}`

---

## Step 1：MCP 搜索政策会议

1. 根据用户 query 构造搜索语句（见 [query_examples.md](references/query_examples.md)）
2. 调用 MCP：`mx_finance_search_news`
3. **Write** `{RUN_DIR}/search_raw.json`
4. **Read** → 合并 → **Write** `mcp_trace.json`
5. 从结果中提炼**标准化会议名称**提案列表（主模型完成，见 [defaults.md](references/defaults.md)）

---

## Step 2：HITL — 确认会议与维度（强制暂停）

**在用户明确确认之前，不得进入 Step 3。**

1. 结合 MCP 结果与 [defaults.md](references/defaults.md)，向用户展示：
   - 拟对比会议（默认 3 场，从近到远）
   - 拟对比维度（默认列表，或说明将自动提炼）
2. 使用 [defaults.md](references/defaults.md) 中的确认话术，询问默认是否可用
3. 用户回复「可以/继续/确认」→ 采用提案；用户补充 → 更新会议和/或维度
4. 确认后 **Write**：
   - `{RUN_DIR}/hitl_config.json`（见 [observability.md](references/observability.md)）
   - `{RUN_DIR}/conferences.json`（见 [data_schema.md](references/data_schema.md)）
5. **Read** `manifest.json` → **Write** 更新 `search_query`、`conferences`、`comparison_dimensions`

---

## Step 3：生成各会议解读报告（docx）

对 `conferences.json` 中每场会议生成 docx。允许由 Agent 调度并行，但**同时运行的 `generate_policy_document.py` 最多 2 个**；必须等待已有任务完成后才能提交下一批。

```bash
scripts/run_py.sh scripts/generate_policy_document.py \
  --conference "{会议名称}" \
  --output-dir skills/policy-comparison/output/{date}/reports
```

- 认证：脚本通过 `EM_API_KEY` 调用 `mx-saas-platform` 聚合接口；不再使用 `CTOKEN`/`UTOKEN`/`UID`
- 调用方式：单次调用 `/policy-comparison/research`，由聚合接口完成多步骤大纲和正文生成
- 聚合接口失败时记录错误信息到 `quality_review.md`
- 脚本 stdout 为 JSON：`success`、`file_path` 等
- 失败时记录到 `quality_review.md`，可跳过该场并告知用户

---

## Step 4：读取报告内容

对每场成功生成的 docx：

```bash
scripts/run_py.sh scripts/read_docx.py --path "{docx_path}"
```

- 可选：汇总 **Write** `{RUN_DIR}/reports_content.json`
- 或主模型直接 **Read** docx / 使用 `read_docx.py` 输出

---

## Step 5：主模型横向比对（无脚本 LLM）

1. **Read** `conferences.json` 与各报告正文
2. 按 [comparison_prompt.md](references/comparison_prompt.md) 生成完整 Markdown（表格 + 差异总结）
3. **Write** `{RUN_DIR}/comparison_result.md`
4. **Read** 该文件，确认非空且含 Markdown 表格

---

## Step 6：可观测性与收尾

1. **Write** `{RUN_DIR}/timing.json`（见 [observability.md](references/observability.md)）
2. **Write** `{RUN_DIR}/quality_review.md`
3. **Read** `manifest.json` → **Write** 更新：`status=completed`，补全 `files`、`comparison_path`
4. 运行校验：

```bash
scripts/run_py.sh scripts/validate.py --date {YYYY-MM-DD}
```

---

## Step 7：回复用户

```markdown
## 政策会议横向比对已完成

- **运行日**：{YYYY-MM-DD}
- **比对报告**：`skills/policy-comparison/output/{date}/comparison_result.md`
- **工作目录**：`skills/policy-comparison/output/{date}/`

### 对比会议
{conferences 列表}

### 对比维度
{dimensions 或「自动提炼」}

### 中间产物
- `reports/*.docx` — 各会议解读报告
- `search_raw.json` / `mcp_trace.json` — 搜索与 MCP  trace
- `hitl_config.json` — 用户确认记录
- `timing.json` / `quality_review.md` / `manifest.json`

### 摘要
{comparison_result 差异总结前 2–3 句}
```

---

## 脚本一览

| 脚本 | 用途 |
|------|------|
| `scripts/ensure_env.py` | Python 环境门禁 |
| `scripts/run_py.sh` / `run_py.cmd` | 统一 Python 启动器 |
| `scripts/generate_policy_document.py` | 单会议 docx 生成（HTTP 流水线，无 LLM） |
| `scripts/read_docx.py` | 读取 docx 输出 JSON |
| `scripts/validate.py` | 交付物校验 |

## 参考文档

| 文件 | 用途 |
|------|------|
| [references/deliverables.md](references/deliverables.md) | 落盘路径与文件清单 |
| [references/defaults.md](references/defaults.md) | 默认会议/维度与 HITL 话术 |
| [references/comparison_prompt.md](references/comparison_prompt.md) | 主模型比对 prompt |
| [references/data_schema.md](references/data_schema.md) | JSON 字段 |
| [references/observability.md](references/observability.md) | timing / trace / quality |
| [references/query_examples.md](references/query_examples.md) | MCP query 示例 |
| [references/runtime.md](references/runtime.md) | Python 环境与 token |
