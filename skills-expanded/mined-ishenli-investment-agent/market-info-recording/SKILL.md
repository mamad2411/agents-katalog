---
name: market-info-recording
description: >
  沉淀市场分析信息到知识库（asset_market_info），以及回查已记录的市场评级、财报分析、投资观点。
  当用户说"把这条分析记下来"、"保存到市场信息"、"XX 我之前记录过什么评级"、"更新一下这个资产的市场信息"，
  或你刚完成一段有价值的分析、用户表示认可并希望下次复用时，**务必使用此技能**。
version: "1.0.0"
category: market
author: investment-agent
---

# 市场信息沉淀与回查

## 回查（读）

- `stockRecallMarketInfoTool`：按 `symbol` 查询知识库中该资产已记录的市场评级、财报分析、投资笔记。
- `dbQueryTool` 查表 `asset_market_info`（列：symbol, sentiment, importance, createdAt）可看最近入库记录：

```json
{"table": "asset_market_info", "whereColumn": "symbol", "whereValue": "AAPL", "orderBy": "created_at", "limit": 10}
```

## 保存（写）：marketInfoSaveTool

用户明确同意保存后调用。必填参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `asset_meta_ids` | ✅ | 数组，**已存在**的资产元数据 ID。先用 `dbQueryTool` 查 `asset_meta`（whereColumn: symbol）拿 ID，**禁止发明不存在的 ID** |
| `title` | ✅ | 信息标题 |
| `symbol` | ✅ | 资产代码 |
| `sentiment` | ✅ | 情绪评级：`positive` / `neutral` / `negative`（应用 UI 按这三个取值展示） |
| `importance` | ✅ | 重要性评分，1-10 的数字字符串（如 `"7"`） |
| `summary` | ✅ | 一段式摘要（供复用与分析时召回） |
| `market_impact` | ✅ | 市场影响描述 |
| `key_topics` | 可选 | 关键主题 |
| `key_data_points` | 可选 | 关键数据（如 P/E、目标价） |
| `source_url` / `source_name` | 可选 | 来源（来自互联网搜索时必填，标注出处） |

## 流程

1. 分析/检索得到结论 → 主动给出拟保存的摘要内容让用户确认。
2. 确认后：先查 `asset_meta` 拿资产 ID → 调用 `marketInfoSaveTool` → 复述保存结果。
3. sentiment / importance 不要放主观空话，写清楚理由（"negative：库存数据背离 + 高盛下调"）。

## 例外

- 保存失败（asset_meta 不存在该标的）时，告知用户该资产尚未纳入资产库，先在应用中添加资产。
