---
name: te-meta
version: 1.0.0
description: "TE 元数据查询：事件目录、属性加载、实体、指标、SQL表结构"
metadata:
  requires:
    bins: ["te-cli"]
  cliHelp: "te-cli meta --help"
---

# te-meta

> **前置条件:** 请先阅读 [`../te-shared/SKILL.md`](../te-shared/SKILL.md)，了解认证、全局参数和输出格式。

## 概述

`te-cli meta` 域提供 ThinkingEngine 平台的元数据查询能力，覆盖以下核心对象：

| 对象 | 命令 | 说明 |
|------|------|------|
| 事件目录 | `+list-events` | 获取项目的完整事件列表 |
| 事件属性 | `+load-event-props` | 加载事件的可筛选属性 |
| 度量属性 | `+load-measure-props` | 加载事件的可度量属性 |
| 分析实体 | `+list-entities` | 获取分析实体列表 |
| 预定义指标 | `+list-metrics` | 获取预定义指标列表 |
| SQL 表 | `+list-tables` | 获取可查询的 SQL 表列表 |
| 表字段 | `+get-table-columns` | 获取指定表的字段定义 |

所有命令均为只读操作（`risk: read`），无需确认即可直接执行。

## 核心场景

### 1. 了解项目有哪些事件

```bash
te-cli meta +list-events --project-id 1
```

### 2. 为分析查询准备属性列表

先获取事件列表，再加载对应的可筛选 / 可度量属性：

```bash
# 加载筛选属性
te-cli meta +load-event-props -p 1 --events '[{"eventName":"login"}]'

# 加载度量属性
te-cli meta +load-measure-props -p 1 --events '[{"eventName":"login"}]'
```

### 3. 查询 SQL 表结构

先列出可用表，再获取目标表的字段定义：

```bash
te-cli meta +list-tables -p 1
te-cli meta +get-table-columns -p 1 --table "v_event_1"
```

### 4. 结合 jq 做字段提取

```bash
# 只输出事件名称
te-cli meta +list-events -p 1 --jq '.events[].eventName'

# 只输出指标名称和描述
te-cli meta +list-metrics -p 1 --jq '.metrics[] | {name, description}'
```

## 参考文档

详细的命令参数说明见 [`references/`](references/) 目录：

- [+list-events](references/list-events.md)
- [+load-event-props](references/load-event-props.md)
- [+load-measure-props](references/load-measure-props.md)
- [+list-entities](references/list-entities.md)
- [+list-metrics](references/list-metrics.md)
- [+list-tables](references/list-tables.md)
- [+get-table-columns](references/get-table-columns.md)
