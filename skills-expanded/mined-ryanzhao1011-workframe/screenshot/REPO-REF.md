# Repo Ref
- source: https://github.com/ryanzhao1011/workframe (path: plugins/core/skills/screenshot/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 通用 HTML / 本地 URL 截图工具：读 JSON 配置，逐项打开 → setup → 等待 → 截图 → 输出 PNG 到 tmp/screenshots/<task-id>/。只负责出图——不上传任何平台、不写 spec、不实现业务交互；调用方通过 `setup_js` 提供 raw JS hook 控制业务逻辑。用于需要把本地 HTML 原型或 Mermaid 图转成 PNG 归档、嵌
