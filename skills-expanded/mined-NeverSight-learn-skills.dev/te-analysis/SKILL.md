---
name: te-analysis
version: 1.0.0
description: "TE 分析查询：报告管理、仪表盘管理、SQL 查询、报告数据查询"
metadata:
  requires:
    bins: ["te-cli"]
  cliHelp: "te-cli analysis --help"
---

# te-analysis

> **前置条件:** 使用本技能前，请先阅读 [`te-shared/SKILL.md`](../te-shared/SKILL.md)，了解认证、全局参数和安全约束。

TE 分析域（`te-cli analysis`）提供报告与仪表盘的管理能力，以及通过 WebSocket 进行数据查询的能力。

## 核心场景

### 1. 查询数据

- **报告数据查询** — 通过 `+query-report-data` 使用 WebSocket 获取已有报告的计算结果
- **SQL 查询** — 通过 `+query-sql` 直接执行 SQL 查询，灵活获取任意数据

### 2. 报告管理

- **列出报告** — `+list-reports` 获取项目下所有报告
- **查看报告** — `+get-report` 获取单个报告的完整定义
- **保存报告** — `+save-report` 创建或修改报告（write 操作，需确认）

### 3. 仪表盘管理

- **列出仪表盘** — `+list-dashboards` 获取项目下所有仪表盘
- **查看仪表盘** — `+get-dashboard` 获取仪表盘详情
- **创建仪表盘** — `+create-dashboard` 新建仪表盘（write 操作）
- **更新仪表盘** — `+update-dashboard` 更新仪表盘布局（write 操作）
- **仪表盘报告列表** — `+list-dashboard-reports` 列出仪表盘中的报告

## 示例

### 查询已有报告数据

```bash
# 查询报告 ID 为 42 的数据
te-cli analysis +query-report-data -p 1 --report-id 42

# 指定时间范围
te-cli analysis +query-report-data -p 1 --report-id 42 \
  --start-time "2026-01-01 00:00:00" --end-time "2026-01-31 23:59:59"
```

### SQL 自由查询

```bash
# 按事件分组统计
te-cli analysis +query-sql -p 1 \
  --sql "SELECT event, count(*) FROM ta.v_event_1 GROUP BY event LIMIT 20"
```

### 报告管理流程

```bash
# 列出所有报告
te-cli analysis +list-reports -p 1

# 查看某个报告定义
te-cli analysis +get-report -p 1 --report-id 42

# 创建新报告（write，需确认）
te-cli analysis +save-report -p 1 --report-name "DAU 趋势" \
  --report-model 0 \
  --events '[...]' --event-view '{...}'
```

### 仪表盘管理流程

```bash
# 列出仪表盘
te-cli analysis +list-dashboards -p 1

# 创建新仪表盘
te-cli analysis +create-dashboard -p 1 --dashboard-name "运营日报"

# 向仪表盘添加报告
te-cli analysis +update-dashboard -p 1 --dashboard-id 10 \
  --reports '[{"reportId": 42, "reportWidth": 6, "indexOrder": 0}]'

# 查看仪表盘中的报告
te-cli analysis +list-dashboard-reports -p 1 --dashboard-id 10
```

## 参考文档

详细的命令 Flags 和用法请查看 [`references/`](./references/) 目录下的各命令文档。
