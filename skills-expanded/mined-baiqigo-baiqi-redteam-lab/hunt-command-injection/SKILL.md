---
name: hunt-command-injection
description: 命令注入专项：对已确认会把用户输入传入系统命令、任务运行器、转换器或诊断功能的路径，以无害可观察 marker 验证解析边界。用于 ping/dns/convert/git/archive/diagnostic/job 等输入信号；不默认执行命令、回连或读取系统数据。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-command-injection

## 0. Engagement Gate

- 仅在用户授权、范围锁定、已建立 host/身份态 baseline 后开展；专项执行前先运行主编排器确认该路线在本轮 Top 3。
- 仅使用自有账户、测试对象、回调域、测试数据和已批准速率。WAF/验证码/超时/单次异常均为 `INCONCLUSIVE`。
- 每个实验遵循 `baseline → 单变量 probe → post-baseline → oracle → evidence`；超出 scope、触及第三方、共享用户或产生不可回滚副作用立即停止。

## 1. Trigger Signals

`command_like_input`、`diagnostic_action`、`dns_lookup_feature`、`archive_converter`、`git_wrapper`、`job_runner`、`shell_error`、`process_execution_boundary`。

## 2. Preconditions / Discovery

先从真实浏览器/Burp 请求或源码证据确认：输入字段、可能调用的组件、同步/异步行为、字符集/编码、输出或任务状态 oracle。区分“服务端调用 library/API”和“shell 解释”：前者不能仅凭功能名称推定命令注入。

## 3. Minimal Safe Validation

优先使用应用明确提供的**自有、无害 marker**（例如测试域名解析记录、任务名称回显、固定输出文件名）验证分隔符/参数边界是否被当作一个值处理。对异步任务只查询自有任务状态。没有隔离执行环境或可观察 marker 时只记录假设，不尝试命令语法。

## 4. Oracle / False Positives

有效：单变量输入导致服务器侧任务参数/安全日志/受控 DNS marker 显示发生了非预期的额外解析，且可重现。shell-like 错误文本、客户端编码差异、WAF 拦截、前端字符串拼接不成立。

## 5. Stop / Evidence / Routing

停止：任何需要执行系统命令、写文件、回连、读取环境变量、触及内网或共享 worker 的验证。保存请求、输入编码、任务/日志 marker、组件版本和 pre/post baseline。只有确认执行边界后才进入 `hunt-rce` 与 `chain-review`；路径类输入转 `hunt-lfi`，模板类转 `hunt-ssti`。
