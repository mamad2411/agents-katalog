# Repo Ref
- source: https://github.com/po-et/workbuddy-skills (path: skills/git-branch-cleanup/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: git 分支清理、删除已合并分支、找出长期不动的陈旧分支、远端已删除但本地还在的分支、分支太多难管理、仓库分支治理。当用户说「帮我清理一下本地分支」「哪些分支已经合并可以删了」「远端有一堆没人动的分支」「生成一个删分支的脚本我看看再执行」时使用。附纯标准库脚本 scripts/branch_cleanup.py：只读分析，自动识别基线分支，把本地（可选远端）分支分成可删除（已合并/无独有提交）、需
