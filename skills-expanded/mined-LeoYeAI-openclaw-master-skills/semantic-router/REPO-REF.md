# Repo Ref
- source: https://github.com/LeoYeAI/openclaw-master-skills (path: skills/semantic-router/SKILL.md, branch: main)
- mined: 2026-10-14
- desc: 让 AI 代理根据对话内容自动选择最合适的模型。层2（多词非连续命中）+ 层1（单词兜底）并行决定模型池；层3（embedding）永远独立运行决定会话切换。B+ 连续漂移计数器（第3次警告，第4次强制 C-auto）。soft_keywords 泛用词降权机制。四池架构（高速/智能/人文/代理），五分支路由，全自动 Fallback 回路。
