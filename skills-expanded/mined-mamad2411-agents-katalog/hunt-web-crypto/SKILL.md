---
name: hunt-web-crypto
description: 浏览器 Web Crypto 与客户端密钥边界专项：验证前端加密、签名、随机数、密钥存储、token 派生和降级处理是否把安全决策错误留在客户端。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-web-crypto

## 0. Engagement Gate

- 仅在授权、scope、host/身份 baseline 和主编排器路由齐备时执行；本 Skill 规划验证，不授予目标操作权限。
- 只使用自有账户、对象、域名、测试数据、回调和批准速率；WAF、超时、单次异常、扫描器命中均为 `INCONCLUSIVE`。
- 固定执行 `baseline → 单变量 probe → post-baseline → server/browser/monitor oracle → evidence`；出现第三方数据、共享基础设施或不可回滚副作用立即停止。

## 1. Trigger Signals

`web_crypto_api`、`client_side_encryption`、`hardcoded_crypto_material`、`weak_randomness_hint`、`signature_in_browser`、`key_storage_hint`。

## 2. Preconditions / Discovery

从范围内 bundle、DevTools 和真实请求确认算法、数据流、key 来源、服务端校验位置及是否影响身份/授权。编码、哈希或 Web Crypto 调用本身不等于漏洞。

## 3. Minimal Safe Validation

仅用自有 test account/canary 比较客户端生成的无害签名、nonce 或加密字段是否被服务端独立校验；本地离线复现可用于判断 deterministic/format 问题。不得尝试恢复或使用真实密钥。

## 4. Oracle / False Positives

有效：服务端接受本应被拒绝的自有边界输入，或关键安全决策可在浏览器端被改变而服务器无独立验证。minified 字符串、算法名、前端校验绕过不成立。

## 5. Stop / Evidence / Routing

停止：密钥提取、token 伪造、真实会话/支付/第三方数据。保存 bundle hash、数据流、server decision、test canary。JWT/signature 转 `hunt-jwt-crypto`/`hunt-webhook-signature`，DOM 转 `hunt-dom`。
