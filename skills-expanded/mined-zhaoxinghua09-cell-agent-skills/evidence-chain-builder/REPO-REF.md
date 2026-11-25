# Repo Ref
- source: https://github.com/zhaoxinghua09-cell/agent-skills (path: skills/evidence-chain-builder/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当用户要『验证 AI 论断 / 防幻觉 / 给结论找证据 / 判断信源可信度』时用。把论断拆成可验证证据链：每条证据标来源类型(official/paper/data/internal/assertion)、是否可独立验证、可信度，输出『证成度』与未支撑论断清单。对齐 EIFP 不编造原教旨——本工具不判定论断真假，只评估证据质量；缺可验证证据的论断明确标『勿作结论』。这是 LGD-II 有证的落
