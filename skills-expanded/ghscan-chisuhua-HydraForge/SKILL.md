---
name: code-review-run
version: 0.3
description: 运行 code-review 工具审查代码文件（顶层 call_tool 语法，匹配 SkillInterpreter V1 解释器支持范围）
---

# 调用 fs.read 读取文件 + code_review/run 审查
call_tool("fs.read", {"path": "examples/pdk_chat_demo/main.cpp"})
call_tool("code_review/run", {"level": "thorough"})
return code_review_run