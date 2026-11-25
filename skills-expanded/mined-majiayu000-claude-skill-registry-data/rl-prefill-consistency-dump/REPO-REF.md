# Repo Ref
- source: https://github.com/majiayu000/claude-skill-registry-data (path: development/rl-prefill-consistency-dump/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: 训推一致性(prefill)采集侧:为训练/推理两侧采集可比的 prefill dump(输入对齐 PROMPTS_ONLY → 参数对齐校验(dump 前前置:校验两侧 config 超参/结构/权重,不一致输出参数不一致点并对齐)→ msprobe 接入采集 → 采集验证 → 恢复代码)。按用户需求判断用法:① 仅采集 dump——用户只要 dump 数据,走采集主流程(0→7→9),直接产出
