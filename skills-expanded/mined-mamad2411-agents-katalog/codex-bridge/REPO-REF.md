# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/topic-yaohui325-codex-bridge-root/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 显式触发的 Claude Code → Codex CLI 桥接 skill。把对话上下文 / plan / 相关文件 / 项目约定外化为 bundle 目录，调用 codex exec 并用 response.schema.json 作结构参考 + Claude Code jq 后处理校验。适用 4 场景（v1.1 起）：plan 审阅、Codex 编码、Claude-Codex 互审最多 2 
