# Repo Ref
- source: https://github.com/i-stack/ai-coding-kit (path: skills-engineering/auto-code-review/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 用户显式触发的跨模型代码审查工作流。仅当用户明确说 `/auto-review`、`使用 auto-code-review`、`启动跨模型代码审查`，或明确要求“审查并修复”时使用；普通代码生成、修改完成或含糊的“看看代码”不自动触发。默认只读审查，只有用户明确要求 `--fix` 或“审查并修复”才允许主 agent 修改代码。
