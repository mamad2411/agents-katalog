---
name: hunt-kubernetes-exposure
description: Kubernetes/容器暴露与配置专项：在确认自有集群和只读范围后验证公开面、身份/RBAC 和 workload 元数据暴露；不执行、提权、逃逸或读取 secrets。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-kubernetes-exposure

## 0. Engagement Gate

- 只在记录了授权、锁定 scope、host/身份态 baseline 后执行；先用主入口确认此路线进入本轮候选。
- 只使用自有账户、对象、域名、回调和可回滚测试数据；WAF、验证码、超时和单次异常均为 `INCONCLUSIVE`。
- 固定节奏为 `baseline → 单变量 probe → post-baseline → oracle → evidence`。第三方资产、共享用户、生产副作用或超出书面窗口时立即停止。

## 1. Trigger Signals

`kubernetes_marker`、`k8s_api_endpoint`、`ingress_controller`、`container_metadata`、`service_account_hint`、`helm_manifest`。

## 2. Preconditions / Discovery

必须确认 cluster/workload 归属、只读权限、测试 namespace/canary、审计日志与变更回滚人；公网端口或 header 不是 ownership 证据。

## 3. Minimal Safe Validation

只读枚举自有 canary namespace 的版本/健康/公开配置，比较匿名与批准的低权角色，使用官方 API discovery 或管理日志。禁止 token 获取、secret list、exec、port-forward、admission 改动或 runtime 操作。

## 4. Oracle / False Positives

有效：在 scope 内，匿名/低权身份可读取本不应公开的自有 canary 元数据或受保护 API，且 audit/RBAC 证实。banner、ingress 404、扫描器命中不成立。

## 5. Stop / Evidence / Routing

停止：secrets、service-account token、RBAC 修改、exec、pod 创建、container escape、跨 namespace。保存 scope/RBAC、audit、endpoint/version、canary read diff。Ingress/CVE 转 `cve-triage`，云归属转 `hunt-cloud-misconfig`。
