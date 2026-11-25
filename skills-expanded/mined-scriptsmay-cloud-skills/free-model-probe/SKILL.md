---
title: "Free Model Probe"
type: skill
tags: [llm, free-models, inference, probing, monitoring, openai-compatible]
created: 2026-10-01
updated: 2026-10-02
author: scriptsmay
status: active
---

# Free Model Probe

免费推理模型可用性探测：动态发现、价格校验、真实推理三层检查。

A three-layer probe for free-tier models on any OpenAI-compatible inference API: dynamic discovery, pricing verification, and real inference.

## 为什么需要这个技能 / Why

模型目录（`/v1/models`）会撒谎。实测案例（2026-09-30，Nous Portal）：

- `stealth/space-bunny-alpha` 在目录中存在，`pricing` 显示 prompt/completion 均为 0
- 但真实 `chat/completions` 调用返回 HTTP 404 / 超时
- 只看目录和价格，会把一个不可用的模型当作默认模型，线上直接炸

**结论：listing ≠ serving。必须做真实推理探测。**

A model can be listed with price=0 yet fail on actual inference. Probing the catalog alone is not enough — you must send a real chat completion.

## 三层检查 / Three Layers

```
1. 动态发现 (Discovery)
   GET /v1/models → 过滤 ID 后缀为 :free 的模型
   （不要硬编码模型列表，目录会变）

2. 价格校验 (Pricing)
   检查 pricing.prompt == 0 && pricing.completion == 0
   （目录标 free 但价格非 0 的，降级为"异常条目"）

3. 真实推理 (Inference Probe)
   POST /v1/chat/completions
   {model: id, messages: [{role: user, content: "hi"}], max_tokens: 5}
   返回 choices 即为可用；error/404/超时即为不可用
```

## 告警策略 / Alert Policy

只在真正重要的事情上告警：

- **ALERT**：默认模型不可用，或可用免费模型数量为 0
- **INFO**（不告警）：目录中有但推理失败的条目（记录即可）
- **INFO**：可用集合的变化（新增/消失的模型，顺带报告）

连续失败计数：单次探测失败不告警（可能是网络抖动），连续 2 次失败才告警。

## 状态文件 / State

```json
{
  "consecutive_failures": 0,
  "last_alert": null,
  "last_working": ["model-a:free", "model-b:free"]
}
```

- `last_working` 用于检测可用集合变化（新增/消失）
- `consecutive_failures` 用于过滤瞬时故障

## 前置条件 / Prerequisites

- OpenAI-compatible API（`/v1/models` + `/v1/chat/completions`）
- Bearer token（环境变量或配置文件）
- `curl`（大响应体下比某些 HTTP 库更稳定）

## 检查清单 / Checklist

- [ ] `GET /v1/models` 能拿到目录
- [ ] `:free` 后缀过滤出候选模型（非硬编码）
- [ ] 每个候选都做了真实 `chat/completions` 探测（`max_tokens: 5` 最小开销）
- [ ] 告警只在默认模型失效或零可用时触发
- [ ] 状态文件持久化，支持跨次运行的变更检测
- [ ] 探测脚本输出 `OK:` / `ALERT:` 前缀，便于 cron 调度

## 参考实现 / Reference

`references/free-model-probe.py` — 通用探测脚本，填入 `API_BASE` 和 token 获取方式即可用。

## 实测记录 / Field Notes

- 2026-09-30（Nous Portal）：6 个可用 `:free` 模型；`space-bunny-alpha` 目录有、价格 0、推理 404 —— 由此确立"必须真实探测"原则
- 动态发现（`:free` 后缀过滤）比硬编码列表更鲁棒 —— 采纳自用户建议
