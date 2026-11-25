# Repo Ref
- source: https://github.com/stargazed-dreamer/localagent-public (path: .agents/skills/dev/log-driven-defect-triage/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 用户贴来一段日志/报错（含 traceback、行号、或"明明报错了为什么还说一切正常"这类矛盾）时，把日志还原成可复现的证据、定位根因、并顺着"那句总结到底在测哪个轴"挖出被掩盖的故障。也覆盖**没有日志**的情形：用户只说"XX 不成功""指定目录没用""这两个不能一起用了吗"——此时靠一次跑完全部输入组合 + 找两套判据的不一致来定位。还覆盖**只有性能症状**的情形（"这个动作卡我一会""
