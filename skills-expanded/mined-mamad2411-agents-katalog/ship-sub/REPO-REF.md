# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/ghscan-blackplume233-Actant/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 子分支交付技能。用于用户要求“ship sub”、“子分支提 PR 再由主分支合并”、“feature branch ship”、“先创建 PR 再 handle-pr 交付”等场景。流程是在当前非主分支执行 finish-work/ship 级检查，提交并推送子分支，创建或复用 PR，然后切回主分支按 pr-handler 流程完成 handle-pr 交付。
