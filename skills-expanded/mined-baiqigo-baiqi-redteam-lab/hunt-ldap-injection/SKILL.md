---
name: hunt-ldap-injection
description: LDAP/目录查询注入专项：验证认证、用户搜索、组查询或同步接口对自有测试目录输入的 LDAP filter/attribute 边界。用于 LDAP 错误、directory search、AD/LDAP 登录、成员搜索或 filter 参数信号；不枚举真实目录、不转储用户。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-ldap-injection

## 0. Engagement Gate

- 仅在用户授权、范围锁定、已建立 host/身份态 baseline 后开展；专项执行前先运行主编排器确认该路线在本轮 Top 3。
- 仅使用自有账户、测试对象、回调域、测试数据和已批准速率。WAF/验证码/超时/单次异常均为 `INCONCLUSIVE`。
- 每个实验遵循 `baseline → 单变量 probe → post-baseline → oracle → evidence`；超出 scope、触及第三方、共享用户或产生不可回滚副作用立即停止。

## 1. Trigger Signals

`ldap_query_input`、`directory_search`、`ldap_error`、`ad_login`、`group_lookup`、`user_search_filter`。

## 2. Preconditions

需要隔离 LDAP/AD 测试 tenant 或服务方提供的自有测试用户/组，且要知道正常匹配与非匹配的 baseline。记录输入字段是 login、search 还是 authorization filter；不同功能风险和 oracle 不同。

## 3. Minimal Safe Validation

以两个自有目录对象建立正/负对照，仅改变一个 filter metacharacter、转义形式或括号结构。验证服务器是否严格转义、是否出现超出指定自有对象集合的匹配、是否改变认证/组成员语义。不要把错误信息当作目录内容泄漏。

## 4. Oracle / False Positives

有效：自有测试 filter 的逻辑边界被绕过，导致额外自有对象被匹配或认证/授权语义异常，且可复现。400/500、框架错误、模糊延迟或合法多属性搜索不是结论。

## 5. Stop / Evidence / Routing

停止：无法隔离目录对象、结果包含真实员工/客户、需要枚举/导出、或目录服务器跨 scope。保存 filter 输入的脱敏形式、正常/异常匹配集合、目录测试对象归属和角色差分。认证后果转 `hunt-auth-bypass`，SSO 转 `hunt-saml`。
