# Repo Ref
- source: https://github.com/stargazed-dreamer/localagent-public (path: .agents/skills/daily/cross-machine-delivery-bundle/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 把一个工作区的文件从 A 机（真机）打包交付到 B 机（VM/另一台机），产出「压缩包 + 完整性清单 + 交付说明 + 落地脚本」四件套。核心是先判"自己在哪台机"（盘符判据），再把报告里出现的每个路径当断言逐条验，最后按"项目 temp/ 内 staging + sha256 清单 + 7z -tzip"打包。当用户说"把缺的东西打包给我 / 帮我打包传进去 / 跨机交接 / 虚拟机缺的补一下
