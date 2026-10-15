---
name: codex-token-summary
description: 统计本机 Codex 最近一段时间按任务目的维度消耗的 Token，并输出包含模型和分类占比的中文表格；仅在存在明确会话级字段时输出 Faster x2 状态。
version: 1.0.0
language: zh-CN
tags:
  - codex
  - token-usage
  - sqlite
  - jsonl
  - reporting
default_timezone: Asia/Shanghai
default_window: 最近 7 个自然日，排除周末休息日
---

# Codex Token 消耗统计

## 快速使用（推荐使用 Python 脚本）

本技能提供参数化的 Python 脚本，无需手工编写 SQL/JSON 解析代码。脚本位于本目录 `codex_token_summary.py`，支持灵活的时间范围、输出格式控制。

### 常用命令

```bash
# 最近 7 天简单表格（默认）
python codex_token_summary.py

# 最近 30 天
python codex_token_summary.py --days 30

# 自定义日期范围
python codex_token_summary.py --start-date 2026-04-01 --end-date 2026-05-18

# 详细格式（含 Token 分类）
python codex_token_summary.py --days 7 --format detailed

# 输出为 JSON
python codex_token_summary.py --days 14 --output json

# 包含周末
python codex_token_summary.py --days 30 --no-exclude-weekends
```

### Windows 环境初始化

若 Windows 上未安装 Python，使用同目录的 `setup_python_env.ps1` 一键安装并配置：

```powershell
# 以管理员身份运行 PowerShell，然后执行
.\setup_python_env.ps1
```

该脚本会自动检测 Python、从 python.org 下载官方安装包、加入 PATH，并安装脚本所需的依赖（仅 Python < 3.9 时需 `backports.zoneinfo`）。

### 脚本参数速查

| 参数 | 说明 | 示例 |
|------|------|------|
| `--days N` | 最近 N 天（默认 7） | `--days 30` |
| `--start-date YYYY-MM-DD` | 自定义开始日期 | `--start-date 2026-04-01` |
| `--end-date YYYY-MM-DD` | 自定义结束日期 | `--end-date 2026-05-18` |
| `--format simple\|detailed` | 输出详细程度（默认 simple） | `--format detailed` |
| `--output json\|table` | 输出类型（默认 table） | `--output json` |
| `--no-exclude-weekends` | 包含周末 | `--no-exclude-weekends` |
| `--tz TIMEZONE` | 时区（默认 Asia/Shanghai） | `--tz America/New_York` |

详见本目录 `README_SCRIPT.md`。

## 适用场景

当用户要求统计本机 Codex / Codex Desktop 在一段时间内的 Token 消耗，尤其是需要按任务目的、会话、模型、Token 类型占比输出表格时，使用本技能。

默认使用中文输出。除非用户另有说明，统计“最近 7 天”时按自然日回看 7 天。

## 数据源

主要读取两个本地数据源：

1. `~/.codex/state_*.sqlite`
   
   - 表：`threads`
   - 用途：获取线程 ID、任务目的、项目路径、模型、rollout 文件路径、创建/更新时间、总 Token 计数。
   - 应在 `~/.codex/` 下发现 `state_*.sqlite`，再按 schema 判断哪个是状态库。
   - 关键字段：
     - `id`
     - `rollout_path`
     - `cwd`
     - `title`
     - `preview`
     - `first_user_message`
     - `created_at`
     - `updated_at`
     - `tokens_used`
     - `model`
     - `reasoning_effort`
     - `agent_role`
     - `thread_source`
   
   兼容来源：
   
   - 旧的 `~/.codex/session_index.jsonl` 里 session 名称字段通常叫 `thread_name`，只在状态库缺失或需要交叉校验时使用。

2. `~/.codex/sessions/**/*.jsonl` 和 `~/.codex/archived_sessions/*.jsonl`
   
   - 路径通常来自 `threads.rollout_path`，不要只扫描 `sessions/`，因为较早或归档会话可能在 `archived_sessions/`。
   - 用途：读取 `token_count` 事件，按事件时间做增量统计。
   - 关键事件：
     - JSONL 行的 `type == "event_msg"`
     - `payload.type == "token_count"`
     - `payload.info.total_token_usage`

## 访问方式

优先发现可用的 Codex 状态 SQLite，再查询线程元数据，最后按 `rollout_path` 逐个读取 JSONL。

状态库发现规则：

1. 在 `~/.codex/` 下查找 `state_*.sqlite`。
2. 对候选文件执行 `.tables` 或查询 `sqlite_master`。
3. 选择包含 `threads` 表的文件。
4. 校验 `threads` 表至少包含这些字段：`id`、`rollout_path`、`cwd`、`created_at`、`tokens_used`。
5. 如果多个文件都匹配，优先选择最近修改时间最新的文件；必要时输出候选列表让用户确认。
6. 不要把 `logs_*.sqlite` 当主统计源。日志库可用于调试，但项目维度和 rollout 路径来自状态库的 `threads` 表。

示例查询：

```bash
STATE_DB="$(find ~/.codex -maxdepth 1 -name 'state_*.sqlite' -type f -print | sort | tail -1)"
sqlite3 -json "$STATE_DB" \
  "select id, rollout_path, cwd, title, preview, first_user_message, tokens_used, created_at, updated_at, model, reasoning_effort, agent_role, thread_source from threads"
```

_注意windows下使用符合windows powershell的脚本命令查询_

推荐用脚本聚合，而不是只使用 `threads.tokens_used`。原因是 `threads.tokens_used` 是线程级累计值，无法按天切分，也无法拆出缓存输入、输出、思考等类型。

## 时间范围

默认口径：

- 时区：`Asia/Shanghai`
- 当前日期以运行环境日期为准。
- “最近 7 天”表示包含今天在内的 7 个自然日。
- 排除 `weekday >= 5` 的日期，即周六和周日。
- 用 JSONL `token_count` 事件的 `timestamp` 判断是否落入统计范围。

示例：如果当前日期是 `2026-05-18`，统计范围为 `2026-05-12` 到 `2026-05-18`，实际计入工作日为 `2026-05-12`、`2026-05-13`、`2026-05-14`、`2026-05-15`、`2026-05-18`。

## 聚合算法

对每个 rollout JSONL 文件：

1. 读取对应 `threads` 行，生成“任务目的”作为主维度。
2. 顺序读取 JSONL 中的 `token_count` 事件。
3. 每个事件里的 `total_token_usage` 是线程累计值，不是单次增量。
4. 对同一文件内相邻 `token_count` 做差，得到本次事件增量。
5. 只累加事件时间落入统计工作日范围内的增量。
6. 按“任务目的”聚合总量。
7. 同时保留项目路径、模型、会话 ID 等明细，便于解释异常大头

任务目的生成规则：

1. 优先使用 `threads.title`。
2. 如果 `title` 为空或明显是系统审查/子 agent 长指令，可回退到 `threads.preview`。
3. 如果 `preview` 也不可用，可回退到 `threads.first_user_message` 的首行或前 80 个字符。
4. 保留 `thread_source` 和 `agent_role`，因为子 agent 的任务目的通常来自 spawn 指令，不一定等同用户原始需求。
5. 对过长任务目的做展示截断，但聚合键应使用完整值，避免不同任务被合并。

如果某个线程创建于统计范围内但找不到任何 `token_count` 事件，需要在结果里说明缺失，不要静默忽略。

## Token 分类

Codex 本地记录能直接拆出的字段：

- `input_tokens`
- `cached_input_tokens`
- `output_tokens`
- `reasoning_output_tokens`
- `total_tokens`

推荐输出分类：

- `新输入/检索上下文`：`input_tokens - cached_input_tokens`
- `缓存输入`：`cached_input_tokens`
- `输出/写代码`：`output_tokens - reasoning_output_tokens`
- `思考`：`reasoning_output_tokens`



## 统计维度

主维度：

- 任务目的：优先来自 `threads.title`，必要时回退到 `threads.preview` 或 `threads.first_user_message`

默认指标：

- `项目`
- `模型`
- `Token 总量`
- `占比`
- `新输入/检索上下文`
- `缓存输入`
- `输出/写代码`
- `思考`

可选辅助维度：

- 日期
- 会话 ID：`id`
- 项目路径：`cwd`
- 模型：`model`
- 推理强度：`reasoning_effort`
- 子 agent 类型：`agent_role`
- 线程来源：`thread_source`

## 模型

模型字段：

- 优先使用 `threads.model`。
- 如果 `threads.model` 为空，可从 rollout JSONL 的 `turn_context.payload.model` 中寻找模型字段。
- 不要把 `session_meta.payload.model_provider` 当成模型名；它通常只是供应商，例如 `openai`。
- 推理强度优先使用 `threads.reasoning_effort`；如果直接读 JSONL，可用 `turn_context.payload.effort`。
- 同一个任务目的下如果出现多个模型，表格中用逗号列出，或显示为 `mixed: model-a / model-b`。



## 输出格式

先用一段话说明统计口径，再输出表格。默认输出“简单”方案；只有用户明确要求详细分类、Token 类型占比、输入/缓存/输出/思考拆分时，才输出“详细”方案。

### 简单方案（默认）

先输出 `合计` 摘要行，再输出明细表格。`合计` 展示总 Token 量和 100% 占比。

```markdown
**合计 Token**：XXX（100%）
```

表格字段固定为：

| 任务目的 | 模型  | Token 总量 | 占比  |
| ---- | --- | --------:| ---:|

示例：

```markdown
| `统计近7天项目Token消耗` | `gpt-5.5` | 255,187,782 | 99.55% |
```

明细表格中不再包含 `合计` 行。

### 详细方案

用户要求详细输出时，先输出 `合计` 摘要行，再输出明细表格。`合计` 展示各分类汇总值及占总量的百分比。

```markdown
**合计 Token**：XXX（100%）| 新输入/检索上下文：XXX (XX%) | 缓存输入：XXX (XX%) | 输出/写代码：XXX (XX%) | 思考：XXX (XX%)
```

明细表格使用当前完整字段：

| 任务目的 | 项目  | 模型  | Token 总量 | 占比  | 新输入/检索上下文 | 缓存输入 | 输出/写代码 | 思考  |
| ---- | --- | --- | --------:| ---:| ---------:| ----:| ------:| ---:|


每个分类字段建议显示为：

```text
数量 (占该任务总量百分比)
```

例如：

```markdown
| `统计近7天项目Token消耗` | `/path/to/project` | `gpt-5.5` | 255,187,782 | 99.55% | 25,302,445 (9.91%) | 229,055,744 (89.76%) | 619,303 (0.24%) | 210,290 (0.08%) |
```

明细表格中不再包含 `合计` 行。

## 结果说明

表格后应补充一段限制说明：

- 数据来自本机 `~/.codex/state_*.sqlite` 中符合 schema 的状态库，以及 rollout JSONL。
- 分类中的 `缓存输入`、`输出`、`思考` 是 Codex 记录的结构化 Token 字段。
- “搜索、写代码、读文件”等语义类型没有独立精确字段，只能通过 Token 字段近似解释。
- 
- 如果存在缺失 rollout 文件或缺失 `token_count` 事件的线程，需要列出受影响线程数量和路径。

## 推荐校验

统计完成后做两项校验：

1. 检查是否有统计范围内创建的线程没有 `token_count` 事件。
2. 对比项目聚合总量与会话增量总量之和是否一致。
