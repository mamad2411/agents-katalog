# Repo Ref
- source: https://github.com/stargazed-dreamer/localagent-public (path: .agents/skills/dev/parcae-remote-sync/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Parcae 主仓库与 origin/master 分叉时，安全完成"和远端合并"的完整流程。两种场景：① 落后且工作区脏（有 WIP，含 CHANGELOG.md）→ 备份/stash/快进/pop/消解冲突；② 领先且工作区干净（改动已提交）→ merge/消解 CHANGELOG 冲突/提交 merge。两种场景都要判"远端那笔是否发版"来决定冲突消解规则，并全程保持 CHANGELOG 的
