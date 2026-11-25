# Repo Ref
- source: https://github.com/findscripter/everything-skills (path: 09-verticals/gatk-variant-calling/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当需要从 WGS/WES 的 BWA-MEM2 比对、去重、BQSR 后 BAM 检测种系 SNP/indel 并对多样本队列联合分型时使用；用 GATK4 最佳实践流程跑 BQSR→HaplotypeCaller(GVCF)→GenomicsDBImport→GenotypeGVCFs→VQSR/硬过滤，产出每样本 GVCF 与过滤后的多样本 VCF；不适用于体细胞/肿瘤变异（用 Mutect2
