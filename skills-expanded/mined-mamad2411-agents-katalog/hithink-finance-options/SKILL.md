---
name: hithink-finance-options
description: '用于 Agent 通过 hithink-finance CLI 查询公开期权品种、合约详情、分时和日 K；端内专用会话时间轴不在本 skill 范围。'
---

# hithink-finance-options

期权公开资料和行情入口。按完整 thscode 和固定行情参数查询。

## 前置条件表

| 条件                                   | 操作                                                                                                  |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| 开始任何 CLI 调用                      | 先读取并遵循 [hithink-finance-shared](../hithink-finance-shared/SKILL.md)                             |
| 不确定命令是否存在或参数是否变化       | 运行 `hithink-finance capabilities --format json`，再运行 `hithink-finance schema <id> --format json` |
| 需要执行下表某个命令                   | 先读取对应 reference 文件，不要只凭命令名猜参数                                                       |
| 结果可能是全市场、分页、多标的或长区间 | 使用命令声明的 `--output <path>` 落盘；远端 stdout 只返回摘要                                         |

## 快速决策

| 用户意图   | 首选命令 / 路由                      |
| ---------- | ------------------------------------ |
| 期权品种   | `options varieties`                  |
| 合约详情   | `options contract-detail`            |
| 分时或日 K | `options intraday` / `options daily` |

## Shortcuts

| 命令                                                             | 何时使用                                      |
| ---------------------------------------------------------------- | --------------------------------------------- |
| [options contract-detail](references/options-contract-detail.md) | Query options contract details                |
| [options daily](references/options-daily.md)                     | Query fixed 1d options prices                 |
| [options intraday](references/options-intraday.md)               | Query current options session intraday prices |
| [options varieties](references/options-varieties.md)             | List public options varieties                 |

## 原生命令与 schema

```bash
hithink-finance capabilities --format json
hithink-finance schema <capability-id> --format json
hithink-finance options <command> --help
```

使用原生命令前必须先看 schema；schema 是当前 CLI 参数契约，reference 是决策和边界补充。

## 权限表

| 命令类型                       | 要求                                                                   |
| ------------------------------ | ---------------------------------------------------------------------- |
| 远端服务查询                   | API Key 来自系统凭据库、`HITHINK_FINANCE_API_KEY` 或 `--api-key-stdin` |
| 本地 DuckDB 查询/导出          | 本地库存在且 schema 兼容；可用全局 `--db <path>` 指定                  |
| 删除、迁移、修复等有副作用操作 | 先预览或说明影响；需要用户明确确认时才加 `--yes`                       |

## 边界声明

- 分时 session 仅为 pre_market、intraday 或 post_market。
- 日 K 周期固定 1d；start/end 必须成对提供。
- 金融数值与日期允许 null，未知期权枚举保留原始编码。
