# Repo Ref
- source: https://github.com/DENGYUFAN0/guashuai-junshi (path: adapters/claude-code/skills/guashuai/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 挂帅模式（orchestrator）：主会话模型（STRONG）挂帅坐镇，把任务拆成边界清晰的子任务，点将派给子代理模型（CHEAP，worker 子代理）并行执行，帅只做拆解、派兵、验收、整合，省下执行环节的贵模型额度。适合多文件批量修改、多线并行的大任务。MANUAL-INVOKE ONLY — 平时绝不自动触发；即使用户说"任务很大""帮我并行做""拆一下任务"也不激活（就算 CLAUDE.
