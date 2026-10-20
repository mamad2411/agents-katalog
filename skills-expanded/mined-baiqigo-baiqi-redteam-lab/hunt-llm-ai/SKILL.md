---
name: hunt-llm-ai
description: LLM 应用与 Agent 工具授权专项：验证聊天、Agent、function/tool calling、文件/RAG 输入与跨租户上下文是否保持数据边界、工具最小权限和人工确认。用于 chat、agent action、tool call、prompt template、document ingestion 信号；不诱导模型外带 secrets、不执行外部工具、不尝试绕过安全策略。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-llm-ai

## 0. Engagement Gate

- 仅在用户授权、范围锁定、已建立 host/身份态 baseline 后开展；专项执行前先运行主编排器确认该路线在本轮 Top 3。
- 仅使用自有账户、测试对象、回调域、测试数据和已批准速率。WAF/验证码/超时/单次异常均为 `INCONCLUSIVE`。
- 每个实验遵循 `baseline → 单变量 probe → post-baseline → oracle → evidence`；超出 scope、触及第三方、共享用户或产生不可回滚副作用立即停止。

## 1. Trigger Signals

`llm_chat`、`agent_tool_call`、`function_calling`、`prompt_template`、`document_ingestion`、`model_action`、`ai_plugin`。

## 2. Model the Trust Boundary

记录用户输入、系统提示、检索来源、工具声明、授权身份、审批点、输出渲染与日志。区分模型“说了什么”与应用实际执行/读取/写入；幻觉、拒答变化或提示文本回显不构成安全影响。

## 3. Minimal Safe Validation

使用自有测试文档、test tenant 和无害 canary，验证：是否跨租户返回 canary、工具调用是否需当前用户授权/确认、引用来源是否正确隔离、模型输出是否被安全渲染。不得让模型请求外部 URL、读取真实数据、执行命令、发邮件/支付或调用高权限 connector。

## 4. Oracle / False Positives

有效：干净自有会话获得另一自有 tenant 的 canary，或应用在未授权/未确认下实际调用敏感工具并有审计证据。模型声称可访问、prompt injection 文本出现、模拟工具返回都不成立。

## 5. Stop / Evidence / Routing

停止：真实秘密/客户文档、外部连接器、自动操作、不可回滚副作用。保存 conversation/test document hash、identity/tenant、工具审计和实际结果。向量检索转 `hunt-rag-vector`，输出 XSS 转 `hunt-xss`，权限问题转 `hunt-idor`/`hunt-auth-bypass`。
