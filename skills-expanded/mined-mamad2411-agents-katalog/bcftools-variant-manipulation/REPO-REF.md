# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-one-step-beh1nd-skillbank/findscripter-everything-skills-bcftools-variant-manipulation/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 当变异检测后需要对 VCF/BCF 做质控过滤、多样本合并、规范化、rsID/基因注释、基因型提取与统计时使用；用 bcftools 流式管线跑 norm→filter→annotate→query/stats/merge/concat，产出过滤注释后的 VCF.gz、基因型矩阵或 QC 报告；不适用于变异检测本身（种系用 gatk-variant-calling、bcftools call 仅做
