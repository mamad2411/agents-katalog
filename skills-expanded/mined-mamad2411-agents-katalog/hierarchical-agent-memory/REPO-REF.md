# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-one-step-beh1nd-skillbank/findscripter-everything-skills-hierarchical-agent-memory-04-/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 当项目有 3+ 目录、智能体每轮都重读整个工程导致输入 token 暴涨时使用；做分层 CLAUDE.md 记忆体系搭建——根级全局上下文(~200 token)+ 子目录作用域上下文(~250 token/个)+ .memory 决策/模式/收件箱层，并配上下文路由与省 token 仪表盘；不适用于跨会话向量记忆/RAG 检索(转 agent-memory-systems)或单文件小项目。触发词
