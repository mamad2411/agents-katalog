# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/s/safe-git-push/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 从 agent 工作区安全推送文件到 GitHub。父级 git 仓库场景下隔离 init,防止敏感配置文件、构建产物目录、其他无关项目子目录被误推。触发:用户说「上传到 GitHub」「推到 GitHub」「创建 GitHub 仓库」「备份项目到 GitHub」,或 OpenClaw 沙箱内 git push 超时需走 Contents API fallback。
