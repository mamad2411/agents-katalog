---
name: hunt-iac-secret-exposure
description: IaC、Terraform state 与部署配置暴露专项：识别范围内公开 state、plan、manifest、artifact 和配置引用，不使用其中的凭据。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-iac-secret-exposure

## 0. Engagement Gate

- 仅在授权、scope、host/身份 baseline 和主编排器路由齐备时执行；本 Skill 规划验证，不授予目标操作权限。
- 只使用自有账户、对象、域名、测试数据、回调和批准速率；WAF、超时、单次异常、扫描器命中均为 `INCONCLUSIVE`。
- 固定执行 `baseline → 单变量 probe → post-baseline → server/browser/monitor oracle → evidence`；出现第三方数据、共享基础设施或不可回滚副作用立即停止。

## 1. Trigger Signals

`terraform_state`、`iac_manifest`、`deployment_config`、`cloud_secret_hint`、`public_artifact`、`state_file_url`。

## 2. Preconditions / Discovery

确认资源当前公开、在 scope、归属组织且不含需访问的私密后端；记录 storage ACL、versioning、artifact 来源和配置用途。不要由文件名推断 state 可读。

## 3. Minimal Safe Validation

仅只读获取当前公开且批准的自有 canary 配置/manifest，核实是否含基础设施拓扑、非敏感变量或指向受保护 secret 的引用；所有疑似凭据只记录字段位置/指纹，不尝试登录。

## 4. Oracle / False Positives

有效：范围内 artifact 可复现公开并包含本不应公开的自有基础设施/配置元数据，或组织确认访问控制错误。敏感字符串正则、过期 URL、第三方 bucket 不成立。

## 5. Stop / Evidence / Routing

停止：secret/token 使用、私有 state 下载、云 API 调用、跨账户资源。保存 URL/hash/ACL/owner evidence 和脱敏字段名。云暴露转 `hunt-cloud-misconfig`，CICD 转 `hunt-cicd`。
