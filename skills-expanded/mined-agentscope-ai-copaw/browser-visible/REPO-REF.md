# Repo Ref
- source: https://github.com/agentscope-ai/copaw (path: src/qwenpaw/agents/tools/deprecated_browser/skills/browser_visible-zh/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当用户需要控制 browser 的浏览器启动方式时，使用本 skill。browser 默认由 Playwright 直接管理、不开放调试端口（需让其他本地工具附加时显式传 `cdp_port`）；`headed` 控制是否显示窗口，`private_mode` 保留用于兼容、不再改变默认行为，`browser_args` 传入额外的 Chromium 启动参数，`executable_path`
