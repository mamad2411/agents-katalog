# Repo Ref
- source: https://github.com/majiayu000/claude-skill-registry-data (path: other/msmodelslim-model-dequant-ascend-msagent/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: 为 msModelSlim 适配流程注入反量化能力。先识别模型权重是否可反量化，再实现反量化脚本并接入 model_adapter。当前仅覆盖 FP8 的 per-block 与 per-channel 两类；若格式不确定或无公开反量化规则，要求用户提供反量化脚本或浮点权重。
