# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-one-step-beh1nd-skillbank/findscripter-everything-skills-harmony-batch-correction-09-v/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 当需要整合来自不同样本/供体/测序批次的单细胞数据并消除技术性批次效应时使用；在 PCA 之后、UMAP 之前对嵌入做 Harmony 校正，产出 X_pca_harmony 校正嵌入及下游邻接图/UMAP/Leiden 聚类，不修改原始计数矩阵；不适用于需要概率式 VAE 校正(scVI)、纯图整合(BBKNN)或锚点式整合(Seurat CCA)的场景；触发词：批次校正、batch corre
