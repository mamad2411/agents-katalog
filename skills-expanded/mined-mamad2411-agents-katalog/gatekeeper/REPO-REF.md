# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-NeverSight-learn-skills.dev/gatekeeper/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: Gatekeeper 流水线【单一规则源 + 总控路由】。仅人工以 `/gatekeeper` 命令触发（禁止 Agent 自动使用）。先定位当前流程走到哪一步，再分派到对应子 skill 继续；若尚无流程则先发起 `/gatekeeper-init`。
