---
name: edgeR
description: R edgeR package for RNA-seq analysis. Use for differential expression with negative binomial models.
---

# edgeR Package

Differential expression analysis for RNA-seq.

## Basic Workflow

```r
library(edgeR)

# Create DGEList
dge <- DGEList(counts = count_matrix, group = group)

# Filter low counts
keep <- filterByExpr(dge)
dge <- dge[keep, , keep.lib.sizes = FALSE]

# Normalize
dge <- calcNormFactors(dge)

# Estimate dispersion
dge <- estimateDisp(dge)

# Exact test (two groups)
et <- exactTest(dge)
topTags(et)
```

## GLM Approach

```r
# Design matrix
design <- model.matrix(~0 + group)
colnames(design) <- levels(group)

# Estimate dispersion
dge <- estimateDisp(dge, design)

# Fit GLM
fit <- glmQLFit(dge, design)

# Contrast
contrast <- makeContrasts(TreatmentA - Control, levels = design)
qlf <- glmQLFTest(fit, contrast = contrast)
topTags(qlf)
```

## Results

```r
# Top genes
results <- topTags(qlf, n = Inf)$table

# Significant genes
sig <- results[results$FDR < 0.05, ]

# Volcano plot
plotMD(qlf)

# MA plot
plotSmear(qlf)
```

## Normalization

```r
# TMM (default)
dge <- calcNormFactors(dge, method = "TMM")

# Other methods
dge <- calcNormFactors(dge, method = "RLE")
dge <- calcNormFactors(dge, method = "upperquartile")

# Get normalized counts
cpm(dge)
rpkm(dge, gene.length = gene_lengths)
```

## MDS Plot

```r
plotMDS(dge, col = as.numeric(group))
```

## Export

```r
write.csv(topTags(qlf, n = Inf)$table, "de_results.csv")
```
