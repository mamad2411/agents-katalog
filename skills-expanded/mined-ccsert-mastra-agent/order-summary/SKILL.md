---
name: order-summary
description: 汇总用户给出的合成订单金额并生成简洁报表。适合订单统计、计算校验与平台接入验收。
license: MIT
compatibility: Node.js 24，脚本无需第三方依赖或网络。
metadata:
  author: agent-platform
  version: "1.0"
---
# 订单汇总

先读取 `references/report-rules.md`，确认报表规则。

从用户输入提取订单编号与金额，不补造缺失数据。使用平台的 `run_skill_script` 工具，选择 `order-summary` 和 `scripts/summary.mjs`。

脚本通过标准输入接收 JSON：

```json
{"orders":[{"id":"DEMO-001","amount":40},{"id":"DEMO-002","amount":80}]}
```

只使用脚本 stdout 中的真实结果生成回答。展示订单数、总额和逐笔金额。如果脚本失败，说明失败，不能编造执行结果。本示例不访问真实订单系统。
