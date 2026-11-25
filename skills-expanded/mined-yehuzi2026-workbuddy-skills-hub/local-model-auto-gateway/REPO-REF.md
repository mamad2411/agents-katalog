# Repo Ref
- source: https://github.com/yehuzi2026/workbuddy-skills-hub (path: categories/08-local-llm/local-model-auto-gateway/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 本机 Ollama 多模型「自动选模型 + Laya 决策兜底」统一网关（AUTO 入口）。当用户要「调用 AUTO / 自动挑最合适的本地模型 / 本地大模型统一入口 / 工单自动分类不手动指定模型」时使用。核心原则：轻量模型优先，只有大文本/多诉求/需推理时才动用 deepseek-r1:7b；图片走视觉模型；模型挂了逐级降级，最终 Laya 兜底不崩。
