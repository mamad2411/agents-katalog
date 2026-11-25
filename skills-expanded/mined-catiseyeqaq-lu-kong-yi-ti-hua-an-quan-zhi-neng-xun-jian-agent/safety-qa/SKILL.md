---
name: safety-qa
description: 受限安全知识问答：基于隐患特征库与当前上下文，不进行开放域臆答。
when_to_use: 安全员询问规范依据、整改措施、当前隐患解释
allowed_tools:
  - safety_knowledge_qa
---

# 安全知识问答

仅检索 `pit_hazard_library` 与 `context_hazards`；合规真假仍由识别阶段 AST+门控决定。
