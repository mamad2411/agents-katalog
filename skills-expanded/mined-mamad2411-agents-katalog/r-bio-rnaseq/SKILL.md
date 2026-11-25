---
name: r-bio-rnaseq
description: R RNA-seq analysis with DESeq2, edgeR. Use for differential expression and gene set enrichment.
---

# R RNA-seq Analysis

Differential expression analysis.

## DESeq2

```r
library(DESeq2)

# Create object
dds <- DESeqDataSetFromMatrix(
  countData = counts,
  colData = sample_info,
  design = ~ condition
)

# Filter low counts
keep <- rowSums(counts(dds)) >= 10
dds <- dds[keep,]

# Run DESeq
dds <- DESeq(dds)

# Results
res <- results(dds, contrast = c("condition", "treated", "control"))
res <- results(dds, alpha = 0.05)
summary(res)

# Significant genes
sig <- res[which(res$padj < 0.05), ]
sig_up <- sig[sig$log2FoldChange > 1, ]
sig_down <- sig[sig$log2FoldChange < -1, ]

# Visualization
plotMA(res)
plotPCA(vst(dds), intgroup = "condition")
```

## edgeR

```r
library(edgeR)

# Create object
y <- DGEList(counts = counts, group = group)

# Filter
keep <- filterByExpr(y)
y <- y[keep, , keep.lib.sizes = FALSE]

# Normalize
y <- calcNormFactors(y)

# Dispersion
y <- estimateDisp(y)

# Test
et <- exactTest(y)
topTags(et)

# GLM approach
design <- model.matrix(~ group)
fit <- glmQLFit(y, design)
qlf <- glmQLFTest(fit, coef = 2)
topTags(qlf)
```

## Gene Set Enrichment

```r
library(clusterProfiler)

# GO enrichment
ego <- enrichGO(gene = sig_genes, OrgDb = org.Hs.eg.db, keyType = "ENSEMBL", ont = "BP")
dotplot(ego)

# KEGG
ekegg <- enrichKEGG(gene = entrez_ids, organism = "hsa")

# GSEA
gse <- gseGO(geneList = ranked_genes, OrgDb = org.Hs.eg.db, ont = "BP")
```
