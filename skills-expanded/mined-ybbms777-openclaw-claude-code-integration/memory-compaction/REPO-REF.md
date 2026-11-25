# Repo Ref
- source: https://github.com/ybbms777/openclaw-claude-code-integration (path: skills/memory-compaction/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: LanceDB 记忆压缩 cron skill。每周日凌晨 3:00 自动执行记忆整理：(1) 备份当前 LanceDB 到 backups/YYYY-MM-DD/（保留最近4份）；(2) 删除 importance &lt; 0.3 且 14 天未访问的记忆；(3) 用 SiliconFlow bge-m3 向量相似度 ≥ 0.85 的碎片合并成一条，保留最高 importance 的 L0 摘
