---
name: trade-journal
description: 把交易/持仓截图或口述结构化录入「交易日志」——记下标的、方向、股数、成本价、建仓日、账户，并当场确认每笔的「来源框架」(framework/直觉/消息/未归因)，写入独立的交易日志表（默认本地 CSV/Markdown，飞书/Notion 等为可选适配器），并联动 openorder thesis-ledger 做归因与盈亏。当用户发券商/持仓/成交截图、说"记一笔/记账/录入交易/建仓/加仓/减仓/平仓/这是我的持仓""帮我把这单记下来""更新持仓"时使用。配合 openorder(归因+thesis-ledger)、stock-data-fetch(现价算盈亏)、claim-verification(截图数字不臆造)。
---

# Trade Journal（交易日志：截图/口述 → 结构化录入）

> **目的**：把"建仓即记"变成习惯——每笔交易记下**成本价 + 建仓日 + 来源框架**，让 openorder `thesis-ledger.md` 的盈亏栏能自动回填、框架命中率自然累积。这是闭合「分析→建仓→盈亏→校准」环最缺的一步。
> **接线**：归因/落档走 [`openorder`](../openorder/SKILL.md)；现价算盈亏走 [`stock-data-fetch`](../stock-data-fetch/SKILL.md)；截图数字不臆造走 [`claim-verification`](../claim-verification/SKILL.md)（看不清的标 ⚠️，不编）。
> **铁律**：交易写入**独立的**交易日志表，**绝不写用户原有的展示/持仓表**，避免污染既有结构与数字。

## 存储后端（默认本地，云端可选）

为了让任何人开箱即用，默认把交易日志存成**本地文件**，云端表格是可选适配器：

| 后端 | 路径 / 配置 | 适用 |
|---|---|---|
| **本地 CSV**（默认） | `${TRADE_JOURNAL:-$HOME/openorder/trade-journal.csv}` | 零依赖，纯文本，git 可追踪 |
| **本地 Markdown 表** | `${OPENORDER_HOME:-$HOME/openorder}/trade-journal.md` | 想跟 openorder wiki 放一起、用 Obsidian 浏览 |
| **云端表格**（可选） | 飞书/Google Sheets/Notion 等，token 放环境变量，**不要硬编码进本仓库** | 多端同步 / 团队共享 |

> 用云端表格时，把 spreadsheet token、sheet_id 等放进你自己的环境变量或本地配置（如 `~/.config/trade-journal/config`），**永远不要把私有 token 提交到任何公共仓库**。

## 表头（统一列结构，CSV/表格通用）

```
日期,账户,标的,方向,股数,成本价,货币,金额,来源框架,thesis-id,备注
```

| 列 | 字段 | 说明 |
|---|---|---|
| 日期 | 成交日 YYYY-MM-DD | |
| 账户 | 券商/钱包名 | FUTU/Tiger/IBKR/Wallet… |
| 标的 | ticker 或中文名 | |
| 方向 | 买 / 卖 / 加仓 / 减仓 / 平仓 | |
| 股数 | 数量 | |
| 成本价 | 成交单价 | |
| 货币 | USD/CNY/HKD… | |
| 金额 | 股数×成本价（本币） | |
| 来源框架 | `framework:{id}` / 直觉 / 消息 / 未归因 | **每笔必确认** |
| thesis-id | 关联 openorder thesis-ledger 的 ID | 可空 |
| 备注 | 截图看不清/存疑的标注在此 | |

## 录入工作流

```
1. 读输入（截图用 Read 读图 / 口述直接取）
   → 抽取每笔：日期、账户、标的、方向、股数、成本价、货币
   → 看不清的字段标 ⚠️，向用户确认，绝不臆造（claim-verification 纪律）

2. 逐笔确认「来源框架」（关键人机边界，必须问）
   → 这笔是哪个框架/thesis 驱动的？还是直觉/消息/未归因？
   → 这是把人的判断变成可复利训练信号的入口，不能省

3. 追加到交易日志表（仅此独立表，不碰原始持仓表）
   → 本地 CSV：按表头顺序 append 一行（多笔批量）；首次创建先写表头
   → 云端表格：用对应 CLI/API append；写前先确认表结构与 sheet_id
     （注意各家 append API 的 range 行数必须 ≥ 要写的行数）

4. 联动 openorder（归因闭环）
   → 框架驱动的建仓：在 thesis-ledger 对应/新建 thesis，回填 头寸=framework:X + 成本 + 建仓日
   → 未归因的：标 直觉/消息，列入复盘提醒
   → 追加 openorder log（action=decision）

5. 回执
   → 列出记了哪几笔、来源框架、写到表的第几行；ASK 是否要据此更新持仓敞口
```

## 盈亏计算（查询时）

要看盈亏时：从交易日志取成本，用 `stock-data-fetch` 取现价（标时间+源），`盈亏 = (现价−成本价)×股数`。**铁律**：框架对错（thesis 结果）与头寸盈亏分开记分，不用单笔盈亏给框架定生死（见 openorder `frameworks/outcome-tracking.md`）。

## 边界：何时不要用我
- 用户只是问行情/分析，没有"记一笔/录入"意图 → 不要触发（那是 strategic-materials / openorder 的活）。
- **绝不写用户的原始持仓/展示表**；只写独立交易日志表。
- 截图数字模糊读不准 → 标 ⚠️ 让用户确认，不猜不填。

## 反模式
- ❌ 不确认来源框架就录入（丢掉最有价值的归因信号）。
- ❌ 把看不清的成本价/股数硬填一个数（违反 claim-verification）。
- ❌ 写进原始持仓表导致结构/数字被污染。
- ❌ 用单笔盈亏判定框架好坏（要看命中率 n，且对错≠盈亏）。
- ❌ 把私有云端表 token 硬编码进公共仓库（放环境变量）。
