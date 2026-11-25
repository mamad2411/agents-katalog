---
name: hunt-api-key-exposure
description: API Key 与客户端凭据暴露专项：区分公开设计的浏览器 key 与可用于敏感服务端操作的 credential，并只在自有 sandbox 验证 scope。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-api-key-exposure

## 0. Engagement Gate

- 仅在授权、scope、host/身份 baseline 和主编排器路由齐备时执行；本 Skill 规划验证，不授予目标操作权限。
- 只使用自有账户、对象、域名、测试数据、回调和批准速率；WAF、超时、单次异常、扫描器命中均为 `INCONCLUSIVE`。
- 固定执行 `baseline → 单变量 probe → post-baseline → server/browser/monitor oracle → evidence`；出现第三方数据、共享基础设施或不可回滚副作用立即停止。

## 1. Trigger Signals

`api_key_hint`、`client_key`、`public_config`、`authorization_header`、`third_party_sdk_key`、`key_scope_hint`。

## 2. Preconditions / Discovery

确认 key 来源、服务 owner、设计用途、限制（origin/referrer/IP/API scope）、当前有效性和自有 sandbox。字符串外观、base64、SDK config 不等于 secret。

## 3. Minimal Safe Validation

仅在组织自有测试 project/tenant 中使用预置 canary key 或 provider 的安全 introspection，验证公开 key 是否被正确限制；不得对生产/第三方服务调用或测试权限。

## 4. Oracle / False Positives

有效：被公开的自有 key 在其设计边界外仍能执行/读取受保护自有 canary，且 provider/audit 确认。key 格式、无效 key、公开 map、客户端报错不成立。

## 5. Stop / Evidence / Routing

停止：真实 key 使用、暴力验证、第三方 API、账单/资源操作。保存来源/hash prefix、限制配置、sandbox audit。source bundle 转 `hunt-source-leak`，云权限转 `hunt-cloud-misconfig`。
