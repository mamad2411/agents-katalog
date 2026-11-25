# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/c/claude-code-third-party-model/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 把本地 Claude Code 接到第三方端点——分两路：① 原生 Anthropic 兼容端点（DeepSeek / Kimi / GLM）直接改 ANTHROPIC_BASE_URL；② 只有 OpenAI 兼容端点的模型（Space Bunny / 各类 stealth 模型）必须加本地网关做 Anthropic→OpenAI 协议转换 —— **用自建零依赖 `ccproxy.py`**（
