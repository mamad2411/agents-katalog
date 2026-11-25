# Repo Ref
- source: https://github.com/ccoalm/ccl-skills (path: skills/worktree-isolation/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 开工前先在独立 git worktree 里再改代码——**绝不在 main（主检出/main 分支）上开发**，任何迭代/功能/哪怕一行修改都先建分支+worktree（并发只是让这条更刚性，单人单线同样适用）；worktree 集成回目标分支后立即清理 worktree+本地分支+远端分支（让位见收尾节）。Never develop on the main checkout/branch — 
