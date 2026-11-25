---
name: bioinformatics
description: Gateway to 400+ genomics and computational biology skills.
version: 1.0.0
author: Teknium (teknium1), Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [bioinformatics, genomics, sequencing, biology, research, science]
    category: research
---

# 生物信息学技能门户

当被问及生物信息学、基因组学、测序技术、变异调用、基因表达分析、单细胞分析、蛋白质结构研究、药物基因组学、宏基因组学、系统发育学或任何计算生物学相关问题时，可使用此技能。

该技能可作为两个开源生物信息学技能库的入口。它不会将数百个领域专用技能打包在一起，而是对这些技能进行索引，按需调用所需功能。

## 资源来源

◆ **bioSkills** — 385个参考技能（代码模板、参数指南、决策树）
  仓库地址：https://github.com/GPTomics/bioSkills
  格式：每个主题对应一个SKILL.md文件，内含代码示例，支持Python/R/CLI语言。

◆ **ClawBio** — 33个可直接运行的分析流程技能（可执行脚本、可复现分析包）
  仓库地址：https://github.com/ClawBio/ClawBio
  格式：包含演示功能的Python脚本。每次分析后会生成report.md、commands.sh和环境配置文件environment.yml。

## 如何获取并使用技能

1. 从下方索引中确定所属领域及具体技能名称。
2. 克隆相应的仓库（建议使用浅克隆以节省时间）：
   ```bash
   # bioSkills (reference material)
   git clone --depth 1 https://github.com/GPTomics/bioSkills.git /tmp/bioSkills

   # ClawBio (runnable pipelines)
   git clone --depth 1 https://github.com/ClawBio/ClawBio.git /tmp/ClawBio
   ```
3. 查阅相应的特定技能说明：
   ```bash
   # bioSkills — each skill is at: <category>/<skill-name>/SKILL.md
   cat /tmp/bioSkills/variant-calling/gatk-variant-calling/SKILL.md

   # ClawBio — each skill is at: skills/<skill-name>/
   cat /tmp/ClawBio/skills/pharmgx-reporter/README.md
   ```
4. 请以获取到的技能文档作为参考资料。这些并非采用Hermes格式编写的技能，应将其视为特定领域的专家指南。它们包含了正确的参数、恰当的工具标志以及经过验证的处理流程。

## 按领域分类的技能索引

### 序列处理基础
bioSkills：
  sequence-io/ — 序列读取、序列写入、格式转换、批量处理、压缩文件处理、FastQ质量检测、序列筛选、双端FastQ处理、序列统计分析
  sequence-manipulation/ — 序列对象操作、反向互补序列生成、转录与翻译过程、模式搜索、密码子使用频率分析、序列属性分析、序列切片处理
ClawBio：
  seq-wrangler — 序列质量检测、比对以及BAM文件处理（整合了FastQC、BWA、SAMtools等工具）

### 读取质量检测与比对
bioSkills：
  read-qc/ — 质量报告生成、fastp工作流、接头去除、质量过滤、UMI序列处理、污染检测、RNA-seq质量检测
  read-alignment/ — BWA比对、STAR比对、HISAT2比对、Bowtie2比对
  alignment-files/ — SAM与BAM文件基础操作、比对结果排序、比对结果过滤、BAM文件统计分析、重复数据处理、重叠区域生成

### 变异调用与注释
bioSkills：
  variant-calling/ — gatk-variant-calling、deepvariant、variant-calling（bcftools）、joint-calling、structural-variant-calling、过滤最佳实践、变异注释、变异标准化、vcf基础知识、vcf数据操作、vcf统计分析、共识序列、临床解读
ClawBio：
  vcf-annotator — 结合VEP、ClinVar及gnomAD注释，并考虑祖先背景信息
  variant-annotation — 变异注释处理流程

### 差异表达分析（批量RNA测序）
bioSkills：
  differential-expression/ — deseq2基础应用、edger基础应用、批次校正、差异分析结果处理、结果可视化、时间序列差异分析
  rna-quantification/ — 无需比对的定量分析方法（Salmon/kallisto）、featurecounts计数、tximport工作流程、计数矩阵质量控制
  expression-matrix/ — 数据导入、基因标识映射、元数据整合、稀疏矩阵处理
ClawBio：
  rnaseq-de — 包含质量控制、标准化及可视化功能的完整差异表达分析流程
  diff-visualizer — 为差异表达分析结果提供丰富的可视化展示与报告功能

### 单细胞RNA测序
bioSkills：
  single-cell/ — 数据预处理、聚类分析、批次整合、细胞注释、细胞间通讯分析、双细胞检测、标记物注释、细胞轨迹推断、多模态数据整合、Perturb-Seq分析、scatac分析、细胞谱系追踪、代谢物通讯分析、数据读写
ClawBio：
  scrna-orchestrator — 完整的Scanpy分析流程（包括质量控制、聚类、标记物识别及注释）
  scrna-embedding — 基于scVI的潜在特征嵌入与批次整合方法

### 空间转录组学
相关生物技能：
  spatial-transcriptomics/ — 空间数据输入输出、空间预处理、空间域划分、空间反卷积、空间信号传递、空间邻域分析、空间统计学、空间可视化、空间多组学、空间蛋白质组学、图像分析

### 表观基因组学
相关生物技能：
  chip-seq/ — 峰值检测、差异结合分析、基序分析、峰值注释、芯片测序质量控制、芯片测序结果可视化、超级增强子研究
  atac-seq/ — ATAC峰值检测、ATAC测序质量控制、染色质可及性差异分析、染色质足迹分析、基序偏差检测、核小体定位分析
  methylation-analysis/ — Bismark对齐工具、甲基化水平检测、DNA甲基化区域识别、MethylKit分析工具
  hi-c-analysis/ — 高分辨率染色体构象捕获数据输入输出、TAD结构识别、环结构检测、细胞区室分析、接触对分析、矩阵运算、高分辨率染色质构象捕获结果可视化、差异分析
ClawBio工具：
  methylation-clock — 表观遗传年龄估算

### 药物基因组学与临床应用
bioSkills 相关功能：
  clinical-databases/ — clinvar 数据查询、gnomad 基因频率查询、dbsnp 变异查询、药物基因组学分析、多基因风险评分计算、HLA 分型、变异优先级排序、体细胞特征分析、肿瘤突变负荷评估、myvariant 变异查询
ClawBio 相关功能：
  pharmgx-reporter — 基于 23andMe/AncestryDNA 数据生成的 PGx 报告（涵盖 12 个基因、31 个 SNP 以及 51 种药物）
  drug-photo — 药物照片输入 → 通过图像识别技术生成个性化 PGx 用药剂量卡
  clinpgx — 提供基因-药物数据及 CPIC 指南相关的 ClinPGx API 接口
  gwas-lookup — 跨 9 个基因组数据库进行变异查询的功能
  gwas-prs — 基于消费者基因数据计算多基因风险评分
  nutrigx_advisor — 基于消费者基因数据提供个性化营养建议

### 种群遗传学与全基因组关联分析
bioSkills 相关功能：
  population-genetics/ — 关联性检测（PLINK GWAS）、plink 基础操作、群体结构分析、连锁不平衡分析、scikit-allel 分析方法、选择统计分析
  causal-genomics/ — 孟德尔随机化分析、精细定位技术、共定位分析、中介效应分析、多效性检测
  phasing-imputation/ — 单倍型分型、基因型填补、填补质量控制、参考基因组面板构建
ClawBio 相关功能：
  claw-ancestry-pca — 基于 SGDP 参考基因组面板进行祖先来源的 PCA 分析

### 元基因组学与微生物组
bioSkills：
  metagenomics/ — Kraken分类、Metaphlan谱型分析、丰度估算、功能特征分析、耐药性检测、菌株追踪、元基因组可视化
  microbiome/ — 扩增子处理、多样性分析、差异丰度分析、分类学鉴定、功能预测、Qiime2工作流程

ClawBio：
  claw-metagenomics — Shotgun技术下的元基因组谱型分析（包括分类学分析、耐药基因组分析及功能通路分析）

### 基因组组装与注释
bioSkills：
  genome-assembly/ — HIFI组装、长读长组装、短读长组装、元基因组组装、组装优化、质量检测、支架构建、污染检测
  genome-annotation/ — 真核生物基因预测、原核生物注释、功能注释、非编码RNA注释、重复序列注释、注释迁移
  long-read-sequencing/ — 基序调用、长读长比对、长读长质量检测、Clair3变异分析、结构变异分析、Medaka组装优化、纳米孔测序甲基化分析、IsoSeq数据分析

### 结构生物学与化学生物信息学
bioSkills：
  structural-biology/ — AlphaFold预测、现代结构预测、结构数据导入导出、结构导航、结构修饰、几何分析
  chemoinformatics/ — 分子数据导入导出、分子描述符构建、相似性搜索、子结构搜索、虚拟筛选、ADMET性质预测、反应路径枚举

ClawBio：
  struct-predictor — 支持局部AlphaFold/Boltz/Chai结构预测，并可进行结果对比分析

### 蛋白组学
bioSkills：
  proteomics/ — 数据导入、肽段鉴定、蛋白质推断、定量分析、差异丰度分析、二聚体分析、蛋白质修饰分析、蛋白组学质量控制、光谱库管理
ClawBio：
  proteomics-de — 蛋白组学差异表达分析

### 通路分析与基因网络
bioSkills：
  pathway-analysis/ — GO通路富集分析、GSEA分析、KEGG通路分析、Reactome通路分析、Wikipathways通路分析、富集结果可视化
  gene-regulatory-networks/ — SCENIC调控子分析、共表达网络分析、差异网络分析、多组学基因调控网络分析、扰动模拟分析

### 免疫信息学
bioSkills：
  immunoinformatics/ — MHC结合预测、表位预测、新抗原预测、免疫原性评分、TCR表位结合分析
  tcr-bcr-analysis/ — MixCR分析、SCIRPY分析、IMMCANTATION分析、受体库可视化、VDJTools分析

### CRISPR与基因组工程
bioSkills：
  crispr-screens/ — MAGECK分析、JACKS分析、靶点筛选、筛选实验质量控制、文库设计、CRISPR编辑、碱基编辑分析、批次校正
  genome-engineering/ — gRNA设计、脱靶效应预测、HDR模板设计、碱基编辑设计、Prime编辑设计

### 工作流管理
bioSkills：
  workflow-management/ — Snakemake工作流、Nextflow流程、CWL工作流、WDL工作流
ClawBio：
  repro-enforcer — 将任意分析结果导出为可复现性数据包（包含Conda环境、Singularity镜像及校验和）
  galaxy-bridge — 访问usegalaxy.org上提供的8,000多种Galaxy工具

### 专业领域
生物技能：
  可变剪接/ — 剪接定量、差异剪接、异构体转换、生鱼片图谱分析、单细胞剪接分析、剪接质量检测
  生态基因组学/ — DNA环境宏条形码分析、景观基因组学、保护遗传学、生物多样性指标分析、群落生态学、物种界定
  流行病学基因组学/ — 病原体分型、变异体监测、病毒传播动态分析、传播途径推断、耐药性监测
  液体活检/ — ctDNA预处理、ctDNA突变检测、片段分析、肿瘤细胞占比估算、甲基化检测、长期监测
  表观转录组学/ — m6A修饰峰定位、m6A差异分析、m6A网络分析、MERIP数据预处理、修饰可视化
  代谢组学/ — XCMS数据预处理、代谢物注释、标准化质量检测、统计分析、代谢途径图谱构建、脂质组学、靶向分析、MSDIAL数据预处理
  流式细胞术/ — FCS数据处理、门控分析、补偿转换、聚类表型分析、差异分析、流式细胞术质量检测、双细胞检测、微球标准化
  系统生物学/ — 流量平衡分析、代谢网络重建、基因必需性分析、特定环境模型构建、模型优化
  RNA结构/ — RNA二级结构预测、非编码RNA搜索、结构探测

### 数据可视化与报告生成
bioSkills模块：
  data-visualization/ — ggplot2基础应用、热图聚类分析、火山图定制、Circos图表绘制、基因组浏览器轨迹展示、交互式可视化、多面板图表生成、网络结构可视化、Upset图制作、颜色调色板设计、特殊组学数据图表生成、基因组轨迹可视化
  reporting/ — Rmarkdown报告生成、Quarto报告生成、Jupyter报告生成、自动化质量控制报告生成、图表导出功能

ClawBio模块：
  profile-report — 分析特征报告生成
  data-extractor — 通过图像识别技术从科学图表中提取数值数据
  lit-synthesizer — PubMed/bioRxiv数据库检索、内容总结及引文关系图谱构建
  pubmed-summariser — 基于结构化格式的基因/疾病相关PubMed文献检索与摘要生成

### 数据库访问功能
bioSkills模块：
  database-access/ — Entrez数据库检索、数据获取、关联查询、BLAST序列搜索、本地BLAST分析、SRA数据查询、地理数据获取、Uniprot数据库访问、批量数据下载、相互作用数据库查询、序列相似性分析

ClawBio模块：
  ukb-navigator — 对UK Biobank数据库中12,000多个字段进行语义搜索
  clinical-trial-finder — 临床试验信息检索工具

### 实验设计功能
bioSkills模块：
  experimental-design/ — 实验功效分析、样本量计算、分组设计、多重检验方法应用

### 基因组学的机器学习应用
bioSkills：
  machine-learning/ — 基因组分类、生物标志物发现、生存分析、模型验证、预测结果解释、图谱构建
ClawBio：
  claw-semantic-sim — 疾病相关文献的语义相似度指数（基于PubMedBERT）
  omics-target-evidence-mapper — 整合来自不同基因组数据源的目标级证据

## 环境配置

这些技能需要生物信息学工作站支持。常见依赖项：

```bash
# Python
pip install biopython pysam cyvcf2 pybedtools pyBigWig scikit-allel anndata scanpy mygene

# R/Bioconductor
Rscript -e 'BiocManager::install(c("DESeq2","edgeR","Seurat","clusterProfiler","methylKit"))'

# CLI tools (Ubuntu/Debian)
sudo apt install samtools bcftools ncbi-blast+ minimap2 bedtools

# CLI tools (macOS)
brew install samtools bcftools blast minimap2 bedtools

# Or via Conda (recommended for reproducibility)
conda install -c bioconda samtools bcftools blast minimap2 bedtools fastp kraken2
```

## 常见问题

- 获取到的技能并非采用 Hermes SKILL.md 格式，而是采用各自特定的结构（bioSkills：代码模式手册；ClawBio：README 文件及 Python 脚本）。这类资料应视为专家参考资料使用。
- bioSkills 仅为参考指南，虽会展示正确的参数与代码模式，但并非可直接运行的流程。
- ClawBio 类技能则是可执行的——许多工具都配备了 `--demo` 参数，可直接运行。
- 这两个代码库均假定用户已安装生物信息学相关工具。在运行相应流程之前，请先检查系统是否满足前置条件。
- 对于 ClawBio，需先在克隆的代码库中执行 `pip install -r requirements.txt` 命令。
- 基因组数据文件通常体积巨大，在下载参考基因组、SRA 数据集或构建索引时，请注意磁盘空间不足的问题。
