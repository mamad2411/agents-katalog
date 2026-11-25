# Repo Ref
- source: https://github.com/findscripter/everything-skills (path: 04-ai/autoresearch-optimization-agent/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当你有一个目标文件、一条会输出可量化指标的评估命令、且代码在 git 仓库中，想让智能体长时间自动优化（更快/更小/质量更高）时使用；做的事：单变量改文件→提交→跑固定评估→改进则保留、变差则 git reset 回退→循环累积并记录到 results.tsv；不适用于无法量化、缺评估命令或不在 git 下的任务，也不要边改评估器边比对。触发词：优化、实验循环、autoresearch
