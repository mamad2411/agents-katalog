# Repo Ref
- source: https://github.com/stargazed-dreamer/localagent-public (path: .agents/skills/daily/wb-history-recall/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 从本机 WorkBuddy 会话库（workbuddy.db + projects/*.jsonl）还原历史对话，找回「用户当时到底怎么说的 / 这个决定是哪来的 / 是不是我说过」。默认同时抽用户原话与 agent 回复，⛔ 禁止只看用户一侧。除对话正文外还能取：会话状态与最后活动时间（list）、尾部若干条（dump --tail）、被 Edit/Write 写过的文件清单（dump --fi
