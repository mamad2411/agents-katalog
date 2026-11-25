# Repo Ref
- source: https://github.com/findscripter/everything-skills (path: 09-verticals/vcf-variant-filtering/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当对变异检测器原始输出的 VCF 计算 Ts/Tv、变异计数、AF 分布等汇总统计前，需要判断 VCF 是否未过滤并做质量过滤时使用；先查 FILTER 列与 QUAL 分布判定 raw/已过滤，对原始 VCF 默认 bcftools view -i 'QUAL>=30' 过滤后再 bcftools stats 算指标，产出过滤后 VCF 与可复现的质控报告；不适用于变异检测本身（用 gatk-v
