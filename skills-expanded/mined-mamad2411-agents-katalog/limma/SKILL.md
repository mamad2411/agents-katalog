---
name: limma
description: R limma package for microarray and RNA-seq. Use for linear models in differential expression.
---

# limma Package

Linear models for microarray and RNA-seq data.

## Microarray Workflow

```r
library(limma)

# Read data
targets <- readTargets("targets.txt")
eset <- read.maimages(targets, source = "agilent")

# Background correction
eset <- backgroundCorrect(eset, method = "normexp")

# Normalize
eset <- normalizeBetweenArrays(eset, method = "quantile")

# Average duplicates
eset <- avereps(eset, ID = eset$genes$ProbeName)
```

## RNA-seq with voom

```r
library(limma)
library(edgeR)

# Create DGEList
dge <- DGEList(counts = counts)
dge <- calcNormFactors(dge)

# Design matrix
design <- model.matrix(~0 + group)

# voom transformation
v <- voom(dge, design, plot = TRUE)

# Fit linear model
fit <- lmFit(v, design)

# Contrasts
contrast <- makeContrasts(Treatment - Control, levels = design)
fit2 <- contrasts.fit(fit, contrast)
fit2 <- eBayes(fit2)

# Results
topTable(fit2, coef = 1, n = Inf)
```

## Results

```r
# Top genes
results <- topTable(fit2, coef = 1, n = Inf)

# Significant genes
sig <- results[results$adj.P.Val < 0.05, ]

# Decide tests
dt <- decideTests(fit2)
summary(dt)
```

## Visualization

```r
# Volcano plot
volcanoplot(fit2, coef = 1, highlight = 10)

# MA plot
plotMA(fit2)

# Venn diagram
vennDiagram(dt)

# Heatmap of top genes
heatmap(v$E[rownames(sig)[1:50], ])
```

## Multiple Comparisons

```r
contrast <- makeContrasts(
  TrtA_vs_Ctrl = TreatmentA - Control,
  TrtB_vs_Ctrl = TreatmentB - Control,
  TrtA_vs_TrtB = TreatmentA - TreatmentB,
  levels = design
)

fit2 <- contrasts.fit(fit, contrast)
fit2 <- eBayes(fit2)

# Results for each contrast
topTable(fit2, coef = "TrtA_vs_Ctrl")
topTable(fit2, coef = "TrtB_vs_Ctrl")
```
