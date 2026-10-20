---
name: hunt-xs-leaks
description: XS-Leaks 与浏览器侧信道专项：验证自有 cross-origin 页面是否可通过导航、frame、缓存、尺寸或时序推断受保护状态；不采集真实用户状态。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-xs-leaks

## 0. Engagement Gate

- 仅在授权、scope、host/身份 baseline 和主编排器路由齐备时执行；本 Skill 规划验证，不授予目标操作权限。
- 只使用自有账户、对象、域名、测试数据、回调和批准速率；WAF、超时、单次异常、扫描器命中均为 `INCONCLUSIVE`。
- 固定执行 `baseline → 单变量 probe → post-baseline → server/browser/monitor oracle → evidence`；出现第三方数据、共享基础设施或不可回滚副作用立即停止。

## 1. Trigger Signals

`cross_origin_frame`、`xs_leak_hint`、`cache_state_difference`、`timing_side_channel`、`window_navigation_signal`、`opaque_response`。

## 2. Preconditions / Discovery

确认两个自有 origin、两自有浏览器 profile、被测资源的敏感状态和浏览器版本；明确候选观测量是否可由攻击 origin 读取。CORS 阻止读取不自动排除 XS-Leak，也不自动证明问题。

## 3. Minimal Safe Validation

在隔离浏览器中比较“有/无自有 canary 状态”的单一跨源观测量，重复多次并控制缓存、网络与登录变量；不使用真实账号、私人内容或高精度性能采集。

## 4. Oracle / False Positives

有效：攻击 origin 能稳定地区分两种自有受保护状态，且该差异在控制变量后仍存在。单次时序差、开发者工具差异、同源读数不成立。

## 5. Stop / Evidence / Routing

停止：跨用户画像、第三方站点、自动化高频测量。保存浏览器版本、profiles、观测数据摘要、控制变量。CORS/缓存/redirect 分别转 `hunt-cors`、`hunt-cache-*`、`hunt-open-redirect`。
