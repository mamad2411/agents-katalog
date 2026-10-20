---
name: hunt-cache-deception
description: Web Cache Deception 专项：验证动态/认证内容是否因路径后缀、重写或缓存规则被错误缓存并在无认证的自有 profile 中读取。用于 account JSON、静态后缀、rewrite、CDN/cache headers 信号；不同于 unkeyed-input 的 cache poisoning。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-cache-deception

## 0. Engagement Gate

- 仅在用户授权、范围锁定、已建立 host/身份态 baseline 后开展；专项执行前先运行主编排器确认该路线在本轮 Top 3。
- 仅使用自有账户、测试对象、回调域、测试数据和已批准速率。WAF/验证码/超时/单次异常均为 `INCONCLUSIVE`。
- 每个实验遵循 `baseline → 单变量 probe → post-baseline → oracle → evidence`；超出 scope、触及第三方、共享用户或产生不可回滚副作用立即停止。

## 1. Trigger Signals

`authenticated_dynamic_page`、`cacheable_path_suffix`、`url_rewrite`、`cdn`、`x_cache_header`、`static_extension_route`。

## 2. Preconditions

要求隔离 cache 测试窗口、两名自有账户/无认证 profile、可控 URL namespace、TTL/purge 计划。先建立认证与无认证页面 baseline、缓存 MISS/HIT 行为和随机路径对照。

## 3. Minimal Safe Validation

在自有低敏感页面，用无害测试 profile data 访问一个路径语义变体，然后以无认证自有 profile 请求同一 URL。只观察自己的测试内容；每轮后 purge 或等候 TTL 并确认恢复。

## 4. Oracle

有效：无认证 profile 在 cache headers 和时间线支持下获得原本仅认证可见的**自有** marker，且能排除浏览器缓存、same-session、前端 fallback 与正常公开页面。仅 200、CDN header 或路径映射不构成漏洞。

## 5. Stop / Evidence / Routing

停止：共享公共页面、未知 TTL/purge、可能缓存真实用户数据、跨用户验证。保存 profile/身份态、请求序列、Age/X-Cache/Vary、marker、清理记录。unkeyed header 影响转 `hunt-cache-poison`。
