# Repo Ref
- source: https://github.com/wgpsec/AboutSecurity (path: skills/tool/githacker-git-leak/SKILL.md, branch: master)
- mined: 2026-10-14
- desc: 使用 GitHacker 利用 .git 目录泄露漏洞恢复目标源码。GitHacker 是多线程 .git 泄露利用工具，相比 git-dumper/GitHack 能恢复更完整的内容——包括 stash、所有分支、标签、reflog。即使目标禁用了目录列表（403），也能通过暴力枚举恢复分支和标签。当目标 /.git/HEAD 或 /.git/config 返回 200、目录列表中发现 .git
