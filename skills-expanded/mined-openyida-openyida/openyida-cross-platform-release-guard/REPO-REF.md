# Repo Ref
- source: https://github.com/openyida/openyida (path: .agents/skills/openyida-cross-platform-release-guard/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: OpenYida 跨端发布风险守卫。当改动涉及浏览器/URL 拉起（openyida login、resolveBrowserLauncher、openBrowser、spawn 打开浏览器），或用户明确要求检查 Windows/Linux 发布风险时使用。用于静态扫描并拦截「cmd /c start 截断 URL」「open -n 假装开新窗口」等跨端问题；普通版本 tag 发布请使用 open
