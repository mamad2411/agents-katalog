# Repo Ref
- source: https://github.com/onescience-ai/oneskills (path: skills/onescience-resource-fetch/SKILL.md, branch: master)
- mined: 2026-11-23
- desc: OneSkills 资源层「物化」技能（type=resource），专管数据准备：任务需要的模型权重/checkpoint 或数据集在本地不存在时，优先复用共享目录 / 本地已有副本，缺失时从共享目录 / ModelScope / HuggingFace / 官网直链四类来源里，按 references/source_selection.md 评估择一，把资源拉到本地统一缓存并返回可用的绝对路径
