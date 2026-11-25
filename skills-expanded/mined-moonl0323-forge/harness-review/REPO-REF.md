# Repo Ref
- source: https://github.com/moonl0323/forge (path: skills/harness-review/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 双 Agent 对抗 Review + GAN 启发式评分。基于 Anthropic Labs 的 Generator/Evaluator 分离原则：Generator（内部视角，有完整上下文）负责 spec compliance；Evaluator（对抗视角，只有 diff+需求）负责独立评价。两者都输出结构化评分，不只是 MUST FIX/PASS。参考：harness-design-long
