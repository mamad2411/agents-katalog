---
name: DESeq2
description: R DESeq2 package for RNA-seq analysis. Use for differential expression analysis with negative binomial models.
---

# DESeq2

Differential expression analysis.

## Basic Workflow

```r
library(DESeq2)

# Create DESeq object
dds <- DESeqDataSetFromMatrix(
  countData = counts,
  colData = sample_info,
  design = ~ condition
)

# Filter low counts
keep <- rowSums(counts(dds)) >= 10
dds <- dds[keep, ]

# Run DESeq
dds <- DESeq(dds)

# Get results
res <- results(dds)
res <- results(dds, contrast = c("condition", "treated", "control"))
```

## Input Data

```r
# From matrix
dds <- DESeqDataSetFromMatrix(
  countData = count_matrix,
  colData = sample_info,
  design = ~ condition
)

# From tximport (salmon/kallisto)
dds <- DESeqDataSetFromTximport(
  txi = txi,
  colData = sample_info,
  design = ~ condition
)

# From HTSeq
dds <- DESeqDataSetFromHTSeqCount(
  sampleTable = sample_table,
  directory = "htseq_counts/",
  design = ~ condition
)
```

## Design Formulas

```r
# Single factor
design = ~ condition

# Two factors
design = ~ batch + condition

# Interaction
design = ~ genotype + treatment + genotype:treatment

# Change design
design(dds) <- ~ new_design
```

## Results

```r
# Basic results
res <- results(dds)

# With contrast
res <- results(dds, contrast = c("condition", "treated", "control"))

# With alpha
res <- results(dds, alpha = 0.05)

# LFC threshold
res <- results(dds, lfcThreshold = 1)

# Shrinkage
res <- lfcShrink(dds, coef = "condition_treated_vs_control", type = "apeglm")

# Order by p-value
res <- res[order(res$padj), ]

# Significant genes
sig <- res[which(res$padj < 0.05), ]
sig_up <- res[which(res$padj < 0.05 & res$log2FoldChange > 1), ]
sig_down <- res[which(res$padj < 0.05 & res$log2FoldChange < -1), ]
```

## Normalization

```r
# Size factors
dds <- estimateSizeFactors(dds)
sizeFactors(dds)

# Normalized counts
counts(dds, normalized = TRUE)

# VST (variance stabilizing transformation)
vsd <- vst(dds)
assay(vsd)

# rlog transformation
rld <- rlog(dds)
assay(rld)
```

## Visualization

```r
# MA plot
plotMA(res)

# Dispersion
plotDispEsts(dds)

# PCA
plotPCA(vsd, intgroup = "condition")

# Heatmap of top genes
library(pheatmap)
top_genes <- head(order(res$padj), 50)
pheatmap(assay(vsd)[top_genes, ],
  scale = "row",
  annotation_col = as.data.frame(colData(dds)[, "condition"])
)

# Volcano plot
library(EnhancedVolcano)
EnhancedVolcano(res,
  lab = rownames(res),
  x = "log2FoldChange",
  y = "pvalue"
)

# Sample distances
sampleDists <- dist(t(assay(vsd)))
pheatmap(as.matrix(sampleDists))
```

## Export

```r
# To data frame
res_df <- as.data.frame(res)

# Add gene names
res_df$gene <- rownames(res_df)

# Write results
write.csv(res_df, "deseq2_results.csv", row.names = FALSE)
```
