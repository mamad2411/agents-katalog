---
name: hunt-xss
description: XSS 专项：验证服务端/DOM/模板/属性/URL 等上下文中，不受信任的自有 canary 是否在隔离浏览器真实执行；不影响其他用户或外带数据。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-xss

## 0. Engagement Gate

- 仅在授权已声明、scope 已锁定并建立了 host / 身份 / 路径 baseline 后进入；主编排器只把本 Skill 作为候选流程，不构成对目标执行动作的授权。
- 只使用自有账户、对象、域名、测试数据和批准速率。WAF、验证码、超时、单次错误、扫描器命中均为 `INCONCLUSIVE`。
- 每一步保持 `baseline → 单变量 probe → post-baseline → server/browser oracle → evidence`；越界、第三方数据、共享用户或不可回滚副作用立即停止。

## 1. Trigger Signals

`reflected_input`、`stored_input`、`dom_sink`、`html_context`、`javascript_context`、`attribute_context`、`admin_bot_hint`。

## 2. Preconditions / Discovery

确定输入生命周期、渲染上下文、编码/净化、CSP、身份态、存储受众和回显位置。需要浏览器执行 oracle；HTML 回显、script 字符串或标签显示不等于 XSS。

## 3. Minimal Safe Validation

在自有会话/自有测试内容中使用无害的、不可外带的 execution canary，结合 DevTools console/network 和 CSP 报告确认是否真的执行。stored 场景不让其他用户/机器人加载。

## 4. Oracle / False Positives

有效：浏览器在预期上下文执行自有 canary，且 input-to-execution trace 可复现。反射、编码、被 CSP 拦截、仅 DOM 文本、WAF 页面不成立。

## 5. Stop / Evidence / Routing

停止：cookie/token 读取、钓鱼、管理员/第三方、跨租户存储、外部回连。保存 context、sanitization/CSP、browser evidence；DOM 转 `hunt-dom`，会话/CSRF 影响先做 `chain-review`。
