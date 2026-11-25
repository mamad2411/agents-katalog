# Repo Ref
- source: https://github.com/zhaoxinghua09-cell/agent-skills (path: skills/agent-loop-guard/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当用户说『agent卡死了』『一直在重复同样动作』『跑飞了烧光token』『怎么给agent设步数上限』，或 agent 出现无限循环/重复调用/原地打转时使用。把 agent 的运行当『受控进程』：监控步数上限·重复动作·状态无进展，触发即熔断并产出诊断。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：agent卡死、无限循环、重复动作、跑飞、步数上限、loop guard、token烧光
