# Repo Ref
- source: https://github.com/findscripter/everything-skills (path: 08-security/security-antipattern-hook/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当 AI Agent 在写代码/改文件（涉及鉴权、支付、用户输入、IaC）时使用；提供一个 PreToolUse 钩子，在 Edit/Write/MultiEdit 落盘前用子串匹配拦截 12 类安全反模式（命令注入、XSS、SQL 注入、不安全反序列化、eval/new Function 代码注入、GitHub Actions 工作流注入）并产出告警；不适用于 AST 级精确扫描或 CI 阶段的
