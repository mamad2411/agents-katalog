# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/g/github-api-push-workaround/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: git 推 GitHub/Gitee/AtomGit 的根因化排查与推送模板：401=凭据问题（helper 链残留死旧 PAT）、超时/挂死=通道问题（代理掐 git 传输，须 no_proxy 直连）、大面积 401=取值前缀坑（--raw 取裸值）。含直连推送模板（令牌走环境变量）、Git Data API 兜底（blob→tree→commit→ref）、Gitee 私有转公开、AtomG
