# Repo Ref
- source: https://github.com/zuoyebang/aiweave (path: templates/skills/io-review/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 审计代码的 IO 铁律。扫描新增/修改的代码，对照 docs/architecture/io_contract.md §2 三条 IO 铁律（批量优先 / 禁止 N+1 / 禁止独立串行编排）与 §3-§5 聚合并行约束，结合 docs/architecture/ai_dev_guide.md §10.2 grep 锚 rule-id 索引（R-IO-*）机械执行。命中标 🟡 待复核（信号级），最
