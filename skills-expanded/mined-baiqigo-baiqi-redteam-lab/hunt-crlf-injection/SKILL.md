---
name: hunt-crlf-injection
description: CRLF 与 HTTP 响应分割专项：验证范围内输入是否能改变响应头、cookie、Location、日志或下游 HTTP 消息边界。用于 redirect/header/download filename、代理重写、邮件/日志 header 输入信号；不向共享缓存或其他用户投递第二响应。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-crlf-injection

## 0. Engagement Gate

- 仅在用户授权、范围锁定、已建立 host/身份态 baseline 后开展；专项执行前先运行主编排器确认该路线在本轮 Top 3。
- 仅使用自有账户、测试对象、回调域、测试数据和已批准速率。WAF/验证码/超时/单次异常均为 `INCONCLUSIVE`。
- 每个实验遵循 `baseline → 单变量 probe → post-baseline → oracle → evidence`；超出 scope、触及第三方、共享用户或产生不可回滚副作用立即停止。

## 1. Trigger Signals

`response_header_input`、`redirect_location`、`download_filename`、`proxy_rewrite`、`header_reflection`、`email_header_input`。

## 2. Discovery

捕获正常响应，记录 header 生成位置、URL decode 次数、CDN/反代层和 cookie/cache 语义。区分页面 body 中的换行回显与真实 HTTP header 解析；后者必须由 Burp raw response 或浏览器网络证据确认。

## 3. Minimal Safe Validation

仅在自有低流量测试路径，使用无害 header marker 检查编码、折叠与拒绝行为；每次只变一次转义形式。默认只允许观察本次响应，不尝试注入第二个请求/响应、不设置共享 cookie、不触发 redirect 到第三方。

## 4. Oracle / Stop

有效：server/proxy 在响应头中产生额外、非预期但无害的 marker header，且干净 baseline 不存在。body 反射、被编码的字符串、WAF 阻断、单次代理错误不成立。停止：cacheable/public response、跨用户 cookie、邮件投递、任何 response splitting 或 request smuggling 迹象；相关链路交 `hunt-http-smuggling` / `hunt-cache-poison`。

## 5. Evidence

保存完整脱敏 raw response、编码层、header 对照、缓存头、影响范围和清理确认。
