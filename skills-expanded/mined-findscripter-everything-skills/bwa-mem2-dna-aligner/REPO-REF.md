# Repo Ref
- source: https://github.com/findscripter/everything-skills (path: 09-verticals/bwa-mem2-dna-aligner/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当需要把 Illumina 短读 DNA（50–250 bp，WGS/WES/ChIP-seq/ATAC-seq）比对到参考基因组、生成带 @RG 读组头的排序 BAM 供 GATK/Picard 变异检测或 peak calling 时使用；用 bwa-mem2 index 建索引、bwa-mem2 mem 比对并管道接 samtools sort/index、再 markdup 去重，产出 s
