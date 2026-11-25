# Repo Ref
- source: https://github.com/majiayu000/claude-skill-registry-data (path: other/rl-consistency-dump-analysis/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: 通用训推一致性(prefill)的 dump 数据分析 skill。分析**已采集**的训推两侧 dump:探查 dump 结构 → 语义边界映射(不要求算子同名)→ 逐边界精确门禁比对 → 定位首差异 → ULP 量化区分舍入/逻辑级 → 追放大链 → 差异点隔离验证(打桩迭代:输出打桩指令给采集侧,等它用 msprobe `load` 覆盖边界再采后比下游,枚举所有独立差异点)→ 排除根因假设
