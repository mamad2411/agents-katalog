# Repo Ref
- source: https://github.com/othmanadi/planning-with-files (path: skills/i18n/planning-with-files-zh/SKILL.md, branch: master)
- mined: 2026-09-20
- desc: 用于多步骤 AI 代理工作的持久化文件规划系统。将 task_plan.md、findings.md 和 progress.md 保存在磁盘上，生命周期钩子会注入选定的项目规划上下文。自动恢复只读取项目规划文件。只有显式运行 session-catchup.py --metadata 才会检查本机同项目的会话元数据；--replay 可输出有长度限制且由 nonce 框定的同项目摘录。可选门禁仅在
