# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-one-step-beh1nd-skillbank/findscripter-everything-skills-gatk-variant-calling-09-verti/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 当需要从 WGS/WES 的 BWA-MEM2 比对、去重、BQSR 后 BAM 检测种系 SNP/indel 并对多样本队列联合分型时使用；用 GATK4 最佳实践流程跑 BQSR→HaplotypeCaller(GVCF)→GenomicsDBImport→GenotypeGVCFs→VQSR/硬过滤，产出每样本 GVCF 与过滤后的多样本 VCF；不适用于体细胞/肿瘤变异（用 Mutect2
