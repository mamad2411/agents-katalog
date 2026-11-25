---
name: brief-data
description: "为周期简报整理数据：统一口径、汇总成表、写明未计入项时使用。"
metadata:
  pibot-name: "简报数据"
  pibot-version: "4"
  pibot-verified: "2026-10-23 · 真实资料两期 / two real periods"
  pibot-contract: "{\"inputs\":[{\"name\":\"本期资料\",\"kind\":\"folder\",\"required\":true},{\"name\":\"口径说明\",\"kind\":\"text\",\"required\":false}],\"deliverables\":[{\"id\":\"data\",\"path\":\"data.md\",\"kind\":\"md\",\"sections\":[\"口径\",\"数据表\",\"未计入\"]}],\"acceptance\":[{\"id\":\"d1\",\"check\":\"exists\",\"deliverable\":\"data\"},{\"id\":\"d2\",\"check\":\"sections\",\"deliverable\":\"data\"},{\"id\":\"columns\",\"check\":\"tableColumns\",\"columns\":[\"指标\",\"数值\",\"来源\"],\"deliverable\":\"data\"}],\"stop\":[\"口径不明确时写出采用的口径和理由，不要停下来\"],\"maxFixRounds\":2,\"budget\":{\"costUsd\":0.3},\"model\":{\"tier\":\"cheap\",\"thinking\":\"low\"}}"
---

# 简报数据

## 步骤
1. 找出资料里的表格和数字（csv / xlsx / 文本中的数），先用 csv-profile 看结构。
2. 统一口径（时间范围、单位、去重规则），汇总成表，每行注明来源文件。
3. 算不了或不该算的列进「未计入」，说明原因。

## 交付物
`data.md`，小节：口径、数据表、未计入。
