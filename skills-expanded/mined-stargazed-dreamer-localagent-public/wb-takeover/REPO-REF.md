# Repo Ref
- source: https://github.com/stargazed-dreamer/localagent-public (path: .agents/skills/daily/wb-takeover/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 限流换号后接手被打断的 WorkBuddy 会话。扫会话库分三段列出候选：被系统打断的（429 限流/报错）、正常收尾但末句把球踢回给你的（「等你上传」「你说一声」这类「看着结束了其实还有话要说」）、其余已收尾的；带连续序号汇总给用户，用户点号后逐场导出独立接手包（HANDOFF 事实头 + 全量对话 + 原 jsonl + 派发提示词），再给出可粘贴的派发提示词，让新 agent 读完就接着做。
