# Repo Ref
- source: https://github.com/dragon-fish/config-file-versioning (path: SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 给小型本地配置文件设置自动版本备份，便于回滚被覆写/误改。当用户希望给某几个 config 文件（如 ~/.ssh/config、~/.zshrc、应用 dotfile 等）加版本史/防覆写/可一键回滚时使用。统一架构：separate-git-dir + 白名单 .gitignore + 操作系统级文件监听 + 自动 commit 脚本。一个被保护的 config 域 = 一个独立小仓库。原生支
