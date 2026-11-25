---
name: hithink-finance-futures
description: '用于 Agent 通过 hithink-finance CLI 查询公开期货品种、合约详情、持仓、仓单、基差、交易日程、分时和日 K；端内专用的品种板块、重点合约目录、F10 与会话时间轴不在本 skill 范围。'
---

# hithink-finance-futures

期货公开资料和行情入口。按完整 thscode、品种与日期语义选择稳定命令。

## 前置条件表

| 条件                                   | 操作                                                                                                  |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| 开始任何 CLI 调用                      | 先读取并遵循 [hithink-finance-shared](../hithink-finance-shared/SKILL.md)                             |
| 不确定命令是否存在或参数是否变化       | 运行 `hithink-finance capabilities --format json`，再运行 `hithink-finance schema <id> --format json` |
| 需要执行下表某个命令                   | 先读取对应 reference 文件，不要只凭命令名猜参数                                                       |
| 结果可能是全市场、分页、多标的或长区间 | 使用命令声明的 `--output <path>` 落盘；远端 stdout 只返回摘要                                         |

## 快速决策

| 用户意图       | 首选命令 / 路由                                                                 |
| -------------- | ------------------------------------------------------------------------------- |
| 期货品种       | `futures varieties`                                                             |
| 合约详情       | `futures contract-detail`                                                       |
| 品种或公司持仓 | `futures variety-positions` / `futures company-variety-positions`               |
| 合约持仓       | `futures contract-positions` / `futures contract-position-history`              |
| 仓单或基差     | `futures warehouse-receipts` / `futures latest-basis` / `futures basis-history` |
| 交易日程       | `futures trading-schedule`                                                      |
| 分时或日 K     | `futures intraday` / `futures daily`                                            |

## Shortcuts

| 命令                                                                                 | 何时使用                                           |
| ------------------------------------------------------------------------------------ | -------------------------------------------------- |
| [futures basis-history](references/futures-basis-history.md)                         | Query historical futures basis                     |
| [futures company-variety-positions](references/futures-company-variety-positions.md) | Query daily company positions by futures varieties |
| [futures contract-detail](references/futures-contract-detail.md)                     | Query futures contract details                     |
| [futures contract-position-history](references/futures-contract-position-history.md) | Query up to one year of futures contract positions |
| [futures contract-positions](references/futures-contract-positions.md)               | Query daily futures contract positions             |
| [futures daily](references/futures-daily.md)                                         | Query fixed 1d futures prices                      |
| [futures intraday](references/futures-intraday.md)                                   | Query current futures session intraday prices      |
| [futures latest-basis](references/futures-latest-basis.md)                           | Query latest main-continuous futures basis         |
| [futures position-companies](references/futures-position-companies.md)               | List futures position companies                    |
| [futures trading-schedule](references/futures-trading-schedule.md)                   | Query futures trading schedule                     |
| [futures varieties](references/futures-varieties.md)                                 | List public futures varieties                      |
| [futures variety-positions](references/futures-variety-positions.md)                 | Query daily futures variety positions              |
| [futures warehouse-receipts](references/futures-warehouse-receipts.md)               | Query historical futures warehouse receipts        |

## 原生命令与 schema

```bash
hithink-finance capabilities --format json
hithink-finance schema <capability-id> --format json
hithink-finance futures <command> --help
```

使用原生命令前必须先看 schema；schema 是当前 CLI 参数契约，reference 是决策和边界补充。

## 权限表

| 命令类型                       | 要求                                                                   |
| ------------------------------ | ---------------------------------------------------------------------- |
| 远端服务查询                   | API Key 来自系统凭据库、`HITHINK_FINANCE_API_KEY` 或 `--api-key-stdin` |
| 本地 DuckDB 查询/导出          | 本地库存在且 schema 兼容；可用全局 `--db <path>` 指定                  |
| 删除、迁移、修复等有副作用操作 | 先预览或说明影响；需要用户明确确认时才加 `--yes`                       |

## 边界声明

- 使用完整期货 thscode；品种代码必须大写并与合约匹配。
- 历史持仓开始日在调用日前一年内；daily 的 start/end 必须成对提供。
- 金融数值与日期允许 null，合法无数据数组保留为空数组。
