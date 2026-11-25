# Repo Ref
- source: https://github.com/majiayu000/claude-skill-registry-data (path: development/quant-tuning-infer-dit-ascend-msagent/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: 在 W8A8 动态量化后，用 MindIE-SD 冒烟测试 DiT 量化权重是否可加载（可选 skill）。与 `quant-tuning-evaluate`（DiT 扩展节）的区别：本 skill 仅做"能跑通 + 权重可用"的轻量验证（4~16 条 prompt，几分钟出结果），不算分；后者产出视频集交 `quant-tuning-score-dit`（AISBench-VBench 16 维
