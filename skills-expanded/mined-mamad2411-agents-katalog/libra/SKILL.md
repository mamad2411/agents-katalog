---
name: libra
description: Query and manage Libra/DataTester A/B experiments — experiment details, traffic allocation, app lists, experiment listing, parameter-path experiment search, report metadata, report rows, metric groups, realtime dashboards, and test users. Use whenever the user mentions Libra, DataTester, experiment flight IDs, A/B traffic, versions, P-Value, significance, metric groups, realtime, parameter-path search, or test-user management. Also trigger when the user wants completed/offline/historical experiments, not only active ones.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# Libra

Libra / DataTester A/B 实验查询与管理 agent。

## When to Use

- 查看实验详情、流量分配、版本配置、owner、tags
- 查看实验报告：指标数据、P-Value、显著性判断、趋势
- 查看实时指标、dashboard、metric group
- 搜索 / 筛选实验
- 按参数路径搜索实验
- 管理实验测试用户

## Quick Start

```bash
# Get experiment details
gdpa-cli run libra --session-id "$SESSION_ID" --input '{
  "action": "get_experiment",
  "flight_id": 123456,
  "vregion": "I18N-TT"
}'

# List experiments by keyword
gdpa-cli run libra --session-id "$SESSION_ID" --input '{
  "action": "list_experiments",
  "app_id": 22,
  "keyword": "tako",
  "vregion": "I18N-TT"
}'

# Search experiments by parameter path
gdpa-cli run libra --session-id "$SESSION_ID" --input '{
  "action": "search_experiment",
  "key_path": "tiktok.tako_server.use_old_lbs_location",
  "app_id": 22,
  "vregion": "I18N-TT"
}'

# Get report metadata first
gdpa-cli run libra --session-id "$SESSION_ID" --input '{
  "action": "get_report_meta",
  "flight_id": 123456,
  "app_id": 22
}'

# Preview test-user change first
gdpa-cli run libra --session-id "$SESSION_ID" --input '{
  "action": "add_test_user",
  "flight_id": 123456,
  "user_ids": ["10001", "10002"]
}'

# Apply only after confirmation
gdpa-cli run libra --session-id "$SESSION_ID" --input '{
  "action": "add_test_user",
  "flight_id": 123456,
  "user_ids": ["10001", "10002"],
  "confirmed": true
}'
```

## Workflows

### 判断实验结果是否显著

```bash
# 1. 查看实验基本信息
gdpa-cli run libra --session-id "$SESSION_ID" --input '{
  "action": "get_experiment",
  "flight_id": <flight_id>
}'

# 2. 列出可用指标组
gdpa-cli run libra --session-id "$SESSION_ID" --input '{
  "action": "get_report_meta",
  "flight_id": <flight_id>
}'

# 3. 查看具体指标组报告
gdpa-cli run libra --session-id "$SESSION_ID" --input '{
  "action": "get_report",
  "flight_id": <flight_id>,
  "metric_group_id": <metric_group_id>
}'

# 4. 如需趋势
gdpa-cli run libra --session-id "$SESSION_ID" --input '{
  "action": "get_report",
  "flight_id": <flight_id>,
  "metric_group_id": <metric_group_id>,
  "trend": true
}'
```

### 查看实时指标

```bash
# 1. 查看实验可用 dashboard
gdpa-cli run libra --session-id "$SESSION_ID" --input '{
  "action": "get_realtime",
  "flight_id": <flight_id>
}'

# 2. 查看 dashboard 详情
gdpa-cli run libra --session-id "$SESSION_ID" --input '{
  "action": "get_realtime",
  "dashboard_info": <dashboard_id>,
  "app_id": <app_id>
}'

# 3. 查看特定实时指标组
gdpa-cli run libra --session-id "$SESSION_ID" --input '{
  "action": "get_realtime",
  "flight_id": <flight_id>,
  "metric_group_id": <metric_group_id>
}'
```

### 搜索并查看实验

```bash
# 列出 App
gdpa-cli run libra --session-id "$SESSION_ID" --input '{"action":"list_apps"}'

# 按关键字列实验
gdpa-cli run libra --session-id "$SESSION_ID" --input '{
  "action": "list_experiments",
  "app_id": <app_id>,
  "keyword": "example"
}'

# 按参数路径搜索实验
gdpa-cli run libra --session-id "$SESSION_ID" --input '{
  "action": "search_experiment",
  "key_path": "example.feature_toggle"
}'
```

### 管理测试用户

```bash
# 查看测试用户
gdpa-cli run libra --session-id "$SESSION_ID" --input '{
  "action": "list_test_users",
  "flight_id": <flight_id>
}'

# 预览添加测试用户
gdpa-cli run libra --session-id "$SESSION_ID" --input '{
  "action": "add_test_user",
  "flight_id": <flight_id>,
  "user_ids": ["10001"]
}'

# 确认执行
gdpa-cli run libra --session-id "$SESSION_ID" --input '{
  "action": "add_test_user",
  "flight_id": <flight_id>,
  "user_ids": ["10001"],
  "confirmed": true
}'
```

## Key Notes

- `list_experiments` 和 `search_experiment` 默认要从起始页开始把后续所有页拿完，不要只拿第一页
- 对 optional 参数，优先使用显式输入、上下文推断、稳定默认值，不要把每个参数都变成追问
- `search_experiment` 结果受状态过滤影响。如果用户在找已完成 / 已下线 / 历史实验，需要包含 inactive 状态
- `get_realtime` 支持 dashboard 列表、dashboard 详情、实验 realtime 三种模式，不要混用
- `add_test_user` / `delete_test_user` 必须 preview first，再 `confirmed=true`
- `I18N-TT`、`row`、`ttp` 这类上下文通常指向 TikTok ROW 场景

## Parameter Resolution Workflow

按下面顺序处理参数，不要反过来：

1. 用户显式输入
2. 上下文推断
3. 稳定默认值
4. AskUserQuestion

### 直接用默认值，不要追问

- `page=1`
- `page_size=20`
- `exact_match=false`
- `merge_type=total`
- `period_type=h`
- `view_type=merge`

### 先推断，不要一上来就问

- `vregion`
- `app_id`
- `search_experiment.status`
- `version`（test-user 写操作）
- report 时间范围
- realtime 时间范围

如果上下文明显提到 `I18N-TT` / `row` / `ttp`，优先按 TikTok ROW 处理。

如果用户在找已完成 / 已下线 / 历史实验，`search_experiment` 不应只查 active 状态。

### 这些情况才应该 AskUserQuestion

- `get_experiment` / `get_traffic` / `get_report_meta` / `get_report` / `list_test_users` / `add_test_user` / `delete_test_user` 缺 `flight_id`
- `search_experiment` 缺 `key_path`
- `get_metric_group` 缺 `id`
- `get_metric_group_template` 缺 `template_id` 和 `url`
- `get_realtime` 既没有 experiment 目标，也没有 dashboard 目标
- `add_test_user` / `delete_test_user` 命中多个可写 version，但用户没指定 version

不要因为参数是 optional 就默认发问。

### 这些不是追问，是确认流程

- `add_test_user`
- `delete_test_user`

必须先 preview，再等待用户确认，然后才允许 `confirmed=true` 执行。

### 结果为空时的处理

如果 `search_experiment` 结果为空，不要直接断言“没有这个实验”。先检查：

- 状态过滤是否把历史实验排掉了
- `exact_match` 是否过严
- `app_id` 是否限制错了
- 上游 key-path 搜索语义是否和用户理解不同

## Action Overview

| Action | Description |
|--------|-------------|
| `get_experiment` | 实验详情（版本、owner、config、重要字段摘要） |
| `get_traffic` | 流量分配和版本权重 |
| `get_report_meta` | 可用指标组列表 |
| `get_report` | 实验报告（指标、P-Value、趋势） |
| `get_realtime` | 实时 dashboard / 实时指标 |
| `get_metric_group` | 指标组详情 |
| `get_metric_group_template` | 指标组模版 / bundle 详情 |
| `list_experiments` | 搜索和筛选实验 |
| `search_experiment` | 按参数路径搜索实验 |
| `list_apps` | 列出可用 App |
| `list_test_users` | 查看测试用户 |
| `add_test_user` | 添加测试用户（预览 + 确认） |
| `delete_test_user` | 删除测试用户（预览 + 确认） |

## Input Notes

- `flight_id` 是实验详情 / report / traffic / test-user 相关动作的关键参数
- `key_path` 是 `search_experiment` 的关键参数
- `id` 是 `get_metric_group` 的关键参数
- `template_id` 或 `url` 是 `get_metric_group_template` 的关键参数
- `page` / `page_size` 只是起始页和抓取批大小，不代表最终只返回这一页
- `get_report` 不带 `metric_group_id` 时，应先返回 report meta / 可用指标组
- `get_realtime` 只有 experiment 没有 metric group 时，优先给可用 dashboard
