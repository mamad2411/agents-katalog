---
name: good-skill
description: "一次性写入的存储(写坏就回不去)怎么写、怎么核对:写前先存原始内容,写后直接读回底层比对。触发词:一次性写入 / 写入前备份 / 读回比对 / write-once storage。"
---

# Good Skill — 写对的示例包 / a package that passes

> 这个包按证据纪律写全,`whetstone verify` 跑出来 0 个错误、0 个警告。
> Written to the evidence rules; `whetstone verify` finds nothing wrong with it.
> 同一个包故意改坏几处,就是 `examples/demo-skill`。

## 原理与约束 (L1)

- 一次性写入的存储写坏就回不去,所以写之前必须先把原始内容存下来。

## 设计与流程 (L2)

- 校验失败时先读回原始字节比对,不从上层现象反推。读回从哪开始见平台参数。

## 坑 (L2)

见 `pitfalls.md`。

## 禁止(本领域) (L2)

- 绝不在没存下原始内容之前写:一次性存储写坏了回不去,没有原始内容就无法复原。
- 绝不拿上层字段当写入成功的凭据:上层显示成功、底层没生效的情况真实存在。

## 平台参数 (L3)

> 具体值见 `params/soc-x.md`。
- 已支持平台:soc-x

## 溯源

- 来源:commit 1a2b3c4d
- 提炼日期:2026-09-02
- 复现记录:
  - soc-x · 2026-08-01 · commit 1a2b3c4d
  - proj-a · 2026-09-01 · commit 5e6f7a8b
- 验证方式:bash scripts/check.sh · 实测:通过 2026-09-01
- 置信度:high
