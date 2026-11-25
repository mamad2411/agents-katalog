---
name: hunt-redos
description: ReDoS 与应用层资源边界专项：仅在批准性能窗口验证正则、解析器或输入处理是否存在可测量且可回滚的资源异常；不对生产实施耗尽。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-redos

## 0. Engagement Gate

- 只在记录了授权、锁定 scope、host/身份态 baseline 后执行；先用主入口确认此路线进入本轮候选。
- 只使用自有账户、对象、域名、回调和可回滚测试数据；WAF、验证码、超时和单次异常均为 `INCONCLUSIVE`。
- 固定节奏为 `baseline → 单变量 probe → post-baseline → oracle → evidence`。第三方资产、共享用户、生产副作用或超出书面窗口时立即停止。

## 1. Trigger Signals

`regex_validation`、`redos_marker`、`catastrophic_backtracking`、`parser_timeout`、`input_length_limit`、`availability_error`。

## 2. Preconditions / Discovery

要求书面性能窗口、隔离测试路径、容量 owner、基线指标、明确停止阈值和恢复方案。先在本地/同版本离线环境复现候选正则，不在在线目标探索输入长度。

## 3. Minimal Safe Validation

使用预先批准的极小测试梯度和单请求，在停止阈值前比较服务端处理时延、CPU/队列和错误率；超过阈值立即中止并恢复。优先使用 vendor fixture/本地复现。

## 4. Oracle / False Positives

有效：在隔离窗口内，输入规模小幅增长导致与基线不成比例、可重复的服务器端资源/时延变化，并由监控证实。网络抖动、WAF、客户端计时不成立。

## 5. Stop / Evidence / Routing

停止：任一资源阈值、共享生产、无监控、并行请求。保存批准、input class（不含危险值）、监控时间线、阈值和恢复记录。框架/CVE 转 `cve-triage`；不自动升级为 DoS。
