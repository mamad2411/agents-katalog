---
name: hunt-rce
description: 受控执行链复核专项：仅在已确认的执行 primitive 与隔离执行窗口下评估 RCE 可行性、影响和证据；不从版本、上传、SSRF 或错误文本直接跳到命令执行。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-rce

## 0. Engagement Gate

- 只在记录了授权、锁定 scope、host/身份态 baseline 后执行；先用主入口确认此路线进入本轮候选。
- 只使用自有账户、对象、域名、回调和可回滚测试数据；WAF、验证码、超时和单次异常均为 `INCONCLUSIVE`。
- 固定节奏为 `baseline → 单变量 probe → post-baseline → oracle → evidence`。第三方资产、共享用户、生产副作用或超出书面窗口时立即停止。

## 1. Trigger Signals

`confirmed_primitive`、`execution_boundary`、`controlled_execution_marker`、`isolated_execution_window`、`cve_applicability_confirmed`。

## 2. Preconditions / Discovery

先读取主 Skill 的 `chain-review.md`，逐跳记录输入控制点、解释器/执行边界、权限、隔离、影响范围、回滚与证据。没有独立 primitive、窗口、marker 和 evidence 时不得启动此 Skill。

## 3. Minimal Safe Validation

仅使用书面批准的隔离实例、平台提供的 no-op execution marker 或预置无害测试任务，确认“应用实际执行”而不是回显/日志伪像。不得执行系统枚举、shell、脚本、网络回连、文件读写、持久化或横向动作。

## 4. Oracle / False Positives

有效：隔离环境中，可重复地观察到预置 no-op marker 被执行，且执行身份/上下文由服务器审计确认。banner、异常、输出反射、WAF 命中或 scanner finding 不成立。

## 5. Stop / Evidence / Routing

停止：没有隔离窗口、涉及生产/共享 worker、需要真实命令或数据访问。保存 primitive 原始证据、批准记录、marker/audit、pre/post baseline、影响边界。完成后只进入 `triage-validation`、证据与修复建议；不自动继续后渗透。
