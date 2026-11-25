# Repo Ref
- source: https://github.com/ryanzhao1011/workframe (path: plugins/core/skills/onboard/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: workframe 一次性可选配置引导。读取 recommended-env.json，逐项询问是否启用（默认 skip），用户授权后写 settings.json 并标记 onboarded。由用户显式调用；未 onboarded 的项目由 SessionStart hook 提示一行
