---
name: req2excel-zh
description: 子 Skill：PRD → 测试用例.xlsx 初稿。由 req-suite-orchestrator-zh 调用。触发词：req2excel、PRD 转 Excel、生成测试用例表。
disable-model-invocation: true
---

# PRD → Excel（子 Skill）

> 端到端编排 → **req-suite-orchestrator-zh**

## 输入

- `requirements/<featureId>/prd.md`（由 req_ingest 生成）
- `requirements/<featureId>/meta.json`

## 输出

- `requirements/<featureId>/测试用例.xlsx`（**评审状态默认「草稿」**）

## 命令

```bash
python scripts/tools/req2excel.py requirements/<featureId>/
```

规则解析：读 PRD `## 验收标准` **每条 → 一行 TC**；自动填「关联脚本」（来自 PRD 关联自动化段）。手机号、断言写在 **步骤描述 / 预期结果**。

## Agent 精修

PRD 复杂时 Agent 构造 `rows.json`（列顺序见 req-suite `reference/excel-columns.md`）：

```bash
python scripts/tools/req2excel.py requirements/<featureId>/ --rows-json rows.json
```

## 禁止

- 默认改为「已通过」
- 跳过 openpyxl（`pip install openpyxl`）
