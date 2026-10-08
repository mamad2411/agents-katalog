---
name: r-bio
description: R bioinformatics packages. Use for genomic data analysis, RNA-seq, phylogenetics, and Bioconductor workflows.
---

# R Bioinformatics Skill

## Sub-skills

| Sub-skill | Description |
|-----------|-------------|
| [r-bio-genomics](r-bio-genomics/SKILL.md) | GenomicRanges, Biostrings, annotation |
| [r-bio-rnaseq](r-bio-rnaseq/SKILL.md) | DESeq2, edgeR, differential expression |
| [r-bio-phylo](r-bio-phylo/SKILL.md) | ape, ggtree, phylogenetics |

Bioinformatics and biostatistics in R.

## Core Packages

| Package | Description |
|---------|-------------|
| **Bioconductor** ★ | Genomic data analysis platform |
| **GenomicRanges** | Genomic intervals |
| **Biostrings** | DNA/RNA/protein sequences |
| **SummarizedExperiment** | Assay data container |

## Genetics & Phylogenetics

| Package | Description |
|---------|-------------|
| **genetics** | Genetic data handling |
| **gap** | Genetic data analysis |
| **ape** | Phylogenetics and evolution |
| **ggtree** | Phylogenetic tree visualization |

## Mixed Effects (Biostatistics)

| Package | Description |
|---------|-------------|
| **lme4** ★ | Mixed-effects models |
| **nlme** | Mixed-effects with custom covariance |
| **glmmTMB** | Generalized mixed-effects |

## Visualization

| Package | Description |
|---------|-------------|
| **pheatmap** | Pretty heatmaps |
| **ComplexHeatmap** | Advanced heatmaps |
| **EnhancedVolcano** | Volcano plots |

## Quick Examples

```r
# Install Bioconductor
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install()

# Install packages
BiocManager::install(c("DESeq2", "edgeR", "GenomicRanges"))

# GenomicRanges
library(GenomicRanges)
gr <- GRanges(
  seqnames = c("chr1", "chr1", "chr2"),
  ranges = IRanges(start = c(100, 200, 150), width = 50),
  strand = c("+", "-", "+"),
  score = c(1.5, 2.0, 3.0)
)
findOverlaps(gr1, gr2)
subsetByOverlaps(gr1, gr2)

# RNA-seq with DESeq2
library(DESeq2)
dds <- DESeqDataSetFromMatrix(
  countData = counts,
  colData = sample_info,
  design = ~ condition
)
dds <- DESeq(dds)
res <- results(dds, contrast = c("condition", "treated", "control"))
sig <- res[which(res$padj < 0.05), ]

# Volcano plot
library(EnhancedVolcano)
EnhancedVolcano(res,
  lab = rownames(res),
  x = 'log2FoldChange',
  y = 'pvalue',
  pCutoff = 0.05,
  FCcutoff = 1
)

# Heatmap
library(pheatmap)
pheatmap(mat,
  scale = "row",
  clustering_distance_rows = "correlation",
  annotation_col = annotation
)

# Phylogenetic analysis
library(ape)
tree <- read.tree("tree.nwk")
plot(tree)

# Gene annotation
library(org.Hs.eg.db)
mapIds(org.Hs.eg.db,
  keys = gene_ids,
  column = "SYMBOL",
  keytype = "ENSEMBL"
)
```

## Common Workflows

### RNA-seq Analysis
```r
# 1. Load counts
counts <- read.csv("counts.csv", row.names = 1)
coldata <- read.csv("samples.csv", row.names = 1)

# 2. Create DESeq object
dds <- DESeqDataSetFromMatrix(counts, coldata, ~ condition)

# 3. Filter low counts
keep <- rowSums(counts(dds)) >= 10
dds <- dds[keep,]

# 4. Run DESeq
dds <- DESeq(dds)

# 5. Get results
res <- results(dds, alpha = 0.05)
resOrdered <- res[order(res$padj),]

# 6. Visualize
plotMA(res)
plotPCA(vst(dds), intgroup = "condition")
```

### Gene Set Enrichment
```r
library(clusterProfiler)
library(org.Hs.eg.db)

# GO enrichment
ego <- enrichGO(
  gene = sig_genes,
  OrgDb = org.Hs.eg.db,
  keyType = "ENSEMBL",
  ont = "BP"
)
dotplot(ego)

# KEGG enrichment
ekegg <- enrichKEGG(
  gene = entrez_ids,
  organism = "hsa"
)
```

## Resources

- Bioconductor: https://www.bioconductor.org/
- DESeq2: https://bioconductor.org/packages/DESeq2/
- edgeR: https://bioconductor.org/packages/edgeR/
- GenomicRanges: https://bioconductor.org/packages/GenomicRanges/
