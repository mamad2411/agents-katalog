# Repo Ref
- source: https://github.com/findscripter/everything-skills (path: 09-verticals/muon-multiomics-singlecell/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当对同一批细胞的两种及以上组学（10x Multiome RNA+ATAC、CITE-seq RNA+蛋白等）做联合分析时使用；用 muon/MuData 按模态分别预处理（ATAC 走 TF-IDF/LSI、蛋白走 CLR）并构建 WNN 联合嵌入、聚类、MOFA+ 因子分析，产出联合 UMAP/聚类/跨模态 marker；不适用于单一 RNA 模态（用 scanpy）、需深度概率批次校正（用 
